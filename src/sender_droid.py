'''
Python script where one droid assumes as a Leader and broadcasts IR messages
'''

import time
import asyncio
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.toy.bolt import BOLT
from spherov2.types import Color

# Find the Sphero Bolt named 'SB-EE23'
toys = scanner.find_toys(toy_names=['SB-EE23'], toy_types=[BOLT])

async def broadcasting(droid):
    while True:
        await asyncio.sleep(0.01)
        droid.start_ir_broadcast(0, 1)

async def rolldroid(droid):
    while True:
        await asyncio.sleep(0.01)
        droid.roll(0, 30, 3)
        time.sleep(1)
        droid.roll(90, 30, 3)
        time.sleep(1)
        droid.roll(180, 30, 3)
        time.sleep(1)
        droid.roll(270, 30, 3)
        time.sleep(1)
        droid.roll(0, 30, 3)
        time.sleep(1)

async def broadcast(toys):
    print(toys)
    with SpheroEduAPI(toys[0]) as sender_droid:
        sender_droid.set_main_led(Color(r=0, g=255, b=0))
        tasks = [asyncio.create_task(broadcasting(sender_droid)), asyncio.create_task(rolldroid(sender_droid))]
        await asyncio.gather(*tasks)

asyncio.run(broadcast(toys))