import time
from spherov2.types import Color
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