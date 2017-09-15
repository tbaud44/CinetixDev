#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
from Modele.Video import Video, Type


class BA(Video):
    '''
    classe de donnee representant une bande annonce
    contient un objet oeuvre
    '''
    
    
    def __init__(self, mere : Video):
        '''
        Constructor
        '''
        Video.__init__(self, mere.nomFichier, mere.duree)
        self.dateFichier = mere.dateFichier
        self.type = Type.BA
        self.color = "chocolate"
        self.oeuvreCinema = None
        
    def setOeuvreCinema(self, oeuvreCinema):
        self.oeuvreCinema = oeuvreCinema
        
   