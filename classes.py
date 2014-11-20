# -*- coding: utf-8 -*-
from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from tkintertable.TablesApp import TablesApp
from datetime import datetime
import OpenOPC
import tkMessageBox
import easygui as eg
import numpy as np

class opcClient():
    def __init__(self,rspntime):
        self.client = OpenOPC.client()
        self.serverName = ''
        self.tags = []
        self.dur = 0
        self.responseTime = 1000*rspntime
        
    def readTagsFromFile(self):
        timeCol = ["Дата","Длит."]
        fileName = eg.fileopenbox()
        f = open(fileName, 'r')
        tgs = f.readlines()
        f.close()
        self.tags = timeCol + tgs

    def connectOPC(self):
        self.serverName = eg.choicebox('Выбери OPC cервер',' ', self.client.servers())
        return self.client.connect(self.serverName,'localhost')

    def getTags(self):
        return [ self.client.read(elem)[0] for elem in self.tags]

class Application(Frame):
    
    def createTable(self,Frame,master):
        tframe = Frame(master)
        tframe.pack()
        self.table = TableCanvas(tframe)
        self.table.createTableFrame()
        self.table.model.createEmptyModel()
        self.table.redrawTable()
        
    def addTagstoTable(self):
        for elem in self.opc.tags:
            self.table.model.addColumn(elem)
        self.table.redrawTable()

    def createMenu(self,master):
        self.menu = Menu(master)
        master.config(menu = self.menu)
        self.fm = Menu(self.menu)
        self.wm = Menu(self.menu)
        self.menu.add_cascade(label = 'Файл', menu = self.fm)
        self.menu.add_cascade(label = 'Опрос', menu = self.wm)
        self.fm.add_command(label = 'Выход',command = self.quit)
        def tryConnect():
            try:
                self.opc.connectOPC()
                self.wm.entryconfig(2,state="normal")
                self.wm.entryconfig(1,state="disabled")
            except:
                tkMessageBox.showerror(' ','Неопознаная ошибка')
                self.quit();
        self.wm.add_command(label = 'Подключится к OPC',command = tryConnect)
        self.wm.add_command(label = 'Старт',command = self.start)
        self.wm.add_command(label = 'Стоп',command = self.stop)
        self.wm.entryconfig(2,state="disabled")
        self.wm.entryconfig(3,state="disabled")

    def updateTable(self):
        if (self.opc.tags == []):
            self.opc.readTagsFromFile()
            self.addTagstoTable()
        fmt = '%d-%m-%y %H:%M:%S'
        now = datetime.now().strftime(fmt)
        self.table.model.addRow()
        r = self.table.model.getRowCount()
        self.table.model.setValueAt(now,r-1,0)
        self.table.model.setValueAt(self.opc.dur,r-1,1)
        tgs = self.opc.getTags()
        for i in range(2,len(tgs)):
            self.table.model.setValueAt(tgs[i],r-1,i)
        self.table.redrawTable()
        if int (self.opc.dur) % 180 == 0 and self.opc.dur != 0:
            self.table.model.save(filename = 'result_' + str(self.opc.dur)+'.table')
        self.opc.dur = self.opc.dur + self.opc.responseTime/1000

    def start(self):
        self.updateTable()
        self.startHandle = self.after(self.opc.responseTime,self.start)
        self.wm.entryconfig(2,state="disabled")
        self.wm.entryconfig(3,state="normal")

    def stop(self):
        self.after_cancel(self.startHandle)
        self.wm.entryconfig(2,state="normal")
        self.wm.entryconfig(3,state="disabled")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.opc = opcClient(3)
        master.resizable(0,0)
        self.createTable(Frame,master)
        self.createMenu(master)
        self.pack()
