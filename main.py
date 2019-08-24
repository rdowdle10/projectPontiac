from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionLabel
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from datetime import (
    datetime, timedelta
)
from time import strftime
import time
import os

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
    pass

class OBD2Screen(Screen):
    pass

class SettingsScreen(Screen):
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
        return presentation

    # Replace the following lines to reflect on what you want any buttons to do
    # in the app, then add them into the KV file in the form of
    # 'app.name_of_function()' if a system program were to be executed
    def test(self):
        os.system("notify-send 'Paused music'")

presentation = Builder.load_file("pontiacpc.kv")

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Code to run the program
MainApp().run()

# ---------------------------------------------------------------------