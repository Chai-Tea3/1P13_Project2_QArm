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

#Alexis Fernandez    MacID:fernaa62
def pick_up():
    arm.move_arm(0.624, 0.0, 0.152)   #Moving the arm to the pickup location
    time.sleep(1)
    arm.control_gripper(30) #Closing the gripper
    time.sleep(1)
    arm.move_arm(0.406, 0.0, 0.483)  #Moving the arm to the home position

    






#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

