#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import pathlib
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import plankton_core
import app_framework
import toolbox_utils


class DatasetViewerTool(app_framework.ToolBase):
    """ """

    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other
        # initialization since the base class calls _create_content().
        super(DatasetViewerTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea
            | QtCore.Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.setBaseSize(600, 600)
        # Filename used when saving data to file.
        self._lastuseddirectory = app_framework.ToolboxUserSettings().home_for_mac()

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_select_dataset())
        contentLayout.addLayout(self._content_result_table())
        contentLayout.addWidget(self._content_save_result())

        # Listen for changes in the toolbox dataset list.
        app_framework.ToolboxDatasets().datasetListChanged.connect(
            self._update_dataset_list
        )

        # Allow synch is confusing. Activate again when used in more tools.
        # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)
        # Listen for changes in the toolbox sync.
        app_framework.AppSync().selected_row_changed.connect(self._set_selected_dataset)

    def _content_select_dataset(self):
        """ """
        # Active widgets and connections.
        self._selectdataset_list = QtWidgets.QComboBox()
        self._selectdataset_list.setSizeAdjustPolicy(
            QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self._selectdataset_list.addItems(["<select dataset>"])
        self._selectdataset_list.currentIndexChanged.connect(self._view_dataset)
        #
        self._numberofrows_label = QtWidgets.QLabel("Number of rows: 0")

        # Allow synch is confusing. Activate again when used in more tools.
        #         self._allowsync_checkbox = QtWidgets.QCheckBox('Allow synch')
        #         self._allowsync_checkbox.setChecked(False)
        # Layout widgets.
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Imports:"))
        layout.addWidget(self._selectdataset_list)
        #         layout.addWidget(self._allowsync_checkbox)
        layout.addStretch(5)
        layout.addWidget(self._numberofrows_label)
        #
        return layout

    def _content_result_table(self):
        """ """
        # Active widgets and connections.
        self._tableview = app_framework.ToolboxQTableView()
        # Layout widgets.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._tableview)
        #
        return layout

    def _content_save_result(self):
        """ """
        saveresultbox = QtWidgets.QGroupBox("Export dataset", self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtWidgets.QPushButton("Copy to clipboard")
        self._copytoclipboard_button.clicked.connect(self._copy_to_clipboard)
        self._saveformat_list = QtWidgets.QComboBox()
        self._saveformat_list.addItems(
            ["Tab delimited text file (*.txt)", "Excel file (*.xlsx)"]
        )
        self._savedataset_button = QtWidgets.QPushButton("Save...")
        self._savedataset_button.clicked.connect(self._save_data)
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
        #         hbox1.addStretch(10)
        hbox1.addWidget(QtWidgets.QLabel("        File format:"))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        hbox1.addStretch(10)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox

    def _update_dataset_list(self):
        """ """
        try:
            self._selectdataset_list.clear()
            self._selectdataset_list.addItems(["<select dataset>"])

            for rowindex, dataset in enumerate(
                app_framework.ToolboxDatasets().get_datasets()
            ):
                self._selectdataset_list.addItems(["Import-" + str(rowindex + 1)])
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _view_dataset(self, index):
        """ """
        try:
            if index <= 0:
                # Clear table.
                self._tableview.clearModel()
                self._refresh_result_table()
            else:
                # envmonlib:
                dataset = app_framework.ToolboxDatasets().get_dataset_by_index(
                    index - 1
                )
                if isinstance(dataset, plankton_core.DatasetTable):
                    self._tableview.setTableModel(dataset)
                    self._refresh_result_table()
                elif isinstance(dataset, plankton_core.DatasetNode):
                    # Tree dataset must be converted to table dataset before viewing.
                    targetdataset = plankton_core.DatasetTable()
                    dataset.convert_to_table_dataset(targetdataset)
                    #
                    self._tableview.setTableModel(targetdataset)
                    self._refresh_result_table()
                #
                # TODO: Remove later. Default alternative used for non toolbox_utils.
                else:
                    self._tableview.setTableModel(dataset)
                    self._refresh_result_table()
            #
            if self._tableview.getTableModel():
                self._numberofrows_label.setText(
                    "Number of rows: "
                    + str(self._tableview.getTableModel().get_row_count())
                )
            else:
                self._numberofrows_label.setText("Number of rows: 0")
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_data(self):
        """ """
        try:
            #         if self._tableview.getTableModel().getModeldata():
            if self._tableview.getTableModel():
                # Show select file dialog box.
                namefilter = "All files (*.*)"
                if self._saveformat_list.currentIndex() == 1:  # Xlsx file.
                    namefilter = "Excel files (*.xlsx);;All files (*.*)"
                else:
                    namefilter = "Text files (*.txt);;All files (*.*)"
                filename, _filters = QtWidgets.QFileDialog.getSaveFileName(
                    self, "Export dataset", self._lastuseddirectory, namefilter
                )
                filename = str(filename)  # QString to str.
                # Check if user pressed ok or cancel.
                if filename:
                    self._lastuseddirectory = str(pathlib.Path(filename).parents[0])
                    if self._saveformat_list.currentIndex() == 0:  # Text file.
                        #                     self._tableview.getTableModel().getModeldata().saveAsTextFile(filename)
                        self._tableview.getTableModel().save_as_file(
                            text_file_name=filename
                        )
                    elif self._saveformat_list.currentIndex() == 1:  # Excel file.
                        #                     self._tableview.getTableModel().getModeldata().saveAsExcelFile(filename)
                        self._tableview.getTableModel().save_as_file(
                            excel_file_name=filename
                        )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _copy_to_clipboard(self):
        """ """
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            field_separator = "\t"
            row_separator = "\r\n"
            clipboardstring = ""
            #
            #         table_dataset = self._tableview.getTableModel().getModeldata()
            table_dataset = self._tableview.getTableModel()
            if table_dataset:
                # Header.
                clipboardstring = (
                    field_separator.join(map(str, table_dataset.get_header()))
                    + row_separator
                )
                # Rows.
                for row in table_dataset.get_rows():
                    clipboardstring += (
                        field_separator.join(map(str, row)) + row_separator
                    )
            #
            clipboard.setText(clipboardstring)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _refresh_result_table(self):
        """ """
        try:
            self._tableview.resetModel()  # Model data has changed.
            self._tableview.resizeColumnsToContents()
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    # Allow synch is confusing. Activate again when used in more tools.
    # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)
    def _set_selected_dataset(self):
        """ """
        try:
            index = app_framework.AppSync().get_row_index("dataset")
            self._selectdataset_list.setCurrentIndex(index + 1)
            self._view_dataset(index + 1)
        #         if self._allowsync_checkbox.isChecked():
        #             index = toolbox_sync.ToolboxSync().get_row_index('dataset')
        #             self._selectdataset_list.setCurrentIndex(index + 1)
        #             self._view_dataset(index + 1)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
