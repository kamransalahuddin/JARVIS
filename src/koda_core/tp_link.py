import asyncio
from kasa import SmartPlug
from dotenv import load_dotenv
from dotenv import dotenv_values
import os

load_dotenv()
print(list(dotenv_values().keys()))
get = os.getenv
print(load_dotenv())
async def right_turn_off():
    dev = SmartPlug(get("IP_Address_right"))
    await dev.turn_off()


async def right_turn_on():
    dev = SmartPlug(get("IP_Address_right"))
    await dev.turn_on()


async def left_turn_off():
    dev = SmartPlug(get("IP_Address_left"))
    await dev.turn_off()


async def left_turn_on():
    dev = SmartPlug(get("IP_Address_left"))
    await dev.turn_on()


async def led1_turn_off():
    dev = SmartPlug(get("IP_Address_LED1"))
    await dev.turn_off()


async def led1_turn_on():
    dev = SmartPlug(get("IP_Address_LED1"))
    await dev.turn_on()


async def led2_turn_off():
    dev = SmartPlug(get("IP_Address_LED2"))
    await dev.turn_off()


async def led2_turn_on():
    dev = SmartPlug(get("IP_Address_LED2"))
    await dev.turn_on()