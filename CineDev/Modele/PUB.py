#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
from Modele.Video import Video, Type


class PUB(Video):
    '''
    classe de donnee representant une publicite
    une oub contient un contact (referent societe qui paye la pub)
    '''
    def __init__(self, mere : Video):
        '''
        Constructor
        '''
        Video.__init__(self, mere.nomFichier, mere.duree)
        self.dateFichier = mere.dateFichier
        self.type = Type.PUB
        self.contact = ""
        self.montantCotis = 0.0
        self.color="pink"
        self.dateDeb = None
        self.dateFin = None
        
    def setContact(self, nomContact):
        self.contact = nomContact
        