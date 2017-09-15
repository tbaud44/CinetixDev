#-*- coding: utf-8 -*-
'''
Created on 14 mai 2017

@author: internet et Thierry baudouin
code repris et adapte à partir du source
https://forum.videolan.org/viewtopic.php?t=128595 
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
import platform
from threading import Thread, Event
import time
from tkinter import ttk

import vlc

import tkinter as Tk


# import standard libraries
class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters



class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None, fullscreen=False, paramVLC='', geometry='' ):
        Tk.Frame.__init__(self, parent)
    
        if not parent: 
            wdw = Tk.Toplevel(bg="black")
            self.parent = wdw
        else:
            self.parent = parent    
        if geometry:
            self.parent.geometry(geometry)
            #self.parent.update()
        if fullscreen:
            #self.parent.attributes('-fullscreen', 2) #fonctionne bien que sous linux
            #self.parent.wm_state(newstate="zoomed") #test ne fonctionne que sous windows et pas bien
            #self.parent.overrideredirect(True) # que sous windows. supprime decoration fenetre
            i=1
        #wdw.geometry('+400+400')
        self.debug = False
        self.fullscreen = fullscreen
        self.videoPlayedTerminee = True #video pas encore jouee 
          
        self.parent.protocol("WM_DELETE_WINDOW", self.quitter)

        if title == None:
            title = "tk_vlc"
        if not fullscreen:    
            self.parent.title(title)

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        
        #en mode plein ecran, aucun bouton de commande
        if not fullscreen:
            ctrlpanel = ttk.Frame(self.parent)
            pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
            play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
            stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
            volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
            pause.pack(side=Tk.LEFT)
            play.pack(side=Tk.LEFT)
            stop.pack(side=Tk.LEFT)
            volume.pack(side=Tk.LEFT)
            self.volume_var = Tk.IntVar()
            self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel, 
                    from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
            self.volslider.pack(side=Tk.LEFT)
            ctrlpanel.pack(side=Tk.BOTTOM)
    
            ctrlpanel2 = ttk.Frame(self.parent)
            self.scale_var = Tk.DoubleVar()
            self.timeslider_last_val = ""
            self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel, 
                    from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
            self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
            self.timeslider_last_update = time.time()
            ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)
         
        if paramVLC:
                self.Instance = vlc.Instance(paramVLC)
        else:
                self.Instance = vlc.Instance()    
             
        # VLC player controls
        
        self.player = self.Instance.media_player_new()

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        self.__setWindowId()
        self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this

    def quitter(self):
        self.timer.stop()
        if not self.fullscreen:
            self.timeslider.destroy() 
        self.player.stop()
        self.parent.destroy()     # stops mainloop
                   
    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def isVideoFinished(self):
        """renvoie booleen.
        """
       # print (self.videoPlayedTerminee)
        return self.videoPlayedTerminee


    def __setWindowId(self):
        '''methode lie a l interface graphique de l OS'''
             # set the window id where to render VLC's video output
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.GetHandle())
        else:
            self.player.set_xwindow(self.GetHandle()) # this line messes up windows
           
    def play(self, videoFile):
        '''declenchement manuel du play
        p1 videoFile
        '''
        media = self.Instance.media_new(videoFile)
        self.player.set_media(media)
        
        self.videoPlayedTerminee = False  #booleen qui permet de savoir si la video jouee est terminee ou pas
        
        self.player.play() # hit the player button
       
            # set the volume slider to the current volume
            #self.volslider.SetValue(self.player.audio_get_volume() / 2)
        if not self.fullscreen:    
            self.volslider.set(self.player.audio_get_volume())

   
    def OnPlay(self):
        
            # Try to launch the media, if this fails display an error message
        if self.player.play() == -1:
            self.errorDialog("Impossible de jouer.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    #def OnPause(self, evt):
    def OnPause(self):
        """Pause the player.
        """
        self.player.pause()

    def OnStop(self):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        if not self.fullscreen:
            self.timeslider.set(0)

    def OnTimer(self):
        """Update the time slider according to the current movie time.
        le timeslider est un widget en mode non fullscreen
        """
        if self.player == None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length() #duree video en ms
        dbl = length * 0.001
        if not self.fullscreen:
            self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        if not self.fullscreen:
            self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
       # print (self.player.get_length())
       # print("dbl est {} et lenght {}.".format(dbl,length * 0.001))
        if not self.fullscreen:
            if time.time() > (self.timeslider_last_update + 2.0):
                self.timeslider.set(dbl)
        if self.debug:        
            print ("dbl {0} et length {1} ".format(dbl, length * 0.001))        
        if self.__estTerminee(tyme, length): #la lecture de la video est terminee
            self.OnStop() #ne marche pas trop
           # self.timer.stop()     #on tue le thread du timer
            self.videoPlayedTerminee = True   

    def __estTerminee(self, dureeTotale, dureeEnCours):
        '''marge erreur de 300 ms'''
        if dureeEnCours > 0 and abs(dureeEnCours - dureeTotale)<300: #la lecture de la video est terminee
            return True
        else:
            return False
        
    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            # this is a hack. The timer updates the time slider. 
            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
            # I can't tell the difference between when the user has manually moved the slider and when
            # the timer changed the slider. But when the user moves the slider tkinter only notifies
            # this rtn about once per second and when the slider has quit moving.
            # Also, the tkinter notification value has no fractional seconds.
            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
            # we know that this notification is due to the timer changing the slider.
            # otherwise the notification is due to the user changing the slider.
            # if the user is changing the slider then I have the timer routine wait for at least
            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the 
            # user)
            #selection = "Value, last = " + sval + " " + str(self.timeslider_last_val)
            #print("selection= ", selection)
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval)) # expects milliseconds


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            #self.errorDialog("Failed to set volume")
            print ("Warning: Probleme pour changer volumz")



    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        """Set the volume according to the volume sider.
        """
        volume = self.volume_var.get()
        print("volume= ", volume)
        #volume = self.volslider.get() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """    
        edialog = Tk.messagebox.showerror(self, 'Error', errormessage)

        