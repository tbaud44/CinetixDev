#-*- coding: utf-8 -*-
'''classe widget qui etend un Label tkinter
le label s'efface apres une duree parametree
possibilite de faire clignoter le label'''

from time import sleep

import tkinter as tk


class LabelPlus(tk.Label):
    
    def __init__(self, master=None, **kw):
        
        tk.Label.__init__(self, master, **kw)
        #on stocke localement certains parametres propres au label
        if kw['textvariable']:
            self.msg = kw['textvariable']
        else:    
            self.msg = tk.StringVar()
        if kw['fg']:
            self.fg = kw['fg']
        else:    
            self.fg = "blue"
                
        self.textIsVisible = True
        self.tempsPauseClignotement = 500
        self.affichable = True #variable qui indique si le text du label doit etre affiché     
    
    '''methode qui affiche un nouveau message dans la zone texte'''
    def affiche(self, message, duree=8, clignotant=False):
        'p1 code message'
        'p2 param'
        'p3 duree affichage en seconde'
        
        #on desactive le precedent affichage
        self.clignotant = False
        
        #on fait une pause de facon a arreter le processus de clignotement du precedent message
        sleep((self.tempsPauseClignotement+1)/1000) #sleep during en seconde
        self._effacer()
        self.msg.set(message) #on modifie le message a l'ecran
        #au bout de duree secondes le message va s'effacer definitivement
        self.after(duree*1000, lambda x='':self._effacer())
        if clignotant:
            self.clignotant = True
            self._clignoter()
        
    '''methode qui efface le message'''
    def _effacer(self):
        
        self.msg.set("")
        #on reinitialise les proprietes de couleur pour afficher de nouveau apres
        self.config(fg=self.fg)
        
        
    '''methode qui fait clignoter le message 
    la couleur du texte est alternativement changee tous les x secondes entre une couleur definie, blue, et la
    couleur du fond (bg)'''    
    def _clignoter(self):
        if self.textIsVisible:
            clr = self.cget('bg')
        else:
            clr = self.fg
 
        self.config(fg=clr)
        self.textIsVisible = not self.textIsVisible
        #on regarde si doit encore faire afficher le label
        if self.clignotant: #test si pas ordre donné d'arret du clignotement
            self.after(self.tempsPauseClignotement, self._clignoter)
 