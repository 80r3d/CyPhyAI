import time
from spherov2.types import Color
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.toy.bolt import BOLT
from spherov2.types import Color
import threading
'''
Define Custom APIs in this file
'''
def on_collision(api):
    api.stop_roll()
    api.set_main_led(Color(255, 0, 0))
    print('Collision')
    api.set_heading(api.get_heading() + 180)
    time.sleep(0.5)
    api.set_main_led(Color(255, 22, 255))
    api.set_speed(100)

def on_charging(api):
    api.set_main_led(Color(6, 0, 255))
    print('charging')
    time.sleep(1)
    print('remove me from my charger')

def on_not_charging(api):
    api.set_main_led(Color(255, 0, 47))
    print('not charging')

def connect_to_bolt(toy,droids):
    
    try:
        with SpheroEduAPI(toy) as droid:
            print(toy.name + ' started!')
            loc = [0.00,0.00]
            action = "up"
            droid.set_main_led(Color(r=0, g=255, b=0))
            droids.append(droid)
            run_bolt(droid)
            # droid.register_event(EventType.on_charging, customapi.on_charging)
            # droid.register_event(EventType.on_not_charging, customapi.on_not_charging)
            # time.sleep(2)           
            
            
    except Exception as e:
        print('Connection failed with ' + toy.name)
        print("error :" +str(e))
        print('Reconnecting to ' + toy.name)
        toy = scanner.find_toy(toy_name=toy.name, toy_types=[BOLT])
        connect_to_bolt(toy,droids)


        
def run_bolt(droid):
    droid.set_heading(0)
    droid.roll(0,255,2)
    time.sleep(1)
    droid.roll(180,255,2)


def run_bolts(toys):
    for toy in toys:
        run_bolt(toy)

def init_connections(toys,droids):
    for toy in toys:
        t = threading.Thread(target=connect_to_bolt, args=(toy,droids))
        t.start()
        time.sleep(1)
        