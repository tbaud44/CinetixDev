#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry BAUDOUIN
classe gerant les playlist au niveau de la couche modele
'''
import datetime
import pickle
import re

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
        
    def calculerNomIHMPL(self, pl : PlayList):
        'retourne un triple nom,date,heure au format string de la playlist'
        'ce  nom sera celui du nom de la PL affichee a l ecran'
        'p1 playlist modele'
        #on verifie coherence de AAAAMMDD
        try:
            aaaammjj=pl.date.strftime('%Y%m%d') #ex 20170321
            heure=pl.heure.strftime('%Hh%M') #ex 15h00
        except ValueError:
            raise CineException("formatDateKO")    
        return (pl.film, aaaammjj, heure)
        
    def __calculerNomPL(self, date, heure):
        '''controle les champs du nom du PL'''
        'retourne un triple nom,date,heure  sous forme de chaine'
        
        #on verifie d'abord qu'il y a bien 6 chiffres
        if not re.match("[\d]{8}", date):
        #on verifie coherence de AAAAMMDD pour une date valide
            raise CineException("formatDateKO")
        try:
            d=datetime.datetime.strptime(date, '%Y%m%d')
            h=datetime.datetime.strptime(heure, '%Hh%M') #ex 15h00
            
        except ValueError:
            raise CineException("formatDateKO")    
        nomPL = "PL__" + d.strftime('%Y-%m-%d') +'__' + heure
        return (nomPL,d,h)
        
    def enregistrerPL(self, date, heure, nomFilmProjete, listVideosNom):
        '''créer et enregistre une playlist avec toutes ses composantes
        sauvegarde la playlist sur disque
        retourne le nom de la PL
        '''
        (nomPL,d,h) = self.__calculerNomPL(date, heure)
        
        
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
    
    def rechercherPLprocheDate(self, pdate):
        '''
        p1 date recherche de la PL selon cette date
        recherche toutes les playlist du meme jour que la date parametre
        si recherche > 1 playlist, on choisit celle qui est le plus proche de l'heure
        retourne le nom du fichier de la playlist'''
        aaaammjjParam=pdate.strftime('%Y%m%d') #ex 20170321
        heureParam=pdate.strftime('%Hh%M') #ex 15h00
        PLcriteresOK = [] #tableau des playlists qui ont le jour ok par rapport au parametre
                    #on stocke l'heure du fichier
        ficPL = Util.listerRepertoire(Util.configValue('commun', 'repertoirePL'), False)
        for fichier in ficPL:
            retour = re.match(r"PL__([\d]{4})-([\d]{2})-([\d]{2})__([\d]{2})h00.obj", fichier)          
            if retour:    
                aaaammjjFichier=retour.group(1)+retour.group(2)+retour.group(3) #ex 20170321
                heureFichier=retour.group(4)+'h00' #ex 15h00
                if aaaammjjFichier==aaaammjjParam:
                    PLcriteresOK.append(retour.group()+':'+heureFichier)
        if len(PLcriteresOK)==0:
            raise CineException('PLRechercheKO')            
        if len(PLcriteresOK)==1:
            #une seule PL matche donc on la retourne
            return PLcriteresOK[0].split(':')[0]
        #il faut faire une recherche en prenant l'heure la plus proche'
        heurePlusProche = '00:00' # heure fictive pour initialiser recherche
        for plTrouvee in PLcriteresOK:
            heurePL=plTrouvee.split(':')[1]
            if Util.heureCompare(heureParam, heurePL, heurePlusProche)<0:
                        plPlusProcheHeureParam = plTrouvee.split(':')[0]
                        heurePlusProche=heurePL
        return plPlusProcheHeureParam
    