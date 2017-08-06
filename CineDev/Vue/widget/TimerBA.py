#-*- coding: utf-8 -*-
'''
Created on 14 mai 2017

@author: Thierry baudouin
classe widget qui affiche un camembert avec une duree qui decroit
Le camembert se remplit(couleur) au fur et a mesure du temps qui avance
attente bloquante optionnel'''

import tkinter as tk
from transverse.CinetixException import CineException


class TimerBA(tk.Canvas):
   
    def __init__(self, master=None, duree=20, **kw):
        
        tk.Canvas.__init__(self, master, **kw)
        self.duree = self.__convertStr(duree)
        self.nbSecondesEcoulees=0
        self.decompteTermine=False
        self.idText = None

    def reinitialiser(self, duree=20):
        
        self.duree = self.__convertStr(duree)
        self.nbSecondesEcoulees=0
        self.decompteTermine=False
        self.idText = None

    def afficherChrono(self, decompte=False):
        '''affiche temps et ; update progress bar
        methode appelee toutes les secondes'''
                
        partieEcoulee = (360*self.nbSecondesEcoulees)/self.duree
        if (partieEcoulee >= 360):
            partieEcoulee=359.99
            self.decompteTermine=True    
        #coord = 10, 10, 140, 110
        coord = 10, 10, 80, 60
        self.delete(tk.ALL)
        self.create_arc(coord, start=0, extent=partieEcoulee, fill="red")
        nbSecondesRestantes = self.duree - self.nbSecondesEcoulees
       # if self.idText:
       #     self.delete(self.idText)
        self.create_text(40, 40, text=nbSecondesRestantes,font=('courier', 25, 'bold'), fill="blue")
       # self.idText = idText
        if (decompte and partieEcoulee< 359.99):  #le cercle n'est pas encore rempli
            self.nbSecondesEcoulees+=1   #1 seconde ecoulee
            self.master.after(1000,lambda x=decompte:self.afficherChrono(x)) #relance de la methode apres 1 sec
   
    def __convertStr(self, s):
        '''convertit une chaine en entier'''
        try:
            ret = int(s)
        except ValueError:
            raise CineException('typeEntierKO')     
        return ret
