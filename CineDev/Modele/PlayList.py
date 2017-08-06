#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
from datetime import date, time

from Modele import Video


class PlayList:
    '''
    classe de donnee representant une playlist de video
    contient des donnees de date, heure de diffusion
    contient un tableau de videos
    '''
    def __init__(self, nom , datePL:date , heurePL:time, nomFilmAProjete):
        '''
        Constructor
        '''
        self.nom=nom
        self.date = datePL
        self.heure = heurePL
        self.film = nomFilmAProjete
        self.videos = [] # faut conserver ordre insertions
        
    def ajouterVideo (self, v:Video):    
        self.videos.append(v)
        