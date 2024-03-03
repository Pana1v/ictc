from collections import defaultdict
import cv2
import numpy as np
import requests
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('./Models/yolov8n.pt')

# IP camera URL
url = "http://100.93.76.64:8080/shot.jpg"

# Store the track history
track_history = defaultdict(lambda: [])

# Skip frames for faster processing
skip_frames = 5

# Differential drive parameters
max_speed = 255
mid_point = 416  # Adjust based on your image size
speed_factor = max_speed / mid_point

# Loop through the video frames
while True:
    try:
        # Fetching image from the IP camera
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, imgsz=416, persist=True, conf=0.2, iou=0.2)  # Adjust as needed

        # Check if there are detections
        if results and results.xyxy is not None and len(results.xyxy) > 0:
            # Get the center coordinates of the bounding box for the first detected person
            box = results.xyxy[0]  # Assuming the first box corresponds to "person"
            center_x = (box[0] + box[2]) / 2

            # Calculate speeds for left and right motors
            right_speed = max_speed - int((center_x - mid_point) * speed_factor)
            left_speed = max_speed + int((center_x - mid_point) * speed_factor)

            # Print the left and right speeds
            print(f"Left Speed: {left_speed}, Right Speed: {right_speed}")

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Break the loop if 'q' key is pressed
            break
        elif key == ord('a'):  # Left arrow key
            # Skip frames backward
            for _ in range(skip_frames):
                img_resp = requests.get(url)
        elif key == ord('d'):  # Right arrow key
            # Skip frames forward
            pass

    except Exception as e:
        print(f"Error: {e}")

# Close the display window
cv2.destroyAllWindows()
