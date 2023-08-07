from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition

class GroupsImPartOf(Screen):

    def display_the_groups(self):

        self.ids.carousel.clear_widgets()
        app = MDApp.get_running_app()
        groups = groups_im_in(app.access_token)

        if groups["list"] == None:
             self.ids.carousel.add_widget(
                  MDBoxLayout(
                    MDLabel(
                        text = 'You either do not have any groups or an error occurred',
                        halign = 'center'
                    )
                  )
             )
             return 0

        for group in groups["list"]:  

            box_layout = MDBoxLayout(orientation = 'vertical', padding = 30, spacing = 5)
            
            grid_layout = MDGridLayout(
                cols = 5,
                size_hint_y = None,
                height = app.root.height / 10,
                spacing = 5
                )
            self.heading_label = MDLabel(
                text = group["name"],
                halign = 'center',
                size_hint_y = None,
                height = app.root.height / 10
                )
            
            box_layout.add_widget(self.heading_label)
            try:
                positions = group["positions"].split(' ')
            except AttributeError:
                positions = []

            headings = ["Position", "Username", "Points", "Three pointers", "One pointers"]
            for heading in headings:
                grid_layout.add_widget(MDLabel(text = heading))

            position = 1
            for user in positions:
                get_user = my_user_info(app.access_token, user)
                grid_layout.add_widget(MDLabel(text = str(position)))
                grid_layout.add_widget(MDLabel(text = get_user["username"]))
                grid_layout.add_widget(MDLabel(text = str(get_user["points"])))
                grid_layout.add_widget(MDLabel(text = str(get_user["three_pointers"])))
                grid_layout.add_widget(MDLabel(text = str(get_user["one_pointers"])))
                position += 1

            box_layout.add_widget(grid_layout)
            box_layout.add_widget(MDLabel(text = 'Swipe left to see more'))
            self.ids.carousel.add_widget(box_layout)