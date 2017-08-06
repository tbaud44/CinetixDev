#-*- coding: utf-8 -*-
'''
Created on 1 juin 2017

@author: Thierry BAUDOUIN
Classe gerant les traitements sur l'ihm
proxy entre l'ihm et les classes Manager
'''
from datetime import date
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from PIL import ImageTk, Image

from Controleur.BiblioManager import BiblioManager
from Controleur.PlayListManager import PlayListManager
from Modele.Video import Type, Video
from Vue import AdminPassword
from Vue.FicheVideo import Fiche
from Vue.widget import PlayerVLC2
import tkinter as tk
from transverse.CinetixException import CineException, CineWarning
from transverse.Util import Util


class EvtIHM(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.bm = BiblioManager()
        self.pm = PlayListManager(self.bm)
        self.debug = False    
    '''debut des pointeurs widgets'''
        
    '''pointeur du widget bibli video'''
    def setBibliIHM(self, bibliIHM):
        self.bibliIHM = bibliIHM
    
    def initialiserDonnees(self):
        '''methode qui charge l'ihm des donnees
           ne doit pas etre bloquant pour ne pass empecher l'affichage de l'ihm
           donc on intercepte les exceptions'''
        
        self.miseAJourEtat('etatDebut')
        '''scan du repertoire video'''
        self.bm.scanDisk()
        '''methode qui remplit les widgets de donnees
        '''
        self.initialiserVideosBibliIHM()
        try:
            '''recherche et charge la playlist du jour à cette heure'''
            plJour = self.pm.rechercherPLprocheDate(date.today())
            self.chargerPL(plJour)
            libelleMessage = Util.configValue('messages', 'PLRechercheOK')
            messagebox.showwarning(
                "Succes:",
                libelleMessage 
                )
        except CineException:
            libelleMessage = Util.configValue('messages', 'PLRechercheKO')
            messagebox.showwarning(
                "Attention",
                libelleMessage 
                )
        self.miseAJourEtat('etatFin')
        
    def transfertCurrentVideoEntetePL(self):
        '''
        methode qui prend la selection video de la liste des video de l'interface et la copie dans l'entete playlist
        de l'interface
        '''
    # get selected line index
        curNomVideo = self._getCurrentVideoBibli()
        curVideo = self.bm.rechercherVideo(curNomVideo)
        if curVideo.type.value != Type.BA.value:
            raise CineException('TypeBAKO')
        self.__setChampDisabledValue('entryVideoPL', curNomVideo) #copie du nom video dans le champ de la PL
        
    
    def ajouterVideoPL(self, plIHM):
    
        '''
        methode qui prend la selection video de la liste IHM et l'ajoute en fin de playlist de l'IHM
        p1, widget playlist 
        '''
        
    # get the line's text
        listWidget = self.bibliIHM.getId('listVideos')  
        
        selVideoIHM = self._getCurrentVideoBibli()
        index = listWidget.curselection()[0]
        bgVideo = listWidget.itemcget(index, "bg") #permet de recopier l'attribut couleur sur la PL
        plIHM.insert(tk.END, selVideoIHM)
        plIHM.itemconfig(tk.END, bg=bgVideo)
        #mettre a jour la duree PL
        selVideoObj = self.bm.rechercherVideo(selVideoIHM)
        duree = self.bibliIHM.getId('entryDureePL').get() #la duree de la PL est la somme  des durees des videos
        dureeEnSecondes = int(Util.minTosec(duree))
        dureeEnSecondes += selVideoObj.duree
        self.__setChampDisabledValue('entryDureePL', Util.secToms(dureeEnSecondes))
           
            
   
    def initialiserVideosBibliIHM(self, nomTri='Nom'):
    
        '''
        methode qui recupere la liste des videos du manager et les inseres dans la bibliotheque ihm
        selon un ordre de tri
        p1: widget bibliotheque des videos
        '''
        '''on vide la list box'''
        listWidget = self.bibliIHM.getId('listVideos')  
        listWidget.delete(0, tk.END)
        for video in self.bm.getAllVideosTriees(nomTri):
            listWidget.insert(tk.END, video.getNom())
            listWidget.itemconfig(tk.END, bg=video.color) #couleur specifique selon BA, AnimBeaulieu ou PUB
             
    def afficheFrameFicheVideo(self, tk):
        '''
        methode qui affiche la frame avec la fiche video (attributs, nom, titre, date, etc ...)
        p1: widget parent global tk
        ''' 
        selVideoIHM =self._getCurrentVideoBibli()
        fiche = Fiche(tk, self)
        fiche.afficher(self.bm.rechercherVideo(selVideoIHM))
    
    def playVideoPC(self, tk):
        '''
        methode qui lance un vlc player(non bloquant) sur ecran pc avec la video selectionnee
        p1: widget parent global tk
        '''
        selVideoIHM =self._getCurrentVideoBibli()
        selVideoObj = self.bm.rechercherVideo(selVideoIHM)
        vlcPlayer =  PlayerVLC2.Player(None,  title=selVideoObj.getNom() , fullscreen=False )
        vlcPlayer.play(Util.configValue('commun', 'repertoireVideo') + selVideoObj.nomFichier) #asynchrone
        
    def enregistrerVideoBiblioGenerale(self, video:Video):
    
        '''
        methode qui enregistre les attributs d'une video dans la bibliotheque des videos
        p1: video qui peut etre ba, animBeaulieu ou pub
        '''
        self.bm.enregistrerVideo(video)
        '''mise a jour etat'''
        self.miseAJourEtat("enregVideoOK")
        
        '''potentiellement la video a change de type (ba,pub,etc...) donc on rafraichit la bibliotheque IHM de videos'''
        self.initialiserVideosBibliIHM()

        '''methode qui met a jour l'etat de l'appli(libelle en haut fenetre)'''
    def miseAJourEtat(self, codeMessageEtat, param=''):
         libelleMessage = Util.configValue('messages', codeMessageEtat)
         try:    
             self.bibliIHM.getId('SVetatLibelle').set("ETAT: " + libelleMessage + ' ' +param)
         except AttributeError:
             pass    #peut arriver lors d'un test unitaire
     
                
                           
         '''methode qui met a jour le timerBA avec une valeur saisie par l administrateur'''
    def miseAJourTimerBA(self, timerBA, entryNewValueDureeAttente):
        'p1 timerBA'
        'p2 tk entry'
        newDureeAttente = entryNewValueDureeAttente.get()
        timerBA.reinitialiser(duree=newDureeAttente)
        Util.setConfigValue('commun', 'dureeAttenteLecturePL', newDureeAttente) #modifie la propriete globalement
        timerBA.afficherChrono(False) #actualise la widget du timerBA
   
    def stopperPL(self):
    
        '''
        methode qui arrete la lecture des playlists (brutalement via le bouton stop)
        '''
        try:
            self.vlcPlayer.quitter()
            self.bibliIHM.getId('pbar').stop() #on arrete la barre de progression
        except AttributeError:
            pass    
    
    def playPL(self, playlistIHM, pbarIHM, timerIHM):
    
        '''
        methode qui joue toutes les v1ideos de la playlist
        p1: widget playlist des videos
        p2 : widget pbar
        p4 : widget timer 20 sec
        '''
        if playlistIHM.size() == 0:
            raise CineException('VidePLKO')
        dureeAttente = Util.configValue('commun', 'dureeAttenteLecturePL')
        timerIHM.reinitialiser(duree=dureeAttente)
        timerIHM.afficherChrono(True) #attente bloquante
        wdw = tk.Toplevel()
        #recherche des parametres externalises
        paramVLC = Util.configValue('ECRAN2', 'paramVLC')
        geometry= Util.configValue('ECRAN2', 'geometry')
        
        self.vlcPlayer =  PlayerVLC2.Player(wdw, \
                                       title='playlist beaulieu' , fullscreen=False, geometry=geometry, paramVLC=paramVLC )
        self.__itererPlayPL(playlistIHM, pbarIHM, timerIHM, -1, self.vlcPlayer)  
            
                       
    def inverserVideoPL(self, playlistIHM, sens='PREC'):
    
        '''
        methode qui inverse la selection video de la PL avec le suivant ou le precedent
        p1, widget playlist
        p2,sens pour inverser 
        '''
        indexCur = playlistIHM.curselection()[0]  
        if (sens == 'PREC'):
            indexAdj = indexCur - 1
        else:
            indexAdj = indexCur + 1
        
        if (indexAdj<0 or indexAdj>= playlistIHM.size()):
            return #en dehors des bornes       
#     # on procede a l'inversion
        videoCur = playlistIHM.get(indexCur)
        bgVideoCur = playlistIHM.itemcget(indexCur, "bg") #permet de recopier l'attribut couleur sur la PL
        
        videoAdj = playlistIHM.get(indexAdj)
        bgVideoAdj = playlistIHM.itemcget(indexAdj, "bg") #permet de recopier l'attribut couleur sur la PL
          
        if (sens == 'PREC'): 
            playlistIHM.delete(indexAdj, indexCur)
            playlistIHM.insert(indexAdj, videoCur)
            playlistIHM.itemconfig(indexAdj, bg=bgVideoCur)
            playlistIHM.insert(indexCur, videoAdj)
            playlistIHM.itemconfig(indexCur, bg=bgVideoAdj)
        else:
            playlistIHM.delete(indexCur,indexAdj)
            playlistIHM.insert(indexCur, videoAdj)
            playlistIHM.itemconfig(indexCur, bg=bgVideoAdj)
            playlistIHM.insert(indexAdj, videoCur)
            playlistIHM.itemconfig(indexAdj, bg=bgVideoCur)
        
        playlistIHM.selection_set(indexAdj)
    
            
    def enregistrerPL(self, bibliIHM):
    
        '''
        methode qui controle et enregistre une playlist sur disque
        calcule l'oeuvre rattachee à la BA sur le site internet
        p1, dico des widgets
        '''
       
        nomPL = self.pm.enregistrerPL(bibliIHM.getId('dateDiffu').get(), bibliIHM.getId('heureDiffu').get(), \
            bibliIHM.getId('entryVideoPL').get(),bibliIHM.getId('listPlL5C3').get(0, tk.END))
        self._majStatusPL('enregPlOK', nomPL)
        #rechercher une video de la BA si la zone est renseignee
        oeuvre = None
        if bibliIHM.getId('entryVideoPL').get():
            baPL = self.bm.rechercherVideo(bibliIHM.getId('entryVideoPL').get()) #la video est forcement de type BA
            if not baPL.oeuvreCinema:
            #rechercher les infos sur le site web du cinema
                oeuvre = self.__calculerOeuvreFilmWeb()
                baPL.setOeuvreCinema(oeuvre)
            else:
                #oeuvre a deja ete calculee precedement et est stockee dans fichier
                #evite de rafaire du parsing
                oeuvre = baPL.oeuvreCinema
                self._majAfficheOeuvreCinema(oeuvre)     
        else:
            '''on peut rechercher affiche uniquement avec date et heure pl'''
            oeuvre = self.__calculerOeuvreFilmWeb()
                    
            
    def viderPL(self, playlistIHM):
    
        '''
        methode qui supprime tous les elements de la playlist IHM
        p1, playlistIHM
       
        '''
        playlistIHM.delete(0, tk.END)
        self.__setChampDisabledValue('entryVideoPL', '')
        
    
    def supprimerVideoPL(self, playlistIHM):
    
        '''
        methode qui supprime la selection courante de la playlist
        p1, playlistIHM
       
        '''
        
        if playlistIHM.curselection():
            #au moins un element dans la liste
            #on actualise la duree pl en soustrayant la duree de la video supprimee
            if playlistIHM.size() ==1:
                #on supprime la derniere video donc on remet a blanc
                self.__setChampDisabledValue('entryDureePL', '')
            else:
                index = playlistIHM.curselection()[0]
        # il faut calculer la nouvelle duree en soustrayant
                selVideoIHM = playlistIHM.get(index)
                selVideoObj = self.bm.rechercherVideo(selVideoIHM)
                duree = self.bibliIHM.getId('entryDureePL').get()
                dureeEnSecondes = int(Util.minTosec(duree))
                dureeEnSecondes -= selVideoObj.duree
                self.__setChampDisabledValue('entryDureePL', Util.secToms(dureeEnSecondes))
                
            playlistIHM.delete(playlistIHM.curselection()[0])
    
    def verifierProfilAdmin(self, tk, bibliVue):
        '''
        methode qui ouvre une boite dialogue pour saisie et controle password admin
        p1 fenetre racine
        p2 bibliVue (pour afficher frameLabelAdmin
        '''
        ap = AdminPassword.PassIHM(tk, self.bm, bibliVue)
        ap.afficher()
            
    def chargerPL(self, pnomPL=None):
        '''
        p1 si à l'init de l'ihm pour charger la playlist du jour
        methode qui ouvre une boite dialogue pour selectionner fichier playlist
        remplit les widgets afferent à la playlist à partir de l'objet modele playlist
        '''
        repPL=Util.configValue('commun', 'repertoirePL')
        if pnomPL:
            nomficPL=repPL+pnomPL
        else:    #boite de dialogue selection de fichier .obj
            nomficPL = askopenfilename(title="Ouvrir le fichier playlist:", initialdir=repPL, \
                filetypes = [("Fichiers Playlist","*.obj")]) 
        if len(nomficPL) > 0:
            plAChargee = self.pm.load(nomficPL)
            #charger les zones de la pl
            (nomFilm, date, heure) = self.pm.calculerNomIHMPL(plAChargee)
            entryDate=self.bibliIHM.getId('dateDiffu')
            entryDate.delete(0, tk.END)
            entryDate.insert(0,date)
            heureRBVar=self.bibliIHM.getId('heureDiffu')
            heureRBVar.set(heure)
            entryVideoPL = self.bibliIHM.getId('entryVideoPL')
            self.__setChampDisabledValue('entryVideoPL', nomFilm)
            playlistIHM = self.bibliIHM.getId('listPlL5C3')
            self.viderPL(playlistIHM)
            #ajouter les videos PlayList
            dureePL=0
            for video in plAChargee.videos:
                playlistIHM.insert(tk.END, video.getNom())
                playlistIHM.itemconfig(tk.END, bg=video.color)
                dureePL+=video.duree
            
            self.__setChampDisabledValue('entryDureePL', Util.secToms(dureePL))
            
            #charger la frame affiche film
            oeuvre = None
            if entryVideoPL.get():
                #si le champ est renseigne alors l'oeuvre fait obligatoirement partie du fichier serialise
                baPL = self.bm.rechercherVideo(entryVideoPL.get()) #la video est forcement de type BA
                oeuvre = baPL.oeuvreCinema
                #on teste au cas ou
                if oeuvre:
                    self._majAfficheOeuvreCinema(oeuvre)     
            else:
                '''on peut rechercher affiche uniquement avec date et heure pl'''
                oeuvre = self.__calculerOeuvreFilmWeb()
            
    def __setChampDisabledValue(self, nomChamp, val):
            '''
            methode qui modifie la valeur d'une zone saisie (entry) a etat disabled
            p1, widget nom du champ 
            p2 nom de la video
            '''
         # delete previous text in enter1
            widget = self.bibliIHM.dicoWidget[nomChamp]
            widget.config(state=tk.NORMAL)
            widget.delete(0, tk.END)
        # now display the selected text
            
            widget.insert(0, val)
            widget.config(state=tk.DISABLED)
    
    def _getCurrentVideoBibli(self):
        '''
        methode qui retourne la selection video de la liste
        '''
    # get selected line index
        listWidget = self.bibliIHM.getId('listVideos')  
        
        if not listWidget.curselection():
            raise CineException('selectionVideoKO')
        index = listWidget.curselection()[0]
    # get the line's text
        selVideo = listWidget.get(index)
        return selVideo
    
        '''methode qui met a jour le libelle du label pour le status des PL'''
    def _majStatusPL(self, codeMessageInfo, param="", duree=8, clignotant=False):
        'p1 code message'
        'p2 param'
        'p3 duree affichage en seconde'
        
        libelleMessage = Util.configValue('messages', codeMessageInfo) + param
        #Affichage du message si condition
        statusPLWidget = self.bibliIHM.getId('statusPL') #widget LabelPlus
        statusPLWidget.affiche(libelleMessage, duree, clignotant)
    
    def __itererPlayPL(self, playlistIHM, pbarIHM, timerIHM, rangPLAjouer, vlcPlayer):
    
        '''
        methode qui joue toutes les videos de la playlist
        p1: widget playlist des videos
        p2 : widget pbar
        p3: timer widget
        p4 : rangPL (index)
        p5: vlcPlayer
        '''
       # print ("rang {0}".format(rangPLAjouer))
        if (rangPLAjouer >= playlistIHM.size()):
            #c'est fini on tue le timer
            vlcPlayer.quitter()
            self._majStatusPL('finPL')
            return #plus de videos a traiter dans la PL
        '''la video en cours est-elle finie ?'''
        
        if ((timerIHM and not timerIHM.decompteTermine) or not vlcPlayer.isVideoFinished()):
            #soit le decompte de 20 sec n'est pas fini soit la video en cours n'est pas fini
             #on attend 300 ms et on reteste
            playlistIHM.after(300, lambda x=playlistIHM,y=pbarIHM,v=timerIHM,z=rangPLAjouer,w=vlcPlayer:\
                              self.__itererPlayPL(x, y, v, z, w))
            return
        #ici soit on est sur premiere video a jouer soit la video vient de se finir
        #on prend la video suivante de la liste si il en reste dans la liste
        if (rangPLAjouer >= 0):
            playlistIHM.itemconfig(rangPLAjouer, bg ='black') #ligne grisee donc traitee
        rangPLAjouer+=1
       # playlistIHM.selection_set(rangPLAjouer)
        if (rangPLAjouer < playlistIHM.size()):
            playlistIHM.itemconfig(rangPLAjouer, bg ='red')    
                
            selVideoIHM = playlistIHM.get(rangPLAjouer)
            selVideoObj = self.bm.rechercherVideo(selVideoIHM)
            if selVideoObj:
                #video bien trouvee
                #lancement de la barre de progression
                pbarIHM.start(selVideoObj.duree)
                #lecture de la video avec vlc
                if self.debug:
                    print ('Lecture {0} ieme/{1} video'.format(rangPLAjouer, playlistIHM.size()))    
                vlcPlayer.play(Util.configValue('commun', 'repertoireVideo') + selVideoObj.nomFichier) #asynchrone
                self.miseAJourEtat('vlcPlay', selVideoObj.getNom())
                if selVideoObj.type.value == Type.PUB.value:
                    self._majStatusPL('InfoPUB', '', duree=200, clignotant=True)
            else:
                #probleme de recherche video
                #Une video est presente dans la PL mais plus sur le disque
                #affichage d'un message et passage au suivant
                self._majStatusPL('NoVideoTrouve', selVideoIHM, 30) 
                rangPLAjouer+=1       
                #appel recursif
            self.__itererPlayPL(playlistIHM, pbarIHM, None, rangPLAjouer, vlcPlayer) #None pour le timer pour ne plus faire le controle avec videoFinished
        else:
            #c'est fini on tue le timer et vlc
            vlcPlayer.quitter()
            self._majStatusPL('finPL')
    
    def __calculerOeuvreFilmWeb(self):
    
        '''
        methode qui ramene des infos comme une affiche a partir du site web du cine
        le  critere de recherche est la date et l'heure de playlist à l'écran
        retourne objet oeuvre
        '''
        oeuvre=None
        try:
            oeuvre = self.bm.rechercherInfosWebVideo(self.bibliIHM.getId('dateDiffu').get(), 
                            self.bibliIHM.getId('heureDiffu').get())
        except CineWarning:
            self._majStatusPL('parsingHtmlKO')
        if oeuvre:
            self._majAfficheOeuvreCinema(oeuvre)
        return oeuvre
    
    def _majAfficheOeuvreCinema(self, oeuvre):
            '''
            met a jour l'image et les infos de l'oeuvre projetee
            on actualise la fenetre'''
            self.bibliIHM.getId('titreOeuvre').set(oeuvre.titre)
            infosFormatte= oeuvre.infos.replace("\t","")
            infosFormatte= infosFormatte.replace("\n"," ")
            self.bibliIHM.getId('infosOeuvre').set(infosFormatte)
          #  bibliIHM.getId('synopsisOeuvre').set(oeuvre.synopsis)
            
            im = Image.open(oeuvre.afficheMoyenFormat)
            widgetAffiche = self.bibliIHM.getId('canvasAffiche')
            widgetAffiche.image = ImageTk.PhotoImage(im)
            widgetAffiche.create_image (0, 0, anchor=tk.NW, image= widgetAffiche.image, tags="bg_img")
    