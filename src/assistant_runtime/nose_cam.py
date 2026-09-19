import cv2
import serial
import sys
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# REPLACED: MediaPipe imports/detector with OpenSeeFace.
load_dotenv()
sys.path.insert(0, os.getenv("OPENSEEFACE_PATH", str(Path(__file__).resolve().parents[2] / "external" / "OpenSeeFace")))
from tracker import Tracker

arduino_port = os.getenv("ARDUINO_PORT", "").strip()
arduinoData = serial.Serial(arduino_port, 115200) if arduino_port else None
if arduinoData is not None:
    time.sleep(2)

def send_coordinates_to_arduino(x, y):
    if arduinoData is None:
        return
    coordinates = f"{x},{y}\r"
    arduinoData.write(coordinates.encode())
    print(f"X{x}Y{y}\n")

def track_nose(img, tracker):
# REPLACED: OpenSeeFace needs the frame size when creating the tracker.

    # REPLACED: MediaPipe face detection with OpenSeeFace tracking.
    faces = tracker.predict(img)
    print("faces detected:", len(faces))

    if len(faces) > 0:
        frame_center_x = img.shape[1] // 2
        frame_center_y = img.shape[0] // 2
        
        face = faces[0]
        # REPLACED: MediaPipe bounding-box center with OpenSeeFace nose landmark.
        nose_y, nose_x, confidence = face.lms[30]

        x = int(nose_x)
        y = int(nose_y)

        error_x = frame_center_x - x
        error_y = frame_center_y - y
        if abs(error_x) < 20:
            error_x = 0

        if abs(error_y) < 20:
            error_y = 0

        cv2.circle(img, (x, y), 6, (0, 0, 255), -1)

        print(x, y)

        send_coordinates_to_arduino(
            int(error_x),
            int(error_y)
        )
    return img
    

