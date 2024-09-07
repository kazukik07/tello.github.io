import time
import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.send_command_with_return("command")

tello.takeoff()

time.sleep(5)
tello.land()

try:
    tello.takeoff()
except Exception as e:
    print(f"Error during takeoff: {e}")
