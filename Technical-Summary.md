# 📌 Technical Summary

## 🔹 Approach
- Used **YOLOv8 (Ultralytics)** pretrained on COCO dataset to detect vehicles (`car`, `motorbike`, `bus`, `truck`).  
- Integrated **ByteTrack** (built-in with YOLOv8) for consistent object tracking across frames.  
- Defined **counting lines** in the frame; vehicles are counted when their trajectory crosses a line.  
- Exported results to **CSV** with `VehicleID`, `Line`, `Frame`, `Timestamp`.  
- Provided **real-time visualization** with bounding boxes, IDs, counts, FPS, and a final summary screen.  

---

## 🔹 Challenges
1. **Multiple IDs for same vehicle**  
   - With SORT, vehicles received new IDs as they moved closer to the camera (due to scale and perspective changes).  

2. **Inaccurate polygon-based lane detection**  
   - Using lane polygons caused flickering: vehicles entered/exited polygons multiple times due to detection jitter.  

3. **Wide-area footage**  
   - Vehicles appeared small far away and large closer to the camera, making consistent detection and counting harder.  

---

## 🔹 Solutions
- Replaced **SORT** with **ByteTrack**, improving ID consistency in wide-perspective videos.  
- Switched from **polygon inclusion** to **line-crossing detection**, ensuring each vehicle is only counted once per lane.  
- Tuned tracker parameters (IoU thresholds, persistence) to handle detection jitter.  
- Added **real-time overlays** (counts, FPS, bounding boxes) for live verification and smooth user experience.  

---
