#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
from Modele.Video import Video, Type


class AnimationBeaulieu(Video):
    '''
    classe de donnee representant une animation specifique cine beaulieu
    '''
    def __init__(self, mere : Video):
        '''
        Constructor
        '''
        Video.__init__(self, mere.nomFichier, mere.duree)
        self.dateFichier = mere.dateFichier
        self.type = Type.ANIM_BEAULIEU
        self.color="aquamarine"
       
    def getNom(self):
        return "ANIM BEAU - " + super(AnimationBeaulieu, self).getNom()        