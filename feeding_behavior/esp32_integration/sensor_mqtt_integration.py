#include <WiFi.h>  
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <Arduino.h>
#include "HX711.h"
#include "soc/rtc.h"
#include "DHT.h"

//Constants for program
#define CELL1_DT_PIN 36
#define CELL1_SCK_PIN 21
#define ULTRA_ECHO_CELL1 39
#define ULTRA_TRIG_CELL1 19
#define DHTPINA 32
#define DHTPINB 33 
#define DHTTYPEA DHT22
#define DHTTYPEB DHT11
DHT dhtA(DHTPINA, DHTTYPEA);
DHT dhtB(DHTPINB, DHTTYPEB);


//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define SETPOINT_CM 60

//---- WiFi settings
const char* ssid = "";
const char* password = "";

//---- MQTT Broker settings
const char* mqtt_server = "192.168.137.66"; // replace with your broker url
const int mqtt_port =1883;
WiFiClient espClient;
PubSubClient client(espClient);
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

//Variable to hold load cell reading and MQTT topic
HX711 penB;
float sensor1;
const char* berkshire_topic= "pigFarm/foodWeight/berkshire";
const char* landrace_topic= "pigFarm/foodWeight/landrace";
const char* pietrain_topic= "pigFarm/foodWeight/pietrain";
const char* duroc_topic= "pigFarm/foodWeight/duroc";
const char* temp_topic= "pigFarm/status/temperature";
const char* hum_topic= "pigFarm/status/humidity";
const char* debug_topic= "pigFarm/status/debug";

//Variable to hold command topic and command
int cell1_status =0;
const char* cell_topic="pigFarm/command/cellstatus";
const char* camera_topic="pigFarm/command/startcamera";

//Variable to store camera status
int camera_status = 0;
int duration;
int distanceCM;

//Variable to hold previous Millis
unsigned long lastMsg = 0;

//Variable to hold pig type, pen status and load cell weight
char penA_status;
char inA;
char penA_pigType;
char cell1_pig; 
int penA_weight_old;
int penA_weight_new;
int done = 0;



void setup() {
  Serial.begin(115200);
  Serial.println("Setting up");
  
  setup_wifi();

  //Initializing load cells 
  pinMode(CELL1_DT_PIN, INPUT);   
  pinMode(CELL1_SCK_PIN, OUTPUT);

  //Initializing ultrasonic sensors
  pinMode(ULTRA_ECHO_CELL1, INPUT);
  pinMode(ULTRA_TRIG_CELL1, OUTPUT);
  
  //WEIGHT SENSOR INITIALIZATION
  rtc_cpu_freq_config_t config;
  rtc_clk_cpu_freq_get_config(&config);
  rtc_clk_cpu_freq_mhz_to_config(80, &config);
  rtc_clk_cpu_freq_set_config_fast(&config);

  Serial.println("Initializing the scale");
  penB.begin(CELL1_DT_PIN, CELL1_SCK_PIN);
  penB.set_scale(218.42);
  penB.tare();  

  //DHT22 initialization
  dhtA.begin();
  dhtB.begin();

  //MQTT initialization
  client.setServer(mqtt_server, 1883 );//mqtt_port
  client.setCallback(callback); //Call back is called when a message comes in
}

