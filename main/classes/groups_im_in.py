from api.db_api import groups_im_in, my_user_info

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen

class GroupsImIn(Screen):

    def display_the_groups(self):

        if self.ids.carousel.children:
            return

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
                self._label = MDLabel(text = heading)
                self._label.font_size = '12dp'
                grid_layout.add_widget(self._label)

            position = 1
            for user in positions:

                get_user = my_user_info(app.access_token, user)


                self.position = MDLabel(text = str(position))
                self.username = MDLabel(text = get_user["username"])
                self.points = MDLabel(text = str(get_user["points"]))
                self.three_pointers = MDLabel(text = str(get_user["three_pointers"]))
                self.one_pointers = MDLabel(text = str(get_user["one_pointers"]))

                self.position.font_size = '12dp'
                self.username.font_size = '12dp'
                self.points.font_size = '12dp'
                self.three_pointers.font_size = '12dp'
                self.one_pointers.font_size = '12dp'


                grid_layout.add_widget(self.position)
                grid_layout.add_widget(self.username)
                grid_layout.add_widget(self.points)
                grid_layout.add_widget(self.three_pointers)
                grid_layout.add_widget(self.one_pointers)
                position += 1

            box_layout.add_widget(grid_layout)
            box_layout.add_widget(MDLabel(text = 'Swipe left to see more'))
            self.ids.carousel.add_widget(box_layout)