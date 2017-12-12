from tkinter import *
import subprocess as sp
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import numpy as np
import subprocess as sp
from xlwt import Workbook
import scipy as sc
import pylab as pl
import datetime
import cv2
from scipy import interpolate
from scipy.interpolate import interp1d
from tkinter.messagebox import showinfo
#from fonction import PourcExe, TempsExe
    

def choosevid():    
    chemin = askopenfilename()
    cheminsplit = chemin.split('/')
    global name
    name = cheminsplit.pop(len(cheminsplit)-1)
    command = ['ffmpeg.exe', '-i', name, '-f', 'image2pipe', '-pix_fmt','rgb24','-vcodec','rawvideo','-']
    vid = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    image = vid.stdout.read(1080*1920*3) # Extraction de l'ensemble des données d'une image
    image = np.fromstring(image, dtype='uint8') # Normalisation des données en int 8 bits
    image = image.reshape((1080,1920,3))
    global img
    
    tkinter.messagebox.showinfo("Instruction","Selectionnez deux points à l'aide d'un double clic en bas a gauche puis en haut a droite du drapeau puis appuyez sur echap")
    
    class CoordinateStore:
        def __init__(self):
            self.points = []
    
        def select_point(self,event,x,y,flags,param):
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    cv2.circle(image,(x,y),3,(255,0,0),-1)
                    self.points.append((x,y))
                    
    coordinateStore1 = CoordinateStore()    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',coordinateStore1.select_point)
    
    while(1):
        cv2.imshow('image',image)
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
    image = image[xmin:xmax,ymin:ymax]        
    img = Image.fromarray(image)
    img = ImageTk.PhotoImage(img)
    global canvas_img
    #canvas = Canvas(fenetre, width=ymax-ymin, height=xmax-xmin)
    canvas_img = Canvas(fenetre, width=ymax-ymin, height=xmax-xmin, bg='ivory')
    canvas_img.create_image(0, 0, anchor=NW, image=img)
    canvas_img.pack()
    
    
#    canvas.pack(side="left", fill="both", expand=True)
    bouton_traitement = Button(fenetre, text = "Commencer traitement",command = Traitement)
    bouton_traitement.pack()


def Traitement(duree = 10, facteur = 1):
    
    duree_traitement_video = datetime.datetime.now()
    
    command = ['ffmpeg.exe', '-i', name, '-f', 'image2pipe', '-pix_fmt','rgb24','-vcodec','rawvideo','-']
    vid = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    
    Namefile = str(name)+'.xls'
    book = Workbook()
    feuil1 = book.add_sheet('Vitesse(temps)')
    feuil1.write(0,0,'Secondes de la video')
    feuil1.write(1,0,'Vitesses mesurees')
    
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
    Mod = interpolate.interp1d(xabs1, yord1, fill_value='extrapolate')
    
    X = []
    Y = []
    
    for t in range(duree):                          #boucle sur chaque seconde de la video
        duree_traitement_par_sec = datetime.datetime.now() #compteur de temps pour chaque seconde de traitement
        regression_moy_sec = 0                       #(ré)initialisation de la valeur de regression moyenne sur le nombre d'image par seconde
        for i in range(5*t,5*(1+t),facteur):      #boucle sur x image par seconde de video (x entre 1 et 25)
            image = vid.stdout.read(1080*1920*3) # Extraction de l'ensemble des données d'une image
            image = np.fromstring(image, dtype='uint8') # Normalisation des données en int 8 bits
            image = image.reshape((1080,1920,3)) # Mise en forme des donnée en une image en RGB de taille 1080x1920
            vid.stdout.flush() # Suppression du buffer          image = image[xmin:ymin,xmax:ymax] 
            image = image[xmin:xmax,ymin:ymax] #Image recadrée autour du drapeau
            image1 = image[:,:,0] #Image en niveau de rouge
            list_pt_x = []                      #Liste de regression des pixels d'absice pour la ie image de la te seconde
            list_pt_y = []                      #Liste de regression des pixels d'ordonnées pour la ie image de la te seconde
            for p in range(len(image)):         #On parcourt l'image
                for pp in range(len(image[0])):
                    if image1[p][pp] > 175:              #On rajoute les coordonnées des pixels appartenant au drapeau dans les listes
                        list_pt_x.append(p)
                        list_pt_y.append(pp)
            reg = np.polyfit(list_pt_y, list_pt_x, 1)       #Liste des valeurs de regression a et b (y=ax+b)
            if -0.0973 >= reg[0] >= -2.7864:     #si la valeurs correspond a un vent dans le cadre du modele alors
                X.append(i/25)                #on ajoute le temps dans la liste des absices
                Y.append(float(Mod(reg[0])))  #On ajoue la valeur du vent dans la liste des ordonnées
            if i == 25*t:                                  #Affichage images seuillées + droites de reg.(une image par sec affichée)
                for p in range(len(image1)):
                    for pp in range(len(image1[0])):
                        if image1[p][pp] > 175:
                            image[p,pp,0] = 255
                            image[p,pp,1] = 255
                            image[p,pp,2] = 255
                        else :
                            image[p,pp,0] = 0
                            image[p,pp,1] = 0
                            image[p,pp,2] = 0
                        y = int(reg[0]*pp + reg[1])
                        if y > 0 and y < len(image1):
                            image[y,pp,0] = 127
                            image[y,pp,1] = 127
                            image[y,pp,2] = 127
                image = Image.fromarray(image)
                global img
                img = ImageTk.PhotoImage(image)
                
                #canvas_img.create_image(0, 0, anchor=NW, image=img)
                #canvas_img.update_idletasks()     
                
        regression_moy_sec = -sum(Y)/len(Y)
        if regression_moy_sec<-2.7865:
            feuil1.write(0,t+1,t)
            feuil1.write(1,t+1,'Vent trop faible')
        elif regression_moy_sec > -0.0973:
            feuil1.write(0,t+1,t)
            feuil1.write(1,t+1,'Vent trop fort')
        else:
            feuil1.write(0,t+1,t)
            feuil1.write(1,t+1,float(Mod(regression_moy_sec)))
        print("Temps video :",t,"s")
        print((datetime.datetime.now()-duree_traitement_par_sec).total_seconds(),"secondes pour traiter une seconde de video")
    pl.plot(X,Y)  #affichage graphique
    pl.show()
    book.save(Namefile) #sauvegarde du fichier excel
    temps_traitement_total=(datetime.datetime.now()-duree_traitement_video).total_seconds()
    print("Temps traitement total :",temps_traitement_total,"s") #temps tratement total
    print(sum(Y)/len(Y))
    showinfo("Boite de dialogue", "Le traitement de la video est terminé")             
    
    
