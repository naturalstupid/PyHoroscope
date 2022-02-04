nakshatra = ["Ashwini","Bharani","Krittika","Rohini","Mrigshira","Ardra","Punarvasu","Pushya","Ashlesha",
    "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyestha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Satabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
    "Abhijit"]
raasi=['Mesham','Rishabam','Mithunam','Katakam','Simmam','Kanni','Thulaam','Vrichigam','Dhanusu','Makaram','Kumbam','Meenam']
TaraConst = [
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0],
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0],
            [1.5, 1.5, 0.0, 1.5, 0.0, 1.5, 0.0, 1.5, 1.5],
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0],
            [1.5, 1.5, 0.0, 1.5, 0.0, 1.5, 0.0, 1.5, 1.5],
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0],
            [1.5, 1.5, 0.0, 1.5, 0.0, 1.5, 0.0, 1.0, 1.0],
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0],
            [3.0, 3.0, 1.5, 3.0, 1.5, 3.0, 1.5, 3.0, 3.0]
            ]
animalMappings = [0,1,2,3,3,4,5,2,5,
                  6,6,7,8,9,8,9,10,10,
                  4,11,12,11,13,0,13,7,1,
                  12]
mahendra_porutham_array = [4, 7, 10, 13, 16, 19, 22, 25]
#vedha_pair = [[1,18], [2,17], [3,16], [4,15], [5,23], [6,22], [7,21], [8,20],[9,19], [10,27], [11,26], [12,25], [13,24] ]
vedha_pair_sum = [19,28,37]
nakshatra = ["Ashwini","Bharani","Krittika","Rohini","Mrigshira","Ardra","Punarvasu","Pushya","Ashlesha",
    "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyestha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Satabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
    "Abhijit"]
head_rajju = [5,14,23] # 5, 5+9, 14+9 (5,(9))
neck_rajju = [4,6,13,15,22,24] # 4, 4+2, 6+7, 13+2, 15+7, 22+2 (4,(2,7,2,7,2))
stomach_rajju = [3,7,12,16,21,25] # 3, 3+4, 7+5, 12+4, 16+5, 21+4 (3,(4,5,4,5,4))
waist_rajju = [2,8,11,17,20,26] # 2, 2+6, 8+3, 11+6, 17+3, 20+6 (2, (6,3,6,3,6))
foot_rajju = [1,9,10,18,19,27] # 1, 1+8, 9+1, 10+8, 18+1, 19+8 (1, (8,1,8,1,8)
YoniArray = [
            [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 1, 3, 2, 1],
            [2, 4, 3, 3, 2, 2, 2, 2, 3, 1, 2, 3, 2, 0],
            [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 3, 1],
            [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 0, 2],
            [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 2, 1, 1],
            [2, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 3, 2, 1],
            [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 2, 1, 2],
            [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 1],
            [0, 3, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 1],
            [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 1, 2, 1],
            [1, 2, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 2, 1],
            [3, 3, 0, 2, 2, 3, 2, 2, 2, 1, 2, 4, 3, 2],
            [2, 2, 3, 0, 1, 2, 1, 2, 2, 2, 2, 3, 4, 2],
            [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 4]
    ]
VarnaArray = [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]
VasyaArray  =[
            [2.0, 0.5, 1.0, 0.0, 2.0],
            [0.5, 2.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 2.0, 2.0, 2.0],
            [0.0, 0.0, 2.0, 2.0, 0.0],
            [1.0, 0.0, 1.0, 0.0, 2.0]]
GanArray = [[6, 5, 1], [6, 6, 0], [0, 0, 6]] ## Based on saravali.de (Maitri)
MaitriMappings = [2,5,3,1,0,3,5,2,4,6,6,4]
MaitriArray = [
            [5.0, 5.0, 5.0, 4.0, 5.0, 0.0, 0.0],
            [5.0, 5.0, 4.0, 1.0, 4.0, 0.5, 0.5],
            [5.0, 4.0, 5.0, 0.5, 5.0, 3.0, 0.5],
            [4.0, 1.0, 0.5, 5.0, 0.5, 5.0, 4.0],
            [5.0, 4.0, 5.0, 0.5, 5.0, 0.5, 3.0],
            [0.0, 0.5, 3.0, 5.0, 0.5, 5.0, 5.0],
            [0.0, 0.5, 0.5, 4.0, 3.0, 5.0, 5.0]]
