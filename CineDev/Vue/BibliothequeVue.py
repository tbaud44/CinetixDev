#-*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: Thierry Baudouin
classe qui dessine les widgets de la fenetre principale de l'ihm
ne contient pas de traitement ni de logique metier
'''
import time
from tkinter import Canvas

from Vue.EvtProxy import EvtIHM
from Vue.widget.LabelPlus import LabelPlus
from Vue.widget.ProgressVideoBar import Pbar
from Vue.widget.TimerBA import TimerBA
import tkinter as tk
from transverse.Util import Util


#import progressbar
class Interface:
    
    '''Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre.'''
    def __init__(self):
        super().__init__()
        
        self.root=tk.Tk()
        self.root.title(Util.configValue('commun', 'titre'))
        self.evtProxy = EvtIHM()
        self.photosIHM = {} #garder une reference sur les photos
        tk.Grid.columnconfigure(self.root,5,weight=1)
        tk.Grid.rowconfigure(self.root,10,weight=1)
        self.root.geometry(Util.configValue('commun', 'geometry'))
        self.root.configure(bg="#FEFEE2")
        #enreg StringVar
        self.dicoWidget = {} #dictionnaire de tous les objets graphiques
    
    def getId(self, id):
        return self.dicoWidget[id]
       
        '''methode qui cree les objets graphiques fenetre principale'''   
    def dessiner(self):
        
        """construit les widgets """
        #L1C3 titre global
        etatLibelle = tk.StringVar()
        self.dicoWidget['SVetatLibelle']=etatLibelle
        labelL1C3 = tk.Label(self.root, textvariable=etatLibelle, width=55, bg="#FEFEE2", font=('Helvetica', 13, 'bold'))
        labelL1C3.grid(row=1, column=2, columnspan=3, padx=1, sticky=tk.W)
        
        #L1C3 titre global
        #heureL1C6
        strHeure = tk.StringVar()
        self.dicoWidget['SVheure']=strHeure
        labelL1C6 = tk.Label(self.root, textvariable=strHeure, width=10, font=('courier', 11, 'bold'))
        labelL1C6.grid(row=1, column=5, padx=1, sticky=tk.W)
        self.miseAJourHeure(strHeure)
        
        pwL2C1 = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg="#FEFEE2") #regroupe la liste et le sidebar
        
        pwL2C1bis = tk.PanedWindow(pwL2C1, orient=tk.HORIZONTAL, bg="#FEFEE2") #regroupe les checkbox de tri
        labelTri = tk.Label(pwL2C1bis, text="Tri:", bg="#FEFEE2")
        pwL2C1bis.add(labelTri)
        
        self.triBibli = tk.StringVar()
        self.triBibli.set('Nom')
        
        radTriNom = tk.Radiobutton(
            pwL2C1bis, text='Nom',
            variable=self.triBibli,
            bg="#FEFEE2",
            command=lambda x='Nom':self.evtProxy.initialiserVideosBibliIHM(x),
            value= 'Nom')
        pwL2C1bis.add(radTriNom)
        
        radTriType = tk.Radiobutton(
            pwL2C1bis, text='Type',
            variable=self.triBibli,
            bg="#FEFEE2",
            command=lambda x='Type':self.evtProxy.initialiserVideosBibliIHM(x),
            value= 'Type')
        pwL2C1bis.add(radTriType)
        
        radTriDate = tk.Radiobutton(
            pwL2C1bis, text='Date',
            variable=self.triBibli,
            bg="#FEFEE2",
            command=lambda x='Date':self.evtProxy.initialiserVideosBibliIHM(x),
            value= 'Date')
        
        pwL2C1bis.add(radTriDate)
        
        labelL2C1 = tk.Label(pwL2C1, text="Bibliotheques de films annonces", width=35, fg="brown", bg="#FEFEE2", font=('courier', 10, 'bold'))
        pwL2C1.add(labelL2C1)
        pwL2C1.add(pwL2C1bis)
        
        pwL2C1.grid(row=2, column=1, padx=1, sticky=tk.NW)
        
        pwL3C1 = tk.PanedWindow(self.root, orient=tk.HORIZONTAL) #regroupe la liste et le sidebar
        # first pane, which would get widgets gridded into it:
    
        listVideos = tk.Listbox(pwL3C1,width=50,height=25)
        self.dicoWidget['listVideos']=listVideos
        
        sbar = tk.Scrollbar(pwL3C1)
        sbar.config(command=listVideos.yview)
        listVideos.config(yscrollcommand=sbar.set)
        #sbar.pack(side=RIGHT, fill=Y)
        
        pwL3C1.add(listVideos)
        self.listVideosIHM = listVideos
        pwL3C1.add(sbar)
        #ajout du menu contextuel
        self.creerMenuContextuel(listVideos)
        # attach popup to frame
        listVideos.bind("<Button-3>", self.popup)

        '''enregistrement widget bibliIHM dans evtProxy'''
        self.evtProxy.setBibliIHM(self)
        
        pwL3C1.grid(row=3, column=1, padx=5, rowspan=6, sticky=tk.NW)

        pwL9C1 = tk.PanedWindow(self.root, orient=tk.HORIZONTAL) #regroupe les 2 boutons
        
        #handler pour quitter application
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        boutonQuitter=tk.Button(pwL9C1, command=self.quitter, text="Quitter") 
        boutonAdmin=tk.Button(pwL9C1, text="Administration", command=\
                     lambda x=self.root,y=self: self.evtProxy.verifierProfilAdmin(x,y))
        pwL9C1.add(boutonQuitter,width=80, height=30)
        pwL9C1.add(boutonAdmin,width=120, height=30)
        pwL9C1.grid(row=9, sticky=tk.N, column=1, padx=5)

        self.photosIHM['photoRecharger'] = tk.PhotoImage(file=Util.configValue('commun', 'recharger'))        
        boutonRechargerL2C2=tk.Button(self.root, command=self.initialiserDonnees, image=self.photosIHM['photoRecharger'])\
        .grid(row=2, column=2, padx=1, sticky=tk.NW)

        
        labelPlL2C3 = tk.Label(self.root, width=15, text="Gestion Playlist", fg="brown", bg="#FEFEE2", font=('courier', 10, 'bold'))
        labelPlL2C3.grid(row=2, column=3)

        framePlL3C3 = tk.LabelFrame(self.root, text='Definition Playlist')

        
        tk.Label(framePlL3C3, width = 15,text='Date Diffusion\n(AAAAMMDD)').grid(in_=framePlL3C3, sticky=tk.NW, row=0, column=0)
        
        dateDiffu = tk.Entry(framePlL3C3, width = 15)
        dateDiffu.grid(in_=framePlL3C3, sticky=tk.W, row=0, column=1)
        self.dicoWidget['dateDiffu']=dateDiffu
        
        #ajout des radio bouton pout l'heure
        
        varHeureDiffu = tk.StringVar()
        varHeureDiffu.set("20h00")
        self.dicoWidget['heureDiffu']=varHeureDiffu
        
        rad11h = tk.Radiobutton(
            framePlL3C3, text="11h00",
            variable=varHeureDiffu,
            value= "11h00")
            
        rad11h.grid(in_=framePlL3C3, sticky=tk.W, row=1, column=0)
        
        rad15h = tk.Radiobutton(
            framePlL3C3, text="15h00",
            variable=varHeureDiffu,
            value= "15h00")
            
        rad15h.grid(in_=framePlL3C3, sticky=tk.W, row=1, column=1)
        
        rad18h00 = tk.Radiobutton(
            framePlL3C3, text="18h00",
            variable=varHeureDiffu,
            value= "18h00")
            
        rad18h00.grid(in_=framePlL3C3, sticky=tk.W, row=1, column=2)
        
        rad20h00 = tk.Radiobutton(
            framePlL3C3, text="20h00",
            variable=varHeureDiffu,
            value= "20h00")
            
        rad20h00.grid(in_=framePlL3C3, sticky=tk.W, row=1, column=3)
       
        #duree PL=somme des dur�es des videos de la PL       
        tk.Label(framePlL3C3, width=10, text='Duree').grid(in_=framePlL3C3, sticky=tk.NW, row=2, column=0)
        
        entryDureePL= tk.Entry(framePlL3C3, width = 10, state='readonly')
        entryDureePL.grid(in_=framePlL3C3, sticky=tk.W, row=2, column=1)
        self.dicoWidget['entryDureePL']=entryDureePL
        
        tk.Label(framePlL3C3, width=15, text='Film projection').grid(in_=framePlL3C3, sticky=tk.W, row=3, column=0)
        
        entryVideoPL= tk.Entry(framePlL3C3, width = 32, state='readonly')
        entryVideoPL.grid(in_=framePlL3C3, sticky=tk.W, row=3, column=1, columnspan=3)
        self.dicoWidget['entryVideoPL']=entryVideoPL
        
        framePlL3C3.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        self.photosIHM['photoCopier'] = tk.PhotoImage(file=Util.configValue('commun', 'copier'))        
        boutonTransfertL3C2=tk.Button(self.root, image=self.photosIHM['photoCopier'], command=self.evtProxy.transfertCurrentVideoEntetePL)
        boutonTransfertL3C2.grid(row=3, column=2, sticky=tk.W)

        msgInfoLibelle = tk.StringVar()
        
        labelStatusPlL4C3 = LabelPlus(self.root, textvariable=msgInfoLibelle, width=40, fg= "dark green" , bg="#DF6D14", font=('courier', 10, 'bold'))
        labelStatusPlL4C3.grid(row=4, column=3, padx=5, sticky=tk.W)
        self.dicoWidget['statusPL']=labelStatusPlL4C3
        
        listPlL5C3 = tk.Listbox(self.root, width=54,height=16)
        listPlL5C3.grid(row=5, column=3, padx=5, rowspan=3, sticky=tk.NW)
        self.dicoWidget['listPlL5C3']=listPlL5C3
        
        boutonTransfertL5C2=tk.Button(self.root, image=self.photosIHM['photoCopier'], command=
                                      lambda x=listPlL5C3:self.evtProxy.ajouterVideoPL(x))
                                    
        boutonTransfertL5C2.grid(row=5, column=2, rowspan=3)

        #ajout d'un label avec StringVar pour afficher la progression de la duree video
        pwL8C3 = tk.PanedWindow(self.root, orient=tk.VERTICAL) #regroupe la liste et le sidebar
        
        tempsEcouleVideo = tk.StringVar()
        labeltempsEcouleVideo = tk.Label(pwL8C3, textvariable=tempsEcouleVideo, width=25,  font=('courier', 9))
        tempsEcouleVideo.set("0 / 0 (min)")
        labeltempsEcouleVideo.grid(in_=pwL8C3, row=1, column=1, padx=10, sticky=tk.W)
        
        pbarVideo = Pbar (master=pwL8C3, strValue=tempsEcouleVideo, orient="horizontal", length=302, mode="determinate")
        pbarVideo.grid(in_=pwL8C3, row=2, column=1, padx=5, sticky=tk.NW)
        self.dicoWidget['pbar']= pbarVideo
        
        pwL8C3.grid(row=8, column=3, padx=5, sticky=tk.NW)
     
        dureeAttente = Util.configValue('commun', 'dureeAttenteLecturePL')
        #necessite de mettre variable tbaL7c4 a cause methode afficherFrameAdmin
        self.tbaL7C4 = TimerBA(self.root, duree=dureeAttente, bg="#FEFEE2", height=60, width=150, highlightbackground="#FEFEE2")
        self.tbaL7C4.grid(row=7, column=4, sticky=tk.N)
        
        self.tbaL7C4.afficherChrono(False)
        
        self.photosIHM['photoPlay'] = tk.PhotoImage(file=Util.configValue('commun', 'imgPlay'))        
        boutonPlayPlL9C3=tk.Button(self.root, image=self.photosIHM['photoPlay'], width=70, command=\
                lambda x=listPlL5C3,y=pbarVideo,w=self.tbaL7C4:self.evtProxy.playPL(x, y, w))
        boutonPlayPlL9C3.grid(row=9, column=3, padx=5, pady=5)
        
        boutonStopPlL10C3=tk.Button(self.root, text="STOP", width=20, command=self.evtProxy.stopperPL)
        boutonStopPlL10C3.grid(row=10, column=3, padx=5,sticky=tk.N)
       
        pwL3C4 = tk.PanedWindow(self.root, orient=tk.VERTICAL) #regroupe la liste et le sidebar
        boutonEnregistrer=tk.Button(pwL3C4, width=15, text="Enregistrer", command=\
                lambda x=self:self.evtProxy.enregistrerPL(x))
        boutonEnregistrer.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=1, column=1, columnspan=3)
        
        boutonCharger=tk.Button(pwL3C4, width=15, text="Charger", command=self.evtProxy.chargerPL)
           
        boutonCharger.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=2, column=1, columnspan=3)
        
        boutonVider=tk.Button(pwL3C4, width=15, text="Vider", command=\
                lambda x=listPlL5C3:self.evtProxy.viderPL(x))
        boutonVider.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=3, column=1, columnspan=3)
        
        self.photosIHM['photoFlecheHaut'] = tk.PhotoImage(file=Util.configValue('commun', 'imgFlecheHaut'))        
        
        boutonFlecheHaut=tk.Button(pwL3C4, image=self.photosIHM['photoFlecheHaut'] , command=\
                                   lambda x=listPlL5C3,y='PREC':self.evtProxy.inverserVideoPL(x,y))
        boutonFlecheHaut.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=4, column=1)
        
        self.photosIHM['photoCroix'] = tk.PhotoImage(file=Util.configValue('commun', 'imgCroix'))        
        
        boutonCroix=tk.Button(pwL3C4, image=self.photosIHM['photoCroix'] , command=\
                                  lambda x=listPlL5C3:self.evtProxy.supprimerVideoPL(x))
        boutonCroix.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=5, column=2)
        
        self.photosIHM['photoFlecheBas'] = tk.PhotoImage(file=Util.configValue('commun', 'imgFlecheBas'))        
        
        boutonFlecheBas=tk.Button(pwL3C4, image=self.photosIHM['photoFlecheBas'] , command=\
                                   lambda x=listPlL5C3,y='SUIV':self.evtProxy.inverserVideoPL(x,y))
        
        boutonFlecheBas.grid(in_=pwL3C4, sticky=tk.W, padx=5, pady=5, row=6, column=1)
        
        pwL3C4.grid(row=3, column=4, rowspan=3, sticky=tk.NW)

        labelLancementBaL6C4 = tk.Label(self.root, text="Lancement dans\n(en secondes) ", bg="#FEFEE2", width=15, font=('courier', 10, 'bold'))
        labelLancementBaL6C4.grid(row=6, column=4, padx=5, sticky=tk.NW)
        self.dicoWidget['titreOeuvre']= tk.StringVar()
        
        labelTitreFilmL2C5 = tk.Label(self.root, textvariable=self.dicoWidget['titreOeuvre'], bg="#FEFEE2", font=('courier', 12, 'bold'))
        labelTitreFilmL2C5.grid(row=2, column=5, sticky=tk.NW)
       
        #Utilisation d'un panewWindow pour gerer formattage
        pwL3C5 = tk.PanedWindow(self.root, relief='ridge', borderwidth=4, orient=tk.VERTICAL, bg="#FEFEE2") #regroupe la liste et le sidebar
       
        canvasAfficheFilmL3C5 = Canvas(pwL3C5, width=240, height=380 ,bg="#FEFEE2")
        #canvasAfficheFilmL3C5.grid(row=3, column=5, rowspan=4, sticky=tk.NW)
        self.dicoWidget['canvasAffiche']=canvasAfficheFilmL3C5
        
        self.dicoWidget['infosOeuvre']= tk.StringVar()
        labelInfosFilmL7C5 = tk.Label(pwL3C5, width=240, height=60, anchor=tk.NW, justify=tk.LEFT, textvariable=self.dicoWidget['infosOeuvre'] , wraplength=220, bg="#FEFEE2")
     #   labelInfosFilmL7C5.grid(row=7, column=5, rowspan=2, padx=5, sticky=tk.NS)
        pwL3C5.add(canvasAfficheFilmL3C5)
        pwL3C5.add(labelInfosFilmL7C5)
        pwL3C5.grid(row=3, column=5, rowspan=8, sticky=tk.NW)
        ###########################################
        
       # f = Fiche(self.root)
      #  f.afficher(self.bm.biblioGenerale.videos['Bande-Annonce Panique - Film 1946 (Drame).flv'])
        #########################"
    def creerMenuContextuel(self, bibliIHM):
        '''
        methode qui cree un menu contextuel sur la bibliotheque video
        '''
         # create a popup menu
        self.aMenu = tk.Menu(self.root, tearoff=0)
        self.aMenu.add_command(label="Fiche Video", state='disabled', command=\
            lambda x=self.root:self.evtProxy.afficheFrameFicheVideo(x)) #apres validation password administrateur, le statut passera enabled                  
        self.aMenu.add_command(label="Lire", command=\
            lambda x=self.root:self.evtProxy.playVideoPC(x))    
    def popup(self, event):
        '''
        methode evenement click droit qui affiche le menu contextuel
        '''
        self.aMenu.post(event.x_root, event.y_root)
     
 
        '''methode qui met a jour l heure'''
    def miseAJourHeure(self, strVarHeure):
        'p1 heure'
        strVarHeure.set(time.strftime('%H:%M'))
        #recalcul heure dans 1 minute
        self.root.after(60*1000, lambda x=strVarHeure:self.miseAJourHeure(x))
            
    def initialiserDonnees(self):
        '''methode qui charge l'ihm des donnees
          '''
        self.evtProxy.initialiserDonnees()
        
    def afficherFrameAdmin(self):
        '''methode qui affiche le frameLabel prope au profil administrateur (si mot de passe saisi correct)'''
        frameAdminL8C4 = tk.LabelFrame(self.root, relief='raised', borderwidth=4, bg='salmon', text='Administration', padx=5, pady=5)

        tk.Label(self.root, bg='salmon', text='Delai lanc 20s>1sec').grid(in_=frameAdminL8C4, sticky=tk.W, row=0, column=0)
        entryAdminDureeAttente = tk.Entry(self.root,width=3)
        entryAdminDureeAttente.grid(in_=frameAdminL8C4, sticky=tk.W, row=0, column=1)
        #Si changement par Admin alors redessiner le camembert en chgt echelle temps/duree
        entryAdminDureeAttente.bind("<FocusOut>", lambda x:self.evtProxy.miseAJourTimerBA(self.tbaL7C4, entryAdminDureeAttente))
        frameAdminL8C4.grid(row=8, column=4, rowspan=2, sticky=tk.NW)
    
    def quitter(self):
        '''methode de fin de l application'''
        '''sauvegarde sur disque'''
        self.evtProxy.bm.save()
        self.root.quit()
        #sauvegarde de la bibliotheque video memoire sur le disque (bib.obj)
        
    def mainLoop(self):
        '''
        methode qui gere la boucle evenement utilisateur
        '''     
        self.root.mainloop()  