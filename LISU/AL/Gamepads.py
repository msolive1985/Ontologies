import os
import sys
import time
import pygame
from pygame.locals import *

PS4Controller = "Wireless Controller"
XBoxController = "Controller (XBOX 360 For Windows)"
PCGameController = "PC Game Controller"

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from AL.Actuation import *
from Data.DataSource import *

class FromOntology:
    def __init__(self, ctr_ont):
        self.name = ctr_ont.name
        self.AXES = int(ctr_ont.AXES)
        self.BTNS = int(ctr_ont.BTNS)
        self.HATS = int(ctr_ont.HATS)
        self.leftTriggerIdx = int(ctr_ont.leftTriggerIdx)
        self.rightTriggerIdx = int(ctr_ont.rightTriggerIdx)
        self.leftStickLRIdx = int(ctr_ont.leftStickLRIdx)
        self.leftStickUDIdx = int(ctr_ont.leftStickUDIdx)
        self.rightStickLRIdx = int(ctr_ont.rightStickLRIdx)
        self.rightStickUDIdx = int(ctr_ont.rightStickUDIdx)
        self.leftBtn1Idx = int(ctr_ont.leftBtn1Idx)
        self.rightBtn1Idx = int(ctr_ont.rightBtn1Idx)
        self.leftBtn2Idx = int(ctr_ont.leftBtn2Idx)
        self.rightBtn2Idx = int(ctr_ont.rightBtn2Idx)
        self.hatLeftIdx = int(ctr_ont.hatLeftIdx)
        self.hatRightIdx = int(ctr_ont.hatRightIdx)
        self.hatUpIdx = int(ctr_ont.hatUpIdx)
        self.hatDownIdx = int(ctr_ont.hatDownIdx)
        self.hatIdx = int(ctr_ont.hatIdx)
        self.selectBtnIdx = int(ctr_ont.selectBtnIdx)
        self.startBtnIdx = int(ctr_ont.startBtnIdx)
        self.triangleBtnIdx = int(ctr_ont.triangleBtnIdx)
        self.squareBtnIdx = int(ctr_ont.squareBtnIdx)
        self.circleBtnIdx = int(ctr_ont.circleBtnIdx)
        self.crossXBtnIdx = int(ctr_ont.crossXBtnIdx)

