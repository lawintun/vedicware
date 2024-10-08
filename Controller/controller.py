from View.view import View,MainView
from Model.model import Model
from View.view import View
from Controller.controlleraid import ControllerAid
from Controller.controlleraid import ControllerAid
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
import re
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.scrollview import ScrollView
import os
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import matplotlib.pyplot as plt
from kivy.cache import Cache

#from jnius import autoclass
#from android.permissions import request_permissions, Permission

from kivy.uix.popup import Popup

class Controller:
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.conaid = ControllerAid()
		self.model = Model()
		self.main_view = MainView(controller=self,model=self.model)							
		self.view = View(controller=self,model=self.model)
		
		#self.main_view = MainView(controller=self,model=self.model)
	
	def select_region(self,instance,*args):
	    self.view.viewaid.popup_show_loc.content.clear_widgets()
	    
        										
	def set_time(self,time,*args):
	    if time:
	        hr = time.hour 
	        hr_str = str(time.hour)
	        min = time.minute
	        min_str = str(time.minute)
	        if hr >= 12:
	            self.day = "PM"
	        else:
	            self.day = "AM"
	        if hr < 10:
	            format_hr = "0" + hr_str
	            self.set_hr = format_hr
	        else:
	            self.set_hr = hr_str
	        if min < 10:
	            format_min = "0" + min_str
	            self.set_min = format_min
	        else:
	            self.set_min = min_str
	        timelist = ["+6.5",self.set_hr,self.set_min,"00",self.day]
	        update_user_data = self.model.set_time(timelist)
	        self.view.label.text = update_user_data
	        return timelist
	    else:
	        return None	    	 					 			 		
	def set_date(self,date,*args):
	    datelist = [date.day,date.month,date.year]
	    update_user_data = self.model.set_date(datelist)
	    self.view.label.text = update_user_data
	    			 		
	def get_screen(self):#get_screen to entry	
	     return self.main_view
	     
	def load_main_view(self):
	    return self.main_view.open_view()
	
    
	       
	def switch_to_analyticscreen(self,*args,**kwargs):
	    if not self.main_view.current == "Analytic":
	     self.main_view.current = "Analytic"
	     self.main_view.view.ana.viewnav.ids.calc_button.md_bg_color = 0,0,0,0
	     self.main_view.view.ana.viewnav.ids.interpret_button.md_bg_color = 0,0,0,0
	     self.main_view.view.ana.viewnav.ids.analytic_button.md_bg_color = 27/255,133/255,1,0.7
	     
	     
	     
	 
	def switch_to_calculationscreen(self,*args,**kwargs):
	       if not self.main_view.current == "View":
	           self.main_view.current = "View"
	           self.main_view.view.viewnav.ids.analytic_button.md_bg_color = 0,0,0,0	           
	           self.main_view.view.viewnav.ids.interpret_button.md_bg_color = 0,0,0,0
	           self.main_view.view.viewnav.ids.calc_button.md_bg_color = 27/255,133/255,1,0.7
	def switch_to_dial(self,*args,**kwargs):
	    path = self.model.view_model.get_inter()
	    astrologer = os.path.join(path,"astrologer.jpg")
	    self.box = BoxLayout(orientation="vertical",size_hint=(1,0.9))
	    self.label = MDLabel(text="Software Support : +959963870503\nName : Ma Moe Pwint Kyi\n\nCustomer Service : +959951180711\nName : Ma Moe Shwe Sin Win\n\nProject Supervisor : +959444011569\nName : Daw Moh Moh Khing \n\nProject Leader :  +959778352457\nName : Mg La Win Tun ",size_hint=(1,1))
	    self.label.theme_text_color="Custom"
	    self.label.text_color =( 27/255,133/255,1,0.7)
	    self.box.add_widget(self.label)
	    self.popup= Popup(title="Contact",content=self.box,size_hint=(0.9,0.4),auto_dismiss=True)
	    self.popup.open()        
    
                
	def switch_to_interpretscreen(self,*args,**kwargs):
	        if not self.main_view.current == "Interpretation":
	           self.main_view.current = "Interpretation"
	           self.main_view.view.inter.viewnav.ids.calc_button.md_bg_color = 0,0,0,0
	           self.main_view.view.inter.viewnav.ids.analytic_button.md_bg_color = 0,0,0,0
	           self.main_view.view.inter.viewnav.ids.interpret_button.md_bg_color = 27/255,133/255,1,0.7    
	def get_sample_lagna(self,*args,**kwargs):
	    return self.model.get_sample_lagna()           
	def get_lagna(self,*args,**kwargs):
	    return self.model.get_lagna()	    
  
	def resetana(self,*args,**kwargs):
	    ana = self.main_view.view.ana
	    ana.gridscroll.children[0].clear_widgets()
	    ganita = self.model.ganita_model
	    viewmodel = self.model.view_model
	    vision = ana.View.model.view_model.vision()
	    v = Image(source=vision,size=(ana.scrollcellwidth,ana.scrollheight),size_hint=(None,None),pos=(10,ana.scrollheight*9.1))
	    ana.gridscroll.children[0].add_widget(v)
	    
	    
	def resetinter(self,*args,**kwargs):
	    inter = self.main_view.view.inter
	    inter.gridscroll.children[0].clear_widgets()
	    ganita = self.model.ganita_model
	    viewmodel = self.model.view_model
	    vedicmodel = self.model.vedic_model
	    
	    posh = inter.scrollheight*99.7
	    intro = inter.View.model.view_model.introduction()[0]
	    io = Image(source=intro,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    ioh = io.texture.height
	    io.pos=(10,posh-ioh)	  
	    inter.gridscroll.children[0].add_widget(io)
	    	    	    	    	    	    	    	    
	    lagna = self.model.view_model.interdb()[0]
	    """lagna = Image(source=lagna,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    lh = lagna.texture.height + ioh + 200
	    lagna.pos=(10,posh-lh)
	    inter.gridscroll.children[0].add_widget(lagna)"""
	    
	    lagnaintro = self.model.view_model.introduction()[1]
	    lagnaintro = Image(source=lagnaintro,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    lih = (lagnaintro.texture.height/1.5)+ioh 
	    lagnaintro.pos=(10,posh-lih)
	    inter.gridscroll.children[0].add_widget(lagnaintro)
	    
	    rasi_purpakatri = viewmodel.interdb()[3]
	    rasi_purpakatri = Image(source=rasi_purpakatri,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    rph = (rasi_purpakatri.texture.height)+lih+400
	    rasi_purpakatri.pos=(10,posh-rph)
	    inter.gridscroll.children[0].add_widget(rasi_purpakatri)
	    
	    bhava_purpakatri = viewmodel.interdb()[4]
	    bhava_purpakatri = Image(source=bhava_purpakatri,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    bph = (bhava_purpakatri.texture.height)+rph
	    bhava_purpakatri.pos=(10,posh-bph)
	    inter.gridscroll.children[0].add_widget(bhava_purpakatri)
	    
	    nav_purpakatri = viewmodel.interdb()[5]
	    nav_purpakatri = Image(source=nav_purpakatri,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    nph = (nav_purpakatri.texture.height)+bph
	    nav_purpakatri.pos=(10,posh-nph)
	    inter.gridscroll.children[0].add_widget(nav_purpakatri)
	    
	    tring = viewmodel.interdb()[6]
	    tring = Image(source=tring,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    th = (tring.texture.height/1.4)+nph - 100
	    tring.pos=(10,posh-th)
	    inter.gridscroll.children[0].add_widget(tring)
	    
	    sthanabala = ganita.Sthanabala()
	    path = viewmodel.get_sthanabala()
	    lord = sthanabala[0][int(sthanabala[1])-1]
	    lordimg = lord+".jpg"
	    lordimg = os.path.join(path,lordimg)
	    lord = Image(source = lordimg,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = th + lord.texture.height + 300
	    lord.pos=(10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(lord)
	    
	    nwdata = ganita.navamlagna()
	    for nwi in nwdata:
	        xi = os.path.join(path,nwi)
	        x = Image(source = xi, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	        self.h = self.h + x.texture.height 
	        x.pos = (10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(x)
	        #example
	    pdata = viewmodel.interdb()
	    paap = [3,4,5]
	    mark = [25] * 3
	    for p,i in zip(paap,range(3)):
	        if "nopurpa" in pdata[p]:
	            mark[i] = (1/12)*100
	        else:
	            mark[i] = 0
	    m = (1/4) * 100
	    if "good" in pdata[6]:
	             m = (1/4) * 100
	             mark.append(m)
	    elif "mixed" in pdata[6]:
	             m = (1/8) * 100
	             mark.append(m)
	    elif "bad" in pdata[6]:
	             m = 0
	             mark.append(m)
	    
	    s = ganita.Sthanabala()
	    navL = ganita.navamlagna()
	    mdict = { "u" : 25,
	    "u+" : 25,
	    "u-" : 25,
	    "m" : 18.75,
	    "o" : 12.5,
	    "f" : 9.375,
	    "nu" : 6.25,
	    "e" : 3.125,
	    "n" : 0,
	    "n+" : 0,
	    "n-" : 0
	        }         
	    mmdict = {
	    "rsu.jpg" : 12.5,
	    "rsm.jpg" : 9.375,
	    "rso.jpg" : 6.25,
	        "rsf.jpg" : 4.6875,
	            "rsnu.jpg" : 3.125,
	                "rse.jpg": 1.5625,
	                "rsn.jpg" : 0,
	    "nwu.jpg": 12.5,
	    "nwm.jpg" : 9.375,
	     "nwo.jpg" : 6.25,
	      "nwf.jpg" : 4.6875,
	        "nwnu.jpg": 3.125,
	            "nwe.jpg": 1.5625,
	                "nwn.jpg" : 0
	    }
	    sb = s[0][int(s[1])-1]
	    mark.append(mdict[sb])
	    
	    if len(navL) < 2:
	        mark.append((1/4)*100)
	    elif len(navL) == 2:
	         mark.append(mmdict[navL[0]])
	         mark.append(mmdict[navL[1]])
	         
	    color = ["lightgreen","Grey"]
	    
	    temp = 0
	    for m in mark:
	        temp += m
	    mark = [temp]
	    self.udaya = temp
	    mark.append(100-temp)
	    sth = "Lagna Strength "  
	    if temp >= 0 and temp <= 20:
	        sth = "Grade E Lagna\n(0% to 20%)"
	        self.grade = "E"
	    if temp > 20 and temp <=40:
	        sth = "Grade D Lagna\n(21% to 40%)"
	        self.grade = "D"
	    if temp > 40 and temp <= 60:
	        sth = "Grade C Lagna\n(41% to 60%)"
	        self.grade = "C"
	    if temp > 60 and temp <= 80:
	        sth = "Grade B Lagna\n(61% to 80%) "
	        self.grade = "B"
	    if temp > 80 and temp <= 100:
	        sth = "Grade A Lagna\n(81% to 100%)"
	        self.grade = "A"
	    plt.figure(figsize=(8, 4)) 
	    label = [sth,""]
	    size = mark
	    fig1, ax1 = plt.subplots()
	    ax1.pie(size,labels=label,colors= color,autopct='%1.1f%%',startangle=90)
	    plt.title("Analysis of Udaya Lagna (Result in Pie Chart)")
	    """plt.text(-1.3, 1, 'Strength ', fontsize=8, color='green')
	    plt.text(-1.3, 0.8, 'Weakness' , fontsize=8, color='#BC002D')"""
	    save_location = viewmodel.get_chartpath()
	    save_location = os.path.join(save_location,"chart.jpg")
	    if os.path.exists(save_location):
	        os.remove(save_location)	    
	    plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	    ch = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    ch.reload()
	    self.h = self.h + ch.texture.height - 500
	    ch.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(ch)
	    Cache.remove("kv.image")
	    #Lagna Nak
	    mainpath = viewmodel.get_inter()
	    Nakshatra = int(ganita.set_lagna()[0]/(360/27))+1
	    nakshatra = "n"+str(Nakshatra)+".jpg"
	    nakshatrapath = os.path.join(mainpath,"nakshatra")
	    nakshatra_path = os.path.join(nakshatrapath,nakshatra)
	    nakshatra_img = Image(source=nakshatra_path,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = self.h + nakshatra_img.texture.height + 450
	    nakshatra_img.pos=(10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(nakshatra_img)
	    #atm
	    pdata = ganita.planetary()[0]
	    exclude = ["8","9"]
	    temp = []
	    for p in pdata:
	        if not p in exclude:
	            temp.append(pdata[p])
	    maxdeg = max(temp)
	    for p,v in pdata.items():
	            if v == maxdeg:
	                atm = str(p)
	                break
	    atm_path = os.path.join(mainpath,p+"atm.jpg")
	    atm_img = Image(source=atm_path,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = self.h + atm_img.texture.height + 50
	    atm_img.pos=(10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(atm_img)
	           
	    #Grade Inter
	    gradeinter = viewmodel.get_inter()
	    g = self.grade + ".jpg"
	    gradepath = os.path.join(gradeinter,g)
	    gradeimg = Image(source = gradepath, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + gradeimg.texture.height - 500
	    gradeimg.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(gradeimg)
	    
	    lag = ganita.set_lagna()[1]
	    lagtext = str(lag)+"i.jpg"
	    mainpath = viewmodel.get_inter()
	    lagpath = os.path.join(mainpath,"lagna")
	    lagpath = os.path.join(lagpath,lagtext)
	    lagimg = Image(source= lagpath, size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = self.h + lagimg.texture.height - 250
	    lagimg.pos=(10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(lagimg)
	   
	    
	    #Cchhanndra
	    chandra = inter.View.model.view_model.introduction()[2]
	    chandra_img = Image(source=chandra,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = self.h + chandra_img.texture.height + 200
	    chandra_img.pos=(10,posh-self.h)	  
	    inter.gridscroll.children[0].add_widget(chandra_img)
	    luner_eclipse = ganita.eclipse()
	    if "len.jpg" in luner_eclipse:
	        luner_eclipse_img = Image( source=luner_eclipse,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + luner_eclipse_img.texture.height+180
	        luner_eclipse_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(luner_eclipse_img)
	        sth = "No Strength "
	        mark =[0,100]
	        self.chandra = 0
	        color = ["lightblue","Grey"]
	        plt.figure(figsize=(8, 4)) 
	        label = [sth,""]
	        size = mark
	        fig1, ax1 = plt.subplots()
	        ax1.pie(size,labels=label,colors= color,autopct='%1.1f%%',startangle=90)
	        plt.title("Analysis of Chandra Lagna  (Result in Pie Chart)")
	        save_location = viewmodel.get_chartpath()
	        save_location = os.path.join(save_location,"AnalyzedChandra.jpg")
	        if os.path.exists(save_location):
	            os.remove(save_location)	    
	        plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	        chandra = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	        chandra.reload()
	        self.h = self.h + chandra.texture.height - 600
	        chandra.pos = (10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(chandra)
	        Cache.remove("kv.image")
	    if not "len.jpg" in luner_eclipse:
	        luner_eclipse_img = Image( source=luner_eclipse,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + luner_eclipse_img.texture.height+180
	        luner_eclipse_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(luner_eclipse_img)
	        planetary = ganita.planet_property("2")
	        pkr,pkb,pkn = planetary[0],planetary[1],planetary[2]
	        getpath = viewmodel.get_inter()
	        
	        if pkr == False:
	           paapr = 25/3
	           pkr = os.path.join(getpath,"norpk.jpg")
	        if pkr == True:
	            paapr = 0
	            pkr = os.path.join(getpath,"rpk.jpg")
	        if pkb == False:
	            paapb = 25/3
	            pkb = os.path.join(getpath,"nobpk.jpg")
	        if pkb == True :
	            paapb = 0
	            pkb = os.path.join(getpath,"bpk.jpg")
	        if pkn == False:
	            paapn = 25/3
	            pkn = os.path.join(getpath,"nonpk.jpg")
	        if pkn == True:
	            paapn = 0
	            pkn = os.path.join(getpath ,"npk.jpg")
	        pkr_img = Image( source=pkr,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + pkr_img.texture.height
	        pkr_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(pkr_img)
	        pkb_img = Image( source=pkb,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + pkb_img.texture.height
	        pkb_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(pkb_img)
	        pkn_img = Image(source=pkn,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + pkn_img.texture.height
	        pkn_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(pkn_img)
	        Bala = { 
	        "u+" : 100,
	        "u" : 100,
	        "u-": 100,
	        "m": 75,
	        "o" : 50,
	        "f" : 37.5,
	        "nu" : 25,
	        "e" : 12.5,
	        "n" : 0,
	        "n-" : 0,
	        "n+" : 0,
	        "vgtm" : 100
	        }
	        bala,nbala = planetary[3],planetary[4]
	        RasiSthanabala = Bala[bala]*0.25
	        NavSthanabala = Bala[nbala]*0.25
	        if nbala != "vgtm":
	            nbala = os.path.join(getpath,nbala+"n.jpg")
	        if nbala == "vgtm":
	            nbala = os.path.join(getpath,"vgtm.jpg")
	        bala = os.path.join(getpath,"r"+bala+".jpg")
	        bala_img = Image(source=bala,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + bala_img.texture.height
	        bala_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(bala_img)
	        nbala_img= Image(source=nbala,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + nbala_img.texture.height
	        nbala_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(nbala_img)
	        Tithi = str(ganita.tithi())
	        Tithi_val = int(Tithi)
	        if Tithi_val == 15:
	            Tithi_val = 0.25
	        if Tithi_val == 30:
	            Tithi_val = 0
	        if Tithi_val < 15:
	            Tithi_val = (((Tithi_val/30)*100)+50)*0.25
	        if Tithi_val > 15 and Tithi_val != 30:
	            Tithi_val = (100-((Tithi_val/30)*100))*0.25
	        Tithi_path = os.path.join(getpath,"tithi")
	        tithi = os.path.join(Tithi_path,Tithi+".jpg")
	        T_img =  Image(source=tithi,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + T_img.texture.height
	        T_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(T_img)
	        
	        sth = "Lagna Strength "  
	        score = paapr+paapn+paapb+RasiSthanabala+NavSthanabala+Tithi_val
	        revscore = 100-score
	        mark =[score,revscore]
	        self.chandra = score
	        color = ["lightblue","Grey"]
	        plt.figure(figsize=(8, 4)) 
	        label = [sth,""]
	        size = mark
	        fig1, ax1 = plt.subplots()
	        ax1.pie(size,labels=label,colors= color,autopct='%1.1f%%',startangle=90)
	        plt.title("Analysis of Chandra Lagna  (Result in Pie Chart)")
	        save_location = viewmodel.get_chartpath()
	        save_location = os.path.join(save_location,"AnalyzedChandra.jpg")
	        if os.path.exists(save_location):
	            os.remove(save_location)	    
	        plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	        chandra = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	        chandra.reload()
	        self.h = self.h + chandra.texture.height - 600
	        chandra.pos = (10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(chandra)
	        Cache.remove("kv.image")
	        Nakshatra = int(ganita.planetary()[0]["2"]/(360/27))+1
	        nakshatra = "n"+str(Nakshatra)+".jpg"
	        nakshatrapath = os.path.join(getpath,"nakshatra")
	        nakshatra_path = os.path.join(nakshatrapath,nakshatra)
	        nakshatra_img = Image(source=nakshatra_path,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + nakshatra_img.texture.height + 450
	        nakshatra_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(nakshatra_img)
	        Nakinter = os.path.join(getpath,"nakshatra")
	        nakinter = os.path.join(Nakinter,str(Nakshatra)+".jpg")
	        nakinter_img = Image(source=nakinter,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        if nakinter_img.texture.height < 1000:
	            self.h = self.h + nakinter_img.texture.height
	        if nakinter_img.texture.height > 1000:
	            self.h = self.h + nakinter_img.texture.height - 500
	        nakinter_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(nakinter_img)
	        #Sara Htira Dwedha
	        rasimoon = None
	        pdata = ganita.planetary()[1]
	        if pdata["2"] in ["1","4","7","10"]:
	            rasimoon = os.path.join(getpath,"14710.jpg")
	        if pdata["2"] in ["2","5","8","11"]:
	            rasimoon = os.path.join(getpath,"25811.jpg")
	        if pdata["2"] in ["3","6","9","12"]:
	            rasimoon = os.path.join(getpath,"36912.jpg")
	        getpath = viewmodel.get_inter()   
	        data = ganita.planetary() 
	        rasideg = data[2]
	        Moon = rasideg["2"]
	        close_fair_farm = None
	        if Moon == 15 or ( Moon >= 10 and Moon <= 20):
	            close_fair_farm = os.path.join(getpath,"rclose.jpg")
	        if (Moon < 10 and Moon > 5) or (Moon > 20 and Moon < 25 ):
	            close_fair_farm = os.path.join(getpath,"rfair.jpg")
	        if Moon == 0 or Moon <= 5 or Moon >= 25:
	            close_fair_farm = os.path.join(getpath,"rfar.jpg")
	        cffm_img = Image(source = close_fair_farm, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	        adder = 500
	        if nakinter_img.texture.height < 1000:
	            adder = 100
	        self.h = self.h + cffm_img.texture.height+adder
	        cffm_img.pos = (10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(cffm_img)
	        #Rasi moon img 
	        rasimoon_img = Image(source=rasimoon,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	        self.h = self.h + rasimoon_img.texture.height - 500
	        rasimoon_img.pos=(10,posh-self.h)
	        inter.gridscroll.children[0].add_widget(rasimoon_img)        
	        
	    #Suriya 
	    Suriya = inter.View.model.view_model.introduction()[3]
	    Suriya_img = Image(source=Suriya,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	    self.h = self.h + Suriya_img.texture.height + 200
	    Suriya_img.pos=(10,posh-self.h)	  
	    inter.gridscroll.children[0].add_widget(Suriya_img)        
	    solar_eclipse = ganita.solareclipse()
	    if "sed.jpg" in solar_eclipse:
	      solar_eclipse_img = Image( source=solar_eclipse,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + solar_eclipse_img.texture.height+180
	      solar_eclipse_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(solar_eclipse_img)
	      sth = "No Strength "
	      self.suriya = 0
	      mark =[0,100]
	      color = ["coral","Grey"]
	      plt.figure(figsize=(8, 4))
	      label = [sth,""]
	      size = mark
	      fig2, ax2 = plt.subplots()
	      ax2.pie(size,labels=label,colors= color,autopct='%1.1f%%',startangle=90)
	      plt.title("Analysis of Suriya Lagna  (Result in Pie Chart)")
	      save_location = viewmodel.get_chartpath()
	      save_location = os.path.join(save_location,"AnalyzedSuriya.jpg")
	      if os.path.exists(save_location):
	         os.remove(save_location)	    
	      plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	      suriya = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	      suriya.reload()
	      self.h = self.h + suriya.texture.height - 600
	      suriya.pos = (10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(suriya)
	      Cache.remove("kv.image")     
	      
	    if not "sed.jpg" in solar_eclipse:        
	      solar_eclipse_img = Image( source=solar_eclipse,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + solar_eclipse_img.texture.height+180
	      solar_eclipse_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(solar_eclipse_img)
	      
	      planetary = ganita.planet_property("1")
	      pkr,pkb,pkn = planetary[0],planetary[1],planetary[2]
	      getpath = viewmodel.get_inter()
	        
	      if pkr == False:
	           paapr = (100/3)/3
	           pkr = os.path.join(getpath,"norpk.jpg")
	      if pkr == True:
	            paapr = 0
	            pkr = os.path.join(getpath,"rpk.jpg")
	      if pkb == False:
	            paapb = (100/3)/3
	            pkb = os.path.join(getpath,"nobpk.jpg")
	      if pkb == True :
	            paapb = 0
	            pkb = os.path.join(getpath,"bpk.jpg")
	      if pkn == False:
	            paapn = (100/3)/3
	            pkn = os.path.join(getpath,"nonpk.jpg")
	      if pkn == True:
	            paapn = 0
	            pkn = os.path.join(getpath ,"npk.jpg")
	      pkr_img = Image( source=pkr,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + pkr_img.texture.height
	      pkr_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(pkr_img)
	      pkb_img = Image( source=pkb,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + pkb_img.texture.height
	      pkb_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(pkb_img)
	      pkn_img = Image(source=pkn,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + pkn_img.texture.height
	      pkn_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(pkn_img)
	      Bala = { 
	        "u+" : 100,
	        "u" : 100,
	        "u-": 100,
	        "m": 75,
	        "o" : 50,
	        "f" : 37.5,
	        "nu" : 25,
	        "e" : 12.5,
	        "n" : 0,
	        "n-" : 0,
	        "n+" : 0,
	        "vgtm" : 100
	        }
	      bala,nbala = planetary[3],planetary[4]
	      RasiSthanabala = Bala[bala]*(1/3)
	      NavSthanabala = Bala[nbala]*(1/3)
	      if nbala != "vgtm":
	            nbala = os.path.join(getpath,nbala+"n.jpg")
	      if nbala == "vgtm":
	            nbala = os.path.join(getpath,"vgtm.jpg")
	      bala = os.path.join(getpath,"r"+bala+".jpg")
	      bala_img = Image(source=bala,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + bala_img.texture.height
	      bala_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(bala_img)
	      nbala_img= Image(source=nbala,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + nbala_img.texture.height
	      nbala_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(nbala_img)
	      score = RasiSthanabala + NavSthanabala + paapr + paapb + paapn 
	      revscore = 100 - score
	      self.suriya = score
	      sth = "Lagna Strength "
	      mark =[score,revscore]
	      color = ["coral","Grey"]
	      plt.figure(figsize=(8, 4))
	      label = [sth,""]
	      size = mark
	      fig2, ax2 = plt.subplots()
	      ax2.pie(size,labels=label,colors= color,autopct='%1.1f%%',startangle=90)
	      plt.title("Analysis of Suriya Lagna  (Result in Pie Chart)")
	      save_location = viewmodel.get_chartpath()
	      save_location = os.path.join(save_location,"AnalyzedSuriya.jpg")
	      if os.path.exists(save_location):
	         os.remove(save_location)	    
	      plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	      suriya = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	      suriya.reload()
	      self.h = self.h + suriya.texture.height - 600
	      suriya.pos = (10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(suriya)
	      Cache.remove("kv.image")     
	      Nakshatra = int(ganita.planetary()[0]["1"]/(360/27))+1
	      nakshatra = "n"+str(Nakshatra)+".jpg"
	      nakshatrapath = os.path.join(getpath,"nakshatra")
	      nakshatra_path = os.path.join(nakshatrapath,nakshatra)
	      nakshatra_img = Image(source=nakshatra_path,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + nakshatra_img.texture.height + 500
	      nakshatra_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(nakshatra_img)
	      
	      #conjoin
	      conjoin = os.path.join(getpath,"conjoin.jpg")
	      conjoin_img = Image(source=conjoin,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	      self.h = self.h + conjoin_img.texture.height 
	      conjoin_img.pos=(10,posh-self.h)
	      inter.gridscroll.children[0].add_widget(conjoin_img)
	      #combust
	      combust = {"2" : 12, "3" : 17, "4" : 14, "5" : 11, "6" : 10, "7" : 15 , "8" : 0, "9" : 0} 
	      planet = {"1" : "sun", "2" : "moon", "3" : "mars", "4" : "mercury", "5": "jupiter","6": "venus", "7": "saturn", "8" : "rahu", "9" : "ketu" }
	      revplanet = { 
	      "sun":"1", "moon":"2", "mars" : "3",  "mercury":"4", "jupiter":"5", "venus":"6", "saturn":"7", "rahu":"8", "ketu" : "9"
	      }
	      comp = [2,3,4,5,6,7]
	      property = ganita.planetary()
	      rasideg = property[0]
	      rasidata = property[1]
	      temp = []
	      for p,v in rasidata.items():
	          if p == "1" :
	              for pkey,val in rasidata.items():
	                  if val == v and pkey != "1":
	                      temp.append(pkey)
	      Path_temp = []
	      if len(temp) != 0:
	          for t in temp:
	              Path = os.path.join(getpath,planet[t] +".jpg")
	              Path_temp.append(Path)
	      if len(Path_temp) == 0:
	          Path = os.path.join(getpath,"noplanet.jpg")
	          Path_temp.append(Path)   
	      for Pt in Path_temp:
	          if Pt: 
	              Pt_img = Image(source=Pt,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	              self.h = self.h + Pt_img.texture.height 
	              Pt_img.pos=(10,posh-self.h)
	              inter.gridscroll.children[0].add_widget(Pt_img)
	          T = ["noplanet","rahu","ketu"]
	          for p,v in planet.items():
	                  if v in Pt and not v in T:
	                      unit = revplanet[v]
	                      d = rasideg["1"] - rasideg[unit]
	                      if d< combust[unit]:
	                          compath = os.path.join(getpath,"combustion.jpg")
	                      if d > combust[unit]:
	                          compath = os.path.join(getpath,"nocombustion.jpg")
	                      com_img =  Image(source=compath,size=(inter.scrollcellwidth,inter.scrollheight),size_hint=(None,None))
	                      self.h = self.h + com_img.texture.height 
	                      com_img.pos=(10,posh-self.h)
	                      inter.gridscroll.children[0].add_widget(com_img)
	    #Rasi inter
	    getpath = viewmodel.get_inter()         
	    pdata = ganita.planetary()
	    rasideg = pdata[2]
	    Sun = rasideg["1"]
	    close_fair_far = None
	    if Sun == 15 or ( Sun >= 10 and Sun <= 20):
	        close_fair_far = os.path.join(getpath,"rclose.jpg")
	    if (Sun < 10 and Sun > 5) or (Sun > 20 and Sun < 25 ):
	        close_fair_far = os.path.join(getpath,"rfair.jpg")
	    if Sun == 0 or Sun <= 5 or Sun >= 25:
	         close_fair_far = os.path.join(getpath,"rfar.jpg")
	    cff_img = Image(source = close_fair_far, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + cff_img.texture.height 
	    cff_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(cff_img)
	    #inter Rasi
	    rasi_inter = os.path.join(getpath,"rasi")
	    sun_inter = os.path.join(rasi_inter,"1")
	    rasi_data = pdata[1]
	    sun = rasi_data["1"]
	    sun_inter_path = os.path.join(sun_inter,sun+".jpg")
	    sun_inter_img = Image(source = sun_inter_path, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    subtractor = None
	    if sun_inter_img.texture.height < 1300:
	        subtractor = 300
	    if sun_inter_img.texture.height > 1300:
	        subtractor = 500
	    self.h = self.h + sun_inter_img.texture.height - subtractor 
	    sun_inter_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(sun_inter_img)
	    #Bhava inter
	    pdata = ganita.planetary()
	    bvdeg = pdata[5]
	    lagnadeg = ganita.set_lagna()[2]
	    Sun = bvdeg["1"]%30
	    close_fair_far = None
	    if Sun == 15 or ( Sun >= 10 and Sun <= 20):
	        close_fair_far = os.path.join(getpath,"bclose.jpg")
	    if (Sun < 10 and Sun > 5) or (Sun > 20 and Sun < 25 ):
	        close_fair_far = os.path.join(getpath,"bfair.jpg")
	    if Sun == 0 or Sun <= 5 or Sun >= 25:
	         close_fair_far = os.path.join(getpath,"bfar.jpg")
	    cff_img = Image(source = close_fair_far, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + cff_img.texture.height + 400
	    cff_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(cff_img)
	    #Inter Bhava
	    
	    
	    bhava_inter = os.path.join(getpath,"bhava")
	    sun_inter = os.path.join(bhava_inter,"1")
	    lagna_rasi = ganita.set_lagna()[1]
	    bhava_data = pdata[4]
	    sun = bhava_data["1"]
	    sun = int(sun) - int(lagna_rasi) + 1
	    if sun < 0:
	        sun += 12
	    if sun == 0:
	        sun = 12
	        
	    sun_inter_path = os.path.join(sun_inter,str(sun)+".jpg")
	    sun_inter_img = Image(source = sun_inter_path, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + sun_inter_img.texture.height - 500
	    sun_inter_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(sun_inter_img)
	    
	    #Navam Intrro
	    nclose= os.path.join(getpath,"nclose.jpg")
	    nclose_img = Image(source = nclose, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + nclose_img.texture.height + 400
	    nclose_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(nclose_img)
	    #Navam Inter Planet
	    nav_inter = os.path.join(getpath,"navam")
	    sun_nav_inter =  os.path.join(nav_inter,"1")
	    sun_nav = pdata[3]
	    sun = sun_nav["1"] 
	    navlord = { "1" : "3" , "2" : "6", "3" :"4", "4":"2","5":"1","6":"4","7":"6","8":"3","9":"5","10":"7","11":"7","12":"5"}
	    nav_p = navlord[sun]
	    nav_p_path = os.path.join(sun_nav_inter,"p"+nav_p+".jpg")
	    nav_p_img  = Image(source = nav_p_path, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + nav_p_img.texture.height - 500
	    nav_p_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(nav_p_img)
	    #Navam Inter House
	    navlagna = ganita.navam_no_finder()
	    nvL = int(navlagna)
	    sun = int(sun) - nvL +1 
	    if sun < 0:
	        sun += 12
	    if sun == 0:
	        sun = 12
	    
	    sun_nav_inter_path = os.path.join(sun_nav_inter,str(sun)+".jpg")
	    sun_nav_inter_img = Image(source = sun_nav_inter_path, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + sun_nav_inter_img.texture.height - 500
	    sun_nav_inter_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(sun_nav_inter_img)
	    
	    #Bar
	    data = [ self.udaya, self.chandra, self.suriya ]
	    labels = [ "Udaya","Chandra","Suriya"]
	    colors = [ "lightgreen","lightblue","coral"]
	    fig, ax = plt.subplots()
	    ax.bar(labels, data, color=colors)
	    # Labeling the graph
	    ax.set_xlabel("Types of lagna")
	    ax.set_ylabel('Strengths')
	    ax.set_title('Comparative Category')
	    save_location = viewmodel.get_chartpath()
	    save_location = os.path.join(save_location,"Comparative.jpg")
	    if os.path.exists(save_location):
	         os.remove(save_location)	    
	    plt.savefig(save_location, format='jpg', dpi=300, bbox_inches = 'tight')
	    comparative = Image(source = save_location, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    comparative.reload()
	    self.h = self.h + comparative.texture.height - 200
	    comparative.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(comparative)
	    Cache.remove("kv.image")     
	    #UCS	   
	    ucs1,ucs2 = os.path.join(getpath,"ucs1.jpg"), os.path.join(getpath,"ucs2.jpg")
	    ucs1_img = Image(source = ucs1, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + ucs1_img.texture.height 
	    ucs1_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(ucs1_img)
	    ucs2_img = Image(source = ucs2, size=(inter.scrollcellwidth,inter.scrollheight), size_hint=(None,None))
	    self.h = self.h + ucs2_img.texture.height 
	    ucs2_img.pos = (10,posh-self.h)
	    inter.gridscroll.children[0].add_widget(ucs2_img)
	    
	    #Yoga 
	    yoga = os.path.join(getpath,"yoga")
	    adder = 0
	    def set_image(path,h,inters,adder):
	        img = Image(source = path, size=(inters.scrollcellwidth,inters.scrollheight), size_hint=(None,None))
	        h = h + img.texture.height + adder
	        img.pos = (10,posh-h)
	        inters.gridscroll.children[0].add_widget(img)
	        return h
	    yoga_path = os.path.join(yoga,"suriya.jpg")
	    self.h = set_image(yoga_path,self.h,inter,adder)
	    
	    #Suriya Yoga Analysis
	    charttype = {"rasi" : 0 , "bhava" : 1, "navamsa" : 2}
	    
	    self.adder = 0
	    def suriya_yoga_view(suriya_yogas,yogas):
	        if suriya_yogas is None or suriya_yoga != [0,1,0]:
	            return None
	        if suriya_yogas and suriya_yogas == [0,1,0]:
	            self.adder = -500
	            yoga_inter_path = os.path.join(yogas,"ubayachari.jpg")
	            return yoga_inter_path
	        else:
	            return suriya_yogas 
	    
	    #intro path    
	    rasi_yoga_path = os.path.join(yoga,"rasi.jpg")
	    bhava_yoga_path = os.path.join(yoga,"bhava.jpg")
	    navamsa_yoga_path = os.path.join(yoga,"navamsa.jpg")
	    
	    #Rasi Yoga view
	    adder = 600 #Rasi yoga intro 
	    self.h = set_image(rasi_yoga_path,self.h,inter,adder)
	    chart = charttype["rasi"]
	    suriya_yoga = ganita.suriya_yoga(chart)
	    yoga_inter_path = suriya_yoga_view(suriya_yoga,yoga)
	    temp, temp2 = None,None
	    if yoga_inter_path is None:
	        temp = ganita.vesi_yoga(chart)
	        temp2 = ganita.vasi_yoga(chart)
	        if temp is None:
	            #temp2 = ganita.vasi_yoga(chart)
	            if temp2 is None:
	                no_yoga = os.path.join(yoga,"noyoga.jpg")
	                self.h = set_image(no_yoga,self.h,inter,self.adder)
	        if not temp2 is None:
	            for t,i in zip(temp2,range(len(temp2))):
	                    path_vasi = os.path.join(yoga,t+"vasi.jpg")
	                    if i == 0:
	                        self.adder = - 500
	                    else:
	                        self.adder = 0
	                    self.h = set_image(path_vasi,self.h,inter,self.adder)
	                    
	        if not temp is None:
	            for t,i in zip(temp,range(len(temp))):
	                path_vesi = os.path.join(yoga,t+"vesi.jpg")
	                if i == 0 and temp2 is None:
	                    self.adder = - 500
	                else:
	                    self.adder = 0
	                self.h = set_image(path_vesi,self.h,inter,self.adder)
	          
	    if yoga_inter_path:
	        self.h = set_image(yoga_inter_path,self.h,inter,self.adder)
	    
	    #Bhava Yoga view
	    self.h = set_image(bhava_yoga_path,self.h,inter,adder)
	    chart = charttype["bhava"]
	    suriya_yoga = ganita.suriya_yoga(chart)
	    yoga_inter_path = suriya_yoga_view(suriya_yoga,yoga) #check ubaya 
	    no_yoga = os.path.join(yoga,"noyoga.jpg")
	    temp, temp2 = None,None
	    if yoga_inter_path is None:
	        temp = ganita.vesi_yoga(chart)
	        temp2 = ganita.vasi_yoga(chart)
	        if temp is None:
	            #temp2 = ganita.vasi_yoga(chart)
	            if temp2 is None:
	                self.adder = 0          
	                self.h = set_image(no_yoga,self.h,inter,self.adder)
	        if not temp2 is None:
	            for t,i in zip(temp2,range(len(temp2))):
	                    path_vasi = os.path.join(yoga,t+"vasi.jpg")
	                    if i == 0:
	                        self.adder = - 500
	                    else:
	                        self.adder = 0
	                    self.h = set_image(path_vasi,self.h,inter,self.adder)
	                    
	        if not temp is None:
	            for t,i in zip(temp,range(len(temp))):
	                path_vesi = os.path.join(yoga,t+"vesi.jpg")
	                if i == 0 and temp2 is None:
	                    self.adder = - 500
	                else:
	                    self.adder = 0
	                self.h = set_image(path_vesi,self.h,inter,self.adder)
	          
	    if yoga_inter_path:
	        self.h = set_image(yoga_inter_path,self.h,inter,self.adder)
	    
	    
	    #Maha Purusha 
	    maha_path = os.path.join(yoga,"maha.jpg")
	    
	    self.h = set_image(maha_path,self.h,inter,adder)
	    #rasi 
	    chart = charttype["rasi"]
	    maha = ganita.mahapurusha(chart)
	    self.h = set_image(rasi_yoga_path,self.h,inter,adder)
	    if maha is None:
	        self.adder = 0
	        self.h = set_image(no_yoga,self.h,inter,self.adder)
	    if maha:
	        for m,i in zip( maha, range(len(maha))):
	            m = str(m)
	            mpath = os.path.join(yoga,m+"maha.jpg")
	            self.adder = 0
	            if i == 0:
	                self.adder = -500
	            self.h = set_image(mpath,self.h,inter,self.adder)
	    #navamsa
	    chart = charttype["navamsa"]
	    maha = ganita.mahapurusha(chart)
	    self.h = set_image(navamsa_yoga_path,self.h,inter,adder)
	    if maha is None:
	        self.adder = 0
	        self.h = set_image(no_yoga,self.h,inter,self.adder)
	    if maha:
	        for m,i in zip( maha, range(len(maha))):
	            m = str(m)
	            mpath = os.path.join(yoga,m+"maha.jpg")
	            self.adder = 0
	            if i == 0:
	                self.adder = -500
	            self.h = set_image(mpath,self.h,inter,self.adder)
	    #Raja
	    self.adder = 0	    
	    rjpath = os.path.join(yoga,"raja.jpg")
	    self.h = set_image(rjpath,self.h,inter,adder)         
	    self.h = set_image(rasi_yoga_path,self.h,inter,adder)
	    no_raja_yoga = os.path.join(yoga,"noraja.jpg")
	    #PVRY
	    parivartana = ganita.parivartana_raja()
	    if parivartana:
	        for k,v in parivartana.items():
	            if not k in ["5","9"]:
	                temp = v 
	                v = k
	                k = temp
	                
	                
	            pvtry = os.path.join(yoga,k+"pv"+v+".jpg")
	            self.h = set_image(pvtry,self.h,inter,self.adder)
	    else:
	        nopvtry = os.path.join(yoga,"noparivartana.jpg")
	        self.h = set_image(nopvtry,self.h,inter,self.adder)
	    #PRY
	    parashari = ganita.parashari_raja()
	    paraeffect = ganita.kentri_effect()[0]
	    if parashari:
	        for p,i in zip(parashari,paraeffect):
	              pry = os.path.join(yoga,p+"pry.jpg")
	              self.h = set_image(pry,self.h,inter,self.adder)
	              pryeffect = os.path.join(yoga,i+".jpg")
	              self.h = set_image(pryeffect,self.h,inter,self.adder)
	              
	    else:
	        pry = os.path.join(yoga,"noparashari.jpg")
	        self.h = set_image(pry,self.h,inter,self.adder)
	    #YTRY
	    yuti = ganita.yuti_raja()
	    yutieffect = ganita.kentri_effect()[1]
	    if yuti:
	        for y,e in zip(yuti,yutieffect):
	            i , j = y[0],y[1]
	            ytry = os.path.join(yoga,i+"c"+j+".jpg")
	            self.h = set_image(ytry,self.h,inter,self.adder)
	            ytryeffect = os.path.join(yoga,e+".jpg")
	            self.h = set_image(ytryeffect,self.h,inter,self.adder)
	            
	    else:
	            ytry = os.path.join(yoga,"noyuti.jpg")
	            self.h = set_image(ytry,self.h,inter,self.adder)
	            
	    #NBRY
	    nbry_raja =  ganita.bhanga_raja()
	    
	    if nbry_raja != None:
	        for nb in nbry_raja:
	            nbry_path = os.path.join(yoga,nb+"nbry.jpg")
	            self.h = set_image(nbry_path,self.h,inter,self.adder)
	    if not nbry_raja:
	        no_nbry_yoga = os.path.join(yoga,"nonbry.jpg")
	        self.h = set_image(no_nbry_yoga,self.h,inter,self.adder)
	    
	    vipreet = ganita.vipreet()
	    if vipreet[0] == 1:
	        hasha = os.path.join(yoga,"6vipreet.jpg")
	        self.h = set_image(hasha,self.h,inter,self.adder)
	    if vipreet[1] == 1:
	        sarala = os.path.join(yoga,"8vipreet.jpg")
	        self.h = set_image(sarala,self.h,inter,self.adder)
	    if vipreet[2] == 1:
	        vimala = os.path.join(yoga,"12vipreet.jpg")
	        self.h = set_image(vimala,self.h,inter,self.adder)
	    if vipreet == [0,0,0]:
	        novipreet = os.path.join(yoga,"novipreet.jpg")
	        self.h = set_image(novipreet,self.h,inter,self.adder)
	    #Gaja Keseri 
	    gkry = ganita.gkry()
	    if gkry:
	        effect = ganita.gkryeffect()
	        effect_yoga = os.path.join(yoga,effect+".jpg")
	        gkry_yoga = os.path.join(yoga,"gkry.jpg")
	        self.h = set_image(gkry_yoga,self.h,inter,self.adder)
	        self.h = set_image(effect_yoga,self.h,inter,self.adder)
	    #self.h = set_image(no_raja_yoga,self.h,inter,self.adder)
	    #Duyoga
	    duyoga1 = os.path.join(yoga,"duyoga1.jpg")
	    duyoga2 = os.path.join(yoga,"duyoga2.jpg")
	    self.adder = -500
	    self.h = set_image(duyoga1,self.h,inter,self.adder)
	    self.adder = 0
	    self.h = set_image(duyoga2,self.h,inter,self.adder)
	    adder = 600
	    self.h = set_image(rasi_yoga_path,self.h,inter,adder)
	    #kalasarpa 
	    kalasarpa = ganita.kalasarpa()
	    if kalasarpa:
	        self.adder = -500
	        kls = os.path.join(yoga,"kls.jpg")
	        self.h = set_image(kls,self.h,inter,self.adder)     
	    if kalasarpa is False:
	        self.adder = 0
	        nokls = os.path.join(yoga,"nokls.jpg")
	        self.h = set_image(nokls,self.h,inter,self.adder)  
	    #chandala 
	    chandal = ganita.chandal()
	    if chandal:
	        self.adder = 0
	        for c in chandal:
	            cpath = os.path.join(yoga,c+"cdl.jpg")
	            self.h = set_image(cpath,self.h,inter,self.adder)
	    else:
	        if kalasarpa:
	            self.adder = 600
	        cpath = os.path.join(yoga,"nocdl.jpg")
	        self.h = set_image(cpath,self.h,inter,self.adder)
	   #vish
	    vish = ganita.vish()
	    if vish is True:
	        self.adder = 0
	        vpath = os.path.join(yoga,"vish.jpg")
	        self.h = set_image(vpath,self.h,inter,self.adder)
	        
	    else:
	        if chandal:
	            self.adder = 600
	        else:
	            self.adder = 0
	        novpath = os.path.join(yoga,"novish.jpg")
	        self.h = set_image(novpath,self.h,inter,self.adder)
	    #kemadruma
	    kmdm = ganita.kemadruma()
	    if kmdm:
	        self.adder = 0
	        kpath = os.path.join(yoga,"kmdm.jpg")
	        self.h = set_image(kpath,self.h,inter,self.adder)
	    else:
	            if vish:
	                self.adder = 600
	            else:
	                self.adder = 0
	            nokpath = os.path.join(yoga,"nokmdm.jpg")
	            self.h = set_image(nokpath,self.h,inter,self.adder)
	    if kmdm:
	        self.adder = 600
	    else:
	        self.adder = 0
	    #bandhana
	    bdn = ganita.bandhana("rasi")
	    bdn = os.path.join(yoga,str(bdn)+"bdn.jpg")
	    self.h = set_image(bdn,self.h,inter,self.adder)
	    #Arihta
	    self.adder = 0
	    arh = ganita.arihta("rasi",self.udaya,self.chandra,self.suriya)
	    if arh:
	        arihta = os.path.join(yoga,"arihta.jpg")
	        self.h = set_image(arihta,self.h,inter,self.adder)
	    else:
	        noarihta = os.path.join(yoga,"noarihta.jpg")
	        self.h = set_image(noarihta,self.h,inter,self.adder)
	    #dhana
	    dhana = os.path.join(yoga,"dhana.jpg")
	    self.adder = -500
	    self.h = set_image(dhana,self.h,inter,self.adder)
	    #dhnana_data rasi 
	    DN = ganita.dhana_yoga("rasi")
	    paraeffect = ganita.dhana_effect("rasi")[1]
	    parashari = DN[0]
	    parivartana = DN[1] 
	    yuti = DN[2]
	    self.adder = 600
	    self.h = set_image(rasi_yoga_path,self.h,inter,adder)
	    self.adder = 0
	    if parashari:
	        i = 0
	        for lord,pe in zip(parashari,paraeffect):
	            paradhana = os.path.join(yoga,lord+"i"+parashari[lord]+"paradhana.jpg")
	            pref = os.path.join(yoga,paraeffect[lord]+".jpg")
	            self.h = set_image(paradhana,self.h,inter,self.adder)
	            self.h = set_image(pref,self.h,inter,self.adder)
	            i += 1
	    else:
	        noparadhana = os.path.join(yoga,"noparadhana.jpg")     
	        self.h = set_image(noparadhana,self.h,inter,self.adder)
	    if yuti:
	        yutieffect = ganita.dhana_effect("rasi")[0]
	        self.adder = 0
	        for yg,effect in zip(yuti,yutieffect):
	              for vlist in yuti[yg]:
	                  for v,i in zip(vlist,range(len(vlist))):
	                      intyg,intv = int(yg) , int(v)
	                      if intyg > intv:
	                          yg = str(intv)
	                          v = str(intyg)
	                  
	                          yutidhana = os.path.join(yoga,yg+"n"+v+"yutidhana.jpg")
	                          self.h = set_image(yutidhana,self.h,inter,self.adder)
	                          ygeffect = os.path.join(yoga,yutieffect[effect][i]+".jpg")
	                          self.h = set_image(ygeffect,self.h,inter,self.adder)
	    else:
	        self.adder = 0
	        noyutidhana = os.path.join(yoga,"noyutidhana.jpg")
	        self.h = set_image(noyutidhana,self.h,inter,self.adder) 
	    if parivartana:
	        for k,v in parivartana.items():
	            intk , intv = int(k) , int(v)
	            if intk > intv:
	                k = str(intv)
	                v = str(intk)
	            paridhana = os.path.join(yoga,k+"v"+v+"paridhana.jpg")
	            self.h = set_image(paridhana,self.h,inter,self.adder)
	    else:
	        noparidhana = os.path.join(yoga,"noparidhana.jpg")
	        self.h = set_image(noparidhana,self.h,inter,self.adder)            
	    
	    self.h = set_image(navamsa_yoga_path,self.h,inter,self.adder)
	    #
	    DN = ganita.dhana_yoga("navam")
	    parashari = DN[0]
	    parivartana = DN[1] 
	    yuti = DN[2]
	    self.adder = 0
	    if parashari:
	        i = 0
	        for lord,house in parashari.items():
	            paradhana = os.path.join(yoga,lord+"i"+house+"paradhana.jpg")
	            self.h = set_image(paradhana,self.h,inter,self.adder)
	            i += 1
	    else:
	        noparadhana = os.path.join(yoga,"noparadhana.jpg")     
	        self.h = set_image(noparadhana,self.h,inter,self.adder)
	    if yuti:
	        self.adder = 0
	        for k,vlist in yuti.items():
	              for v in vlist:
	                  intk,intv = int(k) , int(v)
	                  if intk > intv:
	                      k = str(intv)
	                      v = str(intk)
	                  
	                  yutidhana = os.path.join(yoga,k+"n"+v+"yutidhana.jpg")
	                  self.h = set_image(yutidhana,self.h,inter,self.adder)
	    else:
	        self.adder = 0
	        noyutidhana = os.path.join(yoga,"noyutidhana.jpg")
	        self.h = set_image(noyutidhana,self.h,inter,self.adder) 
	    if parivartana:
	        for k,v in parivartana.items():
	            intk , intv = int(k) , int(v)
	            if intk > intv:
	                k = str(intv)
	                v = str(intk)
	            paridhana = os.path.join(yoga,k+"v"+v+"paridhana.jpg")
	            self.h = set_image(paridhana,self.h,inter,self.adder)
	    else:
	        noparidhana = os.path.join(yoga,"noparidhana.jpg")
	        self.h = set_image(noparidhana,self.h,inter,self.adder)
	    
	    
	    #
	    end = os.path.join(yoga,"end.jpg")
	    self.h = set_image(end,self.h,inter,self.adder)
	    self.adder = -500
	    end2 = os.path.join(yoga,"end2.jpg")
	    self.h = set_image(end2,self.h,inter,self.adder)
	    
	    
	    
	        
	    
	    
	    
	    
	        
	    
	    
	
	def reset(self,*args,**kwargs):
	    self = self.main_view.view
	    self.remove_widget(self.boxlayout)
	    self.boxlayout.clear_widgets()
	    self.boxlayout.add_widget(self.gridlayout)
	    self.boxlayout.add_widget(self.grid_button)
	    self.boxlayout.add_widget(self.grid_button2)
	    self.controller.layout_definder()
	    self.controller.zata_background()	    
	    self.scrollview.add_widget(self.gridscroll)
	    self.boxlayout.add_widget(self.viewnav)
	    self.add_widget(self.boxlayout)
	    
	def layout_definder(self,*args,**kwargs):
	     self = self.main_view.view
	     self.scrollview = ScrollView(
	     size_hint=(1,None),size=(1100,2100/2.4),width = 800, do_scroll_x = False)#scroll declare
	     self.gridscroll = GridLayout(
	     cols=1,size_hint_y=None)#Grid inner scroll
	     self.gridscroll.bind(minimum_height=self.gridscroll.setter('height'))
	     self.gridscroll.spacing=[100,10]
	     self.gridscroll.padding=[100,2]
	     self.boxlayout.add_widget(self.scrollview)
	     
	    
	def Navam_chart_generator(self,Navam,*args,**kwargs):
	    self = self.main_view.view
	    index = 2
	    self.controller.chart_generator(index,Navam)
	
	def Bhava_chart_generator(self,Bhava,*args,**kwargs):
	    self = self.main_view.view
	    index = 1
	    self.controller.chart_generator(index,Bhava)
	def Rasi_chart_generator(self,Rasi,*args,**kwargs):         
             self = self.main_view.view
             index = 0 #0Rasi, 1Bhava, 2Navam
             self.controller.chart_generator(index,Rasi)
             
	def zata_background(self,*args,**kwargs):
	     self = self.main_view.view
	     i = 1
	     region_name = ["ရာသီ","ဘာဝ", "နဝင်း"]
	     for v in region_name:
	           self.v = Button( text=v,
	           size=(900,2100/2.4),
	           size_hint=(None,None),
	           halign = "center",
	           valign = "middle",
	           background_color = (0,1,0,0.1),
	           disabled = True,
	           font_name = self.font_loc)
	           self.gridscroll.rows = i
	           self.v.id= str(i)
	           self.v.theme_color = "Custom"
	           self.v.color = ( 27/255,133/255,1,0.7)
	           if i < 4:
	               self.gridscroll.add_widget(self.v)
	               i+=1
	     self.controller.zata_design()
	     data = self.model.get_lagna()
	     self.controller.Rasi_chart_generator(data[0])
	     self.controller.Bhava_chart_generator(data[1])
	     self.controller.Navam_chart_generator(data[2])
	     
            
	def zata_design(self,*args,**kwargs):
	     self = self.main_view.view
	     j = 0
	     w = 900
	     ws = 1000
	     h = 2100/2.4
	     for wg in self.gridscroll.children:
	           zata = Widget()
	           with zata.canvas.after:
	                Color(27/255,133/255,1,0.7)
	                Line(points=[w/2.2,10+(j*(h+10)),w/2.2,h+(j*(h+10))], width=2)
	                Line(points=[w/1.3,10+(j*(h+10)),w/1.3,h+(j*(h+10))], width=2)
	                Line(points=[100,10+(j*(h+10)),100,h+(j*(h+10))],width=2)
	                Line(points=[ws,10+(j*(h+10)),ws,h+(j*(h+10))],width=2)
	                #horizon line
	                Line(points=[100,h/1.5+(j*h),ws,h/1.5+(j*h)], width=2)
	                Line(points=[100,h/2.5+(j*h),ws,h/2.5+(j*h)], width=2)
	                Line(points=[100,h+(j*(h+10)),ws,h+(j*(h+10))],width=2)
	                Line(points=[100,10+(j*(h+10)),ws,10+(j*(h+10))],width=2)
	                
	                #45deg left bottom
	                Line(points=[100,10+(j*(h+10)),(ws/2.2)-50,h/2.5+(j*h)], width=2)
	                #45deg left upper
	                Line(points=[100,h+(j*(h+10)),(ws/2.2)-50,h/1.5+(j*h)], width=2)
	                #45deg right bottom
	                Line(points=[(ws/1.3)-80,h/2.5+(j*h),ws,10+(j*(h+10))], width=2)
	                #45deg right upper
	                Line(points=[(ws/1.3)-80,h/1.5+(j*h),ws,h+(j*h)], width=2)
	                wg.add_widget(zata)
	                j+=1 
	
	def trigger(self,*args,**kwargs):
	    data = self.model.get_lagna()
	    self.view.Rasi_chart_generator(data)
	    self.view.boxlayout.clear_widgets()
	    self.view.clear_widgets()
	      
	def get_user_data(self,*args):
	     return self.model.get_default_user_data()
	def get_lat_lon(self,*args):
	    return self.model.get_lat_lon() 
	        	     
	def set_pob(self,poblist,*args):
	    original_tob = self.model.get_time()
	    original_pob = self.model.get_lat_lon()
	    original_offset = self.model.get_offset()
	    if isinstance(original_offset, str):
	        update_offset = str(poblist[2])
	    else:
	        original_offset = str(original_offset)
	        update_offset = str(poblist[2])
	    pattern = r'^[+-]\d+(\.\d+)?$' 
	    if re.match(pattern, update_offset):
	        if original_offset == update_offset:
	            update_offset = original_offset
	        else:
	            pass
	    else:
	        update_offset = original_offset
	    pattern_lon = r'([-+]?\d*\.\d+|\d+)\u00b0([WE])'
	    pattern_lat = r'([-+]?\d*\.\d+|\d+)\u00b0([NS])'
	    if re.match(pattern_lon,poblist[0]):
	        update_lon = poblist[0]
	    else:
	        update_lon = original_pob[0]
	        #dialog ထည့်ရန်
	    if re.match(pattern_lat,poblist[1]):
	        update_lat = poblist[1]
	    else:
	        update_lat = original_pob[1]
	        #dialog ထည့်ရန်
	    update_pob = [update_lon,update_lat]
	    original_tob[0] = update_offset
	    update_tob = original_tob
	    #self.view.viewaid.tester(update_tob)
	    update_user_data = self.model.set_time(update_tob)
	    update_user_data = self.model.set_pob(update_pob)
	    self.view.label.text = update_user_data
	    return update_user_data
	    
	def chart_generator(self,index,Rasi,*args,**kwargs):
         self = self.main_view.view
         count = [1,2,3,4,5,6,7,8]
         chartlist = [0,878,1758]
         chart = chartlist[index] 
         for r in Rasi:
             R = Rasi[r]
             for c in count:
                  self.controller.chart_cell_filler(c,chart,R,r)
	def chart_cell_filler(self,c,chart,R,r,*args,**kwargs):
             self = self.main_view.view
             tester = []
             n = len(R) 
             if n == c:
                 j = 0
                 for p,i in zip(R,range(n)):
                     if r == "1":
                         hfactor = 3*770
                         wfactor = 470
                         if i == 3:
                             hfactor = 3*770
                             wfactor = 470
                         if i == 4:
                             hfactor = 3*770
                             wfactor = 470
                         if i == 5:
                             hfactor = 3*770
                             wfactor = 470
                         if i == 6:
                             hfactor = 3*670
                             wfactor = 570
                         if i == 7:
                             hfactor = 3*670
                             wfactor = 570
                     if r == "2":
                         hfactor = 3*800
                         wfactor = 370
                         if i == 4:
                             hfactor = 3*750
                             wfactor = 320
                         if i == 5:
                             hfactor = 3*750
                             wfactor = 280
                         if i == 6:
                             hfactor = 3*750
                             wfactor = 240
                         if i == 7:
                              hfactor = 3*730
                              wfactor = 200
                     if r == "3":
                         hfactor = 3*770
                         wfactor = 120
                         if i == 5:
                             hfactor = 3*730
                             wfactor = 170
                         if i == 6:
                             hfactor = 3*690
                             wfactor = 170
                         if i == 7:
                             hfactor = 3*680
                             wfactor = 200
                     if r == "4":
                         hfactor = 3*695
                         wfactor = 150
                         if i >= 4:
                             hfactor = 3*630
                             wfactor = 250
                     if r == "5":
                         hfactor = 3*600
                         wfactor = 110
                         if i >= 5:
                             hfactor = 3*550
                             wfactor = 200
                     if r == "6":
                         hfactor = 3*590
                         wfactor = 310
                         if i >= 4:
                             hfactor = 3*530
                             wfactor = 370
                     if r == "7":
                         hfactor = 3*598
                         wfactor = 530
                         if i >= 4:
                             hfactor = 3*530
                             wfactor = 470
                     if r == "8":
                         hfactor = 3*600
                         wfactor = 700
                         if i >= 4:
                             hfactor = 3*520
                             wfactor = 770
                     if r == "9":
                         hfactor = 3*600
                         wfactor = 960
                         if i >= 4:
                             hfactor = 3*550
                             wfactor = 910
                     if r == "10":
                         hfactor = 3*695
                         wfactor = 900
                         if i > 3:
                             hfactor = 3*630
                             wfactor = 830
                     if r == "11":
                         hfactor = 3*770
                         wfactor = 890
                         if i >= 3:
                             hfactor = 3*720
                             wfactor = 958
                     if r == "12":
                         hfactor = 3*790
                         wfactor = 710
                         if i > 3:
                             hfactor = 3*740
                             wfactor = 790
                     P1 = MDLabel(text=p,pos=(wfactor,(hfactor+(50*i))-chart))
                     
                     self.gridscroll.children[0].children[0].add_widget(P1)

		      	            
	def set_name(self,name,*args):
	     if len(name) > 25 or len(name) < 1:
	         pass #err dialog activate ရန်
	     else:
	         update_user_data = self.model.set_name(name)
	         self.view.label.text = update_user_data  