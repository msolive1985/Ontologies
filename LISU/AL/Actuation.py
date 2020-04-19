import os
import sys
import socket
import pyautogui

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from Data.DataSource import *


# T: x,y,z R: x,y,z
roll = 0.0
pitch = 0.0
yaw = 0.0

# For the actions coming from the ontology
list_macros = []
macro_name = ""
array_index = 0

# For the speed of Drishti
speed = 0.0
# For the angle in Drishti_VE
angle = 0

class Macros:
    def __init__(self,controller_name):
        self.controller_name = controller_name
        self.header = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX lisu: <https://personalpages.manchester.ac.uk/staff/mario.sandovalolive/ontology/idoo.owl#>"""

    def Get_All_Macros(self):
        list_macros = []

        graph = Graph()
        graph.parse("C:/Users/mso_2/Documents/nDoF project/Ontologies/idoo.owl")

        query_string = """ %s
        SELECT ?controller ?actions ?level ?macros ?name
        WHERE
        {
        ?controller lisu:productName ?name  .
        ?controller lisu:Executes ?actions.
        ?controller lisu:isAppropriate ?level .
        ?actions lisu:macroName ?macros .
        FILTER(?name = "%s")
        }
        GROUP BY ?controller ?actions ?macros ?name ?level""" % (self.header, self.controller_name)

        _query = graph.query(query_string)

        for row in _query:
            list_macros.append(row.macros)

        return list_macros

def send_packet(val):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 7755
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    byt = val.encode()
    sock.sendto(byt, (UDP_IP, UDP_PORT))

def lowpassFilter(input_pwn):
    if input_pwn <= 0.3 and input_pwn >= -0.3:
        input_pwn = 0.0

    elif input_pwn > 1.0:
        input_pwn = 1.0

    elif input_pwn < -1.0:
        input_pwn = -1.0

    return input_pwn

def getSpeed():
    global speed
    if speed == 0.0:
        speed = 0.125 # This is the slowest, but get value based on Hz
    return(speed)

def getMacros(joystick_productName):
    global list_macros
    global macro_name

    # Creates an object of type macro based on the controller
    obj_macro = Macros(joystick_productName)
    list_macros = obj_macro.Get_All_Macros()

    # Sets with the initial value
    #macro_name = list_macros[0]

def packetHandler(xAxis, yAxis, zAxis):
    global macro_name

    xAxis = (-1) * roll
    yAxis = (-1) * pitch
    zAxis = (-1) * yaw

    if (macro_name != "") and (xAxis != 0.0 or yAxis != 0.0 or zAxis != 0.0):
        if macro_name == "clipping":
            if xAxis > 0:
                pyautogui.press('left')
                print("Moving left")
            elif xAxis < 0:
                pyautogui.press('right')
                print("Moving right")
            elif yAxis > 0:
                pyautogui.press('up')
                print("Moving up")
            elif yAxis < 0:
                pyautogui.press('down')
                print("Moving down")
        else:
            packet = "{} {} {} {} {}".format(macro_name, float(xAxis), float(yAxis), float(zAxis), int(angle))
            print(packet)
            send_packet(packet)

def leftTrigChangeHandler(val):
    """Callback function which displays the position of the left trigger whenever it changes"""
    global yaw
    yaw = 0.0
    if lowpassFilter(val) != 0.0:
        yaw = val
        #print("Left Trigger position changed: {}".format( val ) )

def rightTrigChangeHandler(val):
    """Callback function which displays the position of the left trigger whenever it changes"""
    global yaw
    yaw = 0.0
    if lowpassFilter(val) != 0.0:
        yaw = val
        #print("Right Trigger position changed: {}".format( val ) )


def leftStickChangeHandler( valLR, valUD ):
    """Callback function which displays the position of the left stick whenever it changes"""
    global roll
    roll = 0.0
    if lowpassFilter(valLR) != 0.0 or lowpassFilter(valUD) != 0.0:
        #print("Left Stick position changed: L-R {}, U-D {}".format( valLR, valUD ) )
        roll = lowpassFilter(valLR + valUD)

def rightStickChangeHandler( valLR, valUD ):
    """Callback function which displays the position of the left stick whenever it changes"""
    global pitch
    pitch = 0.0
    if lowpassFilter(valLR) != 0.0 or lowpassFilter(valUD) != 0.0:
        #print("Right Stick position changed: L-R {}, U-D {}".format( valLR, valUD ) )
        pitch = lowpassFilter(valLR + valUD)

def hatHandler(valLR, valUD):
    """ Handler function for an joystick hat """
    print("Digital Hat Changed: L/R:{} U/D:{}".format(valLR,valUD) )

def btnHandler(val):
    """ Handler function for a button """
    print("Button State Changed. Value={}".format(val) )

def triangleBtnHandler(val):
    global array_index
    global macro_name

    """ Handler function for the triangle button """
    if val == 1 :
        array_index = array_index + 1
        if array_index >= len(list_macros):
            array_index = 0

        macro_name = list_macros[array_index].rstrip()
        print("Triangle button pressed. Macro selected: {}".format(macro_name))

        if macro_name == "clipping":
            pyautogui.mouseDown()
        else:
            pyautogui.mouseUp()

def squareBtnHandler(val):
    global angle

    """ Handler function for the square button """
    if val == 1 :
        angle = angle - 5
        if angle < 0:
            angle = 90

        print("Square button pressed. Angle reduced: {}".format(angle))

def circleBtnHandler(val):
    global speed

    """ Handler function for the circle button """
    if val == 1 :
        speed = speed + speed
        if speed >= 1:
            speed = 0.125

        print("Circle button pressed. Speed selected {}".format(speed))

def crossXBtnHandler(val):
    global angle

    """ Handler function for the cross button """
    if val == 1 :
        angle = angle + 5
        if angle > 90:
            angle = 0

        print("Cross button pressed. Angle increased: {}".format(angle))