BahkutArray = [
            [7, 0, 7, 7, 0, 0, 7, 0, 0, 7, 7, 0],
            [0, 7, 0, 7, 7, 0, 0, 7, 0, 0, 7, 7],
            [7, 0, 7, 0, 7, 7, 0, 0, 7, 0, 0, 7],
            [7, 7, 0, 7, 0, 7, 7, 0, 0, 7, 0, 0],
            [0, 7, 7, 0, 7, 0, 7, 7, 0, 0, 7, 0],
            [0, 0, 7, 7, 0, 7, 0, 7, 7, 0, 0, 7],
            [7, 0, 0, 7, 7, 0, 7, 0, 7, 7, 0, 0],
            [0, 7, 0, 0, 7, 7, 0, 7, 0, 7, 7, 0],
            [0, 0, 7, 0, 0, 7, 7, 0, 7, 0, 7, 7],
            [7, 0, 0, 7, 0, 0, 7, 7, 0, 7, 0, 7],
            [7, 7, 0, 7, 7, 0, 0, 7, 7, 0, 7, 0],
            [0, 7, 7, 0, 0, 7, 0, 0, 7, 7, 0, 7]
    ]
NadiArray = [[0, 8, 8], [8, 0, 8], [8, 8, 0]]
class Ashtakoota:
    """
        To compute Marriage compatibility score Ashtakoota system based on boy and girl's birth star
        @param boy_nakshatra_number: boy's nakshatra number [1 to 27]
        @param boy_paadham_number: boy's nakshatra paadham number [1 to 4]
        @param girl_nakshatra_number: girl's nakshatra number [1 to 27]
        @param girl_paadham_number: girl's nakshatra paadham number [1 to 4]
    """
    def __init__(self,boy_nakshatra_number,boy_paadham_number,girl_nakshatra_number,girl_paadham_number):
        self.boy_nakshatra_number=boy_nakshatra_number-1
        self.girl_nakshatra_number=girl_nakshatra_number-1
        self.boy_paadham_number = boy_paadham_number
        self.girl_paadham_number = girl_paadham_number
        self.boy_raasi_number=self._raasi_from_nakshatra_pada(boy_nakshatra_number, boy_paadham_number)
        self.girl_raasi_number=self._raasi_from_nakshatra_pada(girl_nakshatra_number, girl_paadham_number)
    def varna_koota(self): # Varna Porutham
        """
            To compute varna koota / Varna Porutham for the given boy/girl birth star combination
            Returns the score in the range [0..3]
        """
        Bvkpoint = 3
        Gvkpoint = 3
        if (self.boy_raasi_number in [4,8,12]):
            Bvkpoint = 0 # Brahmin
        elif (self.boy_raasi_number in [1,5,9]):
            Bvkpoint = 1 #Kshatriya
        elif (self.boy_raasi_number in [2,6,10]):
            Bvkpoint = 2 # Vaishya
        if (self.girl_raasi_number in [4,8,12]):
            Gvkpoint = 0 # Brahmin
        elif (self.girl_raasi_number in [1,5,9]):
            Gvkpoint = 1 # Kshatriya
        elif (self.girl_raasi_number in [2,6,10]):
            Gvkpoint = 2 # Vaishya
#        print(Gvkpoint,Bvkpoint,VarnaArray[Gvkpoint][Bvkpoint])
        return VarnaArray[Gvkpoint][Bvkpoint]

    def vasya_koota(self): #vasiya porutham
        """
            To compute vasya koota / vasiya porutham for the given boy/girl birth star combination
            Returns the score in the range [0.5,0,5,1.0,2.0]
        """
        chatushpada = lambda r,p: r in[1,2] or (r==9 and p in[3,4]) or (r==10 and p in[1,2])
        manava = lambda r,p: r in[3,6,7,11] or (r==9 and p in[1,2])
        vanachara = lambda r: r == 5
        jalachara = lambda r,p: r in[4,12] or (r==10 and p in[3,4])
        keeta = lambda r: r==8
        #Quadruped  Chatushpada
        if (chatushpada(self.boy_raasi_number,self.boy_paadham_number)):
            Bvkpoint = 0
        elif (manava(self.boy_raasi_number,self.boy_paadham_number)):
            Bvkpoint = 1
        elif (jalachara(self.boy_raasi_number,self.boy_paadham_number)):
            Bvkpoint = 2
        elif (vanachara(self.boy_raasi_number)):
            Bvkpoint = 3
        else: #Keeta
            Bvkpoint = 4
        if (chatushpada(self.girl_raasi_number,self.girl_paadham_number)):
            Gvkpoint = 0
        elif (manava(self.girl_raasi_number,self.girl_paadham_number)):
            Gvkpoint = 1
        elif (jalachara(self.girl_raasi_number,self.girl_paadham_number)):
            Gvkpoint = 2
        elif (vanachara(self.girl_raasi_number)):
            Gvkpoint = 3
        else: #keeta
            Gvkpoint = 4
