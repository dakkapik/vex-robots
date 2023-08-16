#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_drive_smart = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
mAxe = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
mTransmission = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
encoderAxe = Encoder(brain.three_wire_port.a)
EncoderTrans = Encoder(brain.three_wire_port.c)
bumperEast = Bumper(brain.three_wire_port.e)
bumperTop = Bumper(brain.three_wire_port.f)
bumperWest = Bumper(brain.three_wire_port.g)


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

                        wait(10, MSEC)

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

robot = Axe()

def when_started1():
    global robot, killSwitch

    while(not killSwitch):
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
