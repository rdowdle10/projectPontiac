from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionLabel
from kivy.uix.behaviors import ButtonBehavior
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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup, PopupException
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp
from datetime import (
    datetime, timedelta
)
from time import strftime
import time
import os
import subprocess

# Importing BeautifulSoup modules
from bs4 import BeautifulSoup
import shutil
import requests
import string
import fileinput
import os.path
from os import path
import sys

# First things first: Attempt to initiate traffic information download...
# Grab URLs for the pages we are going to use to scrape information from.
url_tac = 'https://www.wsdot.com/traffic/trafficalerts/tacoma.aspx'
url_wsdot = 'https://www.wsdot.com/traffic/trafficalerts/printer.aspx'
tacoma_pic = 'https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png'

# Now we download the map for Puget Sound...
def dlIMG():
    try:
        resp = requests.get(tacoma_pic, stream=True)
        with open('tacoma.png', 'wb') as img_file:
            shutil.copyfileobj(resp.raw, img_file)
        del resp
    except requests.exceptions.RequestException as e:
        print('failed')


# Function to grab traffic information...
def trafficRet():
    try:
        traffic_raw_wsdot = requests.get(url_wsdot)
    except requests.exceptions.RequestException as e:
        export_data = open("data_all", "w+")
        export_data.write("No connection \n")
        print("No connection for data")
        export_data.close()
        export_tacoma_data = open("tacoma_data", "w+")
        export_tacoma_data.write("No connection \n")
        print("No connection to get Tacoma data")
        export_tacoma_data.close()
        return

    traffic = BeautifulSoup(traffic_raw_wsdot.text, 'html.parser')
    # Remove any and all <a> elements in the page
    [x.extract() for x in traffic.find_all('a')]

    # Find all div's that contain the information we want...
    all_useful_info = traffic.find("div", class_="printerList")

    # Then print the output... (when uncommented)
    all_data_cont = all_useful_info.get_text()
    #print(all_data_cont)

    # Once we get our data, we must put it in a file
    export_data = open("data_all", "w+")
    export_data.write(all_data_cont)
    export_data.close()

    # The following section is for traffic in Tacoma
    try:
        traffic_raw_tac = requests.get(url_tac)
    except requests.exceptions.RequestException as e:
        export_tacoma_data = open("tacoma_data", "w+")
        export_tacoma_data.write("No connection \n")
        return
        #raise SystemExit(e)

    tacoma_traffic = BeautifulSoup(traffic_raw_tac.text, 'html.parser')
    # Remove any and all <a> elements in the page
    [x.extract() for x in tacoma_traffic.find_all('a')]
    [x.extract() for x in tacoma_traffic.find("div", class_="situationHeader")]

    # Find all of the <div> elements with the "situationDiv" class. These contain
    # the desired information in this website's case.
    all_tacoma_info = tacoma_traffic.find("div", class_="situationDiv")
    #print(all_tacoma_info)

    # Grab all text after parsing is complete.
    tacoma_data_cont = all_tacoma_info.get_text()

    # Remove the whitespace in the beginning of the output for traffic.
    tacoma_data_final = tacoma_data_cont.lstrip()
    #print(tacoma_data_final)

    # Export all of the above work into a file
    export_tacoma_data = open("tacoma_data", "w+")
    export_tacoma_data.write(tacoma_data_final)
    export_tacoma_data.close()

    # For whatever reason, the file printed contains unnecessary \n, so we will be modifying
    # the file to remove them
    counter = 0
    for line in fileinput.input('tacoma_data', inplace=True):
        if not counter:
            if line.startswith('HIGHEST IMPACT'):
                counter = 3
            else:
                print(line, end='')
        else:
            counter -= 1

    counter = 0
    for line in fileinput.input('tacoma_data', inplace=True):
        if not counter:
            if line.startswith('HIGH IMPACT'):
                counter = 3
            else:
                print(line, end='')
        else:
            counter -= 1

    counter = 0
    for line in fileinput.input('tacoma_data', inplace=True):
        if not counter:
            if line.startswith('MODERATE IMPACT'):
                counter = 3
            else:
                print(line, end='')
        else:
            counter -= 1

    counter = 0
    for line in fileinput.input('tacoma_data', inplace=True):
        if not counter:
            if line.startswith('LOW IMPACT'):
                counter = 3
            else:
                print(line, end='')
        else:
            counter -= 1

    counter = 0
    for line in fileinput.input('tacoma_data', inplace=True):
        if not counter:
            if line.startswith('LOWEST IMPACT'):
                counter = 3
            else:
                print(line, end='')
        else:
            counter -= 1

