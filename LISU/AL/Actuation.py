import os
import sys
import socket

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from Data.DataSource import *

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

roll = 0.0
pitch = 0.0
yaw = 0.0

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

def packetHandler(xAxis, yAxis, zAxis):
    xAxis = roll
    yAxis = pitch
    zAxis = yaw
    if xAxis != 0.0 or yAxis != 0.0 or zAxis != 0.0:
        packet = "addrotation {} {} {}".format( float(xAxis), float(yAxis), float(zAxis) )
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
    """ Handler function for the triangle button """
    if val == 1 :
        print("Triangle button pressed")
    else:
        print("Triangle button released")
