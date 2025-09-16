#ok
import paho.mqtt.client as mqtt
import pyrebase

#MQTT_SERVER = "192.168.137.66"
#MQTT_SERVER = "172.16.7.124"
MQTT_SERVER = "192.168.137.1" 
MQTT_PATH = "pigFarm/foodWeight/duroc"

firebaseConfig = {
  'apiKey': "",
  'authDomain': "pigfarm-4b6ab.firebaseapp.com",
  'databaseURL': "https://pigfarm-4b6ab-default-rtdb.firebaseio.com",
  'projectId': "pigfarm-4b6ab",
  'storageBucket': "pigfarm-4b6ab.appspot.com",
  'messagingSenderId': "588943384528",
  'appId': "1:588943384528:web:6e0adbdda7632b2071a3d5",
  'measurementId': "G-2C1FHYK8V3"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# The callback when conected.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    client.subscribe(MQTT_PATH)
 
# Callback when message received
def on_message(client, userdata, msg):
    print("\t\t*****__________"+msg.topic+"\t\t*****__________\t\t\t "+str(msg.payload))
    print(msg.payload.decode('utf-8'))
    print ("Msg received. This listens to All")
    feedweight = msg.payload.decode('utf-8')
    data = {'Feed weight':float(feedweight)}
    db.child('FARM A').child("DUROC").push(data) #Posting feedweight to database

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

print("waiting for messages")
client.loop_forever()


