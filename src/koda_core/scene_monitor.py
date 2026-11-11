import cv2
import time
from rag_system.embedding import model
import numpy as np
from google import genai
from .AI import text_to_speech
import os
from PIL import Image
global similarity
global client
client = genai.Client()

similarity = 1.0
def compare_scenes(loaded_img_1, loaded_img_2):
    global similarity
    loaded_img_1_embedded = model.encode({"image": Image.fromarray(cv2.cvtColor(loaded_img_1, cv2.COLOR_BGR2RGB))})
    loaded_img_2_embedded = model.encode({"image": Image.fromarray(cv2.cvtColor(loaded_img_2, cv2.COLOR_BGR2RGB))})

    similarities = []
    
    dot = np.dot(loaded_img_1_embedded, loaded_img_2_embedded)
    abs = np.linalg.norm(loaded_img_1_embedded) * np.linalg.norm(loaded_img_2_embedded)
    similarity = dot / abs
    similarities.append(similarity)

    if similarity < 0.85:
        pass_image()


    
def pass_image():
    global client
    if not os.path.isfile("frame2.jpg"):
        print("No scene captured yet. Wait for the second camera frame (about two minutes).")
        return
    uploaded_file = client.files.upload(file="frame2.jpg")

    interaction = client.interactions.create(
        model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"),
        input=[
            {"type": "text", "text": "Concise answer only. Describe what's happening here. If needed, ask questions, tell fun facts, make a joke about me, ask if I need assistance based on his surroundings. Don't do all of these things. just do whichever you feel like doing. The person in the camera is always me. Always refer to the person as 'you'"},
            {
                "type": "image",
                "uri": uploaded_file.uri,
                "mime_type": uploaded_file.mime_type
            }
        ]
    )
    text_to_speech(interaction.output_text)



