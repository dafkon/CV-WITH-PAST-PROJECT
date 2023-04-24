# Import for pyrebase, pyrebase helps to connect the program to firebase services
import pyrebase
# import needed to work with json data
import json
# import used to send http requests with python to, used for the RASA local host server
import requests
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
# sets components from Kivy so that they can be used in kv file and within py file
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# used to create parser for parsing the kivy kv file
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
# utilizes kivy md for Buddy class
from kivymd.app import MDApp
# python date and time library
from datetime import datetime

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
    # Help section function to display
    def helpsection(self):
        # Loop that access and goes through all the helpline
        for helplines in db.child("helpline").get():
            # Gets all the values for each helpline entry, rules are applied in firebase for the index-on which means
            # that that queries that involves these properties like the ones down below will be more efficient
            name = helplines.val().get("A")
            desc = helplines.val().get("B")
            contact = helplines.val().get("C")
            # converts values that are obtained into strings and stores them into given names
            name = f'{name}'
            desc = f'{desc}'
            contact = f'{contact}'
            # Will create a label widget for each value this then stores it
            title = Label(text="\n" + name, text_size=(360, None), font_size=30, bold=True, halign='center')
            desc = Label(text="\n" + desc, text_size=(360, None), font_size=15, padding=(20, 0))
            contact = Label(text="\n" + "Contact information: " + contact, text_size=(360, 50), padding=(20, 0))
            # Add the label widget to the helpscreen, this loop will then repeat until all values from the database are displayed
            self.ids.helpscreen.add_widget(title)
            self.ids.helpscreen.add_widget(desc)
            self.ids.helpscreen.add_widget(contact)

    pass

    def loadhistory(self):
        # texture size is set to the same value as the height widget which ensure that text wont be cut off making
        # the widget fully visible, this is set in the labels
        self.texture_size = self.height
        # gets the current users ID
        user_id = auth.current_user['localId']
        # differs from the above loop as it's used to find the user id that is saved from the methods below so that
        # chat history can be brought up.
        for Conversations in db.child(user_id).child("conversation").get():
            # Gets all the values for each helpline entry, rules are applied in firebase for the index-on which means
            # that that queries that involves these properties like the ones down below will be more efficient
            message = Conversations.val().get("message")
            response = Conversations.val().get("response")
            time = Conversations.val().get("timestamp")
            # converts values that are obtained into strings and stores them into given names
            message = f'{message}'
            response = f'{response}'
            time = f'{time}'
            # Will create a label widget for each value this then stores it, differs from the method above
            # as it sets it own height based on its size
            message = Label(text="You:\n" + message, text_size=(360, None), font_size=15, halign='right', markup=True,
                            padding=(20, 0), size=(500, self.texture_size / 1.5))
            response = Label(text="Buddy:\n" + response, text_size=(360, None), font_size=15, padding=(20, 0),
                             halign='left', markup=True, size=(500, self.__sizeof__()))
            time = Label(text="\n" + "TimeStamp: " + time, text_size=(360, None), padding=(20, 0), markup=True,
                         size=(500, self.texture_size / 1.5))
            # Add the label widget to the helpscreen, this loop will then repeat until all values from the database are displayed
            self.ids.listlist.add_widget(message)
            self.ids.listlist.add_widget(response)
            self.ids.listlist.add_widget(time)

    # This method is used to check whether the user actually has chat history to show
    # then will display it if it does
    def historyloader(self):
        # find local id
        user_id = auth.current_user['localId']
        # stores it in k by trying to find the value
        k = db.child(user_id).get().val()
        # if no value is found k will equal non but if the value is found it will load the history of the user
        # as the user is always logged in till they have logged out the user_id will always be correct.
        if k is not None:
            # loads history
            self.loadhistory()
        else:
            pass


# holds Forgot password window
class ForgotPassswordWindow(Screen):
    pass


# manages all windows in kv file or py file
class WindowManager(ScreenManager):
    pass


