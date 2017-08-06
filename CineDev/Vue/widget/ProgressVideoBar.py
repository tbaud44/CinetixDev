#-*- coding: utf-8 -*-
'''
Created on 14 mai 2017

@author: Thierry baudouin
classe permettant d'afficher et de controler une barre de progression (timeline).
Cette barre affiche toute les secondes une zone graphique coloree qui agrandit avec le temps jusqu'a une valeur maximale
'''

import time
from tkinter import ttk

import tkinter as tk
from transverse.Util import Util


class Pbar(ttk.Progressbar):
   
    def __init__(self, master=None, strValue=None, **kw):
        
        if not strValue:
            strValue = tk.StringVar()
        ttk.Progressbar.__init__(self, master, **kw)
        self.strValue = strValue #stringValue qui permet de retouner en asynchrone la valeur courante de la progression
        
    def start(self, duree):
        '''p1 duree est exprimee en sec'''
        self.duree = duree
        self.ordreStop=False #permet de stopper la barre de progression
        self["value"] = 0 #l'echelle de temps varie de 0 à 100 (pourcentage du temps ecoul"/temps restant)
        self.debuttime = time.time()
        self.maxtime = self.debuttime + self.duree #barre de progression de heure courante à heure+duree
        self["maximum"] = 100
        self.displayTime() #debut de la progression
    
    def stop(self):
        '''arete la barre de progression'''
        self.ordreStop=True
        
    def displayTime(self):
        '''affiche temps et  update progress bar'''
        self.value = time.time()
        self.strValue.set("{0} / {1} (min)".format(Util.secToms(self.value- self.debuttime),\
                          Util.secToms(self.duree))) 
        self["value"] = ((self.value- self.debuttime)/self.duree)*100 #pourcentage du temps ecoule 
        #self.progress.update()
        if self.value < self.maxtime and not self.ordreStop:
            # read more bytes after 300 ms
            self.after(300, self.displayTime)
            