class LisuController:
    #Data for supported controllers
    ctr_ont = []
    retr_ont = List_All_Controllers()
    for row in retr_ont:
        ctr_ont.append(FromOntology(row))

    # Creating tuples
    SUPPORTED_JOYSTICKS = ()
    CONTROLLER_DISPLAY_NAMES  = ()
    #Properties of the controller based on ontology
    AXES = ()
    BTNS = ()
    HATS = ()
    #From ontology, this values needs to be satisfied based on the device description
    #Define indices for each control for the different supported controllers
    leftTriggerIdx = ()
    rightTriggerIdx = ()
    leftStickLRIdx = ()
    leftStickUDIdx = ()
    rightStickLRIdx = ()
    rightStickUDIdx = ()
    leftBtn1Idx = ()
    rightBtn1Idx = ()
    leftBtn2Idx = ()
    rightBtn2Idx = ()
    hatLeftIdx = ()
    hatRightIdx = ()
    hatUpIdx = ()
    hatDownIdx = ()
    hatIdx = ()
    selectBtnIdx = ()
    startBtnIdx = ()
    triangleBtnIdx = ()
    squareBtnIdx = ()
    circleBtnIdx = ()
    crossXBtnIdx = ()

    #Filling Tuples
    num_devices = len(ctr_ont)
    for ctr_idx in range(num_devices):
        SUPPORTED_JOYSTICKS = SUPPORTED_JOYSTICKS + (ctr_ont[ctr_idx].name,)
        CONTROLLER_DISPLAY_NAMES = CONTROLLER_DISPLAY_NAMES + (ctr_ont[ctr_idx].name,)
        AXES = AXES + (int(ctr_ont[ctr_idx].AXES),)
        BTNS = BTNS + (int(ctr_ont[ctr_idx].BTNS),)
        HATS = HATS + (int(ctr_ont[ctr_idx].HATS),)
        leftTriggerIdx = leftTriggerIdx + (int(ctr_ont[ctr_idx].leftTriggerIdx),)
        rightTriggerIdx = rightTriggerIdx + (int(ctr_ont[ctr_idx].rightTriggerIdx),)
        leftStickLRIdx = leftStickLRIdx + (int(ctr_ont[ctr_idx].leftStickLRIdx),)
        leftStickUDIdx = leftStickUDIdx + (int(ctr_ont[ctr_idx].leftStickUDIdx),)
        rightStickLRIdx = rightStickLRIdx + (int(ctr_ont[ctr_idx].rightStickLRIdx),)
        rightStickUDIdx = rightStickUDIdx + (int(ctr_ont[ctr_idx].rightStickUDIdx),)
        leftBtn1Idx = leftBtn1Idx + (int(ctr_ont[ctr_idx].leftBtn1Idx),)
        rightBtn1Idx = rightBtn1Idx + (int(ctr_ont[ctr_idx].rightBtn1Idx),)
        leftBtn2Idx = leftBtn2Idx + (int(ctr_ont[ctr_idx].leftBtn2Idx),)
        rightBtn2Idx = rightBtn2Idx + (int(ctr_ont[ctr_idx].rightBtn2Idx),)
        hatLeftIdx = hatLeftIdx + (int(ctr_ont[ctr_idx].hatLeftIdx),)
        hatRightIdx = hatRightIdx + (int(ctr_ont[ctr_idx].hatRightIdx),)
        hatUpIdx = hatUpIdx + (int(ctr_ont[ctr_idx].hatUpIdx),)
        hatDownIdx = hatDownIdx + (int(ctr_ont[ctr_idx].hatDownIdx),)
        hatIdx = hatIdx + (int(ctr_ont[ctr_idx].hatIdx),)
        selectBtnIdx = selectBtnIdx + (int(ctr_ont[ctr_idx].selectBtnIdx),)
        startBtnIdx = startBtnIdx + (int(ctr_ont[ctr_idx].startBtnIdx),)
        triangleBtnIdx = triangleBtnIdx + (int(ctr_ont[ctr_idx].triangleBtnIdx),)
        squareBtnIdx = squareBtnIdx + (int(ctr_ont[ctr_idx].squareBtnIdx),)
        circleBtnIdx = circleBtnIdx + (int(ctr_ont[ctr_idx].circleBtnIdx),)
        crossXBtnIdx = crossXBtnIdx + (int(ctr_ont[ctr_idx].crossXBtnIdx),)

    #Properties holding program status or controlling behaviour
    DETECTED_JOYSTICK_IDX = -1
    initialised = False
    displayControllerOutput = True
    leftTriggerActivated = False
    rightTriggerActivated = False

    #Initialise controller trigger and button states to their rest position values
    leftTriggerPos = -1.0
    rightTriggerPos = -1.0
    leftStickLR = 0.0
    leftStickUD = 0.0
    rightStickLR = 0.0
    rightStickUD = 0.0
    leftBtn1State = 0
    rightBtn1State = 0
    leftBtn2State = 0
    rightBtn2State = 0
    hatLRState = 0
    hatUDState = 0
    selectBtnState = 0
    startBtnState = 0
    triangleBtnState = 0
    squareBtnState = 0
    circleBtnState = 0
    crossXBtnState = 0

    def __init__(self, title, initStatus, joystick_productName, leftTriggerChanged = None, rightTriggerChanged = None,
                 leftStickChanged = None, rightStickChanged = None,
                 leftBtn1Changed = None, rightBtn1Changed = None,
                 leftBtn2Changed = None, rightBtn2Changed = None,
                 hatChanged = None,
                 selectBtnChanged = None, homeBtnChanged = None, startBtnChanged = None, triangleBtnChanged = None,
                 squareBtnChanged = None, circleBtnChanged = None, crossXBtnChanged = None,
                 mouseDown = None, mouseUp = None):
        #Storereferences to callback functions
        self.initStatus = initStatus
        self.leftTriggerChanged = leftTriggerChanged
        self.rightTriggerChanged = rightTriggerChanged
        self.leftStickChanged = leftStickChanged
        self.rightStickChanged = rightStickChanged
        self.leftBtn1Changed = leftBtn1Changed
        self.rightBtn1Changed = rightBtn1Changed
        self.leftBtn2Changed = leftBtn2Changed
        self.rightBtn2Changed = rightBtn2Changed
        self.hatChanged = hatChanged
        self.selectBtnChanged = selectBtnChanged
        self.startBtnChanged = startBtnChanged
        self.triangleBtnChanged = triangleBtnChanged
        self.squareBtnChanged = squareBtnChanged
        self.circleBtnChanged = circleBtnChanged
        self.crossXBtnChanged = crossXBtnChanged
        self.mouseDown = mouseDown
        self.mouseUp = mouseUp

        controllerFound = False
        lastCount = 0

        #Initialise pygame
        pygame.init()

        # Initialize the joysticks
        pygame.joystick.init()

        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        #Examine joysticks if number changed
        if lastCount != joystick_count :
            lastCount = joystick_count

            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                # Get the name from the OS for the controller/joystick
                if joystick_productName == joystick.get_name().rstrip():
                    name = joystick.get_name().rstrip()
                    print("Joystick {} detected as ".format(i) + name )

                    #Determine whether detected joystick is a supported model type
                    for j in range(0, len(self.SUPPORTED_JOYSTICKS) ) :
                        #Looking for the supporter name text as a substring of the detected full name
                        if self.SUPPORTED_JOYSTICKS[j] in name:
                            self.DETECTED_JOYSTICK_IDX = j
                            break

                    if self.DETECTED_JOYSTICK_IDX > -1 :
                        #Check the controller matches the expected specifications
                        axes = joystick.get_numaxes()
                        if axes == self.AXES[self.DETECTED_JOYSTICK_IDX] :
                            hats = joystick.get_numhats()
                            if hats == self.HATS[self.DETECTED_JOYSTICK_IDX] :
                                btns = joystick.get_numbuttons()
                                if btns >= self.BTNS[self.DETECTED_JOYSTICK_IDX] :
                                    #Set up this controller
                                    self.controller = joystick
                                    controllerFound = True

                                    #Send status success to callback function
                                    self.initStatus(0)
                                    break
                                else:
                                    print("Joystick has {} buttons. Expected at least {}.".format( btns,self.BTNS[self.DETECTED_JOYSTICK_IDX] ) )
                            else:
                                print("Joystick has {} hats. Expected {}.".format( hats,self.HATS[self.DETECTED_JOYSTICK_IDX] ) )
                        else:
                            print("Joystick has {} axes. Expected {}.".format( axes,self.AXES[self.DETECTED_JOYSTICK_IDX] ) )
                    else:
                        print("Unsupported joystick {} detected as ".format(i) + name )

        #Finished trying to detect game controller
        if controllerFound == False :
            #Send status failed to callback function
            self.initStatus(-1)
        else:
            # Used to manage how fast the screen updates
            self.clock = pygame.time.Clock()

            #Set initialised flag to indicate everything is ready
            self.initialised = True

    def controllerStatus(self):
        #Process analogue sticks
        if (self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Get stick postitions
            leftStickLR = self.controller.get_axis( self.leftStickLRIdx[self.DETECTED_JOYSTICK_IDX] )
            leftStickUD = self.controller.get_axis( self.leftStickUDIdx[self.DETECTED_JOYSTICK_IDX] )

            #Call the callback function if defined and stick position has changed since last called
            if (self.leftStickChanged is not None
            and ( self.leftStickLR != leftStickLR or self.leftStickUD != leftStickUD ) ):
                self.leftStickLR = leftStickLR
                self.leftStickUD = leftStickUD
                #create new event
                self.leftStickChanged( self.leftStickLR, self.leftStickUD )

        if (self.rightStickLRIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and self.rightStickUDIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Get stick postitions
            rightStickLR = self.controller.get_axis( self.rightStickLRIdx[self.DETECTED_JOYSTICK_IDX] )
            rightStickUD = self.controller.get_axis( self.rightStickUDIdx[self.DETECTED_JOYSTICK_IDX] )

            #Call the callback function if defined and stick position has changed since last called
            if (self.rightStickChanged is not None
            and ( self.rightStickLR != rightStickLR or self.rightStickUD != rightStickUD ) ):
                self.rightStickLR = rightStickLR
                self.rightStickUD = rightStickUD
                #create new event
                self.rightStickChanged( self.rightStickLR, self.rightStickUD )

        #Process analogue triggers
        if self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] != -1 :
            #Get trigger value
            leftTrigger = self.controller.get_axis( self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] )
            #Analogue triggers return zero until first used, even through their rest status is -1
            #so we need to detect the first time they return a non-zero value to activate them and
            #start returning their value to the callback function.
            if self.leftTriggerActivated == False :
                if leftTrigger != 0.0 :
                    self.leftTriggerActivated = True

            #Call the callback function if defined and trigger position has changed since last called
            if (self.leftTriggerChanged is not None
            and self.leftTriggerActivated == True
            and self.leftTriggerPos != leftTrigger ):
                self.leftTriggerPos = leftTrigger
                self.leftTriggerChanged( self.leftTriggerPos )

        if self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] != -1:
            #Get trigger value
            rightTrigger = self.controller.get_axis( self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] )
            #Analogue triggers return zero until first used, even through their rest status is -1
            #so we need to detect the first time they return a non-zero value to activate them and
            #start returning their value to the callback function.
            if self.rightTriggerActivated == False :
                if rightTrigger != 0.0 :
                    self.rightTriggerActivated = True

            #Call the callback function if defined and trigger position has changed since last called
            if (self.rightTriggerChanged is not None
            and self.rightTriggerActivated == True
            and self.rightTriggerPos != rightTrigger ):
                self.rightTriggerPos = rightTrigger
                self.rightTriggerChanged( self.rightTriggerPos )

        #Process Hats
        if self.hatIdx[self.DETECTED_JOYSTICK_IDX] != -1:
            hatState = self.controller.get_hat( self.hatIdx[self.DETECTED_JOYSTICK_IDX] )
            hatLR = hatState[0]
            hatUD = hatState[1]
        elif (self.hatUpIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatDownIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatLeftIdx[self.DETECTED_JOYSTICK_IDX] != -1
        and   self.hatRightIdx[self.DETECTED_JOYSTICK_IDX] != -1 ):
            #Process hat buttons where detected as separate buttons
            hatUpBtn = self.controller.get_button( self.hatUpIdx[self.DETECTED_JOYSTICK_IDX] )
            hatDownBtn = self.controller.get_button( self.hatDownIdx[self.DETECTED_JOYSTICK_IDX] )
            if hatUpBtn == 1 :
                hatUD = 1
            elif hatDownBtn == 1 :
                hatUD = -1
            else:
                hatUD = 0
            hatLeftBtn = self.controller.get_button( self.hatLeftIdx[self.DETECTED_JOYSTICK_IDX] )
            hatRightBtn = self.controller.get_button( self.hatRightIdx[self.DETECTED_JOYSTICK_IDX] )
            if hatLeftBtn == 1 :
                hatLR = -1
            elif hatRightBtn == 1 :
                hatLR = 1
            else:
                hatLR = 0

        #Update Hat state if any button states changed
        if (self.hatChanged is not None
        and (self.hatUDState != hatUD or self.hatLRState != hatLR) ):
            self.hatUDState = hatUD
            self.hatLRState = hatLR
            self.hatChanged( self.hatLRState, self.hatUDState )

        #Process buttons
        self.leftBtn1State = self.processButton(
            self.leftBtn1Idx[self.DETECTED_JOYSTICK_IDX],
            "Left Trigger Button 1", self.leftBtn1State, self.leftBtn1Changed)
        self.rightBtn1State = self.processButton(
            self.rightBtn1Idx[self.DETECTED_JOYSTICK_IDX],
            "Right Trigger Button 1", self.rightBtn1State, self.rightBtn1Changed)
        if self.leftTriggerIdx[self.DETECTED_JOYSTICK_IDX] == -1 :
            #No analogue trigger so handle as simple button
            self.leftBtn2State = self.processButton(
                self.leftBtn2Idx[self.DETECTED_JOYSTICK_IDX],
                "Left Trigger Button 2", self.leftBtn2State, self.leftBtn2Changed)
        if self.rightTriggerIdx[self.DETECTED_JOYSTICK_IDX] == -1 :
            #No analogue trigger so handle as simple button
            self.rightBtn2State = self.processButton(
                self.rightBtn2Idx[self.DETECTED_JOYSTICK_IDX],
                "Right Trigger Button 2", self.rightBtn2State, self.rightBtn2Changed)

        self.selectBtnState = self.processButton(
            self.selectBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Select Button", self.selectBtnState, self.selectBtnChanged)
        self.startBtnState = self.processButton(
            self.startBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Start Button", self.startBtnState, self.startBtnChanged)


        self.triangleBtnState = self.processButton(
            self.triangleBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Triangle Button", self.triangleBtnState, self.triangleBtnChanged)
        self.squareBtnState = self.processButton(
            self.squareBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Square Button", self.squareBtnState, self.squareBtnChanged)
        self.circleBtnState = self.processButton(
            self.circleBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "Circle Button", self.circleBtnState, self.circleBtnChanged)
        self.crossXBtnState = self.processButton(
            self.crossXBtnIdx[self.DETECTED_JOYSTICK_IDX],
            "X-Cross Button", self.crossXBtnState, self.crossXBtnChanged)

        # Limit to 20 frames per second
        self.clock.tick(20)

        # Check for quit event
        keepRunning = True
        for event in pygame.event.get(): # User did something
            if ( (event.type == pygame.MOUSEBUTTONDOWN)
            and (self.mouseDown is not None) ):
                self.mouseDown( pygame.mouse.get_pos(), event.button )            

            elif event.type == pygame.QUIT: # If user clicked close
                keepRunning = False # Flag that we are done so we exit this loop

        return keepRunning

    def processButton(self, btnIdx, btnName, lastState, btnCallback):
        """Internal function to handle any button press"""
        if btnIdx != -1:
            #Get button value
            btnState = self.controller.get_button( btnIdx )

            #Call the callback function if defined and button state has changed since last called
            if (btnCallback is not None
            and lastState != btnState ):
                lastState = btnState
                btnCallback( btnState )
        return lastState

## --- Test functions for this module below this line ---
def initStatus( status ):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )


#def main():
    #Test class
    #cnt = RobotController("Game Controller Test", initStatus, XBoxController, leftTriggerChanged = leftTrigChangeHandler,
    #                      leftStickChanged = leftStickChangeHandler)

    #if cnt.initialised :
    #    keepRunning = True

    #else:
    #    keepRunning = False

    # -------- Main Program Loop -----------
    #while keepRunning == True :
        # Trigger stick events and check for quit
        #keepRunning = cnt.controllerStatus()

    #pygame.quit()


#if __name__ == '__main__':
#    main()
