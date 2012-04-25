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
import locale

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync

import envmonlib

class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._datasettabledata = DatasetTableData()
        self._last_used_textfile_name = ''
        self._last_used_excelfile_name = ''
        # Load available dataset parsers.
        self._parser_path = u'toolbox_data/parsers/'
        self._parser_list = []
        self._semantics_column = None # NOT USED.
        for parserpath in glob.glob(self._parser_path + u'*.xlsx'):
            print("Available parsers: " + os.path.basename(parserpath))
            self._parser_list.append(os.path.basename(parserpath))
        # Initialize parent (self._createContent will be called).
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
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._contentLoadDataset())
        contentLayout.addWidget(self._contentLoadedDatasets(), 10)
#        contentLayout.addStretch(5)
        # Style.
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
    
    def _contentLoadDataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Load dataset", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._contentTextfile(), "Text files (*.txt)")
        tabWidget.addTab(self._contentXlsx(), "Excel files (*.xlsx)")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== TEXT FILES ======
    def _contentTextfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)        
        # - Select dataset parsers:
        self._textfile_parser_list = QtGui.QComboBox()
        self._textfile_parser_list.addItems(["<select>"])
        self.connect(self._textfile_parser_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._textfileParserSelected)                
        # - Add available dataset parsers.
        self._textfile_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._textfile_importcolumn_list = QtGui.QComboBox()
        self._textfile_importcolumn_list.addItems(["<no parser selected>"])        
        # - Select export column:
        self._textfile_exportcolumn_list = QtGui.QComboBox()
        self._textfile_exportcolumn_list.addItems(["<no parser selected>"])        
        # - Select text coding.
        self._textfile_encoding_list = QtGui.QComboBox()
        self._encodings_list = [u"<auto>", 
                                u"cp1258",
                                u"windows-1258", 
                                u"utf8",
                                u"utf16",
                                u"ascii"]
        self._textfile_encoding_list.addItems(self._encodings_list)
        # Load dataset.
        self._textfile_getdataset_button = QtGui.QPushButton("Load dataset(s)...")
        self.connect(self._textfile_getdataset_button, QtCore.SIGNAL("clicked()"), self._loadTextFiles)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select parser:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel("Select import column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("Select export column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel("Dataset character encoding:")
        hbox1.addWidget(label1)
        hbox1.addWidget(self._textfile_encoding_list)
        hbox1.addStretch(10)
        hbox1.addWidget(self._textfile_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def _textfileParserSelected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._parser_list)):
            print('TEST:' + unicode(self._parser_list[selected_row - 1]) )
            
            tabledata = envmonlib.DatasetTable()
            envmonlib.ExcelFiles().readToTableDataset(tabledata, 
                                                 file_name = self._parser_path + self._parser_list[selected_row - 1])
            self._textfile_importcolumn_list.clear()
            self._textfile_exportcolumn_list.clear()
            self._semantics_column = None # NOT USED.
            header = tabledata.getHeader()
            for row in tabledata.getRows():
                if (row[0] == u"INFO") and (row[1] == u"Column type"):
                    for index, item in enumerate(row):
                        if item == u"Import":
                            self._textfile_importcolumn_list.addItems([header[index]])
                        if item == u"Export":
                            self._textfile_exportcolumn_list.addItems([header[index]])
                        if item == u"Semantics":
                            self._semantics_column = header[index] # NOT USED.
        else:
            self._textfile_importcolumn_list.clear()
            self._textfile_importcolumn_list.addItems(["no parser selected"])
            self._textfile_exportcolumn_list.clear()
            self._textfile_exportcolumn_list.addItems(["no parser selected"])

    def _loadTextFiles(self):
        """ """
        try:
            self._parent.statusBar().showMessage(u'Loading datasets...')
            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Text files (*.txt);;All files (*.*)'
            filenames = QtGui.QFileDialog.getOpenFileNames(
                                self,
                                'Load dataset(s)',
                                self._last_used_textfile_name,
                                namefilter)
            # From QString to unicode.
            filenames = map(unicode, filenames)
            # Check if user pressed ok or cancel.
            self._tabledataset = envmonlib.DatasetTable()
            if filenames:
                for filename in filenames:
                    self._last_used_textfile_name = filename
                    
                    
                    # Create a new dataset.
                    dataset = envmonlib.DatasetNode()
                    # Add info to dataset about how to import and export data to/from dataset.
                    dataset.loadDatasetParser(self._parser_path + unicode(self._textfile_parser_list.currentText()),
                                              unicode(self._textfile_importcolumn_list.currentText()),
                                              unicode(self._textfile_exportcolumn_list.currentText()),
                                              self._semantics_column)  # _semantics_column: NOT USED.
                    # Add metadata related to imported file.
                    dataset.addMetadata(u'File name', os.path.basename(filename))
                    dataset.addMetadata(u'File path', filename)
                    # Perform import.
                    impMgr = envmonlib.ImportManager()
                    if unicode(self._textfile_encoding_list.currentText()) == u'<auto>':
                        textfileencoding = locale.getpreferredencoding()
                    else:
                        textfileencoding = unicode(self._textfile_encoding_list.currentText())                        

                    impMgr.importTextFileToDataset(dataset, filename, textfileencoding)
                    # Note: Not the envmonlib datasets class. This is a wrapper containing Qt-code.
                    toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            #
        finally:
            datasetcount = len(envmonlib.Datasets().getDatasets())
            self._parent.statusBar().showMessage(
                        u'Loaded datasets: ' + unicode(datasetcount))

    # ===== EXCEL FILES ======
    def _contentXlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        # Intro:
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        # - Select dataset parser:
        self._excel_parser_list = QtGui.QComboBox()
        self._excel_parser_list.addItems(["<select>"])
        self.connect(self._excel_parser_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._excelParserSelected)                
        # - Add available dataset parsers.
        self._excel_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._excel_importcolumn_list = QtGui.QComboBox()
        self._excel_importcolumn_list.addItems(["<no parser selected>"])        
        # - Select export column:
        self._excel_exportcolumn_list = QtGui.QComboBox()
        self._excel_exportcolumn_list.addItems(["<no parser selected>"])        
        # Load dataset.
        self._excel_getdataset_button = QtGui.QPushButton("Load dataset(s)...")
        self.connect(self._excel_getdataset_button, QtCore.SIGNAL("clicked()"), self._loadExcelFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select parser:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel("Select import column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("Select export column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._excel_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _excelParserSelected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._parser_list)):
            print('TEST:' + unicode(self._parser_list[selected_row - 1]) )
            
            tabledata = envmonlib.DatasetTable()
            envmonlib.ExcelFiles().readToTableDataset(tabledata, 
                                                 file_name = self._parser_path + self._parser_list[selected_row - 1])
            self._excel_importcolumn_list.clear()
            self._excel_exportcolumn_list.clear()
            header = tabledata.getHeader()
            for row in tabledata.getRows():
                if (row[0] == u"INFO") and (row[1] == u"Column type"):
                    for index, item in enumerate(row):
                        if item == u"Import":
                            self._excel_importcolumn_list.addItems([header[index]])
                        if item == u"Export":
                            self._excel_exportcolumn_list.addItems([header[index]])
        else:
            self._excel_importcolumn_list.clear()
            self._excel_importcolumn_list.addItems(["no parser selected"])
            self._excel_exportcolumn_list.clear()
            self._excel_exportcolumn_list.addItems(["no parser selected"])

    def _loadExcelFile(self):
        """ """
        try:
            self._parent.statusBar().showMessage(u'Loading datasets...')
            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            filenames = QtGui.QFileDialog.getOpenFileNames(
                                self,
                                'Load dataset(s)',
                                self._last_used_excelfile_name,
                                namefilter)
            # From QString to unicode.
            filenames = map(unicode, filenames)
            # Check if user pressed ok or cancel.
            self._tabledataset = envmonlib.DatasetTable()
            if filenames:
                for filename in filenames:
                    self._last_used_excelfile_name = filename
                    # Create a new dataset.
                    dataset = envmonlib.DatasetNode()
                    # Add info to dataset about how to import and export data to/from dataset.
                    dataset.loadDatasetParser(self._parser_path + unicode(self._excel_parser_list.currentText()),
                                                   unicode(self._excel_importcolumn_list.currentText()),
                                                   unicode(self._excel_exportcolumn_list.currentText()))
                    # Add metadata related to imported file.
                    dataset.addMetadata(u'File name', os.path.basename(filename))
                    dataset.addMetadata(u'File path', filename)
                    # Perform import.
                    impMgr = envmonlib.ImportManager()
                    impMgr.importExcelFileToDataset(dataset, filename)
                    # Note: Not the envmonlib datasets class. This is a wrapper containing Qt-code.
                    toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        #
        finally:
            datasetcount = len(envmonlib.Datasets().getDatasets())
            self._parent.statusBar().showMessage(
                        u'Loaded datasets: ' + unicode(datasetcount))

    # ===== LOADED DATASETS =====    
    def _contentLoadedDatasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Loaded datasets", self)
        #
        self._datasets_table = utils_qt.ToolboxQTableView()
        self._datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self._datasettabledata.clear()
        self._datasettabledata.setHeader([u'Dataset      ', 
                                          u'Type         ', 
                                          u'Content      ', 
                                          u'File         ', 
                                          u'File path    ',
                                          u'parser       ',
                                          u'Import column',
                                          u'Export column'])
        self._datasets_table.tablemodel.setModeldata(self._datasettabledata)
        self._datasets_table.resizeColumnsToContents()
        
        self._datasets_table.selectionModel.Rows
        
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL("datasetListChanged"), 
             self._updateDatasetList)
        # Connection for selected row.
        self.connect(self._datasets_table.selectionModel, 
                     QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), 
                     self._selectionChanged)                
        # Buttons.
        self._unloadalldatasets_button = QtGui.QPushButton("Unload all datasets")
        self._unloadmarkeddatasets_button = QtGui.QPushButton("Unload marked dataset(s)")
        # Button connections.
        self.connect(self._unloadalldatasets_button, QtCore.SIGNAL("clicked()"), self._unloadAllDatasets)                
        self.connect(self._unloadmarkeddatasets_button, QtCore.SIGNAL("clicked()"), self._unloadMarkedDatasets)                
        # Layout widgets.
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self._unloadalldatasets_button)
        buttonlayout.addWidget(self._unloadmarkeddatasets_button)
        buttonlayout.addStretch(5)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def _unloadAllDatasets(self):
        """ """
