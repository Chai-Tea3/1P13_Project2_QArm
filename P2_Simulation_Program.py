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
#Alexis Fernandez fernaa62

#Small, Large

def main():
    colors = ["red", "green", "blue","red", "green", "blue"]
    sizes = ["small","small","small", "large", "large", "large"]

    for i in range(1,7):
        arm.spawn_cage(i)
        pick_up()
        rotate_Base(colors[i-1])
        drop_off(colors[i],sizes[i-1])
        
    

"""
Rotates the QArm base depending on the value of the right potentiometer.
Stops rotating when the QArm is infront of the specified autoclave color.
"""
def rotate_Base(autoclave_color):
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
    time.sleep(2)
    arm.control_gripper(40) #Closing the gripper
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483)  #Moving the arm to the home position

def drop_off(autoclave_color,container_Size):
    red_position = [[-0.601, 0.231, 0.274], [-0.434, 0.167, 0.148]]
    green_position = [[0.0, -0.61, 0.26],[0.0, -0.383, 0.15]]
    blue_position = [[0.0, 0.627, 0.272], [0.0, 0.439, 0.135]]
    
    pot_left = potentiometer.left()
    arm.activate_autoclaves()
    time.sleep(2)
    
    if autoclave_color == "red":
        while (True):
            if pot_left > 0.5 and pot_left < 1.0: #If the left potentiometer is between 50 and 100%
                time.sleep(2)
                arm.move_arm(red_position[0][0], red_position[0][1], red_position[0][2])   #Rotate shoulder and elbow to first position
                break
            
            elif pot_left == 1: #If the left potentiometer is at 100%
                time.sleep(2)
                arm.open_autoclave("red")
                time.sleep(2)
                arm.move_arm(red_position[1][0], red_position[1][1], red_position[1][2]) #Rotate shoulder and elbow to the second position
                break
            else:
                pass
           
        if container_Size == "small" and arm.effector_position()==red_position[1]: #If a small container is at large container position
            time.sleep(2)
            arm.move_arm(red_position[0][0], red_position[0][1], red_position[0][2]) #Move to position 1
            
        elif container_Size == "large" and arm.effector_position()==red_position[0]: #If a large container is at small container position
            time.sleep(2)
            arm.move_arm(red_position[1][0], red_position[1][1], red_position[1][2]) #Move to position 2
            time.sleep(2)
            
        arm.control_gripper(-35) #Open gripper
        if container_Size == "large": #If the container is large, close the autoclave drawer
            time.sleep(2)
            arm.open_autoclave("red",False)

            
    if autoclave_color == "green":
        if pot_left > 0.5 and pot_left < 1.0: #If the left potentiometer is between 50 and 100%
            arm.move_arm(green_position[0][0], green_position[0][1], green_position[0][2])   #Rotate shoulder and elbow to first position
        
        elif pot_left == 1: #If the left potentiometer is at 100%
            arm.open_autoclave("green")
            arm.move_arm(green_position[1][0], green_position[1][1], green_position[1][2]) #Rotate shoulder and elbow to the second position
        
        if container_Size == "small" and arm.effector_position()==green_position[1]: #If a small container is at large container position
            arm.move_arm(green_position[0][0], green_position[0][1], green_position[0][2]) #Move to position 1
            
        elif container_Size == "large" and arm.effector_position()==green_position[0]: #If a large container is at small container position
            arm.move_arm(green_position[1][0], green_position[1][1], green_position[1][2]) #Move to position 2
        arm.control_gripper(-35) #Open gripper
        if container_Size == "large": #If the container is large, close the autoclave drawer
            arm.open_autoclave("green",False)

            
    if autoclave_color == "blue":
        if pot_left > 0.5 and pot_left < 1.0: #If the left potentiometer is between 50 and 100%
            arm.move_arm(blue_position[0][0], blue_position[0][1], blue_position[0][2])   #Rotate shoulder and elbow to first position
        
        elif pot_left == 1: #If the left potentiometer is at 100%
            arm.open_autoclave("blue")
            arm.move_arm(blue_position[1][0], blue_position[1][1], blue_position[1][2]) #Rotate shoulder and elbow to the second position
        
        if container_Size == "small" and arm.effector_position()==blue_position[1]: #If a small container is at large container position
            arm.move_arm(blue_position[0][0], blue_position[0][1], blue_position[0][2]) #Move to position 1
            
        elif container_Size == "large" and arm.effector_position()==blue_position[0]: #If a large container is at small container position
            arm.move_arm(blue_position[1][0], blue_position[1][1], blue_position[1][2]) #Move to position 2
        arm.control_gripper(-35) #Open gripper
        if container_Size == "large": #If the container is large, close the autoclave drawer
            arm.open_autoclave("blue",False)
            
    arm.deactivate_autoclaves()
    arm.home()
    









#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

