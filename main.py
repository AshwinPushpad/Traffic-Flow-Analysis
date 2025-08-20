import cv2
import time
import numpy as np
import pandas as pd
from ultralytics import YOLO
import argparse

# Vehicle classes from COCO dataset
VEHICLE_IDS = {2, 3, 5, 7}  # car, motorbike, bus, truck

def get_source(source_type, path_or_index):
    if source_type == "video":
        return cv2.VideoCapture(path_or_index)
    elif source_type == "cam":
        return cv2.VideoCapture(int(path_or_index))
    else:
        raise ValueError("Source must be 'video' or 'cam'")

COUNTING_LINES = {
    1: ((131, 418), (496, 445)),
    2: ((531, 451), (723, 454)),
    3: ((952, 440), (1156, 517))
}

def draw_counting_lines(frame):
    for lid, (pt1, pt2) in COUNTING_LINES.items():
        cv2.line(frame, pt1, pt2, (0, 255, 255), 3)
        mid_x = (pt1[0] + pt2[0]) // 2
        mid_y = (pt1[1] + pt2[1]) // 2
        cv2.putText(frame, f"Line {lid}", (mid_x-30, mid_y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

def line_intersection(p1, p2, p3, p4):
    """Check if lines intersects """
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def check_line_crossing(prev_pos, curr_pos, line_id):
    """Check if vehicle crosses a counting line"""
    if prev_pos is None or curr_pos is None:
        return False
    line_start, line_end = COUNTING_LINES[line_id]
    return line_intersection(prev_pos, curr_pos, line_start, line_end)

def main(source_type, path_or_index, output_csv="output.csv"):
    cap = get_source(source_type, path_or_index)
    if not cap.isOpened():
        print("Could not open source")
        return

    model = YOLO("yolov8n.pt")
    device = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
    model.to(device)

    counted = {1: set(), 2: set(), 3: set()}
    vehicle_positions = {}
    records = []
    frame_idx = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

        draw_counting_lines(frame)

        if results[0].boxes.id is not None:
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, tid, cls in zip(boxes, ids, classes):
                if cls in VEHICLE_IDS:
                    x1, y1, x2, y2 = box
                    cx, cy = (x1+x2)//2, (y1+y2)//2
                    curr_pos = (int(cx), int(cy))

                    prev_pos = vehicle_positions.get(tid, None)

                    for line_id in COUNTING_LINES.keys():
                        if check_line_crossing(prev_pos, curr_pos, line_id):
                            if tid not in counted[line_id]:
                                counted[line_id].add(tid)
                                records.append([tid, line_id, frame_idx, time.time()-start_time])
                                cv2.putText(frame, f"Crossed Line {line_id}", (x1, y1-30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

                    vehicle_positions[tid] = curr_pos

                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.putText(frame, f"ID {tid}", (x1,y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        # live counts
        y_offset = 40
        for lid in sorted(counted):
            cv2.putText(frame, f"Line {lid}: {len(counted[lid])}",
                        (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0,255,0), 2)
            y_offset += 30

        # FPS
        elapsed = time.time()-start_time
        fps = (frame_idx+1)/elapsed if elapsed>0 else 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (20, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.imshow("Traffic Flow", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        frame_idx += 1

    # for saving to CSV
    df = pd.DataFrame(records, columns=["VehicleID","Lane","Frame","Timestamp"])
    df.to_csv(output_csv, index=False)

    # final summary frame
    summary = np.zeros_like(frame)
    cv2.putText(summary, "========== FINAL SUMMARY ==========", (50,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 2)
    y = 120
    for lid, ids in counted.items():
        cv2.putText(summary, f"Line {lid}: {len(ids)} vehicles",
                    (50,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
        y += 50

    cv2.imshow("Traffic Flow", summary)
    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, choices=["video","cam"], default="video")
    parser.add_argument("--path", type=str, default="traffic.mp4")
    args = parser.parse_args()

    main(args.source, args.path)
