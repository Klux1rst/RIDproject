# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 17:04:55 2017

@author: KluxMastux
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
from tkinter.filedialog import askopenfilename
#import Image
#Set up GUI

global value1
global value2
global valid
global zone_proc
global duree_ttt
valid = "inprogress"


def FirstCoord():
    scale1.pack_forget()
    bouton_debut.pack_forget()
    global value2
    value2 = IntVar()
    #value2 = value1
    scale2 = Scale(sliderFrame, variable=value2,from_=value1.get(), to=totalFrames, orient=HORIZONTAL, length=500)
    scale2.pack()
    global bouton_fin
    bouton_fin= Button(sliderFrame, text = "Fin du traitement",command = ScndCoord)
    bouton_fin.pack()
    global valid
    valid = "ok" 
    return value1,value2

def ScndCoord():
    global valid
    valid = "finish"
    print(value1.get(),value2.get())
    fenetre.destroy()
    #select_coordinate()
    
def time_maj(duree):
    minutes, seconds = divmod(int(duree), 60) 
    hours, minutes = divmod(minutes, 60)
    global time
    time = "%d:%02d:%02d" % (hours, minutes, seconds)
    return time



def show_frame():
    if valid != "finish":
        if valid=="inprogress":
            cap.set(cv2.CAP_PROP_POS_FRAMES,value1.get())
        elif valid=="ok":
            cap.set(cv2.CAP_PROP_POS_FRAMES,value2.get())
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        res = cv2.resize(cv2image,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        img = Image.fromarray(res)
        imgtk = ImageTk.PhotoImage(image=img)
        display1.imgtk = imgtk #Shows frame for display 1
        display1.configure(image=imgtk)
        fenetre.after(10, show_frame)
        
def select_coordinate():
    cap.set(cv2.CAP_PROP_POS_FRAMES,value1.get())
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    res = cv2.resize(cv2image,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    img = Image.fromarray(res)
    imgtk = ImageTk.PhotoImage(image=img)
    display1.imgtk = imgtk #Shows frame for display 1
    display1.configure(image=imgtk)
        
    class CoordinateStore:
        def __init__(self):
            self.points = []
    
        def select_point(self,event,x,y,flags,param):
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    cv2.circle(imgtk,(x,y),3,(255,0,0),-1)
                    self.points.append((x,y))
                    
    coordinateStore1 = CoordinateStore()    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',coordinateStore1.select_point)
#    display1.imgtk = imgtk #Shows frame for display 1
#    display1.configure(image=imgtk)
    
    while(1):
        cv2.imshow('image',res)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    
    coord = coordinateStore1.points
    print(coord)
    global xmin,xmax,ymin,ymax

    xmin = coord[1][1]
    xmax = coord[0][1]
    ymin = coord[0][0]
    ymax = coord[1][0]

    #image = image[xmin:xmax,ymin:ymax] 
    #img = Image.fromarray(image)
    #img = ImageTk.PhotoImage(img)

fenetre = Tk()  #Makes main window
fenetre.wm_title("Duree de traitement")
fenetre.config(background="#FFFFFF")
               
#Graphics window
imageFrame = Frame(fenetre, width=600, height=500)
imageFrame.pack(side="top", padx=5, pady=5)

#Capture video frames
cap = cv2.VideoCapture("C:/Users/Charles Achen/Desktop/Cours/RID/videotest2.mp4")
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
duree_vid=totalFrames/fps
print(duree_vid)
print(time_maj(duree_vid))

display1 = Label(imageFrame)
display1.grid(row=1, column=0, padx=10, pady=2)

sliderFrame = Frame(fenetre, width=600, height=300)
sliderFrame.pack(side="bottom", padx=5, pady=5)

value1 = IntVar()
scale1 = Scale(sliderFrame, variable=value1,from_=0, to=totalFrames, orient=HORIZONTAL, length=500)
scale1.pack()

bouton_debut = Button(sliderFrame, text = "Debut du traitement",command = FirstCoord)
bouton_debut.pack()

show_frame()
fenetre.mainloop()

debut_ttt=float(value1.get()/fps)
temps_ttt=int(value2.get())-int(value1.get())
duree_ttt=temps_ttt/fps
print(duree_ttt)
print(debut_ttt)
print(time_maj(duree_ttt))

