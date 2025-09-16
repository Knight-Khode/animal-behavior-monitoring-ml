from ultralytics import YOLO
import cv2
import cvzone
import math
from datetime import datetime
import time
import json

# Load the YOLO model
model = YOLO("./yolomodel_320x320.pt")

# Class names
classNames = [
    "Berkshire",
    "Duroc",
    "Landrace",
    "Pietrain",
    "Person"
]

area_info = {"1": {"start_time": None, "last_pig_id": None},
             "2": {"start_time": None, "last_pig_id": None},
             "3": {"start_time": None, "last_pig_id": None},
             "4": {"start_time": None, "last_pig_id": None}}

# Define limits for different areas (these limits determine if pig enters or leaves feeding area
limits = [947, 458, 1044, 484]
limits1 = [1041, 512, 1148, 545]
limits2 = [1149, 559, 1260, 589]
limits3 = [1276, 590, 1410, 624]

# Tracking dictionaries
berkshire_centroids = {"prev": None, "count": 0}
duroc_centroids = {"prev": None, "count": 0}
landrace_centroids = {"prev": None, "count": 0}
pietrain_centroids = {"prev": None, "count": 0}

def update_movement_count(centroid, breed_centroids):
    if breed_centroids["prev"] is not None:
        prev_cx, prev_cy = breed_centroids["prev"]
        cx, cy = centroid
        if math.sqrt((cx - prev_cx) ** 2 + (cy - prev_cy) ** 2) > 5:  # Movement threshold
            breed_centroids["count"] += 1


    breed_centroids["prev"] = centroid

# Open the video capture
cap = cv2.VideoCapture("./video/camera_test.h264.mp4")
cap.set(3, 640)  # Set width
cap.set(4, 640)  # Set height

# Initialize FPS calculation
prev_time = time.time()

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
            # Grabbing bounding box coordinates for each pig
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            val = classNames[cls]
            pig_id = classNames[cls]

            # Grabbing bounding boxes center points
            cx, cy = x1 + w // 2, y1 + h // 2

            if cls == 0:
                update_movement_count((cx, cy), berkshire_centroids)
                cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

            if cls == 1:
                update_movement_count((cx, cy), duroc_centroids)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            if cls == 2:
                update_movement_count((cx, cy), landrace_centroids)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

            if cls == 3:
                update_movement_count((cx, cy), pietrain_centroids)
                cv2.circle(img, (cx, cy), 5, (150, 220, 100), cv2.FILLED)

            # Drawing bounding boxes, labels, and class probabilities on video frame
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=2,thickness=2)
            cvzone.cornerRect(img, (x1, y1, w, h))

            # Check if pig is in defined areas
            if limits[0] < cx < limits[2] and cy <= limits[3] and conf >= 0.5:
                pigs_present["1"] = True

            if limits1[0] < cx < limits1[2] and cy <= limits1[3] and conf >= 0.4:
                pigs_present["2"] = True

            if limits2[0] < cx < limits2[2] and cy <= limits2[3] and conf >= 0.4:
                pigs_present["3"] = True

            if limits3[0] < cx < limits3[2] and cy <= limits3[3] and conf >= 0.4:
                pigs_present["4"] = True

    # Display movement counts
    cvzone.putTextRect(img, f'Berkshire Movements: {berkshire_centroids["count"]}', (20, 400), scale=1.5, thickness=2)
    cvzone.putTextRect(img, f'Duroc Movements: {duroc_centroids["count"]}', (20, 450), scale=1.5, thickness=2)
    cvzone.putTextRect(img, f'Landrace Movements: {landrace_centroids["count"]}', (20, 500), scale=1.5, thickness=2)
    cvzone.putTextRect(img, f'Pietrain Movements: {pietrain_centroids["count"]}', (20, 550), scale=1.5, thickness=2)

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
