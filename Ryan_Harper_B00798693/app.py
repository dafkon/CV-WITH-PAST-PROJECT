import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
Window.size = (360, 640)
class Loginwindow(Screen):
    pass
class Signupwindow(Screen):
    pass
class Homewindow(Screen):
    pass
class Chatnotwindow(Screen):
    pass
class Settingswindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")



class popupclass(FloatLayout):
    pass

class Touch(Widget):
    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass
def show_popup():
    pass

#base class
class Buddy(App):
    #Initialize and return root widget
    def build(self):
        return kv
#Initializes and helps to run the application
if __name__ == "__main__":
    Buddy().run()
