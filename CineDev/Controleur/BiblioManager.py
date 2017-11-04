#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry BAUDOUIN
classe permettant la gestion de la bibliotheque video representees par des bande annonce, pub et animation Beaulieu
gere la persistance des informations avec la couche modele
'''
from datetime import date, datetime
import hashlib
import os.path
import pickle
from urllib.error import HTTPError
from urllib.request import urlretrieve
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

from Modele.Biblio import Biblio
from Modele.OeuvreCinematographique import Oeuvre
from Modele.Video import Video, Type
from Modele.BA import BA
from Vue.widget import PlayerVLCLight
from transverse.CinetixException import CineException, CineWarning
from transverse.Util import Util
from transverse.GestionDureeVideo import DureeVideos

class BiblioManager(object):
    '''
    Gestion de la bibliotheque de videos
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__load()
        self.setStatusChargementEnCours(False)
        
    def __load(self):
        '''
        construit la biblioGenerale a partir d'un fichier bib.obj
        reconstruit a partir du fichier le dictionnaire des videos (ba, pub et animBeaulieu'''
        try:
            fichierBiblio=Util.configValue('commun', 'fichierBiblio')
            with open(fichierBiblio, 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                self.biblioGenerale = mon_depickler.load()
                fichier.close()
        except IOError:
            with open(fichierBiblio, 'w') as nouvFichier: #on cree le fichier
                nouvFichier.close()
                self.biblioGenerale = Biblio("Bibliotheque generale")
        except EOFError:     #fichier vide
            self.biblioGenerale = Biblio("Bibliotheque generale")
             
    def __purger(self):
        '''
        supprime les videos qui n'ont plus de fichier sur disque
        permet de ne plus gerer en memoire les anciennes videos
        '''
        for videoFile in self.biblioGenerale.videos.values():
            if not os.path.isfile(Util.configValue('commun', 'repertoireVideo') + videoFile.nomFichier):
                del self.biblioGenerale.videos[videoFile.nomFichier]
                
    def save(self):
        '''
        sauvegarde la biblioGenerale dans un fichier bib.obj
        '''
        self.__purger()
        fichierBiblio=Util.configValue('commun', 'fichierBiblio')
        with open(fichierBiblio , 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(self.biblioGenerale)
        fichier.close()
        
    def getAllVideosTriees(self, nomTri='Nom'):
        '''
         methode qui retourne toutes les videos selon un ordre de tri
         retourne un tableau d'objets Modele Videos
         p1 ordre tri
        '''
        l=list(self.biblioGenerale.videos.values())
        if nomTri == 'Nom':
            return sorted(l, key=lambda t:t.getNom())
        if nomTri == 'Type':
            return sorted(l, key=lambda t:t.type.value)
        if nomTri == 'Date':
            return sorted(l, key=lambda t:t.dateFichier)
        
    def getColor(self, video:Video):
        '''
         methode qui retoune la couleur d'une video
         par defaut renvoie le champ color
         pour les pubs , regarder les datesDeb et datesFin
         '''
        if video.type.value == Type.PUB.value:
            dateJour = datetime.now()
            if video.dateDeb and dateJour < video.dateDeb:
                return "yellow3" 
            if video.dateFin and dateJour > video.dateFin:
                return "yellow3" 
        return video.color
     
    
    def scanDisk(self):
        '''
        compare le repertoire de la bibliotheque avec l'objet memoire
        Pour chaque nouveau fichier video du repertoire, on crée un objet Video (nom Fichier) et
        on calcule sa durée de lecture via un mini player VLC ainsi que la date du fichier.
        '''
        repVideos=Util.configValue('commun', 'repertoireVideo')
        #test si repVideos est bien un repertoire lisible
        if not os.path.isdir(repVideos):
            raise CineException('repVideoKO')
            return
        
        #appel a un thread qui va scanner, en arriere plan (non bloquant) le repertoire des videos
        # et calculer les durees des nouvelles videos
        threadDureeVideos = DureeVideos(repVideos, self)
        self.setStatusChargementEnCours(True)
        threadDureeVideos.start()
    
    def setStatusChargementEnCours(self, boolStatus):
        '''methode pour gerer etat du status de chargement de la bibliotheque'''
        self.chargementEnCours = boolStatus #booleen pour gerer etat du thread de calcule des durees de videos
    
    def getStatusChargementEnCours(self):
        '''methode pour gerer etat du status de chargement de la bibliotheque'''
        return self.chargementEnCours  #booleen pour gerer etat du thread de calcule des durees de videos
            
    def enregistrerVideo(self, video:Video):
        '''enregistrement dans la bibliotheque la video
        suppression ancienne reference video'''
        self.biblioGenerale.videos[video.nomFichier]=video
    
    def rechercherVideo(self, idVideo):
        '''recherche une video selon son nomfichier ou titre.
            retourne l'objet video associé à sa clef
        '''
        try:
            selVideo = self.biblioGenerale.videos[idVideo]
        except KeyError:
            '''video selectionnee pas trouvee avec clef nomFichier donc recherche sequentielle par titre'''
            selVideo = self.__rechercherVideoParTitre(idVideo)
        return selVideo
        
    
    def __rechercherVideoParTitre(self, titre):
        '''recherche une video selon son titre.
            parcours sequentiel de la bibliotheque et comparaison avec le nom(titre)
        '''
        for video in self.getAllVideosTriees(): 
            if video.getNom() == titre:
                return video
        raise CineException('NoVideoTrouve')    
    
    def validerPasswordAdmin(self, passwordSaisi):
        '''methode qui compare le mot de passe saisi par l'utilisateur avec le mot de passe cripte dans config.ini
        retourne true ou False selon la comparaison'''
         # On encode la saisie pour avoir un type bytes

        entreSaisi = passwordSaisi.encode()
        entreSaisi_chiffre = hashlib.sha1(entreSaisi).hexdigest()
        mot_de_passe_admin_chiffre = Util.configValue('commun', 'passAdminCrypte')
        return (entreSaisi_chiffre == mot_de_passe_admin_chiffre)
        
    def rechercherInfosWebVideo(self, jourDiffusion):
        '''recherche des infos sur le site web du cinema lebeaulieu.
        jourDiffusion='1402201720
        retourne une oeuvre cinema en tant qu'objet
        '''
        dateFormatUrl=jourDiffusion[:2]+'%2F'+jourDiffusion[2:4]+'%2F'+jourDiffusion[4:8]
        heureDiffusion=jourDiffusion[8:10]+':00'
        url = 'https://www.cinemalebeaulieu.com/programme.php?searchMode=date&RechercherDate='+dateFormatUrl
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
        except HTTPError:
            raise CineWarning("AccesSiteBeaulieuKO")

        html = response.read().decode('utf-8')
        #parsing du code html pour retrouver les infos de l'oeuvre projete à une heure precise
        soup = BeautifulSoup(html,'html.parser')
        articles = soup.find_all(class_="article") #un article correspond à une balise div d'une projection
        articlePlusProcheHeureParam = None
        heurePlusProche = '00:00' # heure fictive pour initialiser recherche
        for filmProjete in articles:
            seance=filmProjete.find(class_="seance")
            if seance:    
                heureSeance=seance.find(class_="showtime").getText() #Ex: 18h00
                # peut avoir 18h00 VO donc supprimer le VO
                heureSeanceFormattee = re.match(r"([\d]{2}):([\d]{2}).*", heureSeance)          
            
                #comparaison de l'heure selectionnée dans ihm et heure affichee dans le site web
                if heureSeanceFormattee:
                    heureSeanceFormatteeParsee = heureSeanceFormattee.group(1)+':'+heureSeanceFormattee.group(2)
                    if Util.heureCompare(heureDiffusion, heureSeanceFormatteeParsee, heurePlusProche)<0:
                        articlePlusProcheHeureParam = filmProjete
                        heurePlusProche=heureSeanceFormatteeParsee
        
        if articlePlusProcheHeureParam == None:
           '''probleme aucun film trouve sur le site'''
           raise CineWarning("parsingHtmlKO")
        #on prend les infos sur le site
        #parsing des balises images de la page html
        image=articlePlusProcheHeureParam.find("img")
        urlImage=image['src']
        urlImagePetite = urlImage.replace('ratio=0.5', 'ratio=0.2')
        #on calcule 2 images de taille differente
        titre = articlePlusProcheHeureParam.find(class_="titre").getText()
        infos = articlePlusProcheHeureParam.find(class_="infos").getText()
        synopsis = articlePlusProcheHeureParam.find(class_="synopsis").getText()
        
        #on construit objet a partir des donnes du site web           
        oeuvre = Oeuvre(titre, infos, synopsis)
        #recuperation des images pour requete http
        repAffiche=Util.configValue('commun', 'repertoireAffiche')

        nomFichier1Affiche=repAffiche + urllib.parse.quote(titre, safe='') +'-G.jpg'
        oeuvre.setAfficheImage(2, nomFichier1Affiche)
        
        #on teste si le fichier jpeg a deja ete telecharge
        if not os.path.isfile(nomFichier1Affiche): #le fichier image a t-il deja ete telecharge?
            urlretrieve(urlImage, nomFichier1Affiche) #creer un fichier jpg dans le repertoire en telechargent par http
        
        nomFichier2Affiche=repAffiche + urllib.parse.quote(titre, safe='') +'-P.jpg'
        oeuvre.setAfficheImage(1, nomFichier2Affiche)
        if not os.path.isfile(nomFichier2Affiche):
            urlretrieve(urlImagePetite, nomFichier2Affiche)
        
        return oeuvre   