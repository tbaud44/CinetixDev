'''
Created on 1 nov. 2017


@author: Thierry baudouin
classe thread permettant de detecter nouvelles videos
'''
#! /usr/bin/python
# -*- coding: utf-8 -*-


# import external libraries
from threading import Thread
from datetime import date
import os.path
from Vue.widget import PlayerVLCLight
from transverse.Util import Util
from Modele.Video import Video
from Modele.BA import BA

# import standard libraries
class DureeVideos(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, repVideos, bm):
        Thread.__init__(self)
        self.bm = bm #biblioManager
        self.repVideos = repVideos
    
    #methode principale
    def run(self):
        player =  PlayerVLCLight.Player() #player utilisé pour calcuker duree video
        #on stocke temporairement les videos du repertoire
        videosRepertoireTemp = {};
        for videoFile in Util.listerRepertoire(self.repVideos, False):
            if not videoFile in self.bm.biblioGenerale.videos:
                #nouveau fichier video donc on ajoute on dico memoire
                #print ("Analyse video ",videoFile)
                
                dureeVideo = player.GetDurationVideo(videoFile, self.repVideos)
                mm, ss = divmod(dureeVideo, 60)
                nomficVideoSansAccent = videoFile.encode( 'ascii', errors='ignore' ).decode('mbcs') 
                print ("video et duree:",nomficVideoSansAccent, mm,ss)
  
                newVideo = Video(videoFile, dureeVideo)
                try:
                    mtime = os.path.getmtime(str(os.path.join(self.repVideos, videoFile)))
                except OSError:
                    mtime = 0
                    print ("Problem parsing date fichier " + videoFile)
                last_modified_date = date.fromtimestamp(mtime)
                newVideo.setDateFichier(last_modified_date)
                #crrer un objet video (ba animBeaulieu ou pub)
                videosRepertoireTemp[videoFile]=self.bm.construitObjetVideo(newVideo)
            else:
                #on recopie l'objet video existant
                videosRepertoireTemp[videoFile]=self.bm.biblioGenerale.videos[videoFile]    
        
        self.bm.biblioGenerale.videos=videosRepertoireTemp #mise a jour liste des videos dans objet biblioManager
        self.bm.setStatusChargementEnCours(False)
    