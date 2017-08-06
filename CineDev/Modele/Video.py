#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
classe de video de base, mere des autres classes videos telle que ba, animbeaulieu ou pub
une video est representee par son nom de fichier auquel on ajoute des infos qui decrivent la video
'''

from enum import Enum


class Type(Enum):
    INCONNU = 1
    BA = 2
    PUB = 3
    ANIM_BEAULIEU = 4
        
class Video(object):
    '''
    classe de donnee representant une video
    '''


    def __init__(self, nomFichier, duree):
        '''
        Constructor
        '''
        self.nomFichier=nomFichier
        self.duree = duree
        self.titre=""
        self.type = Type.INCONNU
        self.color="gainsboro"
        self.dateFichier=None
        
    def setTitre(self, titre):
        self.titre = titre
    
    def setDateFichier(self, dateFic):
        self.dateFichier = dateFic
        
    def getNom(self):
        if self.titre:
            return self.titre
        else:
            return self.nomFichier
        
    