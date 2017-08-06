#-*- coding: utf-8 -*-
'''
Created on 14 mai 2017

@author:  internet et Thierry baudouin
code repris et adapte à partir du source
https://forum.videolan.org/viewtopic.php?t=128595 
Classe utilisant le module vlc afin de calculer la duree d'une video
'''
#! /usr/bin/python
# -*- coding: utf-8 -*-

#
# tkinter example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""
A simple example for VLC python bindings using tkinter. Uses python 3.4

Author: Patrick Fay
Date: 23-09-2015
"""

# import external libraries
import os
import time

import vlc


# import standard libraries
class Player():
    """The main window has to deal with events.
    """
    def __init__(self):
            # VLC player controls
        self.Instance = vlc.Instance("--vout", "dummy", "--no-audio"  )
        self.player = self.Instance.media_player_new()

    
    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def _OnOpen(self, mrl):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
     
        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        if os.path.isfile(mrl):
            #print (mrl)
            # Creation
            self.Media = self.Instance.media_new(mrl)
           # self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            # Report the title of the file chosen
            
            # set the volume slider to the current volume
            #self.volslider.SetValue(self.player.audio_get_volume() / 2)
           
    def _OnPlay(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
            # Try to launch the media, if this fails display an error message
        if self.player.play() == -1:
            self.errorDialog("Unable to play.")
            #self.SetVolume(volume)    
    
    def _OnStop(self):
        """Stop the player.
        """
        self.player.stop()
    
    
    """ retourne la duree en seconde de la video """ 
    def _GetDurationCurrentPlaying(self):
        return self.player.get_length() / 1000
    
    
    def GetDurationVideo(self, nomVideo, repertoire):
        self._OnOpen(str(os.path.join(repertoire, nomVideo)))
                
        self._OnPlay()
        time.sleep(1) #on attend une seconde pour que vlc charge entete
        duration = self._GetDurationCurrentPlaying()
        self._OnStop()
        return duration       
    