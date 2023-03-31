import requests
import json
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class ChatApp(App):


    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.message_history = Label(text='')
        message_input = TextInput(multiline=False)
        send_button = Button(text='Send')
        send_button.bind(on_press=self.send_message)
        layout.add_widget(self.message_history)
        layout.add_widget(message_input)
        layout.add_widget(send_button)
        return layout

    def send_message(self, event):
        message_input = self.root.children[1]
        message = message_input.text
        response = self.get_chatbot_response(message)
        self.message_history.text += f'You: {message}\nChatbot: {response}\n'
        message_input.text = ''

    def get_chatbot_response(self, message):
        headers = {'Content-type': 'application/json'}
        data = json.dumps({'sender': 'user', 'message': message})
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
        response_data = json.loads(response.text)
        return response_data[0]['text']

if __name__ == '__main__':
    ChatApp().run()