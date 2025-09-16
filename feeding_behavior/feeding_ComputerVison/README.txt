# 🐷 Feeding Area Marking & Tracking

This module combines two scripts:  
1. **click_event.py** → A utility script to capture image coordinates for defining feeding stall boundaries.  
2. **feeding_area_tracking.py** → The main YOLOv8-based pipeline for tracking pigs inside feeding zones, logging feeding duration, and exporting data.

---

## 📖 Workflow

1. **Mark Feeding Areas**
   - Run `click_event.py` to load an image frame from the pig pen camera.  
   - Click on key points (corners of stalls).  
   - The script prints `(x, y)` coordinates, which you can paste into the `limits`, `limits1`, `limits2`, `limits3` variables in `feeding_area_tracking.py`.  

2. **Track Feeding Behavior**
   - Run `feeding_area_tracking.py`.  
   - YOLOv8 detects pigs and assigns them to Areas A–D.  
   - The system:
     - Highlights stalls red (empty) or green (occupied).  
     - Tracks entry/exit and calculates elapsed feeding time.  
     - Logs pig ID, area, and feeding duration in JSON format.  
     - Displays FPS and real-time overlays on the video.  

---

## 📂 Files
- `click_event.py` → Coordinate marking tool.  
- `feeding_area_tracking.py` → Feeding duration + area occupancy tracking pipeline.  

---

## 🚀 How to Use

### Step 1: Get Feeding Stall Coordinates
```bash
python click_event.py
