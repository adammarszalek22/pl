from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition

from classes.login import LoginWindow
from classes.create_user import CreateUser
from classes.groups import GroupsWindow
from classes.main_window import MainWindow
from classes.view_score import ViewScoreWindow
from classes.my_groups import MyGroupsWindow
from classes.groups_im_in import GroupsImIn
from classes.view_others import ViewOtherScoreWindow


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.prev_screen = {
            'GroupsWindow': 'MainWindow',
            'ViewScoreWindow': 'MainWindow',
            'MyGroupsWindow': 'GroupsWindow',
            'GroupsImIn': 'GroupsWindow',
            'ViewOtherScoreWindow': 'MainWindow'
        }
        self.transition = NoTransition()
        Window.bind(on_keyboard=self.keys)

    def keys(self, window, key, *largs):
        if key == 27:
            self.go_back()
            return True
        
    def go_back(self):
        try:
            self.current = self.prev_screen[self.current]
        except KeyError:
            pass

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('kivy_screens/user.kv')
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        return kv

if __name__ == '__main__':
    AwesomeApp().run()