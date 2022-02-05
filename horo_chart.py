import re
import sys
import os
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from _datetime import datetime, timedelta,time,date
import img2pdf

panchanga = __import__('panchanga')
horoscope = __import__('horoscope')
available_chart_types = ['south indian','north indian','east indian']#,'Western']
available_languages = {"English":'en','Tamil':'ta','Telugu':'te'}
class EastIndianChart(QWidget):
    """
        Draws East Indian Natal Chart and labels the planets
        East Indian chart is 3x3 goes anti-clockwise from top-middle
        @param data: 2-D List of planet names in native language
        NOTE: For East Indian Chart - inner cells of 2-D list should have empty labels
        [ [3/2  1  12/11],
          [ 4   ""  10  ],
          [ 5/6 7  8/9]  
        Example: [ ['Saturn/Moon',     'Neptune',       'Mars'/'Sun'],
                   ['Lagnam',          ''   ,     'Ragu'],
                   ['Ketu/Venus',    'Pluto',  'Mercury/Jupiter']
                ]
    """
    def __init__(self,data=None,*args):
        QWidget.__init__(self, *args)
        self._grid_layout = QGridLayout()
        self.setLayout(self._grid_layout)
        self._grid_labels = []
        self.row_count = 3
        self.col_count = 3
        self.x = 5
        self.y = 5# 250
        self.house_width = 100
        self.house_height = 100
        self.data = data
        self._chart_title = ''
        if self.data==None:
            self.data = ['','','','','','','','','','','','']
    def paintEvent(self, event):
        self.event = event
        self.set_east_indian_chart_data()#event)
    def setData(self,data,chart_title=''):#,event=None):
        self._chart_title = chart_title
        self.data = data
        event = self.event
    def set_east_indian_chart_data(self):
        """
        Sets the planet labels on to the east indian natal chart
        NOTE: For East Indian Chart - inner cells of 2-D list should have empty labels
                And corner cells are divided by a separator
        Example: [ ['Saturn/""',     'Moon',       'Mars'/'Sun'],
                   ['Lagnam',          ''   ,     'Ragu'],
                   ['Ketu/Venus',    'Jupiter',  '""/Jupiter']
                ]
        """
        painter = QPainter(self)
        data = self.data
        chart_title = self._chart_title
        row_count = len(data)
        col_count = len(data[0])
        cell_width = self.house_width
        cell_height = self.house_height
        chart_width = self.col_count * cell_width
        chart_height = self.row_count * cell_height
        _label_counter = 0
        for row in range(row_count):
            for col in range(col_count):
                left_top_cell = (row==0 and col==0) 
                right_bottom_cell = (row==row_count-1 and col==col_count-1)
                right_top_cell = (row==0 and col==col_count-1) 
                left_bottom_cell = (row==row_count-1 and col==0)
                center_cell = row==1 and col==1
                cell = data[row][col]
                cell_x = self.x + col * cell_width
                cell_y = self.y + row * cell_height
                rect = QtCore.QRect(cell_x,cell_y,cell_width,cell_height)
                painter.drawRect(rect)
                if left_top_cell:
                    bottom_cell_text,top_cell_text = cell.split("/")
                    # House 3
                    painter.drawText(rect,Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight,top_cell_text)
                    # House 2
                    painter.drawText(rect,Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeft,bottom_cell_text)
                    # Draw cross line
                    diag_start_x = self.x
                    diag_start_y = self.y
                    diag_end_x = self.x + cell_width
                    diag_end_y = self.y + cell_height
                    painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
                elif right_top_cell:
                    bottom_cell_text,top_cell_text = cell.split("/")
                    # House 11
                    painter.drawText(rect,Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft,top_cell_text)
                    # House 12
                    painter.drawText(rect,Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignRight,bottom_cell_text)
                    # Draw cross line
                    diag_start_x = self.x + chart_width
                    diag_start_y = self.y
                    diag_end_x = self.x + chart_width - cell_width
                    diag_end_y = self.y + cell_height
                    painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
                elif right_bottom_cell:
                    bottom_cell_text,top_cell_text = cell.split("/")
                    # House 8
                    painter.drawText(rect,Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeft,bottom_cell_text)
                    # House 9
                    painter.drawText(rect,Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight,top_cell_text)
                    # Draw cross line
                    diag_start_x = self.x + chart_width - cell_width
                    diag_start_y = self.y + chart_height - cell_height
                    diag_end_x = self.x + chart_width
                    diag_end_y = self.y + chart_height
                    painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
                elif left_bottom_cell:
                    bottom_cell_text,top_cell_text = cell.split("/")
                    # House 5
                    painter.drawText(rect,Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft,bottom_cell_text)
                    # House 6
                    painter.drawText(rect,Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignRight,top_cell_text)
                    # Draw cross line
                    diag_start_x = self.x
                    diag_start_y = self.y + chart_height
                    diag_end_x = self.x + cell_width
                    diag_end_y = self.y + chart_height - cell_height
                    painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
                # write chart title in center of the chart
                elif center_cell and chart_title:
                    painter.drawText(rect,Qt.AlignmentFlag.AlignCenter,chart_title)
                else:
                    painter.drawText(rect,Qt.AlignmentFlag.AlignCenter,cell)
        painter.end()
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
    def __init__(self,data=None,*args):
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
class NorthIndianChart(QWidget):
    def __init__(self,data=None):
        QWidget.__init__(self)
        self.row_count = 4
        self.col_count = 4
        self.data = data
        self.x = 5
        self.y = 5# 250
        self.house_width = 67
        self.house_height = 67
        self._grid_labels = []
        self.label_positions = [(4/10,2/10),(1.5/10,0.5/10),(0.1/10,2/10),(1.5/10,4/10), 
                 (0.1/10,7/10), (1.75/10,8.5/10), (3.5/10,7/10), (6.75/10,8.5/10),
                 (8.5/10,7/10),(6.5/10,4/10),(8.35/10,2.0/10),(6.5/10,0.5/10)]
        if self.data==None:
            self.data = ['','','','','','','','','','','','']
    def paintEvent(self, event):
        self.event = event
        self._draw_north_indian_chart()#event)
    def setData(self,data):#,event=None):
        self.data = data
        event = self.event
    def _draw_north_indian_chart(self):#,event):
        painter = QPainter(self)
        chart_width = self.col_count * self.house_width
        chart_height = self.row_count * self.house_height
        # first draw a square 
        rect = QtCore.QRect(self.x,self.y,chart_width,chart_height)
        painter.drawRect(rect)
        # draw diagonals
        diag_start_x = self.x
        diag_start_y = self.y
        diag_end_x = diag_start_x + chart_width
        diag_end_y = diag_start_y + chart_height
        #print('draw diagnonal 1',diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        diag_start_x = self.x
        diag_start_y = self.y + chart_height
        diag_end_x = self.x + chart_width
        diag_end_y = self.y
        #print('draw diagnonal 2',diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        # Draw internal square
        start_x = self.x
        start_y = self.y + chart_height / 2
        end_x = self.x + chart_width / 2
        end_y = self.y
        #print('Line-1:start_x,start_y,end_x,end_y',start_x,start_y,end_x,end_y)
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x + chart_width
        end_y = self.y + chart_height / 2
        #print('Line-2:start_x,start_y,end_x,end_y',start_x,start_y,end_x,end_y)
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x + chart_width / 2
        end_y = self.y + chart_height
        #print('Line-3:start_x,start_y,end_x,end_y',start_x,start_y,end_x,end_y)
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x
        end_y = self.y + chart_height / 2
        #print('Line-4:start_x,start_y,end_x,end_y',start_x,start_y,end_x,end_y)
        painter.drawLine(start_x,start_y,end_x,end_y) 
        #print('_draw_north_indian_labels')
        chart_width = self.col_count * self.house_width
        chart_height = self.row_count * self.house_height
        _label_counter = 0
        for l, pos in enumerate(self.label_positions):
            x = pos[0]
            y = pos[1]
            label_text = self.data[l]
            label_x = self.x + x*chart_width
            label_y = self.y + y*chart_height
            painter.drawText(QtCore.QRect(label_x,label_y,self.house_width,self.house_height),0,label_text)
            _label_counter += 1
        painter.end()
