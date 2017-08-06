#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''

class Oeuvre(object):
    '''
    classe de donnee representant une oeuvre de cinema
    une oeuvre est un film,documenta projete au cinema
    l'oeuvre est decrite sur le site internet du cinema le beaulieu
    '''
    
    
    def __init__(self, titre, infos, synopsis):
        '''
        Constructor
        '''
        self.titre = titre
        self.infos = infos
        self.synopsis = synopsis
        self.affichePetitFormat = None
        self.afficheMoyenFormat = None
        
    def setAfficheImage(self, taille, dataFichier):
        '''taille=1 taille petite
        taille=2 taille moyenne'''
        if taille==1:
            self.affichePetitFormat = dataFichier
        if taille==2:
            self.afficheMoyenFormat = dataFichier
        