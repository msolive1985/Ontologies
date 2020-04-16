import qprompt
import os
import sys

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from Transport.ThreadPool import *
from Data.DataSource import *

# Future: this comes from ontology as well!
Unity_3D = "Unity 3D"
Drishti_VE = "Drishti"

@qprompt.status("Checking ontology...")
def print_controllers():
    #Data for supported controllers
    qprompt.clear()
    print("SUPORTED DEVICES:")
    retr_ont = List_All_Controllers()
    for row in retr_ont:
        print("Controller '{}' with {} axes".format(row.name, row.AXES))

    print("CONNECTED DEVICES:")
    con_con = get_controllers()
    for row in con_con:
        print("Controller '{}' connected...".format(row.productName))

    qprompt.ask_yesno(default="y")
    qprompt.clear()


def print_synthesizer():
    os.system('cls')
    print("Under construction...")

if __name__ == "__main__":

    qprompt.clear()

    qprompt.echo("LISU (Library for Interactive Settings and Users-modes) 2020")
    qprompt.wrap("Please select one option depending on your skills...", "LISU", width=10)

    qprompt.echo("'Multiplayer' is the traditional mode, sets a controller per player.")
    qprompt.echo("'Synthesizer' is used to set master/slave controllers.")
    qprompt.echo("'Controller' list all the controllers in the OS.")

    menu = qprompt.Menu()
    menu.add("1", "Multiplayer Unity", mainLisuControllers, [Unity_3D])
    menu.add("2", "Multiplayer Drishti", mainLisuControllers, [Drishti_VE])
    menu.add("3", "Synthesizer", print_synthesizer)
    menu.add("4", "Supported devices", print_controllers)
    menu.add("q", "quit")

    while "q" != menu.show():
        pass

    qprompt.clear()
    #choice = menu.show()
