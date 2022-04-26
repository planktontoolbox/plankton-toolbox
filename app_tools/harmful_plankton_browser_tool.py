#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# from PyQt6 import QtWidgets
# from PyQt6 import QtCore
# import webbrowser
# import toolbox_utils
# import plankton_core
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.tools.tool_base as tool_base
# import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources
#
# class HarmfulPlanktonBrowserTool(tool_base.ToolBase):
#     """
#     """
#
#     def __init__(self, name, parentwidget):
#         """ """
#         # Create model.
#         self._harmfulplankton_object = toolbox_resources.ToolboxResources().get_resource_harmful_plankton()
#         self._marinespecies_url = None
#         # Initialize parent. Should be called after other
#         # initialization since the base class calls _create_content().
#         super(HarmfulPlanktonBrowserTool, self).__init__(name, parentwidget)
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
#         contentLayout.addLayout(self._content_item())
#         contentLayout.addLayout(self._content_control())
#         # Used when toolbox resource has changed.
#         toolbox_resources.ToolboxResources().harmfulPlanktonResourceLoaded.connect(self._harmful_plankton_refresh)
#
#     def _content_taxon_list(self):
#         """ """
#         layout = QtWidgets.QVBoxLayout()
#         self._tableView = app_framework.ToolboxQTableView()
#         layout.addWidget(self._tableView)
#         # Data model.
#         self._model = HarmfulPlanktonTableModel(self._harmfulplankton_object)
#         self._tableView.setTableModel(self._model)
#         #
#         self._tableView.getSelectionModel().currentChanged(QModelIndex, QModelIndex)'), self._show_item_info)
#         self._tableView.getSelectionModel().selectionChanged(QModelIndex, QModelIndex)'), self._show_item_info)
#         #
#         return layout
#
#     def _content_item(self):
#         """ """
#         # Active widgets and connections.
#         self._scientificname_label = QtWidgets.QLabel('-')
#         # Layout widgets.
#         form = QtWidgets.QFormLayout()
#         form.addRow('Scientific name:', self._scientificname_label)
# #        hbox = QtWidgets.QHBoxLayout()
# #        hbox.addWidget(self._openmarinespecies)
# #        hbox.addStretch(5)
#         layout = QtWidgets.QVBoxLayout()
#         layout.addLayout(form)
# #        layout.addLayout(hbox)
#         #
#         return layout
#
#     def _content_control(self):
#         """ """
#         # Active widgets and connections.
#         self._loadresource_button = QtWidgets.QPushButton('Load harmful plankton resource')
#         self._loadresource_button.clicked.connect(self._load_resource)
#         self._openmarinespecies = QtWidgets.QPushButton('Open marinespecies.org')
#         self._openmarinespecies.clicked.connect(self._open_marine_species)
#         # Layout widgets.
#         layout = QtWidgets.QHBoxLayout()
#         layout.addWidget(self._openmarinespecies)
#         layout.addStretch(5)
#         layout.addWidget(self._loadresource_button)
#         #
#         return layout
#
#     def _show_item_info(self, index):
#         """ """
#         #
#         taxon = self._harmfulplankton_object.getSortedNameList()[index.row()]
#         self._scientificname_label.setText(
#             '<b>' +
#             '<i>' + taxon.get('Scientific name', '') + '</i>' +
#             '&nbsp;&nbsp;&nbsp;' + taxon.get('Author', '') +
#             '</b>')
#         self._marinespecies_url = \
#                 'http://www.marinespecies.org/' + \
#                 'hab/aphia.php?p=taxdetails&id=' + \
#                 str(taxon['Aphia id'])
#
#
#     def _open_marine_species(self):
#         """ Launch web browser and use show marked species at marinespecies.org. """
#         if not self._marinespecies_url:
#             toolbox_utils.Logging().log('Failed to open www.marinespecies.org. No row selected.')
#             return
#         webbrowser.open(self._marinespecies_url)
#
#     def _load_resource(self):
#         """ """
#         # All resources are needed.
#         toolbox_resources.ToolboxResources().load_unloaded_resource_dyntaxa()
#         toolbox_resources.ToolboxResources().load_resource_harmful_plankton()
#
#     def _harmful_plankton_refresh(self):
#         """ """
#         self._marinespecies_url = None
#         self._tableView.resetModel()
#         self._tableView.resizeColumnsToContents() # Only visible columns.
#
# class HarmfulPlanktonTableModel(QtCore.QAbstractTableModel):
#     """
#     Example:
#             {
#                 "Aphia id": 246835,
#                 "Author": "Balech, 1990",
#                 "Scientific name": "Alexandrium andersonii"
#             },...
#
#     """
#     def __init__(self, dataset):
#         self._dataset = dataset
# #        self._nameandsizelist = self._dataset.getNameAndSizeList()
#         # Initialize parent.
#         super(HarmfulPlanktonTableModel, self).__init__()
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
#         return 4
#
#     def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
#         """ Overridden abstract method.
#             Columns: Taxon, Sizeclass. """
#         if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#             if section == 0:
#                 return QtCore.QVariant('Scientific name')
#             elif section == 1:
#                 return QtCore.QVariant('Aphia id')
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
#                     harmfulplankton = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(harmfulplankton.get('Scientific name', ''))
#                 if index.column() == 1:
#                     sizeclass = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(sizeclass.get('Aphia id', ''))
#                 if index.column() == 2:
#                     harmfulplankton = self._dataset.getSortedNameList()[index.row()]
#                     return QtCore.QVariant(harmfulplankton.get('Dyntaxa id', ''))
#                 if index.column() == 3:
#                     harmfulplankton = self._dataset.getSortedNameList()[index.row()]
#                     dyntaxaresource = toolbox_resources.ToolboxResources().get_resource_dyntaxa()
#                     dyntaxa = dyntaxaresource.getTaxonById(harmfulplankton.get('Dyntaxa id', ''))
#                     if dyntaxa:
#                         return QtCore.QVariant(dyntaxa.get('Scientific name', ''))
#                     else:
#                         return QtCore.QVariant()
#         return QtCore.QVariant()
