import cv2
import RPi.GPIO as GPIO
import time

# Set up the ultrasonic sensor
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set up the camera
cap = cv2.VideoCapture(0)

# Define the parking space dimensions
space_width = 0.5  # meters
space_length = 2.0  # meters

# Define the minimum distance from obstacles
min_distance = 0.2  # meters

# Define the parking trajectory
parking_trajectory = [(0.0, 0.0), (0.0, space_length), (space_width, space_length), (space_width, 0.0)]

# Define the parking assistant algorithm
def parking_assistant():
    # Capture an image from the camera
    ret, frame = cap.read()

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection to identify edges
    edges = cv2.Canny(blur, 50, 150)

    # Use the ultrasonic sensor to measure the distance to nearby obstacles
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    # Check if the distance to nearby obstacles is greater than the minimum distance
    if distance > min_distance:
        # Use contour detection to identify potential parking spaces
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(contour)
            if aspect_ratio > 0.5 and aspect_ratio < 2.0 and area > 1000:
                # If a potential parking space is found, calculate the parking trajectory
                center_x = x + w / 2
                center_y = y + h / 2
                scale_x = space_width / w
                scale_y = space_length / h
                parking_trajectory_scaled = [(scale_x * (x - center_x), scale_y * (y - center_y)) for (x, y) in parking_trajectory]
                return parking_trajectory_scaled

    # If no suitable parking space is found, return None
    return None

# Test the parking assistant algorithm
while True:
    parking_traj = parking_assistant()
    if parking_traj is not None:
        print("Found parking space, trajectory:", parking_traj)
        break
    else:
        print("No suitable parking space found, retrying...")
        time.sleep(1)

# Clean up
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()