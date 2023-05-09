# python3
# import sys
# sys.path.append('C:\\Users\\rutvi\\Desktop\\DeskTopFolder\\cmpe\\295 Code\\RutvikRevamp\\spherov2\\')

import time

from spherov2.scanner import *
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
from spherov2.toy.bolt import BOLT
import asyncio
from multiprocessing import Process
import threading
import json


    

def connect_to_bolt(toy, droids,bots):

    try:
        print(toy.name + ' started!')
        droid = SpheroEduAPI(toy)
        loc = [0.00, 0.00]
        action = "up"
        droid.set_main_led(Color(r=0, g=255, b=0))
        droids.append(droid)
        bots[int(len(droids)-1)] = toy.name
        
        droid.set_main_led(Color(r=0, g=0, b=255))  # Sets whole Matrix
        print("Testing End...")

    except Exception as e:
        print('Connection failed with ' + toy.name)
        print("error :" + str(e))
        print('Reconnecting to ' + toy.name)
        toy = find_toy(toy_name=toy.name, toy_types=[BOLT])
        connect_to_bolt(toy, droids,bots)


def main():

    global droids, bots, data

    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=['SB-C54E', 'SB-3D46'], toy_types=[BOLT])
    droids = []
    bots = {}
    for toy in toys:
        print("toy: " + toy.name)

        connect_to_bolt(toy, droids,bots)
    
    print(bots)


if __name__ == "__main__":
    main()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    processs = []
    data = {}
    for bot in bots:
        data[bots[bot]] = []
    
    broadcaster_num = int(input("Enter the bot number to be the broadcaster: "))
    broadcaster = droids[broadcaster_num]
  
    while True:
        num = int(input("Enter a number: "))
        if (num == 10):
            for droid in droids:
                droid.stop_roll(0)
                droid.__exit__(None, None, None)
            break
        else:
            for droid in droids:
                droid.stop_roll(0)
                if droid != broadcaster:
                    droid.start_ir_follow(0, 1)
            selected_droid = droids[num]
            selected_droid.roll(255, 255, 4)
            # Check if the selected bot is the broadcaster
            if num == broadcaster_num:
                selected_droid.start_ir_broadcast(0, 1)
            tempData = {}
            tempData['acceleration'] = droids[num].get_acceleration()
            tempData['vertical acceleration'] = droids[num].get_vertical_acceleration()
            tempData['orientation'] = droids[num].get_orientation()
            tempData['gyroscope'] = droids[num].get_gyroscope()
            tempData['velocity'] = droids[num].get_velocity()
            tempData['location'] = droids[num].get_location()
            tempData['distance'] = droids[num].get_distance()
            tempData['speed'] = droids[num].get_speed()
            tempData['heading'] = droids[num].get_heading()
            
            data[bots[num]].append(tempData)            
            json_data = json.dumps(data)
            x = droids[num].get_battery_voltage_states()
            print(x.value)
            print(json_data)
