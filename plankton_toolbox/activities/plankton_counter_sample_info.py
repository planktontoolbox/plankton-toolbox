#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

# import os
import datetime
import math
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_core

class PlanktonCounterSampleInfo(QtGui.QWidget):
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
        self.load_data()

    def load_data(self):
        """ """
        self.clear_sample_info()
        #
        sample_info_dict = self._current_sample_object.get_sample_info()
        #                                                       
        self._from_dict_to_fields(sample_info_dict)
        
    def save_data(self):
        """ """
        # Get info from sample object if the count module have added config info.
        sample_info_dict = self._current_sample_object.get_sample_info()
        # 
        self._from_fields_to_dict(sample_info_dict)
        # 
        self._current_sample_object.set_sample_info(sample_info_dict)
        self._current_sample_object.save_sample_info()

    def clear_sample_info(self):
        """ """
        empty_dict = {}
        self._from_dict_to_fields(empty_dict)

    def _create_content_sample_info(self):
        """ """
        self._sample_name_edit = QtGui.QLineEdit()
        self._sample_name_edit.setEnabled(False)
        self._change_sample_name_button = QtGui.QPushButton(' Change name... ')
        self._change_sample_name_button.clicked.connect(self._change_sample_name)
        self._sample_id_edit = QtGui.QLineEdit()
#         self._sample_date = QtGui.QDateEdit()
#         self._sample_date.setCalendarPopup(True)
#         self._sample_date.setDisplayFormat('yyyy-MM-dd')
        self._sample_year_edit = QtGui.QLineEdit()
        self._sample_year_edit.setPlaceholderText('yyyy')
        self._sample_year_edit.setMaximumWidth(60)
        self._visit_month_edit = QtGui.QLineEdit()
        self._visit_month_edit.setPlaceholderText('mm')
        self._visit_month_edit.setMaximumWidth(40)
        self._sample_day_edit = QtGui.QLineEdit()
        self._sample_day_edit.setPlaceholderText('dd')
        self._sample_day_edit.setMaximumWidth(40)
        self._sample_time_edit = QtGui.QLineEdit()
        self._sample_time_edit.setPlaceholderText('hh:mm')
        self._sample_time_edit.setMaximumWidth(80)
        self._sampling_year_edit = QtGui.QLineEdit()
        self._sampling_year_edit.setMaximumWidth(60)
        self._sampling_country_edit = QtGui.QLineEdit()
        self._sampling_country_edit.setMaximumWidth(60)
        self._sampling_platform_edit = QtGui.QLineEdit()
        self._sampling_platform_edit.setMaximumWidth(60)
        self._sampling_series_edit = QtGui.QLineEdit()
        self._sampling_series_edit.setMaximumWidth(80)
        self._sampling_laboratory_edit = QtGui.QLineEdit()
        self._sampling_laboratory_edit.setMinimumWidth(200)
        self._orderer_edit = QtGui.QLineEdit()
        self._orderer_edit.setMinimumWidth(200)
        self._project_edit = QtGui.QLineEdit()
        self._station_name_edit = QtGui.QLineEdit()
        self._latitude_degree = QtGui.QLineEdit()
        self._latitude_degree.setPlaceholderText('dd')
        self._latitude_degree.setMaximumWidth(40)
        self._latitude_degree.textEdited.connect(self._latlong_dm_edited)
        self._latitude_minute = QtGui.QLineEdit()
        self._latitude_minute.setPlaceholderText('mm.mm')
        self._latitude_minute.setMaximumWidth(80)
        self._latitude_minute.textEdited.connect(self._latlong_dm_edited)
        self._longitude_degree = QtGui.QLineEdit()
        self._longitude_degree.setPlaceholderText('dd')
        self._longitude_degree.setMaximumWidth(40)
        self._longitude_degree.textEdited.connect(self._latlong_dm_edited)
        self._longitude_minute = QtGui.QLineEdit()
        self._longitude_minute.setPlaceholderText('mm.mm')
        self._longitude_minute.setMaximumWidth(80)
        self._longitude_minute.textEdited.connect(self._latlong_dm_edited)

        self._latitude_dd = QtGui.QLineEdit()
        self._latitude_dd.setPlaceholderText('dd.dddd')
        self._latitude_dd.setMaximumWidth(100)
        self._latitude_dd.textEdited.connect(self._latlong_dd_edited)
        self._longitude_dd = QtGui.QLineEdit()
        self._longitude_dd.setPlaceholderText('dd.dddd')
        self._longitude_dd.setMaximumWidth(100)
        self._longitude_dd.textEdited.connect(self._latlong_dd_edited)

        self._sample_min_depth_m_edit = QtGui.QLineEdit()
        self._sample_min_depth_m_edit.setMaximumWidth(60)
        self._sample_max_depth_m_edit = QtGui.QLineEdit()
        self._sample_max_depth_m_edit.setMaximumWidth(60)
        self._water_depth_m_edit = QtGui.QLineEdit()
        self._water_depth_m_edit.setMaximumWidth(60)
