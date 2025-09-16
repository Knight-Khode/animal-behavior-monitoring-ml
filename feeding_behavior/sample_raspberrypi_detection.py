import cv2
from picamera2 import Picamera2, Preview
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
import time
import math
from datetime import datetime
import json
from libcamera import Transform
import paho.mqtt.client as mqtt

# MQTT setup
MQTT_SERVER = "192.168.137.66"
MQTT_PATH = "pigFarm/command/startcamera"
MQTT_PATH_STATUS = "pigFarm/command/cellstatus"

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 640)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
model = YOLO('/home/pi/Downloads/model3.pt')
class_list = ["Berkshire", "Duroc", "Landrace", "Pietrain", "Person"]
data = []

areaA = "00"

limits = [670, 83, 769, 117]
limits1 = [1041, 512, 1148, 545]
limits2 = [1149, 559, 1260, 589]
limits3 = [1276, 590, 1410, 624]

frame_count = 0
total_time = 0.0

# Video capture setup
capture_frames = False
bools = False
im = None

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    global capture_frames, bools
    print("\t\t*****__________" + msg.topic + "\t\t*****__________\t\t\t " + str(msg.payload))
    print(msg.payload.decode('utf-8'))
    print("Msg received. This listens to All")
    command = msg.payload.decode('utf-8')
    if command == "1":
        bools = True
        print("Started capturing frames")
    elif command == "0":
        bools = False
        print("Stopped capturing frames")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()

while True:
    if bools:
        im = picam2.capture_array()
        im = cv2.flip(im,-1)
        start_time = time.time()  # Capture start time

        results = model.predict(im)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")

        pigs_present = {"1": False}

        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]

            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            # Draw centroid
            cv2.circle(im, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            cv2.rectangle(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cvzone.putTextRect(im, f'{c}', (x1, y1), 1, 1)
            cv2.line(im, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)

            areaA = "44"

            if limits[0] < cx < limits[2] and cy <= limits[3]:
                cv2.circle(im, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                cv2.line(im, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)
                areaA = "1"
                class_id = d
                areaA = areaA + str(class_id)
                print(areaA)

        cv2.imshow("Camera", im)

        # Calculate time elapsed since start
        time_elapsed = time.time() - start_time

        # Delay for 5 seconds - time elapsed for image capture
        time.sleep(max(0, 0.1 - time_elapsed))

        if cv2.waitKey(1) == ord('q'):
            break

client.loop_stop()
cv2.destroyAllWindows()

