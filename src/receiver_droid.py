#==================================================================
# Project : CyPhyAI
# Python script where a Sphero BOLT listens for IR transmissions
#==================================================================

import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.toy.bolt import BOLT
from spherov2.types import Color
import asyncio

# Find the Sphero Bolt
toys = scanner.find_toys(toy_names=['SB-0EEF'], toy_types=[BOLT])

async def receive_ir(droid):
    while True:
        await asyncio.sleep(0.01)
        droid.start_ir_follow(0, 1)

async def change_color(droid):
    while True:
        await asyncio.sleep(0.01)
        droid.set_main_led(Color(r=255, g=0, b=0))
        time.sleep(2)
        droid.set_main_led(Color(r=255, g=255, b=255))
        time.sleep(2)
        droid.set_main_led(Color(r=255, g=0, b=255))
        time.sleep(2)

async def listen(toys):
    print(toys)
    with SpheroEduAPI(toys[0]) as receiver_droid:        
        tasks = [asyncio.create_task(receive_ir(receiver_droid)), asyncio.create_task(change_color(receiver_droid))]
        await asyncio.gather(*tasks)

asyncio.run(listen(toys))