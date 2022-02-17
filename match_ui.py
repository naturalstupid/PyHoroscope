import re
import sys
import os
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from _datetime import datetime, timedelta,time,date
import img2pdf

compatibility = __import__('compatibility')

available_languages = {"English":'en','Tamil':'ta','Telugu':'te'}
_main_window_width = 600
_main_window_height = 600 #630

class MatchWindow(QWidget):
    def __init__(self,chart_type='south indian'):
        super().__init__()
        self.setMinimumSize(_main_window_width,_main_window_height)
        fp = open('./program_inputs.txt', encoding='utf-8', mode='r')
        window_title = fp.readline().split('=')[1]
        header_title = fp.readline().split('=')[1]
        self._image_icon_path = fp.readline().split('=')[1]
        fp.close()
        self.setWindowIcon(QtGui.QIcon("./images/lord_ganesha2.jpg"))
        self._language = list(available_languages.keys())[0]
        #self.setFixedSize(650,630)
        self.setWindowTitle(window_title)
        v_layout = QVBoxLayout()
        """
        footer_label = QLabel(header_title)#"Copyright © Dr. Sundar Sundaresan, Open Astro Technologies, USA.")
        footer_label.setStyleSheet("border: 1px solid black;")
        footer_label.setFont(QtGui.QFont("Arial Bold",12))
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setFixedHeight(15)
        footer_label.setFixedWidth(self.width())
        v_layout.addWidget(footer_label)
        """
        h_layout = QHBoxLayout()
        self._boy_star_label = QLabel("Boy's Birth Star:")
        h_layout.addWidget(self._boy_star_label)
        self._boy_star_combo = QComboBox()
        self._boy_star_combo.addItems(compatibility.nakshatra_list)
        h_layout.addWidget(self._boy_star_combo)
        self._boy_paadham_label = QLabel("Boy's Star Paadham:")
        h_layout.addWidget(self._boy_paadham_label)
        self._boy_paadham_combo = QSpinBox()
        self._boy_paadham_combo.setRange(1,4)
        h_layout.addWidget(self._boy_paadham_combo)
        self._boy_show_all_matches_label = QLabel('Show All Matching Girl stars:')
        h_layout.addWidget(self._boy_show_all_matches_label)
        v_layout.addLayout(h_layout)
        self._boy_show_all_matches_check = QCheckBox()
        self._boy_show_all_matches_check.setChecked(False)
        h_layout.addWidget(self._boy_show_all_matches_check)
        self._boy_show_all_matches_combo = QSpinBox()
        self._boy_show_all_matches_combo.setRange(0.0,36.0)
        self._boy_show_all_matches_combo.setSingleStep(0.5)
        self._boy_show_all_matches_combo.setValue(18.0)
        h_layout.addWidget(self._boy_show_all_matches_combo)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self._girl_star_label = QLabel("Girl's Birth Star:")
        h_layout.addWidget(self._girl_star_label)
        self._girl_star_combo = QComboBox()
        self._girl_star_combo.addItems(compatibility.nakshatra_list)
        h_layout.addWidget(self._girl_star_combo)
        self._girl_paadham_label = QLabel("Girl's Star Paadham:")
        h_layout.addWidget(self._girl_paadham_label)
        self._girl_paadham_combo = QSpinBox()
        self._girl_paadham_combo.setRange(1,4)
        h_layout.addWidget(self._girl_paadham_combo)
        self._girl_show_all_matches_label = QLabel('Show All Matching Boy stars:')
        h_layout.addWidget(self._girl_show_all_matches_label)
        v_layout.addLayout(h_layout)
        self._girl_show_all_matches_check = QCheckBox()
        self._girl_show_all_matches_check.setChecked(False)
        h_layout.addWidget(self._girl_show_all_matches_check)
        self._girl_show_all_matches_combo = QSpinBox()
        self._girl_show_all_matches_combo.setRange(0.0,36.0)
        self._girl_show_all_matches_combo.setSingleStep(0.5)
        self._girl_show_all_matches_combo.setValue(18.0)
        h_layout.addWidget(self._girl_show_all_matches_combo)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self._mahendra_label = QLabel('Mahendra Porutham:')
        h_layout.addWidget(self._mahendra_label)
        self._mahendra_porutham_check = QCheckBox()
        self._mahendra_porutham_check.setChecked(True)
        h_layout.addWidget(self._mahendra_porutham_check)
        self._vedha_label = QLabel('Vedha Porutham:')
        h_layout.addWidget(self._vedha_label)
        self._vedha_porutham_check = QCheckBox()
        self._vedha_porutham_check.setChecked(True)
        h_layout.addWidget(self._vedha_porutham_check)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self._rajju_label = QLabel('Rajju Porutham:')
        h_layout.addWidget(self._rajju_label)
        self._rajju_porutham_check = QCheckBox()
        self._rajju_porutham_check.setChecked(True)
        h_layout.addWidget(self._rajju_porutham_check)
        self._shree_dheerga_label = QLabel('Shree Dheerga Porutham:')
        h_layout.addWidget(self._shree_dheerga_label)
        self._shree_dheerga_porutham_check = QCheckBox()
        self._shree_dheerga_porutham_check.setChecked(True)
        h_layout.addWidget(self._shree_dheerga_porutham_check)
        v_layout.addLayout(h_layout)
        self._compute_button = QPushButton('Show Match')
        v_layout.addWidget(self._compute_button)
        #self._results_label = QLabel('Results:')
        self._results_table = QTableWidget(13,3)
        self._results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._results_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        v_layout.addWidget(self._results_table)

        self._boy_show_all_matches_check.toggled.connect(self._check_only_boy_or_girl)
        self._girl_show_all_matches_check.toggled.connect(self._check_only_boy_or_girl)
        self._compute_button.clicked.connect(self._get_compatibility)
        self.setLayout(v_layout)
        self._v_layout = v_layout
    def _get_compatibility(self):
        boy_nakshatra_number = self._boy_star_combo.currentIndex()+1
        boy_paadham_number = self._boy_paadham_combo.value()+1
        girl_nakshatra_number = self._girl_star_combo.currentIndex()+1
        girl_paadham_number = self._girl_paadham_combo.value()+1
        a = compatibility.Ashtakoota(boy_nakshatra_number,boy_paadham_number,girl_nakshatra_number,girl_paadham_number)
        ettu_poruthham_list = ['varna porutham', 'vasiya porutham', 'gana porutham', 'nakshathra porutham', 'yoni porutham', 'adhipathi porutham', 'raasi porutham', 'naadi porutham']
        naalu_porutham_list = ['mahendra porutham','vedha porutham','rajju porutham','sthree dheerga porutham']
        ettu_porutham_results,compatibility_score,naalu_porutham_results = a.compatibility_score()
        result = ''
        self._results_table.setHorizontalHeaderItem(0,QTableWidgetItem('Porutham'))
        self._results_table.setHorizontalHeaderItem(1,QTableWidgetItem('Score'))
        self._results_table.setHorizontalHeaderItem(2,QTableWidgetItem('Maximum'))
        format_str = format_str = '%-40s%-20s%-20s\n'
        row = 0
        for p,porutham in enumerate(ettu_poruthham_list):
            #result += format_str % (porutham,str(ettu_porutham_results[p][0]),str(ettu_porutham_results[p][1]))
            self._results_table.setItem(row,0,QTableWidgetItem(porutham))
            self._results_table.setItem(row,1,QTableWidgetItem(str(ettu_porutham_results[p][0])))
            self._results_table.setItem(row,2,QTableWidgetItem(str(ettu_porutham_results[p][1])))
            row += 1
        for p,porutham in enumerate(naalu_porutham_list):
            #result += format_str % (porutham,str(naalu_porutham_results[p]),'')
            self._results_table.setItem(row,0,QTableWidgetItem(porutham))
            self._results_table.setItem(row,1,QTableWidgetItem(str(naalu_porutham_results[p])))
            self._results_table.setItem(row,2,QTableWidgetItem('True'))
            row += 1
        #result += format_str % ('Overall Compatibility Score:', str(compatibility_score) +' out of '+ str(compatibility.max_compatibility_score),'')
        self._results_table.setItem(row,0,QTableWidgetItem('Overall Compatibility Score:'))
        self._results_table.setItem(row,1,QTableWidgetItem(str(compatibility_score)))
        self._results_table.setItem(row,2,QTableWidgetItem(str(compatibility.max_compatibility_score)))
        self._results_table.resizeColumnToContents(0)
        self._results_table.resizeColumnToContents(1)
        self._results_table.resizeColumnToContents(2)
        #self._results_label.setText(result)
    def _check_only_boy_or_girl(self):
        if self._boy_show_all_matches_check.isChecked():
            ' disable all girl ui elements'
            self._girl_star_label.setEnabled(False)
            self._girl_star_combo.setEnabled(False)
            self._girl_paadham_label.setEnabled(False)
            self._girl_paadham_combo.setEnabled(False)
        else: #if not self._boy_show_all_matches_check.isChecked():
            ' enable all girl ui elements'
            self._girl_star_label.setEnabled(True)
            self._girl_star_combo.setEnabled(True)
            self._girl_paadham_label.setEnabled(True)
            self._girl_paadham_combo.setEnabled(True)
        if self._girl_show_all_matches_check.isChecked():
            ' disable all boy ui elements'
            self._boy_star_label.setEnabled(False)
            self._boy_star_combo.setEnabled(False)
            self._boy_paadham_label.setEnabled(False)
            self._boy_paadham_combo.setEnabled(False)
        else: #if not self._girl_show_all_matches_check.isChecked():
            ' enable all boy ui elements'
            self._boy_star_label.setEnabled(True)
            self._boy_star_combo.setEnabled(True)
            self._boy_paadham_label.setEnabled(True)
            self._boy_paadham_combo.setEnabled(True)
        if not self._boy_show_all_matches_check.isChecked() and not self._girl_show_all_matches_check.isChecked():
            ' enable porutham checks'
            self._mahendra_label.setEnabled(True)
            self._mahendra_porutham_check.setEnabled(True)
            self._vedha_label.setEnabled(True)
            self._vedha_porutham_check.setEnabled(True)
            self._rajju_label.setEnabled(True)
            self._rajju_porutham_check.setEnabled(True)
            self._shree_dheerga_label.setEnabled(True)
            self._shree_dheerga_porutham_check.setEnabled(True)
        else:
            ' disable porutham checks'
            self._mahendra_label.setEnabled(False)
            self._mahendra_porutham_check.setEnabled(False)
            self._vedha_label.setEnabled(False)
            self._vedha_porutham_check.setEnabled(False)
            self._rajju_label.setEnabled(False)
            self._rajju_porutham_check.setEnabled(False)
            self._shree_dheerga_label.setEnabled(False)
            self._shree_dheerga_porutham_check.setEnabled(False)
if __name__ == "__main__":
    def except_hook(cls, exception, traceback):
        print('exception called')
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook
    App = QApplication(sys.argv)
    chart = MatchWindow()
    chart.show()
    sys.exit(App.exec())