#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
mAxe = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
mTransmission = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
encoder_axe = Encoder(brain.three_wire_port.a)
bumperEast = Bumper(brain.three_wire_port.e)
bumperTop = Bumper(brain.three_wire_port.g)
bumperWest = Bumper(brain.three_wire_port.f)
encoder_transm = Encoder(brain.three_wire_port.c)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis4
            # right = axis3 - axis4
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis4.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis4.position()
            
            # check if the values are inside of the deadband range
            if abs(drivetrain_left_side_speed) < 5 and abs(drivetrain_right_side_speed) < 5:
                # check if the motors have already been stopped
                if drivetrain_needs_to_be_stopped_controller_1:
                    # stop the drive motors
                    left_drive_smart.stop()
                    right_drive_smart.stop()
                    # tell the code that the motors have been stopped
                    drivetrain_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the motors next
                # time the input is in the deadband range
                drivetrain_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

vexcode_brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0
killSwitch = False

mTransmission.set_velocity(100,PERCENT)
mAxe.set_velocity(100, PERCENT)

class Axe():
    def __init__(self) -> None:
        self.printTimer = 15
        self.count = 0                                                                                                                                                                                  
        self.axePointer = 0

        self.axePower = False
        self.transmissionPower = False
        self.axeForward = True
        self.transmissionEastToWest = True

        self.bumperW = False
        self.bumperE = False
        self.bumperT = False
        
        self.attacking = False
        self.onGear = False

        self.message = 'NA'

    def changeMessage(self, message):
        self.message = message

    def engage_gear(self):
        self.trans_W_E()
        
        pass

    def release_gear(self):
        self.trans_E_W()
        pass

    def trans_E_W(self) :
        self.transmissionEastToWest = True
        self.transmissionPower = True

    def trans_W_E(self) :
        self.transmissionEastToWest = False
        self.transmissionPower = True

    def transStop(self):
        self.transmissionPower = False

    def stopAllMotors(self):
        mAxe.stop()
        mTransmission.stop()

    def bumpedW(self):
        self.bumperW = True
        self.onGear = False
        brain.screen.clear_row(2)
        brain.screen.set_cursor(2,1)
        brain.screen.print("W")

    def bumpedE(self):
        self.bumperE = True
        self.onGear = True
        brain.screen.clear_row(2)
        brain.screen.set_cursor(2,1)
        brain.screen.print("E")

    def axeStop(self):
        self.axePower = False
        self.changeMessage('axe stop')

    def axeAdvance(self):
        self.changeMessage('axe advance')
        self.axePower = True
        self.axeForward = True

    def axeRetreat(self):
        self.changeMessage('axe retreat')
        self.axePower = True
        self.axeForward = False

    def displayUpdate(self):
        if(self.count > self.printTimer):
            brain.screen.clear_row(1)
            brain.screen.set_cursor(1,1)
            brain.screen.print(self.message)
            self.count = 0
        self.count += 1

    def axeStayAngle(self):
        mAxe.set_position( mAxe.position(DEGREES) , DEGREES)
        

    def resetAxe(self):
        self.axePointer = (encoder_axe.position(DEGREES))
        while encoder_axe.position(DEGREES)< self.axePointer + 70 :
            mAxe.spin(REVERSE)
            pass
        mAxe.stop()

    def transmissionCheck(self):
        if(bumperWest.pressing()):
            self.bumpedW()
        else:
            self.bumperW = False

        if(bumperEast.pressing()):
            self.bumpedE()
        else:
            self.bumperE = False

        if(self.transmissionPower):
            if(self.transmissionEastToWest):
                if(not self.bumperW):
                    mTransmission.spin(REVERSE)
                else:
                    mTransmission.stop()
            else:
                if(not self.bumperE):
                    mTransmission.spin(FORWARD)
                else:
                    mTransmission.stop()
        else:
            mTransmission.stop()
        pass


    def axeCheck(self):
        if(bumperTop.pressing()):
            brain.screen.clear_row(5)
            brain.screen.set_cursor(5,1)
            brain.screen.print('reached top')
            self.bumperT = True
        else:
            self.bumperT = False

        if(self.axePower):
            if(self.axeForward):
                # NEED A SENSOR FOR THE BOTTOM? 
                mAxe.spin(FORWARD)

            else:
                if(not self.bumperT):
                    mAxe.spin(REVERSE)
                else:
                    brain.screen.clear_row(6)
                    brain.screen.set_cursor(6,1)
                    brain.screen.print('top stop ran')

                    if(self.attacking):
                        self.attacking = False
                        self.changeMessage("TRIGGER")
                        self.axeStayAngle()
                        self.release_gear()
                        
                        # wait(1, SECONDS)

                        # self.resetAxe()

                        self.axeStop()
                    else:
                        mAxe.stop()
        else:
            mAxe.stop()
        pass
        
    def exec_axe(self):
        self.attacking = True
        self.engage_gear()
        self.axeRetreat()



    def move(self):
        self.displayUpdate()
        self.transmissionCheck()
        self.axeCheck()

robot = Axe.Axe()

def when_started1():
    global robot, killSwitch

    while(not killSwitch):
        print(encoder_axe.position(DEGREES))
        robot.move()

    brain.screen.set_cursor(4,1)
    brain.screen.print("KILLED")
    robot.stopAllMotors()


def onevent_controller_1buttonY_pressed_0():
    global killSwitch
    killSwitch = True

def onevent_controller_1buttonX_pressed_0():
    global robot
    if(robot.onGear):
        robot.release_gear()
        robot.changeMessage("releasing gear")
    else:
        robot.engage_gear()
        robot.changeMessage("engage gear")

def onevent_controller_1buttonLeft_pressed_0():
    global robot
    robot.changeMessage("E-W")
    robot.trans_E_W()

def onevent_controller_1buttonRight_pressed_0():
    global robot
    robot.changeMessage("W-E")
    robot.trans_W_E()

def onevent_controller_1buttonLeft_released_0():
    global robot
    robot.transStop()

def onevent_controller_1buttonRight_released_0():
    global robot
    robot.transStop()


def onevent_controller_1buttonUp_pressed_0():
    global robot
    robot.axeAdvance()

def onevent_controller_1buttonDown_pressed_0():
    global robot
    robot.axeRetreat()

def onevent_controller_1buttonUp_released_0():
    global robot
    robot.axeStop()

def onevent_controller_1buttonDown_released_0():
    global robot
    robot.axeStop()

def execute_axe():
    global robot
    robot.exec_axe()
    pass


# system event handlers
controller_1.buttonR1.pressed(execute_axe)

controller_1.buttonY.pressed(onevent_controller_1buttonY_pressed_0)
controller_1.buttonX.pressed(onevent_controller_1buttonX_pressed_0)
controller_1.buttonLeft.pressed(onevent_controller_1buttonLeft_pressed_0)
controller_1.buttonRight.pressed(onevent_controller_1buttonRight_pressed_0)
controller_1.buttonLeft.released(onevent_controller_1buttonLeft_released_0)
controller_1.buttonRight.released(onevent_controller_1buttonRight_released_0)
controller_1.buttonUp.pressed(onevent_controller_1buttonUp_pressed_0)
controller_1.buttonDown.pressed(onevent_controller_1buttonDown_pressed_0)
controller_1.buttonUp.released(onevent_controller_1buttonUp_released_0)
controller_1.buttonDown.released(onevent_controller_1buttonDown_released_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()
