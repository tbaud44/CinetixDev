
#-*- coding: utf-8 -*-
'''
Created on 16 aout 2018

@author: HOME
Frame permettant de visualiser les references playlist
'''

from transverse.Util import Util
import tkinter as tk
import datetime


class ReferencesPL(object):
    '''
    Fenetre, qui affiche, pour une video, la liste ds playlist qui inclu cette video
    '''


    def __init__(self, rootTK, evtProxy ):
        '''
        Constructor
        '''
        self.tk=rootTK
        self.evtProxy=evtProxy
        
        '''
        affiche la frame avec ses composants
        '''
    def afficher(self, videoIHM, listPL):
        wdw = tk.Toplevel()
        wdw.geometry(Util.configValue('dimensions', 'geometryRefPL'))
        
       # wdw.geometry("{}x{}+{}+{}".format(300, 390, 400, 300))
        #wdw.geometry('+400+300')
        self.frame = wdw
        self.__dessiner(videoIHM)
        self.initialiserPLReferenceesIHM(self.listboxPL, listPL)
        #rendre la fenetre modale
        wdw.transient(self.tk)
        wdw.grab_set()
        self.tk.wait_window(wdw)
          
    def __dessiner(self, videoIHM):
        
        '''on nettoie toute la frame en supprimant les enfants widget'''
        master = self.frame
        
        """construit les widgets """
        frameFiche = tk.LabelFrame(master, width=18, height=60, text='References Playlist ')

        tk.Label(frameFiche,text='Fichier Video').grid(in_=frameFiche, pady=15, sticky=tk.W, row=1, column=1)
        self.entryFichier= tk.Entry(frameFiche, border=2, width=35)
        self.entryFichier.grid(in_=frameFiche, sticky=tk.W, row=1, column=2)
    
        '''affectation donnee '''
        self.entryFichier.insert(0, videoIHM)
        self.entryFichier.config(state=tk.DISABLED)
        
        pw = tk.PanedWindow(frameFiche, orient=tk.HORIZONTAL) #regroupe la liste et le sidebar
        
        largeurBibli = 30
        hauteurBibli = 10
        
        listboxPL = tk.Listbox(pw, width=largeurBibli, height=hauteurBibli, font=Util.getFont('font2'))
        self.listboxPL = listboxPL
        sbar = tk.Scrollbar(pw)
        sbar.config(command=listboxPL.yview)
        listboxPL.config(yscrollcommand=sbar.set)
        #sbar.pack(side=RIGHT, fill=Y)
        listboxPL.bind("<Double-Button-1>",self.evtProxy.chargerSelectionPL)
        self.evtProxy.bibliIHM.dicoWidget['listRefPL']=listboxPL
        pw.add(listboxPL)
        pw.add(sbar)
        # attach popup to frame
        #listboxPL.bind("<Button-3>", self.popup)
        
        pw.grid(row=2, column=1, columnspan = 2, padx=2, sticky=tk.NW)
        frameFiche.pack(padx=15, pady=15)
        
    def initialiserPLReferenceesIHM(self, listboxPL, listPL):
    
        '''
        methode qui insere dans la liste les PL
        '''
        now = datetime.datetime.now()
        for pl in listPL:
            listboxPL.insert(tk.END, pl.nom)
            if pl.date >= now:
                plcolor = 'green'
            else:
                plcolor = 'red'    
            listboxPL.itemconfig(tk.END, bg=plcolor) 
    