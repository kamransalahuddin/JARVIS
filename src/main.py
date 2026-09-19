import cv2
from jarvis_core.nose_cam import track_nose, send_coordinates_to_arduino
from ultralytics import YOLO
from jarvis_core.YOLO import detect_objects
from tracker import Tracker
from jarvis_core.hand_tracker import run_hand_tracker
from jarvis_core import AI
import threading
import time
import os
# Load the model
from jarvis_core.scene_monitor import compare_scenes, pass_image
model = YOLO("yolo26n.pt")
start = int(time.monotonic())

webcam = cv2.VideoCapture(int(os.getenv("CAMERA_INDEX", "0")))
time.sleep(1)

#webcam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
ret, img = webcam.read()
if not ret or img is None:
    webcam.release()
    raise RuntimeError("Cannot read the camera. Check camera permissions and CAMERA_INDEX in .env.")

img_h, img_w = img.shape[:2]
AI_threaded = threading.Thread(target=AI.jarvis_ai, daemon=True)
AI_threaded.start()



tracker = Tracker(
    img_w,
    img_h,
    model_type=3,
    max_faces=1,
    no_gaze=True,
    silent=True,
    detection_threshold=0.1,
    try_hard=True
)
frame_one_captured = False
while True:
    if AI.pre_context_text.strip().lower().rstrip(".!?") == "stop everything":
        break
    now = int(time.monotonic())
    ret, img = webcam.read()

    if not ret:
        continue
    img = cv2.rotate(img, cv2.ROTATE_180)

    #img = detect_objects(img)
    nose_img = cv2.convertScaleAbs(img, alpha=1.5, beta=30)
    print(webcam.get(cv2.CAP_PROP_EXPOSURE))


    img = track_nose(img, tracker=tracker)
    img = run_hand_tracker(img)
    if now - start >= 60 and frame_one_captured == False:
        saved_img_1 = cv2.imwrite('frame1.jpg', img)
        loaded_img_1 = cv2.imread("frame1.jpg")
        frame_one_captured = True
    if AI.pre_context_text.strip().lower().rstrip(".!?") == "look":
        pass_image()

        
        
        
        
    if now - start >= 120 and AI.pre_context_text.strip().lower().rstrip(".!") != "stop":
        saved_img_2 = cv2.imwrite('frame2.jpg', img) 
        loaded_img_2 = cv2.imread("frame2.jpg")
        scene_comparison_thread = threading.Thread(target=compare_scenes, args = (loaded_img_1, loaded_img_2), daemon=True).start()
        start = now
        frame_one_captured = False
        
        
    cv2.imshow("Jarvis", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv2.destroyAllWindows()
