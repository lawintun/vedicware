import matplotlib.pyplot as plt
import matplotlib.patches as patches
from kivymd.app import MDApp     
from kivy.core.window import Window   
from model import Model,VedicModel,VimshottariModel

class ComApp(MDApp):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.model = Model()
        self.vedicmodel = VedicModel(self.model)
        self.dosha = VimshottariModel(self.model)
        date = [7,10,1952]
        time = [9,30,0]
        moon = 39.71
        #data = self.dosha.dosha_entry(date,time,moon)
        #score = self.dosha.dosha_effect(data[0],data[1])
        #self.dosha.dosha_graph(score,data[2],data[3])  
    def build(self):                
        Window.size = (1100, 2100) 
        Window.clearcolor = (1, 1, 1, 1)  
        Window.rotation = 0
        return 0

if __name__ == "__main__":
    ComApp().run()
