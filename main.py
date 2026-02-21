# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Victor                                                        #
# 	Created:      1/3/2026, 12:22:22 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
# define all motors 3 wire ports and any functions and vars

#Drive train motors
motor1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
motor4 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
motor5 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
motor6 = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)

#Intake and outtake
snake_1 = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False) # lower part
snake_2 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False) # upper part
piston_ramp = DigitalOut(brain.three_wire_port.a)
cylinder_piston = DigitalOut(brain.three_wire_port.b)

#grouping for drive train
controller1 = Controller(PRIMARY)
drive_train_right = MotorGroup(motor1, motor2, motor3)
drive_train_left = MotorGroup(motor4, motor5, motor6)
drive_train = DriveTrain(drive_train_left, drive_train_right, 3.25, 12.6, 10.125, INCHES, 72/48) # wheel dia, width, length of drive train, gear ratio

# Variables
cylinder_extended = False
ramp_high = False
snake_running = False
starting_pos_is_right = False # change to false if starting to the left, direction based on facing the board
cylinder_dist = 18 # distance from tile corner to cylinder
two_ball_time = 1 # seconds to intake 2 balls from cylinder
two_ball_side = 8 # sec to outtake 2 balls to side ramp
three_ball_intake = 2 # time to inttake 3 balls

def dist_Conversion(dist):
    # function convert taken in desired dist in inch and convert into a number that is used in mm
    # 4/7 mm = 3 in
    # 5 mm = 21 in
    # 16/7 mm = 10 in
    if(dist == 3):
        return 0.85
    elif(dist == 12):
        return 2.9
    elif(dist == 24):
        return 5.9
    elif(dist == 6):
        return 1.5
    else:
        return (0.000103072*dist**2)+(0.243558*dist)-0.160173

def rot_Conversion(deg):
    # function converts desired deg to coded rots
    # 10 deg = 75-80 deg
    # 6 deg = 45
    # 24 deg = 175
    # 12 deg = 85
    if(deg == 90):
        return 12.5
    elif(deg == 45):
        return 6
    else:
        return deg * 2/15

def intake():
    snake_1.spin(FORWARD, 100, PERCENT)
    snake_2.spin(FORWARD, 100, PERCENT)

def outtake():
    snake_1.spin(REVERSE, 100, PERCENT)
    snake_2.spin(REVERSE, 100, PERCENT)

def stop_snake():
    snake_1.stop()
    snake_2.stop()

def ramp_up():
    piston_ramp.set(True)

def ramp_down():
    piston_ramp.set(False)

def cylinder_extend():
    cylinder_piston.set(True)

def cylinder_retract():
    cylinder_piston.set(False)

def ball_snipe():
    snake_1.spin_for(FORWARD, 2, TURNS, 100, PERCENT)
    snake_2.spin_for(FORWARD, 2, TURNS, 100, PERCENT)
    # NEED TO CHANGE TO GET PRECISE TIME/ROTS TO GET 2 BALLS OUTTAKE

def turn_left_90():
    drive_train_left.spin(REVERSE, 100, PERCENT)
    drive_train_right.spin(FORWARD, 100, PERCENT)
    wait(297, MSEC)
    drive_train_left.stop()
    drive_train_right.stop()

