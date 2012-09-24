#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
This module contains GUI-related utilities for the Plankton Toolbox project.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

class RichTextQLabel(QtGui.QLabel):  
    """ Customized QLabel. Used for informative texts. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setTextFormat(QtCore.Qt.RichText)
        self.setOpenExternalLinks(True) 
        self.setWordWrap(True)
#        self.setStyleSheet(""" 
#            * { color: white; background-color: #00677f; }
#            """)

class HeaderQLabel(QtGui.QLabel):  
    """ Customized QLabel. Used for informative texts. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setTextFormat(QtCore.Qt.RichText)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        
#    def setHeaderText(self, text):
#        """ """ 
#        self.setText(text)

class ClickableQLabel(QtGui.QLabel):  
    """ Customized QLabel. Emits signal when clicked, and change color when hovering. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        # Set style.
        self.setProperty("ActivityStatus", "Unselected")  ### TODO: Remove this when stylesheet fixed.
        self.updateStyleSheet()
  
    def mouseReleaseEvent(self, ev):  
        self.emit(QtCore.SIGNAL('clicked()'))  
  
    def enterEvent(self, ev):
        self.setStyleSheet(""" 
/*            * [ActivityStatus="Selected"] { color: #d1581c; background-color: #eaa97e; }
*/
            * [ActivityStatus="Selected"] { color: #d1581c; background-color: #6da8bd; }
            * [ActivityStatus="Unselected"] { color: #d1581c; background-color: white; }
            """)
  
    def leaveEvent(self, ev):  
        self.setStyleSheet(""" 
/*            * [ActivityStatus="Selected"] { color: #00677f; background-color: #eaa97e; }
*/
            * [ActivityStatus="Selected"] { color: white; background-color: #6da8bd; }
            * [ActivityStatus="Unselected"] { color: #00677f; background-color: white; }
            """)

    def updateStyleSheet(self):  
        self.setStyleSheet(""" 
/*            * [ActivityStatus="Selected"] { color:  #00677f; background-color: #eaa97e; }
*/
            * [ActivityStatus="Selected"] { color:  white; background-color: #6da8bd; }
            * [ActivityStatus="Unselected"] { color:  #00677f; background-color: white; }
            """)


class ActivityMenuQLabel(ClickableQLabel):  
    """ Customized QLabel. Contains a list of all ActivityMenuQLabel objects. Only one is marked as active.  """
    # Static variable:
    activityitems = []
    
    def __init__(self, parent = None):  
        ClickableQLabel.__init__(self, parent)
        # Add to static variable:
        self.activityitems.append(self)
        self.markAsUnselected()
        
    def markAsSelected(self):
        """ """
        # Mark all others as unselected.
        for label in self.activityitems:
            label.markAsUnselected() 
        # Mark this as selected.
        self.setProperty("ActivityStatus", "Selected")
        self.updateStyleSheet()
          
    def markAsUnselected(self):
        """ """
        self.setProperty("ActivityStatus", "Unselected")
        self.updateStyleSheet()


class SelectableQListView(QtGui.QListView):  
    """ Customized QListView. Contains a single column and corresponding checkboxes. """
    def __init__(self, parent = None):
        """ """
        QtGui.QListView.__init__(self, parent)
        self.tablemodel = QtGui.QStandardItemModel()
        self.setModel(self.tablemodel)

    def clear(self):
        """ """
        self.tablemodel.clear()        
         
    def setList(self, data_list = None, default_check_state = True):
        """ """
        self.tablemodel.clear()        
        for tableitem in data_list:
            standarditem = QtGui.QStandardItem(tableitem)
            standarditem.setCheckState(QtCore.Qt.Checked)
            standarditem.setCheckable(default_check_state)
            self.tablemodel.appendRow(standarditem)
         
    def checkAll(self):
        """ """
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def uncheckAll(self):
        """ """
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def getSelectedDataList(self):
        """ """
        selecteddata = []
        self._selected_data_list = []
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selecteddata.append(unicode(item.text()))
        #
        return selecteddata

    def getNotSelectedDataList(self):
        """ """
        selecteddata = []
        self._selected_data_list = []
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            if item.checkState() != QtCore.Qt.Checked:
                selecteddata.append(unicode(item.text()))
        #
        return selecteddata

    def getSelectedIndexList(self):
        """ """
        selectedindexes = []
        self._selected_data_list = []
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedindexes.append(rowindex)
        #
        return selectedindexes

    def getNotSelectedIndexList(self):
        """ """
        selectedindexes = []
        self._selected_data_list = []
        for rowindex in range(self.tablemodel.rowCount()):
            item = self.tablemodel.item(rowindex, 0)
            if item.checkState() != QtCore.Qt.Checked:
                selectedindexes.append(rowindex)
        #
        return selectedindexes


