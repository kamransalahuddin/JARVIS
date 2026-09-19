from ultralytics import YOLO
import cv2
import numpy as np
import serial
import sys
import time
from .nose_cam import send_coordinates_to_arduino

model = YOLO("yolo26n.pt")
def if_overlap(person_coordinates, object_coordinates):
    overlap_left = max(person_coordinates[0], object_coordinates[0])
    overlap_top = min(person_coordinates[1], object_coordinates[1])
    overlap_right = max(person_coordinates[2], object_coordinates[2])
    overlap_bottom = min(person_coordinates[3], object_coordinates[3])
   
    if overlap_left < overlap_right and overlap_top < overlap_bottom:
        print("Kamran is on his bed")
    else:
        print("Kamran is not on his bed") 

    
def detect_objects(img):
    

    # reads frames from a camera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = model.track(img)

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs

    img = result.plot()  # display to screen

    results = model(img, verbose=False)

    dimensions = boxes.xyxy.tolist()
    detected = []
    person_coordinates = []
    object_coordinates = []

    #Seeing if person and bed overlap

    for index, i in enumerate(result.boxes.cls):
        name = result.names[int(i)]
        detected.append(name)

        if name == "person":
            person_coordinates = dimensions[index]

        if name == "bed":
            object_coordinates = dimensions[index]

    if person_coordinates and object_coordinates:
        if_overlap(person_coordinates, object_coordinates)
        print(detected)
        print(dimensions)

        #sending coordinates to Jarvis

    for box in results[0].boxes:
        if int(box.cls == 0):
            coordinates = box.xyxy[0]
            x = int(coordinates[0] + coordinates[2]) / 2
            y = int(coordinates[1] + coordinates[3]) / 2

            frame_center_x = img.shape[1] // 2
            frame_center_y = img.shape[0] // 2

    
    
            error_x = frame_center_x - x
            error_y = frame_center_y - y

            if abs(error_x) < 20:
                error_x = 0
    
            if abs(error_y) < 20:
                error_y = 0

            send_coordinates_to_arduino(
                        int(error_x),
                        int(error_y)
                    )

    return img

    if cv2.waitKey(1) & 0xff == 27:
        cv2.destroyAllWindows()

