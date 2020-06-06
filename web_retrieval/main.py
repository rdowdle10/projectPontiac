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
import threading

# Importing BeautifulSoup modules
from bs4 import BeautifulSoup
import shutil
import requests
import string
import fileinput
import os.path
from os import path
import sys

# Import DBUS -> Python functionalities
import dbus

bus = dbus.SystemBus()

# Used for internet connection testing
import socket

# Used for certain commands
import subprocess as sp 

# Before First things first, we have to assign some variables that tie in with my phone:
# Choosing the adapter (this stays the same)
try:
    adapter_object = bus.get_object('org.bluez', '/org/bluez/hci0')
    adapter = dbus.Interface(adapter_object, 'org.bluez.Adapter1')
    device_object = bus.get_object("org.bluez", "/org/bluez/hci0/dev_58_CB_52_51_0C_FB")
    device = dbus.Interface(device_object, "org.bluez.Device1")
    device_properties = dbus.Interface(device, "org.freedesktop.DBus.Properties")
except:
    print("No bluetooth device found! Insert or enable bluetooth before running this program")
    sys.exit()

# Selecting the phone through dbus (hci0, MAC address, "Device1" stays the same)
#device_object = bus.get_object("org.bluez", "/org/bluez/hci0/dev_58_CB_52_51_0C_FB")
#device = dbus.Interface(device_object, "org.bluez.Device1")

# Getting the device properties
#device_properties = dbus.Interface(device, "org.freedesktop.DBus.Properties")


# First things first: Attempt to initiate traffic information download...
# Grab URLs for the pages we are going to use to scrape information from.
url_tac = 'https://www.wsdot.com/traffic/trafficalerts/tacoma.aspx'
url_wsdot = 'https://www.wsdot.com/traffic/trafficalerts/printer.aspx'
tacoma_pic = 'https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png'

stop_threads = False

# Flags to enable certain features under certain conditions
auto_brightness = 1
night_brightness = 0
phone_connected = 0
internet_connected = 0

# CHANGE THIS IN ORDER TO SEE IF EVERYTHING IS WORKING THROUGH THE USE OF CONSOLE OUTPUT
debugging_flag = 0

# Method to check for a connection..
def internetcheck():
    try:
        check = requests.get("https://www.google.com", timeout = 3)
        internet_connected = 1
        #print(internet_connected)
    except requests.exceptions.RequestException as e:
        print("No internet connectivity! Please try again.")
        internet_connected = 0
        print(internet_connected)

# Create an instance to check for internet connectivity in order to determine connectivity
# for internet related tasks, such as traffic information retrieval.
# Now we download the map for Puget Sound...

def dlIMG():
    try:
        resp = requests.get(tacoma_pic, stream=True, timeout = 5)
        with open('tacoma.png', 'wb') as img_file:
            shutil.copyfileobj(resp.raw, img_file)
        del resp
    except requests.exceptions.RequestException as e:
        print('failed')
        return


# Function to grab traffic information...
def trafficRet():
    try:
        traffic_raw_wsdot = requests.get(url_wsdot, timeout = 5)
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
    #except requests.ConnectTimeout:
    #    print("Timed out after 5 seconds")
    #    export_data = open("data_all", "w+")
    #    export_data.write("No connection \n")
    #    print("No connection for data")
    #    export_data.close()
    #    export_tacoma_data = open("tacoma_data", "w+")
    #    export_tacoma_data.write("No connection \n")
    #    print("No connection to get Tacoma data")
    #    export_tacoma_data.close()
    #    return
    
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
# Power Control! Brightness control
# Lower brightness
def brightLow():
    os.popen("echo 10 > /sys/class/backlight/rpi_backlight/brightness")
# Max brightness
def brightMax():
    os.popen("echo 200 > /sys/class/backlight/rpi_backlight/brightness")

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

class SettingsScreen(Screen):
    pass

class InstructionsScreen(Screen):
    pass
#####################################################################

# This class is the basis of the clock that will
# be displayed on the main screen. It will also control the brightness and 
# the checking of an internet connection.
# NOTE: The rest of the labels and actionlabel will have similar functionality.