void loop() {
  unsigned long now = millis(); 
  if (!client.connected()) reconnect();
  client.loop();

  //GETTING DISTANCE OF ULTRASONIC SENSOR FOR CELL1
  // Clears the trigPin
  digitalWrite(ULTRA_TRIG_CELL1, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(ULTRA_TRIG_CELL1, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRA_TRIG_CELL1, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ULTRA_ECHO_CELL1, HIGH);
  // Calculate the distance
  distanceCM = duration * SOUND_SPEED/2;
  publishMessage(debug_topic,"DISTANCE CM:" + String(distanceCM),true);

  //CONDITION TO TRIGGER ML CAPTURE
  if (distanceCM<=SETPOINT_CM){
    publishMessage(camera_topic,"1",true);  // To start ML code
    inA = '1'; //Pen A is occupied
  }
  else{
    publishMessage(camera_topic,"0",true); //To stop ML code
    }
  
  //Condition to check if penA is occupied in cell1 and a pig is present
  if (inA == '1' && done == 0){
    penB.power_up();
    penA_weight_old = penB.get_units(20); //Get initial weight of feed before pig enters
    penB.power_down();    // put the ADC in sleep mode
    cell1_pig = penA_pigType; //Store type of pig in pen area
    done = 1;
  }

  //Condition to read the feedweight after pig leaves
  if(inA == '1' && done == 1 && (distanceCM>=SETPOINT_CM)){
    penB.power_up();
    penA_weight_new = penB.get_units(20); //Get final weight of feed after pig enters
    penB.power_down();
    inA = '0'; //PenA is not occupied
    done = 0;
    int feedWeight = abs(penA_weight_old - penA_weight_new);
    Serial.print("Weight of feed eaten = ");
    Serial.println(feedWeight);

    //IF PIG DETECTED IS BERKSHIRE
    if(penA_pigType == '0'){
      publishMessage(berkshire_topic,String(feedWeight),true);  //Publishing berkshire feedweight to Raspberry pi
    }
    //IF PIG DETECTED IS DUROC
    else if(penA_pigType == '1'){
      publishMessage(duroc_topic,String(feedWeight),true);  //Publishing duroc feedweight to Raspberry pi
    }
    //IF PIG DETECTED IS LANDRACE
    else if(penA_pigType == '2'){
      publishMessage(landrace_topic,String(feedWeight),true);  //Publishing landrace feedweight to Raspberry pi
    }
    //IF PIG DETECTED IS PIETRAIN
    else if(penA_pigType == '3'){
      publishMessage(pietrain_topic,String(feedWeight),true);  //Publishing pietrain feedweight to Raspberry pi
    }
  }

  if (now - lastMsg > 10000) {
    lastMsg = now;
    float h = dhtA.readHumidity();
    float h1 = dhtB.readHumidity();
    float t = dhtA.readTemperature();
    float t1 = dhtB.readTemperature();
    float h_avg = (h + h1)/2;
    float t_avg = (t + t1)/2;

    //Publishing temperature readings
    publishMessage(temp_topic,String(t),true);  //Publishing temperature to Rasberry Pi

    //Publishing humidity readings
    publishMessage(hum_topic,String(h),true);  //Publishing humidity to Rasberry Pi
  }
  

  //For ultrasonic sensor
  delay(250);
}

//Function to set up WiFi
void setup_wifi() {
  delay(10);
  Serial.print("\nConnecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  //=======
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  //=======
  randomSeed(micros());
  Serial.println("\nWiFi connected\nIP address: ");
  Serial.println(WiFi.localIP());
}


//Function to reconnect to WiFi
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";   // Create a random client ID
    clientId += String(random(0xffff), HEX);  //you could make this static
    // Attempt to connect
    if (client.connect(clientId.c_str())){//, mqtt_username, mqtt_password)) {
      Serial.println("connected");
      client.subscribe(cell_topic);   // subscribe the topics here
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");   // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


// This void is called every time we have a message from the broker
void callback(char* topic, byte* payload, unsigned int length) {
  String incomingMessage = "";
  for (int i = 0; i < length; i++) incomingMessage+=(char)payload[i];
  Serial.println("Message arrived ["+String(topic)+"]: " + incomingMessage);

  //--- check the incomming message
  //TOPIC FOR CELL OCCUPANCY
  if(strcmp(topic,cell_topic) == 0){
    penA_status = incomingMessage.charAt(0);
    penA_pigType = incomingMessage.charAt(1);
    //Serial.println("PenA status: "+penA_status);
    Serial.println("PenA Pig Type: "+penA_pigType);
    publishMessage(debug_topic,"PIG TYPE:" + String(penA_pigType),true);
  }
}


//Publising data as string
void publishMessage(const char* topic, String payload , boolean retained){
  if (client.publish(topic, payload.c_str(), true))
      Serial. println("Message publised ["+String(topic)+"]: "+payload);
}
