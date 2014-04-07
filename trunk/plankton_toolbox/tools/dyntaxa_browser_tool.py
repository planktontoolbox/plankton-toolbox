#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class DyntaxaBrowserTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Create model.
        self._dyntaxa_object = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DyntaxaBrowserTool, self).__init__(name, parentwidget)
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
        contentLayout.addLayout(self._contentDyntaxaItem())
        contentLayout.addLayout(self._contentDyntaxaControl())
        # Used when toolbox resource has changed.        
        self.connect(toolbox_resources.ToolboxResources(), QtCore.SIGNAL("dyntaxaResourceLoaded"), self._dyntaxaRefresh)

    def _contentTaxonList(self):
        """ """
        layout = QtGui.QVBoxLayout()
        self._tableView = utils_qt.ToolboxQTableView()
        layout.addWidget(self._tableView)
        # Data model.        
        self._model = DyntaxaTableModel(self._dyntaxa_object)
        self._tableView.setTablemodel(self._model)
        #
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._showItemInfo)
        self.connect(self._tableView.selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self._showItemInfo)
        #
        return layout
    
    def _contentDyntaxaItem(self):
        """ """
        # Active widgets and connections.
        # Species level.
        self._scientificname_label = QtGui.QLabel('-')
#        self._author_label = QtGui.QLabel('-')
        self._classification_label = QtGui.QLabel('-')
#        self._author_label = QtGui.QLabel('-')
#        self._class_label = QtGui.QLabel('-')
#        self._division_label = QtGui.QLabel('-')
#        self._order_label = QtGui.QLabel('-')
#        # Sizeclass level.
#        self._size_class_label = QtGui.QLabel('-')
#        self._thropy_label = QtGui.QLabel('-')
#        self._shape_label = QtGui.QLabel('-')
#        self._formula_label = QtGui.QLabel('-')
#        self._volume_label = QtGui.QLabel('-')
#        self._carbon_label = QtGui.QLabel('-')
        # Layout widgets.
        layout = QtGui.QFormLayout()
#        layout.addRow("<b><u>Species:</u></b>", None)
        layout.addRow("Scientific name:", self._scientificname_label)
#        layout.addRow("Author:", self._author_label)
        layout.addRow("Classification:", self._classification_label)
#        layout.addRow("Author:", self._author_label)
#        layout.addRow("Class:", self._class_label)
#        layout.addRow("Division:", self._division_label)
#        layout.addRow("Order:", self._order_label)
#        layout.addRow("<b><u>Size class:</u></b>", None)
#        layout.addRow("Size class:", self._size_class_label)
#        layout.addRow("Trophy:", self._thropy_label)
#        layout.addRow("Geometric shape:", self._shape_label)
#        layout.addRow("Formula:", self._formula_label)
#        layout.addRow("Calculated volume:", self._volume_label)
#        layout.addRow("Calculated carbon:", self._carbon_label)
        #
        return layout

    def _contentDyntaxaControl(self):
        """ """
        # Active widgets and connections.
        self._loadresource_button = QtGui.QPushButton("Load Dyntaxa resource")
        self.connect(self._loadresource_button, QtCore.SIGNAL("clicked()"), self._loadResource)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self._loadresource_button)
        #
        return layout

    def _showItemInfo(self, index):
        """ """
#        name_index = self._model.createIndex(index.row(), 0)
#        size_index = self._model.createIndex(index.row(), 1)
#        taxonName = self._model.data(name_index).toString()
#        size = self._model.data(size_index).toString() 
###        taxonName = self._dyntaxa_object.getData(index.row(), 0)
###        size = self._dyntaxa_object.getData(index.row(), 1)
        #
        taxon = self._dyntaxa_object.getSortedNameList()[index.row()]
        self._scientificname_label.setText(
            '<b>' + 
            '<i>' + taxon.get('Scientific name', '') + '</i>' + 
            '&nbsp;&nbsp;&nbsp;' + taxon.get('Scientific name author', '') + 
            '</b>')
        # Build classification hierarchy.
        hier = ''
        delimiter = ''
        name = taxon.get('Scientific name', None)
        while name != None:
            hier = name + delimiter + hier
            delimiter = ' - '
            name = None
            parentid = taxon.get('Parent id', None)
            taxon = self._dyntaxa_object.getTaxonById(parentid)
            if taxon:
                name = taxon.get('Scientific name', None)
            if len(hier) > 1000: # If infinite loops related to error in parent id. 
                self._classification_label.setText('ERROR: Hierachy too long: ' + hier)
                print('ERROR: Hierachy too long: ' + hier)
                return
        self._classification_label.setText(hier)
#        self._author_label.setText(taxon.get('Author', '-'))
#        self._class_label.setText(taxon.get('Class', '-'))
#        self._division_label.setText(taxon.get('Division', '-'))
#        self._order_label.setText(taxon.get('Order', '-'))
#        #
#        sizeclass = self._dyntaxa_object.getNameAndSizeList()[index.row()][1]
#        self._size_class_label.setText('<b>' + unicode(sizeclass.get('Size class', '-')) + '</b>')
#        self._thropy_label.setText(sizeclass.get('Trophy', '-'))
#        self._shape_label.setText(sizeclass.get('Geometric shape', '-'))
#        self._formula_label.setText(sizeclass.get('Formula', '-'))
#        self._volume_label.setText(unicode(sizeclass.get('Calculated volume, um3', '-')))
#        self._carbon_label.setText(unicode(sizeclass.get('Calculated Carbon pg/counting unit', '-')))

    def _loadResource(self):
        """ """
        toolbox_resources.ToolboxResources().loadResourceDyntaxa()

    def _dyntaxaRefresh(self):
        """ """
        self._model.reset()
        self._tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
        
##############################################################
class DyntaxaTableModel(QtCore.QAbstractTableModel):
    """ 
    """
    def __init__(self, dataset):
        self._dataset = dataset
#        self._nameandsizelist = self._dataset.getNameAndSizeList()
        # Initialize parent.
        super(DyntaxaTableModel, self).__init__()
        
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
                    sizeclass = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(sizeclass.get('Taxon id', ''))
                if index.column() == 1:
                    taxon = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(taxon.get('Scientific name', ''))
                if index.column() == 2:
                    taxon = self._dataset.getSortedNameList()[index.row()]
                    return QtCore.QVariant(taxon.get('Taxon type', ''))
                if index.column() == 3:
                    taxon = self._dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'Swedish':
                            return QtCore.QVariant(nameitem.get('Name', ''))
                if index.column() == 4:
                    taxon = self._dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'ITIS-number':
                            return QtCore.QVariant(nameitem.get('Name', ''))
                if index.column() == 5:
                    taxon = self._dataset.getSortedNameList()[index.row()]
                    for nameitem in taxon.get('Names', []):
                        if nameitem['Name type'] == 'ERMS-name':
                            return QtCore.QVariant(nameitem.get('Name', ''))
        return QtCore.QVariant()

