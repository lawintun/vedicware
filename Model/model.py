import os
import json
import datetime
import pprint
#from geopy.geocoders import Nominatim
import re
import pandas as pd
import matplotlib.pyplot as plt
from Model.viewmodel import ViewModel
from Model.vedicmodel import VedicModel,VimshottariModel,GanitaModel#integrating testing
#from viewmodel import ViewModel #for unit testing
#from vedicmodel import VedicModel,VimshottariModel,GanitaModel #for unit testing

class Model:
	def __init__(self,**kwargs):
		self._DB = "/storage/emulated/0/Kivy02/vedicware/Model/Database/User_DB"
		self._db = "/storage/emulated/0/Kivy02/vedicware/Model/Database" #andriod os
		self.viewaidpath = "/storage/emulated/0/Kivy02/vedicware/View"
		self._default_name = "May Pyae Sone Aung"
		self._default_dob = [9 , 5 , 1996 ]
		self._default_tob = ["+6.5", "09" , "09" , "00", "AM"]
		self._default_pob = [
		"96.0880556°E",
		"21.9772222°N"
		]
		self._default_offset = self._default_tob[0]
		
		self._default_user_data = {
		"Name" : self._default_name,
		"DOB" : self._default_dob,
		"TOB" : self._default_tob,
		"POB" : self._default_pob 
		}
		self.view_model = ViewModel(model=self)
		self.vedic_model = VedicModel(model=self)
		self.vimshottari_model = VimshottariModel(model=self)
		self.ganita_model = GanitaModel(model=self)
		
	def get_db(self,*args):
		return self._db
	def get_sample_lagna(self,*args):
	    path = os.path.join(self._DB,"sample_chart.json")
	    with open(path,"r") as f:
	        data = json.load(f)
	        f.close()
	    for d in data:
	        if d == "rasi":
	            Data = data[d]
	    return Data
	    	
	def get_lagna(self,*args):
	    self.ganita_model.update_lagna()
	    path = os.path.join(self._DB,"chart.json")   
	    with open(path,"r") as f:
	        data = json.load(f)
	        print("\n data ", data)
	        f.close()
	    for d in data:
	       if d == "rasi":
	             R = data[d]
	       elif d == "bhava":
	           B = data[d]
	       elif d == "navam":
	           N = data[d]
	    return R,B,N
	    	
	def get_time(self,*args):
	    data = self.user_json_retrieve("default_user.json")
	    for key in data:
	        if key == "TOB":
	            return data[key]
	def get_offset(self,*args):
	    data = self.user_json_retrieve("default_user.json")
	    for key in data:
	        if key == "TOB":
	            return data[key][0]
	            
	def get_lat_lon(self,*args):
	    data = self.user_json_retrieve("default_user.json")
	    if data:
	        for key in data:
	            if key == "POB":
	                return data[key]
	        
	    
	def get_default_user_data(self,*args):
	        		return self._default_user_data 
	        				
   		
	def dir_check(self,path):
		if os.path.isdir(path):
		    return True
		else:
		    return False

#CREATE - C 		    		    
	def user_json_create(self,file_name,json_data,*args):
	   path = os.path.join(self._DB,file_name)
	   try:
		      with open(path, "w") as user_file:
		           json.dump(json_data,user_file,indent=4)
		           return True
	   except Exception as e:
	     return False

#RETRIEVE - R	     	     
	def user_json_retrieve(self,file_name,*args):
	     path = os.path.join(self._DB,file_name)
	     try:
	         with open(path,"r") as user_file:
	             user_data = json.load(user_file)
	             return user_data
	     except Exception as e:
	         return False
	     
      
	# Write Default User Data, 
	#logic အမှား နဲ့ result အမှန်  ၊           
	def set_user_data(self,*args):
		self.file_name = "default_user.json"
		file_name = self.file_name
		if self.dir_check(self._DB):
		    path = os.path.join(self._DB,file_name)
		    if self.dir_check(path): #မရှိသေးပြင်
		        self.user_json_create(file_name,self._default_user_data)
		        return self.user_json_retrieve(file_name)
		    else: #ရှိပြီးသားဆို မပြင်
		        return self.user_json_retrieve(file_name)		    
		else:
		    os.makedirs(self._DB, exist_ok=True)
		    if self.user_json_create(file_name,self._default_user_data):
		        return self.user_json_retrieve(file_name)	       
	
	def get_default_user_data(self,*args):
	    user_data = self.set_user_data()
	    get_data = self.format_user_data(user_data)
	    return get_data
	    