class ClockText(Label):
    def __init__(self, **kwargs):
        # The following line calls itself...
        super(ClockText, self).__init__(**kwargs)
        # The Clock function repeats the "update" def.
        Clock.schedule_once(self.updateBrightness)
        Clock.schedule_once(self.check_connection)
        Clock.schedule_once(self.check_for_phone)
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.updateBrightness, 60)
        Clock.schedule_interval(self.check_connection, 10)
        Clock.schedule_interval(self.check_for_phone, 10)
        Clock.schedule_interval(self.debugging_output, 3)
    
    def debugging_output(self, *args):
        global debugging_flag
        # This portion determines whether outputs for certain mechanisms are active. This is for debugging
        # system functionality...

        if debugging_flag == 1:
            print("--------------------------------")

        # Portion for internet connectivity
            if internet_connected == 1:
                print("Internet Okay")
            elif internet_connected == 0:
                print("Internet not connected")
        
        # Portion for phone connectivity
            if phone_connected == 1:
                print("Phone is connected")
            elif phone_connected == 0:
                print("Phone not connected")
            
        # Portion for autobrightness
            if auto_brightness == 1:
                print("Autobrightness enabled")
            elif auto_brightness == 0:
                print("Autobrightness disabled")
            
            print("--------------------------------")

        elif debugging_flag == 0:
            pass

    # Function to update the clock.
    def update(self, *args):
        self.text = time.strftime('%I:%M%p')

    # Function to check for an internet conenction. Updates every 10 seconds.
    def check_connection(self, *args):
        global phone_connected
        global internet_connected

        # Trying a threaded approach...
        def checkC(n):
            while n > 0:
                internetcheck()
                n -= 1
            return

        connection_checking_thread = threading.Thread(target = checkC, args = (1, ))
        connection_checking_thread.start()

    def check_for_phone(self, *args):
        # Ensure that variable values are brought in (lines 53 - 54, provided it didn't fail on startup)
        global adapter_object
        global adapter
        global phone_connected

        # Attempt to grab values from phone
        try:
            device_object = bus.get_object("org.bluez", "/org/bluez/hci0/dev_58_CB_52_51_0C_FB")
            device = dbus.Interface(device_object, "org.bluez.Device1")
            # Getting the device properties
            device_properties = dbus.Interface(device, "org.freedesktop.DBus.Properties")

        except:
            #print("Phone not found... ")
            phone_connected = 0
        
        try:

            if str(device_properties.Get("org.bluez.Device1", "Connected")) == str("1"):
                #print("Phone connected!")
                phone_connected = 1
            elif str(device_properties.Get("org.bluez.Device1", "Connected")) == str("0"):
                #print("Phone not connected")
                phone_connected = 0
        
        except:
            #print("Phone not connected...")
            phone_connected = 0



    def updateBrightness(self, *args):
        # Determine if auto brightness is enabled or disabled. Brightness of the screen
        # changes here depending on the time and day.
        global night_brightness
        if auto_brightness == 1:
            #print("Auto Brightness Enabled")
            if int(time.strftime("%H")) > 6 or int(time.strftime("%H")) < 21:
                #print("Brightness set to highest")
                os.popen("sudo su -c 'echo 200 > /sys/class/backlight/rpi_backlight/brightness'")

            elif int(time.strftime("%H")) <= 6 and int(time.strftime("%H")) >= 21:
                #print("Brightness set to minimum")
                os.popen("sudo su -c 'echo 10 > /sys/class/backlight/rpi_backlight/brightness'")
                print(time.strftime("%H"))

        elif auto_brightness == 0:
            print("Auto Brightness Disabled")

        # At this point it is important to determine if it is night or day, as this system is planned to
        # be always on. If it is night the system should not update the brightness at all and should keep it minimal



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
#####################################################################
# Label for credit card skimmer detection instructions
class SkimmerDetect(Label):
    def __init__(self, **kwargs):
        super(SkimmerDetect, self).__init__(**kwargs)
        Clock.schedule_once(self.update)

    def update(self, *args):
        instructions = os.popen("cat instructions").read()
        self.text = str(instructions)

class SkimmerIntro(Label):
    def __init__(self, **kwargs):
        super(SkimmerIntro, self).__init__(**kwargs)
        Clock.schedule_once(self.update)

    def update(self, *args):
        instructions = os.popen("cat skimmerintro").read()
        self.text = str(instructions)
