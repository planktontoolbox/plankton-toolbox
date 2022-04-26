#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# import os
import sys
import datetime
import math
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import plankton_core
import app_framework
import toolbox_utils

class PlanktonCounterSampleInfo(QtWidgets.QWidget):
    """ """
    def __init__(self, parentwidget, dataset, sample, current_sample_object):
        """ """   
        self._parentwidget = parentwidget
        self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        #
        super(PlanktonCounterSampleInfo, self).__init__()
        #
        self.setLayout(self._create_content_sample_info())
        #
        self.sample_locked = True
        self.set_read_only()
        #
        self.load_data()

    def load_data(self):
        """ """
        try:
            self.clear_sample_info()
            #
            sample_info_dict = self._current_sample_object.get_sample_info()
            #                                                       
            self._from_dict_to_fields(sample_info_dict)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def save_data(self):
        """ """
        if not self.sample_locked:
            try:
                # Get info from sample object if the count module have added config info.
                sample_info_dict = self._current_sample_object.get_sample_info()
                # 
                self._from_fields_to_dict(sample_info_dict)
                # 
                self._current_sample_object.set_sample_info(sample_info_dict)
                self._current_sample_object.save_sample_info()
            #
            except Exception as e:
                debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
                toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def clear_sample_info(self):
        """ """
        try:
            empty_dict = {}
            self._from_dict_to_fields(empty_dict)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _create_content_sample_info(self):
        """ """
        self._sample_name_edit = QtWidgets.QLineEdit()
        self._sample_name_edit.setEnabled(False)
        self._change_sample_name_button = QtWidgets.QPushButton(' Change name... ')
        self._change_sample_name_button.clicked.connect(self._change_sample_name)
        self._sample_id_edit = QtWidgets.QLineEdit()
#         self._sample_date = QtWidgets.QDateEdit()
#         self._sample_date.setCalendarPopup(True)
#         self._sample_date.setDisplayFormat('yyyy-MM-dd')
        self._sample_year_edit = QtWidgets.QLineEdit()
        self._sample_year_edit.setPlaceholderText('yyyy')
        self._sample_year_edit.setMaximumWidth(60)
        self._visit_month_edit = QtWidgets.QLineEdit()
        self._visit_month_edit.setPlaceholderText('mm')
        self._visit_month_edit.setMaximumWidth(40)
        self._sample_day_edit = QtWidgets.QLineEdit()
        self._sample_day_edit.setPlaceholderText('dd')
        self._sample_day_edit.setMaximumWidth(40)
        self._sample_time_edit = QtWidgets.QLineEdit()
        self._sample_time_edit.setPlaceholderText('hh:mm')
        self._sample_time_edit.setMaximumWidth(80)
        self._sampling_year_edit = QtWidgets.QLineEdit()
        self._sampling_year_edit.setMaximumWidth(60)
        self._sampling_country_edit = QtWidgets.QLineEdit()
        self._sampling_country_edit.setMaximumWidth(60)
        self._sampling_platform_edit = QtWidgets.QLineEdit()
        self._sampling_platform_edit.setMaximumWidth(60)
        self._sampling_series_edit = QtWidgets.QLineEdit()
        self._sampling_series_edit.setMaximumWidth(80)
        self._sampling_laboratory_edit = QtWidgets.QLineEdit()
        self._sampling_laboratory_edit.setMinimumWidth(200)
        self._orderer_edit = QtWidgets.QLineEdit()
        self._orderer_edit.setMinimumWidth(200)
        # self._project_edit = QtWidgets.QLineEdit()
        self._project_code_edit = QtWidgets.QLineEdit()
        self._project_name_edit = QtWidgets.QLineEdit()
        
        self._method_documentation_edit = QtWidgets.QLineEdit()
        self._method_reference_code_edit = QtWidgets.QLineEdit()
        
        self._station_name_edit = QtWidgets.QLineEdit()
        self._station_code_edit = QtWidgets.QLineEdit()
        self._latitude_degree = QtWidgets.QLineEdit()
        self._latitude_degree.setPlaceholderText('dd')
        self._latitude_degree.setMaximumWidth(40)
        self._latitude_degree.textEdited.connect(self._latlong_dm_edited)
        self._latitude_minute = QtWidgets.QLineEdit()
        self._latitude_minute.setPlaceholderText('mm.mm')
        self._latitude_minute.setMaximumWidth(80)
        self._latitude_minute.textEdited.connect(self._latlong_dm_edited)
        self._longitude_degree = QtWidgets.QLineEdit()
        self._longitude_degree.setPlaceholderText('dd')
        self._longitude_degree.setMaximumWidth(40)
        self._longitude_degree.textEdited.connect(self._latlong_dm_edited)
        self._longitude_minute = QtWidgets.QLineEdit()
        self._longitude_minute.setPlaceholderText('mm.mm')
        self._longitude_minute.setMaximumWidth(80)
        self._longitude_minute.textEdited.connect(self._latlong_dm_edited)

        self._latitude_dd = QtWidgets.QLineEdit()
        self._latitude_dd.setPlaceholderText('dd.dddd')
        self._latitude_dd.setMaximumWidth(100)
        self._latitude_dd.textEdited.connect(self._latlong_dd_edited)
        self._longitude_dd = QtWidgets.QLineEdit()
        self._longitude_dd.setPlaceholderText('dd.dddd')
        self._longitude_dd.setMaximumWidth(100)
        self._longitude_dd.textEdited.connect(self._latlong_dd_edited)

        self._sample_min_depth_m_edit = QtWidgets.QLineEdit()
        self._sample_min_depth_m_edit.setMaximumWidth(60)
        self._sample_max_depth_m_edit = QtWidgets.QLineEdit()
        self._sample_max_depth_m_edit.setMaximumWidth(60)
        self._water_depth_m_edit = QtWidgets.QLineEdit()
        self._water_depth_m_edit.setMaximumWidth(60)
