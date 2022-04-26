#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import toolbox_utils
import plankton_core
import app_framework


class AnalyseDatasetsTab2(QtWidgets.QWidget):
    """ """

    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab2, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        try:
            self._main_activity = main_activity
            self._analysisdata = main_activity.get_analysis_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def clear(self):
        """ """
        try:
            self._column_list.clear()
            self._column_list.setEnabled(False)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def update(self):
        """ """
        try:
            self.clear()
            analysisdata = self._analysisdata.get_data()
            if analysisdata:
                # For tab "Generic graphs".
                self._column_list.addItems(
                    [item["header"] for item in analysisdata.get_export_table_columns()]
                )
                #  Make combo-boxes visible.
                self._column_list.setEnabled(True)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    # ===== TAB: Prepare data =====
    def content_prepare_data(self):
        """ """
        # Active widgets and connections.
        #         introlabel = app_framework.RichTextQLabel()
        #         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab2_intro'))
        #
        self._column_list = QtWidgets.QComboBox()
        self._column_list.setMinimumContentsLength(20)
        self._column_list.setSizeAdjustPolicy(
            QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self._column_list.setEnabled(False)
        #
        self._column_list.currentIndexChanged.connect(self._update_column_content)
        # Column content.
        self._content_listview = app_framework.SelectableQListView()
        #         self._content_listview.setMaximumHeight(100)
        #
        clearall_label = app_framework.ClickableQLabel("Clear all")
        markall_label = app_framework.ClickableQLabel("Mark all")
        clearall_label.label_clicked.connect(self._content_listview.uncheckAll)
        markall_label.label_clicked.connect(self._content_listview.checkAll)
        #
        self._keepdata_button = QtWidgets.QPushButton("Keep marked data")
        self._keepdata_button.clicked.connect(self._keep_data)
        self._removedata_button = QtWidgets.QPushButton("Remove marked data")
        self._removedata_button.clicked.connect(self._remove_data)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel("Column:")
        label2 = QtWidgets.QLabel("Content:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_listview, gridrow, 1, 5, 2)
        form1.addWidget(self._keepdata_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._removedata_button, gridrow, 3, 1, 1)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 1, 1, 1)
        form1.addWidget(markall_label, gridrow, 2, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
        #         layout.addWidget(introlabel)
        layout.addLayout(form1)
        #         layout.addStretch(5)
        self.setLayout(layout)
        #
        return self

    def _update_column_content(self, selected_row):
        """ """
        try:
            analysisdata = self._analysisdata.get_data()
            if not analysisdata:
                self._content_listview.clear()
                return  # Empty data.
            #
            columncontent_set = set()
            selectedcolumn = str(self._column_list.currentText())
            # Search for export column corresponding model element.
            nodelevel = ""
            key = ""
            for info_dict in analysisdata.get_export_table_columns():
                if info_dict["header"] == selectedcolumn:
                    nodelevel = info_dict["node"]
                    key = info_dict["key"]
                    break  # Break loop.
            #
            if nodelevel == "dataset":
                if key in analysisdata.get_data_dict().keys():
                    columncontent_set.add(str(analysisdata.get_data(key)))
                else:
                    columncontent_set.add("")  # Add empty field.
            #
            for visitnode in analysisdata.get_children():
                if nodelevel == "visit":
                    if key in visitnode.get_data_dict().keys():
                        columncontent_set.add(str(visitnode.get_data(key)))
                    else:
                        columncontent_set.add("")  # Add empty field.
                    continue
                #
                for samplenode in visitnode.get_children():
                    if nodelevel == "sample":
                        if key in samplenode.get_data_dict().keys():
                            columncontent_set.add(str(samplenode.get_data(key)))
                        else:
                            columncontent_set.add("")  # Add empty field.
                        continue
                    #
                    for variablenode in samplenode.get_children():
                        if nodelevel == "variable":
                            if key in variablenode.get_data_dict().keys():
                                columncontent_set.add(str(variablenode.get_data(key)))
                            else:
                                columncontent_set.add("")  # Add empty field.
                            continue
                # Content list.
            self._content_listview.setList(sorted(columncontent_set))
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _keep_data(self):
        """ """
        try:
            self._remove_data(keep_data=True)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _remove_data(self, keep_data=False):
        """ """
        try:
            selectedcolumn = str(self._column_list.currentText())
            #
            if keep_data == False:
                markedcontent = self._content_listview.getSelectedDataList()
            else:
                markedcontent = (
                    self._content_listview.getNotSelectedDataList()
                )  # Note: "Not-selected" list.
            #
            self._analysisdata.remove_data(selectedcolumn, markedcontent)
            #
            self._main_activity.update_viewed_data_and_tabs()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
