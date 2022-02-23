#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# py -- routines for computing tithi, vara, etc.
#
# Copyright (C) Sundar Sundaresan, USA. carnaticmusicguru2015@comcast.net
# Downloaded from https://github.com/naturalstupid/pyhoroscope
#
# This file is part of the "drik-panchanga" Python library
# for computing Hindu luni-solar calendar based on the Swiss ephemeris
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import swisseph as swe
from _datetime import datetime, timedelta
from datetime import date
panchanga = __import__('panchanga')

class Horoscope():  
    def __init__(self,place_with_country_code=None,latitude=None,longitude=None,timezone_offset=None,date_in=None,birth_time=None,ayanamsa_mode="Lahiri",ayanamsa_value=None):
        self.place_name = place_with_country_code
        self.latitude = latitude
        self.longitude = longitude
        self.timezone_offset = timezone_offset
        self.date = date_in
        self.birth_time = birth_time
        self.ayanamsa_mode = ayanamsa_mode
        self.ayanamsa_value = ayanamsa_value
        #print(self.place_name,self.latitude,self.longitude,self.timezone_offset)
        if self.place_name == None:
            if self.latitude==None or self.longitude==None or self.timezone_offset==None:
                print('Please provide either place_with_country_code or combination of latitude and longitude ...\n Aborting script')
                exit()
            else:
                self.place_name = 'Not Provided'
                self.latitude = latitude
                self.longitude = longitude
                self.timezone_offset = timezone_offset                
        else:
            if self.latitude==None or self.longitude==None or self.timezone_offset==None:
                [_,self.latitude,self.longitude,self.timezone_offset] = \
                    panchanga.get_latitude_longitude_from_place_name(place_with_country_code)
                
                
        if date_in==None:
            self.date = panchanga.Date(date.today().year,date.today().month,date.today().day)
        else:
            self.date = panchanga.Date(date_in.year,date_in.month,date_in.day)
        self.julian_utc = panchanga.gregorian_to_jd(self.date)
        #self.timezone_offset = panchanga.get_place_timezone_offset(self.latitude,self.longitude)
        """ !!!!!!!!!!!! Including birth time gives WRONG RESULTS !!!!!!!!! """
        """ TODO Handle BC date using Panchanga Date Struct """
        if (birth_time!=None):
            """ TODO Convert time to 24 hr time """
            birth_time = birth_time.strip().replace('AM','').replace('PM','')
            btArr = birth_time.split(':')
            self.julian_day = swe.julday(self.date.year,self.date.month,self.date.day, int(btArr[0])+int(btArr[1])/60)
            self.birth_time = (int(btArr[0]),int(btArr[1]),0)
            if (len(btArr)==3):
                self.julian_day = swe.julday(self.date.year,self.date.month,self.date.day, int(btArr[0])+int(btArr[1])/60+int(btArr[2])/3600)
                self.birth_time = (int(btArr[0]),int(btArr[1]),int(btArr[2]))                
        else:
            self.julian_day = panchanga.gregorian_to_jd(self.date)
        # Set Ayanamsa Mode
        key = ayanamsa_mode.upper()
        #print('horoscope setting ayanamsa',key,self.ayanamsa_value,self.julian_day)
        panchanga.set_ayanamsa_mode(key,self.ayanamsa_value,self.julian_day)
        self.ayanamsa_value = panchanga.get_ayanamsa_value(self.julian_day)
        return
    def _get_planet_list(self):
        global PLANET_NAMES
        return PLANET_NAMES
    def _get_calendar_resource_strings(self, language='en'):
      inpFile = 'list_values_'+language+'.txt'
      msgFile = 'msg_strings_'+language+'.txt'
      cal_key_list=panchanga.read_list_types_from_file(msgFile)
      global PLANET_NAMES,NAKSHATRA_LIST,TITHI_LIST,RAASI_LIST,KARANA_LIST,DAYS_LIST,PAKSHA_LIST,YOGAM_LIST,MONTH_LIST,YEAR_LIST,DHASA_LIST,BHUKTHI_LIST
      [PLANET_NAMES,NAKSHATRA_LIST,TITHI_LIST,RAASI_LIST,KARANA_LIST,DAYS_LIST,
       PAKSHA_LIST,YOGAM_LIST,MONTH_LIST,YEAR_LIST,DHASA_LIST,BHUKTHI_LIST
      ] = panchanga.read_lists_from_file(inpFile)
      return cal_key_list
    def get_calendar_information(self, language='en', as_string=False):
        jd = self.julian_utc # self.julian_day
        place = panchanga.Place(self.place_name,self.latitude,self.longitude,self.timezone_offset)
        cal_key_list = self._get_calendar_resource_strings(language)
        calendar_info = {
            cal_key_list['place_str'] : self.place_name,
            cal_key_list['latitude_str'] : panchanga.to_dms(self.latitude,is_lat_long='lat'), #"{0:.2f}".format(self.latitude),
            cal_key_list['longitude_str'] : panchanga.to_dms(self.longitude,is_lat_long='long'), # "{0:.2f}".format(self.longitude),
            cal_key_list['timezone_offset_str'] : "{0:.2f}".format(self.timezone_offset),
            cal_key_list['report_date_str'] : "{0:d}-{1:d}-{2:d}".format(self.date.year,self.date.month,self.date.day)#self.date.isoformat(),         
        }
        vaaram = panchanga.vaara(jd,as_string)
        calendar_info[cal_key_list['vaaram_str']]=vaaram
        jd = self.julian_day
        is_bc_year = self.date.year < 0
        if (is_bc_year):
            maasam_no = panchanga.maasa(jd,place,False)[0]
            maasam = MONTH_LIST[maasam_no-1]
            calendar_info[cal_key_list['maasa_str']] = maasam
        else:
            [maasam_no,day_no] = [panchanga.maasa(jd,place,False)[0], panchanga.tamil_date(self.date,jd, place)]
            maasam = MONTH_LIST[maasam_no-1]
            calendar_info[cal_key_list['maasa_str']] = maasam +" "+cal_key_list['date_str']+' '+str(day_no)
        [kali_year, vikrama_year,saka_year] = panchanga.elapsed_year(jd,maasam_no)
        calendar_info[cal_key_list['kali_year_str']] = kali_year
        calendar_info[cal_key_list['vikrama_year_str']] = vikrama_year
        calendar_info[cal_key_list['saka_year_str']] = saka_year
        _samvatsara = panchanga.samvatsara(jd,maasam_no,as_string)
        calendar_info[cal_key_list['samvatsara_str']] = _samvatsara
        sun_rise = panchanga.sunrise(self.julian_utc,place,as_string)
        calendar_info[cal_key_list['sunrise_str']] = sun_rise[1]
        sun_set = panchanga.sunset(self.julian_utc,place,as_string)
        calendar_info[cal_key_list['sunset_str']] = sun_set[1]
        moon_rise = panchanga.moonrise(self.julian_utc,place,as_string)
        calendar_info[cal_key_list['moonrise_str']] = moon_rise
        moon_set = panchanga.moonset(self.julian_utc,place,as_string)
        calendar_info[cal_key_list['moonset_str']] = moon_set
        """ for tithi at sun rise time - use Julian UTC  """
        calendar_info[cal_key_list['tithi_str']]= panchanga.tithi(self.julian_utc,place,as_string)
        jd = self.julian_day
        calendar_info[cal_key_list['raasi_str']] = panchanga.get_raasi_new(jd,place,as_string)
        calendar_info[cal_key_list['nakshatra_str']] = panchanga.nakshatra(jd,place,as_string)
        self._nakshatra_number, self._paadha_number,_=panchanga.nakshatra(jd,place,as_string=False)
        """ # For kaalam, yogam use sunrise time """
        jd = self.julian_utc 
        _raahu_kaalam = panchanga.raahu_kaalam(jd,place,as_string)
        calendar_info[cal_key_list['raahu_kaalam_str']] = _raahu_kaalam
        kuligai = panchanga.gulikai_kaalam(jd,place,as_string)
        calendar_info[cal_key_list['kuligai_str']] = kuligai
        yamagandam = panchanga.yamaganda_kaalam(jd,place,as_string)
        calendar_info[cal_key_list['yamagandam_str']] = yamagandam
        yogam = panchanga.yoga(jd,place,as_string)
        calendar_info[cal_key_list['yogam_str']] = yogam
        karanam = panchanga.karana(jd,place,as_string)
        calendar_info[cal_key_list['karanam_str']] = karanam
        abhijit = panchanga.abhijit_muhurta(jd,place,as_string)
        calendar_info[cal_key_list['abhijit_str']] = abhijit
        _dhurmuhurtham = panchanga.durmuhurtam(jd,place,as_string)
        calendar_info[cal_key_list['dhurmuhurtham_str']] = _dhurmuhurtham
        return calendar_info
    def get_horoscope_information(self,language='en', as_string=False):
        horoscope_info = {}
        cal_key_list = self._get_calendar_resource_strings(language)
        dhasavarga_dict={2:cal_key_list['hora_str'],
                         3:cal_key_list['drekkanam_str'],
                         7:cal_key_list['saptamsam_str'],
                         9:cal_key_list['navamsam_str'],
                         10:cal_key_list['dhasamsam_str'],
                         16:cal_key_list['dhwadamsam_str'],
                         30:cal_key_list['thrisamsam_str'],
                         60:cal_key_list['sashtiamsam_str']
        }
        jd = self.julian_day  # For ascendant and planetary positions, dasa buthi - use birth time
        place = panchanga.Place(self.place_name,self.latitude,self.longitude,self.timezone_offset)
        _ascendant = panchanga.ascendant(jd,place,as_string)
