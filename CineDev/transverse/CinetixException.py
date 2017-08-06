#-*- coding: utf-8 -*-
'''
Created on 11 juin 2017

@author: HOME
classe qui gere les erreurs,waening en implementant une exception propre a l'application
'''

from tkinter import messagebox

from transverse.Util import Util


class CineException(Exception):
    def __init__(self,codeRaison):
        self.codeRaison = codeRaison
    
    def __str__(self):
        libelleMessage = Util.configValue('messages', self.codeRaison)
        messagebox.showwarning(
            "Attention",
            libelleMessage 
        )
        return self.raison

class CineWarning(Exception):
    def __init__(self,codeRaison):
        self.codeRaison = codeRaison
    
    def __str__(self):
        libelleMessage = Util.configValue('messages', self.codeRaison)
        print ("Warning: " + libelleMessage)
        return self.raison
        