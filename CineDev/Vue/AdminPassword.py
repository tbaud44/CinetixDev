#-*- coding: utf-8 -*-
'''
Created on 30 mai 2017

@author: Thierry Baudoui,
Frame independante de la fenetre principale permettant de saisir dans une zone texte un mot de passe
'''
import tkinter as tk
from transverse.CinetixException import CineException


class PassIHM(object):
    '''
    classdocs
    '''


    def __init__(self, rootTK, bm, bibliVue):
        '''
        Constructor
        '''
        self.tk=rootTK
        self.bibliVue = bibliVue
        self.bm=bm #biblioManager
        
    def afficher(self):
        wdw = tk.Toplevel( ) #nouvelle fenetre fille
        wdw.title('Administrateur')
        wdw.geometry('+200+200')
        self.frame = wdw
        self.__dessiner()
        
        wdw.transient(self.tk) #permet de rendre la fenetre modale
        wdw.grab_set()
        self.tk.wait_window(wdw)
          
    def __dessiner(self):
        
        '''on nettoie toute la frame en supprimant les enfants widget'''
        master = self.frame
        
        """construit les widgets """
        frameAdmin = tk.LabelFrame(master, width=15, text='Acces Administrateur')

        
        tk.Label(frameAdmin, width = 15,text='Password').grid(in_=frameAdmin, sticky=tk.W, row=1, column=1)
        entryPassw= tk.Entry(frameAdmin, show="*", width = 20)
        entryPassw.grid(in_=frameAdmin, padx=10, pady=15, sticky=tk.W, row=1, column=2)
                
        entryPassw.focus_set()
        
        '''ajout des 2 boutons'''
        boutonAnnuler=tk.Button(frameAdmin, width=10, text="Annuler", takefocus=True, command=master.destroy)\
            .grid(in_=frameAdmin, padx=15, pady=15, row=2, column=1)

        boutonValider=tk.Button(frameAdmin, width=10, text="Valider", takefocus=True, command=\
                 lambda x=entryPassw:self.__validerPassword(x))
        boutonValider.grid(in_=frameAdmin, padx=15, pady=15, row=2, column=2)

        frameAdmin.pack(padx=15, pady=15)
        
    def __validerPassword(self, passSaisi):
        '''methode appelle lors d un click sur bouton valider
        p1: password saisi'''
        #print (passSaisi.get())
        retour=self.bm.validerPasswordAdmin(passSaisi.get()) #controle du password 
        self.frame.destroy()
        if retour:
            #le mot de passe de l'administrateur est correct
            #active les fonctions disponible pour administrateur
            #afficher frameLabel Administration
            self.bibliVue.afficherFrameAdmin()
            #active le menu fiche video
            self.bibliVue.aMenu.entryconfig(0, state=tk.NORMAL)
            #activer le bouton enregistrer
            self.bibliVue.dicoWidget['btnEnreg'].config(state=tk.NORMAL)
        else:
            raise CineException('AuthentificationKO')    