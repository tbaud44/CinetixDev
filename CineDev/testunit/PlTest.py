'''
Created on 15 juil. 2017

@author: HOME
'''
import datetime
import os
import random
import unittest

from Controleur.PlayListManager import PlayListManager
from Util import Util
from Vue.EvtProxy import EvtIHM
from Vue.widget.ProgressVideoBar import Pbar
from Vue.widget.TimerBA import TimerBA
import tkinter as tk
from transverse.CinetixException import CineException


class Test(unittest.TestCase):


    def setUp(self):
        os.chdir("C:/Users/HOME/workspace/CINETIXV3")
        self.root=tk.Tk()
        self.evt = EvtIHM()
        self.pm = PlayListManager(None)
        self.evt.debug=True
        self.timer = TimerBA(self.root)
        tempsEcouleVideo = tk.StringVar()
        
        self.pbar = Pbar(self.root,tempsEcouleVideo)
        self.listPl = tk.Listbox(self.root, width=54,height=16)
        self.listPl.grid(row=1, column=1, sticky=tk.NW)
        self.timer.grid(row=2, column=1, sticky=tk.NW)
        self.pbar.grid(row=3, column=1, sticky=tk.NW)
        
        self.dicoWidget={}
        self.dicoWidget['listPlL5C3']=self.listPl
        


    def tearDown(self):
        pass


    def testPlPlay(self):
        '''ajout de 4000 videos dans la PL'''
        return
        repVideos=Util.configValue('commun', 'repertoireVideo')
        ficVideos=Util.listerRepertoire(repVideos, False)
       
        for number in range(1,1001):         
            indAleatoire= random.randint(0,len(ficVideos)-1)
            self.listPl.insert(tk.END, ficVideos[indAleatoire])
            
        #appel de la methode
        self.evt.playPL(self.listPl, self.pbar, self.timer)
        self.root.mainloop()
    
    def testrechercherPLprocheDate(self):
        '''test de la methode rechercherPLprocheDate'''
        #test avec une date ou il n'a aucune playlist pour ce jour
        dateSansPL = datetime.datetime(2016, 2, 14, 5, 30)
        
        with self.assertRaises(CineException):
            self.pm.rechercherPLprocheDate(dateSansPL)    
        
        #test avec une date ou il y'a une seule playlist pour ce jour
        dateUnePL = datetime.datetime(2017, 2, 21, 5, 30)
        retour=self.pm.rechercherPLprocheDate(dateUnePL)
        self.assertEqual('PL__2017-02-21__20h00.obj', retour)
        
        #test avec une date ou il y'a plusieurs playlist pour ce jour
        datePlusieursPL = datetime.datetime(2017, 4, 9, 14, 50)
        retour=self.pm.rechercherPLprocheDate(datePlusieursPL)
        self.assertEqual('PL__2017-04-09__15h00.obj', retour)
        
        datePlusieursPL = datetime.datetime(2017, 4, 9, 15, 50)
        retour=self.pm.rechercherPLprocheDate(datePlusieursPL)
        self.assertEqual('PL__2017-04-09__15h00.obj', retour)
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPlPlay']
    unittest.main()