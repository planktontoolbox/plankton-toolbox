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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import webbrowser
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class HarmfulPlanktonBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self.__harmfulplankton_object = toolbox_resources.ToolboxResources().getResourceHarmfulPlankton()
        self.__marinespecies_url = None
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(HarmfulPlanktonBrowserTool, self).__init__(name, parentwidget)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentTaxonList())
        contentLayout.addLayout(self.__contentItem())
        contentLayout.addLayout(self.__contentControl())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL("harmfulPlanktonResourceLoaded"), self.__harmfulPlanktonRefresh)

    def __contentTaxonList(self):
        """ """
        layout = QtGui.QVBoxLayout()
        self.__tableView = QtGui.QTableView()
        layout.addWidget(self.__tableView)
        #
        self.__tableView.setAlternatingRowColors(True)
        self.__tableView.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.__tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.__tableView.verticalHeader().setDefaultSectionSize(18)
        # Model, data and selection        
        self.__model = HarmfulPlanktonTableModel(self.__harmfulplankton_object)
        self.__tableView.setModel(self.__model)
        selectionModel = QtGui.QItemSelectionModel(self.__model)
        self.__tableView.setSelectionModel(selectionModel)
        self.__tableView.resizeColumnsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        #
        return layout
    
    def __contentItem(self):
        """ """
        # Active widgets and connections.
        self.__scientificname_label = QtGui.QLabel('-')
        # Layout widgets.
        form = QtGui.QFormLayout()
        form.addRow("Scientific name:", self.__scientificname_label)
#        hbox = QtGui.QHBoxLayout()
#        hbox.addWidget(self.__openmarinespecies)
#        hbox.addStretch(5)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form)
#        layout.addLayout(hbox)
        #
        return layout

    def __contentControl(self):
        """ """
        # Active widgets and connections.
        self.__loadresource_button = QtGui.QPushButton("Load harmful plankton resource")
        self.connect(self.__loadresource_button, QtCore.SIGNAL("clicked()"), self.__loadResource)                
        self.__openmarinespecies = QtGui.QPushButton("Open marinespecies.org")
        self.connect(self.__openmarinespecies, QtCore.SIGNAL("clicked()"), self.__openMarineSpecies)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.__openmarinespecies)
        layout.addStretch(5)
        layout.addWidget(self.__loadresource_button)
        #
        return layout

    def __showItemInfo(self, index):
        """ """
        #
        taxon = self.__harmfulplankton_object.getSortedNameList()[index.row()]
        self.__scientificname_label.setText(
            '<b>' + 
            '<i>' + taxon.get('Scientific name', '') + '</i>' + 
            '&nbsp;&nbsp;&nbsp;' + taxon.get('Author', '') + 
            '</b>')
        self.__marinespecies_url = \
                u'http://www.marinespecies.org/' + \
                u'hab/aphia.php?p=taxdetails&id=' + \
                unicode(taxon['Aphia id'])


    def __openMarineSpecies(self):
        """ Launch web browser and use show marked species at marinespecies.org. """
        if not self.__marinespecies_url:
            utils.Logger().log("Failed to open www.marinespecies.org. No row selected.")
            return
        webbrowser.open(self.__marinespecies_url)

    def __loadResource(self):
        """ """
        # All resources are needed.
        toolbox_resources.ToolboxResources().loadUnloadedResourceDyntaxa()
        toolbox_resources.ToolboxResources().loadResourceHarmfulPlankton()

    def __harmfulPlanktonRefresh(self):
        """ """
        self.__marinespecies_url = None
        self.__model.reset()
        self.__tableView.resizeColumnsToContents() # Only visible columns.
        
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
        self.__dataset = dataset
#        self.__nameandsizelist = self.__dataset.getNameAndSizeList()
        # Initialize parent.
        super(HarmfulPlanktonTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self.__dataset = dataset
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self.__dataset:
            return len(self.__dataset.getSortedNameList())
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
                    harmfulplankton = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(harmfulplankton.get('Scientific name', ''))
                if index.column() == 1:
                    sizeclass = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(sizeclass.get('Aphia id', ''))
                if index.column() == 2:
                    harmfulplankton = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(harmfulplankton.get('Dyntaxa id', ''))
                if index.column() == 3:
                    harmfulplankton = self.__dataset.getSortedNameList()[index.row()]
                    dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
                    dyntaxa = dyntaxaresource.getTaxonById(harmfulplankton.get('Dyntaxa id', ''))
                    if dyntaxa:
                        return QtCore.QVariant(dyntaxa.get('Scientific name', ''))
                    else:
                        return QtCore.QVariant()
        return QtCore.QVariant()

