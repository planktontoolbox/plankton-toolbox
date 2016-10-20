#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.analyse_datasets_tab1 as tab1
import plankton_toolbox.activities.analyse_datasets_tab2 as tab2
import plankton_toolbox.activities.analyse_datasets_tab3 as tab3
import plankton_toolbox.activities.analyse_datasets_tab4 as tab4
import plankton_toolbox.activities.analyse_datasets_tab5 as tab5
import plankton_toolbox.activities.analyse_datasets_tab6 as tab6
import plankton_toolbox.activities.analyse_datasets_tab7 as tab7
import plankton_toolbox.activities.analyse_datasets_tab8 as tab8

import toolbox_utils
import plankton_core

class AnalyseDatasetsActivity(activity_base.ActivityBase):
    """
    """
    def __init__(self, name, parentwidget):
        """ """
        # Create object containing analysis data.
        self._analysisdata = plankton_core.AnalysisData()
        self._statisticaldata = plankton_core.StatisticalData()
        self._reportdata = plankton_core.ReportData()
        
        # Filename used when saving data to file.
        self._lastuseddirectory = '.'
        # Create tab widgets.
        self._tab1widget = tab1.AnalyseDatasetsTab1()
        self._tab2widget = tab2.AnalyseDatasetsTab2()
        self._tab3widget = tab3.AnalyseDatasetsTab3()
        self._tab4widget = tab4.AnalyseDatasetsTab4()
        self._tab5widget = tab5.AnalyseDatasetsTab5()
        self._tab6widget = tab6.AnalyseDatasetsTab6()
        self._tab7widget = tab7.AnalyseDatasetsTab7()
        self._tab8widget = tab8.AnalyseDatasetsTab8()
        # 
        self._tab1widget.set_main_activity(self)
        self._tab2widget.set_main_activity(self)
        self._tab3widget.set_main_activity(self)
        self._tab4widget.set_main_activity(self)
        self._tab5widget.set_main_activity(self)
        self._tab6widget.set_main_activity(self)
        self._tab7widget.set_main_activity(self)
        self._tab8widget.set_main_activity(self)
        # Initialize parent.
        super(AnalyseDatasetsActivity, self).__init__(name, parentwidget)
        #
        self._empty_dataset_table = plankton_core.DatasetTable()

    def get_analysis_data(self):
        """ """
        return self._analysisdata 
        
    def get_statistical_data(self):
        """ """
        return self._statisticaldata 
        
    def get_report_data(self):
        """ """
        return self._reportdata 
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = utils_qt.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_analyse_tabs(), 3)
        contentLayout.addWidget(self._content_analysis_data_table(), 10)
        contentLayout.addWidget(self._content_save_analysis_data())
    
    def _content_analyse_tabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._tab1widget.content_select_datasets(), 'Select dataset(s)')
        tabWidget.addTab(self._tab2widget.content_prepare_data(), 'Clean up')
        tabWidget.addTab(self._tab3widget.content_aggregate_data(), 'Aggregate/complement data')
        tabWidget.addTab(self._tab4widget.content_select_data(), 'Filter')
        tabWidget.addTab(self._tab5widget.content_predefined_graphs(), 'Predefined graphs')
        tabWidget.addTab(self._tab6widget.content_generic_graphs(), 'Generic graphs')
        tabWidget.addTab(self._tab7widget.content_statistics(), 'Statistics')
        tabWidget.addTab(self._tab8widget.content_reports(), 'Exports')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== ANALYSIS DATA =====    
    def _content_analysis_data_table(self):
        """ """
        # Active widgets and connections.
        analysisdatagroupbox = QtGui.QGroupBox('Analysis data, filtered data, statistical data and export data', self)
        # Active widgets and connections.
        self._viewdata_list = QtGui.QComboBox()
        self._viewdata_list.addItems(["Analysis data",
                                      "Filtered analysis data",
                                      "Statistical data",
                                      "Export data",
                                      "Hide data (to increase performance)"])
        self.connect(self._viewdata_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._view_data_list_changed)                
        #
        self._numberofrows_label = QtGui.QLabel('Number of rows: 0')
        #
#        self._hidedata_checkbox = QtGui.QCheckBox('Hide data')
#        self._hidedata_checkbox.setChecked(False)
#        self.connect(self._hidedata_checkbox, QtCore.SIGNAL('clicked()'), self._view_hide_data_changed)                
        #
        self._refreshfiltereddata_button = QtGui.QPushButton('Refresh filtered data') # TODO:
        self._refreshfiltereddata_button.hide()
        self.connect(self._refreshfiltereddata_button, QtCore.SIGNAL('clicked()'), self._refresh_filtered_data)                
        #
        self._tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(QtGui.QLabel('View:'))
        hbox1.addWidget(self._viewdata_list)