#         self._sample_type_edit = QtWidgets.QLineEdit()
        self._sampler_type_code_list = QtWidgets.QComboBox()
        self._sampler_type_code_list.setEditable(True)
        self._sampler_type_code_list.setMaximumWidth(300)
        self._sampler_type_code_list.addItems(['<select or edit>', 
                                               'HOS (Hose)', 
                                               'IND (Integrated sample)', 
                                               'NET (Plankton net)', 
                                               'RU (Ruttner sampler)', 
                                               'FBW (Ferry box water sampler)', 
                                               'PDD (Pooled sample from distinct depths)', 
                                               'SEP (Separate depths)', 
                                               ])
        self._sampled_volume_l_edit = QtWidgets.QLineEdit()
        self._sampled_volume_l_edit.setMaximumWidth(60)

        self._net_type_code_list = QtWidgets.QComboBox()
        self._net_type_code_list.setEditable(True)
        self._net_type_code_list.setMaximumWidth(300)
        self._net_type_code_list.addItems(['<select or edit>', 
                                           'NET (Phytoplankton net)', 
                                           'WP2 (Integrated sample)', 
                                           'BONGO (Bongo net)', 
                                           ])
        self._sampler_area_m2_edit = QtWidgets.QLineEdit()
        self._sampler_area_m2_edit.setMaximumWidth(60)
        self._net_mesh_size_um_edit = QtWidgets.QLineEdit()
        self._net_mesh_size_um_edit.setMaximumWidth(60)
        self._wire_angle_deg_edit = QtWidgets.QLineEdit()
        self._wire_angle_deg_edit.setMaximumWidth(60)
        self._net_tow_length_m_edit = QtWidgets.QLineEdit()
        self._net_tow_length_m_edit.setMaximumWidth(60)
