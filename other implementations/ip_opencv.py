import cv2
import numpy as np
import requests
import concurrent.futures
import socket

# IP camera URL
url = "http://100.77.168.241:8080/shot.jpg"

# Display window size
window_size = (640, 360)

# Receiver settings for speed transmission
speed_host = '192.168.144.151'
speed_port = 80

# Create a socket object for speed transmission
speed_sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to process each frame
def process_frame(frame):
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
            speed_factor = max_speed / mid_point

            # Calculate speeds for left and right motors
            right_speed = max_speed - int((cx - mid_point) * speed_factor) / 4
            left_speed = max_speed + int((cx - mid_point) * speed_factor) / 4

            # Transmit left and right speeds
            speed_message = f"{left_speed},{right_speed}"
            speed_sender_socket.sendto(speed_message.encode('utf-8'), (speed_host, speed_port))
            print(f"Speeds transmitted: nigga Left - {left_speed}, nigga Right - {right_speed}")

    # Draw the contour on the frame
    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
    # draw contours on frame
    



    # Display processed frame
    cv2.imshow('Processed Frame', frame)

# Initialize display window
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', window_size[0], window_size[1])

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
            executor.submit(process_frame, frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

        except Exception as e:
            print(f"Error: {e}")

# Cleanup
speed_sender_socket.close()
cv2.destroyAllWindows()
