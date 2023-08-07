import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from fr import *
from TumerDisplay import *
from TumorPridiction import *


class Gui:
    MainW = 0
    listOfWinFrame = list()
    FirFra = object()
    val = 0
    fileN = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainW
        MainW = tkinter.Tk()
        MainW.geometry('1200x720')
        MainW.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileN = tkinter.StringVar()

        self.FirFra = Frames(self, MainW, self.wWidth, self.wHeight, 0, 0)
        self.FirFra.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirFra)

        WindowLabel = tkinter.Label(self.FirFra.getFrames(), text="Brain-Tumor Detection Using MRI Image", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirFra.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirFra.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirFra.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        MainW.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileN = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileN)
        imageName = str(self.fileN)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        global mriImage
        #print(mriImage)
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirFra)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = TumorPridiction(mriImage)
            
            if res > 0.5:
                resLabel = tkinter.Label(self.FirFra.getFrames(), text="Brain Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Times", 18, "bold"), fg="blue")
            else:
                resLabel = tkinter.Label(self.FirFra.getFrames(), text="No Brain Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Times", 18, "bold"), fg="red")

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirFra)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainW, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)


            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if (len(self.listOfWinFrame) > 1):
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")

mainObj = Gui()