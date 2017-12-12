# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:10:21 2017

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
 

cap = cv2.VideoCapture("2ms.mp4")
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
x = 500 # largeur
y = 500 # hauteur

global value1

def FirstCoord():
    scale1.pack_forget()
    bouton_debut.pack_forget()
    global value2
    value2 = IntVar()
    scale2 = Scale(fenetre, variable=value2,from_=0, to=totalFrames, orient=HORIZONTAL, length=400)
    scale2.pack()
    bouton_fin= Button(fenetre, text = "Fin",command = ScndCoord)
    bouton_fin.pack()
    vdebut=value1.get()
    vfin=value2.get()
    return vdebut, vfin

def ScndCoord():
    print(value1.get())
    print(value2.get())
    
def refreshFrame():
    if float(value1.get()) >= 0 and float(value1.get()) <= totalFrames:
    # set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES,value1.get())
        ret, frame = cap.read()
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        fenetre.update
        canvas_img.create_image(0, 0, anchor=NW, image=img)
        canvas_img.pack()
        time.sleep(0.5)
    
    

fenetre = Tk()


canvas_img = Canvas(fenetre, width=x, height=y, bg='ivory')
canvas_img.pack(side="top", fill="both", expand=True)


value1 = IntVar()
scale1 = Scale(fenetre, variable=value1,from_=0, to=totalFrames, orient=HORIZONTAL, length=400)
scale1.pack()

bouton = Button(fenetre, text = "Refresh",command = "")
bouton.pack()

bouton_debut = Button(fenetre, text = "Debut",command = FirstCoord)
bouton_debut.pack()



#while(1):
#    print(value1.get())
if float(value1.get()) >= 0 and float(value1.get()) <= totalFrames:
# set frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES,40)
    ret, frame = cap.read()
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(img)
    fenetre.update
    canvas_img.create_image(0, 0, anchor=NW, image=img)
    canvas_img.pack()
    #time.sleep(0.5)


    #img=numpy.array(frame)
    #image = img.subsample(4, 4) # divide by 4
    #img=img.resize((x, y), Image.ANTIALIAS)
    #img=numpy.array(img)
    #img = Image.fromarray(img)

    #imageio.imsave("my-image.png", img)
    #img = ImageTk.PhotoImage(Image.open("my-image.png").resize(x, y)) # the one-liner I used in my app
#    label = Label(root, image=img, ...)
##    label.image = img # this feels redundant but the image didn't show up without it in my app
#    label.pack()
#    
#    #image = img.subsample(4, 4) # divide by 4
## image = image.zoom(2, 2)    # zoom x 2
#    label = Label(image=image, bg="White")
    #print(img)
    #img = ImageTk.PhotoImage(img)
    #photo = ImageTk.PhotoImage(Image.open(imgpath))
    #img = img.resize((x,y))

    #cv2.imshow("2ms.mp4", frame)

    


    
fenetre.mainloop()

# get total number of frames

# check for valid frame number

        

#while True:
#    ret, frame = cap.read()
#    cv2.imshow("2ms.mp4", frame)
#    k = cv2.waitKey(20) & 0xFF
#    if k == 27:
#        break

#cv2.destroyAllWindows()