#        print(Gvkpoint,Bvkpoint,VasyaArray[Gvkpoint][Bvkpoint])
        return VasyaArray[Gvkpoint][Bvkpoint]
    def dina_koota(self): #dina porutham
        """
            To compute dina / tara koota / dina porutham for the given boy/girl birth star combination
            Returns the score in the range [0, 1.5, 3.0]
        """
        res = 0.0
        count = (self.boy_nakshatra_number - self.girl_nakshatra_number)

        if (count <= 0):
            count = count + 27
        count = count % 9
        if ((count % 2) == 0):
            res += 1.5
        else:
            res += 0
        count = (self.girl_nakshatra_number - self.boy_nakshatra_number)
        if (count <= 0):
            count = count + 27
        count = count % 9
        if ((count % 2) == 0):
            res += 1.5
        else:
            res += 0
        return res
    def gana_koota(self): #Gana Porutham
        """
            To compute gana koota / Gana Porutham for the given boy/girl birth star combination
            Returns the score in the range [0, 1, 5, 6]
        """
        boy_gana = self._find_gana(self.boy_nakshatra_number)
        girl_gana = self._find_gana(self.girl_nakshatra_number)
        return GanArray[girl_gana][boy_gana]
    def _find_gana(self,nak):
        gana=-1
        if (nak in [0,4,6,7,12,14,16,21,26]):
            gana= 0 
        elif (nak in [1,3,5,10,11,19,20,24,25]):
            gana= 1 
        elif (nak in [2,8,9,13,15,17,18,22,23]):
            gana= 2
        return gana
    def yoni_koota(self): # Yoni Porutham
        """
            To compute yoni koota / Yoni Porutham for the given boy/girl birth star combination
            Returns the score in the range [0..4]
        """
        return YoniArray[animalMappings[self.girl_nakshatra_number]][animalMappings[self.boy_nakshatra_number]]
    def maitri_koota(self): #Raasi adhipathi porutham
        """
            To compute maitri koota / Raasi adhipathi porutham for the given boy/girl birth star combination
            Returns the score in the range [0, 0.5, 1.0, 3.0, 4.0, 5.0]
        """
        return MaitriArray[MaitriMappings[self.girl_raasi_number-1]][MaitriMappings[self.boy_raasi_number-1]]
    def bahkut_koota(self): # Raasi Porutham
        """
            To compute bahut koota / Raasi Porutham for the given boy/girl birth star combination
            Returns the score in the range [0 or 7]
        """
        return BahkutArray[self.girl_raasi_number-1][self.boy_raasi_number-1]
    def naadi_koota(self):
        """
            To compute naadi koota for the given boy/girl birth star combination
            Returns the score in the range [0 or 8]
        """
        bv = 2
        gv = 2 
        if (self.boy_nakshatra_number in [0,5,6,11,12,17,18,23,24]):
            bv = 0
        if (self.girl_nakshatra_number in [0,5,6,11,12,17,18,23,24]):
            gv = 0
        if (self.boy_nakshatra_number in [1,4,7,10,13,16,19,22,25]):
            bv = 1
        if (self.girl_nakshatra_number in [1,4,7,10,13,16,19,22,25]):
            gv = 1
        return NadiArray[gv][bv]
    def mahendra_porutham(self):
        """
            To compute mahendra porutham for the given boy/girl birth star combination
            Returns the score as True or False
        """
        rem = (self.girl_nakshatra_number + 27 - self.boy_nakshatra_number) % 27
        return rem in mahendra_porutham_array        
    def vedha_porutham(self):
        """
            To compute vedha porutham for the given boy/girl birth star combination
            Returns the score as True or False
        """
        bn = self.boy_nakshatra_number+1
        gn = self.girl_nakshatra_number+1
        vedha = not (bn+gn in vedha_pair_sum)
        return vedha
    def rajju_porutham(self):
        """
            To compute rajju porutham for the given boy/girl birth star combination
            Returns the score as True or False
        """
        bn = self.boy_nakshatra_number+1
        gn = self.girl_nakshatra_number+1
        if (bn in head_rajju) and (gn in head_rajju):
            return False
        elif (bn in neck_rajju) and (gn in neck_rajju):
            return False
        elif (bn in stomach_rajju) and (gn in stomach_rajju):
            return False
        elif (bn in waist_rajju) and (gn in waist_rajju):
            return False
        elif (bn in foot_rajju) and (gn in foot_rajju):
            return False
        else:
            return True
    def sthree_dheerga_porutham(self):
        """
            To compute sthree dheerga porutham for the given boy/girl birth star combination
            Returns the score as True or False
        """
        return ( (self.boy_nakshatra_number + 27 - self.girl_nakshatra_number) % 27 > 13) # > 9)
    def compatibility_score(self):
        """
            To computer total ashta koota score (sum of all eight koota values)
            Return score ranges from 0 to 36 in steps of 0.5
            @return returns the following values as a list:
            varna_koota, vasya_koota, gana_koota, tara_koota, 
            yoni_koota, maitri_koota, bahkut_koota, naadi_koota,
            compatibility_score,
            mahendra_porutham,vedha_porutham,rajju_porutham,sthree_dheerga_porutham]
        """
        varna_koota = self.varna_koota()
        vasya_koota = self.vasya_koota()
        gana_koota = self.gana_koota()
        tara_koota = self.dina_koota() # dina_koota is same as tara koota
        yoni_koota = self.yoni_koota()
        maitri_koota= self.maitri_koota()
        bahkut_koota= self.bahkut_koota()
        naadi_koota = self.naadi_koota()
        compatibility_score = varna_koota+vasya_koota+gana_koota+tara_koota+yoni_koota+maitri_koota+bahkut_koota+naadi_koota
        mahendra_porutham=self.mahendra_porutham()
        vedha_porutham=self.vedha_porutham()
        rajju_porutham=self.rajju_porutham()
        sthree_dheerga_porutham=self.sthree_dheerga_porutham()
        return [varna_koota, vasya_koota, gana_koota, tara_koota, yoni_koota, maitri_koota, bahkut_koota, naadi_koota,compatibility_score,mahendra_porutham,vedha_porutham,rajju_porutham,sthree_dheerga_porutham]
    def _raasi_from_nakshatra_pada(self,nakshatra_number,paadha_number):
        nakshatra_duration = 360/27.
        raasi_duration = 360/12.
