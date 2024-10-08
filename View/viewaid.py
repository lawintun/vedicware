from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapSource
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.treeview import TreeView, TreeViewLabel 
from kivy.uix.scrollview import ScrollView
import re
import json
import os
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle


#from kivymd.uix.navigationbar import MDTopAppbar

Builder.load_file("View/kv/view.kv")

class ViewAid(Widget):
    view = ObjectProperty()
    controller = ObjectProperty()
    def __init__(self,view,controller,**kwargs):
        super().__init__(**kwargs)
        self.parent_view = view
        self.parent_controller = controller
        self.VM = self.parent_controller.model.view_model  #ViewModel
        self.parent_view.mapfloat = FloatLayout()
        self.user_loc = self.parent_controller.get_lat_lon()  
        self.width = self.parent_view.width
        self.height = self.parent_view.height 
        self.viewmodel = self.parent_controller.model.view_model
        self.region = "None Selected"
        self.town = "None Selected"
        self.lon = "No data"
        self.lat = "No data"
        self.path = os.path.join(self.parent_controller.model.viewaidpath,"view_loc.json")
        self.loc_data = {
        "Region" : self.region,
        "Town" : self.town,
        "Longitude" : self.lon,
        "Latitude" : self.lat        
        }
        #initialized for show_loc fun
        #defined
        self.popup_show_loc = None
        
                
    def tester(self,txt,*args):
        self.parent_view.label = MDLabel(text=str(txt),pos_hint={"center_x":0.65,"center_y":1}) #y 0.94 , x 0.65
        self.parent_view.labeling = MDLabel(text=str(txt),pos_hint={"center_x":0.65,"center_y":1})
        self.parent_view.labeler = MDLabel(text=str(txt),pos_hint={"center_x":0.65,"center_y":1})
        self.parent_view.boxlayout.add_widget(self.parent_view.label)
        self.parent_view.boxlayout.add_widget(self.parent_view.labeling)
        self.parent_view.boxlayout.add_widget(self.parent_view.labeler)
        
    def select_town(self,instance,*args):
        self.town = instance.text
        id = instance.id
        town_loc = self.viewmodel.get_town_loc()
        for k,v in town_loc.items():
            if id == k:
                v.append("+6.5")
                self.temp = v
                #self.tester(v)   
        #self.tester(id)
        #self.tester(temp)
        self.parent_controller.set_pob(self.temp)
        self.parent_view.label.text = self.parent_controller.get_user_data()
        with open(self.path,"r") as fr:
            data = json.load(fr)
        data["Town"] = self.town
        for key,val in data.items():
            if key == "Region":
                self.region = val
        self.lon = self.temp[0]
        self.lat = self.temp[1]
        update_text = f"Region : {self.region} \nTownship : {self.town}\nLongitude :{self.lon}\nLatitude : {self.lat}"
        p=0
        for wg in self.popup_show_loc.content.children:
            if p == 2:
                wg.text = update_text
            p+=1
        if isinstance(id, str):
            return True
        else:
            return False
        
        
    def select_region(self,instance,*args):
            #self.tester(instance.id)
            #self.tester(instance.text)
            self.region = instance.text
            update_text = f"Region : {self.region} \nTownship : {self.town}\nLongitude :{self.lon}\nLatitude : {self.lat}"
            self.loc_data["Region"] = self.region
            with open(self.path,"w") as file:
                json.dump(self.loc_data,file,indent=4)
            p = 0
            for wg in self.popup_show_loc.content.children:
                if p == 2:
                    #self.tester(wg)
                    wg.text = update_text
                p+=1
                
            id = instance.id 
            region_town = self.parent_controller.model.view_model.get_region_town()
            town_name = self.parent_controller.model.view_model.get_town_name()
            temp = {}
            for k,v in region_town.items():
                if id == k:
                       for town_no in v:
                          for i,j in town_name.items():
                              if i == town_no:
                                  temp[i] = j
            path = "/storage/emulated/0/Kivy02/vedicware/View/test.json"
            
            n = 1
            self.grid_scroll_loc = GridLayout(cols=1,size_hint_y=None)
            self.grid_scroll_loc.bind(minimum_height=self.grid_scroll_loc.setter('height'))
            self.grid_scroll_loc.spacing=[10,10]
            o = 0
            for wg in self.popup_show_loc.content.children:
                    if o == 1:
                        wg.clear_widgets()
                    o+=1
        
            for key,val in temp.items():
                    btn = Button(
                    text=val,
                    size=(600,100),
                    size_hint=(None,None),
                    halign = "left",
                    valign = "middle",
                    background_color = (27/255,133/255,1,7),
                    on_release = self.select_town
                    )
                    self.grid_scroll_loc.rows = n
                    btn.id=key
                    self.grid_scroll_loc.add_widget(btn)
                    n+=1 
            u = 0        
            for wg in self.popup_show_loc.content.children:
                    if u == 1:
                        wg.add_widget(self.grid_scroll_loc)
                    u+=1
                
            
            
    def confirm_show_loc(self,instance,*args):
        if self.popup_show_loc:
            self.popup_show_loc.dismiss()
        self.popup_show_loc = None
        self.parent_view.popup_set_pob.dismiss()
        self.parent_view.popup_set_pob = None
            
    def cancel_show_loc(self,instance,*args):
        self.popup_show_loc.dismiss()
        self.popup_show_loc = None
        
    def show_loc(self,*args):
        self.parent_view.box_loc = BoxLayout(orientation = "vertical") #box declare        
        self.parent_view.show_loc_label_text = f"Region : {self.region} \nTownship : {self.town}\nLongitude :{self.lon}\nLatitude : {self.lat}"
        self.parent_view.show_loc_label = MDLabel(
        text=self.parent_view.show_loc_label_text,
        size_hint=(None,None),
        size=(800,250),
        theme_text_color = "Custom",
        text_color =(1,1,1,1)
        )
        
        self.parent_view.scroll_loc = ScrollView(
        size_hint=(1,None),
        size=(700,700),
        width = 500
        )#scroll declare
        
        self.parent_view.grid_scroll_loc = GridLayout(cols=1,size_hint_y=None)
        self.parent_view.grid_scroll_loc.bind(minimum_height=self.parent_view.grid_scroll_loc.setter('height'))
        self.parent_view.grid_scroll_loc.spacing=[10,10]
        
        i = 1
        region_name = self.parent_view.model.view_model.get_region_name()
        for k,v in region_name.items():
            self.v = Button(
            text=v,
            size=(600,100),
            size_hint=(None,None),
            halign = "left",
            valign = "middle",
            background_color = (27/255,133/255,1,7),
            on_release = self.select_region
            )
            self.parent_view.grid_scroll_loc.rows = i
            self.v.id=k
            self.parent_view.grid_scroll_loc.add_widget(self.v)
            i+=1                        
        
        self.parent_view.show_loc_cancel = MDRectangleFlatButton(
        text="ေနာက်သို ့",
        font_name = self.parent_view.font_loc,
        on_release = self.cancel_show_loc
        )
        self.parent_view.show_loc_confirm = MDRectangleFlatButton(
        text = "ပိတ်သိမ်းမည်",
        font_name = self.parent_view.font_loc,
        on_release = self.confirm_show_loc,
        text_color=(1,1,1,1)
        )
        #self.tester(name)
        
        self.parent_view.grid_loc = GridLayout(cols=3,rows=1) #grid declare
        self.parent_view.grid_loc.spacing=[10,10]
        self.parent_view.grid_loc.padding=[0,20]
        
        #adding widget
        self.parent_view.box_loc.add_widget(self.parent_view.show_loc_label)
        self.parent_view.scroll_loc.add_widget(self.parent_view.grid_scroll_loc)
        self.parent_view.box_loc.add_widget(self.parent_view.scroll_loc)
        self.parent_view.grid_loc.add_widget(self.parent_view.show_loc_confirm)
        self.parent_view.grid_loc.add_widget(self.parent_view.show_loc_cancel)
        self.parent_view.box_loc.add_widget(self.parent_view.grid_loc)
                          
                                      
        self.popup_show_loc = Popup(
        title="ေမွးရပ် ေဒသ ေရွးချယ်ပါ",
        size_hint = (0.9,0.65),
        content = self.parent_view.box_loc,
        auto_dismiss = False,
        title_font = self.parent_view.font_loc,
        background_color=(27/255,133/255,1,7)
        )
        self.popup_show_loc.open()
        
        
        
        
        
    def map_open(self,*args):
        self.zoom = 3
        pattern = r'([-+]?\d*\.\d+|\d+)\u00b0([NSWE])'
        match_lat = re.findall(pattern,self.user_loc[1])
        match_lon = re.findall(pattern,self.user_loc[0])
        if match_lat:
            float_lat,lat_dir_sign= match_lat[0]
            self.lat = float(float_lat)
            if lat_dir_sign == "S":
                self.lat *=-1
        if match_lon:
            float_lon,lon_dir_sign = match_lat[0]
            self.lon = float(float_lon)
            if lon_dir_sign == "W":
                self.lon *=-1 
        #self.tester(self.lat)
            
        self.mapview = MapView(lat=self.lat,lon=self.lon,zoom=self.zoom)
        self.mapview.map_source = MapSource(
            url="https://mts1.googleapis.com/vt?lyrs=m@189&src=apiv3&x={x}&y={y}&z={z}&hl=en-US",
            attribution="Google Maps",
        )
        self.parent_view.mapgrid = GridLayout(cols=1,rows=2,size=(self.parent_view.width*3,self.parent_view.height*2),size_hint=(1,1),padding=2,spacing=[10,10])
        self.parent_view.mapbtn = MDRectangleFlatButton(text="ပိတ်သိမ်းမည်", font_name=self.parent_view.font_loc, on_release=self.parent_view.close_map)
        
        self.parent_view.mapgrid.add_widget(self.mapview)
        self.parent_view.mapgrid.add_widget(self.parent_view.mapbtn)
        self.parent_view.dontknow_pob_box.add_widget(self.parent_view.mapgrid)
        

class ViewBox(Widget):
    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        self.h_factor = 16.5
        self.layout = GridLayout(cols=1,size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.layout.size=(self.width*5,self.height*self.h_factor) #content position size
        self.layout.padding=[20,10]
        self.layout.spacing = [10,10]
        birth_chart_widget = Button(text="Hello", size_hint=(None,None),size=(self.width*10,self.height*10))
        birth_chart_widget2 = Button(text="Hello   ",size_hint=(None,None),size=(self.width*10,self.height*10))
        b3 = Button(text="Hello   ",size_hint=(None,None),size=(self.width*10,self.height*10))
        b4 = Button(text="Hello   ",size_hint=(None,None),size=(self.width*10,self.height*10))
        b5 = Button(text="Hello   ",size_hint=(None,None),size=(self.width*10,self.height*10))
        self.layout.add_widget(birth_chart_widget2)
        self.layout.add_widget(birth_chart_widget)
        self.layout.add_widget(b3)
        self.layout.add_widget(b4)
        self.layout.add_widget(b5)
        self.add_widget(self.layout)    