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

"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import webbrowser
import envmonlib
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class HarmfulPlanktonBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self._harmfulplankton_object = toolbox_resources.ToolboxResources().getResourceHarmfulPlankton()
        self._marinespecies_url = None
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(HarmfulPlanktonBrowserTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentTaxonList())
        contentLayout.addLayout(self._contentItem())
        contentLayout.addLayout(self._contentControl())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL("harmfulPlanktonResourceLoaded"), self._harmfulPlanktonRefresh)

    def _contentTaxonList(self):
        """ """
        layout = QtGui.QVBoxLayout()
        self._tableView = utils_qt.ToolboxQTableView()
        layout.addWidget(self._tableView)
        # Data model.        
        self._model = HarmfulPlanktonTableModel(self._harmfulplankton_object)
        self._tableView.setTablemodel(self._model)
        #
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._showItemInfo)
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self._showItemInfo)
        #
        return layout
    
    def _contentItem(self):
        """ """
        # Active widgets and connections.
        self._scientificname_label = QtGui.QLabel('-')
        # Layout widgets.
        form = QtGui.QFormLayout()
        form.addRow("Scientific name:", self._scientificname_label)
#        hbox = QtGui.QHBoxLayout()
#        hbox.addWidget(self._openmarinespecies)
#        hbox.addStretch(5)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form)
#        layout.addLayout(hbox)
        #
        return layout

    def _contentControl(self):
        """ """
        # Active widgets and connections.
        self._loadresource_button = QtGui.QPushButton("Load harmful plankton resource")
        self.connect(self._loadresource_button, QtCore.SIGNAL("clicked()"), self._loadResource)                
        self._openmarinespecies = QtGui.QPushButton("Open marinespecies.org")
        self.connect(self._openmarinespecies, QtCore.SIGNAL("clicked()"), self._openMarineSpecies)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._openmarinespecies)
        layout.addStretch(5)
        layout.addWidget(self._loadresource_button)
        #
        return layout

    def _showItemInfo(self, index):
        """ """
        #
        taxon = self._harmfulplankton_object.getSortedNameList()[index.row()]
        self._scientificname_label.setText(
            '<b>' + 
            '<i>' + taxon.get('Scientific name', '') + '</i>' + 
            '&nbsp;&nbsp;&nbsp;' + taxon.get('Author', '') + 
            '</b>')
        self._marinespecies_url = \
                u'http://www.marinespecies.org/' + \
                u'hab/aphia.php?p=taxdetails&id=' + \
                unicode(taxon['Aphia id'])


    def _openMarineSpecies(self):
        """ Launch web browser and use show marked species at marinespecies.org. """
        if not self._marinespecies_url:
            envmonlib.Logging().log("Failed to open www.marinespecies.org. No row selected.")
            return
        webbrowser.open(self._marinespecies_url)

    def _loadResource(self):
        """ """
        # All resources are needed.
        toolbox_resources.ToolboxResources().loadUnloadedResourceDyntaxa()
        toolbox_resources.ToolboxResources().loadResourceHarmfulPlankton()

    def _harmfulPlanktonRefresh(self):
        """ """
        self._marinespecies_url = None
        self._model.reset()
        self._tableView.resizeColumnsToContents() # Only visible columns.
        
class HarmfulPlanktonTableModel(QtCore.QAbstractTableModel):
    """
    Example:
            {
                "Aphia id": 246835, 
                "Author": "Balech, 1990", 
                "Scientific name": "Alexandrium andersonii"
            },... 
 
    """
    def __init__(self, dataset):
        self._dataset = dataset
#        self._nameandsizelist = self._dataset.getNameAndSizeList()
        # Initialize parent.
        super(HarmfulPlanktonTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self._dataset = dataset
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self._dataset:
            return len(self._dataset.getSortedNameList())
        else:
            return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        return 4

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Columns: Taxon, Sizeclass. """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return QtCore.QVariant('Scientific name')
            elif section == 1:
                return QtCore.QVariant('Aphia id')            
            elif section == 2:
                return QtCore.QVariant('Dyntaxa id')            
            elif section == 3:
                return QtCore.QVariant('Dyntaxa name')            
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                if index.column() == 0:
                    harmfulplankton = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(harmfulplankton.get('Scientific name', ''))
                if index.column() == 1:
                    sizeclass = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(sizeclass.get('Aphia id', ''))
                if index.column() == 2:
                    harmfulplankton = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(harmfulplankton.get('Dyntaxa id', ''))
                if index.column() == 3:
                    harmfulplankton = self._dataset.getSortedNameList()[index.row()]
                    dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
                    dyntaxa = dyntaxaresource.getTaxonById(harmfulplankton.get('Dyntaxa id', ''))
                    if dyntaxa:
                        return QtCore.QVariant(dyntaxa.get('Scientific name', ''))
                    else:
                        return QtCore.QVariant()
        return QtCore.QVariant()

