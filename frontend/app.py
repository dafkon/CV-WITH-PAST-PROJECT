# Import for pyrebase, pyrebase helps to connect the program to firebase services
from tkinter import Button

import pyrebase
# import needed to work with json data
import json
# import used to send http requests with python to, used for the RASA local host server
import requests
from kivy.properties import StringProperty
# sets components from Kivy so that they can be used in kv file and within py file
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# used to create parser for parsing the kivy kv file
from kivy.lang import Builder
# utilizes kivy md for Buddy class
from kivymd.app import MDApp

# sets window size to standard phone size
Window.size = (360, 640)

# Config holds all the necessary keys needed to access the firebase features
# these keys are supplied to the user by firebase themselves
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
# Initializes the firebase components by using the pyrebase import initializing the
# app with the config variable holding of the keys needs
firebase = pyrebase.initialize_app(config)
# DB stores the details for the firebase database that the user has set up on firebase
db = firebase.database()
# Auth stores details for the firebase authenticator, holding user details and
# functions to verify the user
auth = firebase.auth()


# holds login window
class Loginwindow(Screen):
    pass


# holds Sign up window
class Signupwindow(Screen):
    pass


# holds Home screen window
class Homewindow(Screen):
    message_history = StringProperty()
    pass


# holds Forgot password window
class ForgotPassswordWindow(Screen):
    pass


# manages all windows in kv file or py file
class WindowManager(ScreenManager):
    pass


# base class
class Buddy(MDApp):
    # Initialize and return root widget
    message_history = StringProperty()
    def build(self):
        # Global so everything can access kv file mainly just the login and sign up
        global kv
        # Builds kv file
        kv = Builder.load_file("my.kv")
        return kv

    # Forgot password function, that takes the user email, emails them to then reset their password
    def forgotpassword(self, email):
        # Try and catch function, used to catch any errors like the user not typing in
        # the correct email, this then goes to the popup window to prompt the error
        try:
            # Sends the email to the user only if that user is registered to the system
            auth.send_password_reset_email(email)
            # Displays pop up window
            popup = Popup(title='Please Reset Password', title_align='center', size_hint=(0.8, 0.2),
                          content=Label(text='Your email has been sent \n to reset your password', halign='center'))
            popup.open()
            # Returns the user to the login screen
            kv.current = "Login"
        # except used to detect when the email address tpyed in isnt on the system
        except:
            popup = Popup(title='Incorrect email', title_align='center', size_hint=(0.8, 0.3),
                          content=Label(text=' The email you have entered \n is invalid.', halign='center'))
            popup.open()

    # Function used to login
    def login(self, email, password):
        try:
            # Auth signs the user in through auth saving their login, this takes the
            # parameters of email and password which are passed through the kv file
            auth.sign_in_with_email_and_password(email, password)
            kv.current = "Homewindow"
        # used to catch when the user has entered the wrong email or password
        except:
            popup = Popup(title='Inncorect credintials', title_align='center', size_hint=(0.8, 0.3),
                          content=Label(text='Your email or password is incorrect', halign='center'))
            popup.open()

    # function for when the user wants to sign up, takes input from email and password input fields
    def signup(self, email, password):
        try:
            # Creates a new username and password from input and store it in the firebase
            # auth servers
            auth.create_user_with_email_and_password(email, password)
            kv.current = "Login"
        # used to catch when the email has already been used before, or if no data has been inputted
        except:
            popup = Popup(title='Incorrect data', title_align='center', size_hint=(0.8, 0.2),
                          content=Label(text='Email is already taken or \n no data has been entered', halign='center'))
            popup.open()

    def deleteUser(self):
        # takes the current user logged in at the moment and deletes their account
        sis = auth.current_user
        auth.delete_user_account(sis['idToken'])

    def updateprofile(self):
        displayname = 'doug'
        picture = 'https://images.unsplash.com/photo-1575936123452-b67c3203c357?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80'
        sis = auth.current_user
        auth.update_profile(sis['idToken'], displayname, picture)

    def user_message(self, user_input):
        message = user_input
        response = self.response(message)
        self.message_history += f'You: {message}\nChatbot: {response}\n'

    def response(self, message):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'sender': 'user', 'message': message})
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
        response_data = json.loads(response.text)
        return response_data[0]['text']


# Initializes and helps to run the application
if __name__ == "__main__":
    Buddy().run()
