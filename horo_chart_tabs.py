import re
import sys
import os
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from _datetime import datetime,timedelta,time,date
import time as time_sleep
import img2pdf

_images_path = './images/'
""" UI Constants """
_main_window_width = 650
_main_window_height = 490 #630
_info_label1_height = 200
_info_label2_height = 200
_chart_info_label_width = 100
_east_chart_house_x = 5
_east_chart_house_y = 5
_east_chart_house_width = 95
_east_chart_house_height = 95
_north_chart_house_x = 5
_north_chart_house_y = 5
_north_chart_house_width = 67
_north_chart_house_height = 67
_north_label_positions = [(4/10,2/10),(1.5/10,0.5/10),(0.1/10,2/10),(1.5/10,4/10), 
                 (0.1/10,7/10), (1.75/10,8.5/10), (3.5/10,7/10), (6.75/10,8.5/10),
                 (8.5/10,7/10),(6.5/10,4/10),(8.35/10,2.0/10),(6.5/10,0.5/10)]
_footer_label_font_height = 8
_footer_label_height = 26
_lagnam_line_factor = 0.25
_lagnam_line_thickness = 3
_tab_names = ['panchangam_str','raasi_str','hora_str','drekkanam_str','saptamsam_str','navamsam_str',\
              'dhasamsam_str','dhwadamsam_str','thrisamsam_str','sashtiamsam_str','dhasa_bhukthi_str','compatibility_str']
_dhasa_bhukthi_tab_start = 10
_dhasa_bhukthi_tab_count = 3
_compatibility_tab_start = 13
_compatibility_tab_count = 2
_tab_count = len(_tab_names)

panchanga = __import__('panchanga')
horoscope = __import__('horoscope')
compatibility = __import__('compatibility')
available_chart_types = {'south indian':"SouthIndianChart",'north indian':'NorthIndianChart','east indian':'EastIndianChart'}#,'Western'}
available_languages = {"English":'en','Tamil':'ta','Telugu':'te','Hindi':"hi"}
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
        self._asc_house = 0
        self.x = _east_chart_house_x
        self.y = _east_chart_house_y
        self.house_width = _east_chart_house_width
        self.house_height = _east_chart_house_height
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
                And corner cells should be divided by a separator /
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
            _label_counter += 1
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
        self.row_count = 4
        self.col_count = 4
        self._asc_house = 0
        self._grid_labels = []
        self._initialize_south_indian_chart_labels(self._grid_layout)
        if data:
            set_south_indian_chart_data(data)
    def paintEvent(self, event):
        painter = QPainter(self)
        house_x = self._grid_labels[self._asc_house].x()
        house_y = self._grid_labels[self._asc_house].y()
        house_width = self._grid_labels[self._asc_house].width()
        house_height = self._grid_labels[self._asc_house].height()
        line_start_x = house_x
        line_start_y = house_y + _lagnam_line_factor * house_height
        line_end_x = house_x + _lagnam_line_factor * house_width
        line_end_y = house_y
        painter.setPen(QPen(Qt.GlobalColor.black,_lagnam_line_thickness))
        painter.drawLine(line_start_x,line_start_y,line_end_x,line_end_y)
    def _initialize_south_indian_chart_labels(self,grid_layout):
        _label_counter = 0
        row_count = self.row_count
        col_count = self.col_count
        chart_title = ''
        for row in range(row_count):
            for col in range(col_count):
                    self._grid_labels.append(QLabel(''))
                    self._grid_layout.addWidget(self._grid_labels[_label_counter],row,col)
                    _label_counter += 1
        
    def set_south_indian_chart_data(self, data, cell_width=75, cell_height=75, chart_title = None,image_icon_path=_images_path+"/lord_ganesha2.jpg"):
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
                    self._grid_labels[_label_counter].setPixmap(QtGui.QPixmap(_images_path+"lord_ganesha2.jpg"))
                _label_counter += 1
