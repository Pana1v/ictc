from ultralytics import YOLO
import cv2
#Function to merge 2 dictionaries
def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

#The 2 Models
model = YOLO("traffic.pt")#To place filename here
model2 = YOLO("yolov8n.pt")

#Open a new window which captures the image
cap = cv2.VideoCapture(0)
 # Read a frame from the webcam
ret, frame = cap.read()
#Get the class names from the model names
class_names = merge_two_dicts(model.names,model2.names)
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Make predictions with the YOLOv8 model
    results = model.predict(frame, imgsz=224, conf=0.2, iou=0.45) 
    results2 = model2.predict(frame, imgsz=224, conf=0.2, iou=0.45)
    results = results[0]
    results2 = results2[0]

    #Reading from our first model
    # Draw bounding boxes on the frame and display info
    for i, box in enumerate(results.boxes):
        tensor = box.xyxy[0]
        x1, y1, x2, y2 = int(tensor[0].item()), int(tensor[1].item()), int(tensor[2].item()), int(tensor[3].item())

        # Draw bounding box rectangle on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate center coordinates
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Get class index, name, and confidence
        class_index = int(box.cls[0].item())
        class_label = class_names[class_index] if 0 <= class_index < len(class_names) else f"Class {class_index + 1}"
        confidence = round(float(box.conf[0].item()), 2)

        # Display info in the frame
        info_text = f"Object {i + 1}: {class_label} - Confidence: {confidence}\n Center: ({center_x}, {center_y})"
        cv2.putText(frame, info_text, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    #Reading from our 2nd Model
    for i, box in enumerate(results2.boxes):
        tensor = box.xyxy[0]
        x1, y1, x2, y2 = int(tensor[0].item()), int(tensor[1].item()), int(tensor[2].item()), int(tensor[3].item())

        # Draw bounding box rectangle on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate center coordinates
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Get class index, name, and confidence
        class_index = int(box.cls[0].item())
        class_label = class_names[class_index] if 0 <= class_index < len(class_names) else f"Class {class_index + 1}"
        confidence = round(float(box.conf[0].item()), 2)

        # Display info in the frame
        info_text = f"Object {i + 1}: {class_label} - Confidence: {confidence}\n Center: ({center_x}, {center_y})"
        cv2.putText(frame, info_text, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow('YOLOv8 Webcam Inference', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

        