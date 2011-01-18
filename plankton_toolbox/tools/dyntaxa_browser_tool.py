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
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class DyntaxaBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self.__dyntaxa_object = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DyntaxaBrowserTool, self).__init__(name, parentwidget)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentTaxonList())
        contentLayout.addLayout(self.__contentDyntaxaItem())
        contentLayout.addLayout(self.__contentDyntaxaControl())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL("dyntaxaResourceLoaded"), self.__dyntaxaRefresh)

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
        self.__model = DyntaxaTableModel(self.__dyntaxa_object)
        self.__tableView.setModel(self.__model)
        selectionModel = QtGui.QItemSelectionModel(self.__model)
        self.__tableView.setSelectionModel(selectionModel)
        self.__tableView.resizeColumnsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__showItemInfo)
        #
        return layout
    
    def __contentDyntaxaItem(self):
        """ """
        # Active widgets and connections.
        # Species level.
        self.__scientificname_label = QtGui.QLabel('-')
#        self.__author_label = QtGui.QLabel('-')
        self.__hierarchy_label = QtGui.QLabel('-')
#        self.__author_label = QtGui.QLabel('-')
#        self.__class_label = QtGui.QLabel('-')
#        self.__division_label = QtGui.QLabel('-')
#        self.__order_label = QtGui.QLabel('-')
#        # Sizeclass level.
#        self.__size_class_label = QtGui.QLabel('-')
#        self.__thropy_label = QtGui.QLabel('-')
#        self.__shape_label = QtGui.QLabel('-')
#        self.__formula_label = QtGui.QLabel('-')
#        self.__volume_label = QtGui.QLabel('-')
#        self.__carbon_label = QtGui.QLabel('-')
        # Layout widgets.
        layout = QtGui.QFormLayout()
#        layout.addRow("<b><u>Species:</u></b>", None)
        layout.addRow("Scientific name:", self.__scientificname_label)
#        layout.addRow("Author:", self.__author_label)
        layout.addRow("Hierarchy:", self.__hierarchy_label)
#        layout.addRow("Author:", self.__author_label)
#        layout.addRow("Class:", self.__class_label)
#        layout.addRow("Division:", self.__division_label)
#        layout.addRow("Order:", self.__order_label)
#        layout.addRow("<b><u>Size class:</u></b>", None)
#        layout.addRow("Size class:", self.__size_class_label)
#        layout.addRow("Trophy:", self.__thropy_label)
#        layout.addRow("Geometric shape:", self.__shape_label)
#        layout.addRow("Formula:", self.__formula_label)
#        layout.addRow("Calculated volume:", self.__volume_label)
#        layout.addRow("Calculated carbon:", self.__carbon_label)
        #
        return layout

    def __contentDyntaxaControl(self):
        """ """
        # Active widgets and connections.
        self.__loadresource_button = QtGui.QPushButton("Load Dyntaxa resource")
        self.connect(self.__loadresource_button, QtCore.SIGNAL("clicked()"), self.__loadResource)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self.__loadresource_button)
        #
        return layout

    def __showItemInfo(self, index):
        """ """
#        name_index = self.__model.createIndex(index.row(), 0)
#        size_index = self.__model.createIndex(index.row(), 1)
#        taxonName = self.__model.data(name_index).toString()
#        size = self.__model.data(size_index).toString() 
###        taxonName = self.__dyntaxa_object.getData(index.row(), 0)
###        size = self.__dyntaxa_object.getData(index.row(), 1)
        #
        taxon = self.__dyntaxa_object.getSortedNameList()[index.row()]
        self.__scientificname_label.setText(
            '<b>' + 
            '<i>' + taxon.get('Scientific name', '') + '</i>' + 
            '&nbsp;&nbsp;&nbsp;' + taxon.get('Scientific name author', '') + 
            '</b>')
        # Build hierarchy.
        hier = ''
        delimiter = ''
        name = taxon.get('Scientific name', None)
        while name != None:
            hier = name + delimiter + hier
            delimiter = ' - '
            name = None
            parentid = taxon.get('Parent id', None)
            taxon = self.__dyntaxa_object.getTaxonById(parentid)
            if taxon:
                name = taxon.get('Scientific name', None)
            if len(hier) > 1000: # If infinite loops related to error in parent id. 
                self.__hierarchy_label.setText('ERROR: Hierachy too long: ' + hier)
                print('ERROR: Hierachy too long: ' + hier)
                return
        self.__hierarchy_label.setText(hier)
#        self.__author_label.setText(taxon.get('Author', '-'))
#        self.__class_label.setText(taxon.get('Class', '-'))
#        self.__division_label.setText(taxon.get('Division', '-'))
#        self.__order_label.setText(taxon.get('Order', '-'))
#        #
#        sizeclass = self.__dyntaxa_object.getNameAndSizeList()[index.row()][1]
#        self.__size_class_label.setText('<b>' + unicode(sizeclass.get('Size class', '-')) + '</b>')
#        self.__thropy_label.setText(sizeclass.get('Trophy', '-'))
#        self.__shape_label.setText(sizeclass.get('Geometric shape', '-'))
#        self.__formula_label.setText(sizeclass.get('Formula', '-'))
#        self.__volume_label.setText(unicode(sizeclass.get('Calculated volume, um3', '-')))
#        self.__carbon_label.setText(unicode(sizeclass.get('Calculated Carbon pg/counting unit', '-')))

    def __loadResource(self):
        """ """
        toolbox_resources.ToolboxResources().loadResourceDyntaxa()

    def __dyntaxaRefresh(self):
        """ """
        self.__model.reset()
        self.__tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
        
##############################################################
class DyntaxaTableModel(QtCore.QAbstractTableModel):
    """ 
    """
    def __init__(self, dataset):
        self.__dataset = dataset
#        self.__nameandsizelist = self.__dataset.getNameAndSizeList()
        # Initialize parent.
        super(DyntaxaTableModel, self).__init__()
        
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
        return 6

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Columns: Dyntaxa id, Dyntaxa name. """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return QtCore.QVariant('Dyntaxa id')            
            elif section == 1:
                return QtCore.QVariant('Scientific name')            
            elif section == 2:
                return QtCore.QVariant('Type')            
            elif section == 3:
                return QtCore.QVariant('Swedish')            
            elif section == 4:
                return QtCore.QVariant('ITIS')            
            elif section == 5:
                return QtCore.QVariant('ERMS')            
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                if index.column() == 0:
                    sizeclass = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(sizeclass.get('Taxon id', ''))
                if index.column() == 1:
                    taxon = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(taxon.get('Scientific name', ''))
                if index.column() == 2:
                    taxon = self.__dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(taxon.get('Taxon type', ''))
                if index.column() == 3:
                    taxon = self.__dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'Swedish':
                            return QtCore.QVariant(nameitem.get('Name', ''))
                if index.column() == 4:
                    taxon = self.__dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'ITIS-number':
                            return QtCore.QVariant(nameitem.get('Name', ''))
                if index.column() == 5:
                    taxon = self.__dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'ERMS-name':
                            return QtCore.QVariant(nameitem.get('Name', ''))
        return QtCore.QVariant()