#        hbox1.addWidget(self._hidedata_checkbox)
        hbox1.addWidget(self._refreshfiltereddata_button)
        hbox1.addStretch(5)
        hbox1.addWidget(self._numberofrows_label)
        #
        layout.addLayout(hbox1)
        layout.addWidget(self._tableview)
        #
        analysisdatagroupbox.setLayout(layout)
        #
        return analysisdatagroupbox

    def _view_data_list_changed(self, row_index):
        """ """
        if row_index == 1:
            self._refreshfiltereddata_button.show()
        else:
            self._refreshfiltereddata_button.hide()
        #
        self.update_viewed_data()
        
    def _refresh_filtered_data(self):
        """ """
        # Note: row_index used inside update_viewed_data().
        self.update_viewed_data()
        
    def _view_hide_data_changed(self):
        """ """
        self.update_viewed_data()
        
    def _content_save_analysis_data(self):
        """ """
        saveresultbox = QtGui.QGroupBox('Export data', self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtGui.QPushButton('Copy to clipboard')
        self.connect(self._copytoclipboard_button, QtCore.SIGNAL('clicked()'), self._copy_to_clipboard)                
        self._saveformat_list = QtGui.QComboBox()
        self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
                                         "Excel file (*.xlsx)"])
        self._savedataset_button = QtGui.QPushButton('Save...')
        self.connect(self._savedataset_button, QtCore.SIGNAL('clicked()'), self._save_analysis_data)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
#         hbox1.addStretch(5)
        hbox1.addWidget(QtGui.QLabel('File format:'))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        hbox1.addStretch(5)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox
        
#     def set_analysis_data(self, analysis_data):
#         """ """
#         self._analysisdata = analysis_data
#         self.update_viewed_data()
#         self.update_all_tabs()    
    
    def update_viewed_data_and_tabs(self):
        """ """
        self.update_viewed_data()
        self.update_all_tabs()
        
    def hide_viewed_data(self):
        """ """
        # Clear table.
        self._tableview.setTableModel(self._empty_dataset_table)
        self._refresh_viewed_data_table()

        
    def update_viewed_data(self):
        """ """
        # Clear table.
        self._tableview.setTableModel(self._empty_dataset_table)
        self._refresh_viewed_data_table()
        self._numberofrows_label.setText('Number of rows: 0')
        # 
        if not self._analysisdata.get_data():
            return
        #
        selectedviewindex = self._viewdata_list.currentIndex()
        if selectedviewindex == 0:
            # View analysis data.
            # Convert from tree model to table model.
            targetdataset = plankton_core.DatasetTable()
            self._analysisdata.get_data().convert_to_table_dataset(targetdataset)
            # View model.
            self._tableview.setTableModel(targetdataset)
            self._refresh_viewed_data_table()
        elif selectedviewindex == 1:
            # View filtered data only.
            self._tab4widget.update_filter() # Must be done before create_filtered_dataset().
            filtereddataset = self._analysisdata.create_filtered_dataset()
            # Convert from tree model to table model.
            targetdataset = plankton_core.DatasetTable()
            filtereddataset.convert_to_table_dataset(targetdataset)
            # View model.
            self._tableview.setTableModel(targetdataset)
            self._refresh_viewed_data_table()
        elif selectedviewindex == 2:
            # Statistical data.
            self._tableview.setTableModel(self._statisticaldata.get_data())
            self._refresh_viewed_data_table()
        elif selectedviewindex == 3:
            # Export data.
            self._tableview.setTableModel(self._reportdata.get_data())
            self._refresh_viewed_data_table()
        else:
            # Hide data.
            self._tableview.setTableModel(self._empty_dataset_table)
            self._refresh_viewed_data_table()
        #
        if self._tableview.getTableModel():
            self._numberofrows_label.setText('Number of rows: ' + unicode(self._tableview.getTableModel().get_row_count()))
        else:
            self._numberofrows_label.setText('Number of rows: 0')

        
    def _refresh_viewed_data_table(self):
        """ """
        self._tableview.resetModel() # Model data has changed.
        self._tableview.resizeColumnsToContents()

    def _save_analysis_data(self):
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
                            'Export dataset',
                            self._lastuseddirectory,
                            namefilter)
            filename = unicode(filename) # QString to unicode.
            # Check if user pressed ok or cancel.
            if filename:
                self._lastuseddirectory = os.path.dirname(filename)
                if self._saveformat_list.currentIndex() == 0: # Text file.
#                     self._tableview.getTableModel().getModeldata().saveAsTextFile(filename)
                    self._tableview.getTableModel().save_as_file(text_file_name = filename)
                elif self._saveformat_list.currentIndex() == 1: # Excel file.
#                     self._tableview.getTableModel().getModeldata().saveAsExcelFile(filename)
                    self._tableview.getTableModel().save_as_file(excel_file_name = filename)

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
            clipboardstring = field_separator.join(map(unicode, table_dataset.get_header())) + row_separator
            # Rows.
            for row in table_dataset.get_rows():
                clipboardstring += field_separator.join(map(unicode, row)) + row_separator
        #
        clipboard.setText(clipboardstring)

    def clear_all_tabs(self):
        """ """
        self._tab1widget.clear()
        self._tab2widget.clear()
        self._tab3widget.clear()
        self._tab4widget.clear()
        self._tab5widget.clear()
        self._tab6widget.clear()
        self._tab7widget.clear()
        self._tab8widget.clear()

    def update_all_tabs(self):
        """ """
        self._tab1widget.update()
        self._tab2widget.update()
        self._tab3widget.update()
        self._tab4widget.update()
        self._tab5widget.update()
        self._tab6widget.update()
        self._tab7widget.update()
        self._tab8widget.update()

    def update_filter(self):
        """ Must be done before calls to create_filtered_dataset(). """
        self._tab4widget.update_filter()

    def view_analysis_data(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(0)
            self.update_viewed_data()

    def view_statistical_data(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(2)
            self.update_viewed_data()

    def view_report_data(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(3)
            self.update_viewed_data()

