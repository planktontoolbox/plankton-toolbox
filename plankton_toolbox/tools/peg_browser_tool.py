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
Sample part from the resource file:

            "Author": "(P. Richter) Kom\u00e1rek & Anagnostidis 1995", 
            "Class": "Nostocophyceae (Cyanophyceae)", 
            "Division": "CYANOPHYTA (CYANOBACTERIA)", 
            "Dyntaxa id": "CYANOPHYTA (CYANOBACTERIA)", 
            "Order": "CHROOCOCCALES", 
            "Size classes": [
                {
                    "Calculated Carbon pg/counting unit": 4.0, 
                    "Calculated volume, um3": 22.0, 
                    "Comment on Carbon calculation": "based on individual cell", 
                    "Diameter(d1), um": 3.5, 
                    "Filament: length of cell, um": "-", 
                    "Formula": "?/6*d^3", 
                    "Geometric shape": "sphere", 
                    "No. of cells/counting unit": 1.0, 
                    "Size class": 1, 
                    "Size class PW": 1, 
                    "Size range": "3-4", 
                    "Trophy": "AU", 
                    "Unit": "cell"
                }, 
                ... 
            ], 
            "Species": "Aphanocapsa reinboldii"
            "Species PW": "Aphanocapsa reinboldii"
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base
#import plankton_toolbox.core.biology.taxa as taxa
#import plankton_toolbox.core.biology.taxa_sources as taxa_sources
#import plankton_toolbox.core.biology.taxa_prepare as taxa_prepare
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class PegBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self.__peg_object = toolbox_resources.ToolboxResources().getResourcePeg()
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(PegBrowserTool, self).__init__(name, parentwidget)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentTaxonList())
        contentLayout.addLayout(self.__contentPegItem())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL("pegResourceLoaded"), self.__pegRefresh)

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
        self.__model = PegTableModel(self.__peg_object)
        self.__tableView.setModel(self.__model)
        selectionModel = QtGui.QItemSelectionModel(self.__model)
        self.__tableView.setSelectionModel(selectionModel)
        self.__tableView.resizeColumnsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        #
        return layout
    
    def __contentPegItem(self):
        """ """
        # Active widgets and connections.
        # Species level.
        self.__species_label = QtGui.QLabel('-')
        self.__author_label = QtGui.QLabel('-')
        self.__class_label = QtGui.QLabel('-')
        self.__division_label = QtGui.QLabel('-')
        self.__order_label = QtGui.QLabel('-')
        # Sizeclass level.
        self.__size_class_label = QtGui.QLabel('-')
        self.__thropy_label = QtGui.QLabel('-')
        self.__shape_label = QtGui.QLabel('-')
        self.__formula_label = QtGui.QLabel('-')
        self.__volume_label = QtGui.QLabel('-')
        self.__carbon_label = QtGui.QLabel('-')
        # Layout widgets.
        layout = QtGui.QFormLayout()
        layout.addRow("<b><u>Species:</u></b>", None)
        layout.addRow("Taxon name:", self.__species_label)
        layout.addRow("Author:", self.__author_label)
        layout.addRow("Class:", self.__class_label)
        layout.addRow("Division:", self.__division_label)
        layout.addRow("Order:", self.__order_label)
        layout.addRow("<b><u>Size class:</u></b>", None)
        layout.addRow("Size class:", self.__size_class_label)
        layout.addRow("Trophy:", self.__thropy_label)
        layout.addRow("Geometric shape:", self.__shape_label)
        layout.addRow("Formula:", self.__formula_label)
        layout.addRow("Calculated volume:", self.__volume_label)
        layout.addRow("Calculated carbon:", self.__carbon_label)
        #
        return layout

    def __showItemInfo(self, index):
        """ """
#        name_index = self.__model.createIndex(index.row(), 0)
#        size_index = self.__model.createIndex(index.row(), 1)
#        taxonName = self.__model.data(name_index).toString()
#        size = self.__model.data(size_index).toString() 
###        taxonName = self.__peg_object.getData(index.row(), 0)
###        size = self.__peg_object.getData(index.row(), 1)
        #
        taxon = self.__peg_object.getNameAndSizeList()[index.row()][0]
        self.__species_label.setText('<b><i>' + taxon.get('Species', '-') + '</i></b>')
        self.__author_label.setText(taxon.get('Author', '-'))
        self.__class_label.setText(taxon.get('Class', '-'))
        self.__division_label.setText(taxon.get('Division', '-'))
        self.__order_label.setText(taxon.get('Order', '-'))
        #
        sizeclass = self.__peg_object.getNameAndSizeList()[index.row()][1]
        self.__size_class_label.setText('<b>' + unicode(sizeclass.get('Size class', '-')) + '</b>')
        self.__thropy_label.setText(sizeclass.get('Trophy', '-'))
        self.__shape_label.setText(sizeclass.get('Geometric shape', '-'))
        self.__formula_label.setText(sizeclass.get('Formula', '-'))
        self.__volume_label.setText(unicode(sizeclass.get('Calculated volume, um3', '-')))
        self.__carbon_label.setText(unicode(sizeclass.get('Calculated Carbon pg/counting unit', '-')))

    def __pegRefresh(self):
        """ """
        self.__model.reset()
        self.__tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
        
class PegTableModel(QtCore.QAbstractTableModel):
    """ 
    """
    def __init__(self, dataset):
        self.__dataset = dataset
#        self.__nameandsizelist = self.__dataset.getNameAndSizeList()
        # Initialize parent.
        super(PegTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self.__dataset = dataset
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self.__dataset:
            return len(self.__dataset.getNameAndSizeList())
        else:
            return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        return 4

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Columns: Taxon, Sizeclass. """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return QtCore.QVariant('PEG name')
            elif section == 1:
                return QtCore.QVariant('Sizeclass')            
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
                    peg = self.__dataset.getNameAndSizeList()[index.row()][0]
                    return QtCore.QVariant(peg.get('Species', ''))
                if index.column() == 1:
                    sizeclass = self.__dataset.getNameAndSizeList()[index.row()][1]
                    return QtCore.QVariant(sizeclass.get('Size class', ''))
                if index.column() == 2:
                    peg = self.__dataset.getNameAndSizeList()[index.row()][0]
                    return QtCore.QVariant(peg.get('Dyntaxa id', ''))
                if index.column() == 3:
                    peg = self.__dataset.getNameAndSizeList()[index.row()][0]
                    dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
                    dyntaxa = dyntaxaresource.getTaxonById(peg.get('Dyntaxa id', ''))
                    if dyntaxa:
                        return QtCore.QVariant(dyntaxa.get('Valid name', ''))
                    else:
                        return QtCore.QVariant()
        return QtCore.QVariant()




#    def getData(self, row, column):
#        """ Used by table models. """
#        if self.__nameAndSizeList == None:
#            self.__createNameAndSizeList()
#        if column == 0:
##            return self.__nameAndSizeList[row].split(':')[0] 
#            return self.__nameAndSizeList[row][0].get('Species', '')
#        if column == 1:
##            return self.__nameAndSizeList[row].split(':')[1] 
#            return self.__nameAndSizeList[row][1].get('Size class', '') 
#
#    def getRowCount(self):
#        """ Used by table models. """
#        if self.__nameAndSizeList == None:
#            self.__createNameAndSizeList()
#        return len(self.__nameAndSizeList)
    