#####################################################################
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
        global phone_connected
        global internet_connected
        if phone_connected == 0:
            phone_error = Popup(title="ERROR",
                content = Label(text=str("Phone not connected. Traffic information unavailable")),
                size_hint=(None, None), size=(400, 125))
            phone_error.open()
            return
        elif internet_connected == 0:
            net_error = Popup(title="ERROR",
                content = Label(text=str("No Connection. Traffic information unavailable")),
                size_hint=(None, None), size=(400, 125))
            net_error.open()
            return
        elif phone_connected == 1 and internet_connected == 1:
            pass

        reloading = Popup(title='Refreshing Traffic Information',
            content=Label(text=str("Please wait!")),
            size_hint=(None, None), size=(200, 125),
            auto_dismiss = False)

        print("Reload button pressed")

        def updateT(n):
            while n > 0:
                reloading.open(animation=False)
                trafficRet()
                dlIMG()
                n -= 1
                time.sleep(3)
                reloading.dismiss()
                
            
        trafficThread = threading.Thread(target = updateT, args = (1, ))
        if not trafficThread.is_alive():
            trafficThread.start()
        elif trafficThread.is_alive():
            print("Please wait until pressing again")


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
#####################################################################
# Buttons for the Skimmer Scanner page.

class ScanBtn(ButtonBehavior, Image):

    def skanner(self):
        def scanning(n):
            while n > 0:
                subprocess.call(["bash", "scan.sh"])
                n -= 1
                time.sleep(12)

        execScan = threading.Thread(target = scanning, args = (1, ))

        if os.popen("lsusb | grep Bluetooth | wc -l | tr -d '\n\r'").read() == str('1'):
            execScan.start()
        else:
            nobt = Popup(title='ERROR',
                content = Label(text=str("Please check Bluetooth Device")),
                size_hint = (None, None), size = (325, 125))
            nobt.open()


class StopScanBtn(ButtonBehavior, Image):
    def stopscan(self):
        #skimmerThread.stop()
        pass

class StoreScan(ButtonBehavior, Image):
    pass

# Label for the skimmerscanner. This is for the counting of detected
# skimemrs

class NumSkimmers(Label):
    #pass
    #def __init__(self, **kwargs):
        #super(NumSkimmers, self).__init__(**kwargs)
        #Clock.schedule_once(self.update)

    def update(self, *args):
        reloading = Popup(title='Scanning...',
            content=Label(text=str("Scanning for skimmers... Please wait!")),
            size_hint=(None, None), size=(325, 125),
            auto_dismiss = False)
        def updateResults(n):
            while n > 0:
                reloading.open()
                n -= 1
                time.sleep(16)
                amount = os.popen("cat scanct | wc -l").read()
                self.text = str(amount)
                reloading.dismiss()
        execLabel = threading.Thread(target = updateResults, args = (1, ))

        if os.popen("lsusb | grep Bluetooth | wc -l | tr -d '\n\r'").read() == str('1'):
            execLabel.start()
        else:
            self.text = str("EE")


#####################################################################
#####################################################################

