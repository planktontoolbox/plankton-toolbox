#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
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
"""

import os.path
import glob

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync

import mmfw

class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self.__datasettabledata = DatasetTableData()
        self.__last_used_textfile_name = ''
        self.__last_used_excelfile_name = ''
        # Load available import/export matrices.
        self._matrix_path = u'mmfw_data/matrices/'
        self._matrix_list = []
        for matrixpath in glob.glob(self._matrix_path + u'*.xlsx'):
            print("Available matrix: " + os.path.basename(matrixpath))
            self._matrix_list.append(os.path.basename(matrixpath))
        # Initialize parent (self._createContent will be called).
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)        

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self.__activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self.__activityheader.setTextFormat(QtCore.Qt.RichText)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self.__activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self.__contentLoadDataset())
        contentLayout.addWidget(self.__contentLoadedDatasets(), 10)
#        contentLayout.addStretch(5)
        # Style.
        self.__activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
    
    def __contentLoadDataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Load dataset", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.__contentTextfile(), "Text files (*.txt)")
        tabWidget.addTab(self.__contentXlsx(), "Excel files (*.xlsx)")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== TEXT FILES ======
    def __contentTextfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)        
        # - Select import/export matrix:
        self.__textfile_matrix_list = QtGui.QComboBox()
        self.__textfile_matrix_list.addItems(["<select>"])
        self.connect(self.__textfile_matrix_list, QtCore.SIGNAL("currentIndexChanged(int)"), self.__textfileMatrixSelected)                
        # - Add available matrices.
        self.__textfile_matrix_list.addItems(self._matrix_list)                
        # - Select import column:
        self.__textfile_importcolumn_list = QtGui.QComboBox()
        self.__textfile_importcolumn_list.addItems(["<no matrix selected>"])        
        # - Select export column:
        self.__textfile_exportcolumn_list = QtGui.QComboBox()
        self.__textfile_exportcolumn_list.addItems(["<no matrix selected>"])        
        # - Select text coding.
        self.__textfile_encoding_list = QtGui.QComboBox()
        self.__encodings_dict = {u"Windows-1252/CP-1252": u'CP-1252', 
                                 u"UTF-8": u'UTF-8',
                                 u"UTF-16/UCS-2)": u'UTF-16',
                                 u"UTF-16BE": u'UTF-16BE',
                                 u"UTF-16LE": u'UTF-16LE',
                                 u"ANSI": u'ANSI'}
        self.__textfile_encoding_list.addItems(self.__encodings_dict.keys())
        # Load dataset.
        self.__textfile_getdataset_button = QtGui.QPushButton("Load dataset(s)...")
        self.connect(self.__textfile_getdataset_button, QtCore.SIGNAL("clicked()"), self.__loadTextFiles)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select matrix:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__textfile_matrix_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel("Select import column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__textfile_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("Select export column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__textfile_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel("Dataset character encoding:")
        hbox1.addWidget(label1)
        hbox1.addWidget(self.__textfile_encoding_list)
        hbox1.addStretch(10)
        hbox1.addWidget(self.__textfile_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def __textfileMatrixSelected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._matrix_list)):
            print('TEST:' + unicode(self._matrix_list[selected_row - 1]) )
            
            tabledata = mmfw.DatasetTable()
            mmfw.ExcelFiles().readToTableDataset(tabledata, 
                                                 file_name = self._matrix_path + self._matrix_list[selected_row - 1])
            self.__textfile_importcolumn_list.clear()
            self.__textfile_exportcolumn_list.clear()
            self.__semantics_column = None
            header = tabledata.getHeader()
            for row in tabledata.getRows():
                if (row[0] == u"INFO") and (row[1] == u"Column type"):
                    for index, item in enumerate(row):
                        if item == u"Import":
                            self.__textfile_importcolumn_list.addItems([header[index]])
                        if item == u"Export":
                            self.__textfile_exportcolumn_list.addItems([header[index]])
                        if item == u"Semantics":
                            self.__semantics_column = header[index]
        else:
            self.__textfile_importcolumn_list.clear()
            self.__textfile_importcolumn_list.addItems(["no matrix selected"])
            self.__textfile_exportcolumn_list.clear()
            self.__textfile_exportcolumn_list.addItems(["no matrix selected"])

    def __loadTextFiles(self):
        """ """
        self._parent.statusBar().showMessage(u'Loading datasets...')
        # Show select file dialog box. Multiple files can be selected.
        namefilter = 'Text files (*.txt);;All files (*.*)'
        filenames = QtGui.QFileDialog.getOpenFileNames(
                            self,
                            'Load dataset(s)',
                            self.__last_used_textfile_name,
                            namefilter)
        # From QString to unicode.
        filenames = map(unicode, filenames)
        # Check if user pressed ok or cancel.
        self.__tabledataset = mmfw.DatasetTable()
        if filenames:
            for filename in filenames:
                self.__last_used_textfile_name = filename
                
                
                # Create a new dataset.
                dataset = mmfw.DatasetNode()
                # Add info to dataset about how to import and export data to/from dataset.
                dataset.loadImportExportMatrix(self._matrix_path + unicode(self.__textfile_matrix_list.currentText()),
                                               unicode(self.__textfile_importcolumn_list.currentText()),
                                               unicode(self.__textfile_exportcolumn_list.currentText()),
                                               self.__semantics_column)
                # Add metadata related to imported file.
                dataset.addMetadata(u'File name', os.path.basename(filename))
                dataset.addMetadata(u'File path', filename)
                # Perform import.
                impMgr = mmfw.ImportManager()
                impMgr.importFileToDataset(dataset, filename)
                # Note: Not the mmfw datasets class. This is a wrapper containing Qt-code.
                toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        #
        datasetcount = len(mmfw.Datasets().getDatasets())
        self._parent.statusBar().showMessage(
                    u'Loaded datasets: ' + unicode(datasetcount))

    # ===== EXCEL FILES ======
    def __contentXlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        # Intro:
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        # - Select import/export matrix:
        self.__excel_matrix_list = QtGui.QComboBox()
        self.__excel_matrix_list.addItems(["<select>"])
        self.connect(self.__excel_matrix_list, QtCore.SIGNAL("currentIndexChanged(int)"), self.__excelMatrixSelected)                
        # - Add available matrices.
        self.__excel_matrix_list.addItems(self._matrix_list)                
        # - Select import column:
        self.__excel_importcolumn_list = QtGui.QComboBox()
        self.__excel_importcolumn_list.addItems(["<no matrix selected>"])        
        # - Select export column:
        self.__excel_exportcolumn_list = QtGui.QComboBox()
        self.__excel_exportcolumn_list.addItems(["<no matrix selected>"])        
        # Load dataset.
        self.__excel_getdataset_button = QtGui.QPushButton("Load dataset(s)...")
        self.connect(self.__excel_getdataset_button, QtCore.SIGNAL("clicked()"), self.__loadExcelFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select matrix:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_matrix_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel("Select import column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("Select export column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.__excel_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def __excelMatrixSelected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._matrix_list)):
            print('TEST:' + unicode(self._matrix_list[selected_row - 1]) )
            
            tabledata = mmfw.DatasetTable()
            mmfw.ExcelFiles().readToTableDataset(tabledata, 
                                                 file_name = self._matrix_path + self._matrix_list[selected_row - 1])
            self.__excel_importcolumn_list.clear()
            self.__excel_exportcolumn_list.clear()
            header = tabledata.getHeader()
            for row in tabledata.getRows():
                if (row[0] == u"INFO") and (row[1] == u"Column type"):
                    for index, item in enumerate(row):
                        if item == u"Import":
                            self.__excel_importcolumn_list.addItems([header[index]])
                        if item == u"Export":
                            self.__excel_exportcolumn_list.addItems([header[index]])
        else:
            self.__excel_importcolumn_list.clear()
            self.__excel_importcolumn_list.addItems(["no matrix selected"])
            self.__excel_exportcolumn_list.clear()
            self.__excel_exportcolumn_list.addItems(["no matrix selected"])

    def __loadExcelFile(self):
        """ """
        self._parent.statusBar().showMessage(u'Loading datasets...')
        # Show select file dialog box. Multiple files can be selected.
        namefilter = 'Excel files (*.xlsx);;All files (*.*)'
        filenames = QtGui.QFileDialog.getOpenFileNames(
                            self,
                            'Load dataset(s)',
                            self.__last_used_excelfile_name,
                            namefilter)
        # From QString to unicode.
        filenames = map(unicode, filenames)
        # Check if user pressed ok or cancel.
        self.__tabledataset = mmfw.DatasetTable()
        if filenames:
            for filename in filenames:
                self.__last_used_excelfile_name = filename
                # Create a new dataset.
                dataset = mmfw.DatasetNode()
                # Add info to dataset about how to import and export data to/from dataset.
                dataset.loadImportExportMatrix(self._matrix_path + unicode(self.__excel_matrix_list.currentText()),
                                               unicode(self.__excel_importcolumn_list.currentText()),
                                               unicode(self.__excel_exportcolumn_list.currentText()))
                # Add metadata related to imported file.
                dataset.addMetadata(u'File name', os.path.basename(filename))
                dataset.addMetadata(u'File path', filename)
                # Perform import.
                impMgr = mmfw.ImportManager()
                impMgr.importExcelFileToDataset(dataset, filename)
                # Note: Not the mmfw datasets class. This is a wrapper containing Qt-code.
                toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        #
        datasetcount = len(mmfw.Datasets().getDatasets())
        self._parent.statusBar().showMessage(
                    u'Loaded datasets: ' + unicode(datasetcount))

    # ===== LOADED DATASETS =====    
    def __contentLoadedDatasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Loaded datasets", self)
        #
        self.__datasets_table = utils_qt.ToolboxQTableView()
        self.__datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.__datasettabledata.clear()
        self.__datasettabledata.setHeader([u'Dataset      ', 
                                           u'Type         ', 
                                           u'Content      ', 
                                           u'File         ', 
                                           u'File path    ',
                                           u'Matrix       ',
                                           u'Import column',
                                           u'Export column'])
        self.__datasets_table.tablemodel.setModeldata(self.__datasettabledata)
        self.__datasets_table.resizeColumnsToContents()
        
        self.__datasets_table.selectionModel.Rows
        
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL("datasetListChanged"), 
             self.__updateDatasetList)
        # Connection for selected row.
        self.connect(self.__datasets_table.selectionModel, 
                     QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), 
                     self.__selectionChanged)                
        # Buttons.
        self.__unloadalldatasets_button = QtGui.QPushButton("Unload all datasets")
        self.__unloadmarkeddatasets_button = QtGui.QPushButton("Unload marked dataset(s)")
        # Button connections.
        self.connect(self.__unloadalldatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadAllDatasets)                
        self.connect(self.__unloadmarkeddatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadMarkedDatasets)                
        # Layout widgets.
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self.__unloadalldatasets_button)
        buttonlayout.addWidget(self.__unloadmarkeddatasets_button)
        buttonlayout.addStretch(5)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self.__datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def __unloadAllDatasets(self):
        """ """
#        # TODO: MMFW:
#        mmfw.Datasets().clear()

        
        toolbox_datasets.ToolboxDatasets().clear()

    def __unloadMarkedDatasets(self):
        """ """
        
        ###self.columnView.selectionModel().selection().indexes()
        ###tableView->currentIndex()
        ###tableView->selectionModel()->currentIndex()

        # Remove datasets, start with the last one. 
        rowcount = self.__datasets_table.tablemodel.rowCount()
        for rowindex in range(rowcount):
#            item = self.__datasets_table.item(rowcount - rowindex - 1, 0)
#            if item.checkState(): # Check if selected by user.
            if self.__datasets_table.selectionModel.isSelected(self.__datasets_table.tablemodel.createIndex(rowindex, 0)): # Check if selected by user.
                # TODO: MMFW:
                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

                
#                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

    def __updateDatasetList(self):
        """ """
        
        
        # TODO: MMFW:
        self.__datasettabledata.clearRows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            # Get content info depending on dataset type.
            datasettype = u'',
            contentinfo = u''
            if isinstance(dataset, mmfw.DatasetTable):
                datasettype = u'Table dataset'
                contentinfo = u'Rows: ' + unicode(len(dataset.getRows())) + u'. '
            elif isinstance(dataset, mmfw.DatasetNode):
                datasettype = u'Tree dataset'
                visitcount, samplecound, variablecount = dataset.getCounters()
                contentinfo = u'Visits: ' + unicode(visitcount) + u', ' + \
                              u'samples: ' + unicode(samplecound) + u', ' + \
                              u'variables: ' + unicode(variablecount) + u'. '
            else:
                datasettype = u'Unspecified'

            # Add row 
            self.__datasettabledata.addRow(
                [u'Dataset-' + unicode(rowindex),
                 datasettype,
                 contentinfo,
                 dataset.getMetadata(u'File name'),
                 dataset.getMetadata(u'File path'),
                 dataset.getMetadata(u'Matrix'),
                 dataset.getMetadata(u'Import column'),
                 dataset.getMetadata(u'Export column')])
            #
        self.__datasets_table.tablemodel.reset()
        self.__datasets_table.resizeColumnsToContents()





#        self.__datasettabledata.clearRows()
#        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
#            self.__datasettabledata.addRow([u'Dataset-' + unicode(rowindex) + '                                       '])
#        self.__datasets_table.tablemodel.reset()
#        self.__datasets_table.resizeColumnsToContents()
    
    def __selectionChanged(self, modelIndex):
        """ """
        if modelIndex.isValid():
            print('TEST Selected row: ' + unicode(modelIndex.row()))
            toolbox_sync.ToolboxSync().setRowTest(modelIndex.row())

    
class DatasetTableData(object):
    """ """
    def __init__(self):
        """ """
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def clearRows(self):
        """ """
        self._rows = []

    def setHeader(self, header):
        """ """
        self._header = header

    def addRow(self, row):
        """ """
        self._rows.append(row)

    def getHeaderItem(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def getDataItem(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def getColumnCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return ''

    def getRowCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return ''

