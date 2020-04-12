import qprompt
import os
import sys

filepath = os.path.abspath(os.path.join("/Mario/3.3/LISU", os.pardir))
sys.path.insert(0, filepath + "/LISU")

from Transport.ThreadPool import *

if __name__ == "__main__":

    os.system('cls')

    qprompt.echo("LISU (Library for Interactive Settings and Users -modes) 2020")
    qprompt.wrap("Please select one option depending on your skills...", "LISU", width=10)

    qprompt.echo("'Multiplayer' is the traditional mode, sets a controller per player.")
    qprompt.echo("'Synthesizer' is used to set master/slave controllers.")
    qprompt.echo("'Controller' list all the controllers in the OS.")

    menu = qprompt.Menu()
    menu.add("1", "Multiplayer", mainTraditional)
    menu.add("2", "Synthesizer", mainTraditional)
    menu.add("3", "Controllers", mainTraditional)
    menu.add("q", "quit")

    while "q" != menu.show():
        pass

    #choice = menu.show()
