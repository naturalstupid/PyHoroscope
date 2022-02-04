import re
import sys
import os
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from _datetime import datetime, timedelta,time,date
import img2pdf
panchanga = __import__('panchanga')
horoscope = __import__('horoscope')
available_languages = {"English":'en','Tamil':'ta','Telugu':'te'}
available_chart_types = ['South-Indian']#,'North-Indian','East-Indian','Western']

class SouthIndianChart(QWidget):
    """
        Draws South Indian Natal Chart and labels the planets
        @param data: 2-D List of planet names in native language
        NOTE: For South Indian Chart - inner cells of 2-D list should have empty labels
        Example: [ ['Saturn','Moon','Sun', 'Mars'],
                   ['Lagnam', ''   , ''  , 'Ragu'],
                   ['Ketu'  , ''   , ''  , 'Mercury'],
                   [''      , 'Jupiter','','']]
    """
    def __init__(self,data=None,*args): #data, *args):
        QWidget.__init__(self, *args)
        self._grid_layout = QGridLayout()
        self.setLayout(self._grid_layout)
        self._grid_labels = []
        self._initialize_south_indian_chart_labels(self._grid_layout)
        if data:
            set_south_indian_chart_data(data)
    def _initialize_south_indian_chart_labels(self,grid_layout):
        _label_counter = 0
        row_count = 4
        col_count = 4
        chart_title = ''
        for row in range(row_count):
            for col in range(col_count):
                    self._grid_labels.append(QLabel(''))
                    self._grid_layout.addWidget(self._grid_labels[_label_counter],row,col)
                    _label_counter += 1
        
    def set_south_indian_chart_data(self, data, cell_width=75, cell_height=75, chart_title = None,image_icon_path="./images/lord_ganesha2.jpg"):
        """
        Sets the planet labels on to the south indian natal chart
        @param data: 2-D List of planet names in native language
        @param cell_width - in pixels 
        @param cell_height - in pixels
        @chart_title - title of chart (e.g. Raasi, Navamsam) to be displayed in the center of chart
        @image_icon_path - path of 50x50 pixel image you want to display in center of chart
        NOTE: For South Indian Chart - inner cells of 2-D list should have empty labels
        Example: [ ['Saturn','Moon','Sun', 'Mars'],
                   ['Lagnam', ''   , ''  , 'Ragu'],
                   ['Ketu'  , ''   , ''  , 'Mercury'],
                   [''      , 'Jupiter','','']]
        """
        row_count = len(data)
        col_count = len(data[0])
        # Create Labels
        _label_counter = 0
        for row in range(row_count):
            for col in range(col_count):
                cell = data[row][col]
                position = (row,col)
                if row==0 or row==row_count-1 or col==0 or col==col_count-1:
                    self._grid_labels[_label_counter].setText(cell)
                    self._grid_labels[_label_counter].setFixedHeight(cell_height)
                    self._grid_labels[_label_counter].setFixedWidth(cell_width)
                    self._grid_labels[_label_counter].setStyleSheet("border: 1px solid black;")
                # write chart title in center of the chart
                if row == (row_count/2)-1 and col==(col_count/2) and chart_title:
                    self._grid_labels[_label_counter].setText(chart_title)
                if row == (row_count/2) and col==(col_count/2)-1 and chart_title:
                    self._grid_labels[_label_counter].setPixmap(QtGui.QPixmap("./images/lord_ganesha2.jpg"))
                _label_counter += 1