#        print('nakshatra_duration',nakshatra_duration)
        paadha_duration = nakshatra_duration / 4.
#        print('paadha_duration',paadha_duration)
        total_duration = ((nakshatra_number-1)*nakshatra_duration)+((paadha_number-1)*paadha_duration)+0.5*paadha_duration
#        print('total_duration',total_duration)
        raasi_number = int(total_duration / raasi_duration)+1
#        print('nakshatra'+nakshatra[nakshatra_number-1]+' paadham-'+str(paadha_number)+' is raasi',raasi[raasi_number-1])
        return raasi_number
def _generate_full_compatability_matrix():
  import codecs
  outFile = 'all_nak_pad_boy_girl.txt'
  fp = codecs.open(outFile, encoding='utf-8', mode='w')
  for bn in range(27):
      for bp in range(4):
          for gn in range(27):
              for gp in range(4):
                  a = Ashtakoota(bn+1,bp+1,gn+1,gp+1)
                  # [total,m,v,r,s] = a.compatibility_score()[8:]
                  results = a.compatibility_score()
                  print('processing',bn+1,bp+1,gn+1,gp+1)
                  print([bn+1,bp+1,gn+1,gp+1],results, file=fp)
  fp.close()
if __name__ == "__main__":
    _generate_full_compatability_matrix()
    exit()
    boy_nakshatra_number = 16
    boy_paadham_number = 3
    girl_nakshatra_number = 14
    girl_paadham_number = 4
    a = Ashtakoota(boy_nakshatra_number,boy_paadham_number,girl_nakshatra_number,girl_paadham_number)
    [varna_koota, vasya_koota, gana_koota, tara_koota, yoni_koota, maitri_koota, bahkut_koota, naadi_koota,compatibility_score,mahendra_porutham,vedha_porutham,rajju_porutham,sthree_dheerga_porutham] = \
        a.compatibility_score()
    print('varna_koota',varna_koota)  
    print('vasya_koota',vasya_koota)
    ### dina koota same as tara_koota  
    #  print('dina_koota',a.dina_koota())  
    print('gana_koota',gana_koota)
    print('tara_koota',tara_koota)  
    print('yoni_koota',yoni_koota)  
    print('maitri_koota',maitri_koota)  
    print('bahkut_koota',bahkut_koota)  
    print('naadi_koota',naadi_koota)
    print('mahendra_porutham',a.mahendra_porutham())
    print ('vedha_porutham',a.vedha_porutham())
    print('rajju_porutham',a.rajju_porutham())
    print('sthree_dheerga_porutham',a.sthree_dheerga_porutham())
    print(" Total Marriage Compatibility Factor between Boy's nakshatram:"+nakshatra[boy_nakshatra_number-1]+' Paadham-'+str(boy_paadham_number)+ \
    " and Girl's nakshatram:"+nakshatra[girl_nakshatra_number-1]+' Paadham-'+str(girl_paadham_number)+' is '+ str(compatibility_score) +' out of 36 ' )
    exit()
