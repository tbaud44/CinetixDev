#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
'''
import configparser
import datetime 
import os.path
from urllib.parse import urljoin
from urllib.request import pathname2url


class Util:
    """Une classe utilitaire"""
     
    config = configparser.ConfigParser()
    configDejaLue = False
    
    def configValue(rubrique, clef):
        if not(Util.configDejaLue):
            Util.config.read("resources/config.ini",encoding='utf-8')
            Util.configDejaLue = True
        return Util.config.get(rubrique, clef)
    configValue = staticmethod(configValue)
    
    
    def setConfigValue(rubrique, clef, newValue):
        Util.configValue(rubrique, clef) #force lecture
        Util.config.set(rubrique, clef, newValue)
    setConfigValue = staticmethod(setConfigValue)
    
    def listerRepertoire(path, cheminAbsolu=True):  
        fichier=[]  
        for root, dirs, files in os.walk(path):  
            for i in files:
                if (cheminAbsolu):  
                    fichier.append(os.path.join(root, i))
                else:
                    fichier.append(i) 
            return fichier
    listerRepertoire = staticmethod(listerRepertoire)
    
    
    def path2url(path):
        return urljoin('file:', pathname2url(path))
    path2url = staticmethod(path2url)
    
    def secToms(nb_sec):
        m,s=divmod(nb_sec,60)
        if s>=10:
            return "%d:%d" %(m,s)
        else:
            return "%d:0%d" %(m,s)            
    secToms = staticmethod(secToms)

    def minTosec(nb_min):
        liste = nb_min.split(':')
        return str(int(liste[0])*60 + int(liste[1]))    
    minTosec = staticmethod(minTosec)

    def heureCompare(heureReference, heure1, heure2):
        '''heure sont au format hh:mm'''
        '''si heure1 est plus proche de heureReference alors retourne -1'''
        '''si heure2 est plus proche de heureReference alors retourne 1'''
        dref = datetime.datetime (2000, 1, 1,int(heureReference[:2]), int(heureReference[3:5]))    
        d1 = datetime.datetime(2000, 1, 1,int(heure1[:2]), int(heure1[3:5]))    
        d2 = datetime.datetime(2000, 1, 1,int(heure2[:2]), int(heure2[3:5]))    
        
        duree1 = abs(d1 - dref)
        duree2 = abs(d2 - dref)
        if duree1 <= duree2:
            return -1
        else:
            return 1
    heureCompare = staticmethod(heureCompare)
    
    
    