fenetre = Tk()

label = Label(fenetre,text ="ANALYSE DU VENT POUR TIR A LA CARABINE",bg="grey")
label.pack()

bouton = Button(fenetre, text = "Select video",command = choosevid)
bouton.pack() #affiche le bouton dans la fenetre



#global canvas_img
#global canvas_pourc
#global canvas_temps
#
#canvas_img = Canvas(fenetre, width=xmax-xmin, height=ymax-ymin, bg='ivory')
#canvas_img.pack()
#
#canvas_pourc = Canvas(fenetre, width=140, height=140, bg='gray40')
#canvas_pourc.pack(side="top", fill="both", expand=True)
#
#canvas_temps = Canvas(fenetre, width=140, height=140, bg='gray51')
#canvas_temps.pack(side="bottom", fill="both", expand=True)
#
#text_pourc = canvas_pourc.create_text(70, 70,font=("Purisa", 26, "bold"))
#text_temps = canvas_temps.create_text(70, 70,font=("Purisa", 24, "bold"))
#
#def gen_int():
#    global b
#    b = tk.StringVar()
#    a=random.randint(100,500)
#    b.set(a)
#    #time.sleep(3)
#    return a
#
#def increment_label_forever():
#    text = int(label['text'])
#    text += 1
#    time.sleep(1)
#    label['text'] = gen_int()
#    root.after(10, increment_label_forever)
#
#def display_pourc():
#    global pourc
#    canvas_pourc.itemconfigure(text_pourc, text=b) 
#    fenetre.after(1000, display_pourc) 
#text_pourc = canvas_pourc.create_text(70, 70,font=("Purisa", 26, "bold"))
#
##a = StringVar()
#b=str(random.randint(100,500))+"%"
#print(b)
#display_pourc()
#
#def updateTime(): 
#    if fonction.proc == "False":
#        str_time=0
#    else:
#        now = default_timer() - start 
#        minutes, seconds = divmod(now, 60) 
#        hours, minutes = divmod(minutes, 60) 
#        str_time = "%d:%02d:%02d" % (hours, minutes, seconds) 
#        canvas_temps.itemconfigure(text_clock, text=str_time) 
#        fenetre.after(1000, updateTime) 
#start = default_timer() 
#text_clock = canvas_temps.create_text(70, 70,font=("Purisa", 26, "bold"))
#updateTime()

fenetre.mainloop() #fermeture 