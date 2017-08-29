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
#         layout.addStretch(10)
#         layout.addWidget(self._load_button)
        layout.addWidget(self._save_button)
#         layout.addWidget(self._clear_button)
        layout.addStretch(10)
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
        #                                                       
        self._sampletable_editable.setTableModel(self._sampletable_table)
        self._sampletable_editable.resizeColumnsToContents()

    def _save_edit_table(self):
        """ """
        header = self._sampletable_table.get_header()
        rows = self._sampletable_table.get_rows()
        # 
        self._current_sample_object.update_all_sample_rows(header, rows)
        #
        self._current_sample_object.recalculate_sample_data(self._current_sample_method)
        self._current_sample_object.save_sample_data()
        #
        self._load_edit_table()
        
    def _save_sample_report(self):
        """ """
        dialog = ExportSampleDialog(self, self._current_sample, self._current_sample_object)
        if dialog.exec_():
            pass
        

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
#             filepathname = os.path.join(exporttargetdir, exporttargetfilename)
            # Warning.
            if os.path.exists(os.path.join(export_target_dir, export_target_filename)):
                box_result =  QtGui.QMessageBox.warning(self, 'Warning', 
                                             'Excel file already exists. Do you want ro replace it?', 
                                             QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)
                if box_result == QtGui.QMessageBox.Ok:
                    self._current_sample_object.export_sample_to_excel(export_target_dir, export_target_filename)    
            else:
                self._current_sample_object.export_sample_to_excel(export_target_dir, export_target_filename)
            #            
            self.accept() # Close dialog box.
        #        
        except Exception as e:
            toolbox_utils.Logging().error('Failed to export sample. ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Warning', 'Failed to export sample. ' + unicode(e))
        
