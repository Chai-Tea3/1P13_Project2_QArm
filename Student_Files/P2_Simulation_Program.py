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

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

