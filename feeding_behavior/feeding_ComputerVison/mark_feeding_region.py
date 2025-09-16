from ultralytics import YOLO
import cv2
import cvzone
import math
from datetime import datetime
import time
import json

# Load the YOLO model
model = YOLO("./model3.pt")

areaA="00";
areaB="00";
berk=0;
pet=0;
duroc=0;
land=0;

# Class names
classNames = [
    "Berkshire",
    "Duroc",
    "Landrace",
    "Pietrain"
]

area_info = {"1": {"start_time": None, "last_pig_id": None},
             "2": {"start_time": None, "last_pig_id": None},
             "3": {"start_time": None, "last_pig_id": None},
             "4": {"start_time": None, "last_pig_id": None}}

occupied=[0,0,0,0]

# Define limits for different areas (these limits determine if pig enters or leaves feeding area
limits = [947, 458, 1044, 484]
limits1 = [1041, 512, 1148, 545]
limits2 = [1149, 559, 1260, 589]
limits3 = [1276, 590, 1410, 624]
data=[]
areaData2=[]
# Open the video capture
cap = cv2.VideoCapture("./video/camera_test.h264.mp4")
cap.set(3, 640)  # Set width
cap.set(4, 640)  # Set height

# Initialize FPS calculation
prev_time = time.time()
cls=""
elapsed_time =0

while True:
    success, img = cap.read()
    if not success:
        break

    # YOLO model inference
    results = model(img, stream=True)

    pigs_present = {"1": False, "2": False, "3": False, "4": False}
    for r in results:
        boxes = r.boxes

        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
        cv2.line(img, (limits1[0], limits1[1]), (limits1[2], limits1[3]), (0, 0, 255), 5)
        cv2.line(img, (limits2[0], limits2[1]), (limits2[2], limits2[3]), (0, 0, 255), 5)
        cv2.line(img, (limits3[0], limits3[1]), (limits3[2], limits3[3]), (0, 0, 255), 5)

        cvzone.putTextRect(img, "Area A:" , (20,110),scale=2,thickness=2)
        cvzone.putTextRect(img, "Area B:", (20,170),scale=2,thickness=2)
        cvzone.putTextRect(img, "Area C:", (20,240),scale=2,thickness=2)
        cvzone.putTextRect(img, "Area D:", (20,310),scale=2,thickness=2)

        cvzone.putTextRect(img, "Area A", (1040, 225),scale=1.5,thickness=2)
        cvzone.putTextRect(img, "Area B", (1170, 241), scale=1.5, thickness=2)
        cvzone.putTextRect(img, "Area C", (1290, 263), scale=1.5, thickness=2)
        cvzone.putTextRect(img, "Area D", (1400, 281), scale=1.5, thickness=2)


        for box in boxes:
            #Grabbing bounding box coordinates for each pig
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            val = classNames[cls]
            pig_id = classNames[cls]

            #Grabbing bounding boxes center points
            cx, cy = x1 + w // 2, y1 + h // 2

            #Drawing center points, bounding boxes, labels and class probabilities on video frame
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            #cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=2,thickness=2)
            #cvzone.cornerRect(img, (x1, y1, w, h))


            #crossed_line function grabs identity of pig and feeding area occupied
            def crossed_line(cls, area):
                area = area
                areaData = {"Area": area, "Pig_ID": cls}
                areaData2.append((areaData))

            #conditon to check pig presence in first feeding Area
            if limits[0] < cx < limits[2] and cy <= limits[3] and conf >= 0.5:
                crossed_line(cls, "1")
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)
                cv2.putText(img, classNames[cls], (180, 100),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                cvzone.putTextRect(img, "Area A", (1040, 225), scale=1.5, thickness=2, colorR=(0,255,0))
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                pigs_present["1"] = True

            #conditon to check pig presence in 2nd feeding Area
            if limits1[0] < cx < limits1[2] and cy <= limits1[3] and conf >= 0.4:
                crossed_line(cls, "2")
                cv2.line(img, (limits1[0], limits1[1]), (limits1[2], limits1[3]), (0, 255, 0), 5)
                cv2.putText(img, classNames[cls], (180, 170),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                cvzone.putTextRect(img, "Area B", (1170, 241), scale=1.5, thickness=2,colorR=(0,255,0))
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                pigs_present["2"] = True

            #conditon to check pig presence in third feeding Area
            if limits2[0] < cx < limits2[2] and cy <= limits2[3] and conf >= 0.4:
                crossed_line(cls, "3")
                cv2.line(img, (limits2[0], limits2[1]), (limits2[2], limits2[3]), (0, 255, 0), 5)
                cv2.putText(img, classNames[cls], (180, 240),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                cvzone.putTextRect(img, "Area C", (1290, 263), scale=1.5, thickness=2,colorR=(0,255,0))
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                pigs_present["3"] = True

            # condition to check pig presence in last feeding Area
            if limits3[0] < cx < limits3[2] and cy <= limits3[3] and conf >= 0.4:
                crossed_line(cls, "4")
                cv2.line(img, (limits3[0], limits3[1]), (limits3[2], limits3[3]), (0, 255, 0), 5)
                cv2.putText(img, classNames[cls], (180, 310),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                cvzone.putTextRect(img, "Area D", (1400, 281), scale=1.5, thickness=2,colorR=(0,255,0))
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                pigs_present["4"] = True

        # Check if pigs are present in each area and update timers
    for area, present in pigs_present.items():
        if present:
            if area_info[area]["start_time"] is None:
                area_info[area]["start_time"] = time.time()
                area_info[area]["last_pig_id"] = pig_id  # Store the last pig ID when a pig enters
        else:
            # Pig has left the area, stop the timer and store the last value
            if area_info[area]["start_time"] is not None:
                elapsed_time = time.time() - area_info[area]["start_time"]
                last_pig_id = area_info[area]["last_pig_id"]
                area_data = {"Area": area, "Last Pig ID": last_pig_id, "Elapsed Time": elapsed_time}
                data.append(area_data)
                area_info[area]["start_time"] = None
                area_info[area]["last_pig_id"] = None
                print(area_data)

        # Display elapsed time for each area
    for area, info in area_info.items():
        if info["start_time"] is not None:
            elapsed_time = time.time() - info["start_time"]
            cv2.putText(img, f"{elapsed_time:.2f} sec", (330, 30 + 70 * int(area)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(int(area))

    #conditon to post ML inferences to ESP32
    if len(areaData2) != 0:
        data.append(areaData2)
        data2 = data[0]  # Extract the first (and only) list of dictionaries from data
        areaData2 = []
        arr_json = json.dumps(data)
        print(arr_json)
        print(type(data2))  # Check the type of data2, should be a list of dictionaries

        # Initialize variables to store results
        areaA = "44"
        areaB = "44"

        # Iterate over the list of dictionaries
        for i in data2:
            # Check if i is a dictionary with expected keys
            if isinstance(i, dict) and "Area" in i and "Pig_ID" in i:
                if i["Area"] == '1':
                    areaA = "1" + str(i["Pig_ID"])
                elif i["Area"] == '2':
                    areaB = "1" + str(i["Pig_ID"])

        # Print the results
        print(areaA)
        print(areaB)

        # Reset data for the next iteration
        data = []
        data2 = []






    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS on the image
    cv2.putText(img, f'FPS: {fps:.2f}', (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
