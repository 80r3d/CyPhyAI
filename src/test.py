'''
Project : CyPhyAI
Created By : Jay Pate
'''
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.toy.bolt import BOLT
from spherov2.types import Color
import customapi
import threading

toy = scanner.find_toy(toy_name='SB-C54E', toy_types=[BOLT])
while True:
    try:
        with SpheroEduAPI(toy) as droid:
            print(toy.name + ' started!')
            loc = [0.00,0.00]
            action = "up"
            droid.set_main_led(Color(r=255, g=0, b=0))
            droid.register_event(EventType.on_charging, customapi.on_charging)
            droid.register_event(EventType.on_not_charging, customapi.on_not_charging)
            time.sleep(2)
            break            
            
            
    except Exception as e:
        print('Connection failed with ' + toy.name)
        print("error :" +str(e))
        print('Reconnecting to ' + toy.name)
        toy = scanner.find_toy(toy_name=toy.name, toy_types=[BOLT])
        
with SpheroEduAPI(toy) as droid:
    droid.register_event(EventType.on_collision, customapi.on_collision)
    droid.set_main_led(Color(r=0, g=255, b=0))
    time.sleep(2)
    droid.set_main_led(Color(r=0, g=0, b=255))
    time.sleep(2)
      
    droid.spin(180,0.1)
    droid.set_speed(10000)
    time.sleep(10)
    droid.set_speed(0)
            

	
