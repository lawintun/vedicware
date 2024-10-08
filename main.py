from kivymd.app import MDApp     
from kivy.core.window import Window   
from Controller.controller import Controller

class VedicwareApp(MDApp):
    def build(self):
        self.controller = Controller()
        
        Window.size = (1100, 2100) 
        #Window.clearcolor = (1, 1, 1, 1)  
        Window.rotation = 0
        return self.controller.get_screen()

if __name__ == "__main__":
    VedicwareApp().run()
#test = Controller()