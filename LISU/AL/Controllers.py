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
                          hatChanged = hatHandler,
                          triangleBtnChanged = triangleBtnHandler,
                          squareBtnChanged = squareBtnHandler,
                          circleBtnChanged = circleBtnHandler,
                          crossXBtnChanged = crossXBtnHandler)

    if cnt.initialised :
        keepRunning = True
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
            getMacros(joystick_productName)
            packetHandler(xAxis, yAxis, zAxis)

            while elapsed < update_rate:
                elapsed = time.time() - current

    pygame.quit()

# This represents a master controlling all the controllers
def Synthesizer(joystick_productName):
    joysticks = []
    clock = pygame.time.Clock()

    pygame.init()

    # Gets the macro from the ontology
    keepPlaying = False
    array_index = 0
    array_actions = Macros(joystick_productName).Get_All_Macros()
    selected_macro = array_actions[array_index]

    # initializing the inoute device
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        if joysticks[-1].get_name().rstrip() == joystick_productName:
            print ("Detected joystick '",joysticks[-1].get_name(),"'")
            keepPlaying = True

    while keepPlaying:

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Received event 'Quit', exiting.")
                keepPlaying = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Escape key pressed, exiting.")
                keepPlaying = False

            elif event.type == pygame.KEYDOWN:
                print("Keydown,", event.key)
            elif event.type == pygame.KEYUP:
                print("Keyup,", event.key)
            #elif event.type == pygame.MOUSEMOTION:
             #   print("Mouse movement detected."

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button",event.button,"down at",pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())

            elif event.type == pygame.JOYAXISMOTION:
                if joystick_productName == PS4Controller:
                    roll = -1 * (joysticks[event.joy].get_axis(0) - joysticks[event.joy].get_axis(1))
                    pitch = -1 * (joysticks[event.joy].get_axis(2) - joysticks[event.joy].get_axis(3))
                    yaw = -1 * (joysticks[event.joy].get_axis(4) -  joysticks[event.joy].get_axis(4))

                elif joystick_productName == XBoxController:
                    roll = lowpassFilter( -1 * (joysticks[event.joy].get_axis(0) + joysticks[event.joy].get_axis(1)))
                    pitch = lowpassFilter( -1 * (joysticks[event.joy].get_axis(3) + joysticks[event.joy].get_axis(4)))
                    yaw = lowpassFilter((joysticks[event.joy].get_axis(2)))

                elif joystick_productName == PCGameController:
                    roll = joysticks[event.joy].get_axis(0)
                    pitch = joysticks[event.joy].get_axis(1)
                    yaw = joysticks[event.joy].get_axis(3)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    array_index = array_index + 1
                    if array_index >= len(array_actions):
                        array_index = 0
                    selected_macro = array_actions[array_index]
                    print("Joystick '",joysticks[event.joy].get_name(),"' action ", selected_macro ," activated.")

                # Increase speed
                elif event.button == 1:
                    pass
                 # decrease speed
                elif event.button == 2:
                    pass

            elif event.type == pygame.JOYHATMOTION:
                if joysticks[event.joy].get_hat(0) == (0, 1):
                    yaw = 1.0
                elif joysticks[event.joy].get_hat(0) == (0, -1):
                    yaw = -1.0
                elif joysticks[event.joy].get_hat(0) == (-1, 0):
                    yaw = 1.0
                elif joysticks[event.joy].get_hat(0) == (1, 0):
                    yaw = -1.0
                elif joysticks[event.joy].get_hat(0) == (0, 0):
                    yaw = 0.0
                #print("Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved.",joysticks[event.joy].get_hat(event.hat))

            if roll != 0.0 or pitch != 0.0 or yaw != 0.0:
                packet = "%s, %s, %s" % (roll, pitch, yaw)
                print("Joystick ''", joystick_productName, "' : " + packet)
