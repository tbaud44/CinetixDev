#-*- coding: utf-8 -*-
'''
Created on 30 mai 2017

@author: HOME
Frame permettant de saisir une fiche d'une ba,pub
'''
from tkinter import Canvas

from PIL import Image, ImageTk
from transverse.CinetixException import CineException
from Modele.AnimationBeaulieu import AnimationBeaulieu
from Modele.BA import BA
from Modele.PUB import PUB
from Modele.Video import Video, Type
from transverse.Util import Util
import tkinter as tk
import datetime


class Fiche(object):
    '''
    Fenetre, type formulaire, permettant de saisir infos d'une video: pub, ba, animBeaulieu
    '''


    def __init__(self, rootTK, evtProxy):
        '''
        Constructor
        '''
        self.tk=rootTK
        self.evtProxy=evtProxy
        
        '''
        affiche la frame avec ses composants
        '''
    def afficher(self, video:Video):
        wdw = tk.Toplevel()
        wdw.geometry(Util.configValue('dimensions', 'geometryFiche'))
        
       # wdw.geometry("{}x{}+{}+{}".format(300, 390, 400, 300))
        #wdw.geometry('+400+300')
        self.videoObj = video
        self.frame = wdw
        self.__dessiner()
        
        #rendre la fenetre modale
        wdw.transient(self.tk)
        wdw.grab_set()
        self.tk.wait_window(wdw)
          
    def __dessiner(self):
        
        '''on nettoie toute la frame en supprimant les enfants widget'''
        master = self.frame
        video = self.videoObj
       # master.destroy()
        for enfantWidget in master.grid_slaves() + master.pack_slaves() + master.place_slaves():
           enfantWidget.destroy()
        """construit les widgets """
        frameFiche = tk.LabelFrame(master, width=18, height=55, text='Detail Video ')

        
        tk.Label(frameFiche, width = 15,text='Fichier Video').grid(in_=frameFiche, sticky=tk.W, row=1, column=1)
        self.entryFichier= tk.Entry(frameFiche, width = 30)
        self.entryFichier.grid(in_=frameFiche, sticky=tk.W, row=1, column=2)
    
        '''affectation donnee '''
        self.entryFichier.insert(0, video.nomFichier)
        self.entryFichier.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Titre').grid(in_=frameFiche, sticky=tk.W, row=2, column=1)
        self.entryTitre= tk.Entry(frameFiche, width = 25)
        self.entryTitre.grid(in_=frameFiche, sticky=tk.W, row=2, column=2)
        '''affectation donnee '''
        self.entryTitre.insert(0, video.titre)
        
        
        tk.Label(frameFiche, width=15, text='Duree').grid(in_=frameFiche, sticky=tk.W, row=3, column=1)
        self.entryDuree= tk.Entry(frameFiche, width = 10)
        self.entryDuree.grid(in_=frameFiche, sticky=tk.W, row=3, column=2)
        '''affectation donnee '''
        self.entryDuree.insert(0, video.duree)
    
        tk.Label(frameFiche, width = 15,text='Date Video').grid(in_=frameFiche, sticky=tk.W, row=4, column=1)
        self.entryDateFichier= tk.Entry(frameFiche, width = 25)
        self.entryDateFichier.grid(in_=frameFiche, sticky=tk.W, row=4, column=2)
    
        '''affectation donnee '''
        self.entryDateFichier.insert(0, video.dateFichier.isoformat())
        self.entryDateFichier.config(state=tk.DISABLED)
        
        self.varTypeVideo = tk.IntVar()
        self.varTypeVideo.set(video.type.value)
        
        radINCONNU = tk.Radiobutton(
            master, text="INCONNU",
            variable=self.varTypeVideo,
            value= Type.INCONNU.value,
            command=self.__rbChecked)
        radINCONNU.grid(in_=frameFiche, pady=5, sticky=tk.W, row=5, column=1)
        
        radBA = tk.Radiobutton(
            master, text="BA",
            variable=self.varTypeVideo,
            value= Type.BA.value,
            command=self.__rbChecked)
        radBA.grid(in_=frameFiche, sticky=tk.W, row=5, column=2)
        
        radPUB = tk.Radiobutton(
            master, text="PUB",
            variable=self.varTypeVideo,
            value= Type.PUB.value,
            command=self.__rbChecked)
        radPUB.grid(in_=frameFiche, sticky=tk.W, row=6, column=1)
        
        radAnimBeaulieu = tk.Radiobutton(
            master, text="Anim Beaulieu",
            variable=self.varTypeVideo,
            value= Type.ANIM_BEAULIEU.value,
            command=self.__rbChecked)
        radAnimBeaulieu.grid(in_=frameFiche, sticky=tk.W, row=6, column=2)
        
        if (self.varTypeVideo.get() == Type.BA.value):
            #affichage affiche petit format si disponible
            if video.oeuvreCinema and video.oeuvreCinema.affichePetitFormat:
                im = Image.open(video.oeuvreCinema.affichePetitFormat)
                canvasAfficheFilm = Canvas(frameFiche, width=100, height=140 ,bg="#FEFEE2")
                canvasAfficheFilm.image = ImageTk.PhotoImage(im)
                canvasAfficheFilm.create_image (0, 0, anchor=tk.NW, image= canvasAfficheFilm.image, tags="bg_img")
                canvasAfficheFilm.grid(in_=frameFiche, sticky=tk.NW, row=7, column=1)
            else:
                tk.Label(frameFiche, width=20, text='Affiche non disponible').grid(in_=frameFiche, sticky=tk.W, row=7, column=1)
            
        if (self.varTypeVideo.get() == Type.PUB.value):
            tk.Label(frameFiche, width=15, text='Contact').grid(in_=frameFiche, sticky=tk.W, row=7, column=1)
            self.entryContact= tk.Entry(frameFiche, width = 20)
            self.entryContact.grid(in_=frameFiche, sticky=tk.W, row=7, column=2)
            '''affectation donnee '''
            self.entryContact.insert(0, video.contact)
            
            tk.Label(frameFiche, width=15, text='Montant Cotis').grid(in_=frameFiche, sticky=tk.W, row=8, column=1)
            self.entryMontant= tk.Entry(frameFiche, width = 10)
            self.entryMontant.grid(in_=frameFiche, sticky=tk.W, row=8, column=2)
            '''affectation donnee '''
            self.entryMontant.insert(0, video.montantCotis)
        
            tk.Label(frameFiche, width=15, text='Date Debut').grid(in_=frameFiche, sticky=tk.W, row=9, column=1)
            self.entryDateDeb= tk.Entry(frameFiche, width = 15)
            self.entryDateDeb.grid(in_=frameFiche, sticky=tk.W, row=9, column=2)
            '''affectation donnee si non null'''
            if video.dateDeb:
                self.entryDateDeb.insert(0, video.dateDeb.strftime('%d/%m/%Y'))
        
            tk.Label(frameFiche, width=15, text='Date Fin').grid(in_=frameFiche, sticky=tk.W, row=10, column=1)
            self.entryDateFin= tk.Entry(frameFiche, width = 15)
            self.entryDateFin.grid(in_=frameFiche, sticky=tk.W, row=10, column=2)
            '''affectation donnee '''
            if video.dateFin:
                self.entryDateFin.insert(0, video.dateFin.strftime('%d/%m/%Y'))
        
        '''pas de champ specifique pour Anim beaulieu'''
         
        '''ajout des 2 boutons'''
        boutonAnnuler=tk.Button(master, width=10, text="Annuler", command=master.destroy)
           
        boutonEnregistrer=tk.Button(master, width=10, text="Enregistrer", command=self.__enregistrerFicheVideo)
          #  .grid(in_=frameFiche, sticky=tk.W, padx=5, pady=5, row=8, column=2)
        
        frameFiche.pack(padx=15, pady=15)
        boutonAnnuler.pack(side=tk.LEFT, padx=15)
        boutonEnregistrer.pack(side=tk.RIGHT, padx=15)
        
    def __rbChecked(self):
        '''methode appelle lors d'un click sur radio button fiche'''
        
        if (self.varTypeVideo.get() == Type.INCONNU.value):
            '''on reinitialise la frame'''
            dateSav = self.videoObj.dateFichier
            self.videoObj = Video(self.videoObj.nomFichier, self.videoObj.duree)
            self.videoObj.setDateFichier(dateSav)
        
        if (self.varTypeVideo.get() == Type.BA.value):
            '''on reinitialise la frame avec une bande annonce'''
            self.videoObj = BA(self.videoObj)
        
        if (self.varTypeVideo.get() == Type.PUB.value):
            '''on reinitialise la frame avec une bande annonce'''
            self.videoObj = PUB(self.videoObj)
        
        if (self.varTypeVideo.get() == Type.ANIM_BEAULIEU.value):
            '''on reinitialise la frame avec une animation beaulieu'''
            self.videoObj = AnimationBeaulieu(self.videoObj)
        
        '''par defaut on a un titre et une duree et une date fichier'''
        #self.videoObj.duree = self.entryDuree.get()
        #self.videoObj.titre = self.entryTitre.get()
        #self.videoObj.dateFichier = self.entryDateFichier.get() 
        '''on relance le processus de dessin'''
        self.__dessiner() 
        
    def __enregistrerFicheVideo(self):
        '''methode appelle lors d un click sur bouton enregistrer'''
        '''on enregistre les donnees modifiables'''    
        '''par defaut on a un titre et une duree'''
        self.videoObj.duree = float(self.entryDuree.get())
        self.videoObj.titre = self.entryTitre.get()
        
        if (self.varTypeVideo.get() == Type.PUB.value):
            self.videoObj.contact = self.entryContact.get()
            self.videoObj.montantCotis = float(self.entryMontant.get())
            try:
                if self.entryDateDeb.get():
                    self.videoObj.dateDeb=datetime.datetime.strptime(self.entryDateDeb.get(), '%d/%m/%Y')
                if self.entryDateFin.get():
                    self.videoObj.dateFin=datetime.datetime.strptime(self.entryDateFin.get(), '%d/%m/%Y')
            except ValueError:
                raise CineException("formatDateKO")        
        self.frame.destroy()
        
        '''on enregistre la video'''
        self.evtProxy.enregistrerVideoBiblioGenerale(self.videoObj)   