class TrafficImage(Image):
    def __init__(self, **kwargs):
        super(TrafficImage, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 1800)
        self.source = 'tacoma.png'
    def update(self, *args):
        try:
            resp = requests.get(tacoma_pic, stream=True)
            with open('tacoma.png', 'wb') as img_file:
                shutil.copyfileobj(resp.raw, img_file)
            del resp

            self.source = 'tacoma.png'
            self.reload()

        except requests.exceptions.RequestException as e:
            self.source = 'no_connection.png'
            self.reload()


# Creating the window, complete with size and page management.
Window.size = (800, 480)

#####################################################################

# Now specifying which screens are avaiable in the application.
# MUST BE SPECIFIED IN MAIN.KV FOR THEM TO BE VISIBLE TO THE APPLICATION

class ScreenManagement(ScreenManager):
    pass

class MainMenu(Screen):
    pass

class MediaScreen(Screen):
    pass

class TrafficScreen(Screen):
    pass

class TrafficScreenAll(Screen):
    pass

class TrafficScreenTacoma(Screen):
    pass

class TrafficScreenSeattle(Screen):
    pass

class SkimmerScanner(Screen):
    pass

class AllApps(Screen):
    pass

class OffScreen(Screen):
    pass

#####################################################################

# This class is the basis of the clock that will
# be displayed on the main screen.
# NOTE: The rest of the labels and actionlabel will have similar functionality.
class ClockText(Label):
    def __init__(self, **kwargs):
        # The following line calls itself...
        super(ClockText, self).__init__(**kwargs)
        # The Clock function repeats the "update" def.
        Clock.schedule_interval(self.update, 1)

    # Function to update the clock.
    def update(self, *args):
        self.text = time.strftime('%I:%M%p')

