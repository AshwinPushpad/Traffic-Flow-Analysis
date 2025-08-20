import cv2
import json

current_points = []
completed_lines = []
frame = None

def click_event(event, x, y, flags, param):
    global current_points, completed_lines, frame
    
    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append((x, y))
        
        cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)
        cv2.putText(frame, str(len(current_points)), (x+10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        if len(current_points) == 2:
            pt1, pt2 = current_points
            cv2.line(frame, pt1, pt2, (0, 255, 255), 3)
            
            line_id = len(completed_lines) + 1
            completed_lines.append({
                "id": line_id,
                "start": pt1,
                "end": pt2
            })
            
            mid_x = (pt1[0] + pt2[0]) // 2
            mid_y = (pt1[1] + pt2[1]) // 2
            cv2.putText(frame, f"Line {line_id}", (mid_x-30, mid_y-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            print(f"Line {line_id} created with coords: {pt1} to {pt2}")

            current_points = []
        
        cv2.imshow("Frame", frame)

def draw_existing_lines(frame):
    """Redraw all existing lines"""
    global completed_lines
    for line in completed_lines:
        pt1, pt2 = line["start"], line["end"]
        cv2.line(frame, pt1, pt2, (0, 255, 255), 3)
        
        mid_x = (pt1[0] + pt2[0]) // 2
        mid_y = (pt1[1] + pt2[1]) // 2
        cv2.putText(frame, f"Line {line['id']}", (mid_x-30, mid_y-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def reset_current_line():
    """Reset the current line being drawn"""
    global current_points, frame
    current_points = []
    ret, fresh_frame = cv2.VideoCapture("traffic.mp4").read()
    if ret:
        frame = fresh_frame.copy()
        draw_existing_lines(frame)
        cv2.imshow("Frame", frame)

def clear_all_lines():
    """Clear all lines"""
    global completed_lines, current_points, frame
    completed_lines = []
    current_points = []
    ret, fresh_frame = cv2.VideoCapture("traffic.mp4").read()
    if ret:
        frame = fresh_frame.copy()
        cv2.imshow("Frame", frame)

def main(video_path="traffic.mp4", save_file="lines.txt"):
    global frame, completed_lines
    
    print("LINE MARKER TOOL")
    print("Click TWO points to create each counting line")
    print("Controls:")
    print("• Left Click: Place point (2 points = 1 line)")
    print("• ENTER: Save all lines and exit")
    print("• 'R': Reset current line")
    print("• 'C': Clear all lines")
    print("• 'ESC': Exit without saving")
    
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    
    if not ret:
        print("Could not read video")
        return
    
    cap.release()
    
    original_frame = frame.copy()
    
    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", click_event)
    
    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == 13:   # ENTER key =13
            if completed_lines:
                print(f"\nCreated {len(completed_lines)} counting lines")
                
                line_tuples = {}
                for line in completed_lines:
                    line_tuples[line['id']]=((line["start"], line["end"]))
                
                with open(save_file, "a") as f:
                    f.write(str(line_tuples))
                    f.write("\n")
                
                print(f"Saved to {save_file}")
                print(f"Line coordinates: {line_tuples}")
                
                break
            else:
                print("No lines created. Create at least one line before saving.")
                
        elif key == ord('r') or key == ord('R'):
            if current_points:
                print("Resetting current line...")
                reset_current_line()
            else:
                print("No current line to reset.")
                
        elif key == ord('c') or key == ord('C'):
            print("Clearing all lines...")
            clear_all_lines()
            
        elif key == 27:
            print("Exiting without saving")
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
