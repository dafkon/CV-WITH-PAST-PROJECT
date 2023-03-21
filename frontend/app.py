import pyrebase
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
from kivymd.app import MDApp

Window.size = (360, 640)

config = {
    "apiKey": "AIzaSyATYDUZVmsTC7ZNSz3l7Se_Q-Hc5jCCVLY",
    "authDomain": "buddai-users.firebaseapp.com",
    "databaseURL": "https://buddai-users-default-rtdb.firebaseio.com",
    "projectId": "buddai-users",
    "storageBucket": "buddai-users.appspot.com",
    "messagingSenderId": "98354886950",
    "appId": "1:98354886950:web:84713d4d85421f9357e9e7",
    "measurementId": "G-CXHYNCLX60"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


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


class ForgotPassswordWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class popupclass(FloatLayout):
    pass


class Touch(Widget):
    def on_touch_down(self, touch):
        auth.get_account_info()
        pass

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass


def show_popup():
    pass


# base class
class Buddy(MDApp):
    # Initialize and return root widget
    def build(self):
        global kv
        kv = Builder.load_file("my.kv")
        return kv

    def forgotpassword(self, email):
        try:
            reset = auth.send_password_reset_email(email)
            popup = Popup(title='Please Reset Password', size_hint=(0.8, 0.2),
                          content=Label(text='Your email has been sent \n to reset your password'))
            popup.open()
            kv.current = "Login"
        except:
            popup = Popup(title='Inoccrect email', size_hint=(0.8, 0.2),
                          content=Label(text=' The email you have entered \n is invalid'))
            popup.open()

    def login(self, email, password):
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            kv.current = "Home"
        except:
            popup = Popup(title='Inncorect credintials', size_hint=(0.8, 0.2),
                          content=Label(text='Your email or password is incorrect'))
            popup.open()

        # from firebase import firebase
        # firebase = firebase.FirebaseApplication('https://buddai-users-default-rtdb.firebaseio.com/', None)
        # Get Data
        # result = firebase.get('buddai-users-default-rtdb/Users', '')

        # Get certain column like email or password
        # email and password
        # for i in result.keys():
        # if result[i]['Email'] == email:
        # if result[i]['Password'] == password:
        # kv.current = "Home"

    def signup(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            kv.current = "Login"
        except:
            popup = Popup(title='Incorrect data', size_hint=(0.8, 0.2),
                          content=Label(text='Email is already taken or \n no data has been entered'))
            popup.open()

        # data = {
        # 'Email': email,
        # 'Password': password
        # }
        # post data
        # The database with its name and table
        # db.child("Users").child(username).set(data)

    def logindetails(self):
        sis = auth.current_user
        auth.delete_user_account(sis['idToken'])


# Initializes and helps to run the application
if __name__ == "__main__":
    Buddy().run()
