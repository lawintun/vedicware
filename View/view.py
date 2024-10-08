from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
import json
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os
from kivymd.color_definitions import colors
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from kivymd.uix.datatables import MDDataTable 
from kivy.metrics import dp
from kivy.lang import Builder

from kivy_garden.mapview import MapView
from View.viewaid import ViewAid,ViewBox
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.carousel import Carousel
from kivy.core.text import LabelBase

#from jnius import autoclass
#from android.permissions import request_permissions, Permission

Builder.load_file("View/kv/view.kv")  
global source_img_logo 
global source_img_welcome
source_img_logo = "View/src/logo.jpg"
source_img_welcome = "View/src/welcome.jpg"

class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(MyScrollView, self).__init__(**kwargs)
        layout = GridLayout(cols=1, rows=3, size_hint_y=None)
        layout.spacing = [20, 20]
        layout.padding = [10, 10]
        layout.bind(minimum_height=layout.setter('height'))
        #self.bind(size=self.adjust_canvas_size)

        for _ in range(3):
            canvas_widget = CanvasWidget()
            layout.add_widget(canvas_widget)

        self.add_widget(layout)

class ViewNav(Widget):
    def __init__(self,view,controller,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.View = view
        self.Controller = controller
        calc_button = ObjectProperty(None)
        analytic_button = ObjectProperty(None)
        interpret_button = ObjectProperty(None)
        
        
class InterpretScreen(MDScreen):
    def __init__(self,view,controller,*args,**kwargs):
        super(InterpretScreen,self).__init__(*args,**kwargs)
        self.scrollheight = 1800
        self.scrollcellwidth = 1065
        self.View = view
        self.Controller = controller
        self.name = "Interpretation"
        self.viewnav = ViewNav(view=self,controller=self.Controller)
        self.boxlayout = BoxLayout(orientation="vertical")
        self.scrollview = ScrollView(
         size_hint=(1,None),
         size = (100,self.scrollheight),
         width = 80
        )#scroll declare
        self.gridscroll = GridLayout(
         cols=1,size_hint_y=None
        )#Grid inner scroll
        
        self.gridscroll.bind(minimum_height=self.gridscroll.setter('height'))
        self.gridscroll.spacing=[10,10]
        self.gridscroll.padding=[10,2]
        
        i = 1
        for v in range(100):
            self.btn = Button(
            #size=(self.width*11,self.height*8),
            size=(self.scrollcellwidth,self.scrollheight-10),
            size_hint=(None,None),
            text = "",
            halign = "center",
            valign = "middle",
            background_color = (0,0,0,0),
            disabled = True
            )
            self.gridscroll.rows = i
            self.btn.id= str(i)
            if i < 101:
                self.gridscroll.add_widget(self.btn)
            i+=1
        
        intro = self.View.model.view_model.introduction()[0]
        io = Image(source=intro,size=(self.scrollcellwidth,self.scrollheight),size_hint=(None,None),pos=(10,self.scrollheight*9.3))
        self.gridscroll.children[0].add_widget(io)
        self.scrollview.add_widget(self.gridscroll)
        self.boxlayout.add_widget(self.scrollview)
        self.boxlayout.add_widget(self.viewnav)
        self.add_widget(self.boxlayout)
        #self.Controller.reset_button()

class AnalyticScreen(MDScreen):
    def __init__(self,view,controller,*args,**kwargs):
        super(AnalyticScreen,self).__init__(*args,**kwargs)
        self.scrollheight = 1800
        self.scrollcellwidth = 1065
        self.View = view
        self.Controller = controller
        self.name = "Analytic"
        self.boxlayout = BoxLayout(orientation="vertical")
        self.viewnav = ViewNav(view=self,controller=self.Controller)
        self.scrollview = ScrollView(
         size_hint=(1,None),
         size = (100,self.scrollheight),
         width = 80
        )#scroll declare
        self.gridscroll = GridLayout(
         cols=1,size_hint_y=None
        )#Grid inner scroll
        
        self.gridscroll.bind(minimum_height=self.gridscroll.setter('height'))
        self.gridscroll.spacing=[10,10]
        self.gridscroll.padding=[10,2]
        i = 1
        for v in range(10):
            self.btn = Button(
            #size=(self.width*11,self.height*8),
            size=(self.scrollcellwidth,self.scrollheight-10),
            size_hint=(None,None),
            text = "",
            halign = "center",
            valign = "middle",
            background_color = (0,0,0,0),
            disabled = True
            )
            self.gridscroll.rows = i
            self.btn.id= str(i)
            if i < 11:
                self.gridscroll.add_widget(self.btn)
            i+=1
        
        
        
        vision = self.View.model.view_model.vision()
        vo = Image(source=vision,size=(self.scrollcellwidth,self.scrollheight),size_hint=(None,None),pos=(10,self.scrollheight*9.1))
        self.gridscroll.children[0].add_widget(vo)
        self.scrollview.add_widget(self.gridscroll)
        self.boxlayout.add_widget(self.scrollview)
        self.boxlayout.add_widget(self.viewnav)
        self.add_widget(self.boxlayout)
    

#View




class View(MDScreen):
    controller = ObjectProperty()
    model = ObjectProperty()
    ViewAid = ObjectProperty()
    def __init__(self,controller,model,**kwargs):
         super().__init__(**kwargs)
         self.name = "View"
         self.source_img_welcome = source_img_logo
         self.source_image_logo = "View/src/logo.jpg"
         self.font_loc = "View/fonts/NotoSansMyanmar-Regular.ttf"
         self.font_thin_loc = "View/fonts/NotoSerifMyanmar-Thin.ttf"
         LabelBase.register(name='Myanmar', fn_regular='View/fonts/NotoSansMyanmar-Regular.ttf')
         self.model = model
         self.controller = controller
         self.model = model         
         self.gridlayout = GridLayout()
         self.boxlayout = BoxLayout(orientation="vertical")
         
         #test start #ချိန်ညှိရန် 
         self.scrollview = ScrollView(
         size_hint=(1,None),
         size=(self.width*16.2,self.height*9),
         width = self.width*8,
        )#scroll declare
         self.gridscroll = GridLayout(
         cols=1,size_hint_y=None
        )#Grid inner scroll
        
         self.gridscroll.bind(minimum_height=self.gridscroll.setter('height'))
         self.gridscroll.spacing=[10,10]
         self.gridscroll.padding=[10,2]
         
         self.viewaid = ViewAid(view=self,controller=self.controller) #view aid class
         #self.viewbox = ViewBox() #view box class
         self.viewnav = ViewNav(view=self,controller=self.controller)
         #testing Starts
         self.inter = InterpretScreen(view=self,controller=self.controller)
         self.ana = AnalyticScreen(view=self,controller=self.controller)
         
         self.navlayout = BoxLayout(orientation="vertical")         
         #testing End         
         #grid deco
         self.gridlayout.cols = 2
         self.gridlayout.rows = 10
         #User Data Dashboard
         self.gridlayout.size = (self.width*40,self.height*3.5) # for user data height*21 , width*40         
         self.gridlayout.size_hint=(None,None)
         self.gridlayout.spacing=[0,0]
         self.gridlayout.padding=[50,0]
    
         self.fixed_img = Image(source=self.source_img_welcome, size_hint=(None, None), size=(self.width*4, self.height*2.6),pos_hint={"center_x":.08,"center_y":.85})
         self.fixed_button = Button(text="", size_hint=(None,None),size=(self.width,250),disabled=True,background_color=(1,1,1,1))
         self.fixed_button.background_color=(0,0,0,0)
         
         self.user_data = self.controller.get_user_data()
         if self.user_data:
              pass
         else:
          self.user_data = "No Data"
          #"\nName: Ma May Pyae Sone Aung \nTOB: 09:09:00AM\nDOB: 9/5/1996\nPOB_lon: 96.0880556°E\nPOB_lat: 21.9772222°N\nTime Offset: UTC+6.5"
         
         self.label = MDLabel(text=self.user_data   ,size_hint=(None,None),size=(self.width*20,self.height*3))
         self.label.theme_text_color="Custom"
         self.label.text_color =( 27/255,133/255,1,0.7)      
            
         self.gridlayout.add_widget(self.fixed_img)
         self.gridlayout.add_widget(self.label)      
         self.boxlayout.add_widget(self.gridlayout)
         self.button_group()         
         self.boxlayout.add_widget(self.grid_button)
         #self.boxlayout.add_widget(self.fixed_button) 
         self.boxlayout.add_widget(self.grid_button2)
         self.zata_background()
         self.scrollview.add_widget(self.gridscroll)
         self.chart_ui()
         self.boxlayout.add_widget(self.scrollview)
                 
         self.boxlayout.add_widget(self.viewnav)
         self.add_widget(self.boxlayout)
#======Obj Properties Attributes End======    #======To Handle Action and Condi =====     

    def zata_background(self,*args,**kwargs):
         i = 1
         region_name = ["ရာသီ","ဘာဝ", "နဝင်း"]
         for v in region_name:
            self.v = Button(
            text=v,
            size=(self.width*11,self.height*9),
            size_hint=(None,None),
            halign = "center",
            valign = "middle",
            background_color = (0,0,0,0),
            disabled = True,
            font_name = self.font_loc
            )
            self.gridscroll.rows = i
            self.v.id= str(i)
            self.v.theme_color = "Custom"
            self.v.color = ( 27/255,133/255,1,0.7)
            if i < 4:
                self.gridscroll.add_widget(self.v)
            i+=1
            self.zata_design()
    def zata_design(self,*args,**kwargs):
         j = 0         
         for wg in self.gridscroll.children:
            zata = Widget()
            with zata.canvas.after:
                Color(27/255,133/255,1,0.7)
                Line(points=[self.width*4.3,self.height+(j*880),self.width*4.3,self.height+830+(j*880)], width=2)
                Line(points=[self.width*6.5,self.height+0.5+(j*880),self.width*6.5,self.height+830+(j*880)], width=2)
                Line(points=[self.width*1,self.height+0+(j*880),self.width*1,self.height+845+(j*880)],width=2)
                Line(points=[self.width*10,self.height+0+(j*880),self.width*10,self.height+845+(j*880)],width=2)
                #horizon line
                Line(points=[self.width*1,self.height*4+(j*880),self.width*10,self.height*4+(j*880)], width=2)
                Line(points=[self.width*1,self.height*6.2+(j*880),self.width*10,self.height*6.2+(j*880)], width=2)
                Line(points=[self.width*1,self.height*9.5+(j*880),self.width*10,self.height*9.5+(j*880)],width=2)
                Line(points=[self.width*1,self.height*1+(j*880),self.width*10,self.height*1+(j*880)],width=2)
                
                #45deg right bottom
                Line(points=[self.width*1,self.height*1+(j*880),self.width*4.3,self.height+297+(j*880)], width=2)
                #45deg right upper
                Line(points=[self.width*1,self.height+830+(j*880),self.width*4.3,self.height+523+(j*880)], width=2)
                #45deg left bottom
                Line(points=[self.width*10,self.height*1+(j*880),self.width*6.5,self.height+297+(j*880)], width=2)
                #45deg left upper
                Line(points=[self.width*10,self.height+830+(j*880),self.width*6.5,self.height+523+(j*880)], width=2)
                wg.add_widget(zata)                            
                j+=1 

    def chart_ui(self,*args,**kwargs):
        data = self.model.get_lagna()
        self.Rasi_chart_generator(data[0])   
        self.Bhava_chart_generator(data[1])    
        self.Navam_chart_generator(data[2])    
        
            
    def Rasi_chart_generator(self,Rasi,*args,**kwargs):
             index = 0 #0Rasi, 1Bhava, 2Navam
             self.chart_generator(index,Rasi)     
              
    def Bhava_chart_generator(self,Bhava,*args,**kwargs):
            index = 1
            self.chart_generator(index,Bhava)

    def Navam_chart_generator(self,Navam,*args,**kwargs):
            index = 2
            self.chart_generator(index,Navam)
            
    def chart_generator(self,index,Rasi,*args,**kwargs):
         count = [1,2,3,4,5,6,7,8]
         chartlist = [0,880,1760]
         chart = chartlist[index] 
         for r in Rasi:
             R = Rasi[r]
             for c in count:
                  self.chart_cell_filler(c,chart,R,r)
                  
        
    def chart_cell_filler(self,c,chart,R,r,*args,**kwargs):            
             tester = []
             n = len(R) 
             if n == c:
                 j = 0
                 for p,i in zip(R,range(n)):
                     if r == "1":
                         hfactor = 3*780
                         wfactor = 5.3
                         if i == 3:
                             hfactor = 3*750
                             wfactor = 4.8
                         if i == 4:
                             hfactor = 3*700
                             wfactor = 4.7
                         if i == 5:
                             hfactor = 3*640
                             wfactor = 4.7
                         if i == 6:
                             hfactor = 3*630
                             wfactor = 5.8
                         if i == 7:
                             hfactor = 3*640
                             wfactor = 5.8
                     if r == "2":
                         hfactor = 3*780
                         wfactor = 3.8
                         if i == 3:
                             hfactor = 3*750
                             wfactor = 3.3
                         if i == 4:
                             hfactor = 3*700
                             wfactor = 3.2
                         if i == 5:
                             hfactor = 3*680
                             wfactor = 2.8
                         if i == 6:
                             hfactor = 3*670
                             wfactor = 2.4
                         if i == 7:
                              hfactor = 3*650
                              wfactor = 2
                     if r == "3":
                         hfactor = 3*760
                         wfactor = 1.1
                         if i == 3:
                             hfactor = 3*710
                             wfactor = 1.7
                         if i == 4:
                             hfactor = 3*655
                             wfactor = 1.7
                         if i == 5:
                             hfactor = 3*630
                             wfactor = 2.6
                         if i == 6:
                             hfactor = 3*620
                             wfactor = 2.3
                         if i == 7:
                             hfactor = 3*570
                             wfactor = 2.9
                     if r == "4":
                         hfactor = 3*695
                         wfactor = 1.3
                         if i == 2:
                             hfactor = 3*640
                             wfactor = 2.1
                         if i == 3:
                             hfactor = 3*640
                             wfactor = 2.1
                         if i == 4:
                             hfactor = 3*600
                             wfactor = 2.8
                         if i == 5:
                             hfactor = 3*590
                             wfactor = 3.6
                         if i == 6:
                             hfactor = 3*527
                             wfactor = 3.5
                         if i == 7:
                             hfactor = 3*530
                             wfactor = 3.2
                     if r == "5":
                         hfactor = 3*600
                         wfactor = 1.1
                         if i == 3:
                             hfactor = 3*570
                             wfactor = 1.7
                         if i == 4:
                             hfactor = 3*510
                             wfactor = 1.7
                         if i == 5:
                             hfactor = 3*500
                             wfactor = 2.2
                         if i == 6:
                             hfactor = 3*490
                             wfactor = 2.4
                         if i == 7:
                             hfactor = 3*470
                             wfactor = 2.8
                     if r == "6":
                         hfactor = 3*590
                         wfactor = 3.8
                         if i == 3:
                             hfactor = 3*540
                             wfactor = 3.2
                         if i == 4:
                             hfactor = 3*480
                             wfactor = 3.2
                         if i == 5:
                             hfactor = 3*470
                             wfactor = 2.9
                         if i == 6:
                             hfactor = 3*430
                             wfactor = 2.4
                         if i == 7:
                             hfactor = 3*397
                             wfactor = 2
                     if r == "7":
                         hfactor = 3*598
                         wfactor = 5.3
                         if i == 3:
                             hfactor = 3*570
                             wfactor = 4.7
                         if i == 4:
                             hfactor = 3*520
                             wfactor = 4.7
                         if i == 5:
                             hfactor = 3*460
                             wfactor = 4.7
                         if i == 6:
                             hfactor = 3*450
                             wfactor = 5.8
                         if i == 7:
                             hfactor = 3*450
                             wfactor = 5.8
                     if r == "8":
                         hfactor = 3*590
                         wfactor = 6.8
                         if i == 3:
                             hfactor = 3*540
                             wfactor = 7.3
                         if i == 4:
                             hfactor = 3*480
                             wfactor = 7.3
                         if i == 5:
                             hfactor = 3*470
                             wfactor = 7.8
                         if i == 6:
                             hfactor = 3*425
                             wfactor = 8.1
                         if i == 7:
                             hfactor = 3*400
                             wfactor = 8.5
                     if r == "9":
                         hfactor = 3*600
                         wfactor = 9.6
                         if i == 3:
                             hfactor = 3*570
                             wfactor = 9.1
                         if i == 4:
                             hfactor = 3*518
                             wfactor = 9.1
                         if i == 5:
                             hfactor = 3*495
                             wfactor = 8.4
                         if i == 6:
                             hfactor = 3*489
                             wfactor = 8.6
                         if i == 7:
                             hfactor = 3*465
                             wfactor = 7.7
                     if r == "10":
                         hfactor = 3*690
                         wfactor = 9.2
                         if i == 2:
                             hfactor = 3*670
                             wfactor = 8.6
                         if i == 3:
                             hfactor = 3*610
                             wfactor = 8.6
                         if i == 4:
                              hfactor = 3*580
                              wfactor = 8
                         if i == 5:
                              hfactor = 3*590
                              wfactor = 8
                         if i == 6:
                             hfactor = 3*560
                             wfactor = 7.5
                         if i == 7:
                             hfactor = 3*520
                             wfactor = 7
                     if r == "11":
                         hfactor = 3*760
                         wfactor = 9.6
                         if i == 3:
                             hfactor = 3*720
                             wfactor = 9
                         if i == 4:
                             hfactor = 3*660
                             wfactor = 9
                         if i == 5:
                             hfactor = 3*640
                             wfactor = 8.5
                         if i == 6:
                             hfactor = 3*610
                             wfactor = 8
                         if i == 7:
                             hfactor = 3*570
                             wfactor = 7.5
                     if r == "12":
                         hfactor = 3*780
                         wfactor = 6.7
                         if i == 3:
                             hfactor = 3*740
                             wfactor = 7.2
                         if i == 4:
                             hfactor = 3*680
                             wfactor = 7.2
                         if i == 5:
                             hfactor = 3*680
                             wfactor = 7.8
                         if i == 6:
                             hfactor = 3*680
                             wfactor = 8
                         if i == 7:
                             hfactor = 3*640
                             wfactor = 8.4
                     self.P1 = MDLabel(text=p,pos=(self.width*wfactor,(self.height+hfactor+(i*80))-chart))
                     
                     self.gridscroll.children[0].children[0].add_widget(self.P1)
             #return tester 
             
    def cancel_set_name(self,*args):
            self.popup_set_name.dismiss()
            self.popup_set_name = None
            
    def confirm_set_name(self,*args):
            name = self.box.textfield.text
            self.controller.set_name(name) 
            self.user_data = self.controller.get_user_data() 
            self.label.text = self.user_data
            self.popup_set_name.dismiss()
            self.popup_set_name = None    
         
     
    def save_time(self,*args):
        time = self.time_dialouge.time
        self.controller.set_time(time)
        self.user_data = self.controller.get_user_data()
        self.label.text = self.user_data
        #self.viewaid.tester(get_list)
        
    def cancel_time(self,*args):
        pass 
            
    def save_date(self,instance,date,*args):
        self.controller.set_date(date)
        self.user_data = self.controller.get_user_data()
        self.label.text = self.user_data
        #self.viewaid.tester()
        
    def cancel_date(self,*args):
        pass       
    def close_map(self,*args):
        self.popup_dontknow_pob.dismiss()
        self.popup_dontknow_pob = None
   
    def select_town(self,list,*args):
             self.controller.set_pob(list)
             self.user_data = self.controller.get_user_data()
             
    def confirm_set_pob(self,instance,*args):
        lon = self.box.longfield.text 
        lat = self.box.latfield.text
        utc = self.box.utcfield.text
        poblist = [lon,lat,utc]
        self.controller.set_pob(poblist)
        self.user_data = self.controller.get_user_data()
        self.label.text = self.user_data
        #self.viewaid.tester("")
        self.popup_set_pob.dismiss()
        self.popup_set_pob = None
        
    def cancel_set_pob(self,*args):
        self.popup_set_pob.dismiss()
        self.popup_set_pob = None
     
             
    def confirm_chart_gen(self,*args):         
         if self.popup_chart_gen:
             self.controller.reset() 
             self.controller.resetana()
             self.controller.resetinter()
             self.popup_chart_gen.dismiss()
             self.popup_chart_gen = None
                    
                    
                    
                    
    def cancel_chart_gen(self,*args):
                    self.popup_chart_gen.dismiss()
                    self.popup_chart_gen = None
                    
                                                                                                           
 #========End of Handling action & condi                                                                                            
#=======Extended UI ==================         
     
    def anima_(self,*args):
         ani = Animation(size=(self.width,self.height))
         ani += Animation(size=(self.width*2.7,self.height*2.7), transition="in_circ")
         ani.start(self.image)
   
    def show_loc(self,*args):
        return self.viewaid.show_loc()
                   
    def  show_time(self,*args):
        self.time_dialouge = MDTimePicker()
        self.time_dialouge.bind(on_save = self.save_time, on_cancel=self.cancel_time)
        self.time_dialouge.open()
        
    def show_date(self,*args):
        self.date_dialouge = MDDatePicker()
        self.date_dialouge.bind(on_save=self.save_date,on_cancel=self.cancel_date)
        self.date_dialouge.open()
        
        
        
#========Extended UI End==============
#========Fixed UI start ==========             
                  
    def button_group(self,*args):
        #self.font_loc = "fonts/NotoSansMyanmar-Regular.ttf"
        self.name_button = MDRectangleFlatButton(text="အမည်", halign="center",pos_hint={"center_x": .2, "center_y": .77},on_release = self.set_name,font_name=self.font_loc)
        self.tob_button = MDRectangleFlatButton(text="ေမွးချိန်", halign="center",pos_hint={"center_x": .4, "center_y": .77},on_release = self.show_time,font_name=self.font_loc)
        self.dob_button = MDRectangleFlatButton(text="ေမွးေန့ ", halign="center",pos_hint={"center_x": .6, "center_y": .77}, on_release = self.show_date,font_name=self.font_loc)
        self.pob_button = MDRectangleFlatButton(text="ေမွးရပ်",halign="center",pos_hint={"center_x": .8, "center_y": .77},on_release = self.set_pob,font_name=self.font_loc)
        self.chart_gen_button= MDRectangleFlatButton(text="ေဟာကိန်းေပးပါ",halign="center",pos_hint={"center_x": .246,"center_y": .70},on_release = self.chart_gen,font_name=self.font_loc)
        self.chart_gen_button.theme_text_color="Custom"
        self.chart_gen_button.md_bg_color=( 27/255,133/255,1,0.7)
        self.chart_gen_button.text_color=(1,1,1,1)
        
        self.dontknow_pob_button= MDRectangleFlatButton(text="​ေြမပံု",halign="center",pos_hint={"center_x": .479,"center_y": .70},on_release = self.dontknow_pob,font_name=self.font_loc)
        self.dontknow_pob_button.theme_text_color="Custom"
        self.dontknow_pob_button.md_bg_color=( 27/255,133/255,1,0.7)
        self.dontknow_pob_button.text_color=(1,1,1,1)
        #show loc 
        self.dontknow_tob_button= MDRectangleFlatButton(text= "  ေမွးချိန်မသိပါ ", halign="center",pos_hint={"center_x": .73,"center_y": .70},on_release = self.dontknow_pob,font_name=self.font_loc)
        self.dontknow_tob_button.theme_text_color="Custom"
        self.dontknow_tob_button.md_bg_color=( 27/255,133/255,1,0.7)
        self.dontknow_tob_button.text_color=(1,1,1,1)
        self.grid_button = GridLayout(rows=1,cols=4)
        self.grid_button2 = GridLayout(rows=1,cols=3)
        
        self.grid_button.size=(self.width*65,self.height*1.5)
        self.grid_button2.size=(self.width*40,self.height*1.5) # ချိန်ညှိရန်
        self.grid_button.spacing=[10,10]
        self.grid_button.padding = [100,2]
        self.grid_button.size_hint = (None,None)
        self.grid_button2.spacing=[10,0]
        self.grid_button2.padding=[100,1]
        self.grid_button2.size_hint=(None,None)

        self.grid_button.add_widget(self.name_button)        
        self.grid_button.add_widget(self.dob_button)
        self.grid_button.add_widget(self.tob_button)
        self.grid_button.add_widget(self.pob_button)
        
        #self.boxlayout.add_widget(self.grid_button)
        
        
        self.grid_button2.add_widget(self.chart_gen_button)
        self.grid_button2.add_widget(self.dontknow_pob_button)
        self.grid_button2.add_widget(self.dontknow_tob_button)
        
        #self.boxlayout.add_widget(self.grid_button2)

#============Fixed UI End ===========
#===========Popup UI ================     
                        
    def set_name(self,*args):
        self.box = BoxLayout(orientation="vertical")
        self.box.textfield = MDTextField(hint_text="Name in English", multiline=False)
        self.box.add_widget(self.box.textfield)  
        self.layout = GridLayout(cols=2,rows=1) 
        self.layout.spacing=[5,5]    
        self.layout.confirm_set_name = MDRectangleFlatButton(text="ေကာင်းြပီ",
        text_color=(1,1,1,1), font_name = self.font_loc,
        size=(self.width*15,self.height*2),
        size_hint=(None,None),
        on_release=self.confirm_set_name
        )
        self.layout.cancel_set_name = MDRectangleFlatButton(text="ပယ်ဖျက်",size_hint=(None,None),on_release=self.cancel_set_name,font_name=self.font_loc)
        
        self.layout.add_widget(self.layout.confirm_set_name)
        self.layout.add_widget(self.layout.cancel_set_name)
        self.box.add_widget(self.layout) 
                
        self.popup_set_name = Popup(
        title="သင့်အမည်ကို ထည့်သွင်းပါ",
        title_font=self.font_loc,
        content=self.box,
        size=(self.width*8,self.height*5),
        size_hint=(0.6,0.25),
        background_color=(27/255,133/255,1,7),
        auto_dismiss=False        
        )
        self.popup_set_name.open()        
    
#Time of Birth pob ======== start        
    def set_pob(self,*args):
        self.box = BoxLayout(orientation="vertical")
        self.box.longfield = MDTextField(
        hint_text="deg°E or deg°W, for Longitude."
        )
        self.box.latfield = MDTextField(
        hint_text="deg°N or deg°S, for Latitude."
        )
        self.box.utcfield = MDTextField(
        hint_text="+Hour or -Hour ,set your country Time Offset."
        )
        self.box.add_widget(self.box.longfield) 
        self.box.add_widget(self.box.latfield) 
        self.box.add_widget(self.box.utcfield)
        self.layout = GridLayout(cols=3,rows=1) 
        self.layout.spacing=[12,15]    
        self.layout.confirm_set_pob = MDRectangleFlatButton(text="ေကာင်းြပီ",font_name=self.font_loc,
        text_color=(0.1,0.8,0.2,1),
        size_hint=(None,None),pos_hint={"center_x":0.4,"center_y":0.5},
        on_release=self.confirm_set_pob
        )
        self.layout.cancel_set_pob = MDRectangleFlatButton(text="ပယ်ဖျက်",size_hint=(None,None),on_release=self.cancel_set_pob,font_name=self.font_loc,text_color=(0.8,0.1,0.1,1))
        self.layout.option_set_pob = MDRectangleFlatButton(text="ေမွးရပ်ေရွးမယ်",size_hint=(None,None),on_release=self.show_loc,font_name=self.font_loc,text_color=(1,1,1,1))
        
        self.layout.add_widget(self.layout.option_set_pob)
        self.layout.add_widget(self.layout.confirm_set_pob)
        self.layout.add_widget(self.layout.cancel_set_pob)
        
        self.box.add_widget(self.layout) 
                
        self.popup_set_pob = Popup(
        title="သင်ေမွးရပ် အချက်အလက်ကို ထည့်သွင်းပါ။",
        content=self.box,
        title_font = self.font_loc,
        #size=(self.width*8,self.height*10),
        size_hint=(0.96,0.4),
        background_color=(27/255,150/255,1,7),
        auto_dismiss=False        
        )
        self.popup_set_pob.open() 
    
#End of Time of Birth pob ===========
#Chart Gen Button func start ==========      
                    
                                         
    def chart_gen(self,*args):
        self.chart_gen_box = BoxLayout(orientation="vertical",size_hint=(0.5,0.98))
        self.chart_gen_grid = GridLayout(cols = 2, rows = 1,size_hint=(0.9,0.1))
        self.chart_gen_grid.spacing=[13,13]
        self.user_data = self.controller.get_user_data()
        self.content_label = MDLabel(text=self.user_data ,size_hint=(0.8,0.3))
        self.content_label.theme_text_color="Custom"
        self.content_label.text_color =( 27/255,133/255,1,0.7)
        
        #confirm - cancel 
        self.chart_gen_grid.confirm_chart_gen= MDRectangleFlatButton(text="ဟုတ်",
        text_color=(1,1,1,1),
        font_name = self.font_loc,
        size=(self.width*14,self.height*15),
        pos_hint = {"center_x": 0.5, "center_y":0.5},
        on_release=self.confirm_chart_gen
        )
        self.chart_gen_grid.cancel_chart_gen= MDRectangleFlatButton(text="ြပန်လည် ြပင်ဆင်မည်",
        font_name = self.font_loc,
        on_release=self.cancel_chart_gen)
        
        #add_widget
        
        self.chart_gen_box.add_widget(self.content_label)
        self.chart_gen_grid.add_widget(self.chart_gen_grid.confirm_chart_gen)
        self.chart_gen_grid.add_widget(self.chart_gen_grid.cancel_chart_gen)
        self.chart_gen_box.add_widget(self.chart_gen_grid)
        
        self.popup_chart_gen  = Popup(
        title="သင့် အချက်အလက်များ ဟုတ်ပါသလား?",
        content=self.chart_gen_box,
        size_hint=(0.85,0.4),
        auto_dismiss = False,
        title_font = self.font_loc
        )   
        self.popup_chart_gen.open()         
        
#End of Chart Gen Popup ==============
#Start of Map Aids for dontknow_pob ===========
 
    def dontknow_tob(self,*args):
        self.dontknow_tob_box = BoxLayout(orientation="vertical",size_hint=(1,1))
    
    def  dontknow_pob(self,*args):
        self.dontknow_pob_box =  BoxLayout(orientation="vertical",size_hint=(1,1))
        self.viewaid.map_open()
        self.popup_dontknow_pob = Popup(
        title="ေြမပံု",
        title_font= self.font_loc,
        content = self.dontknow_pob_box,
        size_hint=(0.8,0.65),
        auto_dismiss = False
        )
        
        self.popup_dontknow_pob.open()

class WelcomeView(MDScreen):
            def __init__(self,controller,*args,**kwargs):
                super().__init__(*args,**kwargs)
                self.con = controller
                self.name = "Welcome"
                self.boxlayout = BoxLayout(orientation="vertical")
                self.floatlayout = FloatLayout()
                #self.floatlayout.size=(self.width*40,self.height*500)
                self.floatlayout.size=(self.width*30,self.height*21)
                
                #self.progress = ProgressBar(max=100)
                self.img = Image(source=source_img_welcome,size=(self.width*0,self.height*0), size_hint=(None,None),pos_hint={"center_x": .5,"center_y":.73})
                #self.boxlayout.add_widget(self.progress)
                self.floatlayout.add_widget(self.img)
                self.boxlayout.add_widget(self.floatlayout)
                self.anima_()
                self.add_widget(self.boxlayout)
                
                #self.progress.value = 0
                #self.progress.animate = True
                # Start loading data or performing 
                Clock.schedule_once(self.load_main_view, 15)  # Load the main view after 10 seconds
            def load_main_view(self, dt):
                    # Load the main view
                    self.con.load_main_view()
                    
            def anima_(self,*args):
                ani = Animation(size=(self.width,self.height))
                ani += Animation(size=(self.width*17,self.height*5), transition="in_circ")
                ani.start(self.img)
#mainView
class MainView(ScreenManager):
    controller = ObjectProperty()
    model = ObjectProperty()
    def __init__(self,controller,model,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.con = controller
        self.mod = model
        self.view = View(controller=self.con,model=self.mod,name="View")        
        self.welcome_view = WelcomeView(controller=self.con,name="Welcome")
        self.add_widget(self.view.inter)
        self.add_widget(self.view.ana)
        self.add_widget(self.welcome_view)
        self.add_widget(self.view)
        self.current = "Welcome"
    def open_view(self,*args,**kwargs):
        self.current = "View"    
    
        
              
        