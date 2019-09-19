from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionLabel
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from datetime import (
    datetime, timedelta
)
from time import strftime
import time
import os
import subprocess


Window.size = (800, 480)

# ---------------------------------------------------------------------
# Screenmanager to manage the individual screens
class ScreenManagement(ScreenManager):
    pass

# The creation of the individual screens that will be a part of
# the app.
class MainMenu(Screen):
    pass

class A2DPScreen(Screen):
    def volUpdate(self, *args):
        level = self.value
        subprocess.call(["notify-send", level])
    pass

class OBD2Screen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class TrafficScreen(Screen):
    traffic_img = Image(source='tacoma.png')

    def updateTraffic(self):
        subprocess.call("./update_traffic.sh")
        self.canvas.ask_update()
#        self.traffic_img.reload()

#    def __init__(self, **kwargs):
#        super(TrafficScreen, self).__init__(**kwargs)
#        Clock.schedule_interval(self.update, 10)

#    def update(self, *args):
#        subprocess.call("./update_traffic.sh")
    pass

class OffScreen(Screen):
    pass


# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# The class for the clock label that will be displayed all around
# the app. It calls on itself to avoid any execution issues in the main
# App class (ClockText)
class ClockText(Label):
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime('%I:%M%p')
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Class for the Traffic Map Image

class TrafficImage(Image):

    def __init__(self, **kwargs):
        super(TrafficImage, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
    def update(self, *args):
        self.source = 'tacoma.png'
        self.reload()

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# This particular class will be the Label that outputs the song information in the App using dbus...
#'dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_' + bluetoothdevicemac + '/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track'
# The above monster of a line of code will be used to gather data on media being played through the speakers...

class SongAlbum(Label):
    def __init__(self, **kwargs):
        super(SongAlbum, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Album | grep variant | cut -b 43-500").read()

        self.text = str(bluetoothdataraw)

class SongName(Label):
    def __init__(self, **kwargs):
        super(SongName, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Title | grep variant | cut -b 43-500").read()
        
        self.text = str(bluetoothdataraw)

class SongArtist(Label):
    def __init__(self, **kwargs):
        super(SongArtist, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Artist | grep variant | cut -b 43-500").read()
        
        self.text = str(bluetoothdataraw)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# The following classes are to be used for labels that contain information gathered from the
# Washington Department of Transportation.
class BlockedTraffic(Label):
    def __init__(self, **kwargs):
        super(BlockedTraffic, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
    
    def update(self, *args):
        blktrff = os.popen("cat blockedtraffic").read()
        self.text = str(blktrff)

class SpecialTraffic(Label):
    def __init__(self, **kwargs):
        super(SpecialTraffic, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
    
    def update(self, *args):
        spcltrff = os.popen("cat specialevents").read()
        self.text = str(spcltrff)
    
#    def newupdate(self, *args):
#        # Different way to read text from output?
#        specialTraffic = os.popen("cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500").read()
#        
#        self.text = str(specialTraffic)

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Brainstorming space for volume control...

class VolumeControl(Slider):
    def volUpdate(self, *args):
        level = str(self.value)
        percent = str("%")
        #subprocess.call(["notify-send", level])
        subprocess.call(["amixer", "set", "Master", level + percent])

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# TODO: Create a class for a label that takes the output of
# cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/"
# cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/"
# So that it is displayed once information is downloaded off of the WASHDOT website...

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Class for a clock label that will be displayed on the actionbar (ActionClock)
class ActionClock(ActionLabel):
    def __init__(self, **kwargs):
        super(ActionClock, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime('%I:%M%p')

        
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Button that tests out shell commands...
class ActionTestButton(Button):
    def execute(self):
        os.system("notify-send 'ayy lmao'")



# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Class for the main application
class MainApp(App):


    def build(self):
        #This was temporarily superceded by a startup script that downloads data once
        #car is turned on.
        #TODO: Create a method to manually refresh using a button
        #self.updateTrafficPic()
        return presentation

    # Replace the following lines to reflect on what you want any buttons to do
    # in the app, then add them into the KV file in the form of
    # 'app.name_of_function()' if a system program were to be executed
    def play(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Play")
    def nextsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Next")
    def prevsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Previous")
    def pause(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Pause")

    # The following function will be used to update a live traffic image that portrays
    # data on a commute in pierce county. The updating will be handled by a simple shell
    # script.

    def updateTrafficPic(self):
        os.system("bash updateTrafficPic.sh")
    
    # The following function will allow for the Raspberry Pi's screen to be turned off
    # at the operator's will.

    def screenOff(self):
        os.popen("echo 0 > /sys/class/backlight/rpi_backlight/bl_power")

    def testingBtn(self):
        os.popen("notify-send 'button press success'")



volLvl = NumericProperty()

presentation = Builder.load_file("pontiacpc.kv")

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Code to run the program
MainApp().run()

# ---------------------------------------------------------------------