# Media Label classes -- These are for the labels in the MobileMedia screen that shows current playing media
class SongName(Label):
    def __init__(self, **kwargs):
        super(SongName, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            if phone_connected == 1:
                bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Title | grep variant | cut -b 43-500").read()
                self.text = str(bluetoothdataraw)

            elif phone_connected == 0:
                bluetoothdataraw = str("Error: Bluetooth Device not Connected")
                self.text = str(bluetoothdataraw)
                return
        except:
            bluetoothdataraw = str('No audio playing...')

class SongAlbum(Label):
    def __init__(self, **kwargs):
        super(SongAlbum, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            if phone_connected == 1:
                bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Album | grep variant | cut -b 43-500").read()
                self.text = str(bluetoothdataraw)
            elif phone_connected == 0:
                bluetoothdataraw = "EE"
                self.text = str(bluetoothdataraw)
        except:
            bluetoothdataraw = str(' ')
        

class SongArtist(Label):
    def __init__(self, **kwargs):
        super(SongArtist, self).__init__(**kwargs)
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        try:
            if phone_connected == 1:
                bluetoothdataraw = os.popen("dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track | grep -i -A 2 Artist | grep variant | cut -b 43-500").read()
                self.text = str(bluetoothdataraw)
            elif phone_connected == 0:
                bluetoothdataraw = "EE"
                self.text = str(bluetoothdataraw)
        except:
            bluetoothdataraw = str(' ')


class VolumeLevel(Label):
    def __init__(self, **kwargs):
        super(VolumeLevel, self).__init__(**kwargs)
        Clock.schedule_once(self.update)

    def update(self, *args):
        level = os.popen("amixer sget Master | grep 'Front Right' | awk -F '[][]' '{ print $2 }'").read()
        #level = str('5')
        self.text = str(level)
    
#####################################################################
#####################################################################
# Buttons for System Controls in Settings or wherever they go
class PhoneConnect(ButtonBehavior, Image):
    def initconnect(self):
        #os.popen("bluetoothctl power on")
        os.popen("bluetoothctl -- connect 58:CB:52:51:0C:FB")

class PhoneDisconnect(ButtonBehavior, Image):
    def initdisconnect(self):
        os.popen("bluetoothctl -- disconnect")
        os.popen("bluetoothctl -- scan off")
        os.popen("bluetoothctl -- discoverable off")
        os.popen("bluetoothctl -- power off")

class InternetRequest(ButtonBehavior, Image):
    def internetreq(self):
        os.popen("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB org.bluez.Network1.Connect string:'nap'")


#####################################################################
#####################################################################
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
        pass
        #os.system("notify-send 'SUCCESS'")

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
                os.popen("reboot")
        def cb_shutdown(instance):
                print('SHUTDOWN TEST')
                os.popen("shutdown -h now")
        def cb_restart(instance):
                print('RESTART APP TEST')
                os.popen("killall python3 && python3 main.py")
        
        # The buttons being defined with the above callbacks...
        btnReboot = Button(text=('Reboot'), on_press=(cb_reboot))
        btnHalt = Button(text=('Power Off'), on_press=(cb_shutdown))
        btnRestart = Button(text=('Restart App'), on_press=(cb_restart))

        # Adds all of the above buttons into a container
        btnLayout = BoxLayout()
        btnLayout.add_widget(btnReboot)
        btnLayout.add_widget(btnHalt)
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
    
    def play(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Play")
    def nextsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Next")
    def prevsong(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Previous")
    def pause(self):
        os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB/player0 org.bluez.MediaPlayer1.Pause")

    def on_start(self, **kwargs):
    # Check for a valid phone, bluetooth, and net connection before startup
        def preliminary_check(self):
            try:
                adapter_object = bus.get_object('org.bluez', '/org/bluez/hci0')
                adapter = dbus.Interface(adapter_object, 'org.bluez.Adapter1')
                #device_object = bus.get_object("org.bluez", "/org/bluez/hci0/dev_58_CB_52_51_0C_FB")
                #device = dbus.Interface(device_object, "org.bluez.Device1")
                #device_properties = dbus.Interface(device, "org.freedesktop.DBus.Properties")

            except:
                print("Phone not found... ")
                # Exit the app
                sys.exit()
                phone_connected = 0
    
        def cautionPopup():
            caution = Popup(title='CAUTION',
            content=Label(text=str(os.popen("cat caution").read())),
            size_hint=(None, None), size=(550, 450))
            caution.open()
        cautionPopup()

#####################################################################

#####################################################################
    # Important system scripts
    def initialContact(self):
        global phone_connected
        global internet_connected
        global debugging_flag

        def phone_check():
            global phone_connected
            global internet_connected

            bt_addr_chck = sp.getoutput("bluetoothctl -- info 58:CB:52:51:0C:FB | grep Connected | tr -d '\n\r' | cut -b '13-14'")
            if "no"  in bt_addr_chck:
                if debugging_flag == 1:
                    print("Dluetooth device is NOT connected")
                phone_connected = 0
            else:
                if debugging_flag == 1:
                    print("Device is connected!")
                phone_connected = 1
            

        def internet_check(host="8.8.8.8", port=53, timeout=3):
            global phone_connected
            global internet_connected
            """
            Host: 8.8.8.8 (google-public-dns-a.google.com
            OpenPort: 53/tcp
            Service: domain (DNS/TCP)
            """
            try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                internet_connected = 1
                if debugging_flag == 1:
                    print("An internet connection exists")
                return True
            except socket.error as e:
                print(e)
                if debugging_flag == 1:
                    print("No internet connection available. Check interfaces!")
                internet_connected = 0
                return False

        def connectPhone(n):
            global internet_connected
            global phone_connected
            while n > 0:
                os.popen("bluetoothctl -- connect 58:CB:52:51:0C:FB")
                phone_check()
                time.sleep(2)
                os.popen("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB org.bluez.Network1.Connect string:'nap'")
                time.sleep(2)
                internet_check()
                n -= 1
                return
        
        connectionThread = threading.Thread(target = connectPhone, args = (1, ))

        def attemptConnect():
            global phone_connected
            global internet_connected
            # Attempt to connect to phone media and internet
            connectionThread.start()
            time.sleep(5)

            # Check to see if connection was successful:
            if phone_connected == 1:
                phone_success_yes = str("Phone is connected!")

            elif phone_connected == 0:
                phone_success_no = str("Phone NOT connected. Please check Bluetooth Settings.\n")
            
            # Now checking to see if there is an internet connection:
            if internet_connected == 1:
                net_success_yes = str("Internet connection established")
                
            elif internet_connected == 0:
                net_success_no = str("No existing connection... Please check tethering options on phone\n")

            # If any of the above fail, then show this popup

            # If no tests pass
            if phone_connected == 0 and internet_connected == 0:
                btcheck = Popup(title='ALERT',
                    content = Label(text=str("Please check Bluetooth Connection.")),
                    size_hint = (None, None), size = (400, 125))
                btcheck.open()

            # If internet connection fails
            elif phone_connected == 1 and internet_connected == 0:
                btcheck = Popup(title='ALERT',
                    content = Label(text=str("Internet connection not established. Please try again")),
                    size_hint = (None, None), size = (400, 125))
                btcheck.open()
            
            # If both pass
            elif phone_connected == 1 and internet_connected == 1:
                btcheck = Popup(title='ALERT',
                    content = Label(text=str("Success!")),
                    size_hint = (None, None), size = (400, 125))
                btcheck.open()
        # Now we execute the program:
        attemptConnect()

    # Shutting Down
    def shutDownSys(self):
        os.popen("shutdown -h now")

    # Reboot
    def rebootSys(self):
        os.popen("reboot")

    # Restart the Application
    def restartApp(self):
        os.popen("killall python3 && python3 main.py")

    # Disconnect from phone
    def disconnectBT(self):
        os.popen("bluetoothctl -- disconnect")

    # Reconnect to phone
    def reconnectBT(self):
        global phone_connected
        btcheck = Popup(title='ALERT',
            content = Label(text=str("Please ensure that bluetooth is connected")),
            size_hint = (None, None), size = (400, 125))
        btcheck.open()

        if os.popen("lsusb | grep Bluetooth | wc -l | tr -d '\n\r'").read() == str('1'):
            os.popen("bluetoothctl -- connect 58:CB:52:51:0C:FB")
            phone_connected = 1
        else:
            nobt = Popup(title='ERROR',
                content = Label(text=str("There is an issue with the bluetooth system. Try again.")),
                size_hint = (None, None), size = (400, 125))
            nobt.open()    

    # Request Internet Connectivity
    def requestNet(self):
        global internet_connected
        os.popen("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_58_CB_52_51_0C_FB org.bluez.Network1.Connect string:'nap'")
        
        try:
            check = requests.get("https://www.google.com")
            time.sleep(2)
            internet_connected = 1
        except requests.exceptions.RequestException as e:
            print("No internet connection was established. Please try again.")

    # Turn off bluetooth
    def btShutoff(self):
        global phone_connected
        phone_conencted = 0
        os.popen("bluetoothctl -- disconnect")
        os.popen("bluetoothctl -- scan off")
        os.popen("bluetoothctl -- discoverable off")
        os.popen("bluetoothctl -- power off")

    # Bluetooth Power On
    def btTurnOn(self):
        os.popen("bluetoothctl power on")
        os.popen("bluetoothctl -- connect 58:CB:52:51:0C:FB")

    # Turn on bluetooth discoverability and disconnect from current device
    def btConnectNew(self):
        os.popen("bluetoothctl -- connect")

    # Fix audio streaming (in case the bluetooth module is removed and used elsewhere). NOT FUNCTIONAL
    def fixA2DP(self):
        #os.popen("bluetoothctl -- menu gatt")
        #os.popen("bluetoothctl -- register-service 0000110b-0000-1000-8000-00805f9b34fb")
        print("NOT FUNCTIONAL")

    
#####################################################################
#####################################################################
# Bluetooth scanning scrips. These are for the skimmer scanner app portion
    def skanner(self):
        print("Scanning...")
        subprocess.call(["pwd"])
        subprocess.call(["bash", "bt_scan/scan.sh"])


#####################################################################
#####################################################################
# SCRIPT TO HANDLE AUTOBRIGHTNESS AND MORE WITH THE PRESS OF THE OFFSCREEN BUTTON
    def disableautobright(self):
        global auto_brightness
        auto_brightness = 0

    def enableautobright(self):
        global auto_brightness
        auto_brightness = 1
#####################################################################
#####################################################################
# Finally, running the app with the kvlang file.

presentation = Builder.load_file("main.kv")

MainApp().run()

#####################################################################