class NorthIndianChart(QWidget):
    def __init__(self,data=None):
        QWidget.__init__(self)
        self.row_count = 4
        self.col_count = 4
        self.data = data
        self.x = _north_chart_house_x
        self.y = _north_chart_house_y
        self.house_width = _north_chart_house_width
        self.house_height = _north_chart_house_height
        self.resources=[]
        self._grid_labels = []
        self.label_positions = _north_label_positions
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
        painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        diag_start_x = self.x
        diag_start_y = self.y + chart_height
        diag_end_x = self.x + chart_width
        diag_end_y = self.y
        painter.drawLine(diag_start_x,diag_start_y,diag_end_x,diag_end_y)
        # Draw internal square
        start_x = self.x
        start_y = self.y + chart_height / 2
        end_x = self.x + chart_width / 2
        end_y = self.y
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x + chart_width
        end_y = self.y + chart_height / 2
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x + chart_width / 2
        end_y = self.y + chart_height
        painter.drawLine(start_x,start_y,end_x,end_y) 
        start_x = end_x
        start_y = end_y
        end_x = self.x
        end_y = self.y + chart_height / 2
        painter.drawLine(start_x,start_y,end_x,end_y) 
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
        self._init_main_window()
        self._v_layout = QVBoxLayout()
        self._create_row1_ui()
        self._create_row2_ui()
        self.tabWidget = QTabWidget()
        self._v_layout.addWidget(self.tabWidget)
        self.tabNames = _tab_names #["Panchangam","Rasi/Navamsam"]#,"Navamsam":''}
        self.tabCount = len(self.tabNames)
        self.tabWidgets = []
        self._charts = []
        self._chart_info_labels= []
        t = 0
        for tabName in self.tabNames:
            self.tabWidgets.append(QWidget())
            self.tabWidget.addTab(self.tabWidgets[t],tabName)
            if t==0:
                self._init_panchanga_tab_widgets(t)
                t+=1
            elif t==self.tabCount-2:
                self._init_dhasa_bhukthi_tab_widgets(t)
                t += _dhasa_bhukthi_tab_count
            elif t==self.tabCount-1:
                self._init_compatibility_tab_widgets(t)
                t += _compatibility_tab_count
            else:
                self._init_chart_tab_widgets(t)
                t +=1
            #getattr(self,tab_function)(t)
        self._add_footer_to_chart()
        self.setLayout(self._v_layout)
    def _init_compatibility_tab_widgets(self,tab_index):
        """ Add two more tabs for compatibility """
        for t in range(1,_compatibility_tab_count):
            self.tabWidgets.append(QWidget())
            self.tabWidget.addTab(self.tabWidgets[tab_index+t],'')
        self.tabCount += _compatibility_tab_count-1
        self.match_tables = [[ QTableWidget(13,4) for i in range(_compatibility_tab_count)] for j in range(4)] 
        for db_tab in range(_compatibility_tab_count):
            grid_layout = QGridLayout()
            for col in range(2):
                #self.match_tables[db_tab][col].horizontalHeader().hide()
                self.match_tables[db_tab][col].verticalHeader().hide()
                self.match_tables[db_tab][col].setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.match_tables[db_tab][col].setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                grid_layout.addWidget(self.match_tables[db_tab][col],1,col)
            self.tabWidgets[_compatibility_tab_start+db_tab].setLayout(grid_layout)
            self.tabWidget.setTabText(_compatibility_tab_start+db_tab,'compatibility_str'+'-'+str(db_tab+1))
    def _init_dhasa_bhukthi_tab_widgets(self,tab_index):
        """ Add two more tabs for dhasa-bhukthi """
        for t in range(1,_dhasa_bhukthi_tab_count):
            self.tabWidgets.append(QWidget())
            self.tabWidget.addTab(self.tabWidgets[tab_index+t],'')
        #self.tabWidgets.append(QWidget())
        #self.tabWidget.addTab(self.tabWidgets[tab_index+2],'')
        self.tabCount += _dhasa_bhukthi_tab_count-1
        self.db_tables = [[ QTableWidget(10,2) for i in range(_dhasa_bhukthi_tab_count)] for j in range(3)] 
        for db_tab in range(_dhasa_bhukthi_tab_count):
            grid_layout = QGridLayout()
            for col in range(3):
                self.db_tables[db_tab][col].horizontalHeader().hide()
                self.db_tables[db_tab][col].verticalHeader().hide()
                self.db_tables[db_tab][col].setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.db_tables[db_tab][col].setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                grid_layout.addWidget(self.db_tables[db_tab][col],1,col)
            self.tabWidgets[_dhasa_bhukthi_tab_start+db_tab].setLayout(grid_layout)
            self.tabWidget.setTabText(_dhasa_bhukthi_tab_start+db_tab,'dhasa_bhukthi_str-'+str(db_tab+1))
    def _init_panchanga_tab_widgets(self,tab_index):
        h_layout = QHBoxLayout()
        self._info_label1 = QLabel("Information:")
        self._info_label1.setStyleSheet("border: 1px solid black;")
        self._info_label1.setFixedHeight(_info_label1_height)
        h_layout.addWidget(self._info_label1)
        self._info_label2 = QLabel("Information:")
        self._info_label2.setStyleSheet("border: 1px solid black;")
        self._info_label2.setFixedHeight(_info_label2_height)
        h_layout.addWidget(self._info_label2)
        #self._v_layout.addLayout(h_layout)
        self.tabWidgets[tab_index].setLayout(h_layout)
    def _init_chart_tab_widgets(self,tab_index):
        h_layout = QHBoxLayout()
        self._charts.append(eval(available_chart_types[self._chart_type])())
        h_layout.addWidget(self._charts[tab_index-1])
        self._chart_info_labels.append(QLabel('Chart Information'))
        h_layout.addWidget(self._chart_info_labels[tab_index-1])
        h_layout.setSpacing(0)
        #self._add_footer_to_chart()
        self._charts[tab_index-1].update()
        #self._chart2.update()
        self.tabWidgets[tab_index].setLayout(h_layout)
    def _init_main_window(self):
        fp = open('./program_inputs.txt', encoding='utf-8', mode='r')
        window_title = fp.readline().split('=')[1]
        self._footer_title = fp.readline().split('=')[1]
        self._image_icon_path = fp.readline().split('=')[1]
        fp.close()
        self.setWindowIcon(QtGui.QIcon(_images_path+"lord_ganesha2.jpg"))
        self._language = list(available_languages.keys())[0]
        self._chart_type = 'south indian'
        ci = _index_containing_substring(available_chart_types.keys(),chart_type.lower())
        if ci >=0:
            self._chart_type = list(available_chart_types.keys())[ci]
        self.setFixedSize(_main_window_width,_main_window_height)        
    def _create_row1_ui(self):
        h_layout = QHBoxLayout()
        self._name_label = QLabel("Name:")
        h_layout.addWidget(self._name_label)
        self._name_text = QLineEdit("")
        self._name = self._name_text.text()
        self._name_text.setToolTip('Enter your name')
        h_layout.addWidget(self._name_text)
        self._gender_combo = QComboBox()
        self._gender_combo.addItems(['Male','Female'])
        h_layout.addWidget(self._gender_combo)
        self._place_label = QLabel("Place:")
        h_layout.addWidget(self._place_label)
        self._place_name = '' # 'Chennai, IN'
        self._place_text = QLineEdit(self._place_name)#"Chennai, IN")
        self._place_text.editingFinished.connect(lambda : self._get_place_latitude_longitude(self._place_text.text()))
        self._place_text.setToolTip('Enter place of birth, country name')
        h_layout.addWidget(self._place_text)
        self._lat_label = QLabel("Latidude:")
        h_layout.addWidget(self._lat_label)
        self._lat_text = QLineEdit('')
        self._latitude = 0.0
        self._lat_text.setToolTip('Enter Latitude preferably exact at place of birth: Format: +/- xx.xxx')
        h_layout.addWidget(self._lat_text)
        self._long_label = QLabel("Longitude:")
        h_layout.addWidget(self._long_label)
        self._long_text = QLineEdit('')#'xx.xxxx')#"80.2619")
        self._longitude = 0.0
        self._long_text.setToolTip('Enter Longitude preferably exact at place of birth. Format +/- xx.xxx')
        h_layout.addWidget(self._long_text)
        self._tz_label = QLabel("Time Zone:")
        h_layout.addWidget(self._tz_label)
        self._tz_text = QLineEdit('')#'x.x')#"+5.5")
        self._time_zone = 0.0
        self._tz_text.setToolTip('Enter Time offset from GMT e.g. -5.5 or 4.5')
        h_layout.addWidget(self._tz_text)
        self._v_layout.addLayout(h_layout)
    def _create_row2_ui(self):
        h_layout = QHBoxLayout()
        self._dob_label = QLabel("Date of Birth:")
        h_layout.addWidget(self._dob_label)
        self._date_of_birth = ''# '1996,12,7'
        self._dob_text = QLineEdit(self._date_of_birth)#'yyyy,mm,dd')#"1996,12,7")
        self._dob_text.setToolTip('Date of birth in the format YYYY,MM,DD\nFor BC enter negative years.\nAllowed Year Range: -13000 (BC) to 16800 (AD)')
        h_layout.addWidget(self._dob_text)
        self._tob_label = QLabel("Time of Birth:")
        h_layout.addWidget(self._tob_label)
        self._time_of_birth = '' # '10:34:00'
        self._tob_text = QLineEdit(self._time_of_birth)#'hh:mm:ss')#"10:34:00")
        self._tob_text.setToolTip('Enter time of birth in the format HH:MM:SS if afternoon use 12+ hours')
        h_layout.addWidget(self._tob_text)
        """ TODO: Changing chart type does not work with show chart click
        self._chart_type_combo = QComboBox()
        self._chart_type_combo.addItems(available_chart_types.keys())
        self._chart_type_combo.setToolTip('Choose birth chart style north, south or east indian')
        self._chart_type_combo.setCurrentText(self._chart_type)
        h_layout.addWidget(self._chart_type_combo)
        """
        available_ayanamsa_modes = list(panchanga.available_ayanamsa_modes.keys())#[:-1]
        self._ayanamsa_combo = QComboBox()
        self._ayanamsa_combo.addItems(available_ayanamsa_modes)
        self._ayanamsa_combo.setToolTip('Choose Ayanamsa mode from the list')
        self._ayanamsa_mode = "LAHIRI"
        self._ayanamsa_value = None
        self._ayanamsa_combo.setCurrentText(self._ayanamsa_mode)
        h_layout.addWidget(self._ayanamsa_combo)
        self._lang_combo = QComboBox()
        self._lang_combo.addItems(available_languages.keys())
        self._lang_combo.setCurrentText(self._language)
        self._lang_combo.setToolTip('Choose language for display')
        self._lang_combo.currentIndexChanged.connect(self._update_main_window_label_and_tooltips)
        h_layout.addWidget(self._lang_combo)
        self._compute_button = QPushButton("Show Chart")
        self._compute_button.setFont(QtGui.QFont("Arial Bold",9))
        self._compute_button.clicked.connect(self.compute_horoscope)
        self._compute_button.setToolTip('Click to update the chart information based on selections made')
        h_layout.addWidget(self._compute_button)
        self._save_image_button = QPushButton("Save as PDF")
        self._save_image_button.setFont(QtGui.QFont("Arial Bold",8))
        self._save_image_button.clicked.connect(self.save_as_pdf)
        self._save_image_button.setToolTip('Click to save horoscope as a PDF')
        h_layout.addWidget(self._save_image_button)
        self._v_layout.addLayout(h_layout)
    def _add_footer_to_chart(self):
        self._footer_label = QLabel('')
        self._footer_label.setTextFormat(Qt.TextFormat.RichText)
        self._footer_label.setText(self._footer_title)#"Copyright © Dr. Sundar Sundaresan, Open Astro Technologies, USA.")
        self._footer_label.setStyleSheet("border: 1px solid black;")
        self._footer_label.setFont(QtGui.QFont("Arial Bold",_footer_label_font_height))
        self._footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._footer_label.setFixedHeight(_footer_label_height)
        self._footer_label.setFixedWidth(self.width())
        self._footer_label.setWordWrap(True)
        self._v_layout.addWidget(self._footer_label)
    def _on_application_exit(self):
        def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)
        sys.excepthook = except_hook
        QApplication.quit()
    def ayanamsa_mode(self, ayanamsa_mode, ayanamsa=None):
        """
            Set Ayanamsa mode
            @param ayanamsa_mode - Default - Lahiri
            See 'panchanga.available_ayanamsa_modes' for the list of available models
        """
        self._ayanamsa_mode = ayanamsa_mode
        self._ayanamsa_value = ayanamsa
        self._ayanamsa_combo.setCurrentText(ayanamsa_mode)
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
    def gender(self,gender):
        """
            set gender of the person whose horoscope is sought
            @param gender: gender of the person
        """
        if gender.lower()=='male' or gender.lower()=='female':
            self._gender = gender
            self._gender_combo.setCurrentText(gender)
    def chart_type(self,chart_type):
        """
            Set chart type of the horoscope
            @param - chart_type:
                options: 'south indian'. 'north indian'
                Default: south indian
        """
        ci = _index_containing_substring(available_chart_types.keys(),chart_type.lower())
        if ci >=0:
            self._chart_type = list(available_chart_types.keys())[ci]
            """ TODO: changing chart type does not work with Tabs """
            #self._chart_type_combo.setCurrentText(chart_type.lower())
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
                         re.match(r"[\+|\-]?\d{1,4}\,\d{1,2}\,\d{1,2}", self._dob_text.text().strip(),re.IGNORECASE) and \
                         re.match(r"\d{1,2}:\d{1,2}:\d{1,2}", self._tob_text.text().strip(),re.IGNORECASE)
        return all_data_ok
    def _update_main_window_label_and_tooltips(self):
        try:
            if self.resources:
                msgs = self.resources
                self._name_label.setText(msgs['name_str'])
                self._name_label.setToolTip(msgs['name_tooltip_str'])
                self._place_label.setText(msgs['place_str'])
                self._place_label.setToolTip(msgs['place_tooltip_str'])
                self._lat_label.setText(msgs['latitude_str'])
                self._lat_label.setToolTip(msgs['latitude_tooltip_str'])
                self._long_label.setText(msgs['longitude_str'])
                self._long_label.setToolTip(msgs['longitude_tooltip_str'])
                self._tz_label.setText(msgs['timezone_offset_str'])
                self._tz_label.setToolTip(msgs['timezone_tooltip_str'])
                self._dob_label.setText(msgs['date_of_birth_str'])
                self._dob_label.setToolTip(msgs['dob_tooltip_str'])
                self._tob_label.setText(msgs['time_of_birth_str'])
                self._tob_label.setToolTip(msgs['tob_tooltip_str'])
                self._ayanamsa_combo.setToolTip(msgs['ayanamsa_tooltip_str'])
                self._lang_combo.setToolTip(msgs['language_tooltip_str'])
                self._compute_button.setText(msgs['show_chart_str'])
                self._compute_button.setToolTip(msgs['compute_tooltip_str'])
                self._save_image_button.setText(msgs['save_pdf_str'])
                self._save_image_button.setToolTip(msgs['savepdf_tooltip_str'])
                self.update()
        except:
            pass
    def compute_horoscope(self):
        """
            Compute the horoscope based on details entered
            if details missing - error is displayed            
        """
        if not self._validate_ui():
            print('values are not filled properly')
            return
        self._gender = self._gender_combo.currentText()
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
        as_string = True
        if self._place_name.strip() == '' and abs(self._latitude) > 0.0 and abs(self._longitude) > 0.0 and abs(self._time_zone) > 0.0: 
            [self._place_name,self._latitude,self._longitude,self._time_zone] = panchanga.get_latitude_longitude_from_place_name(place_name)
            self._lat_text.setText((self._latitude))
            self._long_text.setText((self._longitude))
            self._tz_text.setText((self._time_zone))
        year,month,day = self._date_of_birth.split(",")
        birth_date = panchanga.Date(int(year),int(month),int(day))
        """ TODO: changing chart type does not work with Tabs """
        #self._chart_type = self._chart_type_combo.currentText()
        """ TODO: With TabWidgets deleteLater and creating widget again is not working
        ' set the chart type and reset widgets'
        #self._chart1.deleteLater()
        #self._chart2.deleteLater()
        #print('update _init_chart_tab_widgets')
        #self._init_chart_tab_widgets()
        """
        if self._place_name.strip() != '' and abs(self._latitude) > 0.0 and abs(self._longitude) > 0.0 and abs(self._time_zone) > 0.0:
            self._horo= horoscope.Horoscope(latitude=self._latitude,longitude=self._longitude,timezone_offset=self._time_zone,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode,ayanamsa_value=self._ayanamsa_value)
        else:
            self._horo= horoscope.Horoscope(place_with_country_code=self._place_name,date_in=birth_date,birth_time=self._time_of_birth,ayanamsa_mode=self._ayanamsa_mode,ayanamsa_value=self._ayanamsa_value)
        self._calendar_info = self._horo.get_calendar_information(language=available_languages[self._language],as_string=True)
        self.resources= self._horo._get_calendar_resource_strings(language=available_languages[self._language])
        self._horoscope_info, self._horoscope_charts, self._dhasa_bhukti_info = [],[],[]
        if as_string:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = self._horo.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
        else:
            self._horoscope_info, self._horoscope_charts,self._dhasa_bhukti_info = self._horo.get_horoscope_information(language=available_languages[self._language],as_string=as_string)
        self._update_main_window_label_and_tooltips()
        self._update_chart_ui_with_info()
        self.resize(self.minimumSizeHint())
    def _fill_information_label1(self,info_str,format_str):
        key = 'sunrise_str'
        sunrise_time = self._calendar_info[self.resources[key]]
        info_str += format_str % (self.resources[key],sunrise_time)
        key = 'sunset_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = 'nakshatra_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = 'raasi_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = 'tithi_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = 'yogam_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = 'karanam_str'
        info_str += format_str % (self.resources[key],self._calendar_info[self.resources[key]])
        key = self.resources['raasi_str']+'-'+self.resources['ascendant_str']
        value = self._horoscope_info[key]#.split()[:1]
        info_str += format_str % (self.resources['ascendant_str'],value)
        birth_time = self._time_of_birth
        info_str += format_str % (self.resources['udhayathi_str'], _udhayadhi_nazhikai(birth_time,sunrise_time))
        key = self.resources['kali_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        key = self.resources['vikrama_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        key = self.resources['saka_year_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        self._info_label1.setText(info_str)
    def _fill_information_label2(self,info_str,format_str):
        info_str = ''
        dhasa = list(self._dhasa_bhukti_info.keys())[8].split('-')[0]
        deb = list(self._dhasa_bhukti_info.values())[8]
        dob = self._dob_text.text().replace(',','-')
        years,months,days = _dhasa_balance(dob, deb)
        value = str(years)+':'+ str(months)+':'+ str(days)
        key = dhasa + ' '+self.resources['balance_str']
        info_str += format_str % (key,value)
        dhasa = ''
        dhasa_end_date = ''
        di = 9
        for p,(k,v) in enumerate(self._dhasa_bhukti_info.items()):
            # get dhasa
            if (p+1) == di:
                dhasa = k.split("-")[0]#+ ' '+self.resources['ends_at_str']
            # Get dhasa end date
            elif (p+1) == di+1:
                """ to account for BC Dates negative sign is introduced"""
                if len(v.split('-')) == 4:
                    _,year,month,day = v.split('-')
                    year = '-'+year
                else:
                    year,month,day = v.split('-')
                dhasa_end_date = year+'-'+month+'-'+str(int(day)-1)+ ' '+self.resources['ends_at_str']
                info_str += format_str % (dhasa, dhasa_end_date)
                di += 9
        key = self.resources['maasa_str']
        value = self._calendar_info[key]
        info_str += format_str % (key,value)
        key = self.resources['ayanamsam_str']+' ('+self._ayanamsa_mode+') '
        value = panchanga.get_ayanamsa_value(self._horo.julian_day)
        self._ayanamsa_value = value
        value = panchanga.to_dms(value,as_string=True,is_lat_long='lat').replace('N','').replace('S','')
        print("horo_chart: Ayanamsa mode",key,'set to value',value)
        info_str += format_str % (key,value)
        self._info_label2.setText(info_str)
    def _update_tabs_with_divisional_charts(self,jd,place):
        for t,tab in enumerate(_tab_names[0:-2]):
            tab_name = self.resources[tab]
            self.tabWidget.setTabText(t,tab_name)
            """ update the chart from horoscope charts """
            if t>0 : #or t<len(_tab_names):
                i_start = (t-1)*10
                i_end = i_start + 10
                chart_info = ''
                for k,v in list(self._horoscope_info.items())[i_start:i_end]:
                    k1 = k.split('-')[-1]
                    v1 = v.split('-')[0]
                    chart_info +='%-15s%-20s\n' % (k1,v1)
                self._chart_info_labels[t-1].setText(chart_info)
                chart_data_1d = self._horoscope_charts[t-1]
                chart_data_1d = [x[:-1] for x in chart_data_1d]
                if self._chart_type.lower() == 'north indian':
                    _ascendant = panchanga.ascendant(jd,place,False)
                    asc_house = _ascendant[0]+1
                    chart_data_north = chart_data_1d[asc_house-1:]+chart_data_1d[0:asc_house-1]
                    self._charts[t-1].setData(chart_data_north)
                    self._charts[t-1].update()
                elif self._chart_type.lower() == 'east indian':
                    chart_data_2d = _convert_1d_house_data_to_2d(chart_data_1d,self._chart_type)
                    row,col = _get_row_col_string_match_from_2d_list(chart_data_2d,self.resources['ascendant_str'])
                    self._charts[t-1]._asc_house = row*self._charts[t-1].row_count+col
                    self._charts[t-1].setData(chart_data_2d,chart_title=tab_name)
                    self._charts[t-1].update()
                else: # south indian
                    chart_data_2d = _convert_1d_house_data_to_2d(chart_data_1d)
                    row,col = _get_row_col_string_match_from_2d_list(chart_data_2d,self.resources['ascendant_str'])
                    self._charts[t-1]._asc_house = row*self._charts[t-1].row_count+col
                    self._charts[t-1].set_south_indian_chart_data(chart_data_2d,chart_title=tab_name,image_icon_path=self._image_icon_path)
                    self._charts[t-1].update()                           
    def _update_tab_chart_information(self):
        jd = self._horo.julian_day  # For ascendant and planetary positions, dasa buthi - use birth time
        place = panchanga.Place(self._place_name,float(self._latitude),float(self._longitude),float(self._time_zone))
        self._update_tabs_with_divisional_charts(jd,place)
    def _update_dhasa_bhukthi_tab_information(self):
        format_str = '%-20s%-30s\n'
        tab_title = self.resources['dhasa_bhukthi_str']
        for db_tab in range(_dhasa_bhukthi_tab_count):
            p = db_tab*27
            row = 1
            for col in range(3):
                i_start = p
                i_end = i_start + 9
                db_list = list(self._dhasa_bhukti_info.items())[i_start:i_end]
                #print(i_start,i_end,db_list)
                db_str = db_list[0][0].split('-')[0]#+'\n'
                self.db_tables[db_tab][col].setItem(0,0,QTableWidgetItem(db_str))
                self.db_tables[db_tab][col].setItem(0,1,QTableWidgetItem(self.resources['ends_at_str']))
                t_row = 1
                for k,v in db_list:
                    k1 = k.split('-')[-1]
                    #db_str += format_str % (k1,v)
                    self.db_tables[db_tab][col].setItem(t_row,0,QTableWidgetItem(k1))
                    self.db_tables[db_tab][col].setItem(t_row,1,QTableWidgetItem(v))
                    t_row += 1
                p = i_end
                self.db_tables[db_tab][col].resizeColumnToContents(0)
                self.db_tables[db_tab][col].resizeColumnToContents(1)
            self.tabWidget.setTabText(_dhasa_bhukthi_tab_start+db_tab,tab_title+'-'+str(db_tab+1))
    def _update_compatibility_tab_information(self):
        bn=None
        bp=None
        gn=None
        gp=None
        if self._gender.lower() == 'male':
            bn = self._horo._nakshatra_number
            bp = self._horo._paadha_number
        else:
            gn = self._horo._nakshatra_number
            gp = self._horo._paadha_number
        comp = compatibility.Match(boy_nakshatra_number=bn,boy_paadham_number=bp,girl_nakshatra_number=gn,girl_paadham_number=gp)
        matching_stars_tuple = comp.get_matching_partners()
        if len(matching_stars_tuple)>4:
            matching_stars_tuple = matching_stars_tuple[:4]
        for t,m_s_tup in enumerate(matching_stars_tuple):
            row = int(t/2)
            tab_index = _compatibility_tab_start + row
            col = (t%2)
            self._update_compatibility_table(m_s_tup,tab_index,row, col)
            self.tabWidget.setTabText(tab_index,self.resources['compatibility_str']+'-'+str(row+1))
            
    def _update_compatibility_table(self,matching_stars_tuple,tab_index,row, col):
        ettu_poruthham_list = [self.resources['varna_str'], self.resources['vasiya_str'], self.resources['gana_str'], 
                               self.resources['tara_str'], self.resources['yoni_str'], self.resources['adhipathi_str'],\
                               self.resources['raasi_str1'], self.resources['naadi_str']]
        ettu_porutham_max_score = [compatibility.varna_max_score,compatibility.vasiya_max_score,compatibility.gana_max_score,\
                                    compatibility.nakshathra_max_score,compatibility.yoni_max_score,compatibility.raasi_adhipathi_max_score, \
                                    compatibility.raasi_max_score, compatibility.naadi_max_score]
        naalu_porutham_list = [self.resources['mahendra_str'],self.resources['vedha_str'],self.resources['rajju_str'],self.resources['sthree_dheerga_str']]
        ettu_porutham_results = matching_stars_tuple[3]
        compatibility_score = matching_stars_tuple[4]
        naalu_porutham_results = matching_stars_tuple[5]
        nakshatra = horoscope.NAKSHATRA_LIST[matching_stars_tuple[0]-1]
        paadham = self.resources['paadham_str']+str(matching_stars_tuple[1])+'-'+str(matching_stars_tuple[2])
        result = ''
        results_table = self.match_tables[row][col]
        results_table.setHorizontalHeaderItem(0,QTableWidgetItem(nakshatra+'-'+paadham))
        results_table.setHorizontalHeaderItem(1,QTableWidgetItem(''))
        results_table.setHorizontalHeaderItem(2,QTableWidgetItem(''))
        results_table.setHorizontalHeaderItem(3,QTableWidgetItem(''))
        row = 0
        for p,porutham in enumerate(ettu_poruthham_list):
            #result += format_str % (porutham,str(ettu_porutham_results[p][0]),str(ettu_porutham_results[p][1]))
            results_table.setItem(row,0,QTableWidgetItem(porutham))
            results_table.setItem(row,1,QTableWidgetItem(str(ettu_porutham_results[p])))
            results_table.setItem(row,2,QTableWidgetItem(str(ettu_porutham_max_score[p])))
            perc = '{:3.0f}%'.format(ettu_porutham_results[p]/ettu_porutham_max_score[p]*100)
            results_table.setItem(row,3,QTableWidgetItem(str(perc)))
            row += 1
        for p,porutham in enumerate(naalu_porutham_list):
            #result += format_str % (porutham,str(naalu_porutham_results[p]),'')
            results_table.setItem(row,0,QTableWidgetItem(porutham))
            results_table.setItem(row,1,QTableWidgetItem(str(naalu_porutham_results[p])))
            results_table.setItem(row,2,QTableWidgetItem('True'))
            if naalu_porutham_results[p]:
                results_table.setItem(row,3,QTableWidgetItem(str('\u2705')))
            else:
                results_table.setItem(row,3,QTableWidgetItem(str('\u274C')))
            row += 1
        #result += format_str % ('Overall Compatibility Score:', str(compatibility_score) +' out of '+ str(compatibility.max_compatibility_score),'')
        results_table.setItem(row,0,QTableWidgetItem(self.resources['overall_str']))
        results_table.setItem(row,1,QTableWidgetItem(str(compatibility_score)))
        results_table.setItem(row,2,QTableWidgetItem(str(compatibility.max_compatibility_score)))
        perc = '{:3.0f}%'.format(compatibility_score/compatibility.max_compatibility_score*100)
        results_table.setItem(row,3,QTableWidgetItem(str(perc)))
        for c in range(3):
            results_table.resizeColumnToContents(c)
        for r in range(13):
            results_table.resizeRowToContents(r)
    def _update_chart_ui_with_info(self):
        info_str = ''
        format_str = '%-20s%-40s\n'
        self._fill_information_label1(info_str, format_str)
        self._fill_information_label2(info_str, format_str)
        self._update_tab_chart_information()
        self._update_dhasa_bhukthi_tab_information()
        self._update_compatibility_tab_information()
        self.update()
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
        image_files = []
        if pdf_file:
            for t in range(self.tabCount):
                def _show_only_tab(t): #set onlt tab t to be visible
                    for ti in range(self.tabCount):
                        self.tabWidget.setTabVisible(ti,False)
                        if t==ti:
                            self.tabWidget.setTabVisible(ti,True)
                self.tabWidget.setCurrentIndex(t)
                _show_only_tab(t)
                image_file = _images_path+'pdf_grb_'+str(t)+'.png'
                image_files.append(image_file)
                im = self.grab()
                im.save(image_file) 
            for t in range(self.tabCount): # reset all tabs to visible
                self.tabWidget.setTabVisible(t,True)
            with open(pdf_file,"wb") as f:
                f.write(img2pdf.convert(image_files))
            f.close()
        for image_file in image_files:
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
def _convert_1d_list_to_2d_list(list_1d,map_1d_to_2d=None):
    if map_1d_to_2d==None:
        rasi_2d = [['X']*row_count for _ in range(col_count)]
        map_1d_to_2d=[ [1,2,3], [4,5,6], [7,8,9]]
        for index, row in enumerate(map_1d_to_2d):
            i,j = [(index, row.index(p)) for index, row in enumerate(map_1d_to_2d) if p in row][0]
            list_2d[i][j] = val
        return list_2d
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
        for index, row in enumerate(map_to_2d):
            if 'south' in chart_type.lower():
                i,j = [(index, row.index(p)) for index, row in enumerate(map_to_2d) if p in row][0]
                rasi_2d[i][j] = val
            elif 'east' in chart_type.lower():
                p_index = _index_containing_substring(row,str(p))
                if p_index != -1:
                    i,j = (index, p_index)
                    if rasi_2d[i][j] != 'X':
                        if index > 0:
                            rasi_2d[i][j] += separator + val
                        else:
                            rasi_2d[i][j] = val + separator + rasi_2d[i][j]
                    else:
                        rasi_2d[i][j] = val
    for i in range(row_count):
        for j in range(col_count):
            if rasi_2d[i][j] == 'X':
                rasi_2d[i][j] = ''
    return rasi_2d
def _get_row_col_string_match_from_2d_list(list_2d,match_string):
    result =(-1,-1)
    for row in range(len(list_2d)):
        for col in range(len(list_2d[0])):
            if match_string in list_2d[row][col]:
                return (row,col)
def _udhayadhi_nazhikai(birth_time,sunrise_time):
    """ TODO: this will not for work for BC dates due to datetime """
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
    chart_type = 'South'
    chart = ChartWindow(chart_type=chart_type)
    chart.language('Tamil')
    #"""
    chart.name('Bhuvana') #Rama
    chart.gender('Female')
    chart.place('Chennai,IN') #Ayodhya,IN
    chart.latitude('13.0389')
    chart.longitude('80.2619')
    chart.date_of_birth('1996,12,7')#'-5114,1,10')
    chart.time_of_birth('10:34:00')#'12:30:00')
    chart.time_zone('5.5')
    chart.chart_type(chart_type)
    #chart.ayanamsa_mode("SIDM_USER",0.0)
    #"""
    chart.compute_horoscope()
    chart.show()
    """
    for year in range(499,899,100):
        chart.date_of_birth(str(year)+',3,21')
        QApplication.processEvents()
        chart.compute_horoscope()
        time_sleep.sleep(2)
    """
    sys.exit(App.exec())
