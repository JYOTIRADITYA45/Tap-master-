from kivy.app import App
from kivy.uix.button import Button

class TapApp(App):
    def build(self):
        return Button(text="Tap Master Ready!")

if __name__ == "__main__":
    TapApp().run()