class ChartWindow(QWidget):
    """
        Main Horoscope Window
        @param title - title of the window
        @param chart_type - South Indian (only supported for now)
        @param chart_language - English, Tamil, Telugu
        NOTE: You can add more languages yourself - by creating list_values_<lang>.txt and msg_string_<lang>.txt
                add adding the language to available_languages list
    """
    def __init__(self,title='',chart_type='South-Indian',chart_language='English'):
        super().__init__()
        fp = open('./program_inputs.txt', encoding='utf-8', mode='r')
        window_title = fp.readline().split('=')[1]
        header_title = fp.readline().split('=')[1]
        self._image_icon_path = fp.readline().split('=')[1]
        fp.close()
        self._language = list(available_languages.keys())[0]
        self._chart_type = available_chart_types[0]
        self.setFixedSize(650,580)
        self.setWindowTitle(window_title)
        v_layout = QVBoxLayout()
        footer_label = QLabel(header_title)#"Copyright © Dr. Sundar Sundaresan, Open Astro Technologies, USA.")
        footer_label.setStyleSheet("border: 1px solid black;")
        footer_label.setFont(QtGui.QFont("Arial Bold",12))
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setFixedHeight(15)
        footer_label.setFixedWidth(self.width())
        v_layout.addWidget(footer_label)
        h_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        h_layout.addWidget(name_label)
        self._name = "Bhuvana"
        self._name_text = QLineEdit(self._name)
        h_layout.addWidget(self._name_text)
        place_label = QLabel("Place:")
        h_layout.addWidget(place_label)
        self._place_name = 'Place_country' # 'Chennai, IN'
        self._place_text = QLineEdit(self._place_name)#"Chennai, IN")
        self._place_text.editingFinished.connect(lambda : self._get_place_latitude_longitude())#self._place_name))
        h_layout.addWidget(self._place_text)
        lat_label = QLabel("Latidude:")
        h_layout.addWidget(lat_label)
        self._latitude = 'xx.xxxx N|S'# '13.0389'
        self._lat_text = QLineEdit(self._latitude)#'xx.xxxx')#"13.0389")
        h_layout.addWidget(self._lat_text)
        long_label = QLabel("Longitude:")
        h_layout.addWidget(long_label)
        self._longitude = 'xx.xxxx E|W'#'80.2619'
        self._long_text = QLineEdit(self._longitude)#'xx.xxxx')#"80.2619")
        h_layout.addWidget(self._long_text)
        tz_label = QLabel("Time Zone:")
        h_layout.addWidget(tz_label)
        self._time_zone = '+|-x.xx'# '+5.5'
        self._tz_text = QLineEdit(self._time_zone)#'x.x')#"+5.5")
        h_layout.addWidget(self._tz_text)
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        dob_label = QLabel("Date of Birth:")
        h_layout.addWidget(dob_label)
        self._date_of_birth = 'yyyy,mm,dd'# '1996,12,7'
        self._dob_text = QLineEdit(self._date_of_birth)#'yyyy,mm,dd')#"1996,12,7")
        h_layout.addWidget(self._dob_text)
        tob_label = QLabel("Time of Birth:")
        h_layout.addWidget(tob_label)
        self._time_of_birth = 'hh:mm:ss' # '10:34:00'
        self._tob_text = QLineEdit(self._time_of_birth)#'hh:mm:ss')#"10:34:00")
        h_layout.addWidget(self._tob_text)
        ayan_label = QLabel("Ayanamsa:")
        h_layout.addWidget(ayan_label)
        available_ayanamsa_modes = panchanga.available_ayanamsa_modes.keys()
        self._ayanamsa_combo = QComboBox()
        self._ayanamsa_combo.addItems(available_ayanamsa_modes)
        self._ayanamsa_mode = "LAHIRI"
        self._ayanamsa_combo.setCurrentText(self._ayanamsa_mode)
        h_layout.addWidget(self._ayanamsa_combo)
        self._lang_combo = QComboBox()
        self._lang_combo.addItems(available_languages.keys())
        self._lang_combo.setCurrentText(self._language)
        h_layout.addWidget(self._lang_combo)
        compute_button = QPushButton("Show Chart")
        compute_button.setFont(QtGui.QFont("Arial Bold",9))
        compute_button.clicked.connect(self.compute_horoscope)
        h_layout.addWidget(compute_button)
        save_image_button = QPushButton("Save as PDF")
        save_image_button.setFont(QtGui.QFont("Arial Bold",8))
        save_image_button.clicked.connect(self.save_as_pdf)
        h_layout.addWidget(save_image_button)
        
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        self._info_label1 = QLabel("Information:")
        h_layout.addWidget(self._info_label1)
        self._info_label2 = QLabel("Information:")
        h_layout.addWidget(self._info_label2)
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        self._table1 = SouthIndianChart()
        h_layout.addWidget(self._table1)
        self._table2 = SouthIndianChart()
        h_layout.addWidget(self._table2)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
    def ayanamsa_mode(self, ayanamsa_mode, ayanamsa=None):
        """
            Set Ayanamsa mode
            @param ayanamsa_mode - Default - Lahiri
            Available ayanamsa_modes are 
            "FAGAN","KP", "LAHIRI""RAMAN","USHASHASHI""YUKTESHWAR", "SURYASIDDHANTA", "SURYASIDDHANTA_MSUN",
            "ARYABHATA", "ARYABHATA_MSUN", "SS_CITRA", "TRUE_CITRA", "TRUE_REVATI","SS_REVATI"
        """
        self._ayanamsa_mode = ayanamsa_mode
    def place(self,place_name):
        """
            Set the place of birth
            @param - place_name - Specify with country code. e.g. Chennai, IN
            NOTE: Uses Nominatim to get the latitude and longitude
            An error message displayed if lat/long could not be found in which case enter lat/long manually.
        """
        self._place_text.setText(place_name)
        self._place_name = place_name
        result = self._get_place_latitude_longitude()#place_name)
        if result == None:
            return
        [_,self._latitude,self._longitude,self._time_zone] = result
    def name(self,name):
        """
            Set name of the person whose horoscope is sought
            @param - Name of person
        """
        self._name = name
        self._name_text.setText(name)
    def latitude(self,latitude):
        """
            Sets the latitude manually
            @param - latitude
        """
        self._latitude = latitude
        self._lat_text.setText(latitude)
    def longitude(self,longitude):
        """
            Sets the longitude manually
            @param - longitude
        """
        self._longitude = longitude
        self._long_text.setText(longitude)
    def time_zone(self,time_zone):
        """
            Sets the time zone offset manually
            @param - time_zone - time zone offset
        """
        self._time_zone = time_zone
        self._tz_text.setText(time_zone)
    def date_of_birth(self, date_of_birth):
        """
            Sets the date of birth (Format:YYYY,MM,DD)
            @param - date_of_birth
        """
        self._date_of_birth = date_of_birth
        self._dob_text.setText(self._date_of_birth)
    def time_of_birth(self, time_of_birth):
        """
            Sets the time of birth (Format:HH:MM:SS)
            @param - time_of_birth
        """
        self._time_of_birth = time_of_birth
        self._tob_text.setText(self._time_of_birth)
    def chart_type(self,chart_type):
        """
            Sets the chart type (South Indian only supported now)
            @param - chart_type
        """
        if chart_type in available_chart_types:
            self._chart_type = chart_type
    def language(self,language):
        """
            Sets the language for display
            @param - language
        """
        if language in available_languages:
            self._language = language
            self._lang_combo.setCurrentText(language)
    def _validate_ui(self):
        all_data_ok = False
        all_data_ok = self._place_text.text().strip() != '' and \
                         self._name_text.text().strip() != '' and \
                         re.match(r"\d+\.\d+\s?[N|S]?", self._lat_text.text().strip(),re.IGNORECASE) and \
                         re.match(r"\d+\.\d+\s?[E|W]?", self._long_text.text().strip(),re.IGNORECASE) and \
                         re.match(r"[\+|\-]?\d{4}\,\d{1,2}\,\d{1,2}", self._dob_text.text().strip(),re.IGNORECASE) and \
                         re.match(r"\d{1,2}:\d{1,2}:\d{1,2}", self._tob_text.text().strip(),re.IGNORECASE)
        return all_data_ok        
    def compute_horoscope(self):
        """
            Compute the horoscope based on details entered
            if details missing - error is displayed            
        """
        if not self._validate_ui():
            print('values are not filled properly')
            return
        self._place_name = self._place_text.text()
        self._latitude = self._lat_text.text()
        self._longitude = self._long_text.text()
        self._time_zone = self._tz_text.text()
        self._language = self._lang_combo.currentText()
        self._date_of_birth = self._dob_text.text()
        self._time_of_birth = self._tob_text.text()
        if self._place_name.lower() == "place, country" or self._place_name.strip() == "":
            return
        horoscope_language = available_languages[self._language]
        self._ayanamsa_mode =  self._ayanamsa_combo.currentText()
        print('ayanamsa mode:',self._ayanamsa_mode)
        as_string = True
        if self._latitude.strip() == "" or self._longitude.strip() == "" or self._time_zone.strip() == "": 
            [self._place_name,self._latitude,self._longitude,self._time_zone] = panchanga.get_latitude_longitude_from_place_name(place_name)
            self._lat_text.setText(str(self._latitude))
            self._long_text.setText(str(self._longitude))
            self._tz_text.setText(str(self._time_zone))
        year,month,day = self._date_of_birth.split(",")
        birth_date = panchanga.Date(int(year),int(month),int(day)) #datetime(int(year),int(month),int(day))
        if (not self._place_name):
            a= horoscope.Horoscope(latitude=self._latitude,longitude=self._longitude,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode)
        else:
            a= horoscope.Horoscope(place_with_country_code=self._place_name,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode)
        self._calendar_info = a.get_calendar_information(language=available_languages[self._language],as_string=True)
        self._calendar_key_list= a._get_calendar_resource_strings(language=available_languages[self._language])
        self._horoscope_info, self._horoscope_charts, self._dhasa_bhukti_info = [],[],[]
        if as_string:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = a.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
        else:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = a.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
        self._update_chart_ui_with_info()
        
    def _update_chart_ui_with_info(self):
        info_str = ''
        format_str = '%-20s%-40s\n'
        key = 'sunrise_str'
        sunrise_time = self._calendar_info[self._calendar_key_list[key]]
        info_str += format_str % (self._calendar_key_list[key],sunrise_time)
        key = 'sunset_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = 'nakshatra_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = 'raasi_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = 'tithi_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = 'yogam_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = 'karanam_str'
        info_str += format_str % (self._calendar_key_list[key],self._calendar_info[self._calendar_key_list[key]])
        key = self._calendar_key_list['raasi_str']+'-'+self._calendar_key_list['ascendant_str']
        value = self._horoscope_info[key]#.split()[:1]
        info_str += format_str % (self._calendar_key_list['ascendant_str'],value)
        birth_time = self._time_of_birth
        info_str += format_str % (self._calendar_key_list['udhayathi_str'], _udhayadhi_nazhikai(birth_time,sunrise_time))
        self._info_label1.setText(info_str)
        info_str = ''
        dhasa = ''
        dhasa_end_date = ''
        di = 9
        for p,(k,v) in enumerate(self._dhasa_bhukti_info.items()):
            # get dhasa
            if (p+1) == di:
                dhasa = k.split("-")[0]#+ ' '+self._calendar_key_list['ends_at_str']
            # Get dhasa end date
            elif (p+1) == di+1:
                """ to account for BC Dates negative sign is introduced"""
                if len(v.split('-')) == 4:
                    _,year,month,day = v.split('-')
                    year = '-'+year
                else:
                    year,month,day = v.split('-')
                dhasa_end_date = year+'-'+month+'-'+str(int(day)-1)+ ' '+self._calendar_key_list['ends_at_str']
                info_str += format_str % (dhasa, dhasa_end_date)
                di += 9
        key = self._calendar_key_list['maasa_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        self._info_label2.setText(info_str)
        rasi_1d = self._horoscope_charts[0]
        rasi_2d = _convert_1d_house_data_to_2d(rasi_1d)
        nava_1d = self._horoscope_charts[4]
        nava_2d = _convert_1d_house_data_to_2d(nava_1d)
        self._table1.set_south_indian_chart_data(rasi_2d,chart_title=self._calendar_key_list['raasi_str'],image_icon_path=self._image_icon_path)
        self._table2.set_south_indian_chart_data(nava_2d,chart_title=self._calendar_key_list['navamsam_str'],image_icon_path=self._image_icon_path)
        
    def _get_place_latitude_longitude(self):
        place_name = self._place_text.text()
        result = panchanga.get_latitude_longitude_from_place_name(place_name)
        if result:
            [_,self._latitude,self._longitude,self._time_zone] = result
            self._place_name = place_name
            self._place_text.setText(self._place_name)
            self._lat_text.setText(str(self._latitude))
            self._long_text.setText(str(self._longitude))
            self._tz_text.setText(str(self._time_zone))
            return result
        else:
            msg = self._place_name+" could not be found in OpenStreetMap.\nTry entering latitude and longitude manually.\nOr try entering nearest big city"
            print(msg)
            QMessageBox.about(self,"City not found",msg)
    def save_as_pdf(self):
        """
            Save the displayed chart as a pdf
            Choose a file from file save dialog displayed
        """
        path = QFileDialog.getSaveFileName(self, 'Choose folder and file to save as PDF file', './output', 'PDF files (*.pdf)')#)
        pdf_file = path[0]
        image_file = "./main_window.png"
        if image_file:
            im = self.grab()
            im.save(image_file) 
            with open(pdf_file,"wb") as f:
                f.write(img2pdf.convert(image_file))
            f.close()
        if os.path.exists(image_file):
            os.remove(image_file)
def show_horoscope(data):
    """
        Same as class method show() to display the horoscope
        @param data - last chance to pass the data to the class
    """
    app=QApplication(sys.argv)
    window=ChartWindow(data)
    window.show()
    app.exec_()

def _convert_1d_house_data_to_2d(rasi_1d):
    map_to_2d = [ [11,0,1,2], [10,"","",3], [9,"","",4], [8,7,6,5] ]
    rasi_2d = [['']*4 for _ in range(4)]
    for p,val in enumerate(rasi_1d):
        i,j = [(index, row.index(p)) for index, row in enumerate(map_to_2d) if p in row][0]
        rasi_2d[i][j] = val
    return rasi_2d
def _udhayadhi_nazhikai(birth_time,sunrise_time):
    def _convert_str_to_time(str_time):
        arr = str_time.split(':')
        arr[-1] = arr[-1].replace('AM','').replace('PM','')
        return time(int(arr[0]),int(arr[1]),int(arr[2]))
    birth_time = _convert_str_to_time(birth_time)
    sunrise_time =_convert_str_to_time(sunrise_time)
    import math
    days = 0
    duration = str(datetime.combine(date.min, birth_time) - datetime.combine(date.min, sunrise_time))
    hour_sign = ''
    if " day" in duration:
        duration = str(datetime.combine(date.min, sunrise_time) - datetime.combine(date.min, birth_time))
        hour_sign = '-'
    hours,minutes,seconds = duration.split(":")
    tharparai = (int(hours)+days)*9000+int(minutes)*150+int(seconds)
    naazhigai = math.floor(tharparai/3600)
    vinadigal = math.floor( (tharparai-(naazhigai*3600))/60 )
    tharparai = math.floor(tharparai - naazhigai*3600 - vinadigal*60)
    return hour_sign+str(naazhigai)+':'+str(vinadigal)+':'+str(tharparai)
def _get_date_difference(then, now = datetime.now(), interval = "default"):
    from dateutil import relativedelta
    diff = relativedelta.relativedelta(now,then)
    years = diff.years
    months = diff.months
    days = diff.days
    return [years,months,days]
def _dhasa_balance(date_of_birth,dhasa_end_date):
    duration = _get_date_difference(date_of_birth,dhasa_end_date)#,starting_text="Dhasa Balance:")
    print(duration)
if __name__ == "__main__":
    """
    date_of_birth = datetime(1996,12,7)
    dhasa_end_date = datetime(2014,7,21)
    _dhasa_balance(date_of_birth,dhasa_end_date)
    """
    """
    time_of_birth = '5:22:15' #time(5,22,15)
    sunrise_time = '6:22:15'# time(6,22,15)
    print(_udhayadhi_nazhikai(time_of_birth, sunrise_time))
    exit()
    """
    """
    place_name='Karamdai,IN'
    result = panchanga.get_latitude_longitude_from_place_name(place_name)
    if result:
        print('result',result)
    else:
        print('else')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('could not locate',place_name)
        msg.setWindowTitle("Error")
        msg.exec_()
        print('end')
    exit()
    """
    #"""
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook
    app=QApplication(sys.argv)
    chart=ChartWindow('FreeHoro 1.0.1 beta')
    chart.chart_type('South-Indian')
    chart.language('Tamil')
    chart.name('Bhuvana')
    chart.place('Chennai,IN')
    chart.date_of_birth('1996,12,7')
    chart.time_of_birth('10:34:00')
    chart.compute_horoscope()
    chart.show()
    #chart.save_as_pdf()
    sys.exit(app.exec())      
    #"""