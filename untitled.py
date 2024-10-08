from kivy.app import App
from kivy.uix.button import Button
from kivy.metrics import dp

class MyApp(App):
    def build(self):
        # Create a button with a size of 100 dp x 50 dp
        button = Button(text='Click Me', size_hint=(None, None),
                        size=(dp(100), dp(50)))

        return button

if __name__ == '__main__':
    MyApp().run()