# Now for the clock that will be on the top bar of every screen
class ActionClock(ActionLabel):
    def __init__(self, **kwargs):
        super(ActionClock, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime('%I:%M%p')

# Label for traffic data for all of WA
class TrafficAll(Label):
    def __init__(self, **kwargs):
        super(TrafficAll, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 1800)
    
    def update(self, *args):
        spcltrff = os.popen("cat data_all").read()
        #spcltrff = subprocess.check_output(["cat", "data_all"])
        self.text = str(spcltrff)

class TrafficTacoma(Label):
    def __init__(self, **kwargs):
        super(TrafficTacoma, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 1800)
    
    def update(self, *args):
        spcltrff = os.popen("cat tacoma_data").read()
        self.text = str(spcltrff)

    
#####################################################################



# Volume control buttons

class VolUp(ButtonBehavior, Image):
    def volUp(self, *args):
        level = str('5')
        percent = str("%")
        up = str("+")
        subprocess.call(["amixer", "set", "Master", level + percent + up])

    #pass

class VolMute(ButtonBehavior, Image):
    pass

class AudioCancel(ButtonBehavior, Image):
    pass

class VolDown(ButtonBehavior, Image):
    def volDown(self, *args):
        level = str('5')
        percent = str('%')
        down = str('-')
        subprocess.call(["amixer", "set", "Master", level + percent + down])
    #pass

class Reload(ButtonBehavior, Image):
    def update(self, *args):
        initial = Popup(title='Updating Traffic Information',
        content=Label(text="Loading, please wait..."),
        size_hint=(None, None), size=(300, 150))
        initial.open(animation=False)
        print("Initializing traffic refresh...")
        time.sleep(2)
        initial.dismiss()
        trafficRet()
        dlIMG()
    #pass

class Play(ButtonBehavior, Image):
    pass

class Pause(ButtonBehavior, Image):
    pass

class Next(ButtonBehavior, Image):
    pass

class Previous(ButtonBehavior, Image):
    pass


#####################################################################

# Dock buttons

class MediaScreenBtn(ButtonBehavior, Image):
    pass

class TrafficScreenBtn(ButtonBehavior, Image):
    #pass
    def update(self):
        print("Traffic screen load success")
        trafficRet()
        dlIMG()
        os.popen("notify-send hi")

class SkimmerScannerBtn(ButtonBehavior, Image):
    pass

class AllAppsBtn(ButtonBehavior, Image):
    pass

#####################################################################

# Media Label classes -- These are for the labels in the MobileMedia screen that shows current playing media
class SongAlbum(Label):
    def __init__(self, **kwargs):
        super(SongAlbum, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Album | grep variant | cut -b 43-500").read()
        except:
            bluetoothdataraw = str('No Data')
        
        self.text = str(bluetoothdataraw)

class SongName(Label):
    def __init__(self, **kwargs):
        super(SongName, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Title | grep variant | cut -b 43-500").read()
        except:
            bluetoothdataraw = str('No Data')
        self.text = str(bluetoothdataraw)

class SongArtist(Label):
    def __init__(self, **kwargs):
        super(SongArtist, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Artist | grep variant | cut -b 43-500").read()
        except:
            bluetoothdataraw = str('No Data')
        self.text = str(bluetoothdataraw)


class VolumeLevel(Label):
    def __init__(self, **kwargs):
        super(VolumeLevel, self).__init__(**kwargs)
        Clock.schedule_once(self.update)

    def update(self, *args):
        level = os.popen("amixer sget Master | grep 'Front Right' | awk -F '[][]' '{ print $2 }'").read()
        #level = str('5')
        self.text = str(level)
    
    
    
#####################################################################

# Main App Functions

class MainApp(App):

    def cautionPopup(self):
        caution = Popup(title='CAUTION',
            content=Label(text=str(os.popen("cat caution").read())),
            size_hint=(None, None), size=(550, 400))
        caution.open()
        time.sleep(10)
        caution.dismiss()

    # Instruct kivy to create the UI with the elements mentioned in the .kv file
    def build(self):
        return presentation

    # Test function. This is used to see if any UI elements work
    def test(self):
        os.system("notify-send 'SUCCESS'")

    # The function for the "About Popup". This specifies a function, which contains a
    # popup with the content outlined in the about file in the root directory.
    
    def aboutBtn(self):
        aboutPopup = Popup(title='About this software',
            content=Label(text=str(os.popen("cat about").read())),
            size_hint=(None, None), size=(550, 400))
        aboutPopup.open()

    # This function shows a popup with common power tasks. Can also initiate a restart of the app itself
    def powerPopup(self):
        # The next 4 functions are the callbacks that initiate any of the power elements (halt, reboot, disconnect all peripherals, etc.)
        def cb_reboot(instance):
                print('REBOOT TEST')
        def cb_shutdown(instance):
                print('SHUTDOWN TEST')
        def cb_restart(instance):
                print('RESTART APP TEST')
                os.popen("killall python && python main.py")
        def cb_disconnect(instance):
                print('DISCONNECT TEST')
                pwr.dismiss()
        
        # The buttons being defined with the above callbacks...
        btnReboot = Button(text=('Reboot'), on_press=(cb_reboot))
        btnHalt = Button(text=('Power Off'), on_press=(cb_shutdown))
        btnDisconnect = Button(text=('Disconnect'), on_press=(cb_disconnect))
        btnRestart = Button(text=('Restart App'), on_press=(cb_restart))

        # Adds all of the above buttons into a container
        btnLayout = BoxLayout()
        btnLayout.add_widget(btnReboot)
        btnLayout.add_widget(btnHalt)
        btnLayout.add_widget(btnDisconnect)
        btnLayout.add_widget(btnRestart)

        # Defining the pop up menu itself. 
        pwr = Popup(title='Power options',
            content = 
                btnLayout,
                size_hint=(None, None), 
                size=(400, 125)
            )
        
        # And finally a way to open the popup menu when called upon
        pwr.open()

#####################################################################

# Functions to call upon when doings things like pausing a song, playing, reconnecting to the phone, etc.

    def reconnectDev(self):
        os.popen("bluetoothctl -- connect AA:BB:CC:DD:EE:FF")
        os.popen("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF org.bluez.Network1.Connect string:'nap'")
    
    def play(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.bluez.MediaPlayer1.Play")
    def nextsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.bluez.MediaPlayer1.Next")
    def prevsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.bluez.MediaPlayer1.Previous")
    def pause(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF/player0 org.bluez.MediaPlayer1.Pause")

    def on_start(self, **kwargs):
        def cautionPopup():
            caution = Popup(title='CAUTION',
            content=Label(text=str(os.popen("cat caution").read())),
            size_hint=(None, None), size=(550, 450))
            caution.open()
        cautionPopup()

#####################################################################

# Finally, running the app with the kvlang file.

presentation = Builder.load_file("main.kv")

MainApp().run()

#####################################################################