#         self._analysis_date = QtWidgets.QDateEdit()
#         self._analysis_date.setCalendarPopup(True)
#         self._analysis_date.setDisplayFormat('yyyy-MM-dd')
        self._analytical_laboratory_edit = QtWidgets.QLineEdit()
        self._analysis_year_edit = QtWidgets.QLineEdit()
        self._analysis_year_edit.setPlaceholderText('yyyy')
        self._analysis_year_edit.setMaximumWidth(60)
        self._analysis_month_edit = QtWidgets.QLineEdit()
        self._analysis_month_edit.setPlaceholderText('mm')
        self._analysis_month_edit.setMaximumWidth(40)
        self._analysis_day_edit = QtWidgets.QLineEdit()
        self._analysis_day_edit.setPlaceholderText('dd')
        self._analysis_day_edit.setMaximumWidth(40)
        self._analysis_today_button = QtWidgets.QPushButton('Today')
        self._analysis_today_button.clicked.connect(self.analysis_today)
        self._analysed_by_edit = QtWidgets.QLineEdit()
        self._sample_comment_edit = QtWidgets.QLineEdit()
        #
        self._clear_sample_info_button = QtWidgets.QPushButton('Clear')
        self._clear_sample_info_button.clicked.connect(self.clear_sample_info_selected)
        self._copyfromsample_button = QtWidgets.QPushButton('Copy from sample...')
        self._copyfromsample_button.clicked.connect(self._copy_sample_info_from)

        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        form1.addWidget(app_framework.LeftAlignedQLabel('<b>Sampling</b>'), gridrow, 0, 1, 1)
        form1.addWidget(app_framework.RightAlignedQLabel(''), gridrow, 1, 1, 10) # Move the rest to left
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sample name:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_name_edit, gridrow, 1, 1, 2)
        form1.addWidget(self._change_sample_name_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sample id:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_id_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sampling: Year:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._sample_year_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Month:'))
        hbox.addWidget(self._visit_month_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Day:'))
        hbox.addWidget(self._sample_day_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Sampling time (UTC):'))
        hbox.addWidget(self._sample_time_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('ICES metadata:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(app_framework.RightAlignedQLabel('Year:'))
        hbox.addWidget(self._sampling_year_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Country code:'))
        hbox.addWidget(self._sampling_country_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Platform code:'))
        hbox.addWidget(self._sampling_platform_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Series:'))
        hbox.addWidget(self._sampling_series_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
#         gridrow += 1
#         form1.addWidget(app_framework.RightAlignedQLabel(''), gridrow, 0, 1, 10) # Empty row.
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sampling laboratory:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._sampling_laboratory_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Orderer:'))
        hbox.addWidget(self._orderer_edit)
        # hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Project code:'), gridrow, 0, 1, 1)
        # form1.addWidget(self._project_edit, gridrow, 1, 1, 3)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._project_code_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Project name:'))
        hbox.addWidget(self._project_name_edit)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Method documentation:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._method_documentation_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Method ref.:'))
        hbox.addWidget(self._method_reference_code_edit)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Station name:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._station_name_edit, 10)
        hbox.addWidget(app_framework.RightAlignedQLabel('Station code:'))
        hbox.addWidget(self._station_code_edit, 3)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Latitude, degree:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._latitude_degree)
        hbox.addWidget(app_framework.RightAlignedQLabel('minute:'))
        hbox.addWidget(self._latitude_minute)
        hbox.addWidget(app_framework.RightAlignedQLabel('Longitude, degree:'))
        hbox.addWidget(self._longitude_degree)
        hbox.addWidget(app_framework.RightAlignedQLabel('minute:'))
        hbox.addWidget(self._longitude_minute)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Latitude, decimal:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._latitude_dd)
        hbox.addWidget(app_framework.RightAlignedQLabel('Longitude, decimal:'))
        hbox.addWidget(self._longitude_dd)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
#         gridrow += 1
#         form1.addWidget(app_framework.RightAlignedQLabel(''), gridrow, 0, 1, 10) # Empty row.
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sampler type code:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sampler_type_code_list, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sample min depth (m):'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._sample_min_depth_m_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Sample max depth (m):'))
        hbox.addWidget(self._sample_max_depth_m_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Water depth (m):'))
        hbox.addWidget(self._water_depth_m_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sampled volume (L):'), gridrow, 0, 1, 1)
        form1.addWidget(self._sampled_volume_l_edit, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.LeftAlignedQLabel('<b>Net sampling</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Net type code:'), gridrow, 0, 1, 1)
        form1.addWidget(self._net_type_code_list, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Sampler area (m2):'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._sampler_area_m2_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Mesh size (µm):'))
        hbox.addWidget(self._net_mesh_size_um_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Wire angle (deg):'))
        hbox.addWidget(self._wire_angle_deg_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Tow length (m):'))
        hbox.addWidget(self._net_tow_length_m_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.LeftAlignedQLabel('<b>Analysis</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Analytical laboratory:'), gridrow, 0, 1, 1)
        form1.addWidget(self._analytical_laboratory_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Analysis. Year:'), gridrow, 0, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._analysis_year_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Month:'))
        hbox.addWidget(self._analysis_month_edit)
        hbox.addWidget(app_framework.RightAlignedQLabel('Day:'))
        hbox.addWidget(self._analysis_day_edit)
        hbox.addWidget(self._analysis_today_button)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Analysed by:'), gridrow, 0, 1, 1)
        form1.addWidget(self._analysed_by_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(app_framework.RightAlignedQLabel('Comments:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_comment_edit, gridrow, 1, 1, 3)
#         # Empty row.
#         gridrow += 1
#         form1.addWidget(app_framework.RightAlignedQLabel(''), gridrow, 0, 1, 10)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._clear_sample_info_button)
        hbox1.addWidget(self._copyfromsample_button)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addStretch(100)
        layout.addLayout(hbox1)
        #
        return layout
    
    def set_read_only(self, read_only=True):
        """ """
        if (not self.sample_locked) and read_only:
            # Save sample before locking.
            self.save_data()
        #
        self.sample_locked = read_only
        #
        enabled = not read_only
        self._sample_name_edit.setReadOnly(read_only)
        self._change_sample_name_button.setEnabled(enabled)
        self._sample_id_edit.setReadOnly(read_only)
        self._sample_year_edit.setReadOnly(read_only)
        self._visit_month_edit.setReadOnly(read_only)
        self._sample_day_edit.setReadOnly(read_only)
        self._sample_time_edit.setReadOnly(read_only)
        self._sampling_year_edit.setReadOnly(read_only)
        self._sampling_country_edit.setReadOnly(read_only)
        self._sampling_platform_edit.setReadOnly(read_only)
        self._sampling_series_edit.setReadOnly(read_only)
        self._sampling_laboratory_edit.setReadOnly(read_only)
        self._orderer_edit.setReadOnly(read_only)
        # self._project_edit.setReadOnly(read_only)
        self._project_code_edit.setReadOnly(read_only)
        self._project_name_edit.setReadOnly(read_only)
        
        self._method_documentation_edit.setReadOnly(read_only)
        self._method_reference_code_edit.setReadOnly(read_only)
        
        self._station_name_edit.setReadOnly(read_only)
        self._station_code_edit.setReadOnly(read_only)
        self._latitude_degree.setReadOnly(read_only)
        self._latitude_minute.setReadOnly(read_only)
        self._longitude_degree.setReadOnly(read_only)
        self._longitude_minute.setReadOnly(read_only)
        self._latitude_dd.setReadOnly(read_only)
        self._longitude_dd.setReadOnly(read_only)
        self._sample_min_depth_m_edit.setReadOnly(read_only)
        self._sample_max_depth_m_edit.setReadOnly(read_only)
        self._water_depth_m_edit.setReadOnly(read_only)
        self._sampler_type_code_list.setEnabled(enabled)
        self._sampled_volume_l_edit.setReadOnly(read_only)
        self._net_type_code_list.setEnabled(enabled)
        self._sampler_area_m2_edit.setReadOnly(read_only)
        self._net_mesh_size_um_edit.setReadOnly(read_only)
        self._wire_angle_deg_edit.setReadOnly(read_only)
        self._net_tow_length_m_edit.setReadOnly(read_only)
        self._analytical_laboratory_edit.setReadOnly(read_only)
        self._analysis_year_edit.setReadOnly(read_only)
        self._analysis_month_edit.setReadOnly(read_only)
        self._analysis_day_edit.setReadOnly(read_only)
        self._analysis_today_button.setEnabled(enabled)
        self._analysed_by_edit.setReadOnly(read_only)
        self._sample_comment_edit.setReadOnly(read_only)
        self._clear_sample_info_button.setEnabled(enabled)
        self._copyfromsample_button.setEnabled(enabled)
    
    
    
    
    def analysis_today(self):
        """ """
        try:
            today = datetime.date.today()
            self._analysis_year_edit.setText(today.strftime('%Y'))
            self._analysis_month_edit.setText(today.strftime('%m'))
            self._analysis_day_edit.setText(today.strftime('%d'))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _latlong_dm_edited(self):
        """ """
        try:
            lat_deg = str(self._latitude_degree.text()).replace(',', '.')
            lat_min = str(self._latitude_minute.text()).replace(',', '.')
            long_deg = str(self._longitude_degree.text()).replace(',', '.')
            long_min = str(self._longitude_minute.text()).replace(',', '.')
            #
            try:
                latitude_dd = float(lat_deg.replace(',', '.').replace(' ', ''))
                if lat_min: 
                    latitude_dd += float(lat_min.replace(',', '.').replace(' ', '')) / 60
                latitude_dd = math.floor(latitude_dd*10000)/10000
                self._latitude_dd.setText(str(latitude_dd))
            except:
                self._latitude_dd.setText('')
            try:
                longitude_dd = float(long_deg.replace(',', '.').replace(' ', ''))
                if long_min:
                    longitude_dd += float(long_min.replace(',', '.').replace(' ', '')) / 60
                longitude_dd = math.floor(longitude_dd*10000)/10000
                self._longitude_dd.setText(str(longitude_dd))
            except:
                self._longitude_dd.setText('')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _latlong_dd_edited(self):
        """ """
        try:
            lat_dd = str(self._latitude_dd.text()).replace(',', '.')
            long_dd = str(self._longitude_dd.text()).replace(',', '.')
            #
            try:
                value = float(lat_dd.replace(',', '.').replace(' ', ''))
                value += 0.0000008 # Round (= 0.5 min).
                degrees = math.floor(abs(value))
                minutes = (abs(value) - degrees) * 60
                minutes = math.floor(minutes*100)/100
                self._latitude_degree.setText(str(int(degrees)))
                self._latitude_minute.setText(str(minutes))
            except:
                self._latitude_degree.setText('')
                self._latitude_minute.setText('')
            try:
                value = float(long_dd.replace(',', '.').replace(' ', ''))
                value += 0.0000008 # Round (= 0.5 min).
                degrees = math.floor(abs(value))
                minutes = (abs(value) - degrees) * 60
                minutes = math.floor(minutes*100)/100
                self._longitude_degree.setText(str(int(degrees)))
                self._longitude_minute.setText(str(minutes))
            except:
                self._longitude_degree.setText('')
                self._longitude_minute.setText('')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def clear_sample_info_selected(self):
        """ """
        try:
            box_result = QtWidgets.QMessageBox.warning(self, 'Warning', 
                                         'Do you want to clear all sample information?', 
                                         QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)
            if box_result == QtWidgets.QMessageBox.Ok:
                self.clear_sample_info()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _copy_sample_info_from(self):
        """ """
        try:
            dialog = CopyFromTemplateDialog(self)
            if dialog.exec():
                dataset = dialog.get_dataset()
                sample = dialog.get_sample()
                if dataset and sample:
                    dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
                    sample_object = plankton_core.PlanktonCounterSample(dir_path,
                                                                   dataset, 
                                                                   sample)
                    metadata_dict = sample_object.get_sample_info()
                    self._from_dict_to_fields(metadata_dict)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _change_sample_name(self):
        """ """
        try:
            self.save_data()
            dialog = RenameSampleDialog(self, self._current_sample)
            if dialog.exec():
                new_sample_name = dialog.get_new_sample_name()
                if new_sample_name:
                    self.save_data()
                    plankton_core.PlanktonCounterManager().rename_sample(self._current_dataset, 
                                                                         self._current_sample,
                                                                         new_sample_name)
                    # Close dialog.
                    self._parentwidget.reject()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _from_fields_to_dict(self, metadata_dict):
        """ """
        try:
            metadata_dict['plankton_toolbox_version'] = app_framework.get_version() # __version__
            metadata_dict['sample_name'] = str(self._current_sample)
            metadata_dict['sample_id'] = str(self._sample_id_edit.text())
            year = str(self._sample_year_edit.text())
            month = str(self._visit_month_edit.text())
            day = str(self._sample_day_edit.text())
            date_tmp = year + '-' + month + '-' + day 
            metadata_dict['sample_date'] = date_tmp
            metadata_dict['sample_time'] = str(self._sample_time_edit.text())
            metadata_dict['visit_year'] = str(self._sampling_year_edit.text())
            metadata_dict['country_code'] = str(self._sampling_country_edit.text())
            metadata_dict['platform_code'] = str(self._sampling_platform_edit.text())
            metadata_dict['sampling_series'] = str(self._sampling_series_edit.text())
            metadata_dict['sampling_laboratory'] = str(self._sampling_laboratory_edit.text())
            metadata_dict['orderer'] = str(self._orderer_edit.text())
            # metadata_dict['project_code'] = str(self._project_edit.text())
            metadata_dict['project_code'] = str(self._project_code_edit.text())
            metadata_dict['project_name'] = str(self._project_name_edit.text())
            
            metadata_dict['method_documentation'] = str(self._method_documentation_edit.text())
            metadata_dict['method_reference_code'] = str(self._method_reference_code_edit.text())
            
            metadata_dict['station_name'] = str(self._station_name_edit.text())
            metadata_dict['station_code'] = str(self._station_code_edit.text())
            lat_deg_tmp = str(self._latitude_degree.text()).replace(',', '.')
            lat_min_tmp = str(self._latitude_minute.text()).replace(',', '.')
            long_deg_tmp = str(self._longitude_degree.text()).replace(',', '.')
            long_min_tmp = str(self._longitude_minute.text()).replace(',', '.')
            lat_dd_tmp = str(self._latitude_dd.text()).replace(',', '.')
            long_dd_tmp = str(self._longitude_dd.text()).replace(',', '.')
            metadata_dict['sample_latitude_dm'] = lat_deg_tmp + ' ' + lat_min_tmp
            metadata_dict['sample_longitude_dm'] = long_deg_tmp + ' ' + long_min_tmp
            metadata_dict['sample_latitude_dd'] = lat_dd_tmp
            metadata_dict['sample_longitude_dd'] = long_dd_tmp
            metadata_dict['sample_min_depth_m'] = str(self._sample_min_depth_m_edit.text())
            metadata_dict['sample_max_depth_m'] = str(self._sample_max_depth_m_edit.text())
            metadata_dict['water_depth_m'] = str(self._water_depth_m_edit.text())
            metadata_dict['sampler_type_code'] = str(self._sampler_type_code_list.currentText())
            metadata_dict['sampled_volume_l'] = str(self._sampled_volume_l_edit.text())
            metadata_dict['net_type_code'] = str(self._net_type_code_list.currentText())        
            metadata_dict['sampler_area_m2'] = str(self._sampler_area_m2_edit.text())
            metadata_dict['net_mesh_size_um'] = str(self._net_mesh_size_um_edit.text())
            metadata_dict['wire_angle_deg'] = str(self._wire_angle_deg_edit.text())
            metadata_dict['net_tow_length_m'] = str(self._net_tow_length_m_edit.text())
            metadata_dict['analytical_laboratory'] = str(self._analytical_laboratory_edit.text())
            year = str(self._analysis_year_edit.text())
            month = str(self._analysis_month_edit.text())
            day = str(self._analysis_day_edit.text())
            date_tmp = year + '-' + month + '-' + day 
            metadata_dict['analysis_date'] = date_tmp
            metadata_dict['analysed_by'] = str(self._analysed_by_edit.text())
            metadata_dict['sample_comment'] = str(self._sample_comment_edit.text())
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _from_dict_to_fields(self, metadata_dict):
        """ """
        try:
            self._sample_name_edit.setText(self._current_sample)
            self._sample_id_edit.setText(metadata_dict.get('sample_id', ''))
    #         self._sample_date.setDate(QtCore.QDate.fromString(date_tmp, 'yyyy-MM-dd'))
            date_tmp = metadata_dict.get('sample_date', '')
            if len(date_tmp) >= 10:
                self._sample_year_edit.setText(date_tmp[0:4])
                self._visit_month_edit.setText(date_tmp[5:7])
                self._sample_day_edit.setText(date_tmp[8:10])
            else:
                self._sample_year_edit.setText('')
                self._visit_month_edit.setText('')
                self._sample_day_edit.setText('')
            self._sample_time_edit.setText(metadata_dict.get('sample_time', ''))
            self._sampling_year_edit.setText(metadata_dict.get('visit_year', ''))
            self._sampling_country_edit.setText(metadata_dict.get('country_code', ''))
            self._sampling_platform_edit.setText(metadata_dict.get('platform_code', ''))
            self._sampling_series_edit.setText(metadata_dict.get('sampling_series', ''))
            self._sampling_laboratory_edit.setText(metadata_dict.get('sampling_laboratory', ''))
            self._orderer_edit.setText(metadata_dict.get('orderer', ''))
            # self._project_edit.setText(metadata_dict.get('project_code', ''))
            self._project_code_edit.setText(metadata_dict.get('project_code', ''))
            self._project_name_edit.setText(metadata_dict.get('project_name', ''))
            
            self._method_documentation_edit.setText(metadata_dict.get('method_documentation', ''))
            self._method_reference_code_edit.setText(metadata_dict.get('method_reference_code', ''))
            
            self._station_name_edit.setText(metadata_dict.get('station_name', ''))
            self._station_code_edit.setText(metadata_dict.get('station_code', ''))
            lat_tmp = str(metadata_dict.get('sample_latitude_dm', ''))
            long_tmp = str(metadata_dict.get('sample_longitude_dm', ''))
            if (len(lat_tmp) > 2) and (' ' in lat_tmp):
                lat_deg_min = lat_tmp.split(' ') 
                self._latitude_degree.setText(lat_deg_min[0])
                self._latitude_minute.setText(lat_deg_min[1])
            else:
                self._latitude_degree.setText('')
                self._latitude_minute.setText('')
            if (len(long_tmp) > 2) and (' ' in long_tmp):
                long_deg_min = long_tmp.split(' ') 
                self._longitude_degree.setText(long_deg_min[0])
                self._longitude_minute.setText(long_deg_min[1])
            else:
                self._longitude_degree.setText('')
                self._longitude_minute.setText('')
            #
            self._latitude_dd.setText(str(metadata_dict.get('sample_latitude_dd', '')))
            self._longitude_dd.setText(str(metadata_dict.get('sample_longitude_dd', '')))
            #       
            self._sample_min_depth_m_edit.setText(metadata_dict.get('sample_min_depth_m', ''))
            self._sample_max_depth_m_edit.setText(metadata_dict.get('sample_max_depth_m', ''))
            self._water_depth_m_edit.setText(metadata_dict.get('water_depth_m', ''))
            sampler_type_code = metadata_dict.get('sampler_type_code', '')
            currentindex = self._sampler_type_code_list.findText(sampler_type_code, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._sampler_type_code_list.setCurrentIndex(currentindex)
            else:
                self._sampler_type_code_list.setItemText(0, sampler_type_code)
            self._sampled_volume_l_edit.setText(metadata_dict.get('sampled_volume_l', ''))
    
            net_type_code = metadata_dict.get('net_type_code', '')
            currentindex = self._net_type_code_list.findText(net_type_code, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._net_type_code_list.setCurrentIndex(currentindex)
            else:
                self._net_type_code_list.setItemText(0, sampler_type_code)
            
            self._sampler_area_m2_edit.setText(metadata_dict.get('sampler_area_m2', ''))
            self._net_mesh_size_um_edit.setText(metadata_dict.get('net_mesh_size_um', ''))
            self._wire_angle_deg_edit.setText(metadata_dict.get('wire_angle_deg', ''))
            self._net_tow_length_m_edit.setText(metadata_dict.get('net_tow_length_m', ''))
            self._analytical_laboratory_edit.setText(metadata_dict.get('analytical_laboratory', ''))
            date_tmp = metadata_dict.get('analysis_date', '')
    #         self._analysis_date.setDate(QtCore.QDate.fromString(date_tmp, 'yyyy-MM-dd'))
            date_tmp = metadata_dict.get('analysis_date', '')
            if len(date_tmp) >= 10:
                self._analysis_year_edit.setText(date_tmp[0:4])
                self._analysis_month_edit.setText(date_tmp[5:7])
                self._analysis_day_edit.setText(date_tmp[8:10])
            else:
                self.analysis_today()
    #             self._analysis_year_edit.setText('')
    #             self._analysis_month_edit.setText('')
    #             self._analysis_day_edit.setText('')
            self._analysed_by_edit.setText(metadata_dict.get('analysed_by', ''))
            self._sample_comment_edit.setText(metadata_dict.get('sample_comment', ''))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

class CopyFromTemplateDialog(QtWidgets.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    
    def __init__(self, parentwidget):
        """ """
        self._parentwidget = parentwidget
        super(CopyFromTemplateDialog, self).__init__(parentwidget)
        self.setWindowTitle("Copy sample info")
        #
        self.setLayout(self._content())
        self._dataset = ''
        self._sample = ''
        self._datasetsample_dict = {}
        self._load_dataset_and_samples()

    def get_dataset(self):
        """ """
        try:
            return self._dataset
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def get_sample(self):
        """ """
        try:
            return self._sample
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
       
    def _content(self):
        """ """
        self._datasetsample_list = QtWidgets.QComboBox(self)
        self._datasetsample_list.addItems(['<select>'])
        copysampleinfo_button = QtWidgets.QPushButton('Copy sample info')
        copysampleinfo_button.clicked.connect(self._copy_sample_info)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('Dataset and sample:', self._datasetsample_list)
        
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(copysampleinfo_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout 
    
    def _load_dataset_and_samples(self):
        """ """
        try:
            datasets = plankton_core.PlanktonCounterManager().get_dataset_names()
            for dataset in datasets:
                samples = plankton_core.PlanktonCounterManager().get_sample_names(dataset)
                for sample in samples:
                    datasetsample = dataset + ': ' + sample
                    self._datasetsample_dict[datasetsample] = (dataset, sample)
            #
            self._datasetsample_list.addItems(sorted(self._datasetsample_dict.keys()))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
        
    def _copy_sample_info(self):
        """ """
        try:
            selectedtext = str(self._datasetsample_list.currentText())
            if selectedtext in self._datasetsample_dict:
                datasetsample = self._datasetsample_dict[selectedtext]
                self._dataset = datasetsample[0]
                self._sample = datasetsample[1]
            else:
                self._dataset = ''
                self._sample = ''            
            #
            self.accept() # Close dialog box.
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        

class RenameSampleDialog(QtWidgets.QDialog):
    """ """
    def __init__(self, parentwidget, old_sample_name):
        """ """
        self._old_sample_name = old_sample_name
        self._new_sample_name = ''
        super(RenameSampleDialog, self).__init__(parentwidget)
        self.setWindowTitle("Rename sample")
        self.setLayout(self._content())

    def get_new_sample_name(self):
        """ """
        return self._new_sample_name

    def _content(self):
        """ """
        self._newsamplename_edit = QtWidgets.QLineEdit(self._old_sample_name)
        self._newsamplename_edit.setMinimumWidth(400)
        createsample_button = QtWidgets.QPushButton(' Rename sample ')
        createsample_button.clicked.connect(self._rename_sample)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('New sample name:', self._newsamplename_edit)
        
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createsample_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _rename_sample(self):
        """ """
        try:
            self._new_sample_name = str(self._newsamplename_edit.text())
            #            
            self.accept() # Close dialog box.
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

