# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:15:51 2016

@author: Lucas
"""
import pylab as pl
import numpy
import numpy as np
from skimage import morphology
from skimage import segmentation
import subprocess as sp
import datetime
import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
from scipy import interpolate
import cv2
from skimage import data, io
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
from xlwt import Workbook
import scipy as sc
from timeit import default_timer 
#from temp import display_pourc
#import Interface



def video_load(name):
    """
    Fonction permettant la creation d'un pipeline pour l'ouverture de la video qui se nomme name
    Pour récupérer les images une à une il faut alors utiliser la fonction lecture video
    """
    command = ['ffmpeg.exe', '-i', name, '-f', 'image2pipe', '-pix_fmt','rgb24','-vcodec','rawvideo','-']
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    return pipe

def lecture_video(pipe,xmin,ymin,xmax,ymax):
    """
    Fonction permettant l'ouverture d'une image de la video Load dans la fonction video_load
    Elle prend en argument le pipeline de la video a ouvrir
    """
    raw_image = pipe.stdout.read(1080*1920*3) # Extraction de l'ensemble des données d'une image
    image = np.fromstring(raw_image, dtype='uint8') # Normalisation des données en int 8 bits
    image = image.reshape((1080,1920,3)) # Mise en forme des donnée en une image en RGB de taille 1080x1920
    image = image[xmin:ymin,xmax:ymax]
    image = processeuil(image, 180)
    #minim_value = 255*minim # booleen to int
    #image = 255*image
    #image = image>180
    pipe.stdout.flush() # Suppression du buffer  
    #pl.figure()
    #pl.imshow(image)
    #pl.show()
    return image#[:,:,0]
  
def count_color_pix(img):
    count=0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 250:
                        count+=255
    print(count)
    return(count)

#min_value=0
#max_values=34425000

def processeuil(img,thre): #conda install -c conda-forge opencv 
    img=img[:,:,0]# Canal B
    img = cv2.split(img)[0] # import cv2
    kernel = numpy.ones((6, 6), numpy.uint8) # kernel 8x8
    (retVal, img) = cv2.threshold(img, thre, 255, cv2.THRESH_BINARY) #seuillage 
    #pl.figure()
    #pl.imshow(img)
    #pl.show()
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    #img = cv2.erode(img, kernel, iterations = 1) # erosion 8x8
    #if count_color_pix(img) >= 350000:
        #img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 10)
    return img

def callback():
    if askretrycancel('Error message', 'Voulez vous precisez la selection ?'):
        Interface.proc(videoname)
    else:
        showerror('Error message', "Relancez le programme")

def finished_traitement():
    showinfo("Boite de dialogue", "Le traitement de la video est terminé")

def determine_points(image):
    global list_pt_x,list_pt_y
    list_pt_x = []
    list_pt_y = []
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] > 100:
                list_pt_x.append(i)
                list_pt_y.append(j)
    return list_pt_x,list_pt_y


def calcul_reg_line(list_pt_x,list_pt_y):
    if list_pt_x and list_pt_y != 0:
        reg = np.polyfit(list_pt_y, list_pt_x, 1)
        return reg

def reg_line_plot(image, reg):
    for k in range(len(image[0])):
        y = int(reg[0]*k + reg[1])
        if y > 0 and y < len(image):
            image[y][k] = 100
    io.imshow(image)
    plt.show()
#    canvas = Canvas(fenetre,width=350, height=200)
#    canvas.create_image(0, 0, anchor=NW, image=image)
#    canvas.pack()
                    #io.imshow(image)
                    #io.show()
                    #pl.figure()
                    #pl.imshow(image)
                    #pl.show()c


def moyim(n,pipe):
    sommim = np.zeros((150,350)) #genere une matrice de 0 aux bonnes dimensions
    print( "Moyenne sur",n,"images"  )
    for i in range (n):
        image_tmp = lecture_video(pipe)
        imagepreprocess = PreProcess(image_tmp,x1, y1, x2, y2)
        sommim = sommim + imagepreprocess
    moy = (sommim/n)
    moy_bin = moy #< 180
    #moy_bin = moy*moy_bin
#io.imsave(name,image_bin)
    
    io.imshow(moy_bin)
    io.show()
    return moy_bin


#m0=infini = float('inf')
    
#[-2.9335539466240941, -1.944600845930706, -0.69897235332654417, -0.72440310547240627, -0.46364247734710246, -0.26939304237011485, -0.19267223727052094, 0.13794022023411831]
"""
m0=-4
m09=-2.7865932
m1=-2.0388858
m15=-0.8956175812
m2=-0.6290396
m35=-0,4
m4=-0.2825853
m5=-0.15290801
m6=-0.097355562
m7=0 #>=
xabs = [m0,m09,m1,m15,m2,m4,m5,m6,m7]
yord = [0,0.9,1,1.5,2,4,5,6,100]
Mod = interp1d(xabs, yord, kind='cubic')
"""

mn09=-2.9335
mn1=-1.9446
mn15=-1
mn2=-0.72440310
mn3=-0.463642477347
mn4=-0.269393042370
mn5=-0.192672237
mn6=0.1379402202341
xabs1 = [mn09,mn1,mn15,mn2,mn3,mn4,mn5,mn6]
yord1=[0.9,1,1.5,2,3,4,5,6]
#Mod = interp1d(xabs1, yord1, kind='cubic')
Mod = interpolate.interp1d(xabs1, yord1, fill_value='extrapolate')




def cf(r):
    r=float(r)*100
    r=int(r)/100
    return r

def cb(r):
    r=int(r)
    return r

def Proc(r):
    if Mod(r)<0:
        a="Vent trop faible"
        #print( a)
        return a
    elif Mod(r)>7:
        a="Vent trop fort et instable"
        #print( a)
        return a
    else:
        a=Mod(r)
        #print(r)
        return a


  
def PourcExe(nbexe, duree):
    p=float(nbexe)/float(duree)*100
    p=p*10
    p=int(p)
    p=float(p)/10
    global pourc
    pourc=str(p)+'%'
    return pourc

ListTps=[]
def TempsExe(temps, duree):
    ListTps.append(temps)
    tempsmoy=moyliste(ListTps)
    tempssom=sommeliste(ListTps)
    tempstotmoy=duree*tempsmoy
    tempsrestant= int(tempstotmoy - tempssom)
    print('Il reste ',decoupe(tempsrestant), ' de temps de traitement')
    return tempsrestant

def decoupe(s):
    if s < 60:
        s=str(s)+'s'
        return s
    elif s >= 60 and s <3600:
        m=str(cb(s/60))+'mn'
        s=str(s%60)+'s'
        if m != 0:
            return m,s
        else:
            return s
    else:
        h=str(cb(s/3600)) +'h'
        m=str(cb((s%3600)/60)) +'mn'
        s=str((s%3600)%60) + 's'
        if h!=0:
            return h,m,s
        else:
            return m,s
    
"""
def decoupe(s):
    heure = str(cf(s)/3600)+'h'
    minute = str(cf(s)/60)+'mn'
    seconde = str(s)+'s'
    if s >= 3600:
        return heure
    elif s >= 60:
        return minute
    else:
        return seconde
