#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# py -- routines for computing tithi, vara, etc.
#
# Copyright (C) 2013 Satish BD  <bdsatish@gmail.com>
# Downloaded from https://github.com/bdsatish/drik-panchanga
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

"""
Use Swiss ephemeris to calculate tithi, nakshatra, etc.
"""

from geopy.geocoders import Nominatim
from pytz import timezone, utc
from math import ceil
from collections import namedtuple as struct
import swisseph as swe
from _datetime import datetime, timedelta
from datetime import date
import math
from collections import OrderedDict as Dict
"""
NAKSHATRA_LIST=['Aswini','Bharani','Karthigai','Rohini','Mrigasheesham','Thiruvaathirai',
                'Punarpoosam','Poosam','Aayilyam','Makam','Pooram','Uthiram','Hastham','Chithirai',
                'Swaathi','Visaakam','Anusham','Kaettai','Moolam','Pooraadam','Uthiraadam','Thiruvonam',
                'Avittam','Sadhayam','Poorattathi','Uthirattathi','Revathi']
TITHI_LIST=['Prathamai','Thuthiyai','Thiruthiyai','Sathurthi','Panjami','Shasti','Sapthami','Astami',
            'Navami','Dhasami','Egadhasi','Dhuvadhasi','Thirayodasi','Sathuradasi','Pournami','Pirathamai',
            'Thuthiyai','Thiruthiyai','Sathurthi','Panjami','Shasti','Sapthami','Ashtami','Navami','Dhasami',
            'Egadhasi','Dhuvadhasi','Thirayodasi','Sathuradasi','Ammavasai']
RAASI_LIST=['Mesham','Rishabam','Mithunam','Katakam','Simmam','Kanni','Thulaam','Vrichigam',
            'Dhanusu','Makaram','Kumbam','Meenam']
KARANA_LIST=['Kimstugna-Bava','Baalava-Kauvala','Taitila-Gara','Vanija-Vishti (Bhadra)','Bava-Baalava',
             'Kauvala-Taitila','Gara-Vanija','Vishti(Bhadra)-Bava','Baalava-Kauvala','Taitila-Gara',
             'Vanija-Vishti (Bhadra)','Bava-Baalava','Kauvala-Taitila','Gara-Vanija','Vishti (Bhadra)-Bava',
             'Baalava-Kauvala','Taitila-Gara','Vanija-Vishti (Bhadra)','Bava-Baalava','Kauvala-Taitila',
             'Gara-Vanija','Vishti (Bhadra)-Bava','Baalava-Kauvala','Taitila-Gara','Vanija-Vishti (Bhadra)',
             'Bava-Baalava','Kauvala-Taitila','Gara-Vanija','Vishti (Bhadra)-Sakuna','Chatushpada-Naga']
DAYS_LIST=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
PAKSHA_LIST=['Krishna Paksha','Sukla Paksha']
"""
### String Constants
"""
    set this to =swe.PLUTO  for Vimoshotari functions. BUT KETHU will be SHOWN AS PLUTO DHASA/BHUKTI
    set this to - -10 for chart creation (otherwise chart will show Pluto for Kethu)
"""
swe.KETU = -10
swe.set_ephe_path("D:\\LaptopBackup\\Local\\Program Files (x86)\\Jagannatha Hora\\jhcore\\ephe\\")
Date = struct('Date', ['year', 'month', 'day'])
Place = struct('Place', ['Place','latitude', 'longitude', 'timezone'])

sidereal_year = 365.256360417   # From WolframAlpha
human_life_span_for_dhasa = 120. ## years
vimsottari_year = sidereal_year  # some say 360 days, others 365.25 or 365.2563 etc

# Nakshatra lords, order matters. See https://en.wikipedia.org/wiki/Dasha_(astrology)
adhipati_list = [ swe.KETU, swe.VENUS, swe.SUN, swe.MOON, swe.MARS,
                  swe.RAHU, swe.JUPITER, swe.SATURN, swe.MERCURY ]

# (Maha-)dasha periods (in years)
mahadasa = { swe.KETU: 7, swe.VENUS: 20, swe.SUN: 6, swe.MOON: 10, swe.MARS: 7,
             swe.RAHU: 18, swe.JUPITER: 16, swe.SATURN: 19, swe.MERCURY: 17 }

# assert(0 <= nak <= 26)
# Return nakshatra lord (adhipati)
adhipati = lambda nak: adhipati_list[nak % (len(adhipati_list))]


# Hindu sunrise/sunset is calculated w.r.t middle of the sun's disk
# They are geometric, i.e. "true sunrise/set", so refraction is not considered
_rise_flags = swe.BIT_DISC_CENTER + swe.BIT_NO_REFRACTION  # + swe.BIT_GEOCTR_NO_ECL_LAT
#_rise_flags = swe.BIT_HINDU_RISING 

# namah suryaya chandraya mangalaya ... rahuve ketuve namah
#swe.KETU =  swe.PLUTO  # I've mapped Pluto to Ketu
planet_list = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
               swe.VENUS, swe.SATURN,swe.RAHU,swe.KETU]#,swe.URANUS,swe.NEPTUNE,swe.PLUTO] # Rahu = MEAN_NODE
               #, swe.NEPTUNE,swe.RAHU,swe.KETU]#,swe.RAHU,swe.KETU ]
#PLANET_NAMES= ['Suriyan', 'Chandran', 'Sevvay','Budhan','Viyaazhan','VeLLi','Sani','Raahu','Kethu','Uranus','Neptune']
revati_359_50 = lambda: swe.set_sid_mode(swe.SIDM_USER, 1926892.343164331, 0)
galc_cent_mid_mula = lambda: swe.set_sid_mode(swe.SIDM_USER, 1922011.128853056, 0)
available_ayanamsa_modes = {"FAGAN":swe.SIDM_FAGAN_BRADLEY ,"KP": swe.SIDM_KRISHNAMURTI, "LAHIRI": swe.SIDM_LAHIRI, "RAMAN": swe.SIDM_RAMAN, 
                            "USHASHASHI": swe.SIDM_USHASHASHI, "YUKTESHWAR": swe.SIDM_YUKTESHWAR, "SURYASIDDHANTA": swe.SIDM_SURYASIDDHANTA,
                            "SURYASIDDHANTA_MSUN": swe.SIDM_SURYASIDDHANTA_MSUN, "ARYABHATA":swe.SIDM_ARYABHATA, "ARYABHATA_MSUN":swe.SIDM_ARYABHATA_MSUN,
                            "SS_CITRA":swe.SIDM_SS_CITRA, "TRUE_CITRA":swe.SIDM_TRUE_CITRA, "TRUE_REVATI":swe.SIDM_TRUE_REVATI,
                            "SS_REVATI": swe.SIDM_SS_REVATI, "SIDM_USER":swe.SIDM_USER,
                            #"KP-SENTHIL":swe.SIDM_KRISHNAMURTI_VP291,
                            #"TRUE_PUSHYA":swe.SIDM_TRUE_PUSHYA, "TRUE_MULA":swe.SIDM_TRUE_MULA, "ARYABHATA_522":swe.SIDM_ARYABHATA_522, 
                            }