#Current Set the name by user	    
	def set_name(self,name,*args):
	     file_name = "default_user.json"
	     data = self.user_json_retrieve(file_name)
	     for key in data:
	         	     if key == "Name":
	         	        data[key] = name
	         	        break
	     if self.user_json_create(file_name,data):
	         update_data = self.user_json_retrieve(file_name)
	         format_update_data = self.format_user_data(update_data)
	         #pprint.pprint(update_data)
	         return format_update_data
	    
	def set_pob(self,poblist,*args):
	    file_name = "default_user.json"
	    data = self.user_json_retrieve(file_name)
	    for key in data:
	        if key == "POB":
	            data[key] = poblist
	            break
	    if self.user_json_create(file_name,data):
	        update_data = self.user_json_retrieve(file_name)
	        format_update_data = self.format_user_data(update_data)
	        return format_update_data
	           	        	
	def set_time(self,timelist,*args):
	    file_name = "default_user.json"
	    data = self.user_json_retrieve(file_name)
	    for key in data:
	        if key == "TOB":
	            data[key] = timelist
	            break
	    if self.user_json_create(file_name,data):
	        update_data = self.user_json_retrieve(file_name)
	        format_update_data = self.format_user_data(update_data)
	        return format_update_data
	        
	def set_date(self,datelist,*args):
	   file_name = "default_user.json"
	   data = self.user_json_retrieve(file_name)
	   for key in data:
	       if key == "DOB":
	           data[key] = datelist
	           break
	   if self.user_json_create(file_name,data):
	       update_data = self.user_json_retrieve(file_name)
	       format_update_data = self.format_user_data(update_data)
	       return format_update_data            	            		         	            		        
	def format_user_data(self,user_data,*args):	        
            values = []
            data = user_data
            dob_string = (
            "{}/{}/{}")
            tob_string = (
            "{}:{}:{}{}"
            )
            base_string = (
            "\nName: {}\n"
            "DOB: {}\n"
            "TOB: {}\n"
            "POB_lon: {}\n"
            "POB_lat: {}\n"
            "Time Offset: UTC{}")
            if data:
                for k,v in data.items():
                    values.append(v)
            
            if values:
                dob_format = dob_string.format(values[1][0],values[1][1],values[1][2])
                tob_format = tob_string.format(values[2][1],values[2][2],values[2][3],values[2][4])
                default_user_data = base_string.format(values[0],dob_format,tob_format,values[3][0],values[3][1],values[2][0])
                print(default_user_data)
                return default_user_data                
  
"""model = Model()
ganita = GanitaModel(model)
vm = ViewModel(model)"""
"""vtd = VimshottariModel(model)
udata = model.user_json_retrieve("default_user.json")
print(udata)
date = udata["DOB"]
h = int(udata["TOB"][1])
m = int(udata["TOB"][2])
s = int(udata["TOB"][3])
time = [h,m,s]
Moon = ganita.planetary()[0]["2"]
vtd.first_dosha_calculator(date,time,Moon)
print("\n  Moon %, " ,Moon)"""
#n = ganita.kentri_raja()
#print(n[0],n[2],n[7])

#de = ganita.dhana_yoga("rasi")
#d = ganita.dhana_effect("rasi")
#print("\n Ans ",d, " : ")
"""rasi = ganita.planetary()[1]
asc = ganita.set_lagna()[1]
n = ganita.uOFn_kendra_aORm("6",rasi,asc)
print("\n   ",n)"""

"""pdata = ganita.planetary()[0]
asc = ganita.set_lagna()[0]
print("\n\n   pdata  , asc "  , pdata , " : \n\n ", asc)
charttype = {"rasi" : 0 , "bhava" : 1, "navamsa" : 2}
chart = charttype["rasi"]
maha = ganita.mahapurusha(chart)
print("\n Maha ", maha)
"""
"""ubayachari = ganita.suriya_yoga(chart)
if ubayachari is None or ubayachari != [0,1,0]:
    vasi = ganita.vasi_yoga(chart)
    vesi = ganita.vesi_yoga(chart)
ganita.vasi_yoga(chart)
print("\n  vesi , vasi , ubayachari ", vesi , " : ", vasi , "  : ",ubayachari)"""
#n = ganita.pakha(63.93,287.28)
#print("\n\n   pakha  :  ", n)

