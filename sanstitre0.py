# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 00:45:14 2017

@author: Lucas
"""
import imageio
from tkinter import *
import subprocess as sp
from PIL import Image, ImageTk
import PIL
from PIL import Image
import tkinter.messagebox
import numpy as np
import numpy
import subprocess as sp
import scipy as sc
import pylab as pl
import datetime
import cv2
import time
#import Image

x = 500 # largeur
y = 500 # hauteur
myFrameNumber = 50
cap = cv2.VideoCapture("2ms.mp4")

fenetre = Tk()


canvas_img = Canvas(fenetre, width=x, height=y, bg='ivory')
canvas_img.pack(side="top", fill="both", expand=True)


# get total number of frames
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# check for valid frame number
if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
    # set frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

for i in range(0,int(totalFrames)):
    ret, frame = cap.read()
    #cv2.imshow("2ms.mp4", frame)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(img)
    canvas_img.create_image(0, 0, anchor=NW, image=img)
    canvas_img.pack()
    fenetre.update
    time.sleep(0.5)

fenetre.mainloop