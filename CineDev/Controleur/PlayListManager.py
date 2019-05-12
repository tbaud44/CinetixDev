#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry BAUDOUIN
classe gerant les playlist au niveau de la couche modele
'''
import datetime
import pickle
import re
import os.path

from Controleur.BiblioManager import BiblioManager
from Modele.PlayList import PlayList
from transverse.CinetixException import CineException
from transverse.Util import Util


class PlayListManager(object):
    '''
    Gestion des playlists
    '''
    def __init__(self, bm:BiblioManager):
        '''
        Constructor
        '''
        self.bm = bm  #acces aux videos de la bibli
        self.statPL = {}  #nombre de pl par jour
        
    def calculerNomIHMPL(self, pl : PlayList):
        'retourne un triple nom,date,heure au format string de la playlist'
        'ce  nom sera celui du nom de la PL affichee a l ecran'
        'p1 playlist modele'
        #on verifie coherence de AAAAMMDD
        try:
            aaaammjj=pl.date.strftime('%d%m%Y') #ex 31032017
            heure=pl.heure.strftime('%H') #ex 15
        except ValueError:
            raise CineException("formatDateKO")    
        return (pl.film, aaaammjj, heure)
        
    def __calculerNomPL(self, date):
        '''controle les champs du nom du PL'''
        'Ex date = 1203201718 -> 12 mars 2017 18h00'
        'retourne un triple nom,date,heure  sous forme de chaine'
        
        #on verifie d'abord qu'il y a bien 10 chiffres
        if not re.match("[\d]{10}", date):
        #on verifie coherence de AAAAMMDD pour une date valide
            raise CineException("formatDateKO")
        try:
            heure=date[-2:]+'h00'
            d=datetime.datetime.strptime(date[:8], '%d%m%Y')
            h=datetime.datetime.strptime(heure, '%Hh%M') #ex 15h00
            
        except ValueError:
            raise CineException("formatDateKO")    
        nomPL = "PL__" + d.strftime('%Y-%m-%d') +'__' + heure
        return (nomPL,d,h)
    
    def existeFichierPL(self, date):
        '''controle la presence du fichier PL
        retourne true si le fichier exite deja'''
        
        (nomPL,d,h) = self.__calculerNomPL(date)
        if os.path.isfile(Util.configValue('commun', 'repertoirePL') + nomPL + '.obj'):
            return True
        else:
            return False
            
    def enregistrerPL(self, date, nomFilmProjete, listVideosNom):
        '''créer et enregistre une playlist avec toutes ses composantes
        sauvegarde la playlist sur disque
        retourne le nom de la PL
        '''
        (nomPL,d,h) = self.__calculerNomPL(date)
        
        
        pl = PlayList(nomPL,d,h, nomFilmProjete)
        
        #rechercher toutes les videos par nom
        for videoNom in listVideosNom:
            videoTrouve = self.bm.rechercherVideo(videoNom)
            #controler que le film projete ne soit pas dans la liste des video
            if (videoTrouve.nomFichier == nomFilmProjete or videoTrouve.getNom() == nomFilmProjete):
                raise CineException('filmProjeteKO')
            pl.ajouterVideo(videoTrouve)
        #sauvegarde sur disque
        self.__save(pl)
        return nomPL
    
    def __save(self, pl:PlayList):
        '''
        sauvegarde d'une playlist dans un fichier sur disque (dossier resources/playlists)
        p1: playlist obj modele
        '''
        fichierPL=Util.configValue('commun', 'repertoirePL') + pl.nom + '.obj' 
        with open(fichierPL , 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(pl)
        fichier.close()
    
    def load(self, nomFichierPL):
        '''
        construit un objet playlist a partir d'un fichier'''
        try:
            with open(nomFichierPL, 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                objPL = mon_depickler.load()
                fichier.close()
        except IOError:
            raise CineException('lecturePLKO')
        except EOFError:
            raise CineException('lecturePLKO')
        return objPL
    
    def calculerStatPL(self):
        '''
        recherche toutes les playlist sur le disque
        stocke dans un dictionnaire le nombre de PL par jour
        '''
                    #on stocke l'heure du fichier
        ficPL = Util.listerRepertoire(Util.configValue('commun', 'repertoirePL'), False)
        for fichier in ficPL:
            retour = re.match(r"PL__([\d]{4})-([\d]{2})-([\d]{2})__([\d]{2})h00.obj", fichier)          
            if retour:    
                jjmmaaaaFichier=retour.group(3) +'-'+ retour.group(2) +'-'+retour.group(1) #ex 09112017
                self.statPL['PL'+jjmmaaaaFichier] = self.statPL.get('PL'+jjmmaaaaFichier, 0) + 1
                
    def getStatPL(self, annee, mois, jour):
        '''
        retourne le nombre de paylist trouvee pour un jour donné
        retourne 0 si jour non present dans dic
        '''
        if len(self.statPL)==0:
            self.calculerStatPL()
        return self.statPL.get("PL%2s-%02d-%04d" %(jour,mois,annee), 0)
                    #on stocke l'heure du fichier
                
    def rechercherPLprocheDate(self, pdate):
        '''
        p1 date recherche de la PL selon cette date
        recherche toutes les playlist du meme jour que la date parametre
        si recherche > 1 playlist, on choisit celle qui est le plus proche de l'heure
        retourne le nom du fichier de la playlist'''
        jjmmaaaaParam=pdate.strftime('%d%m%Y') #ex 21032017
        heureParam=pdate.strftime('%Hh%M') #ex 15h00
        PLcriteresOK = [] #tableau des playlists qui ont le jour ok par rapport au parametre
                    #on stocke l'heure du fichier
        ficPL = Util.listerRepertoire(Util.configValue('commun', 'repertoirePL'), False)
        for fichier in ficPL:
            retour = re.match(r"PL__([\d]{4})-([\d]{2})-([\d]{2})__([\d]{2})h00.obj", fichier)          
            if retour:    
                jjmmaaaaFichier=retour.group(3)+retour.group(2)+retour.group(1) #ex 21032017
                heureFichier=retour.group(4)+'h00' #ex 15h00
                if jjmmaaaaFichier==jjmmaaaaParam:
                    PLcriteresOK.append(retour.group()+':'+heureFichier)
        if len(PLcriteresOK)==0:
            raise CineException('PLRechercheKO')            
        if len(PLcriteresOK)==1:
            #une seule PL matche donc on la retourne
            return PLcriteresOK[0].split(':')[0]
        #il faut faire une recherche en prenant l'heure la plus proche'
        heurePlusProche = None # heure fictive pour initialiser recherche
        for plTrouvee in PLcriteresOK:
            heurePL=plTrouvee.split(':')[1]
            if Util.heureCompare(heureParam, heurePL, heurePlusProche)<0:
                        plPlusProcheHeureParam = plTrouvee.split(':')[0]
                        heurePlusProche=heurePL
        return plPlusProcheHeureParam
    
    def rechercherPLAvecVideo(self, selVideoObj):
        '''
        methode qui recherche les playlist qui contiennent la video en parametre
        retourne une liste de PL
        '''
        retour = []
        ficPL = Util.listerRepertoire(Util.configValue('commun', 'repertoirePL'))
        for fichier in ficPL:
            plCur = self.load(fichier)
            for video in plCur.videos:
                if video.getNom() == selVideoObj.getNom(): 
                    retour.append(plCur)
        return retour     
           