#vm.interdb()
#n = ganita.Sthanabala()
#p = n[0][int(n[1])-1]
#print(p)
#n = ganita.navamlagna()
#p = vm.interdb()
#s = ganita.Sthanabala()
#pn = ganita.planetary()[3]
#planet_rasi = ganita.planetary()[1]
#nrps = ganita.is_paap_kartari("6",planet_rasi)
#print("\n\n   Venus paap kartari ", nrps)
"""su = "1"
mo = "2"
ma = "3"
Ju = "5"
Sa = "7"
Ve = "6"
Ra = "8"
Ke = "9"
Sun = ganita.planet_property(su)
Moon = ganita.planet_property(mo)
Mars = ganita.planet_property(ma)
Jupiter = ganita.planet_property(Ju)
Saturn = ganita.planet_property(Sa)
Venus = ganita.planet_property(Ve)
Rahu = ganita.planet_property(Ra)
Ketu = ganita.planet_property(Ke)
print("\n\n Moon ", Moon)
print("\n\n Sun  ", Sun)
print("\n\n Mars ", Mars)
print("\n\n Jupiter ", Jupiter)
print("\n\n Saturn ", Saturn)
print("\n\n Venus ", Venus)
print("\n\n Rahu ", Rahu)
print("\n\n Ketu ", Ketu)"""
#print("\n\n Chandra Lagna  :  ", ans)
"""if "nopurpa" in p[3]:
    co1 = "lightblue"
else:
    co1 = "black"
if "nopurpa" in p[4]:
    co2 = "lightblue"
else:
    co2 = "black"
if "nopurpa" in p[5]:
    co3 = "lightblue"
else:
    co3 = "black"
print("\n\n  Sthana ", s[0][int(s[1])-1] )  
if "bad" in p[6]:
    print("\n\n   0 mark ")   
if "mixed" in p[6]:
    print("\n\n   1/8 marks ")
if "good" in p[6]:
    print("\n\n   1/4 marks")
print("\n\n navamsalagna  :  ", type(n), "  :  ", n)
print("\n   S val ", s)
print("\n   np val  ", pn)"""
"""
#ganita.local_standard_time()
#model.get_chart()

#test.rasi_check(1) #Original Rasi
#test.rasi_check(3) #Navam Rasi
#test.graph_val()
#test.graph_tool()
date = [31,1,1996]
time = [23,5,0]
Moon = 63.93
data = dosha.dosha_entry(date,time,Moon)"""

#Data = dosha.first_dosha_calculator(date,time,Moon)
#print("\n\n dosha _ entry ", data[1])

"""score = dosha.dosha_effect(data[0],data[1])
dosha.dosha_graph(score,data[2],data[3])"""

#test.computing()


# python Kivy02/vedicware/Model/model.py
#data = test.view_model.get_town_loc()
#print(data)
#test.view_model.test()

#test.get_default_user_data()
#test.get_default_user_data()
#json_list = test.get_default_user_data()
#pprint.pprint(json_list)
#lister = ["+6.5","23","05","00","PM"]
#test.set_time(lister)
#n = test.get_offset()
#print(n)

path = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/city_loc.json"

path_town_name = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/town_name.json"

path_region_name = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/region_name.json"

path_region_town = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/region_town.json"

pathx = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/townships_list.xlsx"

path_town = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/town_loc.json"

path_RT = "/storage/emulated/0/Kivy02/vedicware/Model/Database/Loc_DB/region_town_loc.json"
#Initialize Nominatim geocoder

def load_RT(*args,**kwargs):
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        for k,v in data.items():
            if len(v) > 2:
                print("      ", k)
                
#load_RT()   

def town_match_RT(*args): #town_loc_define
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        temp = {}
        i = 0
    for k,v in data.items():
                temp[i+1] = [v[2],v[3]]
                i+=1
    with open(path_town,"w") as fw:
        json.dump(temp,fw,indent=4)
        print("\n\n  temp  ",temp)
        print("\n\n  temp ", len(temp))
        print("\n\n  data  ", len(data))
        
