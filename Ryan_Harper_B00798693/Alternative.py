import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import widget
#base class
class Alternative(App):
    #Initialize and return root widget
    def build(self):
        return Login()

#Creating Gridlayout, this has been imported from kivy GridLayout
class Login(widget):
    def __init__(self, **kwargs):
        super(Login,self).__init__(**kwargs)
        #Setting Grid size
        self.cols = 1

        self.inside = GridLayout ()
        self.inside.cols = 2

        self.inside.add_widget(Label(text='User Name', font_size = 20))
        self.username = TextInput(multiline=False)
        self.inside.add_widget(self.username)

        self.inside.add_widget(Label(text='password', font_size = 20, ))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.add_widget(self.inside)


        self.submit = Button(text = "login", font_size = 20)
        self.submit.bind(on_press=self.click)
        self.add_widget(self.submit)

    def click(self, instance):
        username= self.username.text
        password = self.password.text

        print("Username:"+username)

        self.username.text = ""
        self.password.text = ""

#Initializes and helps to run the application
if __name__ == "__main__":
    Alternative().run()