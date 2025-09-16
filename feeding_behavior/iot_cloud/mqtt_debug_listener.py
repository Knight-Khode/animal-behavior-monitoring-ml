#ok
import paho.mqtt.client as mqtt

MQTT_SERVER = "192.168.137.66"
#MQTT_SERVER = "192.168.137.1"
#MQTT_SERVER = "172.16.7.124"
MQTT_PATH = "pigFarm/status/debug"
 
# The callback when conected.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    client.subscribe(MQTT_PATH)
 
# Callback when message received
def on_message(client, userdata, msg):
    print("\t\t*****__________"+msg.topic+"\t\t*****__________\t\t\t "+str(msg.payload))
    print(msg.payload.decode('utf-8'))
    print ("Msg received. This listens to All")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

print("waiting for messages")
client.loop_forever()

#client.loop_start() #start the loop
#time.sleep(10) # wait
#client.loop_stop() #stop the loop
 
# Blocking call-  processes messages client.loop_forever()
