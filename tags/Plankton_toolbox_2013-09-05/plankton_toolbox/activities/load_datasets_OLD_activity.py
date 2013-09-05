#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Test version of the 'get dataset activity'. Data is fetched from
the website test.mellifica.org/sharkweb, which should be replaced
by www.mellifica.se/sharkweb later. Search options is based on the 
layout of the corresponding page on the website.
"""

import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files

# TODO: TEST
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets



class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._dataset = monitoring_files.MonitoringFiles() # Empty dataset.
        self._pwsamplefiles = {}
        # Initialize parent.
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
#        self._activityheader.setStyleSheet(""" 
#            * { color: #00677f; background-color: #eaa97e; }
#            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._contentSelectData())
        contentLayout.addWidget(self._contentResultTable())
        contentLayout.addWidget(self._contentSaveResult())
        
    def _contentSelectData(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Select data", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._contentTextfile(), "Text file (tab delimited)")
        tabWidget.addTab(self._contentXlsx(), "Excel file (.xlsx)")
        tabWidget.addTab(self._contentSharkweb(), "Sharkweb")
        tabWidget.addTab(self._contentPW(), "PW")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def _contentTextfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._textfile_edit = QtGui.QLineEdit("")
        self._textfilebrowse_button = QtGui.QPushButton("Browse...")
        self._textfilegetdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self._textfilebrowse_button, QtCore.SIGNAL("clicked()"), self._textFileBrowse)              
        self.connect(self._textfilegetdata_button, QtCore.SIGNAL("clicked()"), self._getTextFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._textfilebrowse_button, gridrow, 10, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._textfilegetdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget
        
    def _contentXlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._xlsxfile_edit = QtGui.QLineEdit("")
        self._xlsxfilebrowse_button = QtGui.QPushButton("Browse...")
        self._xlsxfilegetdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self._xlsxfilebrowse_button, QtCore.SIGNAL("clicked()"), self._xlsxFileBrowse)              
        self.connect(self._xlsxfilegetdata_button, QtCore.SIGNAL("clicked()"), self._getXlsxFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.xlsx):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._xlsxfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._xlsxfilebrowse_button, gridrow, 10, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._xlsxfilegetdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget
        
    def _contentSharkweb(self):
        """ 
        Code sample from Javascript:
            var action = 'download_sample';
            var url = "shark_save.php?action=" + action + 
                "&bounds=" + encodeURIComponent(getBounds()) +
                "&year_from=" + encodeURIComponent($('sample_select_year_from').value) +
                "&year_to=" + encodeURIComponent($('sample_select_year_to').value) +
                "&month=" + encodeURIComponent(get_selected_month_list()) +
                "&datatype=" + encodeURIComponent($('sample_select_datatype').value) +
                "&parameter=" + encodeURIComponent($('sample_select_parameter').value) +
                "&project_code=" + encodeURIComponent($('sample_select_project_code').value) +
                "&orderer=" + encodeURIComponent($('sample_select_orderer').value) +
                "&station_name=" + encodeURIComponent($('sample_select_station_name').value) +
                "&station_name_option=" + encodeURIComponent($('sample_select_station_name_option').value) +
                "&taxon_name=" + encodeURIComponent($('sample_select_taxon').value) +
                "&taxon_name_option=" + encodeURIComponent($('sample_select_taxon_option').value) +
                "&sample_table_view=" + encodeURIComponent($('sample_select_table_view').value) +
                "&delimiters=" + encodeURIComponent($('misc_download_delimiters').value) +
                "&lineend=" + encodeURIComponent($('misc_download_lineend').value) +
                "&headerlang=" + encodeURIComponent($('misc_settings_header_language').value);
                // sample_table_view alternatives:
                // "sample_std",
                // "sample_hyd",
                // "sample_martrans",
                // "sample_bio_agg",
        """
        # Active widgets and connections.
        self._bounds_edit = QtGui.QLineEdit("")
        self._year_from_edit = QtGui.QLineEdit("2008")
        self._year_to_edit = QtGui.QLineEdit("2008")
        self._month_edit = QtGui.QLineEdit("06")
        self._datatype_edit = QtGui.QLineEdit("Phytoplankton")
        self._parameter_edit = QtGui.QLineEdit("COUNTNR")
        self._project_code_edit = QtGui.QLineEdit("")
        self._orderer_edit = QtGui.QLineEdit("")
        self._deliverer_edit = QtGui.QLineEdit("")
        self._station_name_edit = QtGui.QLineEdit(u'släggö, by15')
        self._station_name_option_edit = QtGui.QLineEdit("station_list")
        self._taxon_name_edit = QtGui.QLineEdit("Dinophyceae")
        self._taxon_name_option_edit = QtGui.QLineEdit("class")