#        horoscope_charts = [[ '' for y in range(len(dhasavarga_dict)+1) ]for x in range(len(RAASI_LIST))]
        horoscope_charts = [[ ''  for x in range(len(RAASI_LIST))] for y in range(len(dhasavarga_dict)+1)]
        chart_counter = 0
        if as_string:
            #asc_house = _ascendant[0]
            #horoscope_charts[chart_counter][asc_house] += cal_key_list['ascendant_str'] +"\n"
            asc_house = RAASI_LIST.index(_ascendant.split()[0])
            horoscope_charts[chart_counter][asc_house] += cal_key_list['ascendant_str'] +"\n"
        else:
            asc_house = _ascendant[0]
            horoscope_charts[chart_counter][asc_house] += cal_key_list['ascendant_str'] +"\n"
#        print('raasi','lagnam house',asc_house)
        horoscope_info[cal_key_list['raasi_str']+'-'+cal_key_list['ascendant_str']] = _ascendant
        # assign navamsa data
        planet_positions = panchanga.planetary_positions(jd,place,as_string)
        for sublist in planet_positions:
            #print('sublist',sublist)
            if as_string:
                planet_name = sublist[0]
                k = cal_key_list['raasi_str']+'-'+planet_name
                v = sublist[1]
                planet_house = RAASI_LIST.index(v.split()[0])
                horoscope_charts[chart_counter][planet_house] += planet_name + "\n"
                relative_planet_house = panchanga.get_relative_house_of_planet(asc_house, planet_house)
                horoscope_info[k]=v+'-House #'+str(relative_planet_house)
            else:
                planet_name = PLANET_NAMES[sublist[0]]
                k = cal_key_list['raasi_str']+'-'+planet_name
                v = sublist[:]
                #print('k',k,'v',v)
                planet_house = sublist[2]
                horoscope_charts[chart_counter][planet_house] += planet_name + "\n"
                relative_planet_house = panchanga.get_relative_house_of_planet(asc_house, planet_house)
                horoscope_info[k]=v + [relative_planet_house]
        # Shadow Sub Planet information
        dob = panchanga.Date(self.date.year,self.date.month,self.date.day)
        tob = self.birth_time
        jd = self.julian_day
        as_string=True
        k = cal_key_list['raasi_str']+'-'+cal_key_list['upagraha_str']
        horoscope_info[k]=''
        sub_planet_list_1 = {'kaala_str':'kaala_longitude','mrityu_str':'mrityu_longitude','artha_str':'artha_praharaka_longitude','yama_str':'yama_ghantaka_longitude',
                           'gulika_str':'gulika_longitude','maandi_str':'maandi_longitude'}
        sub_planet_list_2 = ['dhuma','vyatipaata','parivesha','indrachaapa','upaketu']
        place = panchanga.Place(self.place_name,self.latitude,self.longitude,self.timezone_offset)
        for sp,sp_func in sub_planet_list_1.items():
            k = cal_key_list['raasi_str']+'-'+cal_key_list[sp]
            v = eval('panchanga.'+sp_func+'(dob,tob,place,as_string='+str(as_string)+')')
            horoscope_info[k]=v
        for sp in sub_planet_list_2:
            k = cal_key_list['raasi_str']+'-'+cal_key_list[sp+'_str']
            v = eval('panchanga.'+'solar_upagraha_longitudes(jd,sp,as_string='+str(as_string)+')')
            horoscope_info[k]=v
        ## Dhasavarga Charts
        ascendant_longitude = panchanga.ascendant(jd,place,as_string=False)[1]
        for dhasavarga_factor in dhasavarga_dict.keys():
            if as_string:
                ascendant_navamsa = RAASI_LIST[panchanga.dasavarga_from_long(ascendant_longitude,dhasavarga_factor)]
                asc_house = RAASI_LIST.index(ascendant_navamsa)
                chart_counter += 1 
                horoscope_charts[chart_counter][asc_house] += cal_key_list['ascendant_str'] +"\n"
            else:
                ascendant_navamsa = panchanga.dasavarga_from_long(ascendant_longitude,dhasavarga_factor)
                asc_house = ascendant_navamsa
                chart_counter += 1 
                horoscope_charts[chart_counter][asc_house] += cal_key_list['ascendant_str'] +"\n"
            horoscope_info[dhasavarga_dict[dhasavarga_factor] +'-'+cal_key_list['ascendant_str']]=ascendant_navamsa
            planet_positions = panchanga.dhasavarga(jd,place,dhasavarga_factor,as_string)
            for sublist in planet_positions:
                #print('sublist',sublist)
                if as_string:
                    planet_name = sublist[0]
                    k = dhasavarga_dict[dhasavarga_factor]+'-'+planet_name
                    v = sublist[1]
                    planet_house = RAASI_LIST.index(v.split()[0])
                    horoscope_charts[chart_counter][planet_house] += planet_name +'\n'
                    relative_planet_house = panchanga.get_relative_house_of_planet(asc_house, planet_house)
                    horoscope_info[k]=v+'-House #'+str(relative_planet_house)
                else:
                    planet_name = PLANET_NAMES[sublist[0]]
                    k = dhasavarga_dict[dhasavarga_factor]+'-'+planet_name
                    v = sublist[:]
                    #print('k',k,'v',v)
                    planet_house = sublist[1]
                    horoscope_charts[chart_counter][planet_house] += planet_name +'\n'
                    relative_planet_house = panchanga.get_relative_house_of_planet(asc_house, planet_house)
                    horoscope_info[k]=v + [relative_planet_house]
        #print(horoscope_charts)
#       Get Dhasa Bkukthi
        jd = self.julian_day
        db = panchanga.get_dhasa_bhukthi(jd,place)
        dhasa_bhukti_info = {}
        for i in range(len(db)):
#          print(db[i])
          [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
          dhasa_bhukti_info[panchanga.get_dhasa_name(dhasa_lord)+'-'+panchanga.get_bhukthi_name(bukthi_lord)]=bukthi_start

        return horoscope_info, horoscope_charts, dhasa_bhukti_info
