🚦 Traffic Flow Analysis
This project implements a vehicle detection, tracking, and counting system using Computer Vision(OpenCV) and YOLOv8 + ByteTrack.
The system analyzes a video or live camera feed, detects vehicles, tracks their movement, and counts them when crossing defined lines (representing lanes).

📌 Features
1. Vehicle detection using pretrained YOLOv8 COCO model
2. Object tracking using ByteTrack for consistent IDs
3. Line crossing detection for robust vehicle counting

Real-time overlay with:
Vehicle bounding boxes + IDs
Counting lines + live counts per line
FPS (frames per second) display
CSV export with VehicleID, Line, Frame, Timestamp
Final summary screen showing total vehicles per lane

⚙️ Setup Instructions
1. Clone Repository
`git clone https://github.com/AshwinPushpad/Traffic-Flow-Analysis)`
`cd Traffic-Flow-Analysis`

2. Create Virtual Environment (recommended)
`python -m venv .venv`
`source .venv/bin/activate    # Linux/Mac`
`.venv\Scripts\activate       # Windows`

3. Install Dependencies
`pip install -r requirements.txt`

If requirements.txt is not present, manually install:
`pip install ultralytics opencv-python pandas numpy`


Optional for GPU (CUDA 11.8):
`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

▶️ Execution Instructions
Run on a Video File
`python main.py --source video --path traffic.mp4`
or
Run on a Webcam
`python app.py --source cam --path 0`

📊 Outputs
Real-time Window:
Vehicles detected + tracked with unique IDs
Counting lines drawn
Live counts per line
FPS displayed

CSV File (output.csv):
VehicleID,Line,Frame,Timestamp
3,1,45,1.52
7,2,123,3.98

Final Summary (on window close):
=== FINAL SUMMARY ===
Line 1: 15 vehicles
Line 2: 22 vehicles
Line 3: 10 vehicles

📂 Project Structure
Traffic-Flow-Analysis/
│── app.py              # main program
│── README.md           # setup and usage guide
│── requirements.txt    # dependencies
│── traffic.mp4         # sample input video (not included, add your own)
