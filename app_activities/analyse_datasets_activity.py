#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import os.path
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import toolbox_utils
import plankton_core
import app_framework
import app_activities


class AnalyseDatasetsActivity(app_framework.ActivityBase):
    """ """

    def __init__(self, name, parentwidget):
        """ """
        # Create object containing analysis data.
        self._analysisdata = plankton_core.AnalysisData()
        self._statisticaldata = plankton_core.StatisticalData()
        self._reportdata = plankton_core.ReportData()

        # Filename used when saving data to file.
        self._lastuseddirectory = "."
        # Create tab widgets.
        self._tab1widget = app_activities.analyse_datasets_tab1.AnalyseDatasetsTab1()
        self._tab2widget = app_activities.analyse_datasets_tab2.AnalyseDatasetsTab2()
        self._tab3widget = app_activities.analyse_datasets_tab3.AnalyseDatasetsTab3()
        self._tab4widget = app_activities.analyse_datasets_tab4.AnalyseDatasetsTab4()
        self._tab5widget = app_activities.analyse_datasets_tab5.AnalyseDatasetsTab5()
        self._tab6widget = app_activities.analyse_datasets_tab6.AnalyseDatasetsTab6()
        self._tab7widget = app_activities.analyse_datasets_tab7.AnalyseDatasetsTab7()
        self._tab8widget = app_activities.analyse_datasets_tab8.AnalyseDatasetsTab8()
        #
        self._tab1widget.set_main_activity(self)
        self._tab2widget.set_main_activity(self)
        self._tab3widget.set_main_activity(self)
        self._tab4widget.set_main_activity(self)
        self._tab5widget.set_main_activity(self)
        self._tab6widget.set_main_activity(self)
        self._tab7widget.set_main_activity(self)
        self._tab8widget.set_main_activity(self)
        # Initialize parent.
        super(AnalyseDatasetsActivity, self).__init__(name, parentwidget)
        #
        self._empty_dataset_table = plankton_core.DatasetTable()

    def get_analysis_data(self):
        """ """
        return self._analysisdata

    def get_statistical_data(self):
        """ """
        return self._statisticaldata

    def get_report_data(self):
        """ """
        return self._reportdata

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
        self._activityheader.setText("<h2>" + self.objectName() + "</h2>")
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_analyse_tabs(), 3)
        contentLayout.addWidget(self._content_analysis_data_table(), 10)
        contentLayout.addWidget(self._content_save_analysis_data())

    def _content_analyse_tabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtWidgets.QGroupBox("", self)
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(
            self._tab1widget.content_select_datasets(), "Select dataset(s)"
        )
        tabWidget.addTab(self._tab2widget.content_prepare_data(), "Clean up")
        tabWidget.addTab(
            self._tab3widget.content_aggregate_data(), "Aggregate/complement data"
        )
        tabWidget.addTab(self._tab4widget.content_select_data(), "Filter")
        tabWidget.addTab(
            self._tab5widget.content_predefined_graphs(), "Predefined graphs"
        )
        tabWidget.addTab(self._tab6widget.content_generic_graphs(), "Generic graphs")
        tabWidget.addTab(self._tab7widget.content_statistics(), "Statistics")
        tabWidget.addTab(self._tab8widget.content_reports(), "Exports")
        # Layout widgets.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)
        #
        return selectdatabox

    # ===== ANALYSIS DATA =====
    def _content_analysis_data_table(self):
        """ """
        # Active widgets and connections.
        analysisdatagroupbox = QtWidgets.QGroupBox(
            "Analysis data, filtered data, statistical data and export data", self
        )
        # Active widgets and connections.
        self._viewdata_list = QtWidgets.QComboBox()
        self._viewdata_list.addItems(
            [
                "Analysis data",
                "Filtered analysis data",
                "Statistical data",
                "Export data",
                "Hide data (to increase performance)",
            ]
        )
        self._viewdata_list.currentIndexChanged.connect(self._view_data_list_changed)
        #
        self._numberofrows_label = QtWidgets.QLabel("Number of rows: 0")
        #
        #        self._hidedata_checkbox = QtWidgets.QCheckBox('Hide data')
        #        self._hidedata_checkbox.setChecked(False)
        #        self._hidedata_checkbox.clicked.connect(self._view_hide_data_changed)
        #
        self._refreshfiltereddata_button = QtWidgets.QPushButton(
            "Refresh filtered data"
        )  # TODO:
        self._refreshfiltereddata_button.hide()
        self._refreshfiltereddata_button.clicked.connect(self._refresh_filtered_data)
        #
        self._tableview = app_framework.ToolboxQTableView()
        # Layout widgets.
        layout = QtWidgets.QVBoxLayout()
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(QtWidgets.QLabel("View:"))
        hbox1.addWidget(self._viewdata_list)
        #        hbox1.addWidget(self._hidedata_checkbox)
        hbox1.addWidget(self._refreshfiltereddata_button)
        hbox1.addStretch(5)
        hbox1.addWidget(self._numberofrows_label)
        #
        layout.addLayout(hbox1)
        layout.addWidget(self._tableview)
        #
        analysisdatagroupbox.setLayout(layout)
        #
        return analysisdatagroupbox

    def _view_data_list_changed(self, row_index):
        """ """
        try:
            if row_index == 1:
                self._refreshfiltereddata_button.show()
            else:
                self._refreshfiltereddata_button.hide()
            #
            self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _refresh_filtered_data(self):
        """ """
        try:
            # Note: row_index used inside update_viewed_data().
            self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _view_hide_data_changed(self):
        """ """
        try:
            self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _content_save_analysis_data(self):
        """ """
        try:
            saveresultbox = QtWidgets.QGroupBox("Export data", self)
            # Active widgets and connections.
            self._copytoclipboard_button = QtWidgets.QPushButton("Copy to clipboard")
            self._copytoclipboard_button.clicked.connect(self._copy_to_clipboard)
            self._saveformat_list = QtWidgets.QComboBox()
            self._saveformat_list.addItems(
                ["Tab delimited text file (*.txt)", "Excel file (*.xlsx)"]
            )
            self._savedataset_button = QtWidgets.QPushButton("Save...")
            self._savedataset_button.clicked.connect(self._save_analysis_data)
            # Layout widgets.
            hbox1 = QtWidgets.QHBoxLayout()
            hbox1.addWidget(self._copytoclipboard_button)
            #         hbox1.addStretch(5)
            hbox1.addWidget(QtWidgets.QLabel("        File format:"))
            hbox1.addWidget(self._saveformat_list)
            hbox1.addWidget(self._savedataset_button)
            hbox1.addStretch(5)
            #
            saveresultbox.setLayout(hbox1)
            #
            return saveresultbox
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    #     def set_analysis_data(self, analysis_data):
    #         """ """
    #         self._analysisdata = analysis_data
    #         self.update_viewed_data()
    #         self.update_all_tabs()

    def update_viewed_data_and_tabs(self):
        """ """
        try:
            self.update_viewed_data()
            self.update_all_tabs()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def hide_viewed_data(self):
        """ """
        try:
            # Clear table.
            self._tableview.setTableModel(self._empty_dataset_table)
            self._refresh_viewed_data_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def update_viewed_data(self):
        """ """
        try:
            # Clear table.
            self._tableview.setTableModel(self._empty_dataset_table)
            self._refresh_viewed_data_table()
            self._numberofrows_label.setText("Number of rows: 0")
            #
            if not self._analysisdata.get_data():
                return
            #
            selectedviewindex = self._viewdata_list.currentIndex()
            if selectedviewindex == 0:
                # View analysis data.
                # Convert from tree model to table model.
                targetdataset = plankton_core.DatasetTable()
                self._analysisdata.get_data().convert_to_table_dataset(targetdataset)
                # View model.
                self._tableview.setTableModel(targetdataset)
                self._refresh_viewed_data_table()
            elif selectedviewindex == 1:
                # View filtered data only.
                self._tab4widget.update_filter()  # Must be done before create_filtered_dataset().
                filtereddataset = self._analysisdata.create_filtered_dataset()
                # Convert from tree model to table model.
                targetdataset = plankton_core.DatasetTable()
                filtereddataset.convert_to_table_dataset(targetdataset)
                # View model.
                self._tableview.setTableModel(targetdataset)
                self._refresh_viewed_data_table()
            elif selectedviewindex == 2:
                # Statistical data.
                self._tableview.setTableModel(self._statisticaldata.get_data())
                self._refresh_viewed_data_table()
            elif selectedviewindex == 3:
                # Export data.
                self._tableview.setTableModel(self._reportdata.get_data())
                self._refresh_viewed_data_table()
            else:
                # Hide data.
                self._tableview.setTableModel(self._empty_dataset_table)
                self._refresh_viewed_data_table()
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

    def _refresh_viewed_data_table(self):
        """ """
        try:
            self._tableview.resetModel()  # Model data has changed.
            self._tableview.resizeColumnsToContents()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_analysis_data(self):
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
                    self._lastuseddirectory = os.path.dirname(filename)
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

    def clear_all_tabs(self):
        """ """
        try:
            self._tab1widget.clear()
            self._tab2widget.clear()
            self._tab3widget.clear()
            self._tab4widget.clear()
            self._tab5widget.clear()
            self._tab6widget.clear()
            self._tab7widget.clear()
            self._tab8widget.clear()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def update_all_tabs(self):
        """ """
        try:
            self._tab1widget.update()
            self._tab2widget.update()
            self._tab3widget.update()
            self._tab4widget.update()
            self._tab5widget.update()
            self._tab6widget.update()
            self._tab7widget.update()
            self._tab8widget.update()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def update_filter(self):
        """Must be done before calls to create_filtered_dataset()."""
        try:
            self._tab4widget.update_filter()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def view_analysis_data(self):
        """ """
        try:
            if self._viewdata_list.currentIndex() < 4:  # 4 = hide.
                self._viewdata_list.setCurrentIndex(0)
                self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def view_statistical_data(self):
        """ """
        try:
            if self._viewdata_list.currentIndex() < 4:  # 4 = hide.
                self._viewdata_list.setCurrentIndex(2)
                self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def view_report_data(self):
        """ """
        try:
            if self._viewdata_list.currentIndex() < 4:  # 4 = hide.
                self._viewdata_list.setCurrentIndex(3)
                self.update_viewed_data()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
