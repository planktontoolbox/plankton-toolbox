#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
                    "Trophic type": "A', 
                    "Unit": "cell"
                }, 
                ... 
            ], 
            "Species": "Aphanocapsa reinboldii"
            "Species PW": "Aphanocapsa reinboldii"
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class PegBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self._peg_object = toolbox_resources.ToolboxResources().get_resource_peg()
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(PegBrowserTool, self).__init__(name, parentwidget)
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
        contentLayout.addLayout(self._contentPegItem())
        contentLayout.addLayout(self._contentDyntaxaControl())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL('pegResourceLoaded'), self._pegRefresh)

    def _contentTaxonList(self):
        """ """
        layout = QtGui.QVBoxLayout()
        self._tableView = utils_qt.ToolboxQTableView()
        layout.addWidget(self._tableView)
        # Data model.        
        self._model = PegTableModel(self._peg_object)
        self._tableView.setTablemodel(self._model)
        #
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL('currentChanged(QModelIndex, QModelIndex)'), self._showItemInfo)
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL('selectionChanged(QModelIndex, QModelIndex)'), self._showItemInfo)
        #
        return layout
    
    def _contentPegItem(self):
        """ """
        # Active widgets and connections.
        # Species level.
        self._scientificname_label = QtGui.QLabel('-')
        self._class_label = QtGui.QLabel('-')
        self._division_label = QtGui.QLabel('-')
        self._order_label = QtGui.QLabel('-')
        # Sizeclass level.
        self._size_class_label = QtGui.QLabel('-')
        self._trophic_type_label = QtGui.QLabel('-')
        self._shape_label = QtGui.QLabel('-')
        self._formula_label = QtGui.QLabel('-')
        self._volume_label = QtGui.QLabel('-')
        self._carbon_label = QtGui.QLabel('-')
        # Layout widgets.
        layout = QtGui.QFormLayout()
        layout.addRow('<b><u>Species:</u></b>', None)
        layout.addRow('Scientific name:', self._scientificname_label)
        layout.addRow('Class:', self._class_label)
        layout.addRow('Division:', self._division_label)
        layout.addRow('Order:', self._order_label)
        layout.addRow('<b><u>Size class:</u></b>', None)
        layout.addRow('Size class:', self._size_class_label)
        layout.addRow('Trophic type:', self._trophic_type_label)
        layout.addRow('Geometric shape:', self._shape_label)
        layout.addRow('Formula:', self._formula_label)
        layout.addRow('Calculated volume:', self._volume_label)
        layout.addRow('Calculated carbon:', self._carbon_label)
        #
        return layout

    def _contentDyntaxaControl(self):
        """ """
        # Active widgets and connections.
        self._loadresource_button = QtGui.QPushButton('Load PEG resource')
        self.connect(self._loadresource_button, QtCore.SIGNAL('clicked()'), self._loadResource)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self._loadresource_button)
        #
        return layout

    def _showItemInfo(self, index):
        """ """
        #
        taxon = self._peg_object.getNameAndSizeList()[index.row()][0]
        self._scientificname_label.setText(
            '<b>' + 
            '<i>' + taxon.get('Species', '') + '</i>' + 
            '&nbsp;&nbsp;&nbsp;' + taxon.get('Author', '') + 
            '</b>')
        self._class_label.setText(taxon.get('Class', '-'))
        self._division_label.setText(taxon.get('Division', '-'))
        self._order_label.setText(taxon.get('Order', '-'))
        #
        sizeclass = self._peg_object.getNameAndSizeList()[index.row()][1]
        self._size_class_label.setText('<b>' + unicode(sizeclass.get('Size class', '-')) + '</b>')
        self._trophic_type_label.setText(sizeclass.get('Trophic type', '-'))
        self._shape_label.setText(sizeclass.get('Geometric shape', '-'))
        self._formula_label.setText(sizeclass.get('Formula', '-'))
        self._volume_label.setText(unicode(sizeclass.get('Calculated volume, um3', '-')))
        self._carbon_label.setText(unicode(sizeclass.get('Calculated Carbon pg/counting unit', '-')))

    def _loadResource(self):
        """ """
        # Dyntaxa is needed to load PEG.
        self._writeToStatusBar('Loading PEG resource...')
        try:
            toolbox_resources.ToolboxResources().load_unloaded_resource_dyntaxa()
            toolbox_resources.ToolboxResources().load_resource_peg()
        finally:
            self._writeToStatusBar('')

    def _pegRefresh(self):
        """ """
        self._model.reset()
        self._tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
        
class PegTableModel(QtCore.QAbstractTableModel):
    """ 
    """
    def __init__(self, dataset):
        self._dataset = dataset
#        self._nameandsizelist = self._dataset.getNameAndSizeList()
        # Initialize parent.
        super(PegTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self._dataset = dataset
        
    def row_count(self, parent=QtCore.QModelIndex()):
        """ """
        if self._dataset:
            return len(self._dataset.getNameAndSizeList())
        else:
            return 0

    def column_count(self, parent=QtCore.QModelIndex()):
        """ """
        return 4

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Overridden abstract method.
            Columns: Taxon, Sizeclass. """
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
        """ Overridden abstract method. """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                if index.column() == 0:
                    peg = self._dataset.getNameAndSizeList()[index.row()][0]
                    return QtCore.QVariant(peg.get('Species', ''))
                if index.column() == 1:
                    sizeclass = self._dataset.getNameAndSizeList()[index.row()][1]
                    return QtCore.QVariant(sizeclass.get('Size class', ''))
                if index.column() == 2:
                    peg = self._dataset.getNameAndSizeList()[index.row()][0]
                    return QtCore.QVariant(peg.get('Dyntaxa id', ''))
                if index.column() == 3:
                    peg = self._dataset.getNameAndSizeList()[index.row()][0]
                    dyntaxaresource = toolbox_resources.ToolboxResources().get_resource_dyntaxa()
                    dyntaxa = dyntaxaresource.getTaxonById(peg.get('Dyntaxa id', ''))
                    if dyntaxa:
                        return QtCore.QVariant(dyntaxa.get('Scientific name', ''))
                    else:
                        return QtCore.QVariant()
        return QtCore.QVariant()

