import os
import usb.core
import usb.util
import usb.backend.libusb1
import qprompt
import sys

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from multiprocessing import *
from Data.DataSource import *
from AL.Controllers import *

#UDP_IP = "127.0.0.1"
UDP_IP = "192.168.0.1"
UDP_PORT = 7755

def get_controllers():
    controllers_list = []
    BACKEND = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\mso_2\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\libusb\\_platform\\_windows\\x64\\libusb-1.0.dll")
    dev = usb.core.find(find_all=True)
    if dev is None:
        print('Device not found')
    else:
        for d in dev:
            #print('Hexadecimal Vendor ID: ' + hex(d.idVendor) + ' & ProductID: ' + hex(d.idProduct))
            c1 = Controller(hex(d.idVendor), hex(d.idProduct))
            c2 = ControllerManager(c1)
            if hasattr(c2, 'productName'):
                controllers_list.append(c2)
    return controllers_list

def startController(UDP_PORT, i, joystick_productName, virtual_environment):
    PID_proc = os.getpid()
    qprompt.clear()
    print("LISU controller for {}...".format(virtual_environment))
    print("To quit, press ctrl+'c'...")
    print("ID of process running controller {}: {}".format(joystick_productName, PID_proc))
    Joystick(joystick_productName, virtual_environment)

def runInParallel(controllers_list, virtual_environment):
    try:
        proc = []
        no_devices = len(controllers_list)
        #print(str(no_devices))
        qprompt.clear()

        for lx in range(0,no_devices):
            joystick_productName = controllers_list[lx].productName
            #print(joystick_productName)
            #Joystick(joystick_productName)
            p = Process(target=startController, args=(UDP_PORT, lx, joystick_productName,virtual_environment, ))
            p.start()
            proc.append(p)

        for p in proc:
            p.join()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt")
        qprompt.ask_yesno(default="y")
        qprompt.clear()

def mainLisuControllers(virtual_environment):
    controllers_list = get_controllers()
    runInParallel(controllers_list, virtual_environment)

#if __name__ == '__main__':
#    main()
