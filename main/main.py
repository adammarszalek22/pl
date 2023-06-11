from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.clock import Clock

from datetime import datetime

from api.pl_api import *
from api.db_api import *
from classes.login_window import LoginWindow
from classes.create_user_window import CreateUser
from classes.main_window import MainWindow

class WindowManager(ScreenManager):
    pass

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('kivy_screens/user.kv')
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Teal'
        return kv

if __name__ == '__main__':
    AwesomeApp().run()