"""
    #print( "Temps d'execution pour la ",c,"éme seconde : ", temps,'s')    
def moyliste(L):
    compteur=0
    n=len(L)
    for i in range(0,n):
        compteur+=float(L[i])
    moyenne=float(compteur)/n
    return moyenne

def sommeliste(L):
    compteur=0
    n=len(L)
    for i in range(0,n):
        compteur+=L[i]
    return compteur

global pourc
pourc="0%"

def proc():
    # Definir la durée du temps d'analyse EN SECONDE
    
    fname = askopenfilename(filetypes=(("*.avi", "*.mp4"),("All files", "*.*") ))
    Lname=[]
    Lname[:0]=str(fname)
    Lname_=Lname[::-1] 
    videoname_=[]
    for i in range(0,len(Lname)-1):
        if Lname_[i] == '/':
            break
        else:
            videoname_.append(Lname_[i])
            
    global videoname
    videoname=''.join(videoname_[::-1])
    print(videoname)
    
    
    command = ['ffmpeg.exe', '-i', videoname, '-f', 'image2pipe', '-pix_fmt','rgb24','-vcodec','rawvideo','-']
    vid = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    image = vid.stdout.read(1080*1920*3) # Extraction de l'ensemble des données d'une image
    image = np.fromstring(image, dtype='uint8') # Normalisation des données en int 8 bits
    image = image.reshape((1080,1920,3)) # Mise en forme des donnée en une image en RGB de taille 1080x1920
    vid.stdout.flush() # Suppression du buffer          image = image[xmin:ymin,xmax:ymax] 
    
    class CoordinateStore:
        def __init__(self):
            self.points = []
    
        def select_point(self,event,x,y,flags,param):
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    cv2.circle(image,(x,y),3,(255,0,0),-1)
                    self.points.append((x,y))
    
    
    #instantiate class
    coordinateStore1 = CoordinateStore()
    
    
    # Create a black image, a window and bind the function to window
    
    # Ajouter le canvas ici
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',coordinateStore1.select_point)
    
    while(1):
        cv2.imshow('image',image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    
    print ("Coordonnes selectionnees")
    
    x = [y for x,y in coordinateStore1.points]
    y = [x for x,y in coordinateStore1.points]
    
    xmin=x[0]
    ymin=y[0]
    xmax=x[1]
    ymax=y[1]
    
    
    duree=10
    
    
    
    print(xmin,ymin,xmax,ymax)

    #Namefilexls= 'bilan'
    #book = Workbook()
    #feuil1 = book.add_sheet('Vitesse(temps)')
    #ligne1 = feuil1.row(0)
    #ligne2 = feuil1.row(1)
    #
    #t=[0.9,1,1.5,2,2.5,3,3.2,3.5,4,5,6]
    #for i in range(0,len(t)):
    #    video=t[i]
    #    videoname=str(video)+'ms.mp4'
    
    
    # Enregistrement des données sur un fichier Excel
            
    Namefilexls= str(videoname) + '.xls'
    book = Workbook()
    feuil1 = book.add_sheet('Vitesse(temps)')
    feuil1.write(0,0,'Secondes de la video')
    feuil1.write(1,0,'Vitesses mesurees (m/s)')
    ligne1 = feuil1.row(0)
    ligne2 = feuil1.row(1)
    
    
    """Debut du programme"""
    print("Debut du programme, ouverture")
    pipe=video_load(videoname)
    Lvitesse=[] 
    L=[]
    
    for c in range(0,duree):
        list_reg_s = []
        date1 = datetime.datetime.now()
        ips=0
        for k in range (5,25,5): #Nombre de secondes de video a traiter
            #image=moyim(25, pipe) # Ouverture, recadrage, seuillage, moyenne sur 25 images et affichage
            image = lecture_video(pipe,xmin,ymin,xmax,ymax) #200,500,500,950 x1, y1, x2, y2
    #        pl.figure()
    #        pl.imshow(image)
    #        pl.show()
    
            # Détermination des points du fanion
            list_pt_x = []
            list_pt_y = []
            for i in range(len(image)):
                for j in range(len(image[0])):
                    if image[i][j] > 100:
                        list_pt_x.append(i)
                        list_pt_y.append(j)

            # Calcul de la regression lineaire
            #calcul_reg_line(list_pt_x,list_pt_y)
            if list_pt_x and list_pt_y != 0:
                reg = np.polyfit(list_pt_y, list_pt_x, 1)
            else:
                callback()
        
            #print (reg[0]) # reg = [a,b]  tel que  y=a*x+b
        
            # Affichage de la droite de regression lineaire
        
            for k in range(len(image[0])):
                y = int(reg[0]*k + reg[1])
                if y > 0 and y < len(image):
                    image[y][k] = 100
            io.imshow(image)
            #plt.show()
            
            #canvas.create_image(0, 0, anchor=NW, image=image)
            #canvas.pack()
    
    
    
    
        # Calcul de la mediane des valeurs de pente
            if reg[0] < 0:
                list_reg_s.append(reg[0])
            else:
                image = image[xmin-50:ymin-50,xmax+50:ymax+50]
                determine_points(image)
                calcul_reg_line(list_pt_x,list_pt_y)
                list_reg_s.append(reg[0])
            #Lvitesse.append(Mod(reg[0])) # Utilisation de la fonction interpolation
    
    
        c+=1
        temps = (datetime.datetime.now()-date1).total_seconds()
        print( "Temps d'execution pour la",c,"éme seconde : ", temps,'s')
            
        r = np.median(list_reg_s)
        # Determinations de la vitesse du vent sur une seconde
        b = Mod(r) # Utilisation de la fonction interpolation
        a = Proc(r)
        L.append(a)
        global pourc
        pourc = PourcExe(c,duree)
        TempsExe(temps,duree)
        print("")
        
        # Sauvegarde sur un fichier Excel
        ligne1.write(c,c)
        if isinstance(a, str) == True:
            #sligne2.write(c,cf(a))
            a=str(a)
            ligne2.write(c,a)#a
            Lvitesse.append(a)
        else:
            a=cf(a)
            ligne2.write(c,a)#a
            Lvitesse.append(str(a)+'ms')
        print(pourc)
    
        
        
    #    ligne1.write(c,video)
    #    ligne2.write(c,lr)
    
#    Lvitesse.append(b)
#    print(Lvitesse)
#    L_=[]
#    for i in range(0,len(L)):
#        L_.append(float(L[i]))
#    plt.plot(L_)
#    plt.show()
    book.save(Namefilexls)
    print("Fin du traitement")
    finished_traitement()

fenetre = Tk()

label = Label(fenetre,text ="ANALYSE DU VENT POUR TIR A LA CARABINE",bg="grey")
label.pack()

bouton = Button(fenetre, text = "Select video",command = proc)
bouton.pack() #affiche le bouton dans la fenetre

global canvas_img
global canvas_pourc
global canvas_temps

canvas_img = Canvas(fenetre, width=350, height=300, bg='ivory')
canvas_img.pack(side="left", fill="both", expand=True)
fenetre.mainloop() 
    