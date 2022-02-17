import swisseph as swe
from _datetime import datetime, time, timedelta,timezone
from dateutil import tz
from collections import namedtuple as struct
import math
Date = struct('Date', ['year', 'month', 'day'])
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)

def _convert_utc_to_local(date_in,time_zone_offset):
    return date_in.replace(tzinfo=timezone.utc).astimezone(tz=timezone(time_zone_offset))
def calculate_ayanamsa_senthil_from_jd(jd):
    reference_jd =  swe.julday(2000, 1, 1, 12)
    sidereal_year = 365.242198781
    p0 = 50.27972324
    m = 0.0002225
    a0 = 85591.25323
    q = m / 2
    diff_days = (jd - reference_jd) # in days
    t = diff_days / sidereal_year
    ayanamsa = a0 + p0*t + q*t*t
    ayanamsa /= 3600
    ayanamsa_degrees = int(ayanamsa)
    ayanamsa_minutes = int( (ayanamsa - ayanamsa_degrees)*60 )
    ayanamsa_seconds = ((ayanamsa - ayanamsa_degrees)*60 - ayanamsa_minutes)*60
    return (ayanamsa_degrees,ayanamsa_minutes, ayanamsa_seconds)
    
def calculate_ayanamsa(date_in,time_zone_offset):
    """ constants """
    reference_date = datetime(2000,1,1,12,0,0,0)
    reference_date = _convert_utc_to_local(reference_date,time_zone_offset)
    date_in = _convert_utc_to_local(date_in,time_zone_offset)
    sidereal_year = 365.242198781
    p0 = 50.27972324
    m = 0.0002225
    a0 = 85591.25323
    q = m / 2
    diff_days = (date_in - reference_date).days
    t = diff_days / sidereal_year
    ayanamsa = a0 + p0*t + q*t*t
    ayanamsa /= 3600
    ayanamsa_degrees = int(ayanamsa)
    ayanamsa_minutes = int( (ayanamsa - ayanamsa_degrees)*60 )
    ayanamsa_seconds = ((ayanamsa - ayanamsa_degrees)*60 - ayanamsa_minutes)*60
    return (ayanamsa_degrees,ayanamsa_minutes, ayanamsa_seconds)
def ayanamsa_surya_siddhantha_model(jd,in_degrees=True):
    maha_yuga_years = 4320000
    completed_maha_yuga_years = 3888000
    ayanamsa_cycle_years = 7200
    ayanamsa_cycle_in_degrees = 108
    kali_yuga_jd =  swe.julday(-3101,1,23,12,cal=swe.JUL_CAL)
    ss_sideral_year = 365.256363 #365.2421988 # 365.2587565
    diff_days = jd - kali_yuga_jd
    t = diff_days / ss_sideral_year
    ayanamsa_cycle_fraction = (t/ayanamsa_cycle_years)
    ayanamsa = math.sin(ayanamsa_cycle_fraction * 2.0 * math.pi) *ayanamsa_cycle_in_degrees/4.0
    ayanamsa_degrees = int(ayanamsa)
    if in_degrees:
        return ayanamsa
    ayanamsa_minutes = int( (ayanamsa - ayanamsa_degrees)*60 )
    ayanamsa_seconds = ((ayanamsa - ayanamsa_degrees)*60 - ayanamsa_minutes)*60
    return (ayanamsa_degrees,ayanamsa_minutes, ayanamsa_seconds)
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
  ss = (mins-m)*60
  s = int(ss)
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
  #s = int(round((mins - m) * 60))
  if s==60:
      m += 1
      s = 0
  answer = [d, m, s]
  if as_string or is_lat_long != None:
      if is_lat_long=='plong':
          answer = str((d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
      elif is_lat_long=='lat':
          answer = str((d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
          if d > 0: answer += ' N'
          else: answer +=' S' 
      elif is_lat_long=='long':
          answer = str((d))+degree_symbol+" "+str(abs(m))+minute_symbol+" "+str(abs(s))+second_symbol
          if d > 0: answer += ' E'
          else: answer +=' W' 
      else: ## as_string = =True
          answer= str(d).zfill(2)+ sep +str(m).zfill(2)+ sep +str(s).zfill(2)+ampm+next_day
  return answer
    
print(26.999999999971408,to_dms(26.999999999971408,as_string=True,is_lat_long='plong'))
exit()
for year in range(-3101,7200,200):
    date_in = Date(year,1,23)
    time_in = '19:00:00'
    time_in_arr = time_in.split(':')
    time_in_hours = int(time_in_arr[0])+int(time_in_arr[1])/60+int(time_in_arr[2])/3600
    jd = swe.julday(date_in.year,date_in.month,date_in.day,time_in_hours)
    ayanamsa = ayanamsa_surya_siddhantha_model(jd,in_degrees=True)
    print(date_in, ayanamsa,to_dms(ayanamsa,as_string=True,is_lat_long='plong'))
