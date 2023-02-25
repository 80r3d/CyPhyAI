'''
Project : CyPhyAI
Created By : Jay Patel
'''
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.toy.bolt import BOLT
from spherov2.types import Color
import customapi
import threading


toys = scanner.find_toys(toy_names=['SB-0613','SB-C54E','SB-B5BA'], toy_types=[BOLT])

print(toys)     

#==============================================initialize & execute=================================================
droids = []
customapi.init_connections(toys,droids)

#================================================================================================

    

	
