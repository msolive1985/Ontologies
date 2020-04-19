import os
import sys
import time
import pygame
from pygame.locals import *

PS4Controller = "Wireless Controller"
XBoxController = "Controller (XBOX 360 For Windows)"
PCGameController = "PC Game Controller"
Unity_3D = "Unity 3D"

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from AL.Actuation import *
from AL.Gamepads import *

xAxis = 0.0
yAxis = 0.0
zAxis = 0.0

def lowpassFilter(input_pwn):
    if input_pwn <= 0.3 and input_pwn >= -0.3:
        input_pwn = 0.0

    elif input_pwn > 1.0:
        input_pwn = 1.0

    elif input_pwn > 1.0:
        input_pwn = 1.0

    elif input_pwn < -1.0:
        input_pwn = -1.0

    return input_pwn

def pwmConversion(input_pwm):
    return((input_pwm * -0.1) + 0.1)

# This represents a independent controller
def Joystick(joystick_productName, virtual_environment):
    cnt = LisuController("Game Controller", initStatus, joystick_productName,
                          leftTriggerChanged = leftTrigChangeHandler,
                          rightTriggerChanged = rightTrigChangeHandler,
                          leftStickChanged = leftStickChangeHandler,
                          rightStickChanged = rightStickChangeHandler,
                          #hatChanged = hatHandler,
                          triangleBtnChanged = triangleBtnHandler,
                          squareBtnChanged = squareBtnHandler,
                          circleBtnChanged = circleBtnHandler,
                          crossXBtnChanged = crossXBtnHandler)

    if cnt.initialised :
        keepRunning = True
        getMacros(joystick_productName)
    else:
        keepRunning = False

    # -------- Main Program Loop -----------
    if virtual_environment == Unity_3D:
        while keepRunning == True :
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
            packetHandler(xAxis, yAxis, zAxis)

    else:
        while keepRunning == True :
            current = time.time()
            elapsed = 0
            update_rate = getSpeed()

            keepRunning = cnt.controllerStatus()
            packetHandler(xAxis, yAxis, zAxis)

            while elapsed < update_rate:
                elapsed = time.time() - current

    pygame.quit()

# This represents a master controlling all the controllers
def Synthesizer(joystick_productName):
    print("Under construction...")
