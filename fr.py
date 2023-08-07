import tkinter
from PIL import Image
from PIL import ImageTk


class Frames:
    
    method = object()
    winFrame = object()
    
    Axis_X = 0
    btnClose = object()
    Axis_Y = 0
    ViewBTN = object()
    WinM1 = 0
    image = object()
    
    objectMain = 0
    ObjectCall = object()
    labelImg = 0

    def __init__(self, objectMain, MainWin, wWidth, wHeight, function, Object, Axis_X=10, Axis_Y=10):
        self.Axis_X = Axis_X
        self.Axis_Y = Axis_Y
        self.WinM1 = MainWin
        self.objectMain = objectMain
        self.WinM1.title("Brain Tumor Detection")
        if (self.ObjectCall != 0):
            self.ObjectCall = Object

        if (function != 0):
            self.method = function

        global winFrame
        self.winFrame = tkinter.Frame(self.WinM1, width=wWidth, height=wHeight)
        self.winFrame['borderwidth'] = 5
        self.winFrame['relief'] = 'ridge'
        self.winFrame.place(x=Axis_X, y=Axis_Y)

        self.btnClose = tkinter.Button(self.winFrame, text="Close", width=8,
                                      command=lambda: self.quitProgram(self.WinM1))
        self.btnClose.place(x=1020, y=600)
        self.ViewBTN = tkinter.Button(self.winFrame, text="View", width=9, command=lambda: self.NextWindow(self.method))
        self.ViewBTN.place(x=900, y=600)


    def setCallObject(self, obj):
        self.ObjectCall = obj


    def setMethod(self, function):
        self.method = function


    def quitProgram(self, window):
        global WinM1
        self.WinM1.destroy()


    def getFrames(self):
        global winFrame
        return self.winFrame


    def unhide(self):
        self.winFrame.place(x=self.Axis_X, y=self.Axis_Y)


    def hide(self):
        self.winFrame.place_forget()


    def NextWindow(self, methodToExecute):
        listWF = list(self.objectMain.Frlist)

        if (self.method == 0 or self.ObjectCall == 0):
            print("Calling Object/Method")
            return

        if (self.method != 1):
            methodToExecute()
        if (self.ObjectCall == self.objectMain.DT):
            img = self.objectMain.DT.getImage()
        else:
            print("Err = No getImage() function")

        jpgImg = Image.fromarray(img)
        current = 0

        for i in range(len(listWF)):
            listWF[i].hide()
            if (listWF[i] == self):
                current = i

        if (current == len(listWF) - 1):
            listWF[current].unhide()
            listWF[current].readImage(jpgImg)
            listWF[current].displayImage()
            self.ViewBTN['state'] = 'disable'
        else:
            listWF[current + 1].unhide()
            listWF[current + 1].readImage(jpgImg)
            listWF[current + 1].displayImage()

        print("Step " + str(current) + " Extraction complete!")


    def removeComponent(self):
        self.btnClose.destroy()
        self.ViewBTN.destroy()


    def readImage(self, img):
        self.image = img


    def displayImage(self):
        imgTk = self.image.resize((250, 250), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(image=imgTk)
        self.image = imgTk
        self.labelImg = tkinter.Label(self.winFrame, image=self.image)
        self.labelImg.place(x=700, y=150)
