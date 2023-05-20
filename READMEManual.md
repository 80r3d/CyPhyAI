### Steps to recreate the project:
1) Clone the CyPhyAI repository from github and open it using VS Codea using the NVIDEA Jetson Xavier NX
2) Download and Install Python 3.11 or latest
3) (If setting up the first time)In VS Code navigate to the View dropdown on the toolbar and select Command Palette
4) Search for Python: Create Environment and follow the prompts to create a new environment
3) Select the python interpretor to be python 3.11 in VS Code
4) Execute the commands: pip install -r requirements.txt in the CyPhyAI folder
5) Replace **sensor.py** in **.venv/lib/python3.11/site-packages/spherov2/commands with the file sensor.py** in replace folder.
6) Replace **sphero_edu.py** in **.venv/lib/python3.11/site-packages/spherov2/** with the file sphero_edu.py in replace folder.
7) Replace **utils.py** in **.venv/lib/python3.11/site-packages/spherov2/ with the file utils.py** in replace folder.
8) And then run the **BoltTest.py** file using the run button on the top right of VS Code. This file is an example of how to use the Sphero Bolt API to control the Sphero Bolt.
9) When program runs, it will prompt the user to enter options to send predefined policies as commands to the Sphero Bolts.
10) User can enter either 1, 2, or 3, to send the corresponding policy to the Sphero Bolts i.e. 1 for moving multiple Sphero's in a square pattern, 2 for moving multiple Sphero's in a zigzag pattern, and 3 for registering one Sphero as the leader and other Sphero's as its followers. To quit the program, user can enter 10.

**All the required information about most of the APIs used in the code can be found at :**
https://spherov2.readthedocs.io/en/latest/sphero_edu.html


### Things changed after we modified the spherov2 library:

#### How to connect spheros:

```python
toys = find_toys(toy_names=['SB-C54E', 'SB-3D46', 'SB-EE23'], toy_types=[BOLT]) 

for toy in toys:
        print("toy: " + toy.name)
        connect_to_bolt(toy, droids,bots)
```

#### The function to connect spheros:

```python
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

```


#### How to access other apis:
Once you have the list of connected spheros in the list droids, all the spherov2 APIs are accesible:

E.g.
```python
    droid[i].the_api_you_want_to_use() 
```
   where 'i' be the sphero you want to call api on.

**Sample Policies**

```python
def run_in_square(droid): 
    '''Run in a square.'''

    droid.roll(0,80,0.25)
    time.sleep(2)
    droid.roll(90,80,0.25)
    time.sleep(2)
    droid.roll(180,80,0.25)
    time.sleep(2)
    droid.roll(270,80,0.25)
    time.sleep(2)

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
```

### NOTE: 

**The time parameter in ```roll(heading,speed,time)``` has become ineffective as we have to remove it from the core to establish and keep  multiple spheros connected with the host.**

**To stop the sphero use ```stop_roll(0)``` command.**

