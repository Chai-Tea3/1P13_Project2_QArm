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


def main():
    #Order of container properties
    colors = ["red", "green", "blue","red", "green", "blue"]
    sizes = ["small","small","small", "large", "large", "large"]

    for i in range(1,7): #Loops through all 6 containers
        arm.spawn_cage(i) #Spawn new container
        pick_up(sizes[i-1]) #Execute pick up function
        rotate_Base(colors[i-1]) #Use right potentiometer to rotate the base
        drop_off(colors[i-1],sizes[i-1]) #Use left potentiometer to pick drop off location
        
    

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
            
        elif pot_right > 0 and pot_right < 0.5:
            arm.rotate_base(-1)
            
        elif pot_right > 0.5:
            arm.rotate_base(1) 

"""
Executes commands to pick up the container based on its size.
"""
def pick_up(container_Size):
    if container_Size == "small":        
        arm.move_arm(0.589, 0.021, -0.014)   #Moving the arm to the pickup location
        time.sleep(2)
        arm.control_gripper(35) #Closing the gripper
    elif container_Size == "large":
        arm.move_arm(0.617, 0.054, 0.044)   #Moving the arm to the pickup location
        time.sleep(2)
        arm.control_gripper(25) #Closing the gripper
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483)  #Moving the arm to the home position


def drop_off(autoclave_color,container_Size):
    #Small, Large
    red_position = [[-0.601, 0.231, 0.274], [-0.434, 0.167, 0.148]]
    green_position = [[0.0, -0.61, 0.26],[0.0, -0.383, 0.15]]
    blue_position = [[0.0, 0.627, 0.272], [0.0, 0.439, 0.135]]
    
    arm.activate_autoclaves()
    time.sleep(2)
    if autoclave_color == "red":
        while (True):
            pot_left = potentiometer.left() #Get the value of the left potentiometer
            if pot_left > 0.5 and pot_left < 1.0 and container_Size == "small": #If the left potentiometer is between 50 and 100%
                arm.move_arm(red_position[0][0], red_position[0][1], red_position[0][2])   #Rotate shoulder and elbow to first position
                time.sleep(2)
                break
                
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
            arm.open_autoclave("red",False)
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
    
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    
    

    

