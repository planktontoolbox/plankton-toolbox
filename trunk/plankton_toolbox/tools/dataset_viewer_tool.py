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
Template for new tools.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.tools.tool_base as tool_base

class DatasetViewerTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DatasetViewerTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentResultTable())
        contentLayout.addWidget(self.__contentSaveResult())
#        contentLayout.addStretch(5)

    def __contentResultTable(self):
        """ """
#        resultbox = QtGui.QGroupBox("Result table", self)
        # Active widgets and connections.
        self.__selectdataset_list = QtGui.QComboBox()
        self.__selectdataset_list.addItems(["<select loaded dataset>"])
        # TODO: connect...
        
        self.__tableview = QtGui.QTableView()
        self.__tableview.setAlternatingRowColors(True)
        self.__tableview.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.__tableview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.__tableview.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.__tableview.verticalHeader().setDefaultSectionSize(18)
        # Model, data and selection        
####################        self.__model = ResultTableModel(self.__dataset)
####################        self.__tableview.setModel(self.__model)        
####################        selectionModel = QtGui.QItemSelectionModel(self.__model)
####################        self.__tableview.setSelectionModel(selectionModel)
####################        self.__tableview.resizeColumnsToContents()
####################        #
####################        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__test)
####################        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__test2)
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.__selectdataset_list)
        layout.addWidget(self.__tableview)
#        resultbox.setLayout(layout)        
        #
#        return resultbox
        return layout
        
    def __contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Save dataset", self)
        # Active widgets and connections.
        self.__saveformat_list = QtGui.QComboBox()

        self.__savetofile_edit = QtGui.QLineEdit("dataset.txt")
        self.__browse_button = QtGui.QPushButton("Browse...")
        self.__saveformat_list.addItems(["Tab delimited text file (.txt)",
                                         "Excel file (.xlsx)"])
        self.__savedataset_button = QtGui.QPushButton("Save")

#        self.__saveformat_list.addItems(["Tab delimited text file (.txt)",
#                                         "Excel file (.xlsx)"])
#        self.__savetodirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
#        self.__savetofile_edit = QtGui.QLineEdit("data.txt")
#        self.__savedata_button = QtGui.QPushButton("Save")
####        self.connect(self.__saveformat_list, QtCore.SIGNAL("????()"), self.__????) # TODO: Switch between data.txt & data.xlsx.                
#        self.connect(self.__savetodirectory_button, QtCore.SIGNAL("clicked()"), self.__saveToDirectoryBrowse)                
        self.connect(self.__savedataset_button, QtCore.SIGNAL("clicked()"), self.__saveData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("To file:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__savetofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__browse_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Format:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__saveformat_list, gridrow, 1, 1, 2)
        form1.addWidget(self.__savedataset_button, gridrow, 10, 1, 1)
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






#            # Filepath.            
#            reportfilepath = ''
#            if len(unicode(self.__todirectory_edit.text())) > 0:
#                reportfilepath = unicode(self.__todirectory_edit.text()) + '/'
#            reportfilepath += unicode(self.__tofile_edit.text())
        
        
        
        
        
        
        
        
        filename = self.__savetodirectory_edit.text()  + '/' + \
                   self.__savetofile_edit.text()
        if self.__saveformat_list.currentIndex() == 0: # Text file.
            self.__dataset.SaveAsTextFile(unicode(filename))
        elif self.__saveformat_list.currentIndex() == 1: # Xlsx file.
            self.__dataset.SaveExcelXlsxFile(unicode(filename))
        
    def __refreshResultTable(self):
        """ """
        self.__model.reset() # Model data has changed.
        self.__tableview.resizeColumnsToContents()

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

