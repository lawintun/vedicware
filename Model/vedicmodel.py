#import pandas as pd
import os,json
import matplotlib.pyplot as plt
import mplcyberpunk
from datetime import datetime,timedelta
import re
import swisseph as swe
import datetime
import math
from decimal import Decimal, getcontext

class GanitaModel:
    def __init__(self,model,*args,**kwargs):
        super(GanitaModel,self).__init__(*args,**kwargs)
        self.parent = model
        self.cousin = VedicModel(self.parent)
        self._DB = self.parent.get_db()
        self._vedic = os.path.join(self._DB,"Vedic_DB")
        self._user = os.path.join(self._DB,"User_DB")
        self._ephe = os.path.join(self._vedic,"ephe")
        self._inter = os.path.join(self._DB,"Inter_DB")
        self.Uchacha = { "1" : "1", "2" : "2" , "3" : "10", "4" : "6" , "5" : "4" , "6" : "12" , "7" : "7" , "8" : "8" , "9" : "2" }
        self.Moola = {"1" : "5" , "2" : "2" , "3" : "1" , "4" : "6" , "5" : "9", "6" : "7", "7" : "11" , "8" : "" , "9" : "" }
        self.Own = {"1" : ["5"], "2" : [ "4" ], "3": ["1","8"] , "4" : ["3","6"], "5" : ["9","12"] , "6" : [ "2","7"], "7" : [ "10","11"], "8" : ["3","6"], "9" : [ "9","12"]} 
        self.Neecha = { "1" : "7" , "2": "8", "3" : "4", "4" : "12", "5" : "10", "6" : "6", "7" : "1", "8" : "2" , "9" : "8" }
        self.UN_degree = { "1" : 10, "2" : 3 , "3" : 28, "4" : 15 , "5" : 7  , "6" : 20, "7" : 20 , "8" : 20 , "9" : 20 }
        self.Moola_range = { "1" : [1,10], "2": [4,20], "3" : [0,12], "4" : [16,20], "5" : [0,10], "6" : [0,15], "7" : [0,20], "8" : [0,30], "9" : [0,30]}
        self.Friend = {"1" :[ "1","3","4","6","8","9","12"], "2" : ["1","5","8","9","12"], "3":["5","9","12"], "4" : ["2","4","7","10","11"], "5" : ["1","5","8"], "6" : ["3","6","10","11"], "7" : [ "2","7"] , "8" : ["2","7","10","11"],"9":["2","7","10","11"]}
        self.Neutral = {"1" : [""], "2":[""], "3" : ["2","4","7"], "4":[""], "5":["2","3","4","6","7","10","11"], "6" : ["1","4","8"], "7": ["1","3","4","6","8","9","12"], "8":["3","6","9","12"], "9":["3","6","9","12"] }
        self.Lord = {"1": "3", "2" : "6", "3" : "4" ,"4" : "2" , "5" : "1" , "6" : "4", "7" : "6", "8" :"3", "9" : "5", "10":"7","11":"7","12":"5"}
        self.Speed = { "1" : 1,  "2" : 13.18 , "3" : 0.52, "4" : 1.23 , "5" : 0.08, "6" : 1.6 , "7" : 0.03 , "8" : 0.03, "9" : 0.05 } 
        self.Aspect = { "1" : [6] , "2"  : [6] , "3" : [3,6,7] , "4" : [6] , "5" : [4,6,8] , "6" : [6] , "7" : [2,6,9] , "8" : [4,6,8] } 


    def balagraph(self,*args,**kwargs):
        pdata = self.planetary()
        rasibala = []
        navbala = []
        for p in range(9):
            p += 1
            sp = str(p)
            temp = self.planet_property(sp)
            rasi = temp[3]
            nav = temp[4]
            rasibala.append(rasi)
            navbala.append(nav)
        print(rasibala,navbala)
        
    def dhana_effect(self,chart,*args,**kwargs):
        dhana = self.dhana_yoga(chart)
        asc = self.set_lagna()[1]
        yuti = dhana[2]
        yuti2 = yuti
        parashari = dhana[0]
        hrh = self.house_rasi_house(asc)
        house_rasi = hrh[0]
        if yuti:
            if yuti != {}:
                for p,lister in yuti.items():
                    rasi = house_rasi[p]
                    lord = self.Lord[rasi]
                    checker = self.planet_property(lord)[3]
                    if checker in ["e","n-","n-","n+"]:
                        for conp,i in zip( lister,range(len(lister))):
                            yuti[p][i] = "noeffect"
                    for conp,i in zip(lister,range(len(lister))):
                        if conp != "noeffect":
                            pro = self.planet_property(self.Lord[house_rasi[conp]])[3]
                            if pro in ["e","n","n-","n+"]:
                                yuti[p][i] = "noeffect"
                            else:
                                if yuti[p][i] != "noeffect":
                                    yuti[p][i] = "effect"
        if parashari:
            if parashari != {}:
                for hL in parashari:
                       r = house_rasi[hL]    
                       lord = self.Lord[r]  
                       pro = self.planet_property(lord)[3]
                       if pro in ["e","n","n-","n+"]:
                           parashari[hL] = "noeffect"
                       else:
                           parashari[hL] = "effect"
        return yuti,parashari               
                
    
    def dhana_yoga(self,chart,*args,**kwargs):
        asc = self.set_lagna()[1]
        ascstr = str(asc)
        ascint = int(asc)
        if chart == "rasi":
              idx = 1
        if chart == "bhava":
              idx =   4
        if chart == "navam":
              idx = 3
              asc = self.navam_no_finder()
              ascstr = str(asc)
              ascint = int(asc)
        pdata = self.planetary()[idx]
        hrh = self.house_rasi_house(ascstr)
        house_rasi = hrh[0]
        rasi_house = hrh[1]
        #1,2,5,9,11
        Lord = self.Lord[house_rasi["1"]]
        secLord = self.Lord[house_rasi["2"]]
        fivLord = self.Lord[house_rasi["5"]]
        ninLord = self.Lord[house_rasi["9"]]
        levLord = self.Lord[house_rasi["11"]]
        H_1 = house_rasi["1"]
        H_2 = house_rasi["2"]
        H_5 = house_rasi["5"]
        H_9 = house_rasi["9"]
        H_11 = house_rasi["11"]
        parashari = {}
        
        #2 
        Hobj = [ H_1,H_2,H_5,H_9,H_11]
        Hobj2 = [H_2,H_11]
        for p,r in pdata.items():
            if p == secLord:
                if r in Hobj:
                    house = rasi_house[r]
                    parashari["2"] = house
            if p == levLord:
                if r in Hobj:
                    house = rasi_house[r]
                    parashari["11"] = house
            if p == fivLord:
                if r in Hobj2:
                    house = rasi_house[r]
                    parashari["5"] = house
            if p == ninLord:
                if r in Hobj2:
                    house = rasi_house[r]
                    parashari["9"] = house
            if p == Lord:
                if r in Hobj2:
                    house = rasi_house[r]
                    parashari["1"] = house
        #parivartana
        parivartana = {}
        for p,h in parashari.items():
            if h in parashari and p in parashari.values():
                if (h,p) in parashari.items():
                    if h != p:
                       parivartana[p] = h
        if parashari == {}:
            parashari = None
        if parivartana == {}:
            parivartana = None
        secLord_pos = pdata[secLord]
        Lord_pos = pdata[Lord]
        levLord_pos = pdata[levLord]
        fivLord_pos = pdata[fivLord]
        ninLord_pos = pdata[ninLord]
        
        objH = {
        "1" : Lord,
        "2" : secLord,
        "5" : fivLord,
        "9" : ninLord,
        "11" : levLord
        }
        #yuti
        yuti = {}
        secConjoin = []
        for p , r in pdata.items():
                #if not rasi_house[r] in ["8","12"]: 
                    if r == secLord_pos and secLord != p:
                        if p != "9" or p != "8":
                            secConjoin.append(p)
        LH = {}
        for p in range(7):
              p += 1
              p = str(p)
              LH[p] = []
        for L,H in LH.items():
              for r,p in self.Lord.items():
                  if L == p:
                      LH[L].append(rasi_house[r])          
              
                        
                        
        newsecConjoin = []
        for c,i in zip(secConjoin,range(len(secConjoin))):
            if c in LH:
                temp = LH[c]
                for t in temp:
                    if t in objH:
                        newsecConjoin.append(t)
        
                                    
        levConjoin = []
        for p , r in pdata.items():
                #if not rasi_house[r] in ["8","12"]:
                    if r == levLord_pos and levLord != p:
                        if p != "9" or p != "8":
                            levConjoin.append(p)
        newlevConjoin = []
        for c,i in zip(levConjoin,range(len(levConjoin))):
            if c in LH:
                temp = LH[c]
                for t in temp:
                    if t in objH:
                        newlevConjoin.append(t)
            
            
        if newlevConjoin != []:
                yuti["11"] = newlevConjoin
        if newsecConjoin != []:
            yuti["2"] = newsecConjoin
        if yuti == {}:
            yuti = None
        return parashari,parivartana,yuti
              
    def arihta(self,chart,lagna,chandra,suriya,*args,**kwargs):
        asc = self.set_lagna()[1]
        
        if chart == "rasi" :
            idx = 1
        if chart == "bhava":
            idx = 4
        if chart == "navam":
            idx = 3 
        if idx == 3:
            asc =self.navam_no_finder()
        pdata = self.planetary()[idx]
        hrh = self.house_rasi_house(asc)
        house_rasi = hrh[0]
        rasi_house = hrh[1]
        asc = str(asc)
        arihta = [0,0,0,0,0,0,0,0,0,0,0,0]
        ascLord = self.Lord[asc]
        ascrasi = pdata[ascLord] 
        if rasi_house[ascrasi] in ["6","8","12"]:
            arihta[0] = 1 #lagna in 6,8,12 houses
            
        twopaap_h1 = 0
        for paap in ["1","3","7","8","9"]:
            if pdata[paap] == asc:
                twopaap_h1 += 1
        twopaap_h5 = 0
        for paap in ["1","3","7","8","9"]:
            if pdata[paap] == house_rasi["5"]:
                twopaap_h5 += 1
        
        if (lagna < 50 and chandra < 50) or (chandra < 50 and suriya < 50) or (lagna < 50 and suriya < 50):
            if twopaap_h1 > 1 or twopaap_h5 > 1:
                arihta[1] = 1
        if rasi_house[pdata["2"]] in ["6","8","12"]:
            arihta[11] = 1
        aspect = {"3": [3,6,7], "7" : [2,6,9], "8" :[4,6,8]}
        ma_asp = []
        ra_asp = []
        sa_asp = []
        for pasp,house in aspect.items():
            if paap == "3":
                for h in house:
                    rasi = int(pdata["3"]) + h
                    if rasi > 12:
                        rasi -= 12
                    ma_asp.append(str(rasi))
            if paap == "7":
                for h in house:
                    rasi = int(pdata["7"])+h
                    if rasi > 12:
                        rasi -= 12
                    sa_asp.append(str(rasi))
            if paap == "8":
                for h in house:
                    rasi = int(pdata["8"]) + h
                    if rasi > 12:
                        rasi -= 12
                    ra_asp.append(str(rasi))
            
        
        if chandra < 50:
            for paap in ["1","3","7","9","8"]:
                 if pdata[paap] == pdata["2"]:
                     arihta[2] = 1
                     break
            for h in ["6","8","12"]:
                if h == rasi_house[pdata["2"]]:
                    arihta[3] = 1
                    break 
            for asp in sa_asp:
                if asp == pdata["2"]:
                    arihta[4] = 1
                    break
            for asp in ra_asp:
                if asp == pdata["2"]:
                    arihta[5] = 1
                    break            
            for asp in ma_asp:
                if  asp == pdata["2"] :
                    arihta[6] = 1
                    break
            
        if lagna < 50:
            asc = str(asc)
            for paap in ["1","3","7","8","9"]:
                if pdata[paap] == pdata[self.Lord[asc]]:
                    arihta[7] = 1
                    break
            for asp in sa_asp:
                if asp == pdata[self.Lord[asc]]:
                    arihta[8] = 1
                    break
            for asp in ra_asp:
                if asp == pdata[self.Lord[asc]]:
                    arihta[9] = 1
                    break            
            for asp in ma_asp:
                if  asp == pdata[self.Lord[asc]] :
                    arihta[10] = 1
                    break
        score = 0
        for s in arihta:
            score += s
        if score > 1:
            return True
        else:
            return False
        
    def bandhana(self,chart,*args,**kwargs):
        if chart == "rasi":
            idx = 1
        if chart == "bhava":
            idx = 4
        if chart == "navam":
            idx = 3
        pdata = self.planetary()[idx]
        asc = self.set_lagna()[1]
        if idx == 3:
            asc = self.navam_no_finder()
        #G
        hrh = self.house_rasi_house(asc)
        house_rasi = hrh[0]
        rasi_house = hrh[1]
        asc = str(asc)
        #G1
        #paap in H12
        agent = [0,0,0]
        for paap in ["1","3","7","8","9"]:
            rasi = pdata[paap] 
            house = rasi_house[rasi]
            if house == "12":
                agent[0] = 1
                break 
        #paap in H2,H5&H9
        partial_agent = [0,0,0]
        for paap in ["1","3","7","8","9"]:
            rasi = pdata[paap]
            house = rasi_house[rasi]
            if house in ["2"]:
                partial_agent[0] = 1
            if house == "5":
                partial_agent[1] = 1
            if house == "9":
                partial_agent[2] = 1 
                
        if partial_agent == [1,1,1]:
             agent[1] = 1
        else:
            agent[1] = 0
        #Neech lord asp by 6L & 12L
        lord = self.Lord[asc]
        valid_agent = [0,0,0]
        neechlord = 0
        lordpro = self.planet_property(lord)
        if lordpro[3] in ["n","n-","n+","e"]:
            valid_agent[0] = 1
            neechlord = 1
            
        sixL = self.Lord[house_rasi["6"]]
        twelL = self.Lord[house_rasi["12"]]
        ascL = self.Lord[asc]
        Aspect = { "1" : [6] , "2" : [6] , "3" : [3,6,7] , "4" : [6] , "5": [4,6,8] , "6" : [6] , "7" : [2,6,9] , "8" : [4,6,8] }
        sixL_aspect = Aspect[sixL] 
        twelL_aspect = Aspect[twelL]
        
        for int_a in sixL_aspect:
            pos6L = pdata[sixL] #rasi
            posascL = pdata[ascL]
            asp_rasi = int(pos6L) + int_a
            if asp_rasi > 12:
                asp_rasi -= 12            
            str_asp_rasi = str(asp_rasi)
            if str_asp_rasi == posascL :
                valid_agent[1] = 1
                break
        for int_a in twelL_aspect:
            pos12L = pdata[twelL] #rasi
            posascL = pdata[ascL]
            asp_rasi = int(pos12L) + int_a
            if asp_rasi > 12:
                asp_rasi -= 12            
            str_asp_rasi = str(asp_rasi)
            if str_asp_rasi == posascL :
                valid_agent[2] = 1
                break
        if valid_agent == [1,1,1]:
                  agent[2] = 1
        else:
                  agent[2] = 0
                  
        #G2
        agent2 = [0,0,0,0,0]
        valid_agent2 = [0,0,0]
        if neechlord == 1:
            valid_agent2[0] = 1
        nineL = self.Lord[house_rasi["9"]]
        posnineL = pdata[nineL]
        postwelL = pdata[twelL]
        if posnineL == asc:
            valid_agent2[1] = 1
        if postwelL == asc:
            valid_agent2[2] = 1
        if valid_agent2 == [1,1,1]:
            agent2[0] = 1
        #Scissor Patterns 
        checker = self.is_scissor(pdata,rasi_house)
        if checker[0] == 1: #scissor 
            agent2[1] = 1
        if checker[1] == 1: #2,5,12 equal p
            agent2[2] = 1
        if ascL == pdata["7"] : #L+7
            agent2[3] = 1
            Lordpos = pdata[self.Lord[str(asc)]]
            if Lordpos == pdata[self.Lord[house_rasi["6"]]]:
                if Lordpos == pdata["8"] or str(asc) == pdata["9"] :
                    if Lordpos == pdata["7"]:
                        #ascLord+Sa+6L+(Ra or Ke)
                        agent2[4] = 1
        temp1 = 0
        temp2 = 0
        for a1 in agent:
            temp1 += a1
        for a2 in agent2:
            temp2 += a2
        if temp1 > 0 and temp2 > 0:
            return 100
        elif ( temp1 < 1 and temp2 == 1) or (temp1 == 1 and temp2 < 1):
            return 50 
        elif temp1 < 1 and temp2 < 1:
            return 0
        elif temp1 > 1 or temp2 > 1:
            return 100
        else:
            return 0
            
        
    
    def is_scissor(self,pdata,rasi_house,*args,**kwargs):
        scissor_house = {"2" : "12", "3" : "11" , "4" : "10" , "5" : "9" , "6" : "12" }
        lower_scissor = {"2" : [0] , "3" : [0] , "4" : [0] , "5" : [0], "6" : [0] }
        upper_scissor = {"12" : [0] , "11" : [0] , "10" : [0], "9" : [0]}
        for p,r in pdata.items():
            h = rasi_house[r]
            for Lh,Llist in lower_scissor.items():
                if h == Lh:
                    temp = Llist
                    Llist.append(1)
                    lower_scissor[Lh] = Llist
            for Uh,Ulist in upper_scissor.items():
                if h == Uh:
                    temp = Ulist
                    Ulist.append(1)
                    upper_scissor[Uh] = Ulist
        checker = [0,0]
        if len(lower_scissor["6"]) > 1 and len(upper_scissor["12"]) > 1:
            if len(lower_scissor["6"]) == len(upper_scissor["12"]):            
                checker[0] = 1
        for lower,upper in zip(lower_scissor,upper_scissor):
            if len(lower_scissor[lower]) > 1 and len(upper_scissor[upper]) > 1:
                if len(lower_scissor[lower]) == len(upper_scissor[upper]):
                    checker[0] = 1
        if len(lower_scissor["2"]) > 1 and len(lower_scissor["5"]) > 1 and len(upper_scissor["12"])> 12:
            if len(lower_scissor["2"]) ==  len(lower_scissor["5"]) and len(lower_scissor["2"] ) == len(upper_scissor["12"]):
                checker[1] = 1
        return checker
    
    def house_rasi_house(self,asc,*args,**kwargs):
        asc = int(asc)
        rasi_house = {}
        for i in range(12):
            n = str( i + 1)
            rasi_house[n] = None
          
        for h in range(12):
            h += 1
            rasi = h - asc +1
            if rasi < 0:
               rasi += 12
            if rasi == 0:
               rasi = 12
            rasi_house[str(h)] = str(rasi) #r : h
        house_rasi = {}
        for h,r in rasi_house.items(): #h : r 
            house_rasi[r] = h  
        return house_rasi,rasi_house   
    
    def parivartana_raja(self,*args,**kwargs):
        return self.kentri_raja()[2]
    
    def yuti_raja(self,*args,**kwargs):
        return self.kentri_raja()[1]
    
    def parashari_raja(self,*args,**kwargs):
        parashari = self.kentri_raja()[0]
        if parashari:
            if len(parashari) > 0:
                return parashari
            else:
                return None
        else:
            None
            
        

    def kentri_effect(self,*args,**kwargs):
           Data = self.kentri_raja()
           rasi_data = self.planetary()[1]
           asc = Data[4]
           rasi_house = Data[5]
           house_rasi = Data[6]
           parashari = Data[0]
           yuti = Data[1]
           lord_rasi = {}
           paraeffect = []
           if parashari:
               if parashari != []:
                   for HL in parashari: #HL to RL(planet)
                       RL = self.Lord[house_rasi[HL]]
                       pro = self.planet_property(RL)[3]
                       if pro in ["e","n","n-","n+"]:
                           paraeffect.append("noeffect")
                       else:
                           paraeffect.append("effect")         
           yutieffect = []
           if yuti:
               if yuti != []:
                   for ylist, i in zip( yuti,range(len(yuti))):
                       L1= ylist[0]
                       L2 = ylist[1]
                       RL1 = self.Lord[house_rasi[L1]]
                       RL2 = self.Lord[house_rasi[L2]]
                       p1pro = self.planet_property(RL1)[3]
                       p2pro = self.planet_property(RL2)[3]
                       if p1pro in ["e","n","n-","n+"] or p2pro in ["e","n","n+","n-"]:
                           yutieffect.append("noeffect")
                           
                              
                       else:
                           yutieffect.append("effect")
                       
                      
                                   
           
           return paraeffect,yutieffect
           
    def kentri_raja(self,*args,**kwargs):
        pdata = self.planetary()
        rasi_data = pdata[1]
        asc = int(self.set_lagna()[1])
        rasi_house = {}
        for i in range(12):
            n = str( i + 1)
            rasi_house[n] = None
          
        for h in range(12):
            h += 1
            rasi = h - asc +1
            if rasi < 0:
               rasi += 12
            if rasi == 0:
               rasi = 12
            rasi_house[str(h)] = str(rasi) #r : h
        house_rasi = {}
        for h,r in rasi_house.items(): #h : r 
            house_rasi[r] = h     
        Trikona_Lord = []
        Kendra_Lord = []   
        Trikona_Rasi = []
        Kendra_Rasi = []
        Tlord_house = {}
        Klord_house = {}
        for h,r in house_rasi.items():
            if h in ["5","9"] :
                Trikona_Rasi.append(r)
            if h in ["1","4","7","10"]:
                Kendra_Rasi.append(r)
        for tr in Trikona_Rasi:
            Trikona_Lord.append(self.Lord[tr])
            Tlord_house[self.Lord[tr]] = rasi_house[tr] #p : h 
        for kr in Kendra_Rasi:
            Kendra_Lord.append(self.Lord[kr])
            Klord_house[self.Lord[kr]] = rasi_house[kr] #p : h 
        
        parashari = []
        parivartana = {}
        for p,r in rasi_data.items():
                   if p in Trikona_Lord:
                       if r in Kendra_Rasi:
                          T = Tlord_house[p]
                          KH = rasi_house[r]
                          parivartana[T] = KH
                          parashari.append(T)
        for p,r in rasi_data.items():
             if p in Kendra_Lord:
                 if r in Trikona_Rasi:
                     K = Klord_house[p]
                     TH = rasi_house[r] 
                     parivartana[K] = TH
                     parashari.append(K)
        #parivartana
        PVRY = {}
        for p,h in parivartana.items():
            for pp in parivartana:
                if pp == h:
                    if len(PVRY) > 0:
                        if not h in PVRY:
                            PVRY[p] = h
                    else:
                        PVRY[p] = h
        parivartana_raja = None
        if PVRY:
            if len(PVRY) > 0:
                parivartana_raja = PVRY
        #yuti
        conjoin = []
        for p,r in rasi_data.items():
            if p in Trikona_Lord:
                for k,v in rasi_data.items():
                    if k in Kendra_Lord:
                        if r == v and k != p:
                            T = Tlord_house[p]
                            K = Klord_house[k]
                            if not rasi_house[r] in ["6","8","12"] :
                                
                                conjoin.append([T,K])
        yuti = None
        
        if conjoin:
            if len(conjoin) > 0:
                yuti = conjoin
        Confirm_PVRY =  {}
        if PVRY:
            for p,h in PVRY.items():
                if h in PVRY:
                    Confirm_PVRY[p] = h
        if Confirm_PVRY == {}:
                      Confirm_PVRY = None
                      
        return parashari, yuti, Confirm_PVRY, pdata,asc,rasi_house,house_rasi,parivartana
        #return parashari, Kendra_Rasi, house_rasi,asc
    
    def kemadruma(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        moon = int(rasi["2"])
        right = moon + 1
        left = moon -1
        if right > 12:
            right -= 12
        if left < 0:
            left += 12
        right , left = str(right),str(left)
        temp = []
        for p,r in rasi.items():
            if not p in ["1","8","9","2"]:
                temp.append(r)
        m = str(moon)
        def is_lonely(temp,m,right,left):
            if right in temp:
                return False
            elif m in temp:
                return False
            elif left in temp:
                return False
            else:
                return True
        checker = is_lonely(temp,m,right,left)
        # 1,8,9 
        kendra = []
        if checker is True:
            for k in [3,6,9]:
                k = moon + k
                if k > 12:
                    k -= 12
                k = str(k)
                for p,r in rasi.items():
                    if p in ["1","8","9"]: 
                        if r == k:
                            kendra.append(p)
            if kendra != []:
                    return True
            else:
                 return False
                 
        else:
            return checker        
        
        
        
    
    def vish(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        if rasi["7"] == rasi["2"]:
            return True
        else:
            return False
    
    def chandal(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        rahu_house = rasi["8"] 
        ketu_house = rasi["9"]
        chandal = []
        for p,h in rasi.items():
            if rahu_house == h:
                if p != "8":
                    chandal.append(p)
            if ketu_house == h:
                if p != "9":
                    chandal.append(p)
        return chandal
    
    def kalasarpa(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        rahu = rasi["8"]
        rahu= int(rahu)
        rightsemi = []
        leftsemi = []
        for p,h in rasi.items():
             h = int(h)
             d = rahu - h
             if d < 0:
                     d += 12
             if d < 6 and d != 0:
                 rightsemi.append(p)
             if d > 6:
                 leftsemi.append(p)
        #return leftsemi
        if leftsemi:
                if rightsemi:
                    return False
                else:
                    return True
        if rightsemi:
                if leftsemi:
                    return False
                else:
                    return True
                
        
    
    
    def gkryeffect(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        guru_rasi = rasi["5"]
        effect = "gkryeffect"
        neech = True
        is_neech = self.planet_property("5")[3]
        if is_neech in ["n","n+","n-"]:
            neech = True
        else:
            neech = False
        is_gkry = self.gkry()
        if is_gkry: 
            for paap in ["8","9","7"]:
                if rasi[paap] == guru_rasi:
                    effect = "nogkryeffect"
                    break
            if neech:
                effect = "nogkryeffect"
        return effect     
    
    def gkry(self,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        moon = rasi["2"]
        guru = rasi["5"]
        moon, guru = int(moon),int(guru)
        d = abs(moon - guru)
        score = [0,0,0]
        if d in [0,3,6,9]:
            score[0] = 1
        else:
            score[0] = 0
       
        for p in rasi:
            if rasi[p] == str(moon):
                if p in ["7","8","9"]:
                    score[1] = 0
                    break
                else:
                    score[1] = 1
            else:
                    score[1] = 1
                    
        
        for p in rasi:
            if rasi[p] == str(guru):
               if p in ["7","8","9"]:
                   score[2] = 0
                   break
               else:
                   score[2] = 1                 
            else:
                   score[2] = 1
                   
        if score == [1,1,1]:
                if rasi["5"] != "10" or rasi["2"] != "8":
                    return True
                else:
                    return False
        else:
            return False
        
    def vipreet(self,*args,**kwargs):
        pdata = self.planetary()
        asc = self.set_lagna()[1]
        asc = int(asc)
        rasi = pdata[1]
        vipreet = []
        Dusthana = [5,7,11]
        Dusthana_house = []
        for d in Dusthana:
            h = asc + d
            if h > 12:
                h -= 12
            Dusthana_house.append(str(h))
            
        for p,h in rasi.items():
             Ari_house = asc + 5 
             Randra_house = asc + 7
             Vaya_house = asc + 11
             if Ari_house > 12:
                 Ari_house -= 12
             if Randra_house > 12:
                 Randra_house -= 12
             if Vaya_house > 12:
                 Vaya_house -= 12
             if Ari_house == 0:
                 Ari_house = 1
             if Randra_house == 0:
                 Randra_house = 1
             if Vaya_house == 0:
                 Vaya_house = 1
        Ari_house,Randra_house,Vaya_house = str(Ari_house),str(Randra_house),str(Vaya_house)
        Ari_lord = self.Lord[Ari_house] 
        Randra_lord = self.Lord[Randra_house]
        Vaya_lord = self.Lord[Vaya_house]
        if rasi[Ari_lord] in Dusthana_house:
                 vipreet.append(1)
        else:
                 vipreet.append(0)
        if rasi[Randra_lord] in Dusthana_house:
                 vipreet.append(1)
        else:
                 vipreet.append(0)
        if rasi[Vaya_lord] in Dusthana_house:
                 vipreet.append(1)
        else:
                 vipreet.append(0)
        return vipreet
             
    def bhanga_raja(self,*args,**kwargs):
        #NBRY
        pdata = self.planetary()
        rasi = pdata[1]
        nbry_temp = []
        for p,h in rasi.items():
           checker = self.is_neech(p,h)
           if checker == True:
               nbry_temp.append(p)
        nbry_raja = {}
        for p in nbry_temp:
           nbry_raja[p] = self.is_nbry_raja(p)
        return_raja = []
        checksum = 0
        if nbry_raja:
               for p in nbry_raja:
                   if p != "2":
                      checksum = 0
                      for ck in nbry_raja[p]:
                          checksum += ck
                      if checksum > 2:
                           return_raja.append(p)
                   else:
                       nbry_raja[p][2] = 0
                       checksum = 0
                       for ck in nbry_raja[p]:
                           checksum += ck
                       if checksum >2:
                           return_raja.append(p)
        if "8" in return_raja:
            return_raja.remove("8")
        if "9" in return_raja:
            return_raja.remove("9")
        return return_raja
                       
                       
               
    def is_nbry_raja(self,target,*args,**kwargs):
        pdata = self.planetary()
        rasi = pdata[1]
        temp = []
        for p,h in rasi.items():
            temp.append(h)
        #NBRY
        
        #self nav     1
        inspector = self.is_nav_ucha(target,pdata)
        nbry_score = []
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
            
        #self lagna kendra 2
        asc = self.set_lagna()[1]
        inspector = self.is_self_kendra(target,rasi,asc)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
            
        #self moon kendra   3 (if moon cancel)
        asc = rasi["2"]   
        inspector = self.is_self_kendra(target,rasi,asc)  
        if inspector:
          nbry_score.append(1)
        else:
          nbry_score.append(0)
          
        #ucha lord kendra lagna 4
        asc = self.set_lagna()[1]
        inspector = self.is_un_lord_kendra(target,rasi,asc,self.Uchacha)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        
        #ucha lord kendra moon 5
        masc = rasi["2"]
        inspector = self.is_un_lord_kendra(target,rasi,masc,self.Uchacha)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #neech lord kendra lagna 6
        inspector = self.is_un_lord_kendra(target,rasi,asc,self.Neecha)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #neech lord kendra moon 7
        inspector = self.is_un_lord_kendra(target,rasi,masc,self.Neecha)
        if inspector :
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #ucha lord and neech lord mutual kendra 8
        inspector = self.is_mutual_kendra(target,rasi,self.Uchacha,self.Neecha)
        if inspector :
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #Ucha or neecha lord or ucha lord conjoin 9 
        inspector = self.is_conjoin_un(target,rasi)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #Neech lord aspect 10
        inspector = self.is_aspect_unlord(target,rasi,"n")
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        inspector = self.is_aspect_unlord(target,rasi,"u")
        #Uchacha lord aspect 11
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        #Uchacha of Neecha Rasi 12
        inspector = self.uOFn_kendra_aORm(target,rasi,asc)
        if inspector:
            nbry_score.append(1)
        else:
            nbry_score.append(0)
        
        return nbry_score
    
    def uOFn_kendra_aORm(self,p,rasi,asc,*args,**kwargs):
        asc = int(asc)
        masc = int(rasi["2"])
        neech_pos = rasi[p]
        uOFn = None
        for pp in self.Uchacha:
            if self.Uchacha[pp] == neech_pos:
                uOFn = pp
                print("\n uOFn ", pp)
        uOFn_pos = rasi[uOFn]
        kendra = [0,3,6,9]
        checker = []
        for k in kendra:
            mken = masc + k
            aken = asc +k 
            if aken > 12:
                aken -= 12
            if mken > 12:
                mken -= 12
            print("\n aken ", aken)
            print("\n mken ", mken)
            if uOFn_pos == str(aken):
                checker.append(1)
            elif uOFn_pos == str(mken):
                checker.append(1)
            else:
                pass
        if checker != []:
            return True
        else:
            return False
        
    
    def is_aspect_unlord(self,p,rasi,n,*args,**kwargs):
        if n == "n":
            undict = self.Neecha
        else:
            undict = self.Uchacha
        nR = undict[p]
        nL = self.Lord[nR]
        print("\n  nL ", nL)
        special_aspect = {"3" : [3,6,7],
        "5" : [4,6,8],
        "7" : [2,6,9],
        "9" : [2,6,9]}
        nL_pos = int(rasi[nL])
        print("\n nL_pos  ", nL_pos)
        p_pos = int(rasi[p])
        if nL in ["1","2","4","6"]:
            nL_asp = nL_pos+6
            if nL_asp > 12:
                nL_asp -=12
            nL_asp = str(nL_asp)
            if nL_asp == str(p_pos):
                return True
            else:
                return False
        else:
            asplist = special_aspect[nL]
            checker =[]
            for asp in asplist:
                nL_asp = int(nL_pos)+asp
                if nL_asp > 12:
                    nL_asp -= 12
                print("\n nL_asp ", nL_asp)
                if str(nL_asp) == str(p_pos):
                    checker.append(1)
            if checker != []:
                return True
            else:
                return False
        
    
    def is_conjoin_un(self,p,rasi,*args,**kwargs):
        conjoin = []
        for cp in rasi:
            if rasi[p] == rasi[cp]:
                conjoin.append(cp)
        checker = []
        print("\n\n conjoin ", conjoin)
        #if cp is neecha lord
        for cp in conjoin:
           h = rasi[p]
           if self.Lord[h] == cp:
               checker.append(1)
               break
        #if cp is uchacha lord
        for cp in conjoin:
            h = self.Uchacha[p]
            if self.Lord[h] == cp:
                checker.append(1)
                break
        #if cp is uchacha planet
        for cp in conjoin:
            h = self.Uchacha[cp]
            if h == rasi[p]:
                checker.append(1)
                break
        if checker:
            return True
        else:
            return False
       
        
    def is_mutual_kendra(self,p,rasi,u,n,*args,**kwargs):
        kendra = [0,3,6,9]
        h = u[p] 
        uLord = self.Lord[h]
        
        h2 = n[p]
        nLord = self.Lord[h2]
        
        nh = rasi[nLord] 
        uh = rasi[uLord]
        nh,uh = int(nh),int(uh)
        house = abs(uh - nh)
        if house in kendra:
            return True
            
        
        
            
            
    def is_un_lord_kendra(self,p,rasi,asc,un,*args,**kwargs):
        asc = int(asc)
        kendra = [0,3,6,9]
        Ucha_house = un[p] 
        Ucha_Lord = 0
        for h in self.Lord:
            if h == Ucha_house:
                Ucha_Lord = self.Lord[h]
        for k in kendra:
            h = asc + k
            if h > 12:
                h -= 12
            if rasi[Ucha_Lord] == str(h):
                return True
                break
            
            
        pass  
    def is_self_kendra(self,p,rasi,asc,*args,**kwargs):
        #self 
        asc = int(asc)
        kendra = [0,3,6,9]   
        for k in kendra:
            h = asc + k 
            if h > 12:
                h -= 12
            if rasi[p] == str(h):
                return True
                break
                
    def is_nav_ucha(self,p,pdata,*args,**kwargs):
           #self
           nav = pdata[3]
           if self.Uchacha[p] == nav[p] :
               return True
           else:
               return False
    def is_neech(self,p,h,*args,**kwargs):
             print(type(p)," : ",p," : ",type(h), h)
             if self.Neecha[p] == h:
                 return True
             else:
                 return False
            
               
    def tithi(self,*args,**kwargs):
        pdata = self.planetary()
        p = pdata[0]
        Sun,Moon = p["1"],p["2"]
        d = Moon - Sun
        if d < 0:
            d += 360
        tithi = int(( d/12) + 1)
        return tithi
        
    def mahapurusha(self,chart,*args,**kwargs):
        pdata = self.planetary()
        asc = self.set_lagna()[1]
        Nasc = self.navam_no_finder()
        lagna = 0
        Kendra = [0,3,6,9] #adder values 1,4,7,10
        Key = ["3","4","5","6","7"]
        if chart == 2:
            idx = 3 #nav
            lagna = Nasc
        if chart == 0:
            idx = 1 #rasi
            lagna = asc
        if chart == 1:
            idx = 4 #bhava
            lagna = asc
        data = pdata[idx]
        
        #potent planet
        yoga = {} #None
        for k in Key:
            if data[k] == self.Uchacha[k] or data[k] in self.Own[k]:
              yoga[k] = data[k]
        #from lagna
        lagna_maha = []
        lagna = int(lagna)
        for p,h in yoga.items():
            for k in Kendra:
                house = k + lagna
                if house > 12:
                    house -= 12
                if str(house) == h:
                    lagna_maha.append(p)
                    
        #from moon 
        moon_maha = []
        masc = data["2"] 
        masc= int(masc)
        for p,h in yoga.items():
            for k in Kendra:
                house = k + masc
                if house > 12:
                    house -= 12
                if str(house) == h:
                    moon_maha.append(p)
      
       
        #moon_maha checking
        all_destoryer = []
        hamsa_malavya_destoryer = []
        malavya_destoryer = []
        for dp,dh in data.items():
              if dp in ["1","7","8","9"]:
                 if dh == str(masc):
                     all_destoryer.append(1)
        for dp,dh in data.items():
            if dp in ["7","8","9"]:
                if dh == data["5"]:
                    hamsa_malavya_destoryer.append(1)
        for dp,dh in data.items():
            if dp is ["8","9"]:
                if dh == data["6"]:
                    malavya_destoryer.append(1)
        if all_destoryer:
            moon_maha = None
        if hamsa_malavya_destoryer:
            if moon_maha:
                if "5" in moon_maha:
                    moon_maha.remove("5")
            if moon_maha:
                if "6" in moon_maha:
                    moon_maha.remove("6")
        if malavya_destoryer:
            if moon_maha:
                if "6" in moon_maha:
                    moon_maha.remove("6")
            if lagna_maha:
                if "6" in lagna_maha:
                    lagna_maha.remove("6")
            
            
        #Union                            
        com_maha = None
        temp_moon_maha = moon_maha
        temp_lagna_maha = lagna_maha
        if lagna_maha:
            if moon_maha:
                com_maha = list(set(temp_lagna_maha).union(temp_moon_maha))
            else:
                com_maha = lagna_maha
        #Union
        if moon_maha:
           if lagna_maha:
               com_maha = list(set(temp_moon_maha).union(temp_lagna_maha))
           else:
               com_maha = moon_maha
               
       
        
                    
                
        return  com_maha         
            
        
              
        
        
        
    #house check for suriya yoga
    def suriya_house(self,chart,*args,**kwargs):
        pdata = self.planetary()
        if chart == 2:
            idx = 3 #nav
        if chart == 0:
            idx = 1 #rasi
        if chart == 1:
            idx = 4 #bhava
        data = pdata[idx]
        H = data["1"]
        HF = int(H) + 1
        HB = int(H) - 1
        if HF > 12:
            HF  -= 12
        HF = str(HF)
        if HB < 0:
            HB += 12
        HB = str(HB)
        front = []
        back = []
        house  = []
        for p in data:
            if data[p] == HF:
                front.append(p)
            if data[p] == HB:
                back.append(p)
            if data[p] == H:
                house.append(p)
        return front,house,back
        
    def veva_cond(self,house,spec_house):
            scout = []
            breaker = ["2","8","9"]
            if len(house) < 2 and len(spec_house)>0:
                  for b in breaker:
                           if b in spec_house:
                               print("\n breaker ", b)
                               scout.append(b)
                  if len(scout) > 0:
                           return None
                  else:
                      return spec_house
            else:
                           return None   
                           
    def vesi_yoga(self,chart,*args,**kwargs):
        data = self.suriya_house(chart)
        front,house = data[0],data[1]
        print("\n house ", house)
        print("\n front ", front)
        return self.veva_cond(house,front)
        
            
    def vasi_yoga(self,chart,*args,**kwargs):
        data = self.suriya_house(chart)
        house,back = data[1],data[2]
        print("\n back", back)
        print("\n  houze ", house)
        return self.veva_cond(house,back)
        
        
    #Ubayachari 
    def suriya_yoga(self,chart,*args,**kwargs):
        data = self.suriya_house(chart)
        front,house,back = data[0],data[1],data[2]
        #Vesi Ubayachari Vasi
        scout = [0,0,0]
        def escort(scout,front,back):
            if front and back:
                scout[1] = 1
                return scout 
            else:
                return scout
        def uba(scout,front,back,house):
            if escort(scout,front,back) == [0,1,0] :
                temp = []
                breaker = ["2","8","9"]
                for b in breaker:
                    if b in front or b in back or b in house:
                        temp.append(b)
                if temp:
                    if len(temp) > 0:
                        scout[1] = 0
                        return scout
                else:
                    return scout
            else: #to recheck
               scout[1] = 0
               return scout                            
        pioneer = escort(scout,front,back)
        pioneer = uba(pioneer,front,back,house)
        property = self.planet_property("1")
        if property[chart] == False and pioneer == [0,1,0]: #no paap kartari
            pioneer[1] = 1
            return pioneer
        else:
            if pioneer:
                pioneer[1] = 0
            return pioneer 
            
            
        
            
        
        
        
                
        
        
    
    def solareclipse(self,*args,**kwargs):
        pdata = self.planetary()
        Asc = self.set_lagna()[0]
        pdeg = pdata[0]
        Sun, Moon, Rahu = pdeg["1"],pdeg["2"],pdeg["8"]
        print("\n  Solar eclipse ", pdeg)
        inter = self._inter
        def solar_eclipse(Sun,Rahu,inter):
            d = Sun - Rahu
            print("\n   d  = Sun - Rahu ", d)
            if d < 0:
                d += 360
            if (d<195 and d >165) or (d>345 or d<15):
                D = Asc - Sun
                if D < 0:
                    D += 360
                if D > 180:
                    n = os.path.join(inter,"sen.jpg")
                    return n
                if D < 180 or D == 0:
                    n = os.path.join(inter,"sed.jpg")
                    return n
            else:
                    n = os.path.join(inter,"nose.jpg")
                    return n
                    
        d = Moon - Sun
        if d < 0:
           d += 360
        if d < 0.5 or d > 359.5:
           return solar_eclipse(Sun,Rahu,inter)
           print("\n\n Eclipse \n\n")
        if d < 359.5 and d > 0.5:
           n = os.path.join(self._inter,"nose.jpg")
           print("\n\n  No eclipse solar")
           return n
    def eclipse(self,*args,**kwargs):
       pdata = self.planetary()
       Asc = self.set_lagna()[0]
       pdeg = pdata[0] #dict
       Sun , Moon , Rahu = pdeg["1"], pdeg["2"], pdeg["8"]
       print("\n\n  Sun ", Sun ," :  Moon ",Moon)
       inter = self._inter
       def luner_eclipse(Sun,Rahu,inter):
           d = Sun - Rahu 
           if d < 0:
               d += 360
           if (d < 195 and d > 165) or (d>345 or d<15 ):               
               D = Asc - Sun
               if D < 0:
                   D += 360
               if D > 180:
                   n = os.path.join(self._inter,"len.jpg")
                   return n
               if D < 180 or D == 0:
                   n = os.path.join(self._inter,"led.jpg")
                   return n
           else:
               n = os.path.join(inter,"nole.jpg")
               return n
       
       d = Moon - Sun
       if d < 0:
           d += 360
       if d < 180.5 and d > 179.5 :
       #if d == 180:
           return luner_eclipse(Sun,Rahu,inter)
           
       if d < 179.5 or d > 180.5 :
       #if not d == 180:
           n = os.path.join(self._inter,"nole.jpg")
           return n
           
       
       
       
    def aspect(self,*args,**kwargs):
        pdata = self.planetary()
        Asc = self.set_lagna()
        bhava = pdata[4]
        lagna_rasi_degree = Asc[2]
        planet_rasi_degree = pdata[2]
        aspect = {}
        for p in bhava:
            if p == "9":
                break
            hi = bhava[p]
            temp = []
            for a in self.Aspect[p]:
                hf = int(hi)  + a
                if hf > 12:
                    hf -= 12 
                temp.append(str(hf))
            aspect[p] = temp
        first , second , third , fourth = [] , [] , [] , []
        for p in planet_rasi_degree:
            print("\n\n p ", planet_rasi_degree[p])
            d = lagna_rasi_degree - planet_rasi_degree[p]
            d = abs(d)
            if d < 6:
                first.append(p)
            if d > 5 and d < 11:
                second.append(p)
            if d > 10 and d < 16 : 
                third.append(p)
            if d > 15:
                fourth.append(p)
            
        
        return aspect,first,second,third,fourth
    
    def Sthanabala(self,*args,**kwargs):
        asc = self.set_lagna()
        data = self.planetary()
        lagna_degree = asc[0]
        lagna_rasi = asc[1]
        lagna_rasi_degree = asc[2]
        planet_degree = data[0]
        planet_rasi = data[1]
        planet_rasi_degree = data[2]
        print("\n\n\n  planet degree ", planet_degree)
        Su , Mo, Ma , Me , Ju, Ve , Sa, Ra, Ke = "1", "2", "3", "4", "5", "6", "7", "8", "9"         
        Su_rasi , Mo_rasi, Ma_rasi, Me_rasi , Ju_rasi, Ve_rasi, Sa_rasi, Ra_rasi, Ke_rasi =  planet_rasi[Su], planet_rasi[Mo], planet_rasi[Ma], planet_rasi[Me], planet_rasi[Ju], planet_rasi[Ve] , planet_rasi[Sa] , planet_rasi[Ra] , planet_rasi[Ke]
        
        Su_rasi_degree, Mo_rasi_degree, Ma_rasi_degree, Me_rasi_degree, Ju_rasi_degree, Ve_rasi_degree, Sa_rasi_degree, Ra_rasi_degree, Ke_rasi_degree = planet_rasi_degree[Su], planet_rasi_degree[Mo], planet_rasi_degree[Ma], planet_rasi_degree[Me], planet_rasi_degree[Ju],planet_rasi_degree[Ve], planet_rasi_degree[Sa], planet_rasi_degree[Ra], planet_rasi_degree[Ke]        
        
        Su_answer = self.umon(Su,Su_rasi)
        
        Mo_answer = self.umon(Mo,Mo_rasi)
        
        Ma_answer = self.umon(Ma,Ma_rasi)
        
        Me_answer = self.umon(Me,Me_rasi)
        
        Ju_answer = self.umon(Ju,Ju_rasi)
        
        Ve_answer = self.umon(Ve,Ve_rasi)
        
        Sa_answer = self.umon(Sa,Sa_rasi)
        
        Ra_answer = self.umon(Ra,Ra_rasi)
        
        Ke_answer = self.umon(Ke,Ke_rasi)
        
        Su_strength, Mo_strength, Ma_strength, Me_strength, Ju_strength, Ve_strength, Sa_strength, Ra_strength, Ke_strength = self.strength(Su_answer,Su,Su_rasi_degree,Su_rasi), self.strength(Mo_answer,Mo,Mo_rasi_degree,Mo_rasi), self.strength(Ma_answer,Ma,Ma_rasi_degree,Ma_rasi), self.strength(Me_answer,Me,Me_rasi_degree,Me_rasi), self.strength(Ju_answer,Ju,Ju_rasi_degree,Ju_rasi), self.strength(Ve_answer,Ve,Ve_rasi_degree,Ve_rasi), self.strength(Sa_answer, Sa,Sa_rasi_degree,Sa_rasi), self.strength(Ra_answer,Ra,Ra_rasi_degree,Ra_rasi), self.strength(Ke_answer,Ke,Ke_rasi_degree,Ke_rasi)
        if Su_strength == "invalid":
            if self.fcheck(Su,Su_rasi):
                Su_strength = "f"
            else:     
                Su_strength = self.echeck(Su,Su_rasi)                    
        if Mo_strength == "invalid":
            if self.fcheck(Mo,Mo_rasi):
                Mo_strength = "f"
            else:
                Mo_strength = self.echeck(Mo,Mo_rasi)
                  
                    
        if Ma_strength == "invalid":
            if self.fcheck(Ma,Ma_rasi):
                Ma_strength = "f"
            else:
                Ma_strength = self.echeck(Ma,Ma_rasi)
                    
                    
        if Me_strength == "invalid":
            if self.fcheck(Me,Me_rasi):
                Me_strength = "f"
            else: 
                Me_strength = self.echeck(Me,Me_rasi)
                   
      
        if Ju_strength == "invalid":
            if self.fcheck(Ju,Ju_rasi):
                Ju_strength = "f"
            else: 
                Ju_strength = self.echeck(Ju,Ju_rasi)
                       
        if Ve_strength == "invalid":
            if self.fcheck(Ve,Ve_rasi):
                Ve_strength = "f"
            else:
                Ve_strength = self.echeck(Ve,Ve_rasi)
                   
                    
        if Sa_strength == "invalid":
            if self.fcheck(Sa,Sa_rasi):
                Sa_strength = "f"
            else:
                Sa_strength = self.echeck(Sa,Sa_rasi)
                
                    
        if Ra_strength == "invalid":
            if self.fcheck(Ra,Ra_rasi):
                Ra_strength = "f"
            else: 
                Ra_strength = self.echeck(Ra,Ra_rasi)
                
                    
        if Ke_strength == "invalid":
            if self.fcheck(Ke,Ke_rasi):
                Ke_strength = "f"
            else:
                Ke_strength = self.echeck(Ke,Ke_rasi)
               
        ps = [ Su_strength, Mo_strength, Ma_strength,Me_strength,Ju_strength,Ve_strength,Sa_strength,Ra_strength,Ke_strength]
        Lord = self.Lord[str(lagna_rasi)]
        return ps,Lord
        
        
        
        
        
        
        
        
   
    def echeck(self,planet,rasi,*args):
       if rasi in self.Neutral[planet] :
          return "nu"
       else:
          return "e"
             
              
    def fcheck(self,planet,rasi,*args): 
       if rasi in self.Friend[planet]:
             return True
       else:
             return False  
             
    def navamlagna(self,*args,**kwargs):
        nasc = self.navam_no_finder()  
        ndata = self.planetary()[3]
        rasc = self.set_lagna()[1]
        
        nasc = str(nasc)
        rasc = str(rasc)
        if nasc == rasc:
            print("\n\n  vagottama ")
            return ["vgtm.jpg"]
        else:
            answer = self.nrLord_strength(nasc,rasc,ndata)
            print(answer)
            return answer
            
    def pakha(self,m,s,*args):
        d = m - s
        if d < 0 :
            d += 360
        if d > 360:
            d -= 360
        tithi = int(d//12)+1
        state = [ 0,0,0,0]
        #[new,waxing,full,waning]
        
        if tithi == 30:
            state[0] = 1
        if tithi != 30 and tithi < 15 :
            state[1] = 1
        if tithi == 15 :
            state[2] = 1
        if tithi > 15 and thithi != 30:
            state[3] = 1
        return tithi,state
        
            
    
    def planet_property(self,p,*args,**kwargs):
        pi = int(p) -1
        pdata = self.planetary()
        planet_rasi = pdata[1]
        planet_bhava = pdata[4]
        planet_navam = pdata[3]
        pkr = self.is_paap_kartari(p,planet_rasi)
        pkb = self.is_paap_kartari(p,planet_bhava)
        pkn = self.is_paap_kartari(p,planet_navam)
        bala = self.Sthanabala()[0][pi]
        nvdata = pdata[3]
        ans = self.umon(p,nvdata[p])
        nbala = "invalid"
        if ans[0] == 1:
            nbala = "u"
        if ans[0] != 1 and ans[1] == 1:
            nbala = "m"
        if ans[3] == 1:
            nbala = "n"
        if ans == [0,0,1,0]:
            nbala = "o"
        if nbala == "invalid":
            friend = self.fcheck(p,nvdata[p])
            if friend :
                nbala = "f"
            else:
                foe = self.echeck(p,nvdata[p])
                nbala = foe
        if planet_rasi[p] == planet_navam[p]:
                nbala = "vgtm"
                
        return pkr,pkb,pkn,bala,nbala
        
                
    def is_paap_kartari(self,planet,planet_rasi,*args):
        p = planet
        prs = planet_rasi
        rs = planet_rasi[p]
        
        rs_2 = int(rs) + 1 
        if rs_2 > 12 :
            rs_2 -= 12
        rs_2 = str(rs_2)
            
        rs_12 = int(rs) - 1
        if rs_12 < 0:
            rs_12 += 12
        rs_12 = str(rs_12)
            
        ans = []
        for op in prs:
            if op in [ "1","3","7","8","9" ]:
                if rs_2 == prs[op]:
                    ans.append(1)
                    break
        for otp in prs:
            if otp in ["1","3","7","8","9"]:
                if rs_12 == prs[otp]:
                    ans.append(1)
                    break 
                                   
        if ans == [1,1] :
            return True
        else:
            return False     
            
              
    def nrp_strength(self,planet,*args,**kwargs):
        pdata = self.planetary()
        sth = self.Sthanabala()[0]
        planet_rasi = pdata[1]
        planet_nav = pdata[3]
        planet_bha = pdata[4]
        planet_rasi_degree = pdata[2]
        pk = self.is_paap_kartari(planet,planet_rasi)
        
        
        
        
    def nrLord_strength(self,nasc,rasc,ndata,*args,**kwargs):
        nLord = self.Lord[nasc]
        rLord = self.Lord[rasc]
        
        nLord_nrs = ndata[nLord]
        rLord_nrs = ndata[rLord] 
        
        nLord_ans = self.umon(nLord,nLord_nrs)
        rLord_ans = self.umon(rLord,rLord_nrs)
        self.n = None
        self.r = None
        n = None
        r = None
        print(nLord_ans)
        print(rLord_ans)
        if nLord_ans[0] == 1:
            n = "nwu.jpg"
        if nLord_ans[0] != 1 and nLord_ans[1] == 1:
            n = "nwm.jpg"
        if nLord_ans[3] == 1:
            n = "nwn.jpg"
        if nLord_ans == [0,0,1,0] :
            n = "nwo.jpg"
        
        
        if rLord_ans[0] == 1:
            r = "rsu.jpg"
        if rLord_ans[0] != 1 and rLord_ans[1] == 1:
            r = "rsm.jpg"
        if rLord_ans[3] == 1:
            r = "rsn.jpg"
        if rLord_ans == [0,0,1,0]:
            r = "rso.jpg"
        
        print("\n\n   rLord_ans  :  ", rLord_ans)
        if nLord_ans == [0,0,0,0] :
                if self.fcheck(nLord,nLord_nrs):
                    n = "nwf.jpg"
                else:
                    n = self.echeck(nLord,nLord_nrs)
                    if n == "e":
                       n = "nwe.jpg"
                    else:
                        n = "nwnu.jpg"
        if rLord_ans == [0,0,0,0] :
               if self.fcheck(rLord,rLord_nrs):
                    r = "rsf.jpg"
               else:
                    r = self.echeck(rLord,rLord_nrs)
                    if r == "e":
                       r = "rse.jpg"
                    else:
                       r = "rsnu.jpg"
        self.n = n
        self.r = r                
        return self.r,self.n            
                
                
    def umon(self,planet,rasi,*args,**kwargs):
      answer = [0,0,0,0]
      if self.Uchacha[planet] == rasi : 
          answer[0] = 1
      if self.Moola[planet] == rasi :
          answer[1] = 1
      if rasi in self.Own[planet] :
          answer[2] = 1
      if self.Neecha[planet] == rasi : 
          answer[3] = 1 
      return answer
    
    def strength(self,answer,planet,degree,rasi,*args,**kwargs):
        x = self.UN_degree[planet] 
        y = degree 
        d = x - y 
        
        v = self.Moola_range[planet] 
        i = v[0] 
        f = v[1]
        
        def mcheck(i,f,y):
            if y >= i and y <= f:
                return True
            else:
                return False
        
        def ncheck(x,y,d):
            if d > -0.1 and d < 0.1:  
                return "n"
            else:
                if x > y  :
                    return "n+" 
                else:
                    return "n-"
        def ucheck(x,y,d):
            if d > -0.1 and d < 0.1:  
                return "u"
            else:
                if x > y  :
                    return "u+" 
                else:
                    return "u-"        
                
        if answer == [0,0,0,1]:
            return ncheck(x,y,d)            
        elif answer == [1,1,1,0] :
            if mcheck(i,f,y) == True:
                return "m"
            if mcheck(i,f,y) == False:
                return ucheck(x,y,d) 
        elif answer == [0,1,0,0]:
            if mcheck(i,f,y) == True:
                return "m" 
            else:
                return "invalid"
        elif answer == [0,0,0,0] :
            return "invalid"
        elif answer == [0,0,1,0] :
            return "o"
        elif answer == [1,0,1,0] :
            return ucheck(x,y,d)
        elif answer == [1,1,0,0 ]:
            if mcheck(i,f,y) == True:
                return "m"
            else:
                return ucheck(x,y,d)
        elif answer == [0,1,1,0]:
            if mcheck(i,f,y) == True:
                return "m" 
            else:
                return "o"
        elif answer == [1,0,0,0] :
            return ucheck(x,y,d)
        else:
            return "system error"
    
    def set_planetary(self,*args,**kwargs):
        pass
        
    def planetary(self,*args,**kwargs):
        Degree = {}
        btime = self.extract_btime()
        bdate = self.extract_bdate()
        lst = self.local_standard_time()
        corbtime = self.birth_time_correction()
        h = lst[0]
        m = lst[1]
        s = lst[2]
        print(h,m,s)
        
        year,month,day = corbtime.year,corbtime.month,corbtime.day
        birth = datetime.datetime(year,month,day) + datetime.timedelta(hours=btime[0],minutes=btime[1],seconds=btime[2])
        local = datetime.timedelta(hours=h,minutes=m,seconds=s)
        utc = birth - local
        print("\n birth time cor ", utc)
        
        hr = utc.hour+utc.minute/60+utc.second/3600        
        jd = swe.julday(utc.year,utc.month,utc.day,hr)
        print("\n   JD    ", jd)
        
        PLANET = [swe.SUN,swe.MOON,swe.MARS,swe.MERCURY,swe.JUPITER,swe.VENUS,swe.SATURN,swe.TRUE_NODE]
        for p,planet in zip(range(len(PLANET)),PLANET):
            p += 1
            position, ret = swe.calc_ut(jd,planet)
            #name = swe.get_planet_name(planet)
            swe.set_sid_mode(swe.SIDM_LAHIRI_VP285)
            Lahiri = swe.get_ayanamsa(jd)
            sid_position = position[0] - Lahiri
            print("\n\n Lahiri Value ", position[0] , " -  " , Lahiri)
            if sid_position < 0:
                sid_position += 360
            Degree[str(p)] = sid_position
        Ketu = (Degree["8"] + 180)%360
        Degree["9"] = Ketu
        print("\n Planet :::::::: ", Degree)
        
        Rasi = {}
        for p in Degree:
            r = int(Degree[p]/30)+1
            Rasi[p] = str(r)
            
        Rasi_degree = {}
        for p in Degree:
            rd = Degree[p]%30
            Rasi_degree[p] = rd
        print("Rasi ", Rasi , "  Rasi degree ", Rasi_degree)
        
        def navam_finder(p_deg):
            n = 360/108
            mu = 0 
            for multiplicant in range(108):
                nav = n*multiplicant
                d = p_deg - nav
                if d < 0:
                    mu = multiplicant
                    break
            nav_rasi = mu%12
            if nav_rasi == 0:
                nav_rasi = 12
            return nav_rasi
        Navam_rasi = {}
        for p in Degree:
            nd = Degree[p]
            n = navam_finder(nd)
            Navam_rasi[p] = str(n)
        print("\n  Navam Rasi : ", Navam_rasi)
        
        lagna = self.set_lagna()
        print("\n\n Lagna ====== ", lagna[2])
        boundary = 15- lagna[2]  #July 27   
        print("\n boundary ===== ", boundary)       
        Bhava_degree = {}
        print("\n no shifted bound : ", Degree)
        for p in Degree:
            rs = Degree[p] 
            rs += boundary 
            if rs > 360: #edit July 27
                rs -= 360
            elif rs < 0: #boundary July 27
                rs += 360 #360+boundary 
            Bhava_degree[p] = rs
        print("\n had shifted bound : ",Bhava_degree)
        
        Bhava_house = {}
        for p in Bhava_degree:
            bh = int(Bhava_degree[p]/30) + 1
            if bh < 1: #edit
                bh += 1
            if bh == 0:
                bh = 12
            elif bh > 12:
                bh -= 12
            Bhava_house[p] = str(bh)
        print("\n bounded house : ",Bhava_house)
        print("\n   Lagna[2]  == ", lagna[2])
        nakshatra = {}
        for p in Degree:
                  for n in range(27):
                      factor = 13.333333
                      i = n*factor
                      f = (n+1)*factor
                      if Degree[p] >= i and Degree[p] < f:
                          nakshatra[p] = str(n+1)
                          break
                  
        return Degree,Rasi,Rasi_degree,Navam_rasi,Bhava_house,Bhava_degree,boundary,jd,Lahiri,nakshatra

    #navam lagna
    def navam_no_finder(self,*args,**kwargs):
        data , lagna = self.set_lagna(), self.set_lagna()[0]
        #lagna = 180
        n = 360/108
        print("\n    n ===== > ", n)
        print("\n   lagna ", lagna)
        mu = 0
        for multiplicant in range(108):
           nav = n *multiplicant
           #print("\n   nav = ", nav, "  i  value = ", multiplicant)
           d = lagna - nav
           if d < 0:
                mu = multiplicant
                break
        nav_rasi = mu%12
        if nav_rasi == 0:
            nav_rasi = 12
        print("\n\n\n Nav_Rasi : ", nav_rasi)
        return nav_rasi
         
                
        
        
    def noon_lagna(self,sid):
        Ascendent = self.pm_lagna(self,sid)
        return Ascendent 
    def am_lagna(self,sid):
        AH = sid.hour + (sid.minute/60) + sid.second/3600
        asc = AH * 15 
        L = self.extract_bplace()[1]
        Lahiri = self.get_ayanamsa()
        E = self.get_obliquity()
        Ascendent = math.degrees(math.atan(-math.cos(math.radians(asc))/(math.sin(math.radians(E))*math.tan(math.radians(L))+math.cos(math.radians(E))*math.sin(math.radians(asc)))))
        print("\n AM lagna")
        n = int(asc/180)
        if Ascendent >=0:
            valid = True
        else:
            valid = False
        match valid:
            case True:
                Ascendent += -Lahiri
                if  n%2 == 0 : 
                    Ascendent += 180    
                if int(AH) == 12:
                     Ascendent += 180
                if Ascendent < 0:
                     if n%2 != 0:
                         Ascendent += 360
            case False:
                Ascendent += -Lahiri+ 180
                if n%2 != 0:
                     Ascendent += 180
                if int(AH) == 23:
                     Ascendent -= 180
        return Ascendent 
        
    def pm_lagna(self,sid):
            AH = sid.hour+ (sid.minute/60)+sid.second/3600
            asc = AH*15
            L = self.extract_bplace()[1]
            E = self.get_obliquity()
            Lahiri = self.get_ayanamsa()
            Ascendent = math.degrees(math.atan(-math.cos(math.radians(asc))/(math.sin(math.radians(E))*math.tan(math.radians(L))+math.cos(math.radians(E))*math.sin(math.radians(asc)))))
            n = int(asc/180)
            if Ascendent >= 0:
                valid = True
            else:
                valid = False
            match valid:
                case True:
                    Ascendent += -Lahiri 
                    if  n%2 == 0 : 
                     Ascendent += 180
                    if int(AH) == 12:
                     Ascendent += 180
                    if Ascendent < 0:
                         if n%2 != 0:
                             Ascendent += 360
                case False:
                   Ascendent += -Lahiri + 180
                   if n%2 != 0:
                     Ascendent += 180
                   if int(AH) == 23:
                     Ascendent -= 180
            return Ascendent
            
    def lagna_calculator(self,identifier,sid):       
            if identifier == "pm":
                return self.pm_lagna(sid)
            elif identifier == "am":
                return self.am_lagna(sid)
            else:
                return self.noon_lagna(sid)
    def noon_birth(self,noon,sidereal_noon,corbdate):
        sidereal_time = sidereal_noon + corbtime
        #print(sidereal_time)
        return sidereal_time       
         
    def am_birth(self,noon,sidereal_noon,corbtime):
       noon -= corbtime
       sid_corbtime = noon*1.00273896
       sid_corbtime = sidereal_noon - sid_corbtime
       print("\n\n sid_corbtime : " , sid_corbtime)
       return sid_corbtime
        
    def pm_birth(self,noon,sidereal_noon,corbtime):
        corbtime -= noon
        sid_corbtime = corbtime * 1.00273896
        sid_corbtime += sidereal_noon
        print("\n\n sid_corbtime : ", sid_corbtime)
        return sid_corbtime
        
    def set_lagna(self):
      identifier = self.is_afternoon()
      sid = self.get_sidereal_time()
      corbtime = self.birth_time_correction()
      y,m,d = corbtime.year,corbtime.month,corbtime.day
      noon = datetime.datetime(y,m,d,12,0,0)
      localoffset = self.local_mean_time()
      hr = localoffset[0]
      min = localoffset[1]
      sec = localoffset[2]
      LocalOffset = datetime.datetime(y,m,d,0,0,0)
      Local_Offset = datetime.timedelta(hours=hr,minutes=min,seconds=sec)
      hrminsec = hr + min + sec
      if hrminsec < 0:
            LO = LocalOffset - Local_Offset
      elif hrminsec >= 0:
            LO = LocalOffset + Local_Offset
      sidereal_interest = noon - LO
      sidereal_interest *= 1.00273896
      Sidereal_Interest = noon - LO
      sidereal_interest = sidereal_interest - Sidereal_Interest
      print("\n  LO ", LO , "\n sidereal_interest ", sidereal_interest, "  :  Sidereal_Interest ", Sidereal_Interest)
      sidereal_noon = sid + sidereal_interest + noon
      print("\n sidereal noon ", sidereal_noon)
      print("\n\n    sid  : ", sid)
      if identifier == None:
          return self.noon_birth(noon,sidereal_noon,corbtime)
      elif identifier == True:
          sid = self.pm_birth(noon,sidereal_noon,corbtime)
          lagna = self.lagna_calculator("pm",sid)
          rasi_degree = lagna%30
          rasi = int(lagna/30)+1
          #self.updade_user_data()
          return lagna,rasi,rasi_degree
      elif identifier == False:
          sid = self.am_birth(noon,sidereal_noon,corbtime)
          lagna = self.lagna_calculator("am",sid)
          rasi_degree = lagna%30
          rasi = int(lagna/30)+1
          print("\n Rasi ", rasi)
          #self.update_user_data()
          return lagna,rasi,rasi_degree
          
    def get_sidereal_time(self):
        jd = self.get_julian_day()
        sid = swe.sidtime(jd)
        hr = int(sid)
        m = sid - int(sid)
        m*= 60
        min = int(m)
        s = m - int(m)
        s*= 60
        sec = int(s)
        sid = datetime.timedelta(hours=hr,minutes=min,seconds=sec)
        return sid
        
    def get_obliquity(self):
        jd = self.get_julian_day()
        E = swe.calc(jd, swe.ECL_NUT, swe.FLG_SWIEPH)[0][0]
        return E 
    
    def get_ayanamsa(self):
        jd = self.get_julian_day()
        swe.set_sid_mode(swe.SIDM_LAHIRI_VP285)
        Lahiri = swe.get_ayanamsa(jd)
        return Lahiri

    
    def get_julian_day(self): #Testing 
        bdate = self.extract_bdate()
        btime = self.extract_btime()
        corbtime = self.birth_time_correction()
        jd = swe.julday(corbtime.year,corbtime.month,corbtime.day,0)#y,m,d,h
        return jd
    
    def is_afternoon(self):
        h,m,s = 12,0,0
        corbtime = self.birth_time_correction()
        year,month,day = corbtime.year,corbtime.month,corbtime.day
        noon = datetime.datetime(year,month,day,h,m,s)
        if noon < corbtime:
            return True
        elif noon == corbtime:
            return None
        elif noon > corbtime:
            return False
        
        
           
    def birth_time_correction(self):
         birthdate = self.extract_bdate()
         birthtime = self.extract_btime()
         hour , minute , second = birthtime[0] , birthtime[1], birthtime[2]
         day = birthdate[0]
         month = birthdate[1]
         year = birthdate[2]
         localoffset = self.local_mean_time()
         countryoffset = self.extract_offset()
         h = int(countryoffset)
         #print("\n  h : ", type(h))
         m = (countryoffset-h)*60
         s = (m - int(m))*60
         m = int(m)
         s = int(s)
         hms = h + m + s
         CountryOffset = datetime.datetime(year,month,day,0,0,0)
         countryoffset = datetime.timedelta(hours=h,minutes=m,seconds=s)
         if hms < 0:  
             CO = CountryOffset - countryoffset
         elif hms >= 0:
             CO = CountryOffset + countryoffset 
         hr = localoffset[0]
         min = localoffset[1]
         sec = localoffset[2]
         LocalOffset = datetime.datetime(year,month,day,0,0,0)
         localoffset = datetime.timedelta(hours=hr,minutes=min,seconds=sec)
         hrminsec = hr+min+sec
         if hrminsec < 0:
             LO = LocalOffset - localoffset
         elif hrminsec >= 0:
             LO = LocalOffset + localoffset
         MeanTimeDifference = CO - LO          
         BirthTime = datetime.datetime(year,month,day,hour,minute,second)
         CorrectedBirthTime = BirthTime - MeanTimeDifference
         print("\n Corrected Birth Time ", CorrectedBirthTime)
         return CorrectedBirthTime
         
         
            
    def local_standard_time(self):
        data = self.local_mean_time()
        lat = self.extract_bplace()[1]
        total = data[0]+data[1]/60+data[2]/3600
        lst = (-0.0096*(0.00007*lat))%12
        lst = (lst+total)%12
        #print("\n L.S.T : ", lst)
        h = int(lst)
        mm = (lst - h)*60
        m = int(mm)
        ss = (mm - m)*60
        s = int(ss)
        return [h,m,s]
        
        
    def local_mean_time(self):
        data = self.extract_bplace()
        lon = data[0]
        lat = data[1] #Testing
        #lst = (-0.0096*(0.00007*lat))%12
        h = lon/15 
        #h = (h+lst)%12
        m = (h - int(h))*60
        s = (m - int(m))*60        
        h = int(h)
        m = int(m)
        s = int(s)
        #print("\n local standard time ", h, " : ", m , " : ", s)
        return [h,m,s]
        
    def extract_btime(self,*args,**kwargs):
        tob = self.extract_TOB()
        h = int(tob[1])    
        m = int(tob[2])
        s = int(tob[3])
        return [h,m,s]
    def extract_bdate(self,*args,**kwargs):
        dob = self.extract_DOB()
        d = int(dob[0])
        m = int(dob[1])
        y = int(dob[2])
        #print("\n   d/m/y : ", d, "/",m,"/",y)
        return [d,m,y]
    def extract_bplace(self):
        lon = self.extract_POB()[0]
        lat = self.extract_POB()[1]
        pattern_lon = r'([-+]?\d*\.\d+|\d+)\u00b0([WE])'
        pattern_lat = r'([-+]?\d*\.\d+|\d+)\u00b0([NS])'
        lon_match = re.search(pattern_lon,lon)
        lat_match = re.search(pattern_lat,lat)
        if lon_match:
            Longitude = float(lon_match.group(1))
            LonDirection = lon_match.group(2)
            Latitude = float(lat_match.group(1))
            LatDirection = lat_match.group(2)
        if LonDirection == "W":
            Longitude *= -1
        if LatDirection == "S":
            Latitude *= -1 
        #print("\n Lon , Lat ", Longitude," : ",Latitude)
        return [Longitude,Latitude]
        
        
    def extract_offset(self,*args,**kwargs):
        offset = self.extract_TOB()[0]
        #print("\n  Offset ",offset)0
        offsetsign = offset[0]
        offsetvalue = offset[0:]
        if offsetsign == "+":
            offsetvalue = float(offsetvalue)
        elif offsetsign == "-":
            offsetvalue = float(offset)
        return offsetvalue
   
    def extract_POB(self):
        data = self.retrieve_user_data()
        for d in data:
            if d == "POB":
                pob = data[d]
        return pob              
    def extract_DOB(self,*args,**kwargs):
        data  = self.retrieve_user_data()
        for d in data:
            if d == "DOB":
                dob = data[d]
        return dob
    def extract_TOB(self,*args,**kwargs):
        data = self.retrieve_user_data()
        for d in data:
            if d == "TOB":
                tob = data[d]
        return tob
       
#========== R/U (init)=================        
      
    def retrieve_user_data(self,*args,**kwargs):
         path = os.path.join(self._user,"default_user.json")
         with open(path,"r") as f:
             data = json.load(f)
             f.close()
             return data
             
    def update_navam_lagna(self,*args,**kwargs):
        pass
        
    def update_planetary(self,*args,**kwargs):
        planetary = self.planetary()
        
    
    def update_lagna(self,*args,**kwargs):
        path = os.path.join(self._user,"chart.json")
        Lagna = self.set_lagna()
        Navam_Lagna = self.navam_no_finder()
        navam = str(Navam_Lagna)
        rasi = Lagna[1] #it is main
        rasi = str(rasi)
        print("\n rasi ===== ", rasi)
        planet = self.planetary()
        planet_rasi = planet[1]
        planet_nav = planet[3]
        planet_bha = planet[4]
        print("\n\n Planet Rasi  === ", planet_rasi)
        with open(path,"r") as f:
            RetrieveData = json.load(f)
            f.close()
        for N in RetrieveData:
            if N == "navam":
                temp = RetrieveData[N]
                for house in temp:
                    if house == navam:
                        temp[house] = ["A"]
                for house in temp:
                    if house != navam:
                        temp[house] = []
                for p in planet_nav:
                    n = planet_nav[p]
                    temp[n].append(p)
        for R in RetrieveData:
            if R == "rasi":
                temp = RetrieveData[R]
                print("\n Temp R ", temp)
                for house in temp:
                    if house == rasi:
                        temp[house] = ["A"]
                for house in temp:
                    if house != rasi:
                        temp[house] = []
                for p in planet_rasi:
                    r = planet_rasi[p]
                    temp[r].append(p)
                    
        for B in RetrieveData:
            if B == "bhava":
                temp = RetrieveData[B]
                for house in temp:
                    if house == rasi:
                        temp[house] = ["A"]
                    else:
                        temp[house] = []
                for p in planet_bha:
                    b = planet_bha[p]
                    temp[b].append(p)
        print("\n RetrieveData ", RetrieveData)
        with open(path,"w") as fw:
            json.dump(RetrieveData,fw,indent=4)
            fw.close()
        
            
            
        
#========== R/U (End) =================

class VimshottariModel:
    def __init__(self,model,*args,**kwargs):
        super(VimshottariModel,self).__init__(*args,**kwargs)
        self.parent = model
        self.cousin = VedicModel(self.parent)
        self.planet_span = {
        "1": 6,
        "2": 10,
        "3": 7,
        "8": 18,
        "5": 16,
        "7": 19,
        "4": 17,
        "9": 7,
        "6": 20       
        }
        self.normal_planet_series = ["1","2","3","4","5","6","7","8","9"]
        self.dosha_name = {        
        "1" : "Sun",
        "2" : "Moon",
        "3" : "Mars",
        "8" : "Rahu",
        "5" : "Jupiter",
        "7" : "Saturn",
        "4" : "Mercury",
        "9" : "Ketu",
        "6" : "Venus"        
        }
    def set_series(self,id,dosha_series):
        output_series = []
        for p in dosha_series[id:]:
            output_series.append(p)
        for p in dosha_series[:id]:
            output_series.append(p)
        return output_series

    def get_id(self,start_planet,dosha_series):
        for p,c in zip(dosha_series,range(len(dosha_series))):
           if p == start_planet:
               return c
           
               
            
    def dosha_effect(self,pseries,dosha_score):
        #dictionary print(dosha_score)
        map = []
        mapsc = []
        score = []
        for com in pseries:
            mah = com[0]
            ant = com[1]
            for pra in com[2]:
                msc = dosha_score[mah]
                asc = dosha_score[ant]
                psc = dosha_score[pra]
                m_name = self.dosha_name[mah]
                a_name = self.dosha_name[ant]
                p_name = self.dosha_name[pra]
                map.append([m_name,a_name,p_name])
                mapsc.append([msc,asc,psc])
        for sco in mapsc:
             sc = self.effect_calculator(sco)
             score.append(sc)
        return [score,map]
        
    def effect_calculator(self,mapsc):
        m = mapsc[0]
        a = mapsc[1]
        p = mapsc[2]   
        aa = a
        pp = p
        MAPV = 0
        if a < 0:
            aa *= -1
        if p < 0:
            pp *= -1
        mx = 0
        mi = 0  
        value = 0 
        mid = 0
        mean = 0
        #Traditional Effect
       
        Effect  = m+ a*0.5
        Effect += Effect + p*0.75
        
        #New Effect 
        if m != a:      
            MAPV = m+(a-m)*(aa/100)
        if m == a:
            MAPV = m+m*(aa/100)
        if a != p: 
            MAPV +=  a+(p-a)*(pp/100)
        if a == p:
            MAPV += a+a*(pp/100)
         
         
        #Block Effect
        Block = (a-m)*(aa/100)
        Block += (p-Block)*(pp/100)
        
        
        mean = (MAPV+Block+Effect)/3
        
        mx = max(MAPV,Block,Effect)
        mi = min(MAPV,Block,Effect)
        if mi >0: 
            mid = (mx-mi)/2
        else:
            mid = (mi+mx)/2                                    
        
        value = mid                      
        return mx
        
        
                                
        
    def dosha_graph(self,score_map,syr,spnet):
            start_year = syr
            start_planet = spnet
            initial = 81#130
            end = 405#519
            n = 1
            v = 100
            y = score_map[0]
            y = y[initial:end] #items 729 including
            sum = 0
            mx = 0
            mi = 0
            sumlist = []
            maxlist = []
            #sumlist.append(0)
            for i,j in zip(y,range(len(y))):
                sum += i
                sum = sum/v
                sumlist.append(sum)
                maxlist.append(sum)                  
                sum = 0
            y = sumlist
            dosha_total = []
            dosha_temp = 0
            for yi,c in zip(y,range(729)):
                dosha_temp += yi/n
                if c%n == 0:
                    dosha_total.append(dosha_temp)
                    dosha_temp=0
                    
                
                    
            #print("\n Total Dosha " , len(dosha_total),"\n")
            y = dosha_total  
            
                 
            x = score_map[1]
            x = x[initial:end]
            xlist = []
            for k,c in zip(x,range(len(x))):
                if (c+1)%n == 0:
                    xlist.append(k)
            rev = {} 
            for m in self.dosha_name:
                   rev[self.dosha_name[m]] = m
            dosha = []
            for xi in xlist:
              mah = int(rev[xi[0]])
              ant = int(rev[xi[1]])
              pra = int(rev[xi[2]])
              ds = self.dosha_calculator(start_planet,start_year,mah,ant,pra)
              dosha.append(ds)
            #print("\n   ", dosha)
            
            
            dosha_total_date = []
            for di,dt in zip(dosha,range(729)):
                if dt%1 == 0:
                    dxd = self.year_to_date(di[2])
                    dosha_total_date.append(dxd)
            x = dosha_total_date
            
            """dosha_total_set = []
            for xi,xt in zip(xlist,range(729)):
                txt = xi[0]+"×"+xi[1]+"×"+xi[2]
                dosha_total_set.append(txt)
            x = dosha_total_set
            print("\n    inyer x ", len(x))"""
            
            
            #plt.style.use("cyberpunk")
            """plt.plot(y,color="c")
            plt.ylabel = "Dosha Effects" 
            plt.xticks(range(len(x)),x,rotation=90)
            #plt.tight_layout()       
            plt.show()"""
            c = 0
            """for yi,xi in zip(y,x):
                if yi> 0 and yi < 20:
                    c+=1
                    print("\n\n Date : ",c," : ", xi , " 0<x<20 : Karmic Point : ", yi)"""
            
            
    def year_to_date(self,year):
        months = self.isleap(int(year))
        dayc = 0
        for m in months:
            dayc += months[m]
        year_int = int(year)        
        year_float = year - year_int
        day = year_float*dayc
        start_of_year = datetime(year_int,1,1)
        final_date = start_of_year + timedelta(days=day)
        #print("Final date ", final_date)
        
        string = final_date.strftime("%d/%m/%Y")
        
        return string
         
            
            
    #Interface func  
    def dosha_entry(self,date,time,Moon):
        data = self.first_dosha_calculator(date,time,Moon)
        start_year = self.start_year_calculator(data)
        start_planet = next(iter(data[1].items()))[0]
        dosha_date = self.dosha_calculator(start_planet,start_year,3,1,1)
        result = self.cousin.computing()[0] #final_score
        normal_series = self.normal_planet_series
        #matching
        planet_score = {} 
        for x,y in zip(normal_series,result):
            planet_score[x] = y
        
        dosha_series_dict = self.planet_span
        dosha_series = []
        for i in dosha_series_dict:
            dosha_series.append(i)
        id = self.get_id(start_planet,dosha_series)
        series = self.set_series(id,dosha_series)
        
        dosha_score = {}
        for sp in series:
            for p,s in planet_score.items():
                if sp == p:
                    dosha_score[sp] = s
                    
        #print(dosha_date)
        #print("\n\n", dosha_score)                      
        dosha_set = {}
        aseries_temp = {}
       
        mid = []
        for m in series:
          for c,d in zip(range(len(dosha_series)),dosha_series):
              if m == d:
                    mid.append(c)
        
        mdict = {}
        mdict["Maha"] = [series,mid]
        #print(mdict)
        
        aid = []
        adict = {}
        for a in mid:
             aseries = self.set_series(a,dosha_series)
             #print("\n Antar dosha ", aseries)
             adict[aseries[0]] = aseries
             for aa in aseries:
               for c,d in zip( range(len(dosha_series)),dosha_series):
                 if aa == d:
                    aid.append(c)
        #print(adict)
        
        plist = []
        for k,v in adict.items():
           for i in v:
               plist.append([k,i])
        #print(plist)
        
        pseries = []
        for list in plist:
          key = list[1]
          lister = adict[key]
          list.append(lister)
          pseries.append(list)
          
        #print("\n  Pseries ", pseries,"\n ")
        
        """to_date = []
        for com in pseries:
          mah = com[0]
          ant = com[1]
          for pra in com[2]:
              to_date.append([mah,ant,pra])"""
          
          
        return [pseries,dosha_score,start_year,start_planet]
        
          
         
          
                    
                
                
                    
                    
        
    
    def dosha_calculator(self,D,S,M,A,P):
            #D dosha planet
            #print("\n  Start year " , S )
            D = str(D)
            M = str(M)
            A = str(A)
            P = str(P)
            Mspan = self.planet_span[M]
            Aspan = self.planet_span[A]
            Pspan = self.planet_span[P]
            temp_list = []
            base_list = []
            antar_list = []
            pratyantar_list = []
            for i in self.planet_span:
                temp_list.append(i)
            for item,c in zip(temp_list,range(len(temp_list))):
                if D == item:
                    break
                c+=1 
            
            
            for x in temp_list[c:]:
                base_list.append(x)
            for y in temp_list[:c]:
                base_list.append(y)
            
            
            for z in base_list:
                if M == z:
                    break
                else:
                    S += self.planet_span[z]
            #print("\n Maha  ", S)
            Maha = S
            
            for x,ca in zip(temp_list,range(len(temp_list))):
                if M == x:
                    break
                ca+=1
            
            for x in temp_list[ca:]:
                antar_list.append(x)
            for y in temp_list[:ca]:
                antar_list.append(y)
            print(antar_list)
            
            for z in antar_list:
                if A == z :
                    break
                else:
                    S+= (self.planet_span[M]/120)*self.planet_span[z]
            #print("\n Antar  ", S)
            Antar = S
            
            for x,cp in zip(temp_list,range(len(temp_list))):
                if A == x:
                    break
                cp+=1
            for x in temp_list[cp:]:
                pratyantar_list.append(x)
            for y in temp_list[:cp]:
                pratyantar_list.append(y)
            
            for z in pratyantar_list:
                if P == z:
                    break
                S+= (self.planet_span[M]/120)*(self.planet_span[A]/120)*self.planet_span[z]
            #print("\n Pratyantar ", S )
            Pratyantar = S
            return [Maha,Antar,Pratyantar]            
                            
            #D = dosha start Sun,Moon,Mars,etc
            #S = start_year
            #M = Maha
            #A = Antar
            #P = Pratyantar 
            #dosha_calculator(D,)
            
        
    
        
    def start_year_calculator(self,Data,*args,**kwargs):
        data = Data[0]
        dosha = Data[1]
        start_date = data[0]
        start_time = data[1]
        
        series_list = []
        for p in self.planet_span:
            series_list.append(p)
        #print("\n Series List : ", series_list)
        
        dosha_series = {}
        for pnet,index in zip(self.planet_span,range(9)):
            p = int(pnet)            
            start = index
            end = int(len(series_list))
            ds = []
            for i in range(start,end):
                ds.append(series_list[i])
            for x in range(0,start):
                ds.append(series_list[x])
            dosha_series[pnet] = ds            
        #print("\n Dosha Series ",dosha_series)
        
        start_hr = start_time[0]
        start_min = start_time[1]
        start_sec = start_time[2]
        start_year = start_date[2]
        start_month = start_date[1]
        start_day = start_date[0]
        start_year_month = self.isleap(start_year)
        #print(start_year_month)
        
        
        start_year_day = 0
        for m in start_year_month:
            start_year_day += start_year_month[m]        
        #print(start_year_day)#366 or 365
        
        start_month_day = start_day
        for mc,md in zip(range(start_month-1),start_year_month):
            start_month_day += start_year_month[md]
        #print("  Jan to July(not finish month) " ,start_month_day)#jan to june
        start_time_to_hr = start_hr+start_min/60+start_sec/3600
        start_time_to_day = start_time_to_hr/24
        start_time_to_year = start_time_to_day/start_year_day
        #print(start_time_to_year)
        start_month_day_to_year = start_month_day/start_year_day
        print(start_month_day_to_year)
        total_to_year = start_year+start_time_to_year+start_month_day_to_year
        #print(total_to_year)
        magnitude = 120
        start_year_format = total_to_year
        return start_year_format   
        
    #Start point Moon Nak 
    def first_dosha_calculator(self,date,time,Moon,*args,**kwargs):
        Planet_span = {
        "1": 6,
        "2": 10,
        "3": 7,
        "8": 18,
        "5": 16,
        "7": 19,
        "4": 17,
        "9": 7,
        "6": 20       
        }
        """nak_lord = self.cousin.retrieve_nak_lord()
        temp = self.cousin.computing()""" #5/10/2024
        nak_lord = {
  "3": "1",
  "12": "1",
  "21": "1",
  "4": "2",
  "13": "2",
  "22": "2",
  "5": "3",
  "14": "3",
  "23": "3",
  "9": "4",
  "18": "4",
  "27": "4",
  "7": "5",
  "16": "5",
  "25": "5",
  "2": "6",
  "11": "6",
  "20": "6",
  "8": "7",
  "17": "7",
  "26": "7",
  "6": "8",
  "15": "8",
  "24": "8",
  "1": "9",
  "10": "9",
  "19": "9"
}

        month_dict = self.isleap(date[2])
        day = 0
        for m,d in month_dict.items():
            day += d
            
        Day = date[0]
        Month = date[1]
        Year = date[2]
        Day_series = {} #jan 0
        Day_sum = {} #jan 31
        Day_total = 0
        
        for m in month_dict:
            Day_total += month_dict[m]
            Day_series[m] = Day_total - month_dict[m]
            Day_sum[m] = Day_total
            
        Month_series = {}
        i = 0
        for m in month_dict:
             Month_series[i+1] = m
             i+=1
        
        Day_temp = 0
        for m in month_dict:
            if Month_series[Month] == m:
                if Day <= month_dict[m]:
                    Day_temp = Day+Day_series[m]
                    
        Day_to_year = Day_temp / Day_total
        Date_to_year = Year + Day_to_year
        #print(Date_to_year)
        Time_to_year = ((time[0]+time[1]/60+time[2]/3600)/24)/Day_total
        #print("\n Time to Y ", Time_to_year)
        Total_year = Date_to_year + Time_to_year
        #print("\n Total Year : ", Total_year)
        
        nak = Moon/13.3333333
        nak_fration = nak-int(nak)
        nak_str = str(int(nak+1))
        for nk,lord in nak_lord.items():
            if nak_str == nk:
                moon_nak_lord = nak_lord[nk]
        span = Planet_span[moon_nak_lord] 
        #print("\n Lord and Span ", moon_nak_lord," : ", span)
        
        Maha = []
        Dosha_sequence = []
        s = []
        Maha_dosha = {}
        for planet in Planet_span:
            Dosha_sequence.append(int(planet))
            if planet == moon_nak_lord:
               s = int(planet)
        Maha.append(str(s))
        for planet in Dosha_sequence[s:]:
             Maha.append(str(planet))
        for planet in Dosha_sequence[:s]:
             Maha.append(str(planet))
        for p in Maha:
             Maha_dosha[p] = Planet_span[p]
        #print(Maha_dosha)
        
        Nak_span = 13.3333333
        Passed_nak = nak_fration 
        Passed_span = Passed_nak*Nak_span
        Remain_span = Nak_span - Passed_span
        #print("\n Pass deg ", Passed_span, " : ", Remain_span)
        #print("\n   Lord " , s)
        #for sample dosha 
        Dosha_span = Maha_dosha[str(s)]
        #print("\n Dosa span ", Dosha_span)
        
        year_per_deg = Dosha_span/13.333333 #year per°
        Passed_year = Passed_span * year_per_deg
        #print("\n Passed year : ", Passed_year)
        Remain_year = Dosha_span - Passed_year
        #print("\n Remain year : ", Remain_year)
        Start_date = Total_year - Passed_year
        #print("\n Start date " , Start_date)
        
        Start_date_days = self.isleap(int(Start_date))
        
        
        Start_date_days_amount = 0
        for k,v in Start_date_days.items():
            Start_date_days_amount += v
        
        Start_year =  int(Start_date)
        Start_year_float = Start_date - Start_year
        
        Start_year_to_days = Start_year_float*Start_date_days_amount
        
        
        Start_year_to_month = 1 
        for k,v in Start_date_days.items():
            if Start_year_to_days > v:
                Start_year_to_days -= v
                Start_year_to_month +=1
            
        Start_year_to_hours = (Start_year_to_days - int(Start_year_to_days)) * 24
        
        Start_year_to_minutes = (Start_year_to_hours-int(Start_year_to_hours))*60
        
        Start_year_to_seconds = int( (Start_year_to_minutes-int(Start_year_to_minutes))*60)
        
        Dosha_Start_Date = [int(Start_year_to_days),int(Start_year_to_month),Start_year]
        
        Dosha_Start_Time = [int(Start_year_to_hours),int(Start_year_to_minutes),Start_year_to_seconds]
    
        start_date_time = [Dosha_Start_Date,Dosha_Start_Time]
        start_planet = Maha_dosha
        print(start_date_time,start_planet)
        return [start_date_time,start_planet]
                
                  
    def isleap(self,year): #return dict 
        month_dict = {
        "January" : 31,
        "February": 28,
        "March" : 31,
        "April": 30,
        "May":31,
        "June":30,
        "July":31,
        "August":31,
        "September":30,
        "October": 31,
        "November":30,
        "December":31        
        }
        if year%4 == 0 and (year%100 != 0 or year%400 == 0):
            month_dict["February"] = 29
            return month_dict
        else:
            return month_dict
            
        
        
        
        
        
        
        
class VedicModel:
    def __init__(self,model,*args,**kwargs):
        super(VedicModel,self).__init__(*args,**kwargs)
        self.parent = model
        self._DB = self.parent.get_db()
        self._db = os.path.join(self._DB,"Vedic_DB")
        self._user = os.path.join(self._DB,"User_DB")
        self.user_temp = os.path.join(self._user,"planetary_score.json")
        self.user_path = os.path.join(self._user,"lawintun.xlsx")
        
        self._planet_name = os.path.join(self._db,"planet.json")
        self._rasi_name = 0
        self._bhava_name = 0
        self._navam_name = 0
        self._nakshatra_name = 0
        
        self._rasi_navam_lord = 0
        self._nakshatra_lord = os.path.join(self._db,"nakshatra_lord.json")
        self._uch = os.path.join(self._db,"rasi_uch.json")
        self._nech = os.path.join(self._db,"rasi_nech.json")
        self._own = os.path.join(self._db,"rasi_own.json")
        self._rev = os.path.join(self._db,"rasi_rev.json")
        self._nature = os.path.join(self._db,"nature.json")
        self._bhava_type = os.path.join(self._db,"bhava_type.json")
        self._relation_weight = os.path.join(self._db,"relationship_weight.json")
        
        self._factor = 100/192
        
#========= RETRIEVE - R Group ===========

#Main Gear - JSON - R
    def retrieve_json(self,path):
        with open(path,"r") as fr:
            data = json.load(fr)
            fr.close()
        #print(f"\n  Json Data of {path} ", data) 
        return data  
        
#JSON Retrieve
    def retrieve_relation_weight(self,*args):
        data = self.retrieve_json(self._relation_weight)
        return data
    def retrieve_bhava_type(self,*args):
        data = self.retrieve_json(self._bhava_type)
        return data
    def retrieve_rasi_own(self,*args):
         data = self.retrieve_json(self._own)
         return data
    def retrieve_rasi_uch(self,*args):
         data = self.retrieve_json(self._uch)
         return data
    def retrieve_rasi_nech(self,*args):
         data = self.retrieve_json(self._nech)
         return data 
    def retrieve_rasi_rev(self,*args):
         data = self.retrieve_json(self._rev)
         return data
    def retrieve_friend(self,*args): #s1
         data = self.retrieve_json(self._nature)
         #print("\n       ",data["friend"])
         return data["friend"]
    def retrieve_foe(self,*args):#s2
         data = self.retrieve_json(self._nature)
         #print("\n     ", data["foe"])
         return data["foe"]
    def retrieve_neutral(self,*args):#s3
         data = self.retrieve_json(self._nature)
         #print("\n     ", data["neutral"])
         return data["neutral"]                      
    def retrieve_nak_lord(self,*args):
              data = self.retrieve_json(self._nakshatra_lord)
              #print("\n     ",data)
              return data
    def retrieve_planet_name(self,*args):
              data = self.retrieve_json(self._planet_name)
              return data
              
#Excel Retrieve              
    def retrieve_planet(self,*args,**kwargs):
        planet = self.retrieve_excel()[0]
        #print("\n Planets " , planet)
        return planet
    def retrieve_rasi(self):
        rasi = self.retrieve_excel()[1]
        #print("\n  Rasi ", rasi)
        return rasi
    def retrieve_navam(self):
        navam = self.retrieve_excel()[3]
        #print("\n  Navam ", navam)  
        return navam
    def retrieve_bhava(self):
        bhava = self.retrieve_excel()[2]
        #print("\n  Bhava ", bhava)
        return bhava
    def retrieve_nak(self):
        nak = self.retrieve_excel()[4]
        #print("\n  Nakshatra ", nak)
        return nak
       
        
#Main Gear - Excel - R    
    def retrieve_excel(self,*args,**kwargs):
       data = []
       temp = []
       for col in range(5):
           buffer = pd.read_excel(self.user_path,usecols=[col],nrows=11).squeeze().tolist()
           for i in buffer:
               j = str(i)
               temp.append(j)
           data.append(temp)
           temp = []
       #print("\n Excel data", data)
       return data
       
#========= End of R - Group =============

#========= Calculation C - Group =========

    def relation_weight_defining(self,rtype,stype,*args,**kwargs):
        relation_weight = self.retrieve_relation_weight()
        weight = []
        
        for rt in rtype:
           for st in stype:
                #print("\n The planet , its R type : ", rt, " ,  and its S Type : ", st)
                rtw = relation_weight[rt]
                stw = relation_weight[st]
                weight.append(rtw*stw*6)
                print(weight)
          
        w = 0 
        for i in weight:
             w += i
        return w
                
        
    def planet_rule_and_sit_check(self,*args,**kwargs):
        Ruler = self.planet_rule_house_type()[0]
        #{"planet":["house type"]} rulling type
        Sitting = self.planet_sit_house_type()[0]
        #{"planet":["house type"]} sitting type
        House_Key = self.planet_sit_house_type()[1]
        #{"planet":["house no"]}
        House_Lord = self.planet_rule_house_type()[1]
        #{"house no":["lord"]}
        Lord_House = self.planet_rule_house_type()[2]
        #{"lord" :["house no"]}
        Planet = {}
        for planet in range(1,10):
            Planet[str(planet)] = []
        index=1
        for ruler,sitting in zip(Ruler,Sitting):
            if ruler == sitting:
               rt = Ruler[ruler]
               st = Sitting[sitting]
               w = self.relation_weight_defining(rt,st) 
               #weight += w
               Planet[str(index)] = w
               index+=1
        #print(Planet)
        #print("\n   House Key ", House_Key)
        #print("\n   House Lord ", House_Lord)
        #print("\n   Lord House ", Lord_House)
        
        Planet_House_Lord = {}
        for p,h in House_Key.items():
            Lord = House_Lord[h]
            Planet_House_Lord[p] = Lord
            #{"planet":["lord"]}
        #print("\n  planet : the lord of it sit house ", Planet_House_Lord)
        zero = [0,0,0,0,0,0,0,0,0]
        #own check
        c = 0
        Own_Score = zero
        for P,HL in Planet_House_Lord.items():
            for hL in HL:
                if P == hL:
                    Own_Score[c] = 6
                    #Own_Score[c] = Own_Score[c]
                    break
                else:
                    Own_Score[c] = 0
            c += 1                    
        #print("\n\n      Own_Score : ", Own_Score)
        
        #friend check
        Friend_Dict = self.retrieve_friend()
        #{"planet":["planet"]} inter {"planet":["lord"]}
        #print("\n  Friend_Dict ", Friend_Dict)
        c = 0
        Friend_Score = [0,0,0,0,0,0,0,0,0]
        for P,L in Planet_House_Lord.items():
            for p_key,f_list in Friend_Dict.items():
                if P == p_key:
                    x = set(L)
                    y= set(f_list)
                    z = list(x.intersection(y))
                    for i in z:
                        if i:
                            Friend_Score[c] = 6
            c+=1
        #print("\n\n   Friend_Score : ", Friend_Score)         
        #foe check
        Foe_Dict = self.retrieve_foe()
        #print("\n\n   Foe_Dict ",Foe_Dict)
        c = 0
        Foe_Score = [0,0,0,0,0,0,0,0,0]
        for P,L in Planet_House_Lord.items():
             for p_key,e_list in Foe_Dict.items():
                  if P == p_key:
                    x = set(L)
                    y = set(e_list)
                    z = list(x.intersection(y))
                    for i in z:
                        if i:
                            Foe_Score[c] = -6
             c+=1
        #print("\n\n   Foe_Score : ", Foe_Score)
        
        Nature_Score = []
        for o,f,e in zip(Own_Score,Friend_Score,Foe_Score):
            w = o+f+e
            Nature_Score.append(w)
        #print("\n\n Nature_Score ", Nature_Score)
        weg = []
        for p,w in Planet.items():
            weg.append(w)
        
        Score = []        
        for wg,nsc in zip(weg,Nature_Score):
            Score.append(wg+nsc)
        #print("\n  Score : ", Score," : ",Planet)    
        return Score
    
    def planet_sit_house_type(self,*args,**kwargs):
        Bhava_Type = self.retrieve_bhava_type()
        #{"bhava":["type"]}
        PRHT = self.planet_rule_house_type()[0]
        #{"lord":["house_type"]}
        
        Bhava = self.retrieve_bhava()
        #["rasi key as bhava"]
        Lagna = Bhava[9]
        #"no"
        Planet_Bhava = {}
        for planet,bhava in zip(range(1,10),Bhava):
            Planet_Bhava[str(planet)] = bhava
            #{"planet":"rasi no (key as bhava)"}
        
        Rasi = []
        for house in range(1,13):
            house += int(Lagna)-1
            if house > 12:
                house -= 12
            h = str(house)
            Rasi.append(h)
            #["no"]
            
        House_Rasi = {}
        for house,rasi in zip(range(1,13),Rasi):
           House_Rasi[str(house)] = rasi 
           #{ "house" : "rasi" }  
        
        for planet,bhava in Planet_Bhava.items():
            for house,rasi in House_Rasi.items():
                if bhava == rasi:
                    Planet_Bhava[planet] = house       
        #{"planet":"house no (key as bhava)"}
        #print("Planet Sitting Bhava", Planet_Bhava)
        
        Planet_Type = {}
        for Planet,Bhava in Planet_Bhava.items():
            for bhava,type in Bhava_Type.items():
                if Bhava == bhava:
                    Planet_Type[Planet] = type
        #print("\nPlanet Type", Planet_Type)
        Planet_Type_Bhava = [Planet_Type,Planet_Bhava]
        return Planet_Type_Bhava
        
        
    def planet_rule_house_type(self,*args,**kwargs):
        House_Type = self.retrieve_bhava_type()
        #{"house": ["type"]}
        Lord = self.retrieve_rasi_own()
        #{"rasi" : ["lord"] } 
        Lagna = self.retrieve_rasi()[9] 
        #"no"
        
        Rasi = []
        for house in range(1,13):
            house += int(Lagna)-1
            if house > 12:
                house -= 12
            h = str(house)
            Rasi.append(h) 
            #["no"]
        
        House_Rasi = {}
        for house,rasi in zip(range(1,13),Rasi):
           House_Rasi[str(house)] = rasi 
           #{ "house" : "rasi" } 
           
        for house,rasi in House_Rasi.items():
          House_Rasi[house] = Lord[rasi]      
        House_Lord = House_Rasi
        #{"house" : ["lord"] } 
        #print(House_Lord)
        Lord_House = {}
        for planet in range(1,10):
            Lord_House[str(planet)] = []
        for house,lord in House_Lord.items():
            for L in lord:
                Lord_House[L].append(house)
        #{"lord" :["house"]}
        #print(Lord_House)
        
        Lord_Type = {}
        for planet in range(1,10):
            Lord_Type[str(planet)] = []
        for L,H in Lord_House.items():
           for h in H:
               for house,type in House_Type.items():
                 if h == house:
                     for t in type:
                          Lord_Type[L].append(t)  
        #print(Lord_Type)
        #Duplicated item removel from list of dict
        for key in Lord_Type:
            Temp = Lord_Type[key] 
            Update = list(set(Temp))
            Lord_Type[key] = Update
        #print("\n  Lord and Type ",Lord_Type)
        Lord_Type_House_Lord_House = [Lord_Type,House_Lord,Lord_House]
        return Lord_Type_House_Lord_House
        

                                
                                
    def computing(self,*args,**kwargs):
        name_dict = self.retrieve_planet_name()
        name_list = []
        for key,name in name_dict.items():
            name_list.append(name)
        #print(name_list)
        x = name_list
        bhava_score = self.planet_rule_and_sit_check()
        nak_score = self.nak_check()
        rasi_score = self.rasi_check()
        nav_score = self.nav_check()
        
        update_bhava = []
        update_nak = []
        update_rasi = []
        update_nav = []
        total_scorev0 = [] #arithmatic magnitude
        total_scorev1 = [] #mean
        total_scorev2 = [] #mid
        total_scorev3=[] #amplifying magnitude
        total_scorev4 =[] #reverse amplifying magnitude
        #v0 < v3
        #v2 < v1
        total_min = []
        total_max = []
        for bva in bhava_score:
            bva *= (100/12)*2.5
            update_bhava.append(bva)
        for nak in nak_score:
            nak *= (100/12)*1.5
            update_nak.append(nak)
        for rasi in rasi_score:
            rasi *= (100/12)*1
            update_rasi.append(rasi)
        for nav in nav_score:
            nav *= (100/12)*5
            update_nav.append(nav)
        
           
        for b,n,r,v in zip(update_bhava,update_nak,update_rasi,update_nav):
            temp = [b,n,r,v]
            #print("\n b,n,r,v", b,",",n,",",r,",",v)
            neg = 0
            pos = 0
            for num in temp:
                if num < 0:
                    neg += num *(-1)
                if num > 0:
                    pos += num
            weight = max(neg,pos) #max
            #total_scorev3.append(weight)
            if weight == neg:
                weight *= -1
                #print("\n Negative : ", neg)
                total_scorev3.append(weight)
            if weight == pos:
                #print("\n Positive : ", pos)
                total_scorev3.append(weight)
            
            
                
            
                     
            total_scorev0.append(b+n+r+v)
            total_scorev1.append((b+n+r+v)/4)
            total_min.append(min(b,n,r,v))
            total_max.append(max(b,n,r,v))
            minimum = min(b,n,r,v) 
            maximum = max(b,n,r,v)
            xid= maximum+minimum
            if minimum > 0:
                    xis = (maximum-minimum)/2
            else:
                    xis = (maximum+minimum)/2
                    
            
            
            total_scorev2.append(xis)
            total_scorev4.append(xid/2)
            
        final_score = []
        c = 0
        for v0,v1,v2,v3,v4 in zip(total_scorev0,total_scorev1,total_scorev2,total_scorev3,total_scorev4):
            temp = v3
            #temp += (total_max[c]+total_min[c])/2
            #temp *= 1/5 
            c += 1
            
            final_score.append(temp)
        plt.style.use("cyberpunk")
        #plt.plot(x,final_score,marker="x",color="w")
        #plt.plot(x,total_scorev0,marker="o")#normal arthm
        #plt.plot(x,total_scorev1,marker="o",color="b")#normal mean
        #plt.plot(x,total_scorev2,marker="v",color="r")#normal mid
        #plt.plot(x,total_scorev3,marker="x")#amp mag
        #plt.plot(x,total_scorev4,marker="o")# arthm amp mag
        #plt.plot(x,total_max,marker="x",color="c")
        #plt.plot(x,total_min,marker="x",color="c")
        #plt.plot(x,update_bhava,marker="v")
        #plt.plot(x,update_rasi,marker="v")
        #plt.plot(x,update_nav,marker="v")
        #plt.plot(x,update_nak,marker="v",linestyle="solid")
        """mplcyberpunk.add_glow_effects()"""
        #plt.show()
        result_list = [final_score,total_scorev0,total_scorev2,total_scorev3,total_scorev4,total_max,total_min,update_bhava,update_rasi,update_nav,update_nak]
        return result_list
        """for i in y:
            mark += i
        print("Total Score : ", total_score, "and ", mark)"""
        
        """plt.plot(x,y,marker="o",linestyle="solid", color="g", label ="Nakshatra Strength")
        plt.title("Datagtram")
        plt.xlabel("\n Planet")
        plt.ylabel("\n Trait")
        plt.legend()
        plt.show()"""
        
#========= Calculation C End ===========

        
    def zero_setting(self,scorelist):
        index = 0 
        for score in scorelist:
            if isinstance(score,str):
                scorelist[index] = 0
            index += 1
        return scorelist
    
    #UTIF
    def nak_check(self,*args,**kwargs):
        nak = self.retrieve_nak()[:9]
        print("\n   nak ", nak)
        lord_dict = self.retrieve_nak_lord()
        lord_list = []
        #print("\n  lord_dict ", lord_dict)
        for n in nak:
            for k in lord_dict:
                   if n == k: 
                       lord_list.append(lord_dict[k])
                   else:
                       pass
                   
        #print("\n  lord_list ", lord_list)              
        planet_list = []
        own_score = [0,0,0,0,0,0,0,0,0]       
        for planet in range(1,10):
            planet_list.append(planet)
        for lord,planet in zip(lord_list,planet_list):
                      if lord == str(planet):
                          #print("\n lord is ", lord , "  planet is ", planet )
                          own_score[planet-1] = 12
                      
        friend_dict = self.retrieve_friend()           
        friend_score = self.friend_or_foe(lord_list,friend_dict,12)   
        foe_dict = self.retrieve_foe()
        foe_score = self.friend_or_foe(lord_list,foe_dict,-12)
        neutral_dict = self.retrieve_neutral()
        neutral_score = self.friend_or_foe(lord_list,neutral_dict,0)
        #print("\n Own score ", own_score)
        #print("\n Fri score", friend_score)
        #print("\n Foe score ", foe_score)
        #print("\n Neu score ", neutral_score)
        
        total_score = []
        for o,f,e,n in zip(own_score,friend_score,foe_score,neutral_score):
            total_score.append(o+f+e+n)
        
        #print("\n Total score ", total_score)
        return total_score
        
    def friend_or_foe(self,lord_list,nature_dict,val,*args,**kwargs):  
        planet_list = []
        for planet in range(1,10):
            planet_list.append(planet)
        nature_score = [0,0,0,0,0,0,0,0,0]
        i = 0
        for nature,nature_list in nature_dict.items():
            for lord,planet in zip(lord_list,planet_list):
                if lord == nature:
                   for actor in nature_list:
                       if actor == str(planet):
                            nature_score[planet-1] += val
                            break          
        return nature_score
                            
                    
                    
        
        
        
        #UTIF
    def nav_check(self,*args,**kwargs):
        navam = self.retrieve_navam()[:9]
        nav_score = self.property_check(navam)
        #print("\n  Navam Checking : ", nav_score)
        #print("\n Navam Rasi : ", navam)
        lord_dict = self.retrieve_rasi_own()
        friend_dict = self.retrieve_friend()
        fri_score = self.identifier(lord_dict,navam,friend_dict,6)
        foe_dict = self.retrieve_foe()
        foe_score = self.identifier(lord_dict,navam,foe_dict,-6)
        score_list = []
        
        for fr,fo,nv in zip(fri_score,foe_score,nav_score):
           score_list.append(fr+fo+nv)
        #print("\n Score List : ", score_list)
        
        return score_list
        
        #friend or foe identifing
    def identifier(self,lord_dict,rasi_list,nature_dict,val):
        lord_list = []
        for nav in rasi_list:
            for rasi,lord in lord_dict.items():
                if nav == rasi:
                    lord_list.append(lord)
        #print(lord_list)
        pscore = [0,0,0,0,0,0,0,0,0]
        p = 0
        for lord in lord_list:
            f = nature_dict[str(p+1)]
            for lo in lord:
                for fr in f:
                    if lo == fr:
                        pscore[p] += val           
            p+=1
        return pscore
            
        
    
    def rasi_check(self,*args,**kwargs):
        ra = self.retrieve_rasi()[:9] #L မပါ
        rasi_score = self.property_check(ra)
        lord_dict = self.retrieve_rasi_own()
        friend_dict = self.retrieve_friend()
        fri_score = self.identifier(lord_dict,ra,friend_dict,6)
        foe_dict = self.retrieve_foe()
        foe_score = self.identifier(lord_dict,ra,foe_dict,-6)
        score_list = []
        
        for fr,fo,rs in zip(fri_score,foe_score,rasi_score):
           score_list.append(fr+fo+rs)
        #print("\n rasi Score ", rasi_score)
        #print("\n friend Score ", fri_score)
        #print("\n foe Score ", foe_score)
        #print("\n Score List : ", score_list)
        
        return score_list
        
        
        ## UITF
                        
    def property_check(self,rasi,*args,**kwargs):
        uch_score = self.uch_check(rasi)
        own_score = self.own_check(rasi)
        nech_score = self.nech_filter(rasi)
        rev_score = self.rev_filter(rasi)
        Member = [uch_score,own_score,nech_score,rev_score]
        index = len(Member) 
        for scorelist,i in zip(Member,range(index)):
            scorelist = self.zero_setting(scorelist)
            Member[i] = scorelist
        Ans = [0,0,0,0,0,0,0,0,0]
        for mem in Member:
          i = 0
          for m in mem:
              Ans[i] += m
              i += 1
        return Ans
              
          
    def uch_check(self,rasi,*args,**kwargs):
        rasi_uch = self.retrieve_rasi_uch()
        score = self.check(rasi,rasi_uch)
        return score
     
    def own_check(self,rasi,*args,**kwargs):
        rasi_own = self.retrieve_rasi_own()
        score = self.check(rasi,rasi_own)
        return score
    
    def nech_filter(self,rasi,*args,**kwargs):
        rasi_nech = self.retrieve_rasi_nech()
        score = self.filter(rasi,rasi_nech)
        return score
        
    def rev_filter(self,rasi,*args,**kwargs):
        rasi_rev = self.retrieve_rasi_rev()
        score = self.filter(rasi,rasi_rev)
        return score
        
    def  filter(self,rasi,rasi_property):
        score = []
        planet = []
        for p in range(1,10):
            p = str(p)
            planet.append(p)
            score.append(p)
            
        for p,r in zip(planet,rasi):
           for rs,plist in rasi_property.items():
              if rs == r:
                  for pt in plist:
                      if pt == p:
                          i = int(p)-1
                          ck = score[i]
                          if isinstance(ck,str):
                              #print("\n \n rasi ", rs , " \n \n planet", pt)
                              score[i] = -6
                          elif isinstance(ck,(int,float)):
                              score[i] -= 6
                  break
        return score
        
    def check(self,rasi,rasi_property):
        score = []
        planet = []
        for p in range(1,10):
            p = str(p)
            planet.append(p)
            score.append(p)
            
        for p,r in zip(planet,rasi):
           for rs,plist in rasi_property.items():
              if rs == r:
                  for pt in plist:
                      if pt == p:
                          i = int(p)-1
                          ck = score[i]
                          if isinstance(ck,str):
                              score[i] = 6
                          elif isinstance(ck,(int,float)):
                              score[i] += 6
                  break
        return score
                
            
            