#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import os
import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework

class CreateReportsActivity(app_framework.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._parent = parentwidget
#         self._lastusedphytowinfilename = ''
        self._lastuseddirectory = ''
        self._tableview = None
        self._tabledataset = None
        self._report_list = None
        # Initialize parent.
        super(CreateReportsActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        app_framework.ToolboxDatasets().datasetListChanged.connect(self.update)
        #
        self._empty_dataset_table = plankton_core.DatasetTable()

    def update(self):
        """ """
        try:
            # Selectable list of loaded datasets.
            self._loaded_datasets_model.clear()        
            for rowindex, dataset in enumerate(app_framework.ToolboxDatasets().get_datasets()):
                item = QtGui.QStandardItem('Import-' + str(rowindex + 1) + 
                                           '.   Source: ' + dataset.get_metadata('file_name'))
                item.setCheckState(QtCore.Qt.Checked)
    #            item.setCheckState(QtCore.Qt.Unchecked)
                item.setCheckable(True)
                self._loaded_datasets_model.appendRow(item)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content.
        contentLayout.addWidget(self._content_select_datasets(), 5)
#         contentLayout.addWidget(self._content_load_datasets())
        contentLayout.addWidget(self._content_pw_report())
        contentLayout.addWidget(self._content_preview(), 10) # Stretch = 10.
        contentLayout.addWidget(self._content_save_result())
        return content
        
#     def _content_load_datasets(self):
#         """ """
#         selectdatabox = QtWidgets.QGroupBox('Load datasets', self)
#         tabWidget = QtWidgets.QTabWidget()
#         tabWidget.addTab(self._content_phytowin(), 'Phytowin files (*.csv)')
#         # Layout widgets.
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(tabWidget)
#         selectdatabox.setLayout(layout)        
#         #
#         return selectdatabox

    # === Select datasets ===
    def _content_select_datasets(self):
        """ """
        widget = QtWidgets.QGroupBox('Select datasets', self)        
        #
        loaded_datasets_listview = QtWidgets.QListView()
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        #
        self._cleara_metadata_button = app_framework.ClickableQLabel('Clear all')
        self._cleara_metadata_button.label_clicked.connect(self._uncheck_all_datasets)                
        self._markall_button = app_framework.ClickableQLabel('Mark all')
        self._markall_button.label_clicked.connect(self._check_all_datasets)                
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._cleara_metadata_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(loaded_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _check_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Checked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _uncheck_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Unchecked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _content_pw_report(self):
        """ """
        try:
            createreportbox = QtWidgets.QGroupBox('Create report', self)        
            self._report_list = QtWidgets.QComboBox()
            self._report_list.addItems([
                                        'Standard table format',
                                        'Quantitative (counted): Table format',
                                        'Quantitative (counted): Species list',
                                        'Qualitative (NET): Species list',
                                        'Quantitative (counted): Data Center export',
    #                                     'Qualitative (NET): Data Center export',
                                         ])
            #
    # TODO: For development:
    #         self._report_list.setCurrentIndex(4) # TODO:
            #
            self._report_list.currentIndexChanged.connect(self._report_list_changed)            
            #
    #         self._debuginfo_checkbox = QtWidgets.QCheckBox('View debug info')
    #         self._debuginfo_checkbox.setChecked(False)
            #
            self._aggregate_checkbox = QtWidgets.QCheckBox('Aggregate similar rows')
            self._aggregate_checkbox.setChecked(False)
            self._aggregate_checkbox.setEnabled(False)
            #
            self._createreport_button = QtWidgets.QPushButton('Create report')
            self._createreport_button.clicked.connect(self._create_pw_report)                
            # Layout widgets.
            hbox1 = QtWidgets.QHBoxLayout()
            hbox1.addWidget(QtWidgets.QLabel('Report type:'))
            hbox1.addWidget(self._report_list)
    #         hbox1.addWidget(self._debuginfo_checkbox)
            hbox1.addWidget(self._aggregate_checkbox)
            hbox1.addStretch(5)
            #
            hbox2 = QtWidgets.QHBoxLayout()
    #         hbox2.addStretch(5)
            hbox2.addWidget(self._createreport_button)
            hbox2.addStretch(5)
            #
            reportlayout = QtWidgets.QVBoxLayout()
            reportlayout.addLayout(hbox1)
            reportlayout.addWidget(QtWidgets.QLabel('  ')) # Add space.
            reportlayout.addLayout(hbox2)
            #
            createreportbox.setLayout(reportlayout)
            #
            return createreportbox
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _report_list_changed(self):
        """ """
        try:
    #         reportindex = self._report_list.currentIndex()
    #         if (reportindex == 4) or (reportindex == 5):
    #             self._aggregate_checkbox.setEnabled(True)
    #         else:
    #             self._aggregate_checkbox.setEnabled(False)
            self._aggregate_checkbox.setEnabled(False)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))        
        
    def _content_preview(self):
        """ """
        # === GroupBox: previewbox === 
        previewbox = QtWidgets.QGroupBox('Report preview', self)        
        # Active widgets and connections.
        self._tableview = app_framework.ToolboxQTableView()
        # Layout widgets.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._tableview)
        previewbox.setLayout(layout)
        #
        return previewbox

    def _content_save_result(self):
        """ """
        saveresultbox = QtWidgets.QGroupBox('Save report', self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtWidgets.QPushButton('Copy to clipboard')
        self._copytoclipboard_button.clicked.connect(self._copy_to_clipboard)                
        self._saveformat_list = QtWidgets.QComboBox()
        #
        self._saveformat_list.addItems(['Tab delimited text file (*.txt)',
                                         'Excel file (*.xlsx)'])
        self._saveformat_list.setCurrentIndex(1) # Excel file as default.
        self._savedataset_button = QtWidgets.QPushButton('Save as...')
        self._savedataset_button.clicked.connect(self._save_data)                
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
#         hbox1.addStretch(10)
        hbox1.addWidget(QtWidgets.QLabel('        File format:'))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        hbox1.addStretch(10)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox

    def _create_pw_report(self):
        """ """
        try:
            toolbox_utils.Logging().log('PW reports started...')
            toolbox_utils.Logging().start_accumulated_logging()
            try:
                selectedreport = self._report_list.currentText()
                #
                if selectedreport == 'Standard table format':
                    toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                    report = plankton_core.CreateReportStandard()
                    self._create_and_view_report(report)
    #                 # Note: This report was prepared during data file import.
    #                 # Preview result.
    #                 if self._tabledataset:
    #                     self._tableview.setTableModel(self._tabledataset)
    #                     self._tableview.resizeColumnsToContents()
                elif selectedreport == 'Quantitative (counted): Table format':
                    toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                    report = plankton_core.CreateReportCounted()
                    self._create_and_view_report(report)
                elif selectedreport == 'Quantitative (counted): Species list':
                    toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                    report = plankton_core.CreateReportSpecies(report_type = 'counted')
                    self._create_and_view_report(report)
                elif selectedreport == 'Qualitative (NET): Species list':
                    toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
                    report = plankton_core.CreateReportSpecies(report_type = 'net')
                    self._create_and_view_report(report)
                elif selectedreport == 'Quantitative (counted): Data Center export':
                    toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
    #                 report = plankton_core.CreateReportToDataCenterShark(report_type = 'counted')
                    report = plankton_core.CreateReportToDataCenterShark()
                    self._create_and_view_report(report)
    #             elif selectedreport == 'Qualitative (NET): Data Center export':
    #                 toolbox_utils.Logging().log('Selected report: ' + selectedreport + '.')
    # #                 report = plankton_core.CreateReportToDataCenterShark(report_type = 'net')
    #                 report = plankton_core.CreateReportToDataCenterShark()
    #                 self._create_and_view_report(report)
                else:
                    raise UserWarning('Sorry, the selected report \ntype is not yet implemented.')
            except UserWarning as e:
                toolbox_utils.Logging().error('UserWarning: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Warning', str(e))
                raise
            except (IOError, OSError) as e:
                toolbox_utils.Logging().error('Error: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Error', str(e))
                raise
            except Exception as e:
                toolbox_utils.Logging().error('Failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Exception', str(e))
                raise
            finally:
                toolbox_utils.Logging().log_all_accumulated_rows()    
                toolbox_utils.Logging().log('PW reports finished.\r\n')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _create_and_view_report(self, report):
        """ """
        try:
            # Reset and redraw before loading new content.
            self._tableview.setTableModel(self._empty_dataset_table)
            self._tableview.resetModel() # Model data has changed.
            self._tableview.resizeColumnsToContents()
            # Create a list with selected datasets.
            datasets = []
            for rowindex, dataset in enumerate(app_framework.ToolboxDatasets().get_datasets()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    datasets.append(dataset)
            # Preview result.
            result_table = plankton_core.DatasetTable()
            report.create_report(datasets, result_table,
    #                             show_debug_info = self._debuginfo_checkbox.checkState(),
                                aggregate_rows = self._aggregate_checkbox.checkState())
            # Preview result.
            self._tableview.setTableModel(result_table)
            self._tableview.resetModel() # Model data has changed.
            self._tableview.resizeColumnsToContents()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def _save_data(self):
        """ """
        try:
    #         if self._tableview.getTableModel().getModeldata():
            if self._tableview.getTableModel():
                # Show select file dialog box.
                namefilter = 'All files (*.*)'
                if self._saveformat_list.currentIndex() == 1: # Xlsx file.
                    namefilter = 'Excel files (*.xlsx);;All files (*.*)'
                else:
                    namefilter = 'Text files (*.txt);;All files (*.*)'
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                                self,
                                'Save dataset',
                                self._lastuseddirectory,
                                namefilter)
                filename = str(filename) # QString to str.
                # Check if user pressed ok or cancel.
                if filename:
                    self._lastuseddirectory = os.path.dirname(filename)
                    if self._saveformat_list.currentIndex() == 0: # Text file.
                        self._save_as_file(text_file_name = filename)
                    elif self._saveformat_list.currentIndex() == 1: # Excel file.
                        self._save_as_file(excel_file_name = filename)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def _save_as_file(self, text_file_name = None, excel_file_name = None):
        """ """
        try:
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _copy_to_clipboard(self):
        """ """
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            field_separator = '\t'
            row_separator = '\r\n'
            clipboardstring = ''
            #
    #         table_dataset = self._tableview.getTableModel().getModeldata()
            table_dataset = self._tableview.getTableModel()
            if table_dataset:
                # Header.
                clipboardstring = field_separator.join(map(str, table_dataset.get_header())).strip() + row_separator
                # Rows.
                for row in table_dataset.get_rows():
                    clipboardstring += field_separator.join(map(str, row)).strip() + row_separator
            #
            clipboard.setText(clipboardstring)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
 