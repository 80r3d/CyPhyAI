# python3
# import sys
# sys.path.append('C:\\Users\\rutvi\\Desktop\\DeskTopFolder\\cmpe\\295 Code\\RutvikRevamp\\spherov2\\')

from enum import IntEnum
import time

from spherov2.scanner import *
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
from spherov2.toy.bolt import BOLT
import asyncio
from multiprocessing import Process
import threading
import json


class BatteryVoltageStates(IntEnum):
    UNKNOWN = 0
    OK = 1
    LOW = 2
    CRITICAL = 3
    
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

def run_in_square(droid):
    droid.roll(0,80,0.25)
    time.sleep(2)
    droid.roll(90,80,0.25)
    time.sleep(2)
    droid.roll(180,80,0.25)
    time.sleep(2)
    droid.roll(270,80,0.25)
    time.sleep(2)

def run_zigzag(droid):
    
    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(30,80,0.25)
    time.sleep(0.3)
    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(-30,80,0.25)
    time.sleep(0.3)
    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(30,80,0.25)
    time.sleep(0.3)
    droid.roll(-30,80,0.25)

def ir_follow(droids):
    broadcaster = droids[0]
    broadcaster.start_ir_broadcast(0, 1)
    broadcaster.set_main_led(Color(r=255, g=0, b=0))
    for droid in droids:
        if droid != broadcaster:
            droid.start_ir_follow(0, 1)

    # run_zigzag(broadcaster) 
    broadcaster.roll(0,80,0.25)    
    time.sleep(5)  
    broadcaster.stop_roll(0) 
    stop_ir_follow(droids)

def stop_ir_follow(droids):
    broadcaster = droids[0]
    broadcaster.stop_ir_broadcast()
    broadcaster.set_main_led(Color(r=0, g=0, b=255))
    for droid in droids:
        if droid != broadcaster:
            droid.stop_ir_follow()        
    
        
    






def predefined_policy(droids,droid,n):
    if n==1:
        run_in_square(droid)
    elif n==2:
        run_zigzag(droid)   
    elif n==3:
        ir_follow(droids)
    
def main():

    global droids, bots, data

    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=['SB-C54E', 'SB-3D46', 'SB-EE23'], toy_types=[BOLT])
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
    
    # broadcaster_num = int(input("Enter the bolt number to be the broadcaster: "))
    # if broadcaster_num == -1:
    #     print("No broadcaster selected")
    # else:
    #     broadcaster = droids[broadcaster_num]
    
    # Check if the selected bot is the broadcaster
    # if broadcaster_num != -1:
    #     broadcaster.start_ir_broadcast(0, 1)
    #     broadcaster.set_main_led(Color(r=255, g=0, b=0))
    # for droid in droids:
    #     droid.stop_roll(0)
    #     if broadcaster_num != -1:
    #         if droid != broadcaster:
    #             droid.start_ir_follow(0, 1)
    #             time.sleep(0.075)
    while True:
        num = int(input("Enter a custom policy number: (1) Square (2) Zigzag (3) IR Follow (10) Exit:"))
        if (num == 10):
            for droid in droids:
                droid.stop_roll(0)
                droid.__exit__(None, None, None)
            break
        else:
            # selected_droid = droids[num]
            # user_speed = int(input("Enter speed at which the bolt should roll: "))
            # zigzag policy
            # selected_droid.roll(0,80,0.25)
            # time.sleep(0.3)
            # selected_droid.roll(30,80,0.25)
            # time.sleep(0.3)
            # selected_droid.roll(0,80,0.25)
            # time.sleep(0.3)

            # selected_droid.roll(-30,80,0.25)

            # selected_droid.roll(0,80,0.25)
            # time.sleep(0.3)
            # selected_droid.roll(30,80,0.25)
            # time.sleep(0.3)
            # # selected_droid.roll(-30,80,0.25)
            # selected_droid.roll(0, user_speed, 3)

            for droid in droids:
                predefined_policy(droids,droid,num)
                droid.stop_roll(0)

                tempData = {}
                tempData['acceleration'] = droid.get_acceleration()
                tempData['vertical acceleration'] = droid.get_vertical_acceleration()
                tempData['orientation'] = droid.get_orientation()
                tempData['gyroscope'] = droid.get_gyroscope()
                tempData['velocity'] = droid.get_velocity()
                tempData['location'] = droid.get_location()
                tempData['distance'] = droid.get_distance()
                tempData['speed'] = droid.get_speed()
                tempData['heading'] = droid.get_heading()
                if(droid.get_battery_voltage_states() == 0):
                    tempData['battery'] = "UNKNOWN"
                elif(droid.get_battery_voltage_states() == 1):
                    tempData['battery'] = "OK"
                elif(droid.get_battery_voltage_states() == 2):
                    tempData['battery'] = "LOW"
                elif(droid.get_battery_voltage_states() == 3):
                    tempData['battery'] = "CRITICAL"
                # data[droid].append(tempData)            
                # json_data = json.dumps(data)
                print(tempData)
