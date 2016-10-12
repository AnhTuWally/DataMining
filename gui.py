#!/usr/bin/python

from Tkinter import Tk, Label, Frame, Entry, StringVar, LEFT, RIGHT, TOP, BOTTOM, Button
import Tkconstants, tkFileDialog
import run
import time

class Gui():
    def __init__(self):

        #output file
        self.fileOut = None

        #The window entity
        self.root = Tk(className = 'Text Mining V1.0')
        #Set the default size
        self.root.minsize(250, 80)
        #self.root.geometry("500x150")

        #frame for data entry and clearing
        self.entryFrame = Frame(self.root)
        self.entryFrame.pack(side = TOP)

        #Entry Label
        self.urlLabel = Label(self.entryFrame, text = 'URL')
        self.urlLabel.pack(side = LEFT)
        ##Data entry
        self.entry = Entry(self.entryFrame, width = 80)
        self.entry.pack(side = LEFT)

        #Status report
        self.status = StringVar()
        #initial status
        self.status.set('')
        #Status report
        self.statLabel = Label(self.root, textvariable = self.status)
        self.statLabel.pack()

        #frame for button
        self.buttonFrame = Frame(self.root)
        self.buttonFrame.pack(side = BOTTOM)
        #clear button
        self.clear = Button(self.buttonFrame, text = 'Clear', command = lambda : self.entry.delete(0, 'end'))
        self.clear.pack(side = LEFT)
        #function to submmitt
        self.buttonSub = Button(self.buttonFrame, text='Generate Text', command = self.sub)
        self.buttonSub.pack(side = RIGHT)

        #function to submmitt
        self.buttonSub = Button(self.root, text='Save', command = self.setOutput)
        self.buttonSub.pack()

        #show the window
        self.root.mainloop()

    #function to set the output
    def setOutput(self):
        self.fileOut = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")

    #function to run the program
    def sub(self):
        url = self.entry.get()
        if url:
            self.statLabel.config(foreground="black")
            self.status.set('Processing')
            time.sleep(1000)
            try:
                run.getText(url, fileOut = self.fileOut)
                self.status.set('Done')
                self.statLabel.config(foreground="magenta")
            except:
                self.status.set('Error!')
                self.statLabel.config(foreground="Red")
        else:
            self.status.set('Please entry an URL')
            self.statLabel.config(foreground="Blue")

if __name__ == '__main__':
    a = Gui()