# base class
class Buddy(MDApp):
    # Stores text from user_message method, so it can then be displayed in the .kv file, each method will be a string
    # rather than a label like the other method from above.
    message_user = StringProperty()
    message_response = StringProperty()

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

    # set the current user to None to ensure that no other user is in this current system, auth will do this regardless
    # when the next user logs in, however this is a back-up incase that fails.
    def signout(self):
        auth.current_user = None

    # For displaying a popup window for when the user wants to delete their account
    def popupwindow_DeleteUser(self):
        # Creates box layout to store the popup window widgets
        box = BoxLayout(orientation='vertical', padding=20)
        # adds a label widget
        box.add_widget(
            Label(text="Are you sure you want to delete\n Your account? This cannot be undone.", halign="center"))
        # Creates the popup assigning a title towards it
        popup = Popup(title='ACCOUNT DELETION', title_size=20, title_align='center', content=box,
                      size_hint=(None, None), size=(300, 300), auto_dismiss=True)
        # store the input from the text input into email_input
        email_input = TextInput(multiline=False, hint_text="Email:", size_hint=(0.8, 0.5),
                                pos_hint={"x": 0.1, "top": 0.75})
        # adds email input widget to box layout, is can do this as its considered a textinput object but can also
        # store the user input
        box.add_widget(email_input)
        # stores password input
        password_input = TextInput(multiline=False, password=True, hint_text="Password:", size_hint=(0.8, 0.5),
                                   pos_hint={"x": 0.1, "top": 0.65})
        # adds password input widget to boxlayout
        box.add_widget(password_input)
        # adds button to box layout, this buttons dismisses the popup, this could potentially be removed as when the
        # user clicks out of the popup it closes
        box.add_widget(Button(text="Cancel", on_press=lambda instance: popup.dismiss(), size_hint=(0.5, 0.5),
                              pos_hint={"x": 0.25, "top": 0.55}))
        # adds another button to delete the user, this button sends email & password input along with the popup window
        # to the deleteUser function, it will then run through the function until it is complete
        box.add_widget(Button(text="Delete User", on_press=lambda instance: self.deleteUser(email_input.text,
                                                                                            password_input.text, popup),
                              size_hint=(0.5, 0.5), pos_hint={"x": 0.25, "top": 0.45}))
        # opens popup
        popup.open()

    def deleteUser(self, email_input, password_input, popup):
        # takes the current user logged in at the moment and deletes their account
        user_id = auth.current_user['localId']
        # Access realtime database to get the current user id that is logged in, this method can return none if the user
        # doesn't have a chat-history
        db_user_id = db.child(user_id).get()
        try:
            # logs the user in first by taking the data the user typed from email & password input, if fails goes to
            # except
            auth.sign_in_with_email_and_password(email_input, password_input)
            # compares user_id to db_user_id value to see if they ae both equal, this checks that the k value has a
            # user id in the first place
            if user_id == db_user_id.key():
                # removes that field with the user id
                db.child(user_id).remove(user_id)
            # Gets current user and stores it in sis
            sis = auth.current_user
            # deletes the current user account by using sis and getting its id_token
            auth.delete_user_account(sis['idToken'])
            # signs the user out by calling function
            self.signout()
            # dismiess popup
            popup.dismiss()
            # goes to login screen
            kv.current = "Login"
        # goes to except if any line in the try fails
        except:
            # Creates another pop up to say that details entered for verification are incorrect
            box = BoxLayout(orientation='vertical', padding=20)
            box.add_widget(
                Label(text="Account information is \n incorrect please try again", halign="center"))
            popup2 = Popup(title='Incorrect Credentials', title_size=20, title_align='center', content=box,
                           size_hint=(None, None), size=(200, 200), auto_dismiss=True)
            popup2.open()

    def Deletechats(self):
        # Same layout as popupwindow_DeleteUser minus function used to clear data
        box = BoxLayout(orientation='vertical', padding=20)
        box.add_widget(
            Label(text="Are you sure you want to delete\n Your chat history?", halign="center"))
        popup = Popup(title='CHAT DELETION', title_size=20, title_align='center', content=box,
                      size_hint=(None, None), size=(300, 300), auto_dismiss=True)
        email_input = TextInput(multiline=False, hint_text="Email:", size_hint=(0.8, 0.5),
                                pos_hint={"x": 0.1, "top": 0.75})
        box.add_widget(email_input)
        password_input = TextInput(multiline=False, password=True, hint_text="Password:", size_hint=(0.8, 0.5),
                                   pos_hint={"x": 0.1, "top": 0.65})
        box.add_widget(password_input)
        box.add_widget(Button(text="Cancel", on_press=lambda instance: popup.dismiss(), size_hint=(0.5, 0.5),
                              pos_hint={"x": 0.25, "top": 0.55}))
        # Sends email & password input and popup window but this to clearchathistory
        box.add_widget(Button(text="Delete User", on_press=lambda instance: self.clearchathistory(email_input.text,
                                                                                                  password_input.text,
                                                                                                  popup),
                              size_hint=(0.5, 0.5), pos_hint={"x": 0.25, "top": 0.45}))
        popup.open()

    def clearchathistory(self, email_input, password_input, popup):
        user_id = auth.current_user['localId']
        db_user_id = db.child(user_id).get()
        try:
            # logs the user in first by taking the data the user typed from email & password input, if fails goes to
            # except
            auth.sign_in_with_email_and_password(email_input, password_input)
            # compares user_id to db_user_id value to see if they ae both equal, this checks that the k value has a
            # user id in the first place
            if user_id == db_user_id.key():
                # removes that field with the user id
                db.child(user_id).remove(user_id)
            # dismiss popup
            popup.dismiss()
        # goes to except if any line in the try fails
        except:
            # Creates another pop up to say that details entered for verification are incorrect
            box = BoxLayout(orientation='vertical', padding=20)
            box.add_widget(
                Label(text="Account information is \n incorrect please try again", halign="center"))
            popup2 = Popup(title='Incorrect Credentials', title_size=20, title_align='center', content=box,
                           size_hint=(None, None), size=(200, 200), auto_dismiss=True)
            popup2.open()

    def user_message(self, user_input):
        # Stores user message
        message = user_input
        # Stores chatbot response
        response = self.response(message)
        # Store the user message to then be displayed in the code in the .kv file
        self.message_user = f'You: {message}'
        # Store the chatbot response message to then be displayed in the code in the .kv file
        self.message_response = f'Buddy: {response}'
        # gets current time and date and stores it
        current_time = datetime.now()
        # uses python library to format the current time into string format. the letters display
        # the format that it appears in.
        timestamp = current_time.strftime("%d\%m\%Y %H:%M:%S")
        # This is a python dictionary that contains three key values. It stores messages from the user, response from
        # the chatbot and the timestamp.
        data = {"message": message, "response": response, "timestamp": timestamp}
        # get the user local id
        user_id = auth.current_user['localId']
        # retries the conversation data for a specifc user from a firebase Realtime database
        # or returns and empty list if there is no data
        conversation = db.child(user_id).child("conversation").get().val() or []
        # used to append new item to conversation, this passes the data dictionary as a parameter.
        conversation.append(data)
        # used to update the conversation data for a particular user, adding another field that stores reposes, messages
        # and time stamps
        db.child(user_id).update({"conversation": conversation})

    def response(self, message):
        # This is used to specify the type of data being sent to the HTTP request
        headers = {'content-type': 'application/json'}
        # Creates a json formatted string, it has both key values of sender and user
        # and message with the value of the message variable
        data = json.dumps({'sender': 'user', 'message': message})
        # Sends a http post request to the RASAa chatbot URL using the previous created
        # headers and data it then assigns that to the response
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
        # Uses json module to parse the response text, it then assigns it to response data to be returned
        response_data = json.loads(response.text)
        # Returns response_data with the first response in response data
        return response_data[0]['text']


# Initializes and helps to run the application
if __name__ == "__main__":
    Buddy().run()
