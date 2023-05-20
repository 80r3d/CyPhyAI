Steps to recreate the project:
1) Clone the CyPhyAI repository from github and open it using VS Codea using the NVIDEA Jetson Xavier NX
2) Download and Install Python 3.11 or latest
3) (If setting up the first time)In VS Code navigate to the View dropdown on the toolbar and select Command Palette
4) Search for Python: Create Environment and follow the prompts to create a new environment
3) Select the python interpretor to be python 3.11 in VS Code
4) Execute the commands: pip install speherov2 and pip install bleak in the CyPhyAI folder
5) Replace sensor.py in .venv/lib/python3.11/site-packages/spherov2/commands with the file sensor.py in replace folder.
6) Replace sphero_edu.py in .venv/lib/python3.11/site-packages/spherov2/ with the file sphero_edu.py in replace folder.
7) Replace utils.py in .venv/lib/python3.11/site-packages/spherov2/ with the file utils.py in replace folder.
8) And then run the BoltTest.py file using the run button on the top right of VS Code. This file is an example of how to use the Sphero Bolt API to control the Sphero Bolt.
9) When program runs, it will prompt the user to enter options to send predefined policies as commands to the Sphero Bolts.
10) User can enter either 1, 2, or 3, to send the corresponding policy to the Sphero Bolts i.e. 1 for moving multiple Sphero's in a square pattern, 2 for moving multiple Sphero's in a zigzag pattern, and 3 for registering one Sphero as the leader and other Sphero's as its followers. To quit the program, user can enter 10.