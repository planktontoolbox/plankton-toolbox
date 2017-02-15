#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""
This module contains GUI-related toolbox_utils for the Plankton Toolbox project.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_core

__version__ = '' 

def set_version(version):
        """ """
        global __version__
        __version__ = version

class RichTextQLabel(QtGui.QLabel):  
    """ Customized QLabel. Used for informative texts. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setTextFormat(QtCore.Qt.RichText)
        self.setOpenExternalLinks(True) 
        self.setWordWrap(True)

class HeaderQLabel(QtGui.QLabel):  
    """ Customized QLabel. Used for informative texts. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setTextFormat(QtCore.Qt.RichText)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setStyleSheet(""" 
            * { color: white; background-color: black; }
            """)
        
class RightAlignedQLabel(QtGui.QLabel):  
    """ Customized QLabel. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
 
class CenterAlignedQLabel(QtGui.QLabel):  
    """ Customized QLabel. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

class LeftAlignedQLabel(QtGui.QLabel):  
    """ Customized QLabel. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

class ClickableQLabel(QtGui.QLabel):  
    """ Customized QLabel. Emits signal when clicked, and change color when hovering. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)  
        # Set style.
        self.setProperty('ActivityStatus', 'Unselected')  ### TODO: Remove this when stylesheet fixed.
        self.updateStyleSheet()
  
    def mouseReleaseEvent(self, ev):  
        """ Overridden abstract method. """
        self.emit(QtCore.SIGNAL('clicked()'))  
  
    def enterEvent(self, ev):
        """ Overridden abstract method. """
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color: #d1581c; background-color: #6da8bd; }
            * [ActivityStatus="Unselected"] { color: #d1581c; background-color: white; }
            """)
  
    def leaveEvent(self, ev):  
        """ Overridden abstract method. """
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color: white; background-color: black; }
            * [ActivityStatus="Unselected"] { color: black; background-color: white; }
            """)

    def updateStyleSheet(self):  
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color:  white; background-color: black; }
            * [ActivityStatus="Unselected"] { color:  black; background-color: white; }
            """)


class ClickableLinkQLabel(QtGui.QLabel):  
    """ Customized QLabel. Emits signal when clicked, and change color when hovering. """
    def __init__(self, parent = None):  
        QtGui.QLabel.__init__(self, parent)
        #  
        self.setStyleSheet(""" 
            * { color: black; }
            """)
  
    def mouseReleaseEvent(self, ev):  
        """ Overridden abstract method. """
        self.emit(QtCore.SIGNAL('clicked()'))  
  
    def enterEvent(self, ev):
        """ Overridden abstract method. """
        self.setStyleSheet(""" 
            * { color: #d1581c; }
            """)
  
    def leaveEvent(self, ev):  
        """ Overridden abstract method. """
        self.setStyleSheet(""" 
            * { color: black; }
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
        self.setProperty('ActivityStatus', 'Selected')
        self.updateStyleSheet()
          
    def markAsUnselected(self):
        """ """
        self.setProperty('ActivityStatus', 'Unselected')
        self.updateStyleSheet()


class SelectableQListView(QtGui.QListView):  
    """ Customized QListView. Contains a single column and corresponding checkboxes. """
    def __init__(self, parent = None):
        """ """
        QtGui.QListView.__init__(self, parent)
        self._tablemodel = QtGui.QStandardItemModel()
        self.setModel(self._tablemodel)

    def clear(self):
        """ """
        self._tablemodel.clear()        
         
    def setList(self, data_list = None, default_check_state = True):
        """ """
        self._tablemodel.clear()        
        for tableitem in data_list:
            standarditem = QtGui.QStandardItem(tableitem)
            standarditem.setCheckState(QtCore.Qt.Checked)
            standarditem.setCheckable(default_check_state)
            self._tablemodel.appendRow(standarditem)
         
    def checkAll(self):
        """ """
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def uncheckAll(self):
        """ """
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def getSelectedDataList(self):
        """ """
        selecteddata = []
        self._selected_data_list = []
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selecteddata.append(unicode(item.text()))
        #
        return selecteddata

    def getNotSelectedDataList(self):
        """ """
        selecteddata = []
        self._selected_data_list = []
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            if item.checkState() != QtCore.Qt.Checked:
                selecteddata.append(unicode(item.text()))
        #
        return selecteddata

    def getSelectedIndexList(self):
        """ """
        selectedindexes = []
        self._selected_data_list = []
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedindexes.append(rowindex)
        #
        return selectedindexes

    def getNotSelectedIndexList(self):
        """ """
        selectedindexes = []
        self._selected_data_list = []
        for rowindex in range(self._tablemodel.rowCount()):
            item = self._tablemodel.item(rowindex, 0)
            if item.checkState() != QtCore.Qt.Checked:
                selectedindexes.append(rowindex)
        #
        return selectedindexes


class ToolboxQTableView( QtGui.QTableView):  
    """ Customized QTableView. The table is automatically connected to an 
        instance of ToolboxTableModel.  """
    def __init__(self, parent = None, filter_column_index = None):
        """ """
        QtGui.QTableView.__init__(self, parent)
        self._tablemodel = ToolboxTableModel(modeldata = plankton_core.DatasetTable())
        self._selectionmodel = None # Created below.
        # Connect models.
        if filter_column_index is None:
            self.setModel(self._tablemodel)
            #
            self._selectionmodel = QtGui.QItemSelectionModel(self._tablemodel) 
            self.setSelectionModel(self._selectionmodel)
            self.resizeColumnsToContents()
        else:
            """ Use this method if the default model should be replaced by a filtered model. """
            # Filter proxy model.
            self.filterproxymodel = QtGui.QSortFilterProxyModel(self)
            self.filterproxymodel.setSourceModel(self._tablemodel)
            self.filterproxymodel.setFilterKeyColumn(filter_column_index)
            self.setModel(self.filterproxymodel)
            #
            self._selectionmodel = QtGui.QItemSelectionModel(self.filterproxymodel) 
            self.setSelectionModel(self._selectionmodel)
            self.resizeColumnsToContents()        
        # Default setup for tables.
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
#         self.verticalHeader().setDefaultSectionSize(18)
           
    def clearModel(self):
        """ """
        if self._tablemodel.getModeldata():
            self._tablemodel.getModeldata().clear()
#         # Call same method in parent class.
#         super(ToolboxQTableView, self).clear()
          
    def resetModel(self):
        """ Used to repaint. """
        if self._tablemodel:
            self._tablemodel.reset()
          
    def getTableModel(self):
        """ """
        return self._tablemodel.getModeldata()
          
    def setTableModel(self, tablemodeldata):
        """ """
        self._tablemodel.setModeldata(tablemodeldata)
          
    def getSelectionModel(self):
        """ """
        return self._selectionmodel
          
    def onFilterTextChanged(self, text):
        """ link the textChanged signal to this method for filtering. 
            In the constructor 'filter_column_index' must be defined. """          
        filterString = QtCore.QRegExp(unicode(text),
                                QtCore.Qt.CaseInsensitive,
#                                 QtCore.QRegExp.RegExp
                                )
        self.filterproxymodel.setFilterRegExp(filterString)
        

class ToolboxTableModel(QtCore.QAbstractTableModel):
    """ """
    def __init__(self, modeldata = None):
        """ """
        self._modeldata = modeldata
        # Initialize parent.
        QtCore.QAbstractTableModel.__init__(self)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return 0
        return self._modeldata.get_row_count()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return 0
        return self._modeldata.get_column_count()

    def getModeldata(self):
        """ """
        return self._modeldata

    def setModeldata(self, tablemodeldata):
        """ """
        self._modeldata = tablemodeldata
        self.reset() 

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(unicode(self._modeldata.get_header_item(section)))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(unicode(section + 1))
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(unicode(self._modeldata.get_data_item(index.row(), index.column())))
        return QtCore.QVariant()


class ToolboxEditableQTableView( QtGui.QTableView):  
    """ Customized QTableView for editing. The table is automatically connected to an 
        instance of ToolboxEditableTableModel.  """
    def __init__(self, parent = None):
        """ """
        QtGui.QTableView.__init__(self, parent)
        self._tablemodel = ToolboxTableModel(modeldata = plankton_core.DatasetTable())
        self._selectionmodel = None
         
        # Default setup for tables.
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
#         self.verticalHeader().setDefaultSectionSize(18)
        # Default model, data and selection        
        self._tablemodel = ToolboxEditableTableModel()
        self.setModel(self._tablemodel)
        self._selectionmodel = QtGui.QItemSelectionModel(self._tablemodel)
        self.setSelectionModel(self._selectionmodel)
        self.resizeColumnsToContents()
 
    def clearModel(self):
        """ """
        if self._tablemodel.getModeldata():
            self._tablemodel.getModeldata().clear()
         
    def resetModel(self):
        """ Used to repaint. """
        if self._tablemodel:
            self._tablemodel.reset()
          
    def getTableModel(self):
        """ """
        return self._tablemodel.getModeldata()
          
    def setTableModel(self, tablemodeldata):
        """ """
        self._tablemodel.setModeldata(tablemodeldata)
          
    def getSelectionModel(self):
        """ """
        return self._selectionmodel


class ToolboxEditableTableModel(QtCore.QAbstractTableModel):
    """ Table model for editing. """
    def __init__(self, modeldata = None):
        """ """
        self._modeldata = modeldata
        # Initialize parent.
        QtCore.QAbstractTableModel.__init__(self)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return 0
        return self._modeldata.get_row_count()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return 0
        return self._modeldata.get_column_count()

    def getModeldata(self):
        """ """
        return self._modeldata

    def setModeldata(self, tablemodeldata):
        """ """
        self._modeldata = tablemodeldata
        self.reset() 

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(unicode(self._modeldata.get_header_item(section)))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(unicode(section + 1))
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role = QtCore.Qt.DisplayRole):
        """ Overridden abstract method. """
        if self._modeldata == None:
            return QtCore.QVariant()
        # Also for editing.
        if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
            if index.isValid():
                return QtCore.QVariant(unicode(self._modeldata.get_data_item(index.row(), index.column())))
        return QtCore.QVariant()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        """ Overridden abstract method. For editing. """
        if role == QtCore.Qt.EditRole:
            self._modeldata.set_data_item(index.row(), index.column(), unicode(value.toString()))
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        """ Overridden abstract method. For editing. """
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
         
#def set_app_style_sheet(app):
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

def set_app_style_sheet(app):
    app.setStyleSheet("""
        
/*        QDockWidget .QWidget { background-color: whitesmoke; }
*/
        QAbstractButton:hover { color: #d1581c; }
        
        """)
