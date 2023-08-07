import cv2 as cv
import tkinter
from TumerDisplay import *
from PIL import Image
from TumorPridiction import *
from tkinter import filedialog
from fr import *

class Graphics:

    FirFra = object()

    MainW = 0
    
    Frlist = list()
    
    val = 0

    fileN = 0
    
    DT = object()

    wHeight = 700
    
    wWidth = 1180

    def __init__(self):

        global MainW
        
        MainW = tkinter.Tk()
        
        MainW.geometry('1190x730')
        
        MainW.resizable(width=False, height=False)

        self.fileN = tkinter.StringVar()

        self.DT = TumerDisplay()

        

        self.FirFra = Frames(self, MainW, self.wWidth, self.wHeight, 0, 0)

        self.FirFra.ViewBTN['state'] = 'disable'

        self.Frlist.append(self.FirFra)

        LBWiN = tkinter.Label(self.FirFra.getFrames(), text="Brain-Tumor Detection Using MRI Image", height=1, width=40)

        LBWiN.place(x=320, y=30)

        LBWiN.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()

        RB1 = tkinter.Radiobutton(self.FirFra.getFrames(), text=" Select this to Detect Tumor", variable=self.val, value=1, command=self.check)

        RB1.place(x=250, y=200)
        
        RB2 = tkinter.Radiobutton(self.FirFra.getFrames(), text="View Brain Tumor",variable=self.val, value=2, command=self.check)

        RB2.place(x=260, y=260)

        browseBtn = tkinter.Button(self.FirFra.getFrames(), text="Select Image", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        MainW.mainloop()

    def getlistOfWinFrame(self):
        return self.Frlist

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileN = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileN)
        NIMG = str(self.fileN)
        mriImage = cv.imread(NIMG, 1)
        self.Frlist[0].readImage(image)
        self.Frlist[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        global mriImage
        #print(mriImage)
        if (self.val.get() == 1):
            self.Frlist = 0
            self.Frlist = list()
            self.Frlist.append(self.FirFra)

            self.Frlist[0].setCallObject(self.DT)

            res = TumorPridiction(mriImage)
            
            if res > 0.5:
                resLabel = tkinter.Label(self.FirFra.getFrames(), text="Brain Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Times", 18, "bold"), fg="blue")
            else:
                resLabel = tkinter.Label(self.FirFra.getFrames(), text="No Brain Tumor ", height=1, width=20)
                resLabel.configure(background="White", font=("Times", 18, "bold"), fg="red")

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.Frlist = 0
            self.Frlist = list()
            self.Frlist.append(self.FirFra)

            self.Frlist[0].setCallObject(self.DT)
            self.Frlist[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainW, self.wWidth, self.wHeight, self.DT.TumerDisplay, self.DT)

            self.Frlist.append(secFrame)


            for i in range(len(self.Frlist)):
                if (i != 0):
                    self.Frlist[i].hide()
            self.Frlist[0].unhide()

            if (len(self.Frlist) > 1):
                self.Frlist[0].ViewBTN['state'] = 'active'

        else:
            print("Error")

mainObj = Graphics()