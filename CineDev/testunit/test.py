'''
Created on 13 juil. 2017

@author: HOME
'''
import unittest

from Util import Util


class TestUtil(unittest.TestCase):

    def testsecToms(self):
        retour = Util.secToms(75)
        self.assertEqual('1:15', retour)
        retour = Util.secToms(122)
        self.assertEqual('2:02', retour)
        retour = Util.secToms(45)
        self.assertEqual('0:45', retour)

    def testminTosec(self):
        retour = Util.minTosec('3:21')
        self.assertEqual('201', retour)
        retour = Util.minTosec('0:42')
        self.assertEqual('42', retour)
        retour = Util.minTosec('3:07')
        self.assertEqual('187', retour)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()