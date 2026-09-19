import jarvis_core.tp_link as tp_link
import time
import asyncio
import os
last_gesture = ""
none_start_time = None
elapsed = None
def light_logic(latest_gesture):
    if os.getenv("ENABLE_SMART_LIGHTS", "false").lower() != "true":
        return
    global last_gesture
    global elapsed
    global none_start_time
    if latest_gesture == "None" and none_start_time is None:
        none_start_time = time.time()
    if latest_gesture != "None":
        none_start_time = None
    if latest_gesture == "None":
        elapsed = time.time() - none_start_time
    if latest_gesture == "None" and elapsed != None and elapsed > 0.3:
        last_gesture = "None"

    #Turning on and off right lamp

    if latest_gesture == "Pointing_Up" and last_gesture != latest_gesture: 
        asyncio.run(tp_link.right_turn_on())
        last_gesture = latest_gesture
        none_start_time = None
    if latest_gesture == "Closed_Fist" and last_gesture == "Pointing_Up":         
        asyncio.run(tp_link.right_turn_off())        
        last_gesture = latest_gesture
        none_start_time = None

     #Turning on and off left lamp

    if latest_gesture == "Victory" and last_gesture != latest_gesture: 
        asyncio.run(tp_link.left_turn_on())
        last_gesture = latest_gesture
        none_start_time = None
    if latest_gesture == "Closed_Fist" and last_gesture == "Victory":         
        asyncio.run(tp_link.left_turn_off())        
        last_gesture = latest_gesture
        none_start_time = None


    #Turning on and off LED 1

    if latest_gesture == "Thumb_Up" and last_gesture != latest_gesture: 
        asyncio.run(tp_link.led1_turn_on())
        last_gesture = latest_gesture
        none_start_time = None
    if latest_gesture == "Closed_Fist" and last_gesture == "Thumb_Up":         
        asyncio.run(tp_link.led1_turn_off())        
        last_gesture = latest_gesture
        none_start_time = None


    #Turning on and off LED 2

    if latest_gesture == "Thumb_Down" and last_gesture != latest_gesture: 
        asyncio.run(tp_link.led2_turn_on())
        last_gesture = latest_gesture
        none_start_time = None
    if latest_gesture == "Closed_Fist" and last_gesture == "Thumb_Down":         
        asyncio.run(tp_link.led2_turn_off())        
        last_gesture = latest_gesture
        none_start_time = None


    #Turning on and off all lights

    if latest_gesture == "Open_Palm" and last_gesture != latest_gesture: 
        asyncio.run(tp_link.right_turn_on())
        asyncio.run(tp_link.left_turn_on())
        asyncio.run(tp_link.led1_turn_on())
        asyncio.run(tp_link.led2_turn_on())
        last_gesture = latest_gesture
        none_start_time = None
    if latest_gesture == "Closed_Fist" and last_gesture == "Open_Palm":         
        asyncio.run(tp_link.right_turn_off())
        asyncio.run(tp_link.left_turn_off())
        asyncio.run(tp_link.led1_turn_off())
        asyncio.run(tp_link.led2_turn_off())
        last_gesture = latest_gesture
        none_start_time = None
