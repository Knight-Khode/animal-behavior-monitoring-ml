# 🐷 Feeding Behavior Monitoring

This folder contains the code and hardware implementation for the **feeding behavior monitoring system**.  
The system combines **computer vision, ultrasonic sensors, and load cells** to detect feeding events, measure feed intake, and log results in real time.

---
<img width="975" height="990" alt="image" src="https://github.com/user-attachments/assets/9bd70a85-a6e6-4b95-ad6c-4c46d902741f" />

## 📖 Subsystem Overview
1. **Ultrasonic Sensor Trigger**  
   - Detects object presence within 60 cm at the feeding area.  
   - Activates the computer vision pipeline when a pig enters.  

2. **Computer Vision (YOLOv8 + OpenCV)**  
   - Identifies the pig (by breed or marking).  
   - Detects entry into the feeding region using virtual lines.  
   - Measures feeding duration (entry → exit).  

3. **Feed Weight Subsystem (ESP32 + Load Cells)**  
   - Load cells measure feed weight before (FPA) and after feeding (FL).  
   - Feed consumed = **FPA – FL**.  
   - Data sent to Raspberry Pi via MQTT.  

---

## 📂 Files in This Folder
- `feeding_ComputerVison` → Main script integrating ultrasonic trigger, YOLOv8 inference, and feed weight measurement.  
- `esp32_integration/` → Encapsulation of ESP32 sensing and mqtt communication.  
- `feed_weight_esp32/` → ESP32 + HX711 code for load cell integration.  
- `ultrasonic_trigger/` → ESP32 ultrasonic sensor trigger code.  

---

## 🚀 How to Run
### 1. Flash ESP32  
- Upload `feed_weight_esp32/feed_weight.ino` to ESP32 for load cell readings.  
- Upload `ultrasonic_trigger/ultrasonic.ino` to ESP32 for ultrasonic detection.  

### 2. Run Vision Pipeline  
```bash
python feeding_pipeline.py
