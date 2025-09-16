
# IoT Integration – Pig Farm Monitoring 🐖🌐

This folder contains scripts that bridge the **farm sensors and edge devices** with the **Firebase cloud database** using **MQTT**. Each script either listens to sensor data (e.g., feed weight, temperature, humidity) or system status and then pushes it to the real-time Firebase database.

## 📂 Files Overview

* **`firebase_test.py`** → Test script for Firebase. Pushes dummy worker data to check connectivity.
* **`mqtt_debug_listener.py`** → Subscribes to `pigFarm/status/debug` to monitor debug/status messages.
* **`mqtt_cellstatus_listener.py`** → Subscribes to `pigFarm/command/cellstatus` for cell/command updates.
* **`mqtt_firebase_duroc.py`** → Subscribes to `pigFarm/foodWeight/duroc` and uploads feed weight data for **Duroc pigs** to Firebase.
* **`mqtt_firebase_berkshire.py`** → Subscribes to `pigFarm/foodWeight/berkshire` and uploads feed weight data for **Berkshire pigs** to Firebase.
* **`mqtt_firebase_pietrain.py`** → Subscribes to `pigFarm/foodWeight/pietrain` and uploads feed weight data for **Pietrain pigs** to Firebase.
* **`mqtt_firebase_landrace.py`** → Subscribes to `pigFarm/foodWeight/landrace` and uploads feed weight data for **Landrace pigs** to Firebase.
* **`mqtt_firebase_temp.py`** → Subscribes to `pigFarm/status/temperature` and uploads **temperature readings** to Firebase.
* **`mqtt_firebase_humidity.py`** → Subscribes to `pigFarm/status/humidity` and uploads **humidity readings** to Firebase.

---

## 🔗 How It Works

1. **Edge devices (ESP32, sensors, weight modules, etc.)** publish readings to **MQTT topics**.
2. **These scripts** (Python + `paho-mqtt` + `pyrebase`) listen to those topics.
3. On message arrival, they parse the data and **push structured logs into Firebase**.
4. Firebase becomes the central hub for feeding, movement, and environmental monitoring data.

---

## ⚙️ Requirements

* Python 3.x
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [pyrebase4](https://pypi.org/project/Pyrebase4/)

Install dependencies:

```bash
pip install paho-mqtt pyrebase4
```

---

## 🚀 Running the Scripts

Each script can be run individually depending on the sensor/topic you want to monitor. For example:

```bash
python mqtt_firebase_duroc.py
```

This will listen to the feed weight MQTT topic for Duroc pigs and automatically push updates into Firebase.

---

## 🌍 System Role

These IoT integration scripts ensure that:

* **Vision-based behavior tracking** (feeding & movement)
* **Sensor-based measurements** (feed weight, temp, humidity)

are all synchronized into **one central database** for further analysis, visualization, and decision-making.