_ayanamsa_mode = "KP"
def set_ayanamsa_mode(ayanamsa_mode = "KP",ayanamsa_value=None):
    """
        Set Ayanamsa mode
        @param ayanamsa_mode - Default - Lahiri
        @param ayanamsa_value - in case of 'SIDM_USER'
        Available ayanamsa_modes are 
        "FAGAN","KP", "LAHIRI""RAMAN","USHASHASHI""YUKTESHWAR", "SURYASIDDHANTA", "SURYASIDDHANTA_MSUN",
        "ARYABHATA", "ARYABHATA_MSUN", "SS_CITRA", "TRUE_CITRA", "TRUE_REVATI","SS_REVATI","SIDM_USER"
    """
    global _ayanamsa_mode
    #print("Ayanamsa mode before",ayanamsa_mode)
    if ayanamsa_mode.upper() in [am.upper() for am in available_ayanamsa_modes.keys()]:
        if ayanamsa_mode.upper() == "SIDM_USER":
            swe.set_sid_mode(available_ayanamsa_modes[ayanamsa_mode],ayanamsa_value)
        else:
            swe.set_sid_mode(available_ayanamsa_modes[ayanamsa_mode.upper()])
    else:
        print('Ayanamsa mode',ayanamsa_mode,' is not a valid option. Set to LAHIRI')
        swe.set_sid_mode(swe.SIDM_LAHIRI)
    #print("Ayanamsa mode",ayanamsa_mode,'set')
    _ayanamsa_mode = ayanamsa_mode
#set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
reset_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

def read_list_types_from_file(lstTypeFile):
    import os.path
    from os import path
    import codecs
    if not path.exists(lstTypeFile):
        print('Error: List Types iile:'+lstTypeFile+' does not exist. Script aborted.')
        exit()
    
    global cal_key_list
    cal_key_list = {}
    with codecs.open(lstTypeFile, encoding='utf-8', mode='r') as fp:
        line_list = fp.read().splitlines()
    fp.close()
    for line in line_list: #  fp:
        if line.replace("\r\n","").replace("\r","").rstrip().lstrip()[0] == '#':
            continue
        splitLine = line.split('=')
        cal_key_list[splitLine[0].strip()]=splitLine[1].strip()
#    print (cal_key_list)
    return cal_key_list       
    
def read_lists_from_file(inpFile):
    import os.path
    from os import path
    import codecs
    global PLANET_NAMES,NAKSHATRA_LIST,TITHI_LIST,RAASI_LIST,KARANA_LIST,DAYS_LIST,PAKSHA_LIST,YOGAM_LIST, MONTH_LIST,YEAR_LIST,DHASA_LIST,BHUKTHI_LIST
    if not path.exists(inpFile):
        print('Error: input iile:'+inpFile+' does not exist. Script aborted.')
        exit()
    fp = codecs.open(inpFile, encoding='utf-8', mode='r')
    line = fp.readline().strip().replace('\n','')
    line = line.replace("\r","").rstrip()
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    PLANET_NAMES = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    line = line.replace("\r","").rstrip()
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    NAKSHATRA_LIST = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    TITHI_LIST = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    RAASI_LIST = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    KARANA_LIST = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    DAYS_LIST = line.rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    PAKSHA_LIST = line.replace("\r","").rstrip('\n').split(',')
    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    YOGAM_LIST = line.replace("\r","").rstrip('\n').split(',')

    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    MONTH_LIST = line.replace("\r","").rstrip('\n').split(',')

    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    YEAR_LIST = line.rstrip('\n').split(',')

    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    DHASA_LIST = line.rstrip('\n').split(',')

    line = fp.readline().strip().replace('\n','')
    if line.lstrip()[0] == '#':
        line = fp.readline().strip().replace('\n','')
    BHUKTHI_LIST = line.rstrip('\n').split(',')
#    exit()
    return [PLANET_NAMES,NAKSHATRA_LIST,TITHI_LIST,RAASI_LIST,KARANA_LIST,DAYS_LIST,PAKSHA_LIST,YOGAM_LIST,MONTH_LIST,YEAR_LIST,DHASA_LIST,BHUKTHI_LIST]
    
def get_place_timezone_offset(latitude, longitude):
    """
        returns a location's time zone offset from UTC in minutes.
    """
    from timezonefinder import TimezoneFinder
    tf = TimezoneFinder()
    today = datetime.now()
    tz_target = timezone(tf.timezone_at(lng=longitude, lat=latitude))
    # ATTENTION: tz_target could be None! handle error case
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    tz_offset = (today_utc - today_target).total_seconds() / 60 / 60 # in hours
    return tz_offset
        
def get_latitude_longitude_from_place_name(place_with_country_code):
    #[city,latitude,longitude,tz_offset]=''
    geolocator = Nominatim(user_agent="Astro") #,format_string="%s, Bangalore")
    while True:
        try:
            #print('try')
            address,(latitude,longitude) = geolocator.geocode("city:" + place_with_country_code, featuretype='city')
            break
        except (RuntimeError, TypeError, NameError):
            #print('except')
            ValueError('City:'+place_with_country_code+' not found in OpenStreetMap')
            address = ''
            break;
    if address:    
        #print('address')
        city = address.split(',')[0]
        tz_offset = get_place_timezone_offset(latitude, longitude)
        return [city,latitude,longitude,tz_offset]

# Temporary function
def get_dhasa_name(planet):
  names = { swe.SURYA: DHASA_LIST[0], swe.CHANDRA: DHASA_LIST[1], swe.KUJA: DHASA_LIST[2],
            swe.BUDHA: DHASA_LIST[3], swe.GURU: DHASA_LIST[4], swe.SUKRA: DHASA_LIST[5],
            swe.SANI: DHASA_LIST[6], swe.RAHU: DHASA_LIST[10], swe.KETU: DHASA_LIST[11], swe.URANUS:DHASA_LIST[7], swe.NEPTUNE:DHASA_LIST[8], swe.PLUTO:DHASA_LIST[9]}
  return names[planet]
def get_bhukthi_name(planet):
  names = { swe.SURYA: BHUKTHI_LIST[0], swe.CHANDRA: BHUKTHI_LIST[1], swe.KUJA: BHUKTHI_LIST[2],
            swe.BUDHA: BHUKTHI_LIST[3], swe.GURU: BHUKTHI_LIST[4], swe.SUKRA: BHUKTHI_LIST[5],
            swe.SANI: BHUKTHI_LIST[6], swe.RAHU: BHUKTHI_LIST[10], swe.KETU: BHUKTHI_LIST[11], swe.URANUS:BHUKTHI_LIST[7], swe.NEPTUNE:BHUKTHI_LIST[8], swe.PLUTO:BHUKTHI_LIST[9]}
  return names[planet]

# Convert 23d 30' 30" to 23.508333 degrees
from_dms = lambda degs, mins, secs: degs + mins/60 + secs/3600

# the inverse
def to_dms_prec(deg):
  d = int(deg)
  mins = (deg - d) * 60
  m = int(mins)
  s = round((mins - m) * 60, 6)
  return [d, m, s]

def to_dms(deg,as_string=False, is_lat_long=None):
  sep = ':'
  am = " AM"
  pm = " PM"
  ampm= am
  degree_symbol = "°" 
  minute_symbol = u'\u2019'
  second_symbol = '"'
  next_day = ''
  d = int(deg)
  mins = (deg - d) * 60
  m = int(mins)
  #"""
  if (is_lat_long==None) and d > 23:
      #print('is_lat_long,d',is_lat_long,d)
      # WEIRD Following subtraction does not happen
      q = d // 24
      d = d % 24 #d -= 24
      next_day = ' (+'+str(q)+')'