def turn_left_45():
    drive_train_left.spin(REVERSE, 100, PERCENT)
    drive_train_right.spin(FORWARD, 100, PERCENT)
    wait(200, MSEC)
    drive_train_left.stop()
    drive_train_right.stop()

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    intake()
    #cylinder_extend()
    if(starting_pos_is_right):
        drive_train.drive_for(FORWARD, dist_Conversion(12), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, rot_Conversion(90), DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, rot_Conversion(90), DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(cylinder_dist), MM, 100, PERCENT) #driving up to cylinder, change 18 to whatever needed in in.
        wait(two_ball_time, SECONDS) # time it takes to get 2 balls from cylinder
        stop_snake()
        drive_train.drive_for(REVERSE, dist_Conversion(cylinder_dist+24), MM, 100, PERCENT)
        cylinder_retract()
        ramp_up()
        outtake()
        wait(two_ball_side, SECONDS) # time to deposit 2 balls on ramp, change as needed
        stop_snake()
        drive_train.turn_for(RIGHT, rot_Conversion(90), DEGREES, 100, PERCENT)
        intake()
        drive_train.drive_for(FORWARD, dist_Conversion(30), MM, 100, PERCENT)
        wait(three_ball_intake, SECONDS) # time to intake 3 balls
        stop_snake()
        drive_train.drive_for(REVERSE, dist_Conversion(6), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, rot_Conversion(90), DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(3), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, rot_Conversion(90), DEGREES, 100, PERCENT)
        drive_train.turn_for(RIGHT, rot_Conversion(45), DEGREES, 100, PERCENT)
        drive_train.drive_for(REVERSE, dist_Conversion(24), MM, 100, PERCENT)
        ramp_down()
        outtake()
        wait(2, SECONDS)
        stop_snake()
    elif(starting_pos_is_right == False):
        drive_train.drive_for(FORWARD, dist_Conversion(12), MM, 100, PERCENT)
        turn_left_90()
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        turn_left_90()
        drive_train.drive_for(FORWARD, dist_Conversion(cylinder_dist), MM, 100, PERCENT) #driving up to cylinder, change 18 to whatever needed in in.
        wait(two_ball_time, SECONDS) # time it takes to get 2 balls from cylinder
        stop_snake()
        drive_train.drive_for(REVERSE, dist_Conversion(cylinder_dist+24), MM, 100, PERCENT)
        cylinder_retract()
        ramp_up()
        outtake()
        wait(two_ball_side, SECONDS) # time to deposit 2 balls on ramp
        stop_snake()
        #drive_train.turn_for(LEFT, rot_Conversion(90), DEGREES, 100, PERCENT)
        turn_left_90()
        intake()
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        wait(three_ball_intake, SECONDS) # time to intake 3 balls
        stop_snake()
        turn_left_90()
        drive_train.drive_for(FORWARD, dist_Conversion(3), MM, 100, PERCENT)
        turn_left_90()
        turn_left_45()
        drive_train.drive_for(REVERSE, dist_Conversion(24), MM, 100, PERCENT)
        outtake()
        wait(2, SECONDS)
        stop_snake()

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    snake_running = True
    if(starting_pos_is_right == False):
        ramp_high = True
    else:
        ramp_high = False
    cylinder_extended = False
    while True:
        #up down on left joystick, left right on right joystick 4 driving
        forward_Velocity = controller1.axis3.position()
        side_Velocity = controller1.axis1.position()
        if(forward_Velocity > 0):
            drive_train.drive(FORWARD, forward_Velocity, PERCENT)
        elif(forward_Velocity < 0):
            drive_train.drive(REVERSE, abs(forward_Velocity), PERCENT)
        else:
            drive_train.set_drive_velocity(0)
            drive_train.stop()

        if(side_Velocity > 0): #turn right
            if(forward_Velocity != 0): # turning right
                drive_train_right.set_velocity(100-side_Velocity, PERCENT)
            else:
                drive_train.turn(RIGHT, side_Velocity, PERCENT)
        elif(side_Velocity < 0): # turn left
            if(forward_Velocity != 0): # turning left
                drive_train_left.set_velocity(100-side_Velocity, PERCENT)
            else:
                drive_train_left.spin(FORWARD, side_Velocity, PERCENT)
                drive_train_right.spin(REVERSE, side_Velocity, PERCENT)
        else:
            drive_train.set_turn_velocity(0)
        
      #left top is intake direction, left bottom is outtake for snake, right top for piston ramp, right bottom cylinder mechanism
        if(snake_running == False):
            if(controller1.buttonL1.pressing()):
                intake()
                snake_running = True
            elif(controller1.buttonL2.pressing()):
                outtake()
                snake_running = True
        elif(snake_running == True):
            if(controller1.buttonL1.pressing()):
                stop_snake()
                snake_running = False
            elif(controller1.buttonL2.pressing()):
                stop_snake()
                snake_running = False
        
        if(ramp_high == False):
            if(controller1.buttonR1.pressing()):
                ramp_up()
                ramp_high = True
        elif(ramp_high == True):
            if(controller1.buttonR1.pressing()):
                ramp_down()
                ramp_high = False

        if(cylinder_extended == False):
            if(controller1.buttonR2.pressing()):
                cylinder_extend()
                cylinder_extended = True
        elif(cylinder_extended == True):
            if(controller1.buttonR2.pressing()):
                cylinder_retract()
                cylinder_extended = False
        
        #if(controller1.buttonA.pressing()):
            #ball_snipe()
            #snake_running = False
        wait(20, MSEC)

# create competition instance
#comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
autonomous()
user_control()
# slot 1 = only user control, slot 2 = auton and user control, slot 3 = random testing

# TO DO LIST:

# driver control tasks:
# test driver control drive train DONE
# test driver control snake DONE (maybe??, need hold if it doesnt go, light tap to stop anything)
# test driver control piston
 
# auton tasks
# test two_ball_time var DONE
# test ball_snipe (how many rots to outtake a ball)
# test two_ball_side var DONE
# test three_ball_intake var DONE
# test full auton code for time and accuracy
# 250 msec pause btwn driving and turning, change velocity to 50%
# test how long it takes to rotate 90 and 45 degrees left DONE
# tape in wires to make sure no disconnect DONE