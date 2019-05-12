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
    unicodeExpEntier = {"exp0": "\u2070", "exp1": "\u00B9", "exp2": "\u00B2", "exp3": "\u00B3",
                        "exp4": "\u2074", "exp5": "\u2075", "exp6": "\u2076"   }
    
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
    
    '''calcule une font police'''
    def getFont(nomFont):
        fontConfig=Util.configValue('polices', nomFont)
        mafont = fontConfig.split(',')
        if len(mafont) == 3:
            return (mafont[0], int(mafont[1]), mafont[2])
        if len(mafont) == 2:
            return (mafont[0], int(mafont[1]))
    
    getFont = staticmethod(getFont)

    '''retourne le caractere unicode d'un entier sous forme exposant'''
    def getUnicodeCharExposant(entier):
        return Util.unicodeExpEntier['exp'+str(entier)]
    
    getUnicodeCharExposant = staticmethod(getUnicodeCharExposant)

    def listerRepertoire(path, cheminAbsolu=True):  
        fichier=[]  
        for root, dirs, files in os.walk(path):  
            for f in files:
                if (cheminAbsolu):  
                    fichier.append(os.path.join(root, f))
                else:
                    fichier.append(f) 
            return fichier
    listerRepertoire = staticmethod(listerRepertoire)
    
    
    def path2url(path):
        return urljoin('file:', pathname2url(path))
    path2url = staticmethod(path2url)
    
    """format secondes en  min/sec
        ex 105 sec fait 1:45 min
    """
    def secToms(nb_sec):
        if not nb_sec:
            return "0:00"
        m,s=divmod(nb_sec,60)
        if s>=10:
            return "%d:%d" %(m,s)
        else:
            return "%d:0%d" %(m,s)            
    secToms = staticmethod(secToms)

    '''format minutes en  secondes
        ex 4:10 fait 250 sec
    '''
    def minTosec(nb_min):
        if not nb_min:
            return "0"
        liste = nb_min.split(':')
        return str(int(liste[0])*60 + int(liste[1]))    
    minTosec = staticmethod(minTosec)


    def heureCompare(heureReference, heure1, heure2):
        '''heure sont au format hh:mm'''
        '''heure2 peut etre null'''
        '''si heure1 est plus proche de heureReference alors retourne -1'''
        '''si heure2 est plus proche de heureReference alors retourne 1'''
        if not heure2:
            return -1
        
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
    
    '''
    methode qui compare date param a la date du jour
    '''
    def estDateAnterieurAujourdhui(annee, mois, jour):
        return datetime.date.today() > datetime.date(int(annee), int(mois), int(jour))
    estDateAnterieurAujourdhui = staticmethod(estDateAnterieurAujourdhui)
    