#      print('d=',d)
  #"""
  if d > 12:
      ampm = pm
  if m==60:
      d += 1
      m = 0
  s = int(round((mins - m) * 60))
  if s==60:
      m += 1
      s = 0
  answer = [d, m, s]
  if as_string or is_lat_long != None:
      if is_lat_long=='plong':
          answer = str(abs(d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
      elif is_lat_long=='lat':
          answer = str(abs(d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
          if d > 0: answer += ' N'
          else: answer +=' S' 
      elif is_lat_long=='long':
          answer = str(abs(d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
          if d > 0: answer += ' E'
          else: answer +=' W' 
      else: ## as_string = =True
          answer= str(d).zfill(2)+ sep +str(m).zfill(2)+ sep +str(s).zfill(2)+ampm+next_day
  return answer
def to_dms_old(deg):
  d, m, s = to_dms_prec(deg)
  return [d, m, int(s)]

def unwrap_angles(angles):
  """Add 360 to those elements in the input list so that
     all elements are sorted in ascending order."""
  result = angles
  for i in range(1, len(angles)):
    if result[i] < result[i-1]: result[i] += 360

  assert(result == sorted(result))
  return result

# Make angle lie between [-180, 180) instead of [0, 360)
norm180 = lambda angle: (angle - 360) if angle >= 180 else angle;

# Make angle lie between [0, 360)
norm360 = lambda angle: angle % 360

# Ketu is always 180° after Rahu, so same coordinates but different constellations
# i.e if Rahu is in Pisces, Ketu is in Virgo etc
ketu = lambda rahu: (rahu + 180) % 360
rahu = lambda ketu: (ketu + 180) % 360

def function(point):
    swe.set_sid_mode(swe.SIDM_USER, point, 0.0)
    #swe.set_sid_mode(swe.SIDM_LAHIRI)
    # Place Revati at 359°50'
    #fval = norm180(swe.fixstar_ut("Revati", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0]) - ((359 + 49/60 + 59/3600) - 360)
    # Place Revati at 0°0'0"
    #fval = norm180(swe.fixstar_ut("Revati", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0])
    # Place Citra at 180°
    fval = swe.fixstar_ut("Citra", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0] - (180)
    # Place Pushya (delta Cancri) at 106°
    # fval = swe.fixstar_ut(",deCnc", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0] - (106)
    return fval

def bisection_search(func, start, stop):
  left = start
  right = stop
  epsilon = 5E-10   # Anything better than this puts the loop below infinite

  while True:
    middle = (left + right) / 2
    midval =  func(middle)
    rtval = func(right)
    if midval * rtval >= 0:
      right = middle
    else:
      left = middle

    if (right - left) <= epsilon: break

  return (right + left) / 2

def inverse_lagrange(x, y, ya):
  """Given two lists x and y, find the value of x = xa when y = ya, i.e., f(xa) = ya"""
  assert(len(x) == len(y))
  total = 0
  for i in range(len(x)):
    numer = 1
    denom = 1
    for j in range(len(x)):
      if j != i:
        numer *= (ya - y[j])
        denom *= (y[i] - y[j])

    total += numer * x[i] / denom

  return total

# Julian Day number as on (year, month, day) at 00:00 UTC
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)   # returns (y, m, d, h, min, s)

def local_time_to_jdut1(year, month, day, hour = 0, minutes = 0, seconds = 0, timezone = 0.0):
  """Converts local time to JD(UT1)"""
  y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
  # BUG in pyswisseph: replace 0 by s
  jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0, flag = swe.GREG_CAL)
  return jd_ut1

# moon daily motion
def _lunar_daily_motion(jd):
  """ lunar daily motion"""
  today_longitude = lunar_longitude(jd)
  tomorrow_longitude = lunar_longitude(jd+1)
#      print(tomorrow_longitude,today_longitude)
  if (tomorrow_longitude < today_longitude):
    tomorrow_longitude += dms_to_deg(360,0,0)
  daily_motion = tomorrow_longitude - today_longitude
#      print(tomorrow_longitude,today_longitude)
  return daily_motion
  
# sun daily motion
def _solar_daily_motion(jd):
  """ Sun daily motion"""
  today_longitude = solar_longitude(jd)
  tomorrow_longitude = solar_longitude(jd+1)
  if (tomorrow_longitude < today_longitude):
    tomorrow_longitude = tomorrow_longitude + dms_to_deg(360,0,0)
  daily_motion = tomorrow_longitude - today_longitude
#  print(tomorrow_longitude,today_longitude)
  return daily_motion

def nakshatra_pada(longitude):
  """Gives nakshatra (1..27) and paada (1..4) in which given longitude lies"""
  # 27 nakshatras span 360°
  one_star = (360 / 27)  # = 13°20'
  # Each nakshatra has 4 padas, so 27 x 4 = 108 padas in 360°
  one_pada = (360 / 108) # = 3°20'
  quotient = int(longitude / one_star)
  reminder = (longitude - quotient * one_star)
  pada = int(reminder / one_pada)
#  print (longitude,quotient,pada)
  # convert 0..26 to 1..27 and 0..3 to 1..4
  return [1 + quotient, 1 + pada]

def sidereal_longitude(jd, planet):
  """Computes nirayana (sidereal) longitude of given planet on jd"""
  global _ayanamsa_mode
  set_ayanamsa_mode(_ayanamsa_mode)
  longi = swe.calc_ut(jd, planet, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
  reset_ayanamsa_mode()
  return norm360(longi[0]) # degrees

solar_longitude = lambda jd: sidereal_longitude(jd, swe.SUN)
lunar_longitude = lambda jd: sidereal_longitude(jd, swe.MOON)

def sunrise(jd, place,as_string=False):
  """Sunrise when centre of disc is at horizon for given date and place"""
  city,lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)
  rise = result[1][0]  # julian-day number
  # Convert to local time
  return [rise + tz/24., to_dms((rise - jd) * 24 + tz,as_string)]

def sunset(jd, place,as_string=False):
  """Sunset when centre of disc is at horizon for given date and place"""
  city,lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_SET)
  setting = result[1][0]  # julian-day number
  # Convert to local time
  return [setting + tz/24., to_dms((setting - jd) * 24 + tz,as_string)]

def moonrise(jd, place,as_string=False):
  """Moonrise when centre of disc is at horizon for given date and place"""
  city, lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.MOON, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)
  rise = result[1][0]  # julian-day number
  # Convert to local time
  return to_dms((rise - jd) * 24 + tz,as_string)

def moonset(jd, place,as_string=False):
  """Moonset when centre of disc is at horizon for given date and place"""
  city, lat, lon, tz = place
  result = swe.rise_trans(jd - tz/24, swe.MOON, lon, lat, rsmi = _rise_flags + swe.CALC_SET)
  setting = result[1][0]  # julian-day number
  # Convert to local time
  return to_dms((setting - jd) * 24 + tz,as_string)

# Tithi doesn't depend on Ayanamsa
def tithi(jd, place, as_string=False):
  """Tithi at sunrise for given date and place. Also returns tithi's end time."""
  tz = place.timezone
  paksha = ''
  # 1. Find time of sunrise
  rise = sunrise(jd, place)[0] - tz / 24
  
  # 2. Find tithi at this JDN
  moon_phase = lunar_phase(rise)
  today = ceil(moon_phase / 12)  
  degrees_left = today * 12 - moon_phase

  # 3. Compute longitudinal differences at intervals of 0.25 days from sunrise
  offsets = [0.25, 0.5, 0.75, 1.0]
  lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
  solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
  relative_motion = [ moon - sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]

  # 4. Find end time by 4-point inverse Lagrange interpolation
  y = relative_motion
  x = offsets
  # compute fraction of day (after sunrise) needed to traverse 'degrees_left'
  approx_end = inverse_lagrange(x, y, degrees_left)
  ends = (rise + approx_end -jd) * 24 + tz
  tithi_no = int(today)
  if tithi_no <15:
      paksha = PAKSHA_LIST[0]
  elif tithi_no > 15 and tithi_no <= 30:
      paksha = PAKSHA_LIST[1]
      
  answer = [tithi_no, to_dms(ends,as_string)]
  if as_string:
      answer=paksha + '-'+TITHI_LIST[tithi_no-1]+' '+ to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']

  # 5. Check for skipped tithi
  moon_phase_tmrw = lunar_phase(rise + 1)
  tomorrow = ceil(moon_phase_tmrw / 12)
  isSkipped = (tomorrow - today) % 30 > 1
  if isSkipped:
    # interpolate again with same (x,y)
    leap_tithi = today + 1
    tithi_no = int(leap_tithi)
    degrees_left = leap_tithi * 12 - moon_phase
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end -jd) * 24 + place.timezone
    leap_tithi = 1 if today == 30 else leap_tithi
    if tithi_no <15:
        paksha = PAKSHA_LIST[0]
    elif tithi_no > 15 and tithi_no < 30:
        paksha = PAKSHA_LIST[1]
    if as_string:
      answer += paksha + '-'+TITHI_LIST[tithi_no-1]+' '+to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']
    else:
      answer += [tithi_no, to_dms(ends,as_string)]
  return answer

def get_raasi_new(jd, place, as_string=False):
  city, lat, lon, tz = place
  jd_ut = jd - place.timezone / 24.
  rise = sunrise(jd, place)[0] - tz / 24
  offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
  longitudes = [sidereal_longitude(jd_ut+t, swe.MOON) for t in offsets]
  nirayana_long = longitudes[0]
  raasi_no = int(nirayana_long/360*12)+1
  # 3. Find end time by 5-point inverse Lagrange interpolation
  y = unwrap_angles(longitudes)
  x = offsets
  approx_end = inverse_lagrange(x, y, raasi_no * 360 / 12)
  ends = (rise - jd + approx_end) * 24 + tz
  #print('jd,jd_ut,rise,approx_end,ends',jd,jd_ut,rise,approx_end,ends)
  answer = [raasi_no, to_dms(ends,as_string)]
  if as_string:
      answer=RAASI_LIST[raasi_no-1]+' '+to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']

  # 4. Check for skipped raasi
  raasi_tmrw = ceil(longitudes[-1] * 12 / 360)
  isSkipped = (raasi_tmrw - raasi_no) % 12 > 1
  if isSkipped:
    leap_raasi = raasi_no + 1
    approx_end = inverse_lagrange(offsets, longitudes, leap_raasi * 360 / 12)
    ends = (rise - jd + approx_end) * 24 + tz
    leap_raasi = 1 if raasi_no == 12 else leap_raasi
    raasi_no = int(leap_raasi)
    if as_string:
      answer+=[RAASI_LIST[raasi_no-1], to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']]
    else:
      answer += [raasi_no, to_dms(ends,as_string)]
  #print(' rassi new ends',ends,isSkipped, answer)
  return answer
   
def nakshatra(jd, place, as_string=False):
  city, lat, lon, tz = place
  jd_ut = jd - place.timezone / 24.
  rise = sunrise(jd, place)[0] - tz / 24
  offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
  longitudes = [sidereal_longitude(jd_ut+t, swe.MOON) for t in offsets]
  nirayana_long = longitudes[0]
  nak_no,padam_no = nakshatra_pada(nirayana_long)
  # 3. Find end time by 5-point inverse Lagrange interpolation
  y = unwrap_angles(longitudes)
  x = offsets
  approx_end = inverse_lagrange(x, y, nak_no * 360 / 27)
  ends = (rise - jd + approx_end) * 24 + tz
  answer = [nak_no,padam_no, to_dms(ends,as_string)]
  if as_string:
      answer=NAKSHATRA_LIST[nak_no-1]+' '+cal_key_list['paadham_str']+str(padam_no)+' '+to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']

  # 4. Check for skipped nakshatra
  nak_tmrw = ceil(longitudes[-1] * 27 / 360)
  isSkipped = (nak_tmrw - nak_no) % 27 > 1
  if isSkipped:
    leap_nak = nak_no + 1
    approx_end = inverse_lagrange(offsets, longitudes, leap_nak * 360 / 27)
    ends = (rise - jd + approx_end) * 24 + tz
    leap_nak = 1 if nak_no == 27 else leap_nak
    nak_no = int(leap_nak)
    if as_string:
      answer+=[NAKSHATRA_LIST[nak_no-1]+' '+cal_key_list['paadham_str']+str(padam_no), to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']]
    else:
      answer += [nak_no,padam_no, to_dms(ends,as_string)]
  return answer
   
def _nakshatra_old(jd, place,as_string=False):
  """Current nakshatra as of julian day (jd)
     1 = Asvini, 2 = Bharani, ..., 27 = Revati
  """
  # 1. Find time of sunrise
  jd_ut = jd - place.timezone / 24.
  city, lat, lon, tz = place
  offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
  longitudes=[]
  rise = sunrise(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00    
  longitudes = [ lunar_longitude(rise + t) for t in offsets]
#  print(longitudes)
  # 2. Today's nakshatra is when offset = 0
  # There are 27 Nakshatras spanning 360 degrees
#  nak = ceil(longitudes[0] * 27 / 360)
#  print('moon longitude=',longitudes[0])
  nak,padam_no = nakshatra_pada(longitudes[0])
#  print(nak,padam_no)
  nak_no = int(nak)
  # 3. Find end time by 5-point inverse Lagrange interpolation
  y = unwrap_angles(longitudes)
  x = offsets
  approx_end = inverse_lagrange(x, y, nak_no * 360 / 27)
  ends = (rise - jd + approx_end) * 24 + tz
  answer = [nak_no,padam_no, to_dms(ends,as_string)]
  if as_string:
      answer=[NAKSHATRA_LIST[nak_no-1]+' '+cal_key_list['paadham_str']+str(padam_no), to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']]

  # 4. Check for skipped nakshatra
  nak_tmrw = ceil(longitudes[-1] * 27 / 360)
  isSkipped = (nak_tmrw - nak_no) % 27 > 1
  if isSkipped:
    leap_nak = nak_no + 1
    approx_end = inverse_lagrange(offsets, longitudes, leap_nak * 360 / 27)
    ends = (rise - jd + approx_end) * 24 + tz
    leap_nak = 1 if nak_no == 27 else leap_nak
    nak_no = int(leap_nak)
    if as_string:
      answer+=NAKSHATRA_LIST[nak_no-1]+' '+cal_key_list['paadham_str']+str(padam_no), to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']
    else:
      answer += [nak_no,padam_no, to_dms(ends,as_string)]
  return answer


def yoga(jd, place,as_string=False):
  """Yoga at given jd and place.
     1 = Vishkambha, 2 = Priti, ..., 27 = Vaidhrti
  """
  # 1. Find time of sunrise
  city, lat, lon, tz = place
  rise = sunrise(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00

  # 2. Find the Nirayana longitudes and add them
  lunar_long = lunar_longitude(rise)
  solar_long = solar_longitude(rise)
  total = (lunar_long + solar_long) % 360
  # There are 27 Yogas spanning 360 degrees
  yog = ceil(total * 27 / 360)
  yogam_no = int(yog)
  # 3. Find how many longitudes is there left to be swept
  degrees_left = yog * (360 / 27) - total

  # 3. Compute longitudinal sums at intervals of 0.25 days from sunrise
  offsets = [0.25, 0.5, 0.75, 1.0]
  lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
  solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
  total_motion = [ moon + sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]

  # 4. Find end time by 4-point inverse Lagrange interpolation
  y = total_motion
  x = offsets
  # compute fraction of day (after sunrise) needed to traverse 'degrees_left'
  approx_end = inverse_lagrange(x, y, degrees_left)
  ends = (rise + approx_end - jd) * 24 + tz
  answer = [yogam_no, to_dms(ends,as_string)]
  if as_string:
      answer = YOGAM_LIST[yogam_no-1]+' '+to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']

  # 5. Check for skipped yoga
  lunar_long_tmrw = lunar_longitude(rise + 1)
  solar_long_tmrw = solar_longitude(rise + 1)
  total_tmrw = (lunar_long_tmrw + solar_long_tmrw) % 360
  tomorrow = ceil(total_tmrw * 27 / 360)
  isSkipped = (tomorrow - yog) % 27 > 1
  if isSkipped:
    # interpolate again with same (x,y)
    leap_yog = yog + 1
    degrees_left = leap_yog * (360 / 27) - total
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end - jd) * 24 + tz
    leap_yog = 1 if yog == 27 else leap_yog
    yogam_no = int(leap_yog)
    if as_string:
        answer += YOGAM_LIST[yogam_no-1]+' '+to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']
    else:
        answer += [yogam_no, to_dms(ends,as_string)]

  return answer


def karana(jd, place,as_string=False):
  """Returns the karana and their ending times. (from 1 to 60)"""
  # 1. Find time of sunrise
  rise = sunrise(jd, place)[0]

  # 2. Find karana at this JDN
#  solar_long = solar_longitude(rise)
#  lunar_long = lunar_longitude(rise)
#  moon_phase = (lunar_long - solar_long) % 360
  moon_phase = lunar_phase(jd)
  today = ceil(moon_phase / 6 )
  degrees_left = today * 6 - moon_phase
  answer = int(today)
  if as_string:
      answer=KARANA_LIST[answer-1] 
  return answer

def vaara(jd,as_string=False):
  """Weekday for given Julian day. 0 = Sunday, 1 = Monday,..., 6 = Saturday"""
  answer = int(ceil(jd + 1) % 7)
  if as_string:
      answer=DAYS_LIST[answer] 
  return answer
  
def tamil_maadham(date_in,place,as_string=False):
  city, lat, lon, tz = place
  jd = gregorian_to_jd(date_in)
  sun_set = sunset(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00
#  sr=sun_long_precessed(dt,zone)
  sr = solar_longitude(sun_set)
  #print('sun long',sr,'at',date_in)
  month_no = (int(sr/30))
  daycount=1
  dt = date_in
  while True:
    if sr%30<1 and sr%30>0:
      break
    dt = dt - timedelta(days=1)
    jdn = gregorian_to_jd(dt)
    sr=solar_longitude(jdn)
    #print('sun long',sr,'at',dt)
    daycount+=1
    #print (dt,jdn,sr,daycount)
  day_no = daycount
  if as_string:
      return MONTH_LIST[int(month_no)]+'-'+str(day_no)
  else:
      return [month_no, day_no]
  
def maasa(jd, place,as_string=False):
  """Returns lunar month and if it is adhika or not.
     0 = Chaitra, 2 = Vaisakha, ..., 11 = Phalguna"""
  ti = tithi(jd, place,as_string=False)[0]
  critical = sunrise(jd, place)[0]  # - tz/24 ?
  last_new_moon = new_moon(critical, ti, -1)
  next_new_moon = new_moon(critical, ti, +1)
#  this_solar_month = _raasi(last_new_moon,place,as_string=False)[0]
#  next_solar_month = _raasi(next_new_moon,place,as_string=False)[0]
  this_solar_month = get_raasi(last_new_moon,place,as_string=False)[0]
  next_solar_month = get_raasi(next_new_moon,place,as_string=False)[0]
#  print ('next new moon',next_new_moon,next_solar_month)
  is_leap_month = (this_solar_month == next_solar_month)
  maasa = this_solar_month+1
  if maasa > 12: maasa = (maasa % 12)
  if as_string:
      return [MONTH_LIST[int(maasa-1)], is_leap_month]
  else:
      return [int(maasa), is_leap_month]

# epoch-midnight to given midnight
# Days elapsed since beginning of Kali Yuga
ahargana = lambda jd: jd - 588465.5

def elapsed_year(jd, maasa_num):
  ahar = ahargana(jd)  # or (jd + sunrise(jd, place)[0])
  kali = int((ahar + (4 - maasa_num) * 30) / sidereal_year)
  saka = kali - 3179
  vikrama = saka + 135
  return kali, vikrama, saka

# New moon day: sun and moon have same longitude (0 degrees = 360 degrees difference)
# Full moon day: sun and moon are 180 deg apart
def new_moon(jd, tithi_, opt = -1):
  """Returns JDN, where
     opt = -1:  JDN < jd such that lunar_phase(JDN) = 360 degrees
     opt = +1:  JDN >= jd such that lunar_phase(JDN) = 360 degrees
  """
  if opt == -1:  start = jd - tithi_         # previous new moon
  if opt == +1:  start = jd + (30 - tithi_)  # next new moon
  # Search within a span of (start +- 2) days
  x = [ -2 + offset/4 for offset in range(17) ]
  y = [lunar_phase(start + i) for i in x]
  y = unwrap_angles(y)
  y0 = inverse_lagrange(x, y, 360)
  return start + y0

def get_raasi(jd, place, as_string=False):
  """Tithi at sunrise for given date and place. Also returns tithi's end time."""
  city, lat, lon, tz = place
  rise = sunrise(jd, place)[0] - tz / 24
  moon_longitude = lunar_longitude(jd)
  if (moon_longitude > 360):
      moon_longitude -= 360
  raasi_durn = 360/12
  raasi_no = ceil(moon_longitude / raasi_durn)
  raasi_remaining = moon_longitude- (raasi_no-1)*raasi_durn
  raasi = RAASI_LIST[raasi_no-1]
  moon_daily_motion = _lunar_daily_motion(jd)
  raasi_remain_degrees = (raasi_no*raasi_durn) - moon_longitude
  sun_rise_time = (rise - jd) * 24 + tz
  raasi_ends_at = ( sun_rise_time + raasi_remain_degrees*24/(moon_daily_motion) ) % 360
#  raasi_end_time = (rise - jd + raasi_ends_at) * 24 + tz
#      print(moon_longitude,raasi_no,nak_no,moon_daily_motion,raasi_remain_degrees,nak_remain_degrees,raasi_ends_at,nak_ends_at)
  if as_string:
      answer = [RAASI_LIST[raasi_no-1], to_dms(raasi_ends_at,as_string)+' '+cal_key_list['ends_at_str']]
  else:
      answer = [raasi_no, to_dms(raasi_ends_at,as_string)]

  return answer

def _raasi(jd,place, as_string=False):
  """Zodiac of given jd. 1 = Mesha, ... 12 = Meena"""
  city, lat, lon, tz = place
  rise = sunrise(jd, place)[0] - tz / 24.  # Sunrise at UT 00:00

  offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
  longitudes = [ solar_longitude(rise + t) for t in offsets]
  raasi_durn = 360/12
  solar_nirayana = longitudes[0]
  # 12 rasis occupy 360 degrees, so each one is 30 degrees
  raasi_no = ceil(solar_nirayana / raasi_durn)
  # 3. Find end time by 5-point inverse Lagrange interpolation
  y = unwrap_angles(longitudes)
  x = offsets
  approx_end = inverse_lagrange(x, y, raasi_no * raasi_durn)
  ends = (rise - jd + approx_end) * 24 + tz
#  print('raasi end time',ends)
  if as_string:
      answer = [RAASI_LIST[raasi_no-1], to_dms(ends,as_string)+' '+cal_key_list['ends_at_str']]
  else:
      answer = [raasi_no, to_dms(ends,as_string)]

  return answer
  
def lunar_phase(jd):
  solar_long = solar_longitude(jd)
  lunar_long = lunar_longitude(jd)
  moon_phase = (lunar_long - solar_long) % 360
  return moon_phase

def samvatsara(jd, maasa_num,as_string=False):
  kali = elapsed_year(jd, maasa_num)[0]
  # Change 14 to 0 for North Indian tradition
  # See the function "get_Jovian_Year_name_south" in pancanga.pl
  if kali >= 4009:    kali = (kali - 14) % 60
  samvat = (kali + 27 + int((kali * 211 - 108) / 18000)) % 60
  if as_string:
      samvat = YEAR_LIST[samvat-1]
  return samvat

def ritu(masa_num):
  """0 = Vasanta,...,5 = Shishira"""
  return (masa_num - 1) // 2

def day_duration(jd, place):
  srise = sunrise(jd, place)[0]  # julian day num
  sset = sunset(jd, place)[0]    # julian day num
  diff = (sset - srise) * 24     # In hours
  return [diff, to_dms(diff)]

# The day duration is divided into 8 parts
# Similarly night duration
def gauri_chogadiya(jd, place,as_string=False):
  city, lat, lon, tz = place
  tz = place.timezone
  srise = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)

  end_times = []
  for i in range(1, 9):
    if (as_string):
        end_times.append(to_dms((srise + (i * day_dur) / 8 - jd) * 24 + tz,as_string)+' '+cal_key_list['ends_at_str'])
    else:
        end_times.append(to_dms((srise + (i * day_dur) / 8 - jd) * 24 + tz))

  # Night duration = time from today's sunset to tomorrow's sunrise
  srise = swe.rise_trans((jd + 1) - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  night_dur = (srise - sset)
  for i in range(1, 9):
      if(as_string):
          end_times.append(to_dms((sset + (i * night_dur) / 8 - jd) * 24 + tz,as_string)+' '+cal_key_list['ends_at_str'])
      else:
          end_times.append(to_dms((sset + (i * night_dur) / 8 - jd) * 24 + tz))

  return end_times

def trikalam(jd, place, option='raahu kaalam',as_string=False):
  city, lat, lon, tz = place
  tz = place.timezone
  srise = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)
  weekday = vaara(jd)

  # value in each array is for given weekday (0 = sunday, etc.)
  offsets = { 'raahu kaalam': [0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25],
              'gulikai': [0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0],
              'yamagandam': [0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625] }

  start_time = srise + day_dur * offsets[option][weekday]
  end_time = start_time + 0.125 * day_dur

  # to local timezone
  start_time = (start_time - jd) * 24 + tz
  end_time = (end_time - jd) * 24 + tz
  if as_string:
      start_time = to_dms(start_time,as_string)
      end_time = to_dms(end_time,as_string)+' '+cal_key_list['ends_at_str']
  else:
      start_time = to_dms(start_time,as_string=False)
      end_time = to_dms(end_time,as_string=False)

  return [start_time, end_time] # decimal hours to H:M:S

raahu_kaalam = lambda jd, place,as_string=False: trikalam(jd, place, 'raahu kaalam', as_string=False)
yamaganda_kaalam = lambda jd, place,as_string=False: trikalam(jd, place, 'yamagandam', as_string=False)
gulikai_kaalam = lambda jd, place,as_string=False: trikalam(jd, place, 'gulikai',as_string=False)

def durmuhurtam(jd, place,as_string=False):
  city, lat, lon, tz = place
  tz = place.timezone

  # Night = today's sunset to tomorrow's sunrise
  sset = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_SET)[1][0]
  srise = swe.rise_trans((jd + 1) - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  night_dur = (srise - sset)

  # Day = today's sunrise to today's sunset
  srise = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  day_dur = (sset - srise)

  weekday = vaara(jd)

  # There is one durmuhurtam on Sun, Wed, Sat; the rest have two
  offsets = [[10.4, 0.0],  # Sunday
             [6.4, 8.8],   # Monday
             [2.4, 4.8],   # Tuesday, [day_duration , night_duration]
             [5.6, 0.0],   # Wednesday
             [4.0, 8.8],   # Thursday
             [2.4, 6.4],   # Friday
             [1.6, 0.0]]   # Saturday

  # second durmuhurtam of tuesday uses night_duration instead of day_duration
  dur = [day_dur, day_dur]
  base = [srise, srise]
  if weekday == 2:  dur[1] = night_dur; base[1] = sset

  # compute start and end timings
  start_times = [0, 0]
  end_times = [0, 0]
  answer = []
  for i in range(0, 2):
    offset = offsets[weekday][i]
    if offset != 0.0:
      start_times[i] = base[i] + dur[i] * offsets[weekday][i] / 12
      end_times[i] = start_times[i] + day_dur * 0.8 / 12

      # convert to local time
      start_times[i] = (start_times[i] - jd) * 24 + tz
      end_times[i] = (end_times[i] - jd) * 24 + tz
      if (as_string):
          start_times[i] = to_dms(start_times[i],as_string)
          end_times[i]=to_dms(end_times[i],as_string)+' '+cal_key_list['ends_at_str']
      else:
          start_times[i] = to_dms(start_times[i],as_string=False)
          end_times[i] = to_dms(end_times[i],False)
      answer += [start_times[i],end_times[i]]
          
  return answer
#  return [start_times, end_times]  # in decimal hours

def abhijit_muhurta(jd, place,as_string=False):
  """Abhijit muhurta is the 8th muhurta (middle one) of the 15 muhurtas
  during the day_duration (~12 hours)"""
  city, lat, lon, tz = place
  tz = place.timezone
  srise = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_RISE)[1][0]
  sset = swe.rise_trans(jd - tz/24, swe.SUN, lon, lat, rsmi = _rise_flags + swe.CALC_SET)[1][0]
  day_dur = (sset - srise)

  start_time = srise + 7 / 15 * day_dur
  end_time = srise + 8 / 15 * day_dur
  start_time = (start_time - jd) * 24 + tz
  end_time = (end_time - jd) * 24 + tz
  if (as_string):
      start_time = to_dms(start_time,as_string)
      end_time = to_dms(end_time,as_string)+' '+cal_key_list['ends_at_str']
  else:
      start_time = to_dms(start_time,as_string=False)
      end_time = to_dms(end_time,False)
  # to local time
  return [start_time, end_time]

# 'jd' can be any time: ex, 2015-09-19 14:20 UTC
# today = swe.julday(2015, 9, 19, 14 + 20./60)
def planetary_positions(jd, place,as_string=False):
  """Computes instantaneous planetary positions
     (i.e., which celestial object lies in which constellation)

     Also gives the nakshatra-pada division
   """
  jd_ut = jd - place.timezone / 24.

  positions = []
  #print('planet list',planet_list)
  for planet in planet_list:
    p_id = planet_list.index(planet)
    #print('planet in planetrary positions',planet,p_id,'ketu=',swe.KETU)
    if planet == swe.KETU:
      nirayana_long = ketu(sidereal_longitude(jd_ut, swe.RAHU))
    else: # Ketu
      nirayana_long = sidereal_longitude(jd_ut, planet)
    nak_no,paadha_no = nakshatra_pada(nirayana_long)
    # 12 zodiac signs span 360°, so each one takes 30°
    # 0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
    constellation = int(nirayana_long / 30)
    coordinates = to_dms(nirayana_long-constellation*30,as_string,is_lat_long='plong')
#    positions.append([planet, constellation, coordinates, nakshatra_pada(nirayana_long)])
    if as_string:
        positions.append([PLANET_NAMES[p_id],RAASI_LIST[constellation]+' '+coordinates+' '+ NAKSHATRA_LIST[nak_no-1]+'-'+cal_key_list['paadham_str']+str(paadha_no)])
    else:
        positions.append([p_id,nirayana_long, constellation])

  return positions

def ascendant(jd, place, as_string=False):
  """Lagna (=ascendant) calculation at any given time & place"""
  global _ayanamsa_mode
  city, lat, lon, tz = place
  jd_utc = jd - (tz / 24.)
  set_ayanamsa_mode(_ayanamsa_mode) # needed for swe.houses_ex()

  # returns two arrays, cusps and ascmc, where ascmc[0] = Ascendant
  nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flag = swe.FLG_SIDEREAL)[1][0]
  nak_no,paadha_no = nakshatra_pada(nirayana_lagna)
  # 12 zodiac signs span 360°, so each one takes 30°
  # 0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
  constellation = int(nirayana_lagna / 30)
  coordinates = to_dms(nirayana_lagna-constellation*30,as_string,is_lat_long='plong')

  reset_ayanamsa_mode()
  if as_string:
      return RAASI_LIST[constellation]+' '+coordinates+' '+NAKSHATRA_LIST[nak_no-1]+'-'+cal_key_list['paadham_str']+str(paadha_no)
  else:
      return [constellation, nirayana_lagna, nak_no, paadha_no]

get_relative_house_of_planet = lambda from_house, planet_house: (planet_house + 12 -from_house) % 12 + 1
    
def dasavarga_from_long(longitude, sign_division_factor):
  """Calculates the dasavarga-sign in which given longitude falls
    sign_division_factor = 2 => Hora, 3=>Drekana 7=>Saptamsa, 9=>Navamsa, 10=>Dasamsa, 12=>Dwadamsa, 16=>Shodamsa, 30=>Trisamsa, 60=>Shastyamsa
  0 = Aries, 1 = Taurus, ..., 11 = Pisces
  """
  valid_sign_factors = [2,3,7,9,10,16,30,60]
  if sign_division_factor not in valid_sign_factors:
      raise ValueError("Wrong sign_division_factor",sign_division_factor,' Valid value:',valid_sign_factors)
  one_pada = (360.0 / (12 * sign_division_factor))  # There are also 108 navamsas
  one_sign = 12.0 * one_pada    # = 40 degrees exactly
  signs_elapsed = longitude / one_sign
  fraction_left = signs_elapsed % 1
  position = int(fraction_left * 12)
  return position

navamsa_from_long = lambda longitude: dasavarga_from_long(longitude,9) 

# http://www.oocities.org/talk2astrologer/LearnAstrology/Details/Navamsa.html
# Useful for making D9 divisional chart
def navamsa_from_long_old(longitude):
  """Calculates the navamsa-sign in which given longitude falls
  0 = Aries, 1 = Taurus, ..., 11 = Pisces
  """
  one_pada = (360 / (12 * 9))  # There are also 108 navamsas
  one_sign = 12 * one_pada    # = 40 degrees exactly
  signs_elapsed = longitude / one_sign
  fraction_left = signs_elapsed % 1
  return int(fraction_left * 12)

def dhasavarga(jd, place,sign_division_factor, as_string=False):
  jd_utc = jd - place.timezone / 24.
  """
      ERROR: Rahu/Kethu positions are same for Hora, Dhasamsa, Dhwadhamsa, Thrisamsa, Sashtiamsa
  """
  positions = []
  for planet in planet_list:
    p_id = planet_list.index(planet)
    if planet != swe.KETU:
      nirayana_long = sidereal_longitude(jd_utc, planet)
    else: # Ketu
      nirayana_long = ketu(sidereal_longitude(jd_utc, swe.RAHU))

    if as_string:
        positions.append([PLANET_NAMES[p_id],RAASI_LIST[dasavarga_from_long(nirayana_long,sign_division_factor)]])
    else:
        positions.append([p_id, dasavarga_from_long(nirayana_long,sign_division_factor)])
  return positions
    
def navamsa(jd, place,as_string=False):
  """Calculates navamsa of all planets"""
  jd_utc = jd - place.timezone / 24.

  positions = []
  for planet in planet_list:
    p_id = planet_list.index(planet)
    if planet != swe.KETU:
      nirayana_long = sidereal_longitude(jd_utc, planet)
    else: # Ketu
      nirayana_long = ketu(sidereal_longitude(jd_utc, swe.RAHU))

    if as_string:
        positions.append([PLANET_NAMES[p_id],to_dms(nirayana_long,is_lat_long='plong')+' '+RAASI_LIST[navamsa_from_long(nirayana_long)]])
    else:
        positions.append([[planet,nirayana_long], navamsa_from_long(nirayana_long)])
  return positions

### --- Vimoshatari functions
def next_adhipati(lord):
    """Returns next guy after `lord` in the adhipati_list"""
    current = adhipati_list.index(lord)
    next_index = (current + 1) % len(adhipati_list)
    return adhipati_list[next_index]

def nakshatra_position(jdut1):
    """Get the Nakshatra index and degrees traversed at a given JD(UT1) """
    moon = sidereal_longitude(jdut1, swe.MOON)
    one_star = (360 / 27.)        # 27 nakshatras span 360°
    nak = int(moon / one_star)    # 0..26
    rem = (moon - nak * one_star) # degrees traversed in given nakshatra

    return [nak, rem]

def dasha_start_date(jdut1):
    """Returns the start date (UT1) of the mahadasa which occured on or before `jd(UT1)`"""
    nak, rem = nakshatra_position(jdut1)
    one_star = (360 / 27.)        # 27 nakshatras span 360°
    lord = adhipati(nak)          # ruler of current nakshatra
    period = mahadasa[lord]       # total years of nakshatra lord
    period_elapsed = rem / one_star * period # years
    period_elapsed *= sidereal_year        # days
    start_date = jdut1 - period_elapsed      # so many days before current day

    return [lord, start_date]

def vimsottari_mahadasa(jdut1):
    """List all mahadashas and their start dates"""
    lord, start_date = dasha_start_date(jdut1)
    retval = Dict()
    for i in range(9):
        retval[lord] = start_date
        start_date += mahadasa[lord] * sidereal_year
        lord = next_adhipati(lord)

    return retval

def vimsottari_bhukti(maha_lord, start_date):
    """Compute all bhuktis of given nakshatra-lord of Mahadasa
    and its start date"""
    lord = maha_lord
    retval = Dict()
    for i in range(9):
        retval[lord] = start_date
        factor = mahadasa[lord] * mahadasa[maha_lord] / human_life_span_for_dhasa
        start_date += factor * sidereal_year
        lord = next_adhipati(lord)

    return retval

# North Indian tradition: dasa-antardasa-pratyantardasa
# South Indian tradition: dasa-bhukti-antara-sukshma
def vimsottari_antara(maha_lord, bhukti_lord, start_date):
    """Compute all antaradasas from given bhukit's start date.
    The bhukti's lord and its lord (mahadasa lord) must be given"""
    lord = bhukti_lord
    retval = Dict()
    for i in range(9):
        retval[lord] = start_date
        factor = mahadasa[lord] * (mahadasa[maha_lord] / human_life_span_for_dhasa)
        factor *= (mahadasa[bhukti_lord] / human_life_span_for_dhasa)
        start_date += factor * sidereal_year
        lord = next_adhipati(lord)

    return retval


def where_occurs(jd, some_dict):
    """Returns minimum key such that some_dict[key] < jd"""
    # It is assumed that the dict is sorted in ascending order
    # i.e. some_dict[i] < some_dict[j]  where i < j
    for key in reversed(some_dict.keys()):
        if some_dict[key] < jd: return key


def compute_antara_from(jd, mahadashas):
    """Returns antaradasha within which given `jd` falls"""
    # Find mahadasa where this JD falls
    i = where_occurs(jd, mahadashas)
    # Compute all bhuktis of that mahadasa
    bhuktis = vimsottari_bhukti(i, mahadashas[i])
    # Find bhukti where this JD falls
    j = where_occurs(jd, bhuktis)
    # JD falls in i-th dasa / j-th bhukti
    # Compute all antaras of that bhukti
    antara = vimsottari_antara(i, j, bhuktis[j])
    return (i, j, antara)

# ---------------------- ALL TESTS ------------------------------
def __adhipati_tests():
    # nakshatra indexes counted from 0
    satabhisha, citta, aslesha = 23, 13, 8
    assert(adhipati(satabhisha) == swe.RAHU)
    assert(mahadasa[adhipati(satabhisha)] == 18)
    assert(adhipati(citta) == swe.MARS)
    assert(mahadasa[adhipati(citta)] == 7)
    assert(adhipati(aslesha) == swe.MERCURY)
    assert(mahadasa[adhipati(aslesha)] == 17)

def get_dhasa_bhukthi(jd, place):
    # jd is julian date with birth time included
    city,lat,long,tz = place
    jdut1 = jd - tz/24
    dashas = vimsottari_mahadasa(jdut1)
    #print('dasha lords',dashas)
    dhasa_bukthi=[]
    for i in dashas:
        #print(' ---------- ' + get_dhasa_name(i) + ' ---------- ')
        bhuktis = vimsottari_bhukti(i, dashas[i])
        dhasa_lord = i
        for j in bhuktis:
            bhukthi_lord = j
            jd = bhuktis[j]
            y, m, d, h = swe.revjul(round(jd + tz))
            date_str = '%04d-%02d-%02d' %(y,m,d)
            bhukthi_start = date_str
            dhasa_bukthi.append([dhasa_lord,bhukthi_lord,bhukthi_start]) 
            #dhasa_bukthi[i][j] = [dhasa_lord,bhukthi_lord,bhukthi_start]
    return dhasa_bukthi

### --- get tamil date private functions
def _fract(x):
    return x - int(x)


def _cd_to_jd(gdate):
    """Convert Greenwich date to Julian date."""
    result = 1721424.5 + gdate.toordinal()
    try:
        return result + (gdate.hour * 3600 + gdate.minute * 60 +
                         gdate.second + gdate.microsecond * 1e-6) / 86400.0
    except AttributeError:
        # date parameter is of type 'date' instead of 'datetime'
        return result

def _jd_to_cd(jd):
    """Convert Julian date to calendar date."""
    date = jd - 1721424.5
    result = dtm.datetime.fromordinal(int(date))
    result += dtm.timedelta(seconds=86400.0 * _fract(date))
    return result
def _eccentric_anomaly(am, ec):
    """Return eccentric anomaly for given mean anomaly and eccentricity.

    am: mean anomaly
    ec: eccentricity,
    """
    m = am % (2 * math.pi)
    ae = m
    while 1:
        d = ae - (ec * math.sin(ae)) - m
        if abs(d) < 0.000001:
            break
        ae -= d / (1.0 - (ec * math.cos(ae)))
    return ae


def _true_anomaly(am, ec):
    """Return true anomaly for given mean anomaly and eccentricity.

    am: mean anomaly
    ec: eccentricity,
    """
    ae = _eccentric_anomaly(am, ec)
    return 2.0 * math.atan(math.sqrt((1.0 + ec) / (1.0 - ec)) * math.tan(ae * 0.5))

  
def _get_ayan(year, month, day):
    a = 16.90709 * year/1000 - 0.757371 * year/1000 * year/1000 - 6.92416100010001000
    b = (month-1 + day/30) * 1.1574074/1000
    return -(a+b)

def _sun_long(gdate, zone):
    """Return sun longitude in degrees for given Greenwich datetime (UTC)."""

    t = (_cd_to_jd(gdate) - 2415020.0 + zone/24.0) / 36525.0
    t2 = t * t

    l = 279.69668 + 0.0003025 * t2 + 360.0 * _fract(100.0021359 * t)
    m1 = 358.47583 - (0.00015 + 0.0000033 * t) * t2 + 360.0 * _fract(99.99736042 * t)
    ec = 0.01675104 - 0.0000418 * t - 0.000000126 * t2

    # sun anomaly
    at = _true_anomaly(math.radians(m1), ec)

    a1 = math.radians(153.23 + 360.0 * _fract(62.55209472 * t))
    b1 = math.radians(216.57 + 360.0 * _fract(125.1041894 * t))
    c1 = math.radians(312.69 + 360.0 * _fract(91.56766028 * t))
    d1 = math.radians(350.74 - 0.00144 * t2 + 360.0 * _fract(1236.853095 * t))
    e1 = math.radians(231.19 + 20.2 * t)
    h1 = math.radians(353.4 + 360.0 * _fract(183.1353208 * t))

    d2 = (0.00134 * math.cos(a1) + 0.00154 * math.cos(b1) + 0.002 * math.cos(c1) +
          0.00179 * math.sin(d1) + 0.00178 * math.sin(e1))

    sr = (at + math.radians(l - m1 + d2)) % (2 * math.pi)
    return math.degrees(sr)
  
def _sun_long_precessed(gdate, zone):
    t = (_cd_to_jd(gdate) - 2415020.0 + zone/24.0) / 36525.0
    sr = _sun_long(gdate, zone)
    ay = _get_ayan(gdate.year, gdate.month, gdate.day+gdate.hour/24.0)
    return sr+ay

def tamil_date(date_in,jd, place):
  """
      TODO: Does not work for BC Dates as datetime is used
  """
  city, lat, lon, tz = place
#  hour,minute=18,10
  [sunset_hour,sunset_minute,sunset_second] = sunset(jd,place,as_string=False)[1]
#  print('sunset',hour,minute,seconds)
  zone=-tz
  dt=datetime(date_in.year,date_in.month,date_in.day,sunset_hour,sunset_minute,sunset_second)
  sr=_sun_long_precessed(dt,zone)
#  print('sun long',sr,'at',dt)
#  print(month_names[int(sr/30)])
  daycount=1
  while True:
    if sr%30<1 and sr%30>0:
      break
    dt = dt - timedelta(days=1)
    sr=_sun_long_precessed(dt,zone)
#    print('sun long',sr,'at',dt)
    daycount+=1
  return daycount

if __name__ == "__main__":
    pass