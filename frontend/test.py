# import needed to work with json data
import json
# import used to send http requests with python to, used for the RASA local host server
import requests
from kivy.properties import StringProperty
# manage and navigate through screens
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# used to create parser for parsing the kivy kv file
from kivy.lang import Builder
# utilizes kivy md for Buddy class
from kivymd.app import MDApp

# sets window size to standard phone size
Window.size = (360, 640)


# holds Home screen window
class Homewindow(Screen):
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

        kv = Builder.load_file("test.kv")
        return kv

    def user_message(self, user_input):
        message_history = StringProperty()
        message = user_input
        response = self.response(message)
        # kv.root.ids["message_history"] += f'you: {message}\nChatbot: {response}\n'
        # message_history = f'You: {message}\nChatbot: {response}\n'
        self.message_history += f'You: {message}\nChatbot: {response}\n'
        # print(message_history)

    def response(self, message):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'sender': 'user', 'message': message})
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
        response_data = json.loads(response.text)
        return response_data[0]['text']


# Initializes and helps to run the application
if __name__ == "__main__":
    Buddy().run()
