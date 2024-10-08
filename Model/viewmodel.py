import os
import json

class ViewModel:
    def __init__(self,model,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.parent = model
        self._DB = self.parent.get_db()
        self._db = os.path.join(self._DB,"Loc_DB")
        self._inter = os.path.join(self._DB,"Inter_DB")
        self._region_town = os.path.join(self._db,"region_town.json")
        self._region_name = os.path.join(self._db,"region_name.json")
        self._town_name = os.path.join(self._db,"town_name.json")
        self._town_loc = os.path.join(self._db,"town_loc.json")
        self._sthanabala = os.path.join(self._inter,"Sthanabala")
        self._chartpath = self._sthanabala
     
    def get_inter(self,*args):
        return self._inter
    def get_chartpath(self,*args):
        return self._chartpath
    def get_region_town(self,*args):
           with open(self._region_town,"r") as fr:
               data = json.load(fr)
           return data
           
    def get_region_name(self,*args):
        with open(self._region_name,"r") as fr:
            data = json.load(fr)
        return data
    
    def get_town_name(self,*args):
        with open(self._town_name,"r") as fr:
            data = json.load(fr)
        return data
    
    def get_town_loc(self,*args):
       with open(self._town_loc,"r") as fr:
           data = json.load(fr)
       return data
    
                                 
    def vision(self,*args):
        v = os.path.join(self._inter,"vision.jpg")
        return v
    
    def introduction(self,*args):
        intro = os.path.join(self._inter,"intro.jpg")
        lagna = os.path.join(self._inter,"lagna.jpg")
        chandra = os.path.join(self._inter,"chandra.jpg")
        suriya = os.path.join(self._inter,"suriya.jpg")
        return intro,lagna,chandra,suriya
    
    def get_sthanabala(self,*args):
        return self._sthanabala
        
    def interdb(self,*args):
        data = os.path.join(self._inter,"lagna")
        lagna = self.parent.ganita_model.set_lagna()
        lagna_img = str(lagna[1])+".jpg"
        path = os.path.join(data,lagna_img)
        print("lagna img : ", path)
        
        planetary = self.parent.ganita_model.planetary()
        nakdata = os.path.join(self._inter,"nakshatra")
        nak = planetary[9]
        nak_img = nak["2"]+".jpg"
        pathnak = os.path.join(nakdata,nak_img)
        
        rasidict = planetary[1]
        su,mo,ma,me,ju,ve,sa,ra,ke = rasidict["1"],rasidict["2"],rasidict["3"],rasidict["4"],rasidict["5"],rasidict["6"],rasidict["7"],rasidict["8"],rasidict["9"]
        su,mo,ma,me,ju,ve,sa,ra,ke = str(su),str(mo),str(ma),str(me),str(ju),str(ve),str(sa),str(ra),str(ke)
                                
        lagna_rasi = os.path.join(self._inter,"lagna_rasi")
        rasi_lagna = os.path.join(lagna_rasi,str(lagna[1]))
        lagna_planet = os.path.join(rasi_lagna,"1")
        planet_rasi = os.path.join(lagna_planet,su)
        
        rasi_img= planet_rasi+".jpg"
        pathrasi = os.path.join(planet_rasi,rasi_img)
        print(pathrasi)
        
        navlagna = ["bla"]
        navlagna.append(self.parent.ganita_model.navam_no_finder())
        rasi_purpakatri = self.purpa(data,planetary[1],lagna,0)
        bhava_purpakatri = self.purpa(data,planetary[4],lagna,1)
        nav_purpakatri = self.purpa(data,planetary[3],navlagna,2)
        
        lg_deg = lagna[2]
        lg_no = str( lagna[1] )
        lagna_party = { "1" : "sara" ,
        "2" : "htira",
        "3" : "dwedaha",
        "4" : "sara",
        "5" : "htira",
        "6" : "dwedaha",
        "7" : "sara",
        "8" : "htira",
        "9" : "dwedaha",
        "10" : "sara",
        "11" : "htira",
        "12" : "dwedaha" } 
        sara = {"good" : 10 ,
        "mixed" : 20,
        "bad" : 30 } 
        htira = {"good" : 20 , 
        "mixed" : 30,
        "bad": 10}
        dwedaha = {"good" : 30,
        "mixed" : 20,
        "bad" : 10} 
        nature = 0
        if lagna_party[lg_no] == "sara" :
            for n in sara:
                deg = sara[n] - lg_deg 
                if deg < 10 :
                    nature = n 
                    break
            
        if lagna_party[lg_no] == "htira" :
            for n in htira:
                deg = htira[n] - lg_deg 
                if deg < 10 :
                    nature = n 
                    break
        if lagna_party[lg_no] == "dwedaha" :
            for n in dwedaha:
                deg = dwedaha[n] - lg_deg 
                if deg <= 10 :
                    nature = n 
                    break
        print("\n    nature  " , nature )
        tring = lagna_party[lg_no]+"_"+nature+".jpg"
        print("\n   tring   : ", tring)
        tring = os.path.join(data,tring)
        return path,pathnak,pathrasi,rasi_purpakatri,bhava_purpakatri,nav_purpakatri,tring
        
    def purpa(self,data,planetary,lagna,index):
        bhava = planetary
        temp = []
        print("\n\n    lagna rasi " , lagna[1])
        init = lagna[1] + 1
        desti = lagna[1] +11
        if init > 12:
            init -= 12
        if desti > 12:
            desti -= 12
        purpa = ["1","3","7","8","9"]
        for p in purpa:
                if bhava[p] == str(init):
                    temp.append(p)
                    print("\n str(init) ", init)
                    break
        if len(temp) > 0:
                for p in purpa:
                    print("\n  purpa : ", p)
                    print("\n bhava[p] ", bhava[p] , "  : p :   ", p)
                    print("\n  bhava " , bhava)
                    if bhava[p] == str(desti):
                        temp.append(p)
                        print("\n  desti ", desti)
                        print("\n temp ", temp)
                        break
        nopurpa = ["nopurpa_rasi.jpg","nopurpa_bhava.jpg","nopurpa_nav.jpg"]
        purpa = ["purpa_rasi.jpg","purpa_bhava.jpg","purpa_nav.jpg"]
        
                
        if len(temp) < 2:
            purpakatri = os.path.join(data,nopurpa[index])
            print("\n   temp  ", temp, "  :  len(temp)", len(temp))
            print("\n   purpakatri   ", purpakatri)
        if len(temp) >= 2 :
            purpakatri = os.path.join(data,purpa[index])
            print("\n  purpakatri   ", purpakatri)
            print("\n   rasi ", planetary)
            print("\n temp  ", temp)
        return purpakatri
    
    
    def tester(self,*args):
        return self.parent.get_default_user_data()
        
    







        