ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#Fri-27 Environment: 1
#Riley Chai, chair3

colors = ["red", "green", "blue"]
sizes = ["small", "large"]
blue_position = [[0.0, 0.627, 0.272], [0.0, 0.439, 0.135]]
red_position = [[-0.601, 0.231, 0.274], [-0.434, 0.167, 0.148]]
green_position = [[0.0, -0.61, 0.26],[0.0, -0.383, 0.15]]

"""
Rotates the QArm base depending on the value of the right potentiometer.
Stops rotating when the QArm is infront of the specified autoclave color.
"""
def rotate_QArm_Base(autoclave_color):
    pot_right = potentiometer.right() #Stores the value of the right potentiometer in a variable
    
    while(pot_right > 0): #Loops until the QArm is infront of the correct autoclave
        pot_right = potentiometer.right()
        cur_color = arm.check_autoclave(autoclave_color) #Checks the color of the autoclave

        if pot_right > 0 and pot_right < 0.5 and cur_color == False:
            arm.rotate_base(-1.5)
            
        elif pot_right > 0.5 and cur_color == False:
            arm.rotate_base(1.5)
            
        elif cur_color == True: #Once the correct autoclave is detected, exits the loop.
            pot_right = 0
def pick_up():
    arm.move_arm(0.619, 0.0, 0.043)   #Moving the arm to the pickup location
    time.sleep(1)
    arm.control_gripper(30) #Closing the gripper
    time.sleep(1)
    arm.move_arm(0.406, 0.0, 0.483)  #Moving the arm to the home position

def drop_off():
    pot_left = potentiometer.left()
    activate_autoclaves()
    time.sleep(2)
    
    if colors[x] == "blue":
        if pot_left > 0.5 and pot_left <1:
            arm.move_arm(blue_position[0][0], blue_position[0][1], blue_position[0][2])   #rotate shoulder and elbow to first position
        
        elif pot_left == 1:
            arm.open_autoclave("blue")
            arm.move_arm(blue_position[1][0], blue_position[1][1], blue_position[1][2]) #Rotate shoulder and elbow to the second position
        
        if sizes[x] == "large" and arm.move_arm(blue_position[0][0], blue_position[0][1], blue_position[0][2])
    
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    
    

