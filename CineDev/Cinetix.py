#-*- coding: utf-8 -*-
'''
Created on 10 mai 2017

@author: Thiery BAUDOUIN
Programme principal lancant l'interface graphique qui initialise des données necessaires
'''
from Vue.BibliothequeVue import *

if __name__ == '__main__': 
    
    ihm = Interface()
    
    ihm.dessiner()
    ihm.initialiserDonnees()
    try:
        
        ihm.mainLoop()
    except :
        print ("Erreur geree")
    exit(0)        