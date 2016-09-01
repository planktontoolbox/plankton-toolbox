#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import datetime
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_core
import toolbox_utils

class PlanktonCounterSampleEdit(QtGui.QWidget):
    """ """
    def __init__(self, parentwidget, dataset, sample, current_sample_object):
        """ """        
        self._parentwidget = parentwidget
        self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        #
        super(PlanktonCounterSampleEdit, self).__init__()
        #
        self.setLayout(self._create_content_sample_edit())
        #
#         self.load_data()

    def load_data(self):
        """ """
        self._load_edit_table()

    def save_data(self):
        """ """
#         self._save_edit_table() # Don't save when tab in plankton_counter_dialog changed.

    def clear(self):
        """ """
        self._sampletable_table.clear()
        self._sampletable_editable.setTableModel(self._sampletable_table)
        self._sampletable_editable.resizeColumnsToContents()

    def _create_content_sample_edit(self):
        """ """
        contentlayout = QtGui.QVBoxLayout()
        # 
        contentlayout.addWidget(self._content_info(), 1)
        contentlayout.addWidget(self._content_table(), 100)
        contentlayout.addWidget(self._content_end(), 1)
        #
        return contentlayout

    # ===== COUNTER DATASETS =====    
    def _content_info(self):
        """ """
        widget = QtGui.QWidget()
        # 
        form1 = QtGui.QGridLayout()
        gridrow = 0
        # Empty row.
        form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
#         layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget

    # ===== COUNTER DATASETS =====    
    def _content_table(self):
        """ """
        widget = QtGui.QWidget()
#         widget = QtGui.QGroupBox('Plankton counter - sample editor', self._parentwidget)
        #
        self._sampletable_editable = utils_qt.ToolboxEditableQTableView()
        self._sampletable_table = plankton_core.DatasetTable()
#         self._sampletable_editable.setTableModel(self._sampletable_table)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sampletable_editable)
        widget.setLayout(layout)                
        #
        return widget

    def _content_end(self):
        """ """
        widget = QtGui.QWidget()
        self._exportsamplereport_button = QtGui.QPushButton('Export sample (.xlsx)...')
        self._exportsamplereport_button.clicked.connect(self._save_sample_report)
        self._save_button = QtGui.QPushButton('Save edited changes')
        self._save_button.clicked.connect(self._save_edit_table)
        #
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._exportsamplereport_button)
        layout.addStretch(10)
#         layout.addWidget(self._load_button)
        layout.addWidget(self._save_button)
#         layout.addWidget(self._clear_button)
        widget.setLayout(layout)
        #
        return widget
    
    def _load_edit_table(self):
        """ """
        self.clear()
        #
        header, rows = self._current_sample_object.get_sample_header_and_rows()
        self._sampletable_table.set_header(header)
        for row in rows:
            if len(''.join(row)) > 0:
                self._sampletable_table.append_row(row)
#         # Add some extra rows to be used when adding rows.
#         self._sampletable_table.append_row(['', ''])
#         self._sampletable_table.append_row(['', ''])
        #                                                       
        self._sampletable_editable.setTableModel(self._sampletable_table)
        self._sampletable_editable.resizeColumnsToContents()

    def _save_edit_table(self):
        """ """
        header = self._sampletable_table.get_header()
        rows = self._sampletable_table.get_rows()
        # 
        self._current_sample_object.update_all_sample_rows(header, rows)
        self._current_sample_object.save_sample_data()
        #
        self._load_edit_table()
        
    def _save_sample_report(self):
        """ """
        dialog = ExportSampleDialog(self, self._current_sample, self._current_sample_object)
        if dialog.exec_():
            pass
        
# TODO:
# TODO:
# TODO:

class ExportSampleDialog(QtGui.QDialog):
    """ """
    def __init__(self, parentwidget, sample, current_sample_object):
        """ """
