
---

# 🐖 Movement Tracking – Pig Behavior Monitoring

This module implements **real-time pig movement tracking** using **YOLOv8 detections** combined with two tracking strategies:

1. **Centroid Tracking** – lightweight and simple approach based on bounding box center points.
2. **SORT Tracking** – advanced tracker using Kalman Filters + Hungarian Algorithm for stable ID assignment.

Both methods allow pigs to be tracked across frames while monitoring their movement and feeding behavior.

---

## 📂 Files

* **`centroid_tracking.py`** → Tracks pigs by comparing bounding box centroids frame-to-frame.
* **`sort_tracking.py`** → Uses SORT (Simple Online and Realtime Tracking) for more robust and stable tracking.
* **`sort.py`** → Required helper module for SORT-based tracking (Kalman filter + association).

---

## ⚙️ How It Works

1. **Detection (YOLOv8):**

   * Each frame is processed using YOLO to detect pigs.
   * Outputs: bounding box, class (breed), confidence score.

2. **Tracking:**

   * **Centroid Tracker** → assigns IDs based on distance between centroids across frames.
   * **SORT Tracker** → predicts object motion with a Kalman Filter, assigns IDs using IoU-based matching.

3. **Feeding Area Monitoring:**

   * Pen is divided into **Areas A, B, C, D**.
   * For each pig, entry/exit is logged and **time spent in feeding zones** is calculated.

4. **Data Logging:**

   * Events are stored as structured JSON for integration with **IoT/Firebase dashboards**.

---

## 🚀 Usage

### Run Centroid Tracking

```bash
python centroid_tracking.py
```

### Run SORT Tracking

Make sure `sort.py` is in the same folder, then run:

```bash
python sort_tracking.py
```

---

## 📊 Comparison of Tracking Methods

| Feature           | Centroid Tracking 🟢     | SORT Tracking 🔵               |
| ----------------- | ------------------------ | ------------------------------ |
| **Speed**         | Faster, lightweight      | Slightly slower                |
| **Robustness**    | Struggles with occlusion | Handles occlusion better       |
| **ID Stability**  | IDs may switch           | IDs remain stable              |
| **Best Use Case** | Small herds, simple pens | Crowded pens, overlapping pigs |

---

## ✅ Applications

* Track **movement intensity** of different pig breeds.
* Measure **feeding behavior** (time spent in specific areas).
* Provide **real-time inputs** for farm management and IoT systems.

