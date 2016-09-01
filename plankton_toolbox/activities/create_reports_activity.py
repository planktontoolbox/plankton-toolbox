#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets

import toolbox_utils
import plankton_core

class CreateReportsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._parent = parentwidget
        self._lastusedphytowinfilename = ''
        self._lastuseddirectory = ''
        self._tableview = None
        self._tabledataset = None
        self._report_list = None
        # Initialize parent.
        super(CreateReportsActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL('datasetListChanged'), 
                     self.update)
        #
        self._empty_dataset_table = plankton_core.DatasetTable()

    def update(self):
        """ """
        # Selectable list of loaded datasets.
        self._loaded_datasets_model.clear()        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            item = QtGui.QStandardItem('Dataset-' + unicode(rowindex + 1) + 
                                       '.   Source: ' + dataset.get_metadata('file_name'))
            item.setCheckState(QtCore.Qt.Checked)
#            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._loaded_datasets_model.appendRow(item)
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = utils_qt.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content.
        contentLayout.addWidget(self._content_select_datasets(), 5)
#         contentLayout.addWidget(self._content_load_datasets())
        contentLayout.addWidget(self._content_pw_report())
        contentLayout.addWidget(self._content_preview(), 10) # Stretch = 10.
        contentLayout.addWidget(self._content_save_result())
        return content
        
    def _content_load_datasets(self):
        """ """
        selectdatabox = QtGui.QGroupBox('Load datasets', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_phytowin(), 'Phytowin files (*.csv)')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # === Select datasets ===
    def _content_select_datasets(self):
        """ """
        widget = QtGui.QGroupBox('Select datasets', self)        
        #
        loaded_datasets_listview = QtGui.QListView()
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        #
        self._cleara_metadata_button = QtGui.QPushButton('Clear all')
        self.connect(self._cleara_metadata_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_datasets)                
        self._markall_button = QtGui.QPushButton('Mark all')
        self.connect(self._markall_button, QtCore.SIGNAL('clicked()'), self._check_all_datasets)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._cleara_metadata_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(loaded_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _check_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _content_pw_report(self):
        """ """
        createreportbox = QtGui.QGroupBox('Create report', self)        
        self._report_list = QtGui.QComboBox()
        self._report_list.addItems([
#                                      'Raw data: Table format',
#                                      'Qualitative (NET samples): DV format',
#                                      'Qualitative (NET samples): Species list',
#                                      'Quantitative (counted): DV format',
#                                      'Quantitative (counted): Table format',
                                     'Quantitative (counted): Species list'
                                     ])
        #
#         self._report_list.setCurrentIndex(0) # Select: 'Raw data: Table format'.
#         self._report_list.setCurrentIndex(4) # TEST
        #
        self.connect(self._report_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._report_list_changed)                
        #
        self._debuginfo_checkbox = QtGui.QCheckBox('View debug info')
        self._debuginfo_checkbox.setChecked(False)
        #
        self._aggregate_checkbox = QtGui.QCheckBox('Aggregate similar rows')
        self._aggregate_checkbox.setChecked(False)
        self._aggregate_checkbox.setEnabled(False)
        #
        self._createreport_button = QtGui.QPushButton('Create report')
        self.connect(self._createreport_button, QtCore.SIGNAL('clicked()'), self._create_pw_report)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(QtGui.QLabel('Report type:'))
        hbox1.addWidget(self._report_list)
        hbox1.addStretch(5)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(5)
        hbox2.addWidget(self._debuginfo_checkbox)
        hbox2.addWidget(self._aggregate_checkbox)
        hbox2.addWidget(self._createreport_button)
        #
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(hbox1)
        reportlayout.addLayout(hbox2)
        #
        createreportbox.setLayout(reportlayout)
        #
        return createreportbox

    def _report_list_changed(self):
        """ """
        reportindex = self._report_list.currentIndex()
        if (reportindex == 4) or (reportindex == 5):
            self._aggregate_checkbox.setEnabled(True)
        else:
            self._aggregate_checkbox.setEnabled(False)
        
        
    def _content_preview(self):
        """ """
        # === GroupBox: previewbox === 
        previewbox = QtGui.QGroupBox('Report preview', self)        
        # Active widgets and connections.
        self._tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._tableview)
        previewbox.setLayout(layout)
        #
        return previewbox

    def _content_save_result(self):
        """ """
        saveresultbox = QtGui.QGroupBox('Save report', self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtGui.QPushButton('Copy to clipboard')
        self.connect(self._copytoclipboard_button, QtCore.SIGNAL('clicked()'), self._copy_to_clipboard)                
        self._saveformat_list = QtGui.QComboBox()
        #
        self._saveformat_list.addItems(['Tab delimited text file (*.txt)',
                                         'Excel file (*.xlsx)'])
        self._saveformat_list.setCurrentIndex(1) # Excel file as default.
        self._savedataset_button = QtGui.QPushButton('Save as...')
        self.connect(self._savedataset_button, QtCore.SIGNAL('clicked()'), self._save_data)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
        hbox1.addStretch(10)
        hbox1.addWidget(QtGui.QLabel('File format:'))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox

    def _create_pw_report(self):
        """ """
        toolbox_utils.Logging().log('PW reports started...')
        toolbox_utils.Logging().start_accumulated_logging()
        try:
            selectedreport = self._report_list.currentText()
            #
            if selectedreport == 'Raw data: Table format':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                # Note: This report was prepared during data file import.
                # Preview result.
                if self._tabledataset:
                    self._tableview.setTableModel(self._tabledataset)
                    self._tableview.resizeColumnsToContents()
            elif selectedreport == 'Qualitative (NET samples): DV format':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                report = plankton_core.CreateReportToSharkweb(report_type = 'net')
                self._create_and_view_report(report)
            elif selectedreport == 'Qualitative (NET samples): Species list':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                report = plankton_core.CreateReportNetSpecies()
                self._create_and_view_report(report)
            elif selectedreport == 'Quantitative (counted): DV format':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                report = plankton_core.CreateReportToSharkweb(report_type = 'counted')
                self._create_and_view_report(report)
            elif selectedreport == 'Quantitative (counted): Table format':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                report = plankton_core.CreateReportCounted()
                self._create_and_view_report(report)
            elif selectedreport == 'Quantitative (counted): Species list':
                toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                report = plankton_core.CreateReportCountedSpecies()
                self._create_and_view_report(report)
            else:
                raise UserWarning('Sorry, the selected report \ntype is not yet implemented.')
        except UserWarning, e:
            toolbox_utils.Logging().error('UserWarning: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Warning', unicode(e))
            raise
        except (IOError, OSError), e:
            toolbox_utils.Logging().error('Error: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Error', unicode(e))
            raise
        except Exception, e:
            toolbox_utils.Logging().error('Failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Exception', unicode(e))
            raise
        finally:
            toolbox_utils.Logging().log_all_accumulated_rows()    
            toolbox_utils.Logging().log('PW reports finished.\r\n')

    def _create_and_view_report(self, report):
        """ """
        # Reset and redraw before loading new content.
        self._tableview.setTableModel(self._empty_dataset_table)
        self._tableview.resetModel() # Model data has changed.
        self._tableview.resizeColumnsToContents()
        # Create a list with selected datasets.
        datasets = []
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:        
                datasets.append(dataset)
        # Preview result.
        result_table = plankton_core.DatasetTable()
        report.create_report(datasets, result_table,
                            show_debug_info = self._debuginfo_checkbox.checkState(),
                            aggregate_rows = self._aggregate_checkbox.checkState())
        # Preview result.
        self._tableview.setTableModel(result_table)
        self._tableview.resetModel() # Model data has changed.
        self._tableview.resizeColumnsToContents()
    
    def _save_data(self):
        """ """
#         if self._tableview.getTableModel().getModeldata():
        if self._tableview.getTableModel():
            # Show select file dialog box.
            namefilter = 'All files (*.*)'
            if self._saveformat_list.currentIndex() == 1: # Xlsx file.
                namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            else:
                namefilter = 'Text files (*.txt);;All files (*.*)'
            filename = QtGui.QFileDialog.getSaveFileName(
                            self,
                            'Save dataset',
                            self._lastuseddirectory,
                            namefilter)
            filename = unicode(filename) # QString to unicode.
            # Check if user pressed ok or cancel.
            if filename:
                self._lastuseddirectory = os.path.dirname(filename)
                if self._saveformat_list.currentIndex() == 0: # Text file.
                    self._save_as_file(text_file_name = filename)
                elif self._saveformat_list.currentIndex() == 1: # Excel file.
                    self._save_as_file(excel_file_name = filename)
    
    def _save_as_file(self, text_file_name = None, excel_file_name = None):
        """ """
        tablefilewriter = toolbox_utils.TableFileWriter(
                                file_path = '', # Is included in the file names below.
                                text_file_name = text_file_name,                 
                                excel_file_name = excel_file_name,                 
                                )
        #
#         table_dataset = self._tableview.getTableModel().getModeldata()
        table_dataset = self._tableview.getTableModel()
        #
        tablefilewriter.write_file(table_dataset.get_header(), 
                                   table_dataset.get_rows())
        
    def _copy_to_clipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        field_separator = '\t'
        row_separator = '\r\n'
        clipboardstring = ''
        #
#         table_dataset = self._tableview.getTableModel().getModeldata()
        table_dataset = self._tableview.getTableModel()
        if table_dataset:
            # Header.
            clipboardstring = field_separator.join(map(unicode, table_dataset.get_header())).strip() + row_separator
            # Rows.
            for row in table_dataset.get_rows():
                clipboardstring += field_separator.join(map(unicode, row)).strip() + row_separator
        #
        clipboard.setText(clipboardstring)
        
 