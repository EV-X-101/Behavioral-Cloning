import eventlet
import numpy as np
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2
import RPi.GPIO as GPIO
import time


# Set up GPIO pins for motor control
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)  # Left motor
GPIO.setup(11, GPIO.OUT)  # Right motor
left_pwm = GPIO.PWM(7, 100)
right_pwm = GPIO.PWM(11, 100)
left_pwm.start(0)
right_pwm.start(0)


def img_preprocess(img):
    img = img[50:135,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img
 
 
def telemetry(sid, data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    throttle = 1.0 - speed/speed_limit
    print('{} {} {}'.format(steering_angle, throttle, speed))
    send_control(steering_angle, throttle)
 
 
def send_control(steering_angle, throttle):
    # Convert steering angle to duty cycle for left and right motors
    left_duty = 7.5 - steering_angle * 3.75
    right_duty = 7.5 + steering_angle * 3.75
    # Set motor speeds
    left_pwm.ChangeDutyCycle(max(min(throttle * left_duty, 10), 0))
    right_pwm.ChangeDutyCycle(max(min(throttle * right_duty, 10), 0))


if __name__ == '__main__':
    model = load_model('Models/model51.h5')
    speed_limit = 30  # Set speed limit for throttle calculation
    try:
        eventlet.wsgi.server(eventlet.listen(('', 4567)), telemetry)
    except KeyboardInterrupt:
        pass
    finally:
        left_pwm.stop()
        right_pwm.stop()
        GPIO.cleanup()