#        self._sample_table_view_edit = QtGui.QLineEdit("sample_std")
        self._sample_table_view_edit = QtGui.QLineEdit("sample_col_bio")
        self._delimiters_edit = QtGui.QLineEdit("point-tab")
        self._lineend_edit = QtGui.QLineEdit("unix")
        self._limit_edit = QtGui.QLineEdit("2000")
        self._headerlang_edit = QtGui.QLineEdit("sv")
        #
        self._get_data_button = QtGui.QPushButton("Get data")
        self.connect(self._get_data_button, QtCore.SIGNAL("clicked()"), self._getSharkwebData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label00 = QtGui.QLabel("Year")
        label01 = QtGui.QLabel("-")
        label02 = QtGui.QLabel("Datatype")
        label03 = QtGui.QLabel("Project")
        label04 = QtGui.QLabel("Month")
        label05 = QtGui.QLabel("Parameter")
        label06 = QtGui.QLabel("Orderer")
        label07 = QtGui.QLabel("Deliverer")
        label08 = QtGui.QLabel("Station")
        label09 = QtGui.QLabel("Species/taxon")
        label10 = QtGui.QLabel("Header language")
        label11 = QtGui.QLabel("Column set")
        gridrow += 1
        form1.addWidget(label00, gridrow, 0, 1, 3)
        form1.addWidget(label02, gridrow, 3, 1, 1)
        form1.addWidget(label03, gridrow, 4, 1, 2)
        gridrow += 1
        form1.addWidget(self._year_from_edit, gridrow, 0, 1, 1)
        form1.addWidget(label01, gridrow, 1, 1, 1)
        form1.addWidget(self._year_to_edit, gridrow, 2, 1, 1)        
        form1.addWidget(self._datatype_edit, gridrow, 3, 1, 1)        
        form1.addWidget(self._project_code_edit, gridrow, 4, 1, 2)
        gridrow += 1
        form1.addWidget(label04, gridrow, 0, 1, 1)
        form1.addWidget(label05, gridrow, 3, 1, 1)
        form1.addWidget(label06, gridrow, 4, 1, 1)
        form1.addWidget(label07, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(self._month_edit, gridrow, 0, 1, 3)
        form1.addWidget(self._parameter_edit, gridrow, 3, 1, 1)
        form1.addWidget(self._orderer_edit, gridrow, 4, 1, 1)
        form1.addWidget(self._deliverer_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(label08, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._station_name_edit, gridrow, 3, 1, 2)
        form1.addWidget(self._station_name_option_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(label10, gridrow, 0, 1, 1)
        form1.addWidget(label11, gridrow, 2, 1, 1)
        form1.addWidget(label09, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._headerlang_edit, gridrow, 0, 1, 1)
        form1.addWidget(self._sample_table_view_edit, gridrow, 2, 1, 1)
        form1.addWidget(self._taxon_name_edit, gridrow, 3, 1, 2)
        form1.addWidget(self._taxon_name_option_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(self._get_data_button, gridrow, 5, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self._get_data_button)
        # Layout widgets.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addLayout(form1)
#        layout.addLayout(hbox1)
        #
        return widget

    def _contentPW(self):
        """ """
        # Active widgets and connections.
        self._pwfromdirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
#        self._pwfromdirectory_edit = QtGui.QLineEdit("../../../../data/planktondata/phytowin_files") # TODO: Use toolbox settings.
        self._pwfromdirectory_button = QtGui.QPushButton("Browse...")
        #
        self._files_table = QtGui.QTableWidget()
        self._files_table.setAlternatingRowColors(True)
        self._files_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self._files_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._files_table.verticalHeader().setDefaultSectionSize(18)
        self._files_table.setColumnCount(1)
        self._files_table.horizontalHeader().setStretchLastSection(True)
        self._files_table.setHorizontalHeaderLabels(["File"])
        self._getpwdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self._pwfromdirectory_button, QtCore.SIGNAL("clicked()"), self._pwFromDirectoryBrowse)                
        self.connect(self._getpwdata_button, QtCore.SIGNAL("clicked()"), self._getPwData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From directory:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._pwfromdirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._pwfromdirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Files (CSV):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._files_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._getpwdata_button)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        #
        return widget
        
    def _contentResultTable(self):
        """ """
        resultbox = QtGui.QGroupBox("Result table", self)
        # Active widgets and connections.
        self._tableView = QtGui.QTableView()
        self._tableView.setAlternatingRowColors(True)
        self._tableView.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self._tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._tableView.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self._tableView.verticalHeader().setDefaultSectionSize(18)
        # Model, data and selection        
        self._model = ResultTableModel(self._dataset)
        self._tableView.setModel(self._model)        
        selectionModel = QtGui.QItemSelectionModel(self._model)
        self._tableView.setSelectionModel(selectionModel)
        self._tableView.resizeColumnsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._test)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self._test2)
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._tableView)
        resultbox.setLayout(layout)        
        #
        return resultbox
        
    def _contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Export data", self)
        # Active widgets and connections.
        self._saveformat_list = QtGui.QComboBox()
        self._saveformat_list.addItems(["Tab delimited text file (.txt)",
                                         "Excel file (.xlsx)"])
        self._savetodirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
        self._savetodirectory_button = QtGui.QPushButton("Browse...")
        self._savetofile_edit = QtGui.QLineEdit("data.txt")
        self._savedata_button = QtGui.QPushButton("Save")
####        self.connect(self._saveformat_list, QtCore.SIGNAL("????()"), self._????) # TODO: Switch between data.txt & data.xlsx.                
        self.connect(self._savetodirectory_button, QtCore.SIGNAL("clicked()"), self._saveToDirectoryBrowse)                
        self.connect(self._savedata_button, QtCore.SIGNAL("clicked()"), self._saveData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Format:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._saveformat_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("To directory:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._savetodirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._savetodirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._savetofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._savedata_button, gridrow, 10, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self._savedata_button)
        #
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(form1)
#        reportlayout.addLayout(hbox1)
        saveresultbox.setLayout(reportlayout)
        #
        return saveresultbox
        
    def _textFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._textfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._textfile_edit.setText(filepath)

    def _getTextFile(self):
        """ """
###        self._dataset.clear()
        self._refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self._dataset = monitoring_files.TextFile()
        self._model.setDataset(self._dataset)
        #
        self._dataset.readFile(unicode(self._textfile_edit.text()))
        #        
        self._refreshResultTable()

    def _xlsxFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._xlsxfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._xlsxfile_edit.setText(filepath)

    def _getXlsxFile(self):
        """ """
        self._dataset.clear()
        self._refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self._dataset = monitoring_files.ExcelXlsxFile()
        self._model.setDataset(self._dataset)
        #
        self._dataset.readFile(unicode(self._xlsxfile_edit.text()))
        #        
        self._refreshResultTable()
    
    def _getSharkwebData(self):
        """ """
        self._dataset.clear()
        self._refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self._dataset = monitoring_files.SharkwebDownload()
        self._model.setDataset(self._dataset)
        #
        parameters = {}
        parameters['action'] = unicode('download_sample') # Not json
#        parameters['action'] = unicode('get_sample_table') # Json
        parameters['bounds'] = unicode('')
        parameters['year_from'] = unicode(self._year_from_edit.text())
        parameters['year_to'] = unicode(self._year_to_edit.text())
        parameters['month'] = unicode(self._month_edit.text())
        parameters['datatype'] = unicode(self._datatype_edit.text())
        parameters['parameter'] = unicode(self._parameter_edit.text())
        parameters['project_code'] = unicode(self._project_code_edit.text())
        parameters['orderer'] = unicode(self._orderer_edit.text())
#        parameters['deliverer'] = unicode(self._deliverer_edit.text()
        parameters['station_name'] = unicode(self._station_name_edit.text())
        parameters['station_name_option'] = unicode(self._station_name_option_edit.text())
        parameters['taxon_name'] = unicode(self._taxon_name_edit.text())
        parameters['taxon_name_option'] = unicode(self._taxon_name_option_edit.text())
        parameters['sample_table_view'] = unicode(self._sample_table_view_edit.text())
        parameters['delimiters'] = unicode(self._delimiters_edit.text())
        parameters['lineend'] = unicode(self._lineend_edit.text())
        parameters['limit'] = unicode(self._limit_edit.text())
        parameters['headerlang'] = unicode(self._headerlang_edit.text())
        # Get data.
        self._dataset.getData(parameters)
        self._refreshResultTable()

    def _pwFromDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._pwfromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self._pwfromdirectory_edit.setText(dirpath)
            self._pwsamplefiles.clear()
            # Add files in selected directory to QTableWidget.
            for row, filename in enumerate(sorted(os.listdir(unicode(self._pwfromdirectory_edit.text())))):
                if os.path.splitext(unicode(filename))[1] in ['.csv', '.CSV']:
                    self._files_table.setRowCount(row + 1)
                    item = QtGui.QTableWidgetItem(unicode(filename))
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self._files_table.setItem(row, 0, item)            
        
    def _getPwData(self):
        """ """
        self._dataset.clear()
        self._refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self._dataset = monitoring_files.PwCsvTable()
        self._model.setDataset(self._dataset)
        #
        for index in range(self._files_table.rowCount()):
            item = self._files_table.item(index, 0)
            if item.checkState(): # Check if selected by user.
                # When reading from a table the display rule must be used.
                filename = unicode(item.data(QtCore.Qt.DisplayRole).toString())
                print(self._pwfromdirectory_edit.text())
                print(filename)
                self._dataset.readFile(self._pwfromdirectory_edit.text() + '/' + filename)
        #        
        self._refreshResultTable()

    def _saveToDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._savetodirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self._savetodirectory_edit.setText(dirpath)
        
    def _saveData(self):
        """ """






#            # Filepath.            
#            reportfilepath = ''
#            if len(unicode(self._todirectory_edit.text())) > 0:
#                reportfilepath = unicode(self._todirectory_edit.text()) + '/'
#            reportfilepath += unicode(self._tofile_edit.text())
        
        
        
        
        
        
        
        
        filename = self._savetodirectory_edit.text()  + '/' + \
                   self._savetofile_edit.text()
        if self._saveformat_list.currentIndex() == 0: # Text file.
            self._dataset.SaveAsTextFile(unicode(filename))
        elif self._saveformat_list.currentIndex() == 1: # Xlsx file.
            self._dataset.SaveExcelXlsxFile(unicode(filename))
        
    def _refreshResultTable(self):
        """ """
        self._model.reset() # Model data has changed.
        self._tableView.resizeColumnsToContents()

    def _test(self, index):
        """ """
        print("TEST..." + "%f" % index.row())

    def _test2(self, index, index2):
        """ """
        print("TEST2..." + "%f" % index.row() + " %f" % index.column())


class ResultTableModel(QtCore.QAbstractTableModel):
    """
    """
    def __init__(self, dataset):
        """ """
        self._dataset = dataset
        # Initialize parent.
        super(ResultTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self._dataset = dataset
        
        ############ Test
        toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        
        

    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self._dataset.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self._dataset.getColumnCount()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._dataset.getHeaderItem(section))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(self._dataset.getDataItem(index.row(), index.column()))
        return QtCore.QVariant()

