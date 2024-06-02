import re
import requests
import json
import subprocess
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

# Custom button class without texture
class TexturedButton(Button):
    def __init__(self, **kwargs):
        super(TexturedButton, self).__init__(**kwargs)

# Custom bordered box class with background color
class TexturedBox(BoxLayout):
    def __init__(self, **kwargs):
        super(TexturedBox, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Custom layout class with background texture
class TexturedLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(TexturedLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source='images/bgtexture.png', size=Window.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)
            Window.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = Window.size
        self.rect.pos = self.pos

# Function to load opposites from JSON file
def load_opposites(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to normalize card name
def normalize_card_name(name):
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = name.lower()  # Convert to lowercase
    return name

# Function to search for a card using the Scryfall API
def search_card(card_name):
    normalized_name = normalize_card_name(card_name)
    url = f"https://api.scryfall.com/cards/named?fuzzy={normalized_name}"
    response = requests.get(url)
    if response.status_code == 200:
        card_data = response.json()
        return card_data
    else:
        return None

# Function to convert Oracle text to its mechanical opposite
def opposite_mechanic(text, opposites):
    for key, value in opposites.items():
        text = re.sub(key, value, text, flags=re.IGNORECASE)
    return text

# Function to speak the text using the 'say' command on macOS
def speak_text(text):
    subprocess.call(['say', text])

# Kivy App
class EmTeeGeeApp(App):
    def build(self):
        self.layout = TexturedLayout(orientation='vertical', padding=(0, 10), spacing=10)

        # Add banner image
        self.banner = Image(source='images/banner.png', size_hint_y=None, height=150)  # Increase the size of the banner
        self.layout.add_widget(self.banner)

        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=(20, 0, 20, 0), spacing=10)
        
        self.card_name_input = TextInput(hint_text='Enter the name of the MTG card', multiline=False, height=60, size_hint=(None, 1), width=800, font_size='20sp', font_name='Roboto-Bold')
        input_layout.add_widget(self.card_name_input)

        self.search_button = TexturedButton(text='Search Card', height=60, size_hint=(None, 1), width=300, font_size='20sp', bold=True)
        self.search_button.bind(on_press=self.on_search_button_pressed)
        input_layout.add_widget(self.search_button)

        self.layout.add_widget(input_layout)

        # Textured box for the result with background color
        self.textured_box = TexturedBox(size_hint=(1, None), height=500, padding=10)
        self.result_scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(size_hint_y=None, text='', markup=True, text_size=(Window.width - 60, None), color=(0, 0, 0, 1))  # Set text color to black
        self.result_label.bind(size=self._update_text_size, texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        self.textured_box.add_widget(self.result_scroll)
        self.layout.add_widget(self.textured_box)

        # Buttons at the bottom
        bottom_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        self.exit_button = TexturedButton(text='Exit', height=65, size_hint=(None, 1), width=350, font_size='20sp', bold=True)
        self.exit_button.bind(on_press=self.on_exit_button_pressed)
        bottom_layout.add_widget(self.exit_button)

        self.speak_button = TexturedButton(text='Speak', height=65, size_hint=(None, 1), width=350, font_size='20sp', bold=True)
        self.speak_button.bind(on_press=self.on_speak_button_pressed)
        bottom_layout.add_widget(self.speak_button)

        self.layout.add_widget(bottom_layout)

        # Set the window size to 600x450 and make it not resizable
        Window.size = (600, 450)
        Window.resizable = False

        return self.layout

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width - 20, None)

    def on_search_button_pressed(self, instance):
        card_name = self.card_name_input.text
        self.card_name_input.text = ''  # Clear the search bar
        card_data = search_card(card_name)
        if card_data:
            original_text = card_data['oracle_text']
            opposites = load_opposites('opposites.json')
            opposite_text = opposite_mechanic(original_text, opposites)
            result_text = (
                f"[b]Original Card Text:[/b]\n{original_text}\n\n"
                f"[b]Opposite Card Text:[/b]\n{opposite_text}"
            )
            self.result_label.text = result_text
            self.opposite_text = opposite_text  # Save the opposite text for speaking
        else:
            self.result_label.text = "[b]Card not found. Please check the card name and try again.[/b]"
            self.opposite_text = None  # Clear the opposite text

    def on_exit_button_pressed(self, instance):
        App.get_running_app().stop()
        Window.close()

    def on_speak_button_pressed(self, instance):
        if hasattr(self, 'opposite_text') and self.opposite_text:
            speak_text(self.opposite_text)
        else:
            random_phrases = [
                "No card found. Please Try again",
                "Red deck wins",
                "Ban Jace",
                "Topdecked",
                "Strictly better",
                "Counterspell everything",
                "Dies to removal",
                "Draw, land, pass"
            ]
            speak_text(random.choice(random_phrases))

if __name__ == '__main__':
    EmTeeGeeApp().run()
