#-*- coding: utf-8 -*-
'''
Created on 10 mai 2017

@author: Thiery BAUDOUIN
Programme principal lancant l'interface graphique initialise des données necessaires
'''
from Vue.BibliothequeVue import *
import os
import sys

if __name__ == '__main__': 
    

    if  len(sys.argv)==2 and sys.argv[1] == '-nodir':
        #dans environnement eclipse, faire un chdir
        #sous bat ou shell, se postionner dans le repertoire workspace/CINETIXV3 
        os.chdir("C:/Users/HOME/git/CINETIXV3")
   
    ihm = Interface()
    
    ihm.dessiner()
    ihm.initialiserDonnees()
    try:
        
        ihm.mainLoop()
    except :
        print ("Erreur geree")
    exit(0)        