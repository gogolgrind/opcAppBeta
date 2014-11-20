# -*- coding: utf-8 -*-
from classes import opcClient,Application
from Tkinter import *

def makeWidget():
    root = Tk()
    root.title("Простой OPC клиент")
    app = Application(master=root)
    app.mainloop()
    app.opc.client.close()
    root.destroy()
makeWidget()