#         self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        super(ExportSampleDialog, self).__init__(parentwidget)
        self.setWindowTitle("Export sample to Excel")
        self.setLayout(self._content())
        self.setMinimumSize(800, 100)

    def _content(self):
        """ """
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._content_export())
        #
        return layout                
 
    def _content_export(self):
        """ """
        widget = QtGui.QWidget()
        self._exporttargetdir_edit = QtGui.QLineEdit('')
        self._exporttargetdir_button = QtGui.QPushButton('Browse...')
        self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
        self._exporttargetfilename_edit = QtGui.QLineEdit(self._current_sample + '.xlsx')
        
        self._export_button = QtGui.QPushButton('Export')
        self._export_button.clicked.connect(self._export_dataset)
        self._exportcancel_button = QtGui.QPushButton('Cancel')
        self._exportcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label2 = QtGui.QLabel('Export to directory:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._exporttargetdir_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('Export file name:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetfilename_edit, gridrow, 1, 1, 9)
        gridrow += 1
        # Empty row.
        form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
        gridrow += 1
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._export_button)
        hbox1.addWidget(self._exportcancel_button)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget
        
    def _browse_target_dir(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._exporttargetdir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self._exporttargetdir_edit.setText(dirpath)
    
    def _export_dataset(self):
        """ """
        try:
            # Export path and file name.
            export_target_dir = unicode(self._exporttargetdir_edit.text())
            export_target_filename = unicode(self._exporttargetfilename_edit.text())
    #         filepathname = os.path.join(exporttargetdir, exporttargetfilename)
            #
            self._current_sample_object.export_sample_to_excel(export_target_dir, export_target_filename)
            #            
            self.accept() # Close dialog box.
        #        
        except Exception as e:
            toolbox_utils.Logging().error('Failed to export sample. ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Warning', 'Failed to export sample. ' + unicode(e))
        
#         # Prepare sample info header and rows.
#         sample_info_dict = self._current_sample_object.get_sample_info()
#         #
#         sample_info_header = ['key', 'value']
#         sample_info_header_order = [
#                 'sample_name',
#                 'sample_id',
#                 'sample_date',
#                 'sample_time',
#                 'year',
#                 'country_code',
#                 'platform_code',
#                 'sampling_series',
#                 'project',
#                 'station_name',
#                 'latitude_dm',
#                 'longitude_dm',
#                 'latitude_dd',
#                 'longitude_dd',
#                 'sample_min_depth_m',
#                 'sample_max_depth_m',
#                 'water_depth_m',
#                 'sampler_type_code',
#                 'sampled_volume_l',
#                 'sampler_area_m2',
#                 'net_mesh_size_um',
#                 'wire_angle_deg',
#                 'net_tow_length_m',
#                 'analysis_laboratory', 
#                 'analysis_date',
#                 'analysed_by',
#                 'sample_comment',               
#                 ]
#         sample_info_rows = []
#         for header_item in sample_info_header_order:
#             row = []
#             sample_info_rows.append([header_item, sample_info_dict.get(header_item, '')])
#         
#         # Prepare sample info header and rows.
#         sample_data_header = self._current_sample_object.get_header()
#         sample_data_rows = self._current_sample_object.get_rows()
#         
#         # Prepare sample info header and rows.
#         sample_method_header = []
#         sample_method_rows = []
#         sample_path = self._current_sample_object.get_dir_path()
#         if os.path.exists(os.path.join(sample_path, 'counting_method.txt')):
#             sample_method_header, sample_method_rows = plankton_core.PlanktonCounterMethods().get_counting_method_table(
#                                                 sample_path, 'counting_method.txt')        
# 
#         # Use openpyxl for Excel.
#         workbook = openpyxl.Workbook(optimized_write = True)  # Supports big files.
#         sampleinfo_worksheet = workbook.create_sheet(0)
#         sampleinfo_worksheet.title = 'Sample info'
#         # Header.
#         sampleinfo_worksheet.append(sample_info_header)
#         # Rows.
#         for row in sample_info_rows:
#             sampleinfo_worksheet.append(row)
#         #
#         sampledata_worksheet = workbook.create_sheet(1)
#         sampledata_worksheet.title = 'Sample data'
#         # Header.
#         sampledata_worksheet.append(sample_data_header)
#         # Rows.
#         for row in sample_data_rows:
#             sampledata_worksheet.append(row)
#         #
#         samplemethod_worksheet = workbook.create_sheet(2)
#         samplemethod_worksheet.title = 'Sample method'
#         # Header.
#         samplemethod_worksheet.append(sample_method_header)
#         # Rows.
#         for row in sample_method_rows:
#             samplemethod_worksheet.append(row)
#         # Save to file.   
#         workbook.save(filepathname)

