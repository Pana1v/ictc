import torch
from ultralytics import YOLO
import cv2
import numpy as np
import imutils
import requests

# Checking if CUDA is available
cuda_available = torch.cuda.is_available()

# Loading YOLOv8 model from the specified checkpoint file
model = YOLO('./Models/yolov8n.pt')

# Move the model to GPU if CUDA is available
if cuda_available:
    model = model.cuda()
# Differential drive parameters
max_speed = 255
mid_point = 416  # Adjust based on your image size
speed_factor = max_speed / mid_point

# Function to calculate speeds for left and right motors
def calculate_speeds(center_x):
    # Calculate speeds for left and right motors
    right_speed = max_speed - int((center_x - mid_point) * speed_factor)
    left_speed = max_speed + int((center_x - mid_point) * speed_factor)
    left_speed/=3
    right_speed/=3
    # Print the left and right speeds
    print(f"Left Speed: {left_speed}, Right Speed: {right_speed}")

# Replace the below URL with your own IP provided by the IP WEBCAM APP.
# Make sure to add "/shot.jpg" at last.
url = "http://10.38.0.178:8080/shot.jpg"
while True:
    try:
        # Fetching image from the IP camera
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=800, height=600)

        # Move the image to GPU if CUDA is available
        if cuda_available:
            img = torch.from_numpy(img).cuda()

        # Make predictions with the YOLOv8 model
        results = model.predict(img, imgsz=400, conf=0.07, iou=0.25)
        results = results[0]

        # Move the results to CPU for further processing
        if cuda_available:
            results.xyxy = results.xyxy.cpu()

        # Draw bounding boxes on the frame and display info
        for i, box in enumerate(results.boxes):     
            tensor = box.xyxy[0]
            x1, y1, x2, y2 = int(tensor[0].item()), int(tensor[1].item()), int(tensor[2].item()), int(tensor[3].item())

            # Draw bounding box rectangle on the frame
            # use orange for rectangle
            # if class is not person

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            
            # Calculate center coordinates
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            # Get class index, name, and confidence
            class_index = int(box.cls[0].item())
            class_label = model.names[class_index] if 0 <= class_index < len(model.names) else f"Class {class_index + 1}"
            confidence = round(float(box.conf[0].item()), 2)

            # Display info in the frame
            # info_text = f"Object {i + 1}: {class_label} - Confidence: {confidence}\n Center: ({center_x}, {center_y})"
            info_text = f"Object {i + 1}: {class_label}"
            # use green for text
            # cv2.putText(img, info_text, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            if class_label == 'person':
                # cv2.putText(img, info_text, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                calculate_speeds(center_x)
                cv2.putText(img, info_text, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
        # Display the frame
        cv2.imshow('YOLOv8 IP Camera Inference', img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")

# Close the OpenCV window
cv2.destroyAllWindows()
