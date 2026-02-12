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
motor4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
motor5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
motor6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)

#Intake and outtake
snake_1 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
snake_2 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
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
starting_pos_is_right = True # change to false if starting to the left, direction based on facing the board
cylinder_dist = 18 # distance from tile corner to cylinder
two_ball_time = 1.5 # seconds to intake 2 balls from cylinder
turn_amt = 0.88 # numebr of rots to turn 90 deg

def dist_Conversion(dist):
    # function convert taken in desired dist in inch and convert into a number that is used in mm
    # 4/7 mm = 3 in
    # 5 mm = 21 in
    # 16/7 mm = 10 in
    return (0.000103072*dist**2)+(0.243558*dist)-0.160173

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

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    intake()
    if(starting_pos_is_right):
        drive_train.drive_for(FORWARD, dist_Conversion(12), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(cylinder_dist), MM, 100, PERCENT) #driving up to cylinder, change 18 to whatever needed in in.
        wait(two_ball_time, SECONDS) # time it takes to get 2 balls from cylinder
        stop_snake()
        cylinder_retract()
        drive_train.drive_for(REVERSE, dist_Conversion(cylinder_dist+24), MM, 100, PERCENT)
        ramp_up()
        outtake()
        drive_train.turn_for(RIGHT, 90, DEGREES, 100, PERCENT)
        intake()
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        wait(500, MSEC)
        stop_snake()
        drive_train.turn_for(RIGHT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(3), MM, 100, PERCENT)
        drive_train.turn_for(RIGHT, 135, DEGREES, 100, PERCENT)
        drive_train.drive_for(REVERSE, dist_Conversion(24), MM, 100, PERCENT)
        ramp_down()
        outtake()
    elif(starting_pos_is_right == False):
        drive_train.drive_for(FORWARD, dist_Conversion(12), MM, 100, PERCENT)
        drive_train.turn_for(LEFT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        drive_train.turn_for(LEFT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(cylinder_dist), MM, 100, PERCENT) #driving up to cylinder, change 18 to whatever needed in in.
        wait(two_ball_time, SECONDS) # time it takes to get 2 balls from cylinder
        stop_snake()
        cylinder_retract()
        drive_train.drive_for(REVERSE, dist_Conversion(cylinder_dist+24), MM, 100, PERCENT)
        ramp_up()
        outtake()
        drive_train.turn_for(LEFT, 90, DEGREES, 100, PERCENT)
        intake()
        drive_train.drive_for(FORWARD, dist_Conversion(24), MM, 100, PERCENT)
        wait(500, MSEC)
        stop_snake()
        drive_train.turn_for(LEFT, 90, DEGREES, 100, PERCENT)
        drive_train.drive_for(FORWARD, dist_Conversion(3), MM, 100, PERCENT)
        drive_train.turn_for(LEFT, 135, DEGREES, 100, PERCENT)
        drive_train.drive_for(REVERSE, dist_Conversion(24), MM, 100, PERCENT)
        outtake()

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    while True:
        #up down on left joystick, left right on right joystick 4 driving
        forward_Velocity = controller1.axis4.position()
        side_Velocity = controller1.axis2.position()
        if(forward_Velocity > 0):
            drive_train.drive(FORWARD, forward_Velocity, PERCENT)
        elif(forward_Velocity < 0):
            drive_train.drive(REVERSE, abs(forward_Velocity), PERCENT)
        else:
            drive_train.set_drive_velocity(0)
            drive_train.stop()

        if(side_Velocity > 0): #turn right
            if(forward_Velocity != 0): # turning right
                drive_train_right.set_velocity(1-side_Velocity)
            else:
                drive_train.turn(RIGHT, side_Velocity, PERCENT)
        elif(side_Velocity < 0): # turn left
            if(forward_Velocity != 0): # turning left
                drive_train_left.set_velocity(1-side_Velocity)
            else:
                drive_train.turn(LEFT, side_Velocity, PERCENT)
        else:
            drive_train.set_turn_velocity(0)
        
      #left top is intake direction, left bottom is outtake for snake, right top for piston ramp, right bottom cylinder mechanism
        if(snake_running == False):
            controller1.buttonL1.pressed(intake)
            controller1.buttonL2.pressed(outtake)
            snake_running = True
        elif(snake_running == True):
            controller1.buttonL1.pressed(stop_snake)
            controller1.buttonL2.pressed(stop_snake)
            snake_running = False
        
        if(ramp_high == False):
            controller1.buttonR1.pressed(ramp_up)
            ramp_high = True
        elif(ramp_high == True):
            controller1.buttonR1.pressed(ramp_down)
            ramp_high = False
        if(cylinder_extended == False):
            controller1.buttonR2.pressed(cylinder_extend)
            cylinder_extended = True
        elif(cylinder_extended == True):
            controller1.buttonR2.pressed(cylinder_retract)
            cylinder_extended = False
        
        if(controller1.buttonA.pressing() == 1):
            ball_snipe()
            snake_running = False

        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
#controller1.buttonX.pressed(autonomous)
#user_control()
# Drive forwards and backwards
drive_train.drive_for(FORWARD, dist_Conversion(12), MM)
wait(10, SECONDS)
drive_train.drive_for(REVERSE, dist_Conversion(12), MM)
drive_train.turn_for(RIGHT, 90, DEGREES)

# 0.88 turns = 1 Foot 