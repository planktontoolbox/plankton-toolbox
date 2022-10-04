#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import sys
from PyQt6 import QtWidgets

import plankton_core
import toolbox_utils
import app_framework


class PlanktonCounterSampleEdit(QtWidgets.QWidget):
    """ """

    def __init__(self, parentwidget, dataset, sample, current_sample_object):
        """ """
        self._parentwidget = parentwidget
        self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        #
        super(PlanktonCounterSampleEdit, self).__init__()
        #
        self.setLayout(self._create_content_sample_edit())
        #
        self.sample_locked = True
        self.set_read_only()
        #

    #         self.load_data()

    def load_data(self):
        """ """
        try:
            self._load_edit_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def save_data(self):
        """ """

    #         if not self.sample_locked:
    #         try:
    #         # self._save_edit_table() # Don't save when tab in plankton_counter_dialog changed.
    #         #
    #         except Exception as e:
    #             debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
    #             toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def clear(self):
        """ """
        try:
            self._sampletable_table.clear()
            self._sampletable_editable.setTableModel(self._sampletable_table)
            self._sampletable_editable.resizeColumnsToContents()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _create_content_sample_edit(self):
        """ """
        contentlayout = QtWidgets.QVBoxLayout()
        #
        contentlayout.addWidget(self._content_info(), 1)
        contentlayout.addWidget(self._content_table(), 100)
        contentlayout.addWidget(self._content_end(), 1)
        #
        return contentlayout

    # ===== COUNTER DATASETS =====
    def _content_info(self):
        """ """
        widget = QtWidgets.QWidget()
        #
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        # Empty row.
        form1.addWidget(QtWidgets.QLabel(""), gridrow, 0, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        #         layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget

    # ===== COUNTER DATASETS =====
    def _content_table(self):
        """ """
        widget = QtWidgets.QWidget()
        #         widget = QtWidgets.QGroupBox('Plankton counter - sample editor', self._parentwidget)
        #
        self._sampletable_editable = app_framework.ToolboxEditableQTableView()
        self._sampletable_table = plankton_core.DatasetTable()
        self._sampletable_editable.setTableModel(self._sampletable_table)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._sampletable_editable)
        widget.setLayout(layout)
        #
        return widget

    def _content_end(self):
        """ """
        widget = QtWidgets.QWidget()
        self._exportsamplereport_button = QtWidgets.QPushButton(
            "Export sample (.xlsx)..."
        )
        self._exportsamplereport_button.clicked.connect(self._save_sample_report)
        self._save_button = QtWidgets.QPushButton("Save edited changes")
        self._save_button.clicked.connect(self._save_edit_table)
        #
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._exportsamplereport_button)
        #         layout.addStretch(10)
        #         layout.addWidget(self._load_button)
        layout.addWidget(self._save_button)
        #         layout.addWidget(self._clear_button)
        layout.addStretch(10)
        widget.setLayout(layout)
        #
        return widget

    def set_read_only(self, read_only=True):
        """ """
        if (not self.sample_locked) and read_only:
            # Save sample before locking.
            self.save_data()
        #
        self.sample_locked = read_only
        #
        enabled = not read_only
        #         self._sampletable_table
        self._save_button.setEnabled(enabled)
        self._sampletable_editable.setEnabled(enabled)

    def _load_edit_table(self):
        """ """
        try:
            self.clear()
            #
            header, rows = self._current_sample_object.get_sample_header_and_rows()
            self._sampletable_table.set_header(header)
            for row in rows:
                if len("".join(row)) > 0:
                    self._sampletable_table.append_row(row)
            #
            self._sampletable_editable.setTableModel(self._sampletable_table)
            self._sampletable_editable.resizeColumnsToContents()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_edit_table(self):
        """ """
        try:
            header = self._sampletable_table.get_header()
            rows = self._sampletable_table.get_rows()
            #
            self._current_sample_object.update_all_sample_rows(header, rows)
            #
            #         self._current_sample_object.recalculate_sample_data(self._current_sample_method)
            self._current_sample_object.save_sample_data()
            #
            self._load_edit_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_sample_report(self):
        """ """
        try:
            dialog = ExportSampleDialog(
                self, self._current_sample, self._current_sample_object
            )
            if dialog.exec():
                pass
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))


class ExportSampleDialog(QtWidgets.QDialog):
    """ """

    def __init__(self, parentwidget, sample, current_sample_object):
        """ """
        #         self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        super(ExportSampleDialog, self).__init__(parentwidget)
        self.setWindowTitle("Export sample to Excel")
        self.setLayout(self._content())
        self.setMinimumSize(800, 100)

    def _content(self):
        """ """
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._content_export())
        #
        return layout

    def _content_export(self):
        """ """
        widget = QtWidgets.QWidget()
        self._exporttargetdir_edit = QtWidgets.QLineEdit("")
        self._exporttargetdir_button = QtWidgets.QPushButton("Browse...")
        self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
        self._exporttargetfilename_edit = QtWidgets.QLineEdit(
            self._current_sample + ".xlsx"
        )

        self._export_button = QtWidgets.QPushButton("Export")
        self._export_button.clicked.connect(self._export_dataset)
        self._exportcancel_button = QtWidgets.QPushButton("Cancel")
        self._exportcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label2 = QtWidgets.QLabel("Export to directory:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._exporttargetdir_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtWidgets.QLabel("Export file name:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetfilename_edit, gridrow, 1, 1, 9)
        gridrow += 1
        # Empty row.
        form1.addWidget(QtWidgets.QLabel(""), gridrow, 0, 1, 1)
        gridrow += 1
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._export_button)
        hbox1.addWidget(self._exportcancel_button)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget

    def _browse_target_dir(self):
        """ """
        try:
            dirdialog = QtWidgets.QFileDialog(self)
            dirdialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
            dirdialog.setOptions(QtWidgets.QFileDialog.Option.ShowDirsOnly)
            dirdialog.setDirectory(str(self._exporttargetdir_edit.text()))
            dirpath = dirdialog.getExistingDirectory()
            if dirpath:
                self._exporttargetdir_edit.setText(dirpath)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _export_dataset(self):
        """ """
        try:
            # Export path and file name.
            export_target_dir = str(self._exporttargetdir_edit.text())
            export_target_filename = str(self._exporttargetfilename_edit.text())
            # Warning.
            if pathlib.Path(export_target_dir, export_target_filename).exists():
                box_result = QtWidgets.QMessageBox.warning(
                    self,
                    "Warning",
                    "Excel file already exists. Do you want ro replace it?",
                    QtWidgets.QMessageBox.StandardButton.Cancel,
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )
                if box_result == QtWidgets.QMessageBox.StandardButton.Ok:
                    self._current_sample_object.export_sample_to_excel(
                        export_target_dir, export_target_filename
                    )
            else:
                self._current_sample_object.export_sample_to_excel(
                    export_target_dir, export_target_filename
                )
            #
            self.accept()  # Close dialog box.
        #
        except Exception as e:
            toolbox_utils.Logging().error("Failed to export sample. " + str(e))
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Failed to export sample. " + str(e)
            )
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
