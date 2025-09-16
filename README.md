# animal-behavior-monitoring-ml
Non-intrusive animal behavior monitoring system using computer vision (YOLOv8 + OpenCV), embedded systems (ESP32, Raspberry Pi), and IoT (MQTT + Firebase). Tracks movement and feeding behavior of pigs with real-time detection, feed intake measurement, and cloud-based visualization.

# 🐖 Animal Behavior Monitoring (Computer Vision + Embedded Systems)

Non-intrusive animal behavior monitoring system using **computer vision (YOLOv8 + OpenCV)**, **embedded hardware (ESP32, Raspberry Pi)**, and **IoT (MQTT + Firebase)**.  
The system integrates **movement tracking** and **feeding behavior analysis** for pigs, enabling real-time detection, feed intake measurement, and cloud-based visualization.

---

## 📖 Overview
This project introduces a **low-cost, non-intrusive, real-time solution** for monitoring pig behavior.  
It combines:
- **Computer Vision** (YOLOv8n + OpenCV) for pig detection, breed classification, and behavior tracking.  
- **Embedded Systems** (ESP32 + load cells + ultrasonic sensors) for feed intake measurement.  
- **IoT** (MQTT + Firebase) for transmitting and visualizing behavior data.  

Two subsystems are implemented:  
1. **Movement Tracking** – using centroid and SORT algorithms.  
2. **Feeding Behavior Monitoring** – detecting feeding events, measuring duration, and calculating feed consumption.  

---

## ⚙️ System Architecture
- **Feed Weight Subsystem** – ESP32 + HX711 + load cells for feed intake measurement.  
- **Computer Vision Subsystem** – Raspberry Pi 4 + Pi Camera + YOLOv8n + OpenCV.  
- **End-User Subsystem** – Data aggregated and visualized in Firebase.  
<img width="1697" height="1000" alt="image" src="https://github.com/user-attachments/assets/0eb13824-a242-4827-9de7-ff0a081cf935" />

---

## 🚀 Features
- Detects and classifies pigs by breed (Landrace, Pietrain, Duroc, Berkshire).  
- Tracks individuals using **Marking, Centroid, and SORT algorithms**.  
- Measures feeding duration via **virtual line crossing** in OpenCV.  
- Calculates feed consumed per visit with load cells.  
- Publishes behavior data to the cloud (MQTT + Firebase).  
- Visualizes feeding patterns as time-series graphs.  

