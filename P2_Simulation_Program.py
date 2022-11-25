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
#Alexis Fernandez, fernaa62

import random

def main():
    #Order of container properties
    container_id = [1,2,3,4,5,6]
    colors = ["red", "green", "blue","red", "green", "blue"]
    sizes = ["small","small","small", "large", "large", "large"]

    arm.home() #Reset the location of the QArm
    time.sleep(2)

    random_list = random.sample(container_id,6) #Randomizes the spawning order
    
    for x in range(6): #Repeats for all 6 containers

        #Check to ensure potentiometers are reset
        if potentiometer.left() != 0.5 or potentiometer.right() != 0.5:
            print("Please adjust both potentiometers to 50%")
            
            while(potentiometer.left() != 0.5 or potentiometer.right() != 0.5):
                #Waits until both are set to 50%
                pass
        
        cur_container = random_list[x]
        arm.spawn_cage(cur_container) #Spawns a new container
        
        pick_up(sizes[cur_container-1]) #Executes the pick up function
        rotate_Base(colors[cur_container-1]) #Uses right potentiometer to rotate the base
        drop_off(colors[cur_container-1],sizes[cur_container-1]) #Use left potentiometer to determine drop off location
    
    print("Completed")
        
    

"""
Rotates the QArm base depending on the value of the right potentiometer.
Stops rotating when the QArm is infront of the specified autoclave color.
"""
def rotate_Base(autoclave_color):
    pot_right = potentiometer.right() #Stores the value of the right potentiometer in a variable

    #The exact position of each autoclave
    if autoclave_color == "red":
        autoclave_position = [-0.377, 0.152, 0.483]
    elif autoclave_color == "green":
        autoclave_position = [0.0, -0.406, 0.483]
    elif autoclave_color == "blue":
        autoclave_position =[0.0, 0.406, 0.483]
    
    correct = False
    while(correct == False): #Loops until the QArm is infront of the correct autoclave
        pot_right = potentiometer.right()
        cur_position = arm.effector_position() #Checks the current position of the autoclave

        #Uses a range to detect when the QArm is infront of the correct autoclave
        if (cur_position[0] < autoclave_position[0]+0.01) and (cur_position[1] > autoclave_position[1]-0.01) and autoclave_color == "red": #Once the correct autoclave is detected, exits the loop.
            correct = True
        elif (cur_position[0] < autoclave_position[0]+0.01) and (cur_position[1] < autoclave_position[1]+0.01) and autoclave_color == "green": #Once the correct autoclave is detected, exits the loop.
            correct = True
        elif (cur_position[0] < autoclave_position[0]+0.01) and (cur_position[1] > autoclave_position[1]-0.01) and autoclave_color == "blue": #Once the correct autoclave is detected, exits the loop.
            correct = True   
            
        elif pot_right > 0 and pot_right < 0.5: #Rotate the base counter-clockwise when the right potentiometer is between 0 and 50%
            arm.rotate_base(-1)
            
        elif pot_right > 0.5: #Rotate the base clockwise when the right potentiometer is between 50 and 100%
            arm.rotate_base(1) 

"""
Executes commands to pick up the container based on its size.
"""
def pick_up(container_Size):
    if container_Size == "small":        
        arm.move_arm(0.589, 0.021, -0.014)   #Moves the arm to the pickup location
        time.sleep(2)
        arm.control_gripper(35) #Closes the gripper for the small container
    elif container_Size == "large":
        arm.move_arm(0.617, 0.054, 0.044)  
        time.sleep(2)
        arm.control_gripper(25) #Closes the gripper for the large container
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483)  #Moving the arm to the home position


def drop_off(autoclave_color,container_Size):
    #Small, Large
    red_position = [[-0.614, 0.236, 0.286], [-0.434, 0.167, 0.148]]
    green_position = [[0.0, -0.644, 0.255],[0.0, -0.409, 0.174]]
    blue_position = [[0.0, 0.627, 0.272], [0.0, 0.439, 0.135]]

    if container_Size == "large":
        print("Please adjust the left potentiometer to 100%")
    else:
        print("Please adjust the left potentiometer above 50%")
    
    arm.activate_autoclaves()
    time.sleep(2)
    if autoclave_color == "red":
        while (True): #Loops until the container has been dropped off in the correct
            pot_left = potentiometer.left() #Get the value of the left potentiometer
            if pot_left > 0.5 and pot_left < 1.0 and container_Size == "small": #If the left potentiometer is between 50 and 100%
                arm.move_arm(red_position[0][0], red_position[0][1], red_position[0][2])   #Rotate shoulder and elbow to first position
                time.sleep(2)
                break #Exits the loop
                
            elif pot_left == 1 and container_Size == "large": #If the left potentiometer is at 100%
                arm.open_autoclave("red")
                time.sleep(2)
                arm.move_arm(red_position[1][0], red_position[1][1], red_position[1][2]) #Rotate shoulder and elbow to the second position
                time.sleep(2)
                break
            else:
                pass             
                
        arm.control_gripper(-25) #Open gripper
        time.sleep(2)
        if container_Size == "large": #If the container is large, close the autoclave drawer
            arm.open_autoclave("red",False) #Closes the autoclave drawer
            time.sleep(2)

            
    if autoclave_color == "green":
        while (True):
            pot_left = potentiometer.left() #Get the value of the left potentiometer
            if pot_left > 0.5 and pot_left < 1.0 and container_Size == "small": #If the left potentiometer is between 50 and 100%
                arm.move_arm(green_position[0][0], green_position[0][1], green_position[0][2])   #Rotate shoulder and elbow to first position
                time.sleep(2)
                break
                
            elif pot_left == 1 and container_Size == "large": #If the left potentiometer is at 100%
                arm.open_autoclave("green")
                time.sleep(2)
                arm.move_arm(green_position[1][0], green_position[1][1], green_position[1][2]) #Rotate shoulder and elbow to the second position
                time.sleep(2)
                break
            else:
                pass             
                
        arm.control_gripper(-25) #Open gripper
        time.sleep(2)
        if container_Size == "large": #If the container is large, close the autoclave drawer
            arm.open_autoclave("green",False)
            time.sleep(2)

            
    if autoclave_color == "blue":
        while (True):
            pot_left = potentiometer.left() #Get the value of the left potentiometer
            if pot_left > 0.5 and pot_left < 1.0 and container_Size == "small": #If the left potentiometer is between 50 and 100%
                arm.move_arm(blue_position[0][0], blue_position[0][1], blue_position[0][2])   #Rotate shoulder and elbow to first position
                time.sleep(2)
                break
                
            elif pot_left == 1 and container_Size == "large": #If the left potentiometer is at 100%
                arm.open_autoclave("blue")
                time.sleep(2)
                arm.move_arm(blue_position[1][0], blue_position[1][1], blue_position[1][2]) #Rotate shoulder and elbow to the second position
                time.sleep(2)
                break
            else:
                pass             
                
        arm.control_gripper(-25) #Open gripper
        time.sleep(2)
        if container_Size == "large": #If the container is large, close the autoclave drawer
            arm.open_autoclave("blue",False)
            time.sleep(2)
            
    arm.deactivate_autoclaves()
    arm.home()
    
main()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    
    

    