class ChartWindow(QWidget):
    def __init__(self,chart_type='south indian'):
        super().__init__()
        fp = open('./program_inputs.txt', encoding='utf-8', mode='r')
        window_title = fp.readline().split('=')[1]
        header_title = fp.readline().split('=')[1]
        self._image_icon_path = fp.readline().split('=')[1]
        fp.close()
        self.setWindowIcon(QtGui.QIcon("./images/lord_ganesha2.jpg"))
        self._language = list(available_languages.keys())[0]
        self._chart_type = 'south indian'
        ci = _index_containing_substring(available_chart_types,chart_type.lower())
        if ci >=0:
            self._chart_type = available_chart_types[ci]
        self.setFixedSize(650,630)
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
        self._name_text = QLineEdit("")
        self._name = self._name_text.text()
        self._name_text.setToolTip('Enter your name')
        h_layout.addWidget(self._name_text)
        place_label = QLabel("Place:")
        h_layout.addWidget(place_label)
        self._place_name = '' # 'Chennai, IN'
        self._place_text = QLineEdit(self._place_name)#"Chennai, IN")
        self._place_text.editingFinished.connect(lambda : self._get_place_latitude_longitude(self._place_text.text()))
        self._place_text.setToolTip('Enter place of birth, country name')
        h_layout.addWidget(self._place_text)
        lat_label = QLabel("Latidude:")
        h_layout.addWidget(lat_label)
        self._lat_text = QLineEdit('')
        self._latitude = 0.0
        self._lat_text.setToolTip('Enter Latitude preferably exact at place of birth: Format: +/- xx.xxx')
        h_layout.addWidget(self._lat_text)
        long_label = QLabel("Longitude:")
        h_layout.addWidget(long_label)
        self._long_text = QLineEdit('')#'xx.xxxx')#"80.2619")
        self._longitude = 0.0
        self._long_text.setToolTip('Enter Longitude preferably exact at place of birth. Format +/- xx.xxx')
        h_layout.addWidget(self._long_text)
        tz_label = QLabel("Time Zone:")
        h_layout.addWidget(tz_label)
        self._tz_text = QLineEdit('')#'x.x')#"+5.5")
        self._time_zone = 0.0
        self._tz_text.setToolTip('Enter Time offset from GMT e.g. -5.5 or 4.5')
        h_layout.addWidget(self._tz_text)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        dob_label = QLabel("Date of Birth:")
        h_layout.addWidget(dob_label)
        self._date_of_birth = ''# '1996,12,7'
        self._dob_text = QLineEdit(self._date_of_birth)#'yyyy,mm,dd')#"1996,12,7")
        self._dob_text.setToolTip('Date of birth in the format YYYY,MM,DD\nFor BC enter negative years')
        h_layout.addWidget(self._dob_text)
        tob_label = QLabel("Time of Birth:")
        h_layout.addWidget(tob_label)
        self._time_of_birth = '' # '10:34:00'
        self._tob_text = QLineEdit(self._time_of_birth)#'hh:mm:ss')#"10:34:00")
        self._tob_text.setToolTip('Enter time of birth in the format HH:MM:SS if afternoon use 12+ hours')
        h_layout.addWidget(self._tob_text)
        self._chart_type_combo = QComboBox()
        self._chart_type_combo.addItems(available_chart_types)
        self._chart_type_combo.setToolTip('Choose birth chart style north, south or east indian')
        self._chart_type_combo.setCurrentText(self._chart_type)
        h_layout.addWidget(self._chart_type_combo)
        available_ayanamsa_modes = panchanga.available_ayanamsa_modes.keys()
        self._ayanamsa_combo = QComboBox()
        self._ayanamsa_combo.addItems(available_ayanamsa_modes)
        self._ayanamsa_combo.setToolTip('Choose Ayanamsa mode from the list')
        self._ayanamsa_mode = "LAHIRI"
        self._ayanamsa_combo.setCurrentText(self._ayanamsa_mode)
        h_layout.addWidget(self._ayanamsa_combo)
        self._lang_combo = QComboBox()
        self._lang_combo.addItems(available_languages.keys())
        self._lang_combo.setCurrentText(self._language)
        self._lang_combo.setToolTip('Choose language for display')
        h_layout.addWidget(self._lang_combo)
        compute_button = QPushButton("Show Chart")
        compute_button.setFont(QtGui.QFont("Arial Bold",9))
        compute_button.clicked.connect(self.compute_horoscope)
        compute_button.setToolTip('Click to update the chart information based on selections made')
        h_layout.addWidget(compute_button)
        save_image_button = QPushButton("Save as PDF")
        save_image_button.setFont(QtGui.QFont("Arial Bold",8))
        save_image_button.clicked.connect(self.save_as_pdf)
        save_image_button.setToolTip('Click to save horoscope as a PDF')
        h_layout.addWidget(save_image_button)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self._info_label1 = QLabel("Information:")
        self._info_label1.setStyleSheet("border: 1px solid black;")
        self._info_label1.setFixedHeight(220)
        h_layout.addWidget(self._info_label1)
        self._info_label2 = QLabel("Information:")
        self._info_label2.setStyleSheet("border: 1px solid black;")
        self._info_label2.setFixedHeight(220)
        h_layout.addWidget(self._info_label2)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        if self._chart_type.lower() == 'south indian':
            self._table1 = SouthIndianChart()
            self._table2 = SouthIndianChart()
        elif self._chart_type.lower() == 'east indian':
            self._table1 = EastIndianChart()
            self._table2 = EastIndianChart()
        else:
            self._table1 = NorthIndianChart()
            self._table2 = NorthIndianChart()
        h_layout.addWidget(self._table1)
        h_layout.addWidget(self._table2)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        self._v_layout = v_layout
    def _on_application_exit(self):
        def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)
        sys.excepthook = except_hook
        QApplication.quit()
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
        self._place_name = place_name
        result = self._get_place_latitude_longitude(place_name)
        if result == None:
            return
        [self._place_name,self._latitude,self._longitude,self._time_zone] = result
    def name(self,name):
        """
            Set name of the person whose horoscope is sought
            @param - Name of person
        """
        self._name = name
        self._name_text.setText(name)
    def chart_type(self,chart_type):
        """
            Set chart type of the horoscope
            @param - chart_type:
                options: 'south indian'. 'north indian'
                Default: south indian
        """
        ci = _index_containing_substring(available_chart_types,chart_type.lower())
        if ci >=0:
            self._chart_type = available_chart_types[ci]
            self._chart_type_combo.setCurrentText(chart_type.lower())
    def latitude(self,latitude):
        """
            Sets the latitude manually
            @param - latitude
        """
        self._latitude = float(latitude)
        self._lat_text.setText(latitude)
    def longitude(self,longitude):
        """
            Sets the longitude manually
            @param - longitude
        """
        self._longitude = float(longitude)
        self._long_text.setText(longitude)
    def time_zone(self,time_zone):
        """
            Sets the time zone offset manually
            @param - time_zone - time zone offset
        """
        self._time_zone = float(time_zone)
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
                         re.match(r"[\+|\-]?\d+\.\d+\s?", self._lat_text.text().strip(),re.IGNORECASE) and \
                         re.match(r"[\+|\-]?\d+\.\d+\s?", self._long_text.text().strip(),re.IGNORECASE) and \
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
        self._latitude = float(self._lat_text.text())
        self._longitude = float(self._long_text.text())
        self._time_zone = float(self._tz_text.text())
        self._language = self._lang_combo.currentText()
        self._date_of_birth = self._dob_text.text()
        self._time_of_birth = self._tob_text.text()
        if self._place_name.strip() == "":
            print("Please enter a place of birth")
            return
        horoscope_language = available_languages[self._language]
        self._ayanamsa_mode =  self._ayanamsa_combo.currentText()
        print('ayanamsa mode:',self._ayanamsa_mode)
        as_string = True
        if self._place_name.strip() == '' and abs(self._latitude) > 0.0 and abs(self._longitude) > 0.0 and abs(self._time_zone) > 0.0: 
            [self._place_name,self._latitude,self._longitude,self._time_zone] = panchanga.get_latitude_longitude_from_place_name(place_name)
            self._lat_text.setText((self._latitude))
            self._long_text.setText((self._longitude))
            self._tz_text.setText((self._time_zone))
        year,month,day = self._date_of_birth.split(",")
        birth_date = panchanga.Date(int(year),int(month),int(day))
        ' set the chart type and reset widgets'
        self._table1.deleteLater()
        self._table2.deleteLater()
        self._chart_type = self._chart_type_combo.currentText()
        if self._chart_type.lower() == 'south indian':
            self._table1 = SouthIndianChart()
            self._table2 = SouthIndianChart()
        elif self._chart_type.lower() == 'east indian':
            self._table1 = EastIndianChart()
            self._table2 = EastIndianChart()
        else:
            self._table1 = NorthIndianChart()
            self._table2 = NorthIndianChart()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self._table1)
        h_layout.addWidget(self._table2)
        self._v_layout.addLayout(h_layout)
        self._table1.update()
        self._table2.update()
        print(self._place_name,self._latitude,self._longitude,self._time_zone)
        if self._place_name.strip() != '' and abs(self._latitude) > 0.0 and abs(self._longitude) > 0.0 and abs(self._time_zone) > 0.0:
            self._horo= horoscope.Horoscope(latitude=self._latitude,longitude=self._longitude,timezone_offset=self._time_zone,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode)
        else:
            self._horo= horoscope.Horoscope(place_with_country_code=self._place_name,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode)
        self._calendar_info = self._horo.get_calendar_information(language=available_languages[self._language],as_string=True)
        self._calendar_key_list= self._horo._get_calendar_resource_strings(language=available_languages[self._language])
        self._horoscope_info, self._horoscope_charts, self._dhasa_bhukti_info = [],[],[]
        if as_string:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = self._horo.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
        else:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = self._horo.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
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
        key = self._calendar_key_list['kali_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        key = self._calendar_key_list['vikrama_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        key = self._calendar_key_list['saka_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        self._info_label1.setText(info_str)
        info_str = ''
        dhasa = list(self._dhasa_bhukti_info.keys())[8].split('-')[0]
        deb = list(self._dhasa_bhukti_info.values())[8]
        dob = self._dob_text.text().replace(',','-')
        #print('dhasa balance',dhasa,deb,dob)
        years,months,days = _dhasa_balance(dob, deb)
        value = str(years)+':'+ str(months)+':'+ str(days)
        key = dhasa + ' '+self._calendar_key_list['balance_str']
        #print(key,value)
        info_str += format_str % (key,value)
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
        if self._chart_type.lower() == 'north indian':
            jd = self._horo.julian_day  # For ascendant and planetary positions, dasa buthi - use birth time
            place = panchanga.Place(self._place_name,float(self._latitude),float(self._longitude),float(self._time_zone))
            _ascendant = panchanga.ascendant(jd,place,False)
            asc_house = _ascendant[0]+1
            rasi_north = rasi_1d[asc_house-1:]+rasi_1d[0:asc_house-1]
            self._table1.setData(rasi_north)
            self._table1.update()
        elif self._chart_type.lower() == 'east indian':
            rasi_2d = _convert_1d_house_data_to_2d(rasi_1d,self._chart_type)
            self._table1.setData(rasi_2d,chart_title=self._calendar_key_list['raasi_str'])
        else: # south indian
            rasi_2d = _convert_1d_house_data_to_2d(rasi_1d)
            self._table1.set_south_indian_chart_data(rasi_2d,chart_title=self._calendar_key_list['raasi_str'],image_icon_path=self._image_icon_path)
        nava_1d = self._horoscope_charts[4]
        if self._chart_type.lower() == 'north indian':
            jd = self._horo.julian_day  # For ascendant and planetary positions, dasa buthi - use birth time
            place = panchanga.Place(self._place_name,float(self._latitude),float(self._longitude),float(self._time_zone))
            ascendant_longitude = panchanga.ascendant(jd,place,as_string=False)[1]
            ascendant_navamsa = panchanga.dasavarga_from_long(ascendant_longitude,9)
            asc_house = ascendant_navamsa+1
            nava_north = nava_1d[asc_house-1:]+nava_1d[0:asc_house-1]
            self._table2.setData(nava_north)
            self._table2.update()
        elif self._chart_type.lower() == 'east indian':
            nava_2d = _convert_1d_house_data_to_2d(nava_1d,self._chart_type)
            self._table2.setData(nava_2d,chart_title=self._calendar_key_list['navamsam_str'])
        else: # south indian
            nava_2d = _convert_1d_house_data_to_2d(nava_1d)
            self._table2.set_south_indian_chart_data(nava_2d,chart_title=self._calendar_key_list['navamsam_str'],image_icon_path=self._image_icon_path)
    def _get_place_latitude_longitude(self,place_name):
        result = panchanga.get_latitude_longitude_from_place_name(place_name)
        if result:
            [self._place_name,self._latitude,self._longitude,self._time_zone] = result
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

def _index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1
def _convert_1d_house_data_to_2d(rasi_1d,chart_type='south indian'):
    separator = '/'
    if 'south' in chart_type.lower():
        row_count = 4
        col_count = 4
        map_to_2d = [ [11,0,1,2], [10,"","",3], [9,"","",4], [8,7,6,5] ]
    elif 'east' in chart_type.lower():
        row_count = 3
        col_count = 3
        map_to_2d = [['2'+separator+'1','0','11'+separator+'10'], ['3', "",'9' ], ['4'+separator+'5','6','7'+separator+'8']]
    rasi_2d = [['X']*row_count for _ in range(col_count)]
    for p,val in enumerate(rasi_1d):
        #print('p,val',p,val,'<<')
        for index, row in enumerate(map_to_2d):
            #print('index,row',index,row)
            if 'south' in chart_type.lower():
                i,j = [(index, row.index(p)) for index, row in enumerate(map_to_2d) if p in row][0]
                rasi_2d[i][j] = val
            elif 'east' in chart_type.lower():
                p_index = _index_containing_substring(row,str(p))
                #print('str(p),row,p_index,val',str(p),row,p_index,val,'<<')
                if p_index != -1:
                    i,j = (index, p_index)
                    if rasi_2d[i][j] != 'X':
                        if index > 0:
                            rasi_2d[i][j] += separator + val
                        else:
                            rasi_2d[i][j] = val + separator + rasi_2d[i][j]
                    else:
                        rasi_2d[i][j] = val
                    #print('i,j,val,rasi_2d[i,j]',i,j,val,'<<',rasi_2d[i][j])
    for i in range(row_count):
        for j in range(col_count):
            if rasi_2d[i][j] == 'X':
                rasi_2d[i][j] = ''
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
    years = abs(diff.years)
    months = abs(diff.months)
    days = abs(diff.days)
    return [years,months,days]
def _dhasa_balance(date_of_birth,dhasa_end_date):
    d_arr = date_of_birth.split('-')
    if len(d_arr) == 4:
        _,year,month,day = d_arr
    else:
        year,month,day = d_arr
    dob = datetime(abs(int(year)),int(month),int(day))
    d_arr = dhasa_end_date.split('-')
    if len(d_arr) == 4:
        _,year,month,day = d_arr
    else:
        year,month,day = d_arr
    ded = datetime(abs(int(year)),int(month),int(day))
    duration = _get_date_difference(dob,ded)#,starting_text="Dhasa Balance:")
    return duration
if __name__ == "__main__":
    def except_hook(cls, exception, traceback):
        print('exception called')
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook
    App = QApplication(sys.argv)
    chart_type = 'North'
    chart = ChartWindow(chart_type=chart_type)
    chart.language('Tamil')
    """
    chart.name('Krishna')
    chart.place('Mathura,IN')
    chart.date_of_birth('-3229,6,17')
    chart.time_of_birth('23:59:00')
    chart.time_zone('-5.0')
    chart.chart_type(chart_type)
    """
    chart.compute_horoscope()
    chart.show()
    sys.exit(App.exec())
