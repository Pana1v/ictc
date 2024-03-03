import cv2
import numpy as np
import requests
import concurrent.futures
import socket
import websocket
import json

# IP camera URL
url = "http://100.123.114.14:8080/shot.jpg"

# Display window size
window_size = (640, 360)

# Receiver settings for speed transmission
speed_host = '192.168.120.232'
speed_port = 80

# WebSocket server address
websocket_server_address = 'ws://192.168.120.232/ws'

# Create a socket object for speed transmission
speed_sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to process each frame
def process_frame(frame, ws):
    # Convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Erode to eliminate noise, Dilate to restore eroded parts of the image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in frame
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of the largest contour and calculate speeds for both motors
    if len(contours) > 0:
        # Find the largest contour area and image moments
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # Find x-axis centroid using image moments
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])

            # Speed mapping for differential steering
            max_speed = 255
            mid_point = window_size[0] // 2
            speed_factor = (max_speed / mid_point)/2

            # Calculate speeds for left and right motors
            right_speed = max_speed - int((cx - mid_point) * speed_factor) 
            left_speed = max_speed + int((cx - mid_point) * speed_factor) 
            
            # divide both speeds by four
            right_speed = right_speed // 0.6
            left_speed = left_speed // 0.6
            # Transmit left and right speeds
            speed_message = {"left_speed": left_speed, "right_speed": right_speed}
            ws.send(json.dumps(speed_message))
            print(f"Speeds transmitted: Left - {left_speed}, Right - {right_speed}")
            # add 5ms delay
            cv2.waitKey(5)
    # Draw the contour on the frame
    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

    # Display processed frame
    cv2.imshow('Processed Frame', frame)

# WebSocket on_message callback
def on_message(ws, message):
    print(f"Received message from WebSocket server: {message}")

# Initialize display window
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', window_size[0], window_size[1])

# Connect to the WebSocket server
ws = websocket.WebSocketApp(websocket_server_address, on_message=on_message)
ws_thread = concurrent.futures.ThreadPoolExecutor().submit(ws.run_forever)

with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
        try:
            # Fetching image from the IP camera
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            frame = cv2.resize(frame, window_size)

            # Display camera input
            cv2.imshow('img', frame)

            # Process the frame in a separate thread
            executor.submit(process_frame, frame, ws)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

        except Exception as e:
            print(f"Error: {e}")

# Cleanup
speed_sender_socket.close()
ws.close()
cv2.destroyAllWindows()