#town_match_RT()
def town_name_match_RT(*args): #town_name_define
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        temp = {}
        i = 0
    for k,v in data.items():
                temp[i+1] = v[1]
                i+=1
    with open(path_town_name,"w") as fw:
        json.dump(temp,fw,indent=4)
        print("\n\n  temp  ",temp)
        print("\n\n  temp ", len(temp))
        print("\n\n  data  ", len(data))

#town_name_match_RT()
 
def region_name(*args):
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        temp = {}
        dic = {}
        lister = []
        i = 0
    for k,v in data.items():
                lister.append(i+1)
                temp[v[0]] = len(lister)
                i+=1
    print(temp)
    i = 0
    for a,b in temp.items():
        dic[str(i+1)] = a
        i+=1
    print("\n\n", dic)
    with open(path_region_name,"w") as fw:
        json.dump(dic,fw,indent=4)
        #print("\n\n  temp  ",temp)
        #print("\n\n  temp ", len(temp))
        #print("\n\n  data  ", len(data))

#region_name()

def region_town_list(*args):
    templist = []
    tempdict = {}
    with open(path_RT,"r") as fr:
          base = json.load(fr)
    with open(path_region_name,"r") as f:
          mass = json.load(f)
    for k,v in mass.items():
        for key,val in base.items():
                    if v == val[0]:
                        templist.append(key)
        tempdict[k] = templist
        templist = []
    print(tempdict)
    with open(path_region_town,"w") as file:
          json.dump(tempdict,file,indent=2)

#region_town_list()
                   
def town_len(*args):
    with open(path_town,"r") as fr:
        data = json.load(fr)
        print("\n\n    town loc   : ", len(data))
def RT_len(*args):
                with open(path_RT,"r") as fr:
                    data = json.load(fr)
                    print("\n\n  region town loc  :  ", len(data))



#RT_len()                                
#town_len()

def extract_region_RT(*args):
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        temp = {}
        templist = []
        i = 1
        for k,v in data.items():
                     temp[v[0]] = str(i)
                     i+=1
        for k,v in temp.items():
            templist.append(k)
        print(templist)
#extract_region_RT()                     

citylist = ["Yangon",
"Sittwe",
"Mawlamyine",
"Pathein",
"Magway",
"Mandalay",
"Naypyidaw",
"Hinthada",
"Thanlyin",
"Pyay",
"Taungoo",
"Pyin Oo Lwin",
"Meiktila",
"Taunggyi",
"Myeik",
"Lashio",
"Hakha",
"Taungdwingyi",
"Myitkyina",
"Hpa-An",
"Mogok",
"Bago",
"Pakokku",
"Letpadan",
"Myawaddy",
"Katha",
"Bhamo",
"Shwebo",
"Phyu",
"Sagaing",
"Labutta",
"Gyobingauk",
"Keng Tung",
"Kanbalu",
"Hsipaw",
"Maubin",
"Bogale",
"Minbu",
"Kyaiklat",
"Nyaunglebin",
"Tachileik",
"Kale",
"Kyaukme",
"Yesagyo",
"Muse",
"Pantanaw",
"Tangyan",
"Tamu",
"Mohnyin",
"Hopin",
"Namhkam"]

def town_loc_format_retrieve(*args,**kwargs):
    try:
        with open(path_town,"r") as fr:
            data = json.load(fr)
            print(data)
    except Exception as e:
        print("Retrieve Error ! ")

def dictval_2_list(dict,*args,**kwargs):
    templist = []
    for k,v in dict.items():
        templist.append(v)
    return templist

def city_loc(city,loc,*args,**kwargs):
		try:
		    with open(path,"r") as fr:
		        data = json.load(fr)
		        for k,v in data.items():
		             	if k == city:
		             	    data[k] = loc
		    with open(path,"w") as fw:
		        json.dump(data,fw,indent=4)
		        print(len(data))	        
		except Exception as e:
		    print("Something wrong R ! ")
		    
def town_loc_format(townlist,*args,**kwargs):
    tempdict = {}
    default = ["1°E,1°N"]
    for town in townlist:
        tempdict[town] = default    
    try:
        with open(path_town,"w") as fw:
            json.dump(tempdict,fw,indent=4)
    except Exception as e:
        print("Something wrong in Write format ! ")

