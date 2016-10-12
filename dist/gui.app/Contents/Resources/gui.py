#!/usr/bin/python
from Tkinter import Tk, Label, Frame, Entry, StringVar, LEFT, RIGHT, TOP, BOTTOM, Button
import Tkconstants, tkFileDialog
import run
import time

class Gui():
    def __init__(self):



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

        #output file
        self.fileOut = None
        #output file label
        self.fileOutLabel = StringVar()
        #initial status
        self.fileOutLabel.set('')
        #Status report
        self.fileLable = Label(self.root, textvariable = self.fileOutLabel)
        self.fileLable.pack()

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

        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

        #show the window
        self.root.mainloop()

    #function to set the output
    def setOutput(self):
        temp = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
        self.fileOutLabel.set(temp.name)
        self.fileOut = temp.name
        print self.fileOut

    #function to run the program
    def sub(self):
        self.statLabel.config(foreground="black")
        self.status.set('Processing')
        url = self.entry.get()
        if url:
            try:
                if self.fileOut:
                    run.getText(url, fileOut = file(self.fileOut, 'w'))
                    self.status.set('Done')
                    self.statLabel.config(foreground="magenta")
                else:
                    self.setOutput()
                    run.getText(url, fileOut = file(self.fileOut, 'w'))
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
