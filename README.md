# 🚦 Traffic Flow Analysis

This project implements a **vehicle detection, tracking, and counting system** using **YOLOv8 + ByteTrack**.  
It analyzes a video or live camera feed, detects vehicles, tracks their movement, and counts them when they cross predefined counting lines.

---

## ✨ Features
- 🔍 **Vehicle Detection** with YOLOv8 (pretrained COCO model)  
- 🆔 **Object Tracking** with ByteTrack for stable IDs  
- 📏 **Line Crossing Detection** for accurate counting  
- 📊 **CSV Export** (`output.csv`) with:
  - Vehicle ID  
  - Line number  
  - Frame index  
  - Timestamp  
- 🖥️ **Real-Time Visualization**:
  - Vehicle bounding boxes + IDs  
  - Counting lines  
  - Live counts per line  
  - FPS overlay  
- 📝 **Final Summary Screen** showing total vehicles per line  

---

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/AshwinPushpad/Traffic-Flow-Analysis
cd Traffic-Flow-Analysis
```

### 2. Create Virtual Environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate    # Linux/Mac
```


### 3. Download Test video from:
# https://drive.google.com/file/d/1_14ZzfBrVzl6QQZ-vtdEvSFbBBf8VxID/view?usp=sharing

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
If requirements.txt is not present, manually install:
```bash
pip install ultralytics opencv-python pandas numpy
```
Optional for GPU (CUDA 11.8):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## ▶️ Execution Instructions
Run on a Video File
```bash
python main.py --source video --path traffic.mp4
```
or
Run on a Webcam
```bash
python app.py --source cam --path 0
```
## 📊 Outputs
# Real-time Window:
Vehicles detected + tracked with unique IDs
Counting lines drawn
Live counts per line
FPS displayed

# CSV File (output.csv):
VehicleID,Line,Frame,Timestamp
3,1,45,1.52
7,2,123,3.98

# Final Summary (on window close):
=== FINAL SUMMARY ===
Line 1: 15 vehicles
Line 2: 22 vehicles
Line 3: 10 vehicles

### 📂 Project Structure
Traffic-Flow-Analysis/
│── app.py              # main program
│── README.md           # setup and usage guide
│── requirements.txt    # dependencies
│── traffic.mp4         # sample input video (not included, add your own)