"""
geolocator = Nominatim(user_agent="my_geocoder")
city = ["Kawa"]
for town in city:
    try:
        location = geolocator.geocode(f"{town},Bago Region, Myanmar")
        if location:
            print(f"{city}")           
            print("Latitude:", location.latitude)
            print("Longitude:", location.longitude,"\n\n")
            lat = location.latitude
            lon = location.longitude
            loc = [str(lon)+"°E",str(lat)+"°N"]
            city_loc(city,loc)
        else:
           print("Location not found.")
    except Exception as e:
        print("No Sufficient Connection")
        break"""




def townlist(*args,**kwargs):
    townlist = pd.read_excel(pathx,usecols=[4],nrows=331).squeeze().tolist()
    return townlist
    
def regionlist(*args,**kwargs):
    regionlist = pd.read_excel(pathx,usecols=[2],nrows=331).squeeze().tolist()
    return regionlist

def regiontownlists(*args,**kwargs):
    tempre = []
    tempto = []
    with open(path_RT,"r") as fr:
        data = json.load(fr)
        for k,v in data.items():
            tempre.append(v[0])
            tempto.append(v[1])
        return [tempre,tempto]

#regiontown = regiontownlists()
#ReList = regiontown[0]
#TList = regiontown[1]
#print(TList)
def town_loc(ReList,TList,*args,**kwargs):
    geolocator = Nominatim(user_agent="my_geocoder")
    with open(path_RT,"r") as fr:
        data = json.load(fr)
    for re,tn in zip(ReList,TList):
        try:
            location = geolocator.geocode(f"{re},{tn},Myanmar")
            if location:
                lon = str(location.longitude)+"°E"
                lat = str(location.latitude)+"°N"
                for k,v in data.items():
                    if v[0] == re and v[1] == tn:
                        if len(v) > 2:
                            print("\n\n    Already had been  : ",v[2],"\n\n")
                        else:
                            print(data[k])
                            v.append(lon)
                            v.append(lat)
                            data[k] = v
                            print(data[k])
                            with open(path_RT,"w") as fw:
                                json.dump(data,fw,indent=4)
        except Exception as e:
            print(f"Con err {e}")

#town_loc(ReList[120:],TList[120:]) 
                    
        
    
    


"""regiontowndict = region_n_town(pathx)
print(regiontowndict)
townlist = dictval_2_list(regiontowndict)
town_loc_format(townlist)
town_loc_format_retrieve()"""

def regiontowndict(regionlist,townlist,*args,**kwargs):
    tempdict = {}
    for region,town in zip(regionlist,townlist):
        tempdict[region] = town
    #print(tempdict)
    return tempdict
       
def regiontown_write(*args,**kwargs):
    tempdict = {}
    try:
        with open(path_RT,"r") as fr:
            data = json.load(fr)
        with open(path_RT,"w") as fw:
            i=0
            for info in data:
                i+=1
                tempdict[str(i)]=info
            json.dump(tempdict,fw,indent=4)
    except Exception as e:
        print(f"Writing Region Town JSON err {e}!")

def region_write(list,*args,**kwargs):
    try:
        with open(path_RT,"w") as fw:
            json.dump(list,fw,indent=4)
    except Exception as e:
        print(f"Writing Region JSON err{e} !")
        
def region_town_format(regionlist,townlist,*args,**kwargs):
    templist = []
    try:
            with open(path_RT,"w") as fw:
                for region,town in zip(regionlist,townlist):
                    templist.append([region,town])
                json.dump(templist,fw,indent=4)
                return templist
    except Exception as e:
        print(f"Retrieve Region Town Format err {e} ! ")

#townlist = townlist()#Step - 1
#print(townlist)
#town_loc_format(townlist)
#town_loc_format_retrieve()
#regionlist = regionlist()#Step - 2
#print(regionlist)
#region_write(regionlist)

#RTdict = regiontowndict(regionlist,townlist)
#print(RTdict)

#RTlist = region_town_format(regionlist,townlist)#Step - 3
#print(RTlist)
#regiontown_write()#Step - 4

"""tempkey = []
tempvalues = []
with open(path_region_town,"r") as f:
    data = json.load(f)
#print(data)
for keys,values in data.items():
    tempkey.append(keys)
print(tempkey)

for keys,values in data.items():
    tempvalues.append(values)
print(tempvalues)"""