class ToolboxQTableView( QtGui.QTableView):  
    """ Customized QTableView. The table is automatically connected to an 
        instance of ToolboxTableModel.  """
    def __init__(self, parent = None):
        """ """
        QtGui.QTableView.__init__(self, parent)
        self.tablemodel = None # Note: Public. 
        self.selectionModel = None # Note: Public. 
        
        # Default setup for tables.
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.verticalHeader().setDefaultSectionSize(18)
        # Default model, data and selection        
        self.tablemodel = ToolboxTableModel()
        self.setModel(self.tablemodel)
        self.selectionModel = QtGui.QItemSelectionModel(self.tablemodel)
        self.setSelectionModel(self.selectionModel)
        self.resizeColumnsToContents()
          
    def clear(self):
        """ """
        self.selectionModel.clear()
        # Call same method in parent class.
        super(ToolboxQTableView, self).clear()
        
    def setTablemodel(self, model):
        """ Use this method if the default model should be replaced. """
        self.tablemodel = model
        self.setModel(self.tablemodel)
        self.selectionModel = QtGui.QItemSelectionModel(self.tablemodel)
        self.setSelectionModel(self.selectionModel)
        self.resizeColumnsToContents()

class ToolboxTableModel(QtCore.QAbstractTableModel):
    """ """
    def __init__(self, modeldata = None):
        """ """
        self._modeldata = modeldata
        # Initialize parent.
        QtCore.QAbstractTableModel.__init__(self)
        
    def setModeldata(self, modeldata):
        """ """
        self._modeldata = modeldata
        self.reset() 

    def getModeldata(self):
        """ """
        return self._modeldata

    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self._modeldata == None:
            return 0
        return self._modeldata.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self._modeldata == None:
            return 0
        return self._modeldata.getColumnCount()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if self._modeldata == None:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._modeldata.getHeaderItem(section))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if self._modeldata == None:
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(self._modeldata.getDataItem(index.row(), index.column()))
        return QtCore.QVariant()


class ToolboxEditableQTableView( QtGui.QTableView):  
    """ Customized QTableView for editing. The table is automatically connected to an 
        instance of ToolboxEditableTableModel.  """
    def __init__(self, parent = None):
        """ """
        QtGui.QTableView.__init__(self, parent)
        self.tablemodel = None # Note: Public. 
        self.selectionModel = None # Note: Public. 
        
        # Default setup for tables.
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.verticalHeader().setDefaultSectionSize(18)
        # Default model, data and selection        
        self.tablemodel = ToolboxEditableTableModel()
        self.setModel(self.tablemodel)
        self.selectionModel = QtGui.QItemSelectionModel(self.tablemodel)
        self.setSelectionModel(self.selectionModel)
        self.resizeColumnsToContents()
          
    def clear(self):
        """ """
        self.selectionModel.clear()
        # Call same method in parent class.
        super(ToolboxQTableView, self).clear()
        
    def setTablemodel(self, model):
        """ Use this method if the default model should be replaced. """
        self.tablemodel = model
        self.setModel(self.tablemodel)
        self.selectionModel = QtGui.QItemSelectionModel(self.tablemodel)
        self.setSelectionModel(self.selectionModel)
        self.resizeColumnsToContents()