#        # TODO: envmonlib:
#        envmonlib.Datasets().clear()

        
        toolbox_datasets.ToolboxDatasets().clear()

    def _unloadMarkedDatasets(self):
        """ """
        
        ###self.columnView.selectionModel().selection().indexes()
        ###tableView->currentIndex()
        ###tableView->selectionModel()->currentIndex()

        # Remove datasets, start with the last one. 
        rowcount = self._datasets_table.tablemodel.rowCount()
        for rowindex in range(rowcount):
#            item = self._datasets_table.item(rowcount - rowindex - 1, 0)
#            if item.checkState(): # Check if selected by user.
            if self._datasets_table.selectionModel.isSelected(self._datasets_table.tablemodel.createIndex(rowindex, 0)): # Check if selected by user.
                # TODO: envmonlib:
                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

                
#                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

    def _updateDatasetList(self):
        """ """
        
        
        # TODO: envmonlib:
        self._datasettabledata.clearRows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            # Get content info depending on dataset type.
            datasettype = u'',
            contentinfo = u''
            if isinstance(dataset, envmonlib.DatasetTable):
                datasettype = u'Table dataset'
                contentinfo = u'Rows: ' + unicode(len(dataset.getRows())) + u'. '
            elif isinstance(dataset, envmonlib.DatasetNode):
                datasettype = u'Tree dataset'
                visitcount, samplecound, variablecount = dataset.getCounters()
                contentinfo = u'Visits: ' + unicode(visitcount) + u', ' + \
                              u'samples: ' + unicode(samplecound) + u', ' + \
                              u'variables: ' + unicode(variablecount) + u'. '
            else:
                datasettype = u'Unspecified'

            # Add row 
            self._datasettabledata.addRow(
                [u'Dataset-' + unicode(rowindex),
                 datasettype,
                 contentinfo,
                 dataset.getMetadata(u'File name'),
                 dataset.getMetadata(u'File path'),
                 dataset.getMetadata(u'parser'),
                 dataset.getMetadata(u'Import column'),
                 dataset.getMetadata(u'Export column')])
            #
        self._datasets_table.tablemodel.reset()
        self._datasets_table.resizeColumnsToContents()





#        self._datasettabledata.clearRows()
#        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
#            self._datasettabledata.addRow([u'Dataset-' + unicode(rowindex) + '                                       '])
#        self._datasets_table.tablemodel.reset()
#        self._datasets_table.resizeColumnsToContents()
    
    def _selectionChanged(self, modelIndex):
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

