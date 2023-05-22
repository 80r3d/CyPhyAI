#for spherov2 api reference visit: https://spherov2.readthedocs.io/en/latest/sphero_edu.html

'''
Project : CyPhyAI (CLOUD INFRASTRUCTURE)
This file is created and modified by CLOUD TEAM for purpose of demonstartion of integration with cloud
'''


from enum import IntEnum
import time
from unittest import result
from spherov2.scanner import *
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
from spherov2.toy.bolt import BOLT
import asyncio
from multiprocessing import Process
import threading
import json


class BatteryVoltageStates(IntEnum):  
    '''Battery voltage states.'''

    UNKNOWN = 0
    OK = 1
    LOW = 2
    CRITICAL = 3

def get_all_data(droid):
    '''Get all data from the droid.'''
    print("The data in droid is ", droid)
    data = {}
    
    data['acceleration'] = droid.get_acceleration()
    data['vertical acceleration'] = droid.get_vertical_acceleration()
    data['orientation'] = droid.get_orientation()
    data['gyroscope'] = droid.get_gyroscope()
    data['velocity'] = droid.get_velocity()
    data['location'] = droid.get_location()
    data['distance'] = droid.get_distance()
    data['speed'] = droid.get_speed()
    data['heading'] = droid.get_heading()
    if(droid.get_battery_voltage_states() == 0):
        data['battery'] = "UNKNOWN"
    elif(droid.get_battery_voltage_states() == 1):
        data['battery'] = "OK"
    elif(droid.get_battery_voltage_states() == 2):
        data['battery'] = "LOW"
    elif(droid.get_battery_voltage_states() == 3):
        data['battery'] = "CRITICAL"
    return data
    
    
def connect_to_bolt(toy, droids,bots):
    '''Connect to the bolt toy.'''

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
        toys = find_toys(toy_names=[toy.name], toy_types=[BOLT])
        connect_to_bolt(toys[0], droids,bots)

def run_in_square(droid): 
    '''Run in a square.'''

    droid.roll(0,40,0.25)
    time.sleep(2)
    droid.roll(90,40,0.25)
    time.sleep(2)
    droid.roll(180,40,0.25)
    time.sleep(2)
    droid.roll(270,40,0.25)
    time.sleep(2)


def run_in_spin(droid): 
    '''Run in a spin.'''

    droid.spin(360, 0.2)
    time.sleep(5)


def run_zigzag(droid):
    '''Run in a zigzag.'''

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
    '''IR follow.'''

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
    '''Stop IR follow.'''

    broadcaster = droids[0]
    broadcaster.stop_ir_broadcast()
    broadcaster.set_main_led(Color(r=0, g=0, b=255))
    for droid in droids:
        if droid != broadcaster:
            droid.stop_ir_follow()        
    

def predefined_policy(droids,droid,n):
    '''Run a predefined policy.'''

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
    toys = find_toys(toy_names=['SB-3D46'], toy_types=[BOLT]) #find toys is a spherov2 api function
    droids = []
    bots = {}
    for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)
    
    print(bots)
    

def sampleapitest():
    global droids, bots, data
    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=['SB-3D46'], toy_types=[BOLT]) #find toys is a spherov2 api function
    droids = []
    bots = {}
    for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)
    processs = []
    data = {}

    for bot in bots:
        data[bots[bot]] = []
    
    for droid in droids:
        run_in_square(droid)
        droid.stop_roll(0)
        data[bots[droids.index(droid)]].append(get_all_data(droid))
    return "Now Moving!"

def getData(robotId):
    global droids, bots, data
    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=[robotId], toy_types=[BOLT]) #find toys is a spherov2 api function
    droids = []
    bots = {}

    for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)
    results = []
    for droid in droids:
        results.append(get_all_data(droid))

    return results

def moveWithPredefinedPath(robotId,path_type):
    global droids, bots, data
    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=[robotId], toy_types=[BOLT]) #find toys is a spherov2 api function
    droids = []
    bots = {}

    for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)

    for droid in droids:
        if path_type == 'zigzag':
            run_zigzag(droid)
            droid.stop_roll(0)
            droid.__exit__(None, None, None)


        elif path_type == 'square':
            run_in_square(droid)
            droid.stop_roll(0)
            droid.__exit__(None, None, None)

        elif path_type == 'spin':
            run_in_spin(droid)
            droid.stop_roll(0)
            droid.__exit__(None, None, None)

        else :
            False
    return True


def moveWithSpeedAndAngle(robotId,angle,speed,time):
    global droids, bots, data
    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=[robotId], toy_types=[BOLT]) #find toys is a spherov2 api function
    droids = []
    bots = {}
    

    for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)

    for droid in droids:
        droid.roll(angle,speed,time)
        time.sleep(1)
        droid.stop_roll(0)
        droid.__exit__(None, None, None)

    return True

if __name__ == "__main__":
    '''Main function.'''
    sampleapitest()
    # main()

    # processs = []
    # data = {}

    # for bot in bots:
    #     data[bots[bot]] = []
    
    # for droid in droids:
    #     run_in_square(droid)
    #     droid.stop_roll(0)
    #     data[bots[droids.index(droid)]].append(get_all_data(droid))

    # while True:
    #     num = int(input("Enter a custom policy number: (1) Square (2) Zigzag (3) IR Follow (10) Exit:"))
    #     if (num == 10):
    #         for droid in droids:
    #             droid.stop_roll(0)
    #             droid.__exit__(None, None, None)
    #         break
    #     else:
           
    #         for droid in droids:
    #             predefined_policy(droids,droid,num)
    #             droid.stop_roll(0)
    #             data[bots[droids.index(droid)]].append(get_all_data(droid))