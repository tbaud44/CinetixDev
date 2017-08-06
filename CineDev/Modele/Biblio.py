#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
class Biblio:
    '''
    classe de donnee representant une bibliotheque de video
    '''
    
    def __init__(self, nom):
        '''
        Constructor
        '''
        self.nom=nom
        self.videos = {}   #cle du dictionnaire est nom fichier video
    