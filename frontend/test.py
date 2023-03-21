from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
Window.size = (360, 640)
class ContentNavigationDrawer(BoxLayout):
    pass
class BuddyAI(MDApp):
    def build(self):

        return Builder.load_file('test.kv')

if __name__ == "__main__":
    BuddyAI().run()