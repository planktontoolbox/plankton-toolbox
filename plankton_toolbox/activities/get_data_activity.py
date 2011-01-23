#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

class GetDataActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self.__dataset = monitoring_files.MonitoringFiles() # Empty dataset.
        self._pwsamplefiles = {}
        # Initialize parent.
        super(GetDataActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        #
        contentLayout.addWidget(self.__contentSelectData())
        contentLayout.addWidget(self.__contentResultTable())
        contentLayout.addWidget(self.__contentSaveResult())
        
    def __contentSelectData(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Select data", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.__contentTextfile(), "Text file (tab delimited)")
        tabWidget.addTab(self.__contentXlsx(), "Excel file (.xlsx)")
        tabWidget.addTab(self.__contentSharkweb(), "Sharkweb")
        tabWidget.addTab(self.__contentPW(), "PW")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def __contentTextfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self.__textfile_edit = QtGui.QLineEdit("")
        self.__textfilebrowse_button = QtGui.QPushButton("Browse...")
        self.__textfilegetdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self.__textfilebrowse_button, QtCore.SIGNAL("clicked()"), self.__textFileBrowse)              
        self.connect(self.__textfilegetdata_button, QtCore.SIGNAL("clicked()"), self.__getTextFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__textfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__textfilebrowse_button, gridrow, 10, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__textfilegetdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget
        
    def __contentXlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self.__xlsxfile_edit = QtGui.QLineEdit("")
        self.__xlsxfilebrowse_button = QtGui.QPushButton("Browse...")
        self.__xlsxfilegetdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self.__xlsxfilebrowse_button, QtCore.SIGNAL("clicked()"), self.__xlsxFileBrowse)              
        self.connect(self.__xlsxfilegetdata_button, QtCore.SIGNAL("clicked()"), self.__getXlsxFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.xlsx):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__xlsxfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__xlsxfilebrowse_button, gridrow, 10, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__xlsxfilegetdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget
        
    def __contentSharkweb(self):
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
        self.__bounds_edit = QtGui.QLineEdit("")
        self.__year_from_edit = QtGui.QLineEdit("2008")
        self.__year_to_edit = QtGui.QLineEdit("2008")
        self.__month_edit = QtGui.QLineEdit("06")
        self.__datatype_edit = QtGui.QLineEdit("Phytoplankton")
        self.__parameter_edit = QtGui.QLineEdit("COUNTNR")
        self.__project_code_edit = QtGui.QLineEdit("")
        self.__orderer_edit = QtGui.QLineEdit("")
        self.__deliverer_edit = QtGui.QLineEdit("")
        self.__station_name_edit = QtGui.QLineEdit("släggö, by15")
        self.__station_name_option_edit = QtGui.QLineEdit("station_list")
        self.__taxon_name_edit = QtGui.QLineEdit("Dinophyceae")
        self.__taxon_name_option_edit = QtGui.QLineEdit("class")
        self.__sample_table_view_edit = QtGui.QLineEdit("sample_std")
        self.__delimiters_edit = QtGui.QLineEdit("point-tab")
        self.__lineend_edit = QtGui.QLineEdit("unix")
        self.__limit_edit = QtGui.QLineEdit("2000")
        self.__headerlang_edit = QtGui.QLineEdit("sv")
        #
        self.__get_data_button = QtGui.QPushButton("Get data")
        self.connect(self.__get_data_button, QtCore.SIGNAL("clicked()"), self.__getSharkwebData)                
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
        form1.addWidget(self.__year_from_edit, gridrow, 0, 1, 1)
        form1.addWidget(label01, gridrow, 1, 1, 1)
        form1.addWidget(self.__year_to_edit, gridrow, 2, 1, 1)        
        form1.addWidget(self.__datatype_edit, gridrow, 3, 1, 1)        
        form1.addWidget(self.__project_code_edit, gridrow, 4, 1, 2)
        gridrow += 1
        form1.addWidget(label04, gridrow, 0, 1, 1)
        form1.addWidget(label05, gridrow, 3, 1, 1)
        form1.addWidget(label06, gridrow, 4, 1, 1)
        form1.addWidget(label07, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(self.__month_edit, gridrow, 0, 1, 3)
        form1.addWidget(self.__parameter_edit, gridrow, 3, 1, 1)
        form1.addWidget(self.__orderer_edit, gridrow, 4, 1, 1)
        form1.addWidget(self.__deliverer_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(label08, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self.__station_name_edit, gridrow, 3, 1, 2)
        form1.addWidget(self.__station_name_option_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(label10, gridrow, 0, 1, 1)
        form1.addWidget(label11, gridrow, 2, 1, 1)
        form1.addWidget(label09, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self.__headerlang_edit, gridrow, 0, 1, 1)
        form1.addWidget(self.__sample_table_view_edit, gridrow, 2, 1, 1)
        form1.addWidget(self.__taxon_name_edit, gridrow, 3, 1, 2)
        form1.addWidget(self.__taxon_name_option_edit, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(self.__get_data_button, gridrow, 5, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self.__get_data_button)
        # Layout widgets.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addLayout(form1)
#        layout.addLayout(hbox1)
        #
        return widget

    def __contentPW(self):
        """ """
        # Active widgets and connections.
        self.__pwfromdirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
#        self.__pwfromdirectory_edit = QtGui.QLineEdit("../../../../data/planktondata/phytowin_files") # TODO: Use toolbox settings.
        self.__pwfromdirectory_button = QtGui.QPushButton("Browse...")
        #
        self.__files_table = QtGui.QTableWidget()
        self.__files_table.setAlternatingRowColors(True)
        self.__files_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.__files_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.__files_table.verticalHeader().setDefaultSectionSize(18)
        self.__files_table.setColumnCount(1)
        self.__files_table.horizontalHeader().setStretchLastSection(True)
        self.__files_table.setHorizontalHeaderLabels(["File"])
        self.__getpwdata_button = QtGui.QPushButton("Get data")
        #
        self.connect(self.__pwfromdirectory_button, QtCore.SIGNAL("clicked()"), self.__pwFromDirectoryBrowse)                
        self.connect(self.__getpwdata_button, QtCore.SIGNAL("clicked()"), self.__getPwData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From directory:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__pwfromdirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__pwfromdirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Files (CSV):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__files_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__getpwdata_button)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        #
        return widget
        
    def __contentResultTable(self):
        """ """
        resultbox = QtGui.QGroupBox("Result table", self)
        # Active widgets and connections.
        self.__tableView = QtGui.QTableView()
        self.__tableView.setAlternatingRowColors(True)
        self.__tableView.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.__tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.__tableView.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.__tableView.verticalHeader().setDefaultSectionSize(18)
        # Model, data and selection        
        self.__model = ResultTableModel(self.__dataset)
        self.__tableView.setModel(self.__model)        
        selectionModel = QtGui.QItemSelectionModel(self.__model)
        self.__tableView.setSelectionModel(selectionModel)
        self.__tableView.resizeColumnsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__test)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__test2)
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.__tableView)
        resultbox.setLayout(layout)        
        #
        return resultbox
        
    def __contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Save data", self)
        # Active widgets and connections.
        self.__saveformat_list = QtGui.QComboBox()
        self.__saveformat_list.addItems(["Tab delimited text file (.txt)",
                                         "Excel file (.xlsx)"])
        self.__savetodirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
        self.__savetodirectory_button = QtGui.QPushButton("Browse...")
        self.__savetofile_edit = QtGui.QLineEdit("data.txt")
        self.__savedata_button = QtGui.QPushButton("Save")
####        self.connect(self.__saveformat_list, QtCore.SIGNAL("????()"), self.__????) # TODO: Switch between data.txt & data.xlsx.                
        self.connect(self.__savetodirectory_button, QtCore.SIGNAL("clicked()"), self.__saveToDirectoryBrowse)                
        self.connect(self.__savedata_button, QtCore.SIGNAL("clicked()"), self.__saveData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Format:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__saveformat_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("To directory:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__savetodirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__savetodirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__savetofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__savedata_button, gridrow, 10, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self.__savedata_button)
        #
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(form1)
#        reportlayout.addLayout(hbox1)
        saveresultbox.setLayout(reportlayout)
        #
        return saveresultbox
        
    def __textFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__textfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__textfile_edit.setText(filepath)

    def __getTextFile(self):
        """ """
        self.__dataset.clear()
        self.__refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self.__dataset = monitoring_files.TextFile()
        self.__model.setDataset(self.__dataset)
        #
        self.__dataset.readFile(unicode(self.__textfile_edit.text()))
        #        
        self.__refreshResultTable()

    def __xlsxFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__xlsxfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__xlsxfile_edit.setText(filepath)

    def __getXlsxFile(self):
        """ """
        self.__dataset.clear()
        self.__refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self.__dataset = monitoring_files.ExcelXlsxFile()
        self.__model.setDataset(self.__dataset)
        #
        self.__dataset.readFile(unicode(self.__xlsxfile_edit.text()))
        #        
        self.__refreshResultTable()
    
    def __getSharkwebData(self):
        """ """
        self.__dataset.clear()
        self.__refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self.__dataset = monitoring_files.SharkwebDownload()
        self.__model.setDataset(self.__dataset)
        #
        parameters = {}
        parameters['action'] = unicode('download_sample') # Not json
#        parameters['action'] = unicode('get_sample_table') # Json
        parameters['bounds'] = unicode('')
        parameters['year_from'] = unicode(self.__year_from_edit.text())
        parameters['year_to'] = unicode(self.__year_to_edit.text())
        parameters['month'] = unicode(self.__month_edit.text())
        parameters['datatype'] = unicode(self.__datatype_edit.text())
        parameters['parameter'] = unicode(self.__parameter_edit.text())
        parameters['project_code'] = unicode(self.__project_code_edit.text())
        parameters['orderer'] = unicode(self.__orderer_edit.text())
#        parameters['deliverer'] = unicode(self.__deliverer_edit.text()
        parameters['station_name'] = unicode(self.__station_name_edit.text())
        parameters['station_name_option'] = unicode(self.__station_name_option_edit.text())
        parameters['taxon_name'] = unicode(self.__taxon_name_edit.text())
        parameters['taxon_name_option'] = unicode(self.__taxon_name_option_edit.text())
        parameters['sample_table_view'] = unicode(self.__sample_table_view_edit.text())
        parameters['delimiters'] = unicode(self.__delimiters_edit.text())
        parameters['lineend'] = unicode(self.__lineend_edit.text())
        parameters['limit'] = unicode(self.__limit_edit.text())
        parameters['headerlang'] = unicode(self.__headerlang_edit.text())
        # Get data.
        self.__dataset.getData(parameters)
        self.__refreshResultTable()

    def __pwFromDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self.__pwfromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self.__pwfromdirectory_edit.setText(dirpath)
            self._pwsamplefiles.clear()
            # Add files in selected directory to QTableWidget.
            for row, filename in enumerate(sorted(os.listdir(unicode(self.__pwfromdirectory_edit.text())))):
                if os.path.splitext(unicode(filename))[1] in ['.csv', '.CSV']:
                    self.__files_table.setRowCount(row + 1)
                    item = QtGui.QTableWidgetItem(unicode(filename))
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.__files_table.setItem(row, 0, item)            
        
    def __getPwData(self):
        """ """
        self.__dataset.clear()
        self.__refreshResultTable()
        QtGui.QApplication.processEvents()
        #
        self.__dataset = monitoring_files.PwCsvTable()
        self.__model.setDataset(self.__dataset)
        #
        for index in range(self.__files_table.rowCount()):
            item = self.__files_table.item(index, 0)
            if item.checkState(): # Check if selected by user.
                # When reading from a table the display rule must be used.
                filename = unicode(item.data(QtCore.Qt.DisplayRole).toString())
                print(self.__pwfromdirectory_edit.text())
                print(filename)
                self.__dataset.readFile(self.__pwfromdirectory_edit.text() + '/' + filename)
        #        
        self.__refreshResultTable()

    def __saveToDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self.__savetodirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self.__savetodirectory_edit.setText(dirpath)
        
    def __saveData(self):
        """ """
        if self.__saveformat_list.currentIndex() == 0: # Text file.
            self.__dataset.SaveAsTextFile()
        elif self.__saveformat_list.currentIndex() == 1: # Xlsx file.
            self.__dataset.SaveExcelXlsxFile()
        
    def __refreshResultTable(self):
        """ """
        self.__model.reset() # Model data has changed.
        self.__tableView.resizeColumnsToContents()

    def __test(self, index):
        """ """
        print("TEST..." + "%f" % index.row())

    def __test2(self, index, index2):
        """ """
        print("TEST2..." + "%f" % index.row() + " %f" % index.column())


class ResultTableModel(QtCore.QAbstractTableModel):
    """
    """
    def __init__(self, dataset):
        """ """
        self.__dataset = dataset
        # Initialize parent.
        super(ResultTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self.__dataset = dataset

    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self.__dataset.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self.__dataset.getColumnCount()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.__dataset.getHeaderItem(section))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(self.__dataset.getDataItem(index.row(), index.column()))
        return QtCore.QVariant()