class ToolboxEditableTableModel(QtCore.QAbstractTableModel):
    """ Table model for editing. """
    def __init__(self, modeldata = None):
        """ """
        self._modeldata = modeldata
        # Initialize parent.
        QtCore.QAbstractTableModel.__init__(self)
        
    def setModeldata(self, modeldata):
        """ """
        self._modeldata = modeldata
        self.reset() 

    def getModeldata(self):
        """ """
        return self._modeldata

    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self._modeldata == None:
            return 0
        return self._modeldata.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self._modeldata == None:
            return 0
        return self._modeldata.getColumnCount()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if self._modeldata == None:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._modeldata.getHeaderItem(section))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if self._modeldata == None:
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(self._modeldata.getDataItem(index.row(), index.column()))
        return QtCore.QVariant()

    # For editing:
    def setData(self, index, value, role):
        """ """
        try:        
            self._modeldata.setDataItem(index.row(), index.column(), unicode(value.toString()))
            return True
        except:
            return False

    # For editing:
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable



# === Style sheets: ===

# Nordic Microalgae colors:
#    Red: #d1581c
#    Blue: #00677f
#    Green: #89a45e
#    Red 50%: #eaa97e
#    Blue 50%: (#6da88d) #6da8bd 
#    Green 50%: #cbd1aa
#    Red 25%: #f5d5bd
#    Blue 25%: #b7d3de
#    Green 30%: #e0e3cd
         
#def setAppStyleSheet(app):
#    app.setStyleSheet("""
#        /* Default for all dock widgets.*/
#
#
#        /* QWidget, QWidget *  { color: black; background-color: #ffffff; }
#        */
#
#        QDockWidget, QDockWidget *  { color: black; background-color: #eeeeee; }
#        QDockWidget QPushButton:hover { color: #d1581c; }
#        
#        /* Default for all widgets used in tools. */        
#        ToolBase, ToolBase * { color: black; background-color: #eeeeee; } 
#        ToolBase QPushButton:hover { color: #d1581c; } 
#
#        /* Default for all widgets used in activities. */        
#        ActivityBase, ActivityBase * { color: black; background-color: #ffffff; } 
#        ActivityBase QPushButton:hover { color: #d1581c; } 
#        
#        QStatusBar { background-color: #eeeeee; }
#        
#        QLineEdit { background-color: #f8f8f8; }
#        
#        """)

#        QAbstractButton, 
#        QAbstractSlider, 
#        QAbstractSpinBox, 
#        QAxWidget, 
#        QCalendarWidget, 
#        QComboBox, 
#        QDesignerActionEditorInterface, 
#        QDesignerFormWindowInterface, 
#        QDesignerObjectInspectorInterface, 
#        QDesignerPropertyEditorInterface, 
#        QDesignerWidgetBoxInterface, 
#        QDesktopWidget, 
#        QDialog, 
#        QDialogButtonBox, 
#        QDockWidget, 
#        QFocusFrame, 
#        QFrame, 
#        QGLWidget, 
#        QGroupBox, 
#        QHelpSearchQueryWidget, 
#        QHelpSearchResultWidget, 
#        QLineEdit, 
#        QMainWindow, 
#        QMdiSubWindow, 
#        QMenu, 
#        QMenuBar, 
#        QPrintPreviewWidget, 
#        QProgressBar, 
#        QRubberBand, 
#        QSizeGrip, 
#        QSplashScreen, 
#        QSplitterHandle, 
#        QStatusBar, 
#        QSvgWidget, 
#        QTabBar, 
#        QTabWidget, 
#        QToolBar, 
#        QWebView, 
#        QWizardPage, 
#        QWorkspace 

def setAppStyleSheet(app):
    app.setStyleSheet("""
        
/*        QDockWidget .QWidget { background-color: whitesmoke; }
*/
        QAbstractButton:hover { color: #d1581c; }
        
        """)
