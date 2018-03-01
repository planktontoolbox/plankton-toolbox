#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# """
# Sample part from the resource file:
# 
#             "Author": "(P. Richter) Kom\u00e1rek & Anagnostidis 1995", 
#             "Class": "Nostocophyceae (Cyanophyceae)", 
#             "Division": "CYANOPHYTA (CYANOBACTERIA)", 
#             "Dyntaxa id": "CYANOPHYTA (CYANOBACTERIA)", 
#             "Order": "CHROOCOCCALES", 
#             "Size classes": [
#                 {
#                     "Calculated Carbon pg/counting unit": 4.0, 
#                     "Calculated volume, um3": 22.0, 
#                     "Comment on Carbon calculation": "based on individual cell", 
#                     "Diameter(d1), um": 3.5, 
#                     "Filament: length of cell, um": "-", 
#                     "Formula": "?/6*d^3", 
#                     "Geometric shape": "sphere", 
#                     "No. of cells/counting unit": 1.0, 
#                     "Size class": 1, 
#                     "Size class PW": 1, 
#                     "Size range": "3-4", 
#                     "Trophic type": "A', 
#                     "Unit": "cell"
#                 }, 
#                 ... 
#             ], 
#             "Species": "Aphanocapsa reinboldii"
#             "Species PW": "Aphanocapsa reinboldii"
# """
# 
# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.tools.tool_base as tool_base
# import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources
# 
# class PegBrowserTool(tool_base.ToolBase):
#     """
#     """
#     
#     def __init__(self, name, parentwidget):
#         """ """
#         # Create model.
#         self._peg_object = toolbox_resources.ToolboxResources().get_resource_peg()
#         # Initialize parent. Should be called after other 
#         # initialization since the base class calls _create_content().
#         super(PegBrowserTool, self).__init__(name, parentwidget)
#         #
#         # Where is the tool allowed to dock in the main window.
#         self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
#         self.setBaseSize(600,600)
#         
#     def _create_content(self):
#         """ """
#         content = self._create_scrollable_content()
#         contentLayout = QtWidgets.QVBoxLayout()
#         content.setLayout(contentLayout)
#         contentLayout.addLayout(self._content_taxon_list())
#         contentLayout.addLayout(self._content_peg_item())
#         contentLayout.addLayout(self._content_dyntaxa_control())
#         # Used when toolbox resource has changed.        
#         toolbox_resources.ToolboxResources().pegResourceLoaded.connect(self._peg_refresh)
# 
#     def _content_taxon_list(self):
#         """ """
#         layout = QtWidgets.QVBoxLayout()
#         self._tableView = app_framework.ToolboxQTableView()
#         layout.addWidget(self._tableView)
#         # Data model.        
#         self._model = PegTableModel(self._peg_object)
#         self._tableView.setTableModel(self._model)
#         #
#         self._tableView.getSelectionModel().currentChanged(QModelIndex, QModelIndex)'), self._show_item_info)
#         self._tableView.getSelectionModel().selectionChanged(QModelIndex, QModelIndex)'), self._show_item_info)
#         #
#         return layout
#     
#     def _content_peg_item(self):
#         """ """
#         # Active widgets and connections.
#         # Species level.
#         self._scientificname_label = QtWidgets.QLabel('-')
#         self._class_label = QtWidgets.QLabel('-')
#         self._division_label = QtWidgets.QLabel('-')
#         self._order_label = QtWidgets.QLabel('-')
#         # Sizeclass level.
#         self._size_class_label = QtWidgets.QLabel('-')
#         self._trophic_type_label = QtWidgets.QLabel('-')
#         self._shape_label = QtWidgets.QLabel('-')
#         self._formula_label = QtWidgets.QLabel('-')
#         self._volume_label = QtWidgets.QLabel('-')
#         self._carbon_label = QtWidgets.QLabel('-')
#         # Layout widgets.
#         layout = QtWidgets.QFormLayout()
#         layout.addRow('<b><u>Species:</u></b>', None)
#         layout.addRow('Scientific name:', self._scientificname_label)
#         layout.addRow('Class:', self._class_label)
#         layout.addRow('Division:', self._division_label)
#         layout.addRow('Order:', self._order_label)
#         layout.addRow('<b><u>Size class:</u></b>', None)
#         layout.addRow('Size class:', self._size_class_label)
#         layout.addRow('Trophic type:', self._trophic_type_label)
#         layout.addRow('Geometric shape:', self._shape_label)
#         layout.addRow('Formula:', self._formula_label)
#         layout.addRow('Calculated volume:', self._volume_label)
#         layout.addRow('Calculated carbon:', self._carbon_label)
#         #
#         return layout
# 
#     def _content_dyntaxa_control(self):
#         """ """
#         # Active widgets and connections.
#         self._loadresource_button = QtWidgets.QPushButton('Load PEG resource')
#         self._loadresource_button.clicked.connect(self._load_resource)                
#         # Layout widgets.
#         layout = QtWidgets.QHBoxLayout()
#         layout.addStretch(5)
#         layout.addWidget(self._loadresource_button)
#         #
#         return layout
# 
#     def _show_item_info(self, index):
#         """ """
#         #
#         taxon = self._peg_object.getNameAndSizeList()[index.row()][0]
#         self._scientificname_label.setText(
#             '<b>' + 
#             '<i>' + taxon.get('Species', '') + '</i>' + 
#             '&nbsp;&nbsp;&nbsp;' + taxon.get('Author', '') + 
#             '</b>')
#         self._class_label.setText(taxon.get('Class', '-'))
#         self._division_label.setText(taxon.get('Division', '-'))
#         self._order_label.setText(taxon.get('Order', '-'))
#         #
#         sizeclass = self._peg_object.getNameAndSizeList()[index.row()][1]
#         self._size_class_label.setText('<b>' + str(sizeclass.get('Size class', '-')) + '</b>')
#         self._trophic_type_label.setText(sizeclass.get('Trophic type', '-'))
#         self._shape_label.setText(sizeclass.get('Geometric shape', '-'))
#         self._formula_label.setText(sizeclass.get('Formula', '-'))
#         self._volume_label.setText(str(sizeclass.get('Calculated volume, um3', '-')))
#         self._carbon_label.setText(str(sizeclass.get('Calculated Carbon pg/counting unit', '-')))
# 
#     def _load_resource(self):
#         """ """
#         # Dyntaxa is needed to load PEG.
#         self._write_to_status_bar('Loading PEG resource...')
#         try:
#             toolbox_resources.ToolboxResources().load_unloaded_resource_dyntaxa()
#             toolbox_resources.ToolboxResources().load_resource_peg()
#         finally:
#             self._write_to_status_bar('')
# 
#     def _peg_refresh(self):
#         """ """
#         self._tableView.resetModel()
#         self._tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
#         
# class PegTableModel(QtCore.QAbstractTableModel):
#     """ 
#     """
#     def __init__(self, dataset):
#         self._dataset = dataset
# #        self._nameandsizelist = self._dataset.getNameAndSizeList()
#         # Initialize parent.
#         super(PegTableModel, self).__init__()
#         
#     def set_dataset(self, dataset):
#         """ """
#         self._dataset = dataset
#         
#     def rowCount(self, parent=QtCore.QModelIndex()):
#         """ """
#         if self._dataset:
#             return len(self._dataset.getNameAndSizeList())
#         else:
#             return 0
# 
#     def columnCount(self, parent=QtCore.QModelIndex()):
#         """ """
#         return 4
# 
#     def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
#         """ Overridden abstract method.
#             Columns: Taxon, Sizeclass. """
#         if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#             if section == 0:
#                 return QtCore.QVariant('PEG name')
#             elif section == 1:
#                 return QtCore.QVariant('Sizeclass')            
#             elif section == 2:
#                 return QtCore.QVariant('Dyntaxa id')            
#             elif section == 3:
#                 return QtCore.QVariant('Dyntaxa name')            
#         if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
#             return QtCore.QVariant(section + 1)
#         return QtCore.QVariant()
# 
#     def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
#         """ Overridden abstract method. """
#         if role == QtCore.Qt.DisplayRole:
#             if index.isValid():
#                 if index.column() == 0:
#                     peg = self._dataset.getNameAndSizeList()[index.row()][0]
#                     return QtCore.QVariant(peg.get('Species', ''))
#                 if index.column() == 1:
#                     sizeclass = self._dataset.getNameAndSizeList()[index.row()][1]
#                     return QtCore.QVariant(sizeclass.get('Size class', ''))
#                 if index.column() == 2:
#                     peg = self._dataset.getNameAndSizeList()[index.row()][0]
#                     return QtCore.QVariant(peg.get('Dyntaxa id', ''))
#                 if index.column() == 3:
#                     peg = self._dataset.getNameAndSizeList()[index.row()][0]
#                     dyntaxaresource = toolbox_resources.ToolboxResources().get_resource_dyntaxa()
#                     dyntaxa = dyntaxaresource.getTaxonById(peg.get('Dyntaxa id', ''))
#                     if dyntaxa:
#                         return QtCore.QVariant(dyntaxa.get('Scientific name', ''))
#                     else:
#                         return QtCore.QVariant()
#         return QtCore.QVariant()

