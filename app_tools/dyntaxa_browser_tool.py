#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# from PyQt6 import QtWidgets
# from PyQt6 import QtCore
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.tools.tool_base as tool_base
# import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources
#
# class DyntaxaBrowserTool(tool_base.ToolBase):
#     """
#     """
#
#     def __init__(self, name, parentwidget):
#         """ """
#         # Create model.
#         self._dyntaxa_object = toolbox_resources.ToolboxResources().get_resource_dyntaxa()
#         # Initialize parent. Should be called after other
#         # initialization since the base class calls _create_content().
#         super(DyntaxaBrowserTool, self).__init__(name, parentwidget)
#         #
#         # Where is the tool allowed to dock in the main window.
#         self.setAllowedAreas(QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
#         self.setBaseSize(600,600)
#
#     def _create_content(self):
#         """ """
#         content = self._create_scrollable_content()
#         contentLayout = QtWidgets.QVBoxLayout()
#         content.setLayout(contentLayout)
#         contentLayout.addLayout(self._content_taxon_list())
#         contentLayout.addLayout(self._content_dyntaxa_item())
#         contentLayout.addLayout(self._content_dyntaxa_control())
#         # Used when toolbox resource has changed.
#         toolbox_resources.ToolboxResources().dyntaxaResourceLoaded.connect(self._dyntaxa_refresh)
#
#     def _content_taxon_list(self):
#         """ """
#         layout = QtWidgets.QVBoxLayout()
#         self._tableView = app_framework.ToolboxQTableView()
#         layout.addWidget(self._tableView)
#         # Data model.
#         self._model = DyntaxaTableModel(self._dyntaxa_object)
#         self._tableView.setTableModel(self._model)
#         #
#         self._tableView.getSelectionModel().currentChanged.connect(self._show_item_info)
#         self._tableView.getSelectionModel().selectionChanged.connect(self._show_item_info)
#         #
#         return layout
#
#     def _content_dyntaxa_item(self):
#         """ """
#         # Active widgets and connections.
#         # Species level.
#         self._scientificname_label = QtWidgets.QLabel('-')
# #        self._author_label = QtWidgets.QLabel('-')
#         self._classification_label = QtWidgets.QLabel('-')
# #        self._author_label = QtWidgets.QLabel('-')
# #        self._class_label = QtWidgets.QLabel('-')
# #        self._division_label = QtWidgets.QLabel('-')
# #        self._order_label = QtWidgets.QLabel('-')
# #        # Sizeclass level.
# #        self._size_class_label = QtWidgets.QLabel('-')
# #        self._trophic_type_label = QtWidgets.QLabel('-')
# #        self._shape_label = QtWidgets.QLabel('-')
# #        self._formula_label = QtWidgets.QLabel('-')
# #        self._volume_label = QtWidgets.QLabel('-')
# #        self._carbon_label = QtWidgets.QLabel('-')
#         # Layout widgets.
#         layout = QtWidgets.QFormLayout()
# #        layout.addRow('<b><u>Species:</u></b>", None)
#         layout.addRow('Scientific name:', self._scientificname_label)
# #        layout.addRow('Author:", self._author_label)
#         layout.addRow('Classification:', self._classification_label)
# #        layout.addRow('Author:", self._author_label)
# #        layout.addRow('Class:", self._class_label)
# #        layout.addRow('Division:", self._division_label)
# #        layout.addRow('Order:", self._order_label)
# #        layout.addRow('<b><u>Size class:</u></b>", None)
# #        layout.addRow('Size class:", self._size_class_label)
# #        layout.addRow('Trophic type:", self._trophic_type_label)
# #        layout.addRow('Geometric shape:", self._shape_label)
# #        layout.addRow('Formula:", self._formula_label)
# #        layout.addRow('Calculated volume:", self._volume_label)
# #        layout.addRow('Calculated carbon:", self._carbon_label)
#         #
#         return layout
#
#     def _content_dyntaxa_control(self):
#         """ """
#         # Active widgets and connections.
#         self._loadresource_button = QtWidgets.QPushButton('Load Dyntaxa resource')
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
# #        name_index = self._model.createIndex(index.row(), 0)
# #        size_index = self._model.createIndex(index.row(), 1)
# #        taxonName = self._model.data(name_index).toString()
# #        size = self._model.data(size_index).toString()
# ###        taxonName = self._dyntaxa_object.getData(index.row(), 0)
# ###        size = self._dyntaxa_object.getData(index.row(), 1)
#         #
#         taxon = self._dyntaxa_object.getSortedNameList()[index.row()]
#         self._scientificname_label.setText(
#             '<b>' +
#             '<i>' + taxon.get('Scientific name', '') + '</i>' +
#             '&nbsp;&nbsp;&nbsp;' + taxon.get('Scientific name author', '') +
#             '</b>')
#         # Build classification hierarchy.
#         hier = ''
#         delimiter = ''
#         name = taxon.get('Scientific name', None)
#         while name != None:
#             hier = name + delimiter + hier
#             delimiter = ' - '
#             name = None
#             parentid = taxon.get('Parent id', None)
#             taxon = self._dyntaxa_object.getTaxonById(parentid)
#             if taxon:
#                 name = taxon.get('Scientific name', None)
#             if len(hier) > 1000: # If infinite loops related to error in parent id.
#                 self._classification_label.setText('ERROR: Hierachy too long: ' + hier)
#                 print('ERROR: Hierachy too long: ' + hier)
#                 return
#         self._classification_label.setText(hier)
# #        self._author_label.setText(taxon.get('Author', '-'))
# #        self._class_label.setText(taxon.get('Class', '-'))
# #        self._division_label.setText(taxon.get('Division', '-'))
# #        self._order_label.setText(taxon.get('Order', '-'))
# #        #
# #        sizeclass = self._dyntaxa_object.getNameAndSizeList()[index.row()][1]
# #        self._size_class_label.setText('<b>' + str(sizeclass.get('Size class', '-')) + '</b>')
# #        self._trophic_type_label.setText(sizeclass.get('Trophic type', '-'))
# #        self._shape_label.setText(sizeclass.get('Geometric shape', '-'))
# #        self._formula_label.setText(sizeclass.get('Formula', '-'))
# #        self._volume_label.setText(str(sizeclass.get('Calculated volume, um3', '-')))
# #        self._carbon_label.setText(str(sizeclass.get('Calculated Carbon pg/counting unit', '-')))
#
#     def _load_resource(self):
#         """ """
#         toolbox_resources.ToolboxResources().load_resource_dyntaxa()
#
#     def _dyntaxa_refresh(self):
#         """ """
#         self._tableView.resetModel()
#         self._tableView.resizeColumnsToContents() # TODO: Check if time-consuming...
#
# ##############################################################
# class DyntaxaTableModel(QtCore.QAbstractTableModel):
#     """
#     """
#     def __init__(self, dataset):
#         self._dataset = dataset
# #        self._nameandsizelist = self._dataset.getNameAndSizeList()
#         # Initialize parent.
#         super(DyntaxaTableModel, self).__init__()
#
#     def set_dataset(self, dataset):
#         """ """
#         self._dataset = dataset
#
#     def rowCount(self, parent=QtCore.QModelIndex()):
#         """ """
#         if self._dataset:
#             return len(self._dataset.getSortedNameList())
#         else:
#             return 0
#
#     def columnCount(self, parent=QtCore.QModelIndex()):
#         """ """
#         return 6
#
#     def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
#         """ Overridden abstract method.
#             Columns: Dyntaxa id, Dyntaxa name. """
#         if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#             if section == 0:
#                 return QtCore.QVariant('Dyntaxa id')
#             elif section == 1:
#                 return QtCore.QVariant('Scientific name')
#             elif section == 2:
#                 return QtCore.QVariant('Type')
#             elif section == 3:
#                 return QtCore.QVariant('Swedish')
#             elif section == 4:
#                 return QtCore.QVariant('ITIS')
#             elif section == 5:
#                 return QtCore.QVariant('ERMS')
#         if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
#             return QtCore.QVariant(section + 1)
#         return QtCore.QVariant()
#
#     def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
#         """ Overridden abstract method. """
#         if role == QtCore.Qt.DisplayRole:
#             if index.isValid():
#                 if index.column() == 0:
#                     sizeclass = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(sizeclass.get('Taxon id', ''))
#                 if index.column() == 1:
#                     taxon = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(taxon.get('Scientific name', ''))
#                 if index.column() == 2:
#                     taxon = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(taxon.get('Taxon type', ''))
#                 if index.column() == 3:
#                     taxon = self._dataset.getSortedNameList()[index.row()]
#                     for nameitem in taxon.get('Names', []):
#                         if nameitem['Name type'] == 'Swedish':
#                             return QtCore.QVariant(nameitem.get('Name', ''))
#                 if index.column() == 4:
#                     taxon = self._dataset.getSortedNameList()[index.row()]
#                     for nameitem in taxon.get('Names', []):
#                         if nameitem['Name type'] == 'ITIS-number':
#                             return QtCore.QVariant(nameitem.get('Name', ''))
#                 if index.column() == 5:
#                     taxon = self._dataset.getSortedNameList()[index.row()]
#                     for nameitem in taxon.get('Names', []):
#                         if nameitem['Name type'] == 'ERMS-name':
#                             return QtCore.QVariant(nameitem.get('Name', ''))
#         return QtCore.QVariant()
