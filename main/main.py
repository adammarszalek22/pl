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
from db import *
from classes.login_window import LoginWindow
from classes.create_user_window import CreateUser
from classes.main_window import MainWindow
from classes.groups_window import GroupsWindow
from classes.view_score_window import ViewScoreWindow
from classes.my_groups_window import MyGroupsWindow
from classes.groups_im_part_of_window import GroupsImPartOf
from classes.view_other_score_window import ViewOtherScoreWindow

class WindowManager(ScreenManager):
    def go_back(self):
        if self.current == 'GroupsWindow':
            self.current = 'MainWindow'
        elif self.current == 'ViewScoreWindow':
            self.current = 'MainWindow'
        elif self.current == 'MyGroupsWindow':
            self.current = 'GroupsWindow'
        elif self.current == 'GroupsImPartOf':
            self.current = 'GroupsWindow'
        elif self.current == 'ViewOtherScoreWindow':
            self.current = 'MainWindow'

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('kivy_screens/user.kv')
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        return kv

if __name__ == '__main__':
    AwesomeApp().run()