#         self._sample_type_edit = QtGui.QLineEdit()
        self._sampler_type_code_list = QtGui.QComboBox()
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
        self._sampled_volume_l_edit = QtGui.QLineEdit()
        self._sampled_volume_l_edit.setMaximumWidth(60)

        self._net_type_code_list = QtGui.QComboBox()
        self._net_type_code_list.setEditable(True)
        self._net_type_code_list.setMaximumWidth(300)
        self._net_type_code_list.addItems(['<select or edit>', 
                                           'NET (Phytoplankton net)', 
                                           'WP2 (Integrated sample)', 
                                           'BONGO (Bongo net)', 
                                           ])
        self._sampler_area_m2_edit = QtGui.QLineEdit()
        self._sampler_area_m2_edit.setMaximumWidth(60)
        self._net_mesh_size_um_edit = QtGui.QLineEdit()
        self._net_mesh_size_um_edit.setMaximumWidth(60)
        self._wire_angle_deg_edit = QtGui.QLineEdit()
        self._wire_angle_deg_edit.setMaximumWidth(60)
        self._net_tow_length_m_edit = QtGui.QLineEdit()
        self._net_tow_length_m_edit.setMaximumWidth(60)
#         self._analysis_date = QtGui.QDateEdit()
#         self._analysis_date.setCalendarPopup(True)
#         self._analysis_date.setDisplayFormat('yyyy-MM-dd')
        self._analytical_laboratory_edit = QtGui.QLineEdit()
        self._analysis_year_edit = QtGui.QLineEdit()
        self._analysis_year_edit.setPlaceholderText('yyyy')
        self._analysis_year_edit.setMaximumWidth(60)
        self._analysis_month_edit = QtGui.QLineEdit()
        self._analysis_month_edit.setPlaceholderText('mm')
        self._analysis_month_edit.setMaximumWidth(40)
        self._analysis_day_edit = QtGui.QLineEdit()
        self._analysis_day_edit.setPlaceholderText('dd')
        self._analysis_day_edit.setMaximumWidth(40)
        self._analysis_today_button = QtGui.QPushButton('Today')
        self._analysis_today_button.clicked.connect(self.analysis_today)
        self._analysed_by_edit = QtGui.QLineEdit()
        self._sample_comment_edit = QtGui.QLineEdit()
        #
        self._clear_sample_info_button = QtGui.QPushButton('Clear')
        self._clear_sample_info_button.clicked.connect(self.clear_sample_info_selected)
        self._copyfromsample_button = QtGui.QPushButton('Copy from sample...')
        self._copyfromsample_button.clicked.connect(self._copy_sample_info_from)

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        form1.addWidget(utils_qt.LeftAlignedQLabel('<b>Sampling</b>'), gridrow, 0, 1, 1)
        form1.addWidget(utils_qt.RightAlignedQLabel(''), gridrow, 1, 1, 10) # Move the rest to left
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sample name:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_name_edit, gridrow, 1, 1, 2)
        form1.addWidget(self._change_sample_name_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sample id:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_id_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sampling: Year:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._sample_year_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Month:'))
        hbox.addWidget(self._visit_month_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Day:'))
        hbox.addWidget(self._sample_day_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Sampling time (UTC):'))
        hbox.addWidget(self._sample_time_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('ICES metadata:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(utils_qt.RightAlignedQLabel('Year:'))
        hbox.addWidget(self._sampling_year_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Country code:'))
        hbox.addWidget(self._sampling_country_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Platform code:'))
        hbox.addWidget(self._sampling_platform_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Series:'))
        hbox.addWidget(self._sampling_series_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
#         gridrow += 1
#         form1.addWidget(utils_qt.RightAlignedQLabel(''), gridrow, 0, 1, 10) # Empty row.
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sampling laboratory:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._sampling_laboratory_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Orderer:'))
        hbox.addWidget(self._orderer_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Project:'), gridrow, 0, 1, 1)
        form1.addWidget(self._project_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Station name:'), gridrow, 0, 1, 1)
        form1.addWidget(self._station_name_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Latitude, degree:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._latitude_degree)
        hbox.addWidget(utils_qt.RightAlignedQLabel('minute:'))
        hbox.addWidget(self._latitude_minute)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Longitude, degree:'))
        hbox.addWidget(self._longitude_degree)
        hbox.addWidget(utils_qt.RightAlignedQLabel('minute:'))
        hbox.addWidget(self._longitude_minute)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Latitude, decimal:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._latitude_dd)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Longitude, decimal:'))
        hbox.addWidget(self._longitude_dd)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
#         gridrow += 1
#         form1.addWidget(utils_qt.RightAlignedQLabel(''), gridrow, 0, 1, 10) # Empty row.
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sampler type code:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sampler_type_code_list, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sample min depth (m):'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._sample_min_depth_m_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Sample max depth (m):'))
        hbox.addWidget(self._sample_max_depth_m_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Water depth (m):'))
        hbox.addWidget(self._water_depth_m_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sampled volume (L):'), gridrow, 0, 1, 1)
        form1.addWidget(self._sampled_volume_l_edit, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.LeftAlignedQLabel('<b>Net sampling</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Net type code:'), gridrow, 0, 1, 1)
        form1.addWidget(self._net_type_code_list, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Sampler area (m2):'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._sampler_area_m2_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Mesh size (µm):'))
        hbox.addWidget(self._net_mesh_size_um_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Wire angle (deg):'))
        hbox.addWidget(self._wire_angle_deg_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Tow length (m):'))
        hbox.addWidget(self._net_tow_length_m_edit)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.LeftAlignedQLabel('<b>Analysis</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Analytical laboratory:'), gridrow, 0, 1, 1)
        form1.addWidget(self._analytical_laboratory_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Analysis. Year:'), gridrow, 0, 1, 1)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._analysis_year_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Month:'))
        hbox.addWidget(self._analysis_month_edit)
        hbox.addWidget(utils_qt.RightAlignedQLabel('Day:'))
        hbox.addWidget(self._analysis_day_edit)
        hbox.addWidget(self._analysis_today_button)
        hbox.addStretch(10)
        form1.addLayout(hbox, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Analysed by:'), gridrow, 0, 1, 1)
        form1.addWidget(self._analysed_by_edit, gridrow, 1, 1, 3)
        gridrow += 1
        form1.addWidget(utils_qt.RightAlignedQLabel('Comments:'), gridrow, 0, 1, 1)
        form1.addWidget(self._sample_comment_edit, gridrow, 1, 1, 3)
#         # Empty row.
#         gridrow += 1
#         form1.addWidget(utils_qt.RightAlignedQLabel(''), gridrow, 0, 1, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._clear_sample_info_button)
        hbox1.addWidget(self._copyfromsample_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addStretch(100)
        layout.addLayout(hbox1)
        #
        return layout
    
    def analysis_today(self):
        """ """
        today = datetime.date.today()
        self._analysis_year_edit.setText(today.strftime('%Y'))
        self._analysis_month_edit.setText(today.strftime('%m'))
        self._analysis_day_edit.setText(today.strftime('%d'))

    def _latlong_dm_edited(self):
        """ """
        lat_deg = unicode(self._latitude_degree.text()).replace(',', '.')
        lat_min = unicode(self._latitude_minute.text()).replace(',', '.')
        long_deg = unicode(self._longitude_degree.text()).replace(',', '.')
        long_min = unicode(self._longitude_minute.text()).replace(',', '.')
        #
        try:
            latitude_dd = float(lat_deg.replace(',', '.').replace(' ', ''))
            if lat_min: 
                latitude_dd += float(lat_min.replace(',', '.').replace(' ', '')) / 60
            latitude_dd = math.floor(latitude_dd*10000)/10000
            self._latitude_dd.setText(unicode(latitude_dd))
        except:
            self._latitude_dd.setText('')
        try:
            longitude_dd = float(long_deg.replace(',', '.').replace(' ', ''))
            if long_min:
                longitude_dd += float(long_min.replace(',', '.').replace(' ', '')) / 60
            longitude_dd = math.floor(longitude_dd*10000)/10000
            self._longitude_dd.setText(unicode(longitude_dd))
        except:
            self._longitude_dd.setText('')
        
    def _latlong_dd_edited(self):
        """ """
        lat_dd = unicode(self._latitude_dd.text()).replace(',', '.')
        long_dd = unicode(self._longitude_dd.text()).replace(',', '.')
        #
        try:
            value = float(lat_dd.replace(',', '.').replace(' ', ''))
            value += 0.0000008 # Round (= 0.5 min).
            degrees = math.floor(abs(value))
            minutes = (abs(value) - degrees) * 60
            minutes = math.floor(minutes*100)/100
            self._latitude_degree.setText(unicode(int(degrees)))
            self._latitude_minute.setText(unicode(minutes))
        except:
            self._latitude_degree.setText('')
            self._latitude_minute.setText('')
        try:
            value = float(long_dd.replace(',', '.').replace(' ', ''))
            value += 0.0000008 # Round (= 0.5 min).
            degrees = math.floor(abs(value))
            minutes = (abs(value) - degrees) * 60
            minutes = math.floor(minutes*100)/100
            self._longitude_degree.setText(unicode(int(degrees)))
            self._longitude_minute.setText(unicode(minutes))
        except:
            self._longitude_degree.setText('')
            self._longitude_minute.setText('')
    
    def clear_sample_info_selected(self):
        """ """
        box_result = QtGui.QMessageBox.warning(self, 'Warning', 
                                     'Do you want to clear all sample information?', 
                                     QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)
        if box_result == QtGui.QMessageBox.Ok:
            self.clear_sample_info()

    def _copy_sample_info_from(self):
        """ """
        dialog = CopyFromTemplateDialog(self)
        if dialog.exec_():
            dataset = dialog.get_dataset()
            sample = dialog.get_sample()
            if dataset and sample:
                dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
                sample_object = plankton_core.PlanktonCounterSample(dir_path,
                                                               dataset, 
                                                               sample)
                metadata_dict = sample_object.get_sample_info()
                self._from_dict_to_fields(metadata_dict)

    def _change_sample_name(self):
        """ """
        self.save_data()
        dialog = RenameSampleDialog(self, self._current_sample)
        if dialog.exec_():
            new_sample_name = dialog.get_new_sample_name()
            if new_sample_name:
                self.save_data()
                plankton_core.PlanktonCounterManager().rename_sample(self._current_dataset, 
                                                                     self._current_sample,
                                                                     new_sample_name)
                # Close dialog.
                self._parentwidget.reject()

    def _from_fields_to_dict(self, metadata_dict):
        """ """
        metadata_dict['plankton_toolbox_version'] = utils_qt.__version__
        metadata_dict['sample_name'] = unicode(self._current_sample)
        metadata_dict['sample_id'] = unicode(self._sample_id_edit.text())
        year = unicode(self._sample_year_edit.text())
        month = unicode(self._visit_month_edit.text())
        day = unicode(self._sample_day_edit.text())
        date_tmp = year + '-' + month + '-' + day 
        metadata_dict['sample_date'] = date_tmp
        metadata_dict['sample_time'] = unicode(self._sample_time_edit.text())
        metadata_dict['visit_year'] = unicode(self._sampling_year_edit.text())
        metadata_dict['country_code'] = unicode(self._sampling_country_edit.text())
        metadata_dict['platform_code'] = unicode(self._sampling_platform_edit.text())
        metadata_dict['sampling_series'] = unicode(self._sampling_series_edit.text())
        metadata_dict['sampling_laboratory'] = unicode(self._sampling_laboratory_edit.text())
        metadata_dict['orderer'] = unicode(self._orderer_edit.text())
        metadata_dict['project_code'] = unicode(self._project_edit.text())
        metadata_dict['station_name'] = unicode(self._station_name_edit.text())
        lat_deg_tmp = unicode(self._latitude_degree.text()).replace(',', '.')
        lat_min_tmp = unicode(self._latitude_minute.text()).replace(',', '.')
        long_deg_tmp = unicode(self._longitude_degree.text()).replace(',', '.')
        long_min_tmp = unicode(self._longitude_minute.text()).replace(',', '.')
        lat_dd_tmp = unicode(self._latitude_dd.text()).replace(',', '.')
        long_dd_tmp = unicode(self._longitude_dd.text()).replace(',', '.')
        metadata_dict['sample_latitude_dm'] = lat_deg_tmp + ' ' + lat_min_tmp
        metadata_dict['sample_longitude_dm'] = long_deg_tmp + ' ' + long_min_tmp
        metadata_dict['sample_latitude_dd'] = lat_dd_tmp
        metadata_dict['sample_longitude_dd'] = long_dd_tmp
        metadata_dict['sample_min_depth_m'] = unicode(self._sample_min_depth_m_edit.text())
        metadata_dict['sample_max_depth_m'] = unicode(self._sample_max_depth_m_edit.text())
        metadata_dict['water_depth_m'] = unicode(self._water_depth_m_edit.text())
        metadata_dict['sampler_type_code'] = unicode(self._sampler_type_code_list.currentText())
        metadata_dict['sampled_volume_l'] = unicode(self._sampled_volume_l_edit.text())
        metadata_dict['net_type_code'] = unicode(self._net_type_code_list.currentText())        
        metadata_dict['sampler_area_m2'] = unicode(self._sampler_area_m2_edit.text())
        metadata_dict['net_mesh_size_um'] = unicode(self._net_mesh_size_um_edit.text())
        metadata_dict['wire_angle_deg'] = unicode(self._wire_angle_deg_edit.text())
        metadata_dict['net_tow_length_m'] = unicode(self._net_tow_length_m_edit.text())
        metadata_dict['analytical_laboratory'] = unicode(self._analytical_laboratory_edit.text())
        year = unicode(self._analysis_year_edit.text())
        month = unicode(self._analysis_month_edit.text())
        day = unicode(self._analysis_day_edit.text())
        date_tmp = year + '-' + month + '-' + day 
        metadata_dict['analysis_date'] = date_tmp
        metadata_dict['analysed_by'] = unicode(self._analysed_by_edit.text())
        metadata_dict['sample_comment'] = unicode(self._sample_comment_edit.text())

    def _from_dict_to_fields(self, metadata_dict):
        """ """
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
        self._project_edit.setText(metadata_dict.get('project_code', ''))
        self._station_name_edit.setText(metadata_dict.get('station_name', ''))
        lat_tmp = unicode(metadata_dict.get('sample_latitude_dm', ''))
        long_tmp = unicode(metadata_dict.get('sample_longitude_dm', ''))
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
        self._latitude_dd.setText(unicode(metadata_dict.get('sample_latitude_dd', '')))
        self._longitude_dd.setText(unicode(metadata_dict.get('sample_longitude_dd', '')))
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
                       

class CopyFromTemplateDialog(QtGui.QDialog):
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
        return self._dataset
    
    def get_sample(self):
        """ """
        return self._sample
       
    def _content(self):
        """ """
        self._datasetsample_list = QtGui.QComboBox(self)
        self._datasetsample_list.addItems(['<select>'])
        copysampleinfo_button = QtGui.QPushButton('Copy sample info')
        copysampleinfo_button.clicked.connect(self._copy_sample_info)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('Dataset and sample:', self._datasetsample_list)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(copysampleinfo_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout 
    
    def _load_dataset_and_samples(self):
        """ """
        datasets = plankton_core.PlanktonCounterManager().get_dataset_names()
        for dataset in datasets:
            samples = plankton_core.PlanktonCounterManager().get_sample_names(dataset)
            for sample in samples:
                datasetsample = dataset + ': ' + sample
                self._datasetsample_dict[datasetsample] = (dataset, sample)
        #
        self._datasetsample_list.addItems(sorted(self._datasetsample_dict.keys()))
            
        
    def _copy_sample_info(self):
        """ """
        selectedtext = unicode(self._datasetsample_list.currentText())
        if selectedtext in self._datasetsample_dict:
            datasetsample = self._datasetsample_dict[selectedtext]
            self._dataset = datasetsample[0]
            self._sample = datasetsample[1]
        else:
            self._dataset = ''
            self._sample = ''            
        #
        self.accept() # Close dialog box.
        

class RenameSampleDialog(QtGui.QDialog):
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
        self._newsamplename_edit = QtGui.QLineEdit(self._old_sample_name)
        self._newsamplename_edit.setMinimumWidth(400)
        createsample_button = QtGui.QPushButton(' Rename sample ')
        createsample_button.clicked.connect(self._rename_sample)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('New sample name:', self._newsamplename_edit)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createsample_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _rename_sample(self):
        """ """
        self._new_sample_name = unicode(self._newsamplename_edit.text())
        #            
        self.accept() # Close dialog box.

