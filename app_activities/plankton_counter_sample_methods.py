#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import os
import sys
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import plankton_core
import app_framework
import toolbox_utils


class PlanktonCounterSampleMethods(QtWidgets.QWidget):
    """ """

    def __init__(self, parentwidget, dataset, sample, current_sample_object):
        """ """
        self._parentwidget = parentwidget
        self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        self._current_sample_method = None
        self._dont_update_current_sample_method_flag = False
        #
        super(PlanktonCounterSampleMethods, self).__init__()
        #
        self._selectdefaultmethod_list = None
        self._selectmethod_list = None
        self._selectmethod_table = None
        self._selectmethodstep_table = None
        #
        self.setLayout(self._create_content_methods())
        #
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(200, self.load_data)
        #
        self.sample_locked = True
        self.set_read_only()
        #

    #         self.load_data()

    def load_data(self):
        """Load data from method stored in sample."""
        try:
            self._update_default_method_list()
            self._update_counting_species_list()
            self._load_current_sample_method()
            #         self._select_default_method_changed()
            self._reset_default_method_values()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def save_data(self):
        """Save data to method stored in sample."""
        if not self.sample_locked:
            try:
                self._save_method_to_current_sample()
            #
            except Exception as e:
                debug_info = (
                    self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
                )
                toolbox_utils.Logging().error(
                    "Exception: (" + debug_info + "): " + str(e)
                )

    def _load_current_sample_method(self):
        """ """
        try:
            sample_path = self._current_sample_object.get_dir_path()
            if os.path.exists(os.path.join(sample_path, "counting_method.txt")):
                (
                    header,
                    rows,
                ) = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                    sample_path, "counting_method.txt"
                )
                self._current_sample_method = plankton_core.PlanktonCounterMethod(
                    header, rows
                )
            else:
                self._current_sample_method = plankton_core.PlanktonCounterMethod(
                    [], []
                )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_method_to_current_sample(self):
        """ """
        try:
            if self._current_sample_method is None:
                return
            #
            sample_path = self._current_sample_object.get_dir_path()
            self._current_sample_method.save_method_config_to_file(
                sample_path, "counting_method.txt"
            )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _create_content_methods(self):
        """ """
        # Stored default methods.
        self._selectdefaultmethod_list = QtWidgets.QComboBox(self)
        #         self._selectdefaultmethod_list.addItems(['<method for current sample>'])
        self._selectdefaultmethod_list.addItems(["<select>"])
        #         self._selectdefaultmethod_list.currentIndexChanged._select_default_method_changed)
        self._defaultmethod_copy_button = QtWidgets.QPushButton(
            "Copy values from selected setup"
        )
        self._defaultmethod_copy_button.clicked.connect(
            self._copy_default_method_values
        )
        self._defaultmethod_reset_button = QtWidgets.QPushButton(
            "Reset to used values for this sample"
        )
        self._defaultmethod_reset_button.clicked.connect(
            self._reset_default_method_values
        )
        # Stored methods.
        self._selectmethod_table = QtWidgets.QListWidget(
            self
        )  # app_framework.ToolboxQTableView(self)
        self._selectmethod_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self._selectmethod_table.setStyleSheet(
            "QListWidget::item:hover{background-color:#cccccc;}"
        )
        #         self._selectmethod_table.itemSelectionChanged._select_method_changed)
        self._selectmethod_table.itemClicked.connect(self._select_method_changed)
        # Stored method steps.
        self._selectmethodstep_table = QtWidgets.QListWidget(
            self
        )  # app_framework.ToolboxQTableView(self)
        self._selectmethodstep_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self._selectmethodstep_table.setStyleSheet(
            "QListWidget::item:hover{background-color:#cccccc;}"
        )
        self._selectmethodstep_table.itemSelectionChanged.connect(
            self._select_method_step_changed
        )
        #         self._selectmethodstep_table.itemClicked._select_method_step_changed)
        #         self._methodstepdescription_edit = QtWidgets.QLineEdit('')
        #         self._methodstepdescription_edit.textEdited._field_changed)

        # 'qualitative_quantitative'
        self._methodtype_list = QtWidgets.QComboBox()
        self._methodtype_list.addItems(
            ["Quantitative", "Qualitative", "Quantitative and qualitative"]
        )
        self._methodtype_list.setMaximumWidth(200)
        self._methodtype_list.currentIndexChanged.connect(self._field_changed)

        self._sampledvolume_edit = QtWidgets.QLineEdit("")
        self._sampledvolume_edit.setMaximumWidth(60)
        self._sampledvolume_edit.textEdited.connect(self._field_changed)
        self._countedvolume_edit = QtWidgets.QLineEdit("")
        self._countedvolume_edit.setMaximumWidth(60)
        self._countedvolume_edit.textEdited.connect(self._field_changed)
        self._chamber_filter_diameter_edit = QtWidgets.QLineEdit("")
        self._chamber_filter_diameter_edit.setMaximumWidth(60)
        self._chamber_filter_diameter_edit.textEdited.connect(self._field_changed)
        self._preservative_list = QtWidgets.QComboBox()
        self._preservative_list.setEditable(True)
        self._preservative_list.addItems(
            [
                "<select or edit>",
                "ALU (Alkaline Lugol´s solution)",
                "CLU (Acid Lugol´s solution)",
                "LUG (Neutral Lugol´s solution)",
                "NBF (Formalin - neutral buffered formalin 10%)",
                "GLU (Glutaraldehyde)",
            ]
        )
        self._preservative_list.setMaximumWidth(200)
        self._preservative_list.currentIndexChanged.connect(self._field_changed)
        #
        self._preservative_volume_edit = QtWidgets.QLineEdit("")
        self._preservative_volume_edit.setMaximumWidth(60)
        self._preservative_volume_edit.textEdited.connect(self._field_changed)
        #
        self._magnification_edit = QtWidgets.QLineEdit("")
        self._magnification_edit.setMaximumWidth(60)
        self._magnification_edit.textEdited.connect(self._field_changed)
        self._microscope_edit = QtWidgets.QLineEdit("")
        self._microscope_edit.textEdited.connect(self._field_changed)
        self._countareatype_list = QtWidgets.QComboBox()
        self._countareatype_list.addItems(
            [
                "<select>",
                "Chamber/filter",
                "1/2 Chamber/filter",
                "Field of views",
                "Transects",
                "Rectangles",
            ]
        )
        self._countareatype_list.currentIndexChanged.connect(self._field_changed)
        self._viewdiameter_edit = QtWidgets.QLineEdit("")
        self._viewdiameter_edit.setMaximumWidth(60)
        self._viewdiameter_edit.textEdited.connect(self._field_changed)
        self._transectrectanglewidth_edit = QtWidgets.QLineEdit("")
        self._transectrectanglewidth_edit.setMaximumWidth(60)
        self._transectrectanglewidth_edit.textEdited.connect(self._field_changed)
        self._transectrectanglelength_edit = QtWidgets.QLineEdit("")
        self._transectrectanglelength_edit.setMaximumWidth(60)
        self._transectrectanglelength_edit.textEdited.connect(self._field_changed)
        self._coefficient_one_unit_edit = QtWidgets.QLineEdit()
        self._coefficient_one_unit_edit.setMaximumWidth(100)
        self._coefficient_one_unit_edit.setEnabled(False)
        self._coefficient_one_unit_edit.textEdited.connect(self._field_changed)
        self._coefficient_by_user_checkbox = QtWidgets.QCheckBox("Calc. by user")
        self._coefficient_by_user_checkbox.stateChanged.connect(self._field_changed)
        self._counting_species_list = QtWidgets.QComboBox()
        self._counting_species_list.addItems(["<valid taxa>"])
        #         self._counting_species_list.addItems(['<all species>'])
        self._counting_species_list.currentIndexChanged.connect(self._field_changed)
        self._viewsizeclassinfo_checkbox = QtWidgets.QCheckBox("View sizeclass info")
        self._viewsizeclassinfo_checkbox.setChecked(True)
        self._viewsizeclassinfo_checkbox.stateChanged.connect(self._field_changed)

        # Buttons.
        #         self._addmethod_button = QtWidgets.QPushButton('Add method...')
        #         self._addmethod_button.clicked.connect(self._add_method)

        self._addmethodstep_button = QtWidgets.QPushButton("Add method/method step...")
        self._addmethodstep_button.clicked.connect(self._add_method_step)
        self._deletemethodsteps_method_button = QtWidgets.QPushButton(
            "Delete method step(s)..."
        )
        self._deletemethodsteps_method_button.clicked.connect(self._delete_method_steps)

        #         self._savedefault_method_button = QtWidgets.QPushButton('Save changes to selected default method setup')
        #         self._savedefault_method_button.clicked.connect(self._save_default_method)
        self._saveasdefault_method_button = QtWidgets.QPushButton(
            "Save as default method setup..."
        )
        self._saveasdefault_method_button.clicked.connect(self._save_as_default_method)
        self._deletedefault_method_button = QtWidgets.QPushButton(
            "Delete default method setup(s)..."
        )
        self._deletedefault_method_button.clicked.connect(self._default_method_delete)

        # Layout widgets.

        # ===== GRID 1. =====
        grid1 = QtWidgets.QGridLayout()
        gridrow = 0
        grid1.addWidget(
            app_framework.LeftAlignedQLabel("<b>Counting methods</b>"),
            gridrow,
            0,
            1,
            10,
        )
        gridrow += 1
        grid1.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.
        gridrow += 1
        grid1.addWidget(
            app_framework.RightAlignedQLabel("Default method setup:"), gridrow, 0, 1, 1
        )
        grid1.addWidget(self._selectdefaultmethod_list, gridrow, 1, 1, 2)
        gridrow += 1
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._defaultmethod_copy_button)
        hbox.addWidget(self._defaultmethod_reset_button)
        hbox.addStretch(10)
        grid1.addLayout(hbox, gridrow, 1, 1, 2)
        gridrow += 1
        grid1.setRowStretch(gridrow, 10)
        gridrow += 1
        grid1.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.

        # ===== GRID 2. =====
        grid2 = QtWidgets.QGridLayout()
        gridrow = 0
        grid2.addWidget(
            app_framework.LeftAlignedQLabel("<b>Methods:</b>"), gridrow, 0, 1, 1
        )
        gridrow += 1
        grid2.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.
        gridrow += 1
        grid2.addWidget(self._selectmethod_table, gridrow, 0, 10, 1)

        # ===== GRID 3. =====
        grid3 = QtWidgets.QGridLayout()
        gridrow = 0
        grid3.addWidget(
            app_framework.LeftAlignedQLabel("<b>Method values:</b>"), gridrow, 0, 1, 2
        )
        gridrow += 1
        grid3.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.
        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Sampled volume (mL):"), gridrow, 0, 1, 1
        )
        grid3.addWidget(self._sampledvolume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Preservative:"), gridrow, 0, 1, 1
        )
        grid3.addWidget(self._preservative_list, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Preservative volume (mL):"),
            gridrow,
            0,
            1,
            1,
        )
        grid3.addWidget(self._preservative_volume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Counted volume (mL):"), gridrow, 0, 1, 1
        )
        grid3.addWidget(self._countedvolume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Chamber/filter diameter (mm):"),
            gridrow,
            0,
            1,
            1,
        )
        grid3.addWidget(self._chamber_filter_diameter_edit, gridrow, 1, 1, 1)

        gridrow += 1
        grid3.addWidget(
            app_framework.RightAlignedQLabel("Method type:"), gridrow, 0, 1, 1
        )
        grid3.addWidget(self._methodtype_list, gridrow, 1, 1, 1)

        gridrow += 1
        grid3.setRowStretch(gridrow, 10)

        # ===== GRID 4. =====
        grid4 = QtWidgets.QGridLayout()
        gridrow = 0
        grid4.addWidget(
            app_framework.LeftAlignedQLabel("<b>Method steps:</b>"), gridrow, 0, 1, 1
        )
        gridrow += 1
        grid4.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.
        gridrow += 1
        grid4.addWidget(self._selectmethodstep_table, gridrow, 0, 10, 1)

        # ===== GRID 5. =====
        grid5 = QtWidgets.QGridLayout()
        gridrow = 0
        grid5.addWidget(
            app_framework.LeftAlignedQLabel("<b>Method step values:</b>"),
            gridrow,
            0,
            1,
            2,
        )
        gridrow += 1
        grid5.addWidget(QtWidgets.QLabel(""), gridrow, 1, 1, 1)  # Add space.
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Magnification:"), gridrow, 0, 1, 1
        )
        grid5.addWidget(self._magnification_edit, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Microscope:"), gridrow, 0, 1, 1
        )
        grid5.addWidget(self._microscope_edit, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Count area type:"), gridrow, 0, 1, 1
        )
        grid5.addWidget(self._countareatype_list, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Diameter of view (mm):"), gridrow, 0, 1, 1
        )
        grid5.addWidget(self._viewdiameter_edit, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Transect/rectangle width (mm):"),
            gridrow,
            0,
            1,
            1,
        )
        grid5.addWidget(self._transectrectanglewidth_edit, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Transect/rectangle length (mm):"),
            gridrow,
            0,
            1,
            1,
        )
        grid5.addWidget(self._transectrectanglelength_edit, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Coefficient for one area:"),
            gridrow,
            0,
            1,
            1,
        )
        #         grid5.addWidget(app_framework.LeftAlignedQLabel('Coefficient for one area:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._coefficient_one_unit_edit, gridrow, 1, 1, 1)
        grid5.addWidget(self._coefficient_by_user_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        grid5.addWidget(
            app_framework.RightAlignedQLabel("Default counting species list:"),
            gridrow,
            0,
            1,
            1,
        )
        grid5.addWidget(self._counting_species_list, gridrow, 1, 1, 2)
        gridrow += 1
        grid5.addWidget(self._viewsizeclassinfo_checkbox, gridrow, 1, 1, 2)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addLayout(grid2, 10)
        hbox1.addLayout(grid3, 5)
        hbox1.addStretch(5)
        hbox1.addLayout(grid4, 10)
        hbox1.addLayout(grid5, 10)
        hbox1.addStretch(20)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        #         hbox2.addWidget(self._addmethod_button)
        hbox2.addWidget(self._addmethodstep_button)
        hbox2.addWidget(self._deletemethodsteps_method_button)
        hbox2.addStretch(1)
        #         hbox2.addWidget(self._savedefault_method_button)
        hbox2.addWidget(self._saveasdefault_method_button)
        hbox2.addWidget(self._deletedefault_method_button)
        hbox2.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        layout.addWidget(
            app_framework.LeftAlignedQLabel("<b>Manage counting methods:</b>")
        )
        layout.addLayout(hbox2)
        #
        return layout

    def set_read_only(self, read_only=True):
        """ """
        if (not self.sample_locked) and read_only:
            # Save sample before locking.
            self.save_data()
        #
        self.sample_locked = read_only
        #
        enabled = not read_only
        self._selectdefaultmethod_list
        self._defaultmethod_copy_button.setEnabled(enabled)
        self._defaultmethod_reset_button.setEnabled(enabled)
        #         self._selectmethod_table.setEnabled(enabled)
        #         self._selectmethodstep_table.setEnabled(enabled)
        self._methodtype_list.setEnabled(enabled)
        self._sampledvolume_edit.setReadOnly(read_only)
        self._countedvolume_edit.setReadOnly(read_only)
        self._chamber_filter_diameter_edit.setReadOnly(read_only)
        self._preservative_list.setEnabled(enabled)
        self._preservative_volume_edit.setReadOnly(read_only)
        self._magnification_edit.setReadOnly(read_only)
        self._microscope_edit.setReadOnly(read_only)
        self._countareatype_list.setEnabled(enabled)
        self._viewdiameter_edit.setReadOnly(read_only)
        self._transectrectanglewidth_edit.setReadOnly(read_only)
        self._transectrectanglelength_edit.setReadOnly(read_only)
        self._coefficient_one_unit_edit.setReadOnly(read_only)
        self._coefficient_by_user_checkbox.setEnabled(enabled)
        self._counting_species_list.setEnabled(enabled)
        self._viewsizeclassinfo_checkbox.setEnabled(enabled)
        self._addmethodstep_button.setEnabled(enabled)
        self._deletemethodsteps_method_button.setEnabled(enabled)
        self._saveasdefault_method_button.setEnabled(enabled)
        self._deletedefault_method_button.setEnabled(enabled)
        self._coefficient_by_user_checkbox.setEnabled(enabled)
        #
        self._set_fields_valid_for_data()

    def _update_default_method_list(self):
        """ """
        try:
            self._selectdefaultmethod_list.clear()
            #
            defaultmethods = (
                plankton_core.PlanktonCounterMethods().get_default_method_list()
            )
            if len(defaultmethods) > 0:
                self._selectdefaultmethod_list.addItems(["<select>"] + defaultmethods)
            #             self._selectdefaultmethod_list.addItems(defaultmethods)
            else:
                self._selectdefaultmethod_list.addItems(["<not available>"])
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _update_counting_species_list(self):
        """ """
        try:
            self._counting_species_list.clear()
            specieslists = (
                plankton_core.PlanktonCounterMethods().get_counting_species_lists()
            )
            if len(specieslists) > 0:
                self._counting_species_list.addItems(["<valid taxa>"] + specieslists)
            #             self._counting_species_list.addItems(['<all species>'] + specieslists)
            else:
                self._counting_species_list.addItems(["<not available>"])
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _copy_default_method_values(self):
        """ """
        try:
            self._selectmethod_table.clear()
            self._selectmethodstep_table.clear()
            self._update_method_step_fields({})  # Clear.
            #
            if self._selectdefaultmethod_list.currentIndex() == 0:
                self._load_current_sample_method()
            else:
                selecteddefaultmethod = str(
                    self._selectdefaultmethod_list.currentText()
                )
                try:
                    path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                    (
                        header,
                        rows,
                    ) = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                        path, selecteddefaultmethod + ".txt"
                    )
                    self._current_sample_method = plankton_core.PlanktonCounterMethod(
                        header, rows
                    )
                except:
                    self._current_sample_method = plankton_core.PlanktonCounterMethod(
                        [], []
                    )
            #
            self._update_method_table()
            self._update_method_step_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    #####
    def _update_method_table(self):
        """ """
        try:
            self._selectmethod_table.clear()
            #
            countingmethods = self._current_sample_method.get_counting_methods_list()
            if len(countingmethods) > 0:
                self._selectmethod_table.addItems(countingmethods)
                self._selectmethod_table.setCurrentRow(0)
            else:
                self._selectmethod_table.addItems(["<not available>"])
                self._selectmethod_table.setCurrentRow(0)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _update_method_step_table(self):
        """ """
        try:
            self._selectmethodstep_table.clear()
            #
            currentmethod = str(self._selectmethod_table.currentItem().text())
            countingmethods = (
                self._current_sample_method.get_counting_method_steps_list(
                    currentmethod
                )
            )
            if len(countingmethods) > 0:
                self._selectmethodstep_table.addItems(countingmethods)
                self._selectmethodstep_table.setCurrentRow(0)
            else:
                self._selectmethodstep_table.addItems(["<not available>"])
                self._selectmethodstep_table.setCurrentRow(0)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _reset_default_method_values(self):
        """ """
        try:
            self._selectmethod_table.clear()
            self._selectmethodstep_table.clear()
            #
            self._load_current_sample_method()
            #
            countingmethods = self._current_sample_method.get_counting_method_list()
            if len(countingmethods) > 0:
                self._selectmethod_table.addItems(countingmethods)
                self._selectmethod_table.setCurrentRow(0)
            else:
                self._selectmethod_table.addItems(["<not available>"])
                self._selectmethod_table.setCurrentRow(0)
            #
            currentmethod = str(self._selectmethod_table.currentItem().text())
            countingmethods = (
                self._current_sample_method.get_counting_method_steps_list(
                    currentmethod
                )
            )
            if len(countingmethods) > 0:
                self._selectmethodstep_table.addItems(countingmethods)
                self._selectmethodstep_table.setCurrentRow(0)
            else:
                self._selectmethodstep_table.addItems(["<not available>"])
                self._selectmethodstep_table.setCurrentRow(0)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    #####
    def _update_method_fields(self, fields_dict):
        """ """
        try:
            try:
                self._dont_update_current_sample_method_flag = True
                #
                #             self._methodstepdescription_edit.setText(fields_dict.get('method_description', ''))

                #
                methodtype = fields_dict.get("qualitative_quantitative", "")
                currentindex = self._methodtype_list.findText(
                    methodtype, QtCore.Qt.MatchFlag.MatchFixedString
                )
                if currentindex >= 0:
                    self._methodtype_list.setCurrentIndex(currentindex)
                else:
                    self._methodtype_list.setCurrentIndex(0)

                self._sampledvolume_edit.setText(
                    fields_dict.get("sampled_volume_ml", "")
                )
                #
                preservative = fields_dict.get("preservative", "")
                currentindex = self._preservative_list.findText(
                    preservative, QtCore.Qt.MatchFlag.MatchFixedString
                )
                if currentindex >= 0:
                    self._preservative_list.setCurrentIndex(currentindex)
                else:
                    self._preservative_list.setCurrentIndex(0)
                #
                self._preservative_volume_edit.setText(
                    fields_dict.get("preservative_volume_ml", "")
                )
                self._countedvolume_edit.setText(
                    fields_dict.get("counted_volume_ml", "")
                )
                self._chamber_filter_diameter_edit.setText(
                    fields_dict.get("chamber_filter_diameter_mm", "")
                )
                #
                self._magnification_edit.setText(fields_dict.get("magnification", ""))
                self._microscope_edit.setText(fields_dict.get("microscope", ""))
                #
                comboindex = self._countareatype_list.findText(
                    fields_dict.get("count_area_type", "<select>")
                )
                self._countareatype_list.setCurrentIndex(comboindex)
                #
                self._viewdiameter_edit.setText(
                    fields_dict.get("diameter_of_view_mm", "")
                )
                self._transectrectanglelength_edit.setText(
                    fields_dict.get("transect_rectangle_length_mm", "")
                )
                self._transectrectanglewidth_edit.setText(
                    fields_dict.get("transect_rectangle_width_mm", "")
                )
                self._coefficient_one_unit_edit.setText(
                    fields_dict.get("coefficient_one_unit", "")
                )
                #
                combostate = fields_dict.get("coefficient_by_user", "FALSE")
                if combostate.upper() == "TRUE":
                    self._coefficient_by_user_checkbox.setChecked(True)
                else:
                    self._coefficient_by_user_checkbox.setChecked(False)
                #
                comboindex = self._counting_species_list.findText(
                    fields_dict.get("counting_species_list", "<valid taxa>")
                )
                #             comboindex = self._counting_species_list.findText(fields_dict.get('counting_species_list', '<all species>'))
                self._counting_species_list.setCurrentIndex(comboindex)
                #
                combostate = fields_dict.get("view_sizeclass_info", "FALSE")
                if combostate.upper() == "TRUE":
                    self._viewsizeclassinfo_checkbox.setChecked(True)
                else:
                    self._viewsizeclassinfo_checkbox.setChecked(False)
                #
            finally:
                self._dont_update_current_sample_method_flag = False
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    #####
    def _select_method_changed(self):
        """ """
        try:
            if self._current_sample_method is None:
                return
            #
            self._update_method_fields({})  # Clear.
            #
            selectedmethod = str(self._selectmethod_table.currentItem().text())
            #
            fields_dict = self._current_sample_method.get_counting_method_fields(
                selectedmethod
            )
            self._update_method_fields(fields_dict)
            #
            self._update_method_step_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _select_method_step_changed(self):
        """ """
        try:
            if self._current_sample_method is None:
                return
            #
            self._update_method_step_fields({})  # Clear.
            #
            selectedmethodstep = str(self._selectmethodstep_table.currentItem().text())
            #
            fields_dict = self._current_sample_method.get_counting_method_step_fields(
                selectedmethodstep
            )
            self._update_method_step_fields(fields_dict)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _update_method_step_fields(self, fields_dict):
        """ """
        try:
            try:
                self._dont_update_current_sample_method_flag = True
                #
                #             self._methodstepdescription_edit.setText(fields_dict.get('method_step_description', ''))

                #
                methodtype = fields_dict.get("qualitative_quantitative", "")
                currentindex = self._methodtype_list.findText(
                    methodtype, QtCore.Qt.MatchFlag.MatchFixedString
                )
                if currentindex >= 0:
                    self._methodtype_list.setCurrentIndex(currentindex)
                else:
                    self._methodtype_list.setCurrentIndex(0)

                self._sampledvolume_edit.setText(
                    fields_dict.get("sampled_volume_ml", "")
                )
                #
                preservative = fields_dict.get("preservative", "")
                currentindex = self._preservative_list.findText(
                    preservative, QtCore.Qt.MatchFlag.MatchFixedString
                )
                if currentindex >= 0:
                    self._preservative_list.setCurrentIndex(currentindex)
                else:
                    self._preservative_list.setItemText(0, preservative)
                #
                self._preservative_volume_edit.setText(
                    fields_dict.get("preservative_volume_ml", "")
                )
                self._countedvolume_edit.setText(
                    fields_dict.get("counted_volume_ml", "")
                )
                self._chamber_filter_diameter_edit.setText(
                    fields_dict.get("chamber_filter_diameter_mm", "")
                )
                #
                self._magnification_edit.setText(fields_dict.get("magnification", ""))
                self._microscope_edit.setText(fields_dict.get("microscope", ""))
                #
                comboindex = self._countareatype_list.findText(
                    fields_dict.get("count_area_type", "<select>")
                )
                self._countareatype_list.setCurrentIndex(comboindex)
                #
                self._viewdiameter_edit.setText(
                    fields_dict.get("diameter_of_view_mm", "")
                )
                self._transectrectanglelength_edit.setText(
                    fields_dict.get("transect_rectangle_length_mm", "")
                )
                self._transectrectanglewidth_edit.setText(
                    fields_dict.get("transect_rectangle_width_mm", "")
                )
                self._coefficient_one_unit_edit.setText(
                    fields_dict.get("coefficient_one_unit", "")
                )
                #
                combostate = fields_dict.get("coefficient_by_user", "FALSE")
                if combostate.upper() == "TRUE":
                    self._coefficient_by_user_checkbox.setChecked(True)
                else:
                    self._coefficient_by_user_checkbox.setChecked(False)
                #
                comboindex = self._counting_species_list.findText(
                    fields_dict.get("counting_species_list", "<valid taxa>")
                )
                #             comboindex = self._counting_species_list.findText(fields_dict.get('counting_species_list', '<all species>'))
                self._counting_species_list.setCurrentIndex(comboindex)
                #
                combostate = fields_dict.get("view_sizeclass_info", "FALSE")
                if combostate.upper() == "TRUE":
                    self._viewsizeclassinfo_checkbox.setChecked(True)
                else:
                    self._viewsizeclassinfo_checkbox.setChecked(False)
                #
            finally:
                self._dont_update_current_sample_method_flag = False
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _field_changed(self):
        """ """
        try:

            self._set_fields_valid_for_data()

            self._update_current_sample_method()
        #         # If any field changed, then go back to sample method.
        #         self._selectdefaultmethod_list.setCurrentIndex(0)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _set_fields_valid_for_data(self):
        """Get info for both method and method step."""
        countareatype = self._countareatype_list.currentText()

        if not self._coefficient_by_user_checkbox.isChecked():
            if countareatype == "Chamber/filter":
                self._viewdiameter_edit.setEnabled(False)
                self._transectrectanglewidth_edit.setEnabled(False)
                self._transectrectanglelength_edit.setEnabled(False)
                self._coefficient_one_unit_edit.setEnabled(False)
            elif countareatype == "1/2 Chamber/filter":
                self._viewdiameter_edit.setEnabled(False)
                self._transectrectanglewidth_edit.setEnabled(False)
                self._transectrectanglelength_edit.setEnabled(False)
                self._coefficient_one_unit_edit.setEnabled(False)
            elif countareatype == "Field of views":
                self._viewdiameter_edit.setEnabled(True)
                self._transectrectanglewidth_edit.setEnabled(False)
                self._transectrectanglelength_edit.setEnabled(False)
                self._coefficient_one_unit_edit.setEnabled(False)
            elif countareatype == "Transects":
                self._viewdiameter_edit.setEnabled(False)
                self._transectrectanglewidth_edit.setEnabled(True)
                self._transectrectanglelength_edit.setEnabled(True)
                self._coefficient_one_unit_edit.setEnabled(False)
            elif countareatype == "Rectangles":
                self._viewdiameter_edit.setEnabled(False)
                self._transectrectanglewidth_edit.setEnabled(True)
                self._transectrectanglelength_edit.setEnabled(True)
                self._coefficient_one_unit_edit.setEnabled(False)
        else:
            self._viewdiameter_edit.setEnabled(False)
            self._transectrectanglewidth_edit.setEnabled(False)
            self._transectrectanglelength_edit.setEnabled(False)
            self._coefficient_one_unit_edit.setEnabled(True)

    def _update_current_sample_method(self):
        """Get info for both method and method step."""
        if self.sample_locked:
            return
        try:
            if self._dont_update_current_sample_method_flag:
                return
            # Method.
            if not self._current_sample_method:
                return
            #
            fields_dict = {}
            fields_dict["counting_method"] = str(
                self._selectmethod_table.currentItem().text()
            )
            fields_dict["counting_method_step"] = str(
                self._selectmethodstep_table.currentItem().text()
            )
            #         fields_dict['method_step_description'] = str(self._methodstepdescription_edit.text())

            fields_dict["qualitative_quantitative"] = str(
                self._methodtype_list.currentText()
            )

            fields_dict["sampled_volume_ml"] = (
                str(self._sampledvolume_edit.text()).replace(",", ".").replace(" ", "")
            )
            fields_dict["preservative"] = str(self._preservative_list.currentText())
            fields_dict["preservative_volume_ml"] = (
                str(self._preservative_volume_edit.text())
                .replace(",", ".")
                .replace(" ", "")
            )
            fields_dict["counted_volume_ml"] = (
                str(self._countedvolume_edit.text()).replace(",", ".").replace(" ", "")
            )
            fields_dict["chamber_filter_diameter_mm"] = (
                str(self._chamber_filter_diameter_edit.text())
                .replace(",", ".")
                .replace(" ", "")
            )
            #
            fields_dict["magnification"] = (
                str(self._magnification_edit.text()).replace(",", ".").replace(" ", "")
            )
            fields_dict["microscope"] = str(self._microscope_edit.text())

            fields_dict["count_area_type"] = str(self._countareatype_list.currentText())

            fields_dict["diameter_of_view_mm"] = (
                str(self._viewdiameter_edit.text()).replace(",", ".").replace(" ", "")
            )
            fields_dict["transect_rectangle_length_mm"] = (
                str(self._transectrectanglelength_edit.text())
                .replace(",", ".")
                .replace(" ", "")
            )
            fields_dict["transect_rectangle_width_mm"] = (
                str(self._transectrectanglewidth_edit.text())
                .replace(",", ".")
                .replace(" ", "")
            )
            fields_dict["coefficient_one_unit"] = (
                str(self._coefficient_one_unit_edit.text())
                .replace(",", ".")
                .replace(" ", "")
            )
            if self._coefficient_by_user_checkbox.isChecked():
                fields_dict["coefficient_by_user"] = "TRUE"
            else:
                fields_dict["coefficient_by_user"] = "FALSE"

            fields_dict["counting_species_list"] = str(
                self._counting_species_list.currentText()
            )
            if self._viewsizeclassinfo_checkbox.isChecked():
                fields_dict["view_sizeclass_info"] = "TRUE"
            else:
                fields_dict["view_sizeclass_info"] = "FALSE"
            #
            counting_method = fields_dict["counting_method"]
            counting_method_step = fields_dict["counting_method_step"]
            self._current_sample_method.update_counting_method_step_fields(
                counting_method, counting_method_step, fields_dict
            )
            # Update coefficient field.
            self._current_sample_method.calculate_coefficient_one_unit(fields_dict)
            self._coefficient_one_unit_edit.setText(
                fields_dict.get("coefficient_one_unit", "0")
            )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _add_method_step(self):
        """ """
        try:
            old_method = ""
            if self._selectdefaultmethod_list.currentIndex() > 0:
                old_method = str(self._selectdefaultmethod_list.currentText())
            current_method = str(self._selectmethod_table.currentItem().text())
            current_method_step = str(self._selectmethodstep_table.currentItem().text())
            #
            try:
                dialog = AddMethodStepDialog(
                    self,
                    self._current_sample_method,
                    current_method,
                    current_method_step,
                )
                if dialog.exec():
                    if old_method:
                        path = (
                            plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                        )
                        self._current_sample_method.save_method_config_to_file(
                            path, old_method + ".txt"
                        )
                    #
                    self._update_default_method_list()
                    #
                    currentindex = self._selectdefaultmethod_list.findText(
                        old_method, QtCore.Qt.MatchFlag.MatchFixedString
                    )
                    if currentindex >= 0:
                        self._selectdefaultmethod_list.setCurrentIndex(currentindex)
                    #
                    self._update_method_table()
                    self._update_method_step_table()
            except Exception as e:
                debug_info = (
                    self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
                )
                toolbox_utils.Logging().error(
                    "Exception: (" + debug_info + "): " + str(e)
                )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _delete_method_steps(self):
        """ """
        try:
            old_method = ""
            if self._selectdefaultmethod_list.currentIndex() > 0:
                old_method = str(self._selectdefaultmethod_list.currentText())
            #
            dialog = DeleteMethodStepsDialog(self, self._current_sample_method)
            if dialog.exec():
                if old_method:
                    path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                    self._current_sample_method.save_method_config_to_file(
                        path, old_method + ".txt"
                    )
                #
                self._update_default_method_list()
                #
                currentindex = self._selectdefaultmethod_list.findText(
                    old_method, QtCore.Qt.MatchFlag.MatchFixedString
                )
                if currentindex >= 0:
                    self._selectdefaultmethod_list.setCurrentIndex(currentindex)
                #
                self._update_method_table()
                self._update_method_step_table()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save_as_default_method(self):
        """ """
        try:
            if self._current_sample_method is None:
                return
            #
            self._update_current_sample_method()
            #
            old_name = ""
            if self._selectdefaultmethod_list.currentIndex() > 0:
                old_name = str(self._selectdefaultmethod_list.currentText())
            #
            dialog = SaveDefaultMethodAsDialog(self, old_name)
            if dialog.exec():
                new_name = dialog.get_new_name()
                if new_name:
                    path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                    self._current_sample_method.save_method_config_to_file(
                        path, new_name + ".txt"
                    )
                    #
                    self._update_default_method_list()
                    #
                    currentindex = self._selectdefaultmethod_list.findText(
                        new_name, QtCore.Qt.MatchFlag.MatchFixedString
                    )
                    if currentindex >= 0:
                        self._selectdefaultmethod_list.setCurrentIndex(currentindex)
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _default_method_delete(self):
        """ """
        try:
            dialog = DeleteDefaultMethodDialog(self)
            if dialog.exec():
                self._update_default_method_list()
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))


#####
# class AddMethodDialog(QtWidgets.QDialog):
#     """ """
#     def __init__(self, parentwidget, current_sample_method, current_method):
#         """ """
#         self._parentwidget = parentwidget
#         self._current_sample_method = current_sample_method
#         self._current_method = current_method
#         super(AddMethodDialog, self).__init__(parentwidget)
#         self.setWindowTitle('Add method')
#         self.setLayout(self._content())
#
#     def get_new_method(self):
#         """ """
#         return self._new_method
#
#     def _content(self):
#         """ """
#         self._new_method_edit = QtWidgets.QLineEdit(self._current_method)
#         self._new_method_edit.setMinimumWidth(400)
# #         self._copycontent_checkbox = QtWidgets.QCheckBox('Copy content')
# #         self._copycontent_checkbox.setChecked(True)
#
#         save_button = QtWidgets.QPushButton('Save')
#         save_button.clicked.connect(self._save)
#         cancel_button = QtWidgets.QPushButton('Cancel')
#         cancel_button.clicked.reject) # Close dialog box.
#         # Layout widgets.
#         formlayout = QtWidgets.QFormLayout()
#         formlayout.addRow('New method:', self._new_method_edit)
# #         formlayout.addRow('', self._copycontent_checkbox)
#
#         hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(10)
#         hbox1.addWidget(save_button)
#         hbox1.addWidget(cancel_button)
#         #
#         layout = QtWidgets.QVBoxLayout()
#         layout.addLayout(formlayout, 10)
#         layout.addLayout(hbox1)
#         #
#         return layout
#
#     def _save(self):
#         """ """
#         new_method_dict = {}
# #         if self._copycontent_checkbox.isChecked():
# #             new_method_dict.update(self._current_sample_method.get_counting_method_fields(self._current_method))
#         #
#         new_method_dict['counting_method'] = str(self._new_method_edit.text())
#         self._current_sample_method.add_method(new_method_dict)
#         #
#         self.accept() # Close dialog box.


class AddMethodStepDialog(QtWidgets.QDialog):
    """ """

    def __init__(
        self, parentwidget, current_sample_method, current_method, current_method_step
    ):
        """ """
        self._parentwidget = parentwidget
        self._current_sample_method = current_sample_method
        self._current_method = current_method
        self._current_method_step = current_method_step
        super(AddMethodStepDialog, self).__init__(parentwidget)
        self.setWindowTitle("Add method or method step")
        self.setLayout(self._content())

    def get_new_method_step(self):
        """ """
        return self._new_method_step

    def _content(self):
        """ """
        self._new_method_edit = QtWidgets.QLineEdit(self._current_method)
        self._new_method_edit.setMinimumWidth(400)
        self._new_method_step_edit = QtWidgets.QLineEdit(self._current_method_step)
        self._new_method_step_edit.setMinimumWidth(400)
        self._copycontent_checkbox = QtWidgets.QCheckBox("Copy content")
        self._copycontent_checkbox.setChecked(True)

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(self._save)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close dialog box.
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
        formlayout.addRow("New method:", self._new_method_edit)
        formlayout.addRow("New method step:", self._new_method_step_edit)
        formlayout.addRow("", self._copycontent_checkbox)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(save_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout

    def _save(self):
        """ """
        try:
            new_method_step_dict = {}
            if self._copycontent_checkbox.isChecked():
                new_method_step_dict.update(
                    self._current_sample_method.get_counting_method_step_fields(
                        self._current_method_step
                    )
                )
            #
            new_method_step_dict["counting_method"] = str(self._new_method_edit.text())
            new_method_step_dict["counting_method_step"] = str(
                self._new_method_step_edit.text()
            )
            self._current_sample_method.add_method_step(new_method_step_dict)
            #
            self.accept()  # Close dialog box.
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))


class DeleteMethodStepsDialog(QtWidgets.QDialog):
    """ """

    def __init__(self, parentwidget, current_sample_method):
        """ """
        self._parentwidget = parentwidget
        self._current_sample_method = current_sample_method
        super(DeleteMethodStepsDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete marked method(s)")
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()

    def _content(self):
        """ """
        methodsteps_listview = QtWidgets.QListView()
        self._methodsteps_model = QtGui.QStandardItemModel()
        methodsteps_listview.setModel(self._methodsteps_model)

        clearall_button = app_framework.ClickableQLabel("Clear all")
        clearall_button.label_clicked.connect(self._uncheck_all_rows)
        markall_button = app_framework.ClickableQLabel("Mark all")
        markall_button.label_clicked.connect(self._check_all_rows)
        delete_button = QtWidgets.QPushButton("Delete marked method step(s)")
        delete_button.clicked.connect(self._delete_marked_rows)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close dialog box.
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(methodsteps_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

        return layout

    def _load_data(self):
        """ """
        try:
            methodstepslists = (
                self._current_sample_method.get_counting_method_steps_list()
            )

            self._methodsteps_model.clear()
            for methodstep in methodstepslists:
                item = QtGui.QStandardItem(methodstep)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                item.setCheckable(True)
                self._methodsteps_model.appendRow(item)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _check_all_rows(self):
        """ """
        try:
            for rowindex in range(self._methodsteps_model.rowCount()):
                item = self._methodsteps_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.CheckState.Checked)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _uncheck_all_rows(self):
        """ """
        try:
            for rowindex in range(self._methodsteps_model.rowCount()):
                item = self._methodsteps_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _delete_marked_rows(self):
        """ """
        try:
            for rowindex in range(self._methodsteps_model.rowCount()):
                item = self._methodsteps_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    selectedname = str(item.text())
                    self._current_sample_method.delete_method_step(selectedname)
            #
            self.accept()  # Close dialog box.
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))


class SaveDefaultMethodAsDialog(QtWidgets.QDialog):
    """ """

    def __init__(self, parentwidget, old_name):
        """ """
        self._old_name = old_name
        self._new_name = ""
        super(SaveDefaultMethodAsDialog, self).__init__(parentwidget)
        self.setWindowTitle("Save as default method setup")
        self.setLayout(self._content())
        self._load_data()

    def get_new_name(self):
        """ """
        return self._new_name

    def _content(self):
        """ """
        self._default_methods_setups = QtWidgets.QComboBox(self)
        self._default_methods_setups.setMinimumWidth(300)
        updatemethodsetup_button = QtWidgets.QPushButton(
            "Update selected default method setup"
        )
        updatemethodsetup_button.clicked.connect(self._update)
        #
        self._new_default_method_edit = QtWidgets.QLineEdit("")
        self._new_default_method_edit.setMinimumWidth(300)
        createmethodsetup_button = QtWidgets.QPushButton(
            "Create new default method setup"
        )
        createmethodsetup_button.clicked.connect(self._save)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close dialog box.
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
        #         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow("Select default method setup:", self._default_methods_setups)
        formlayout.addRow("", updatemethodsetup_button)
        formlayout.addRow("", QtWidgets.QLabel(""))
        formlayout.addRow(
            "New default method setup name:", self._new_default_method_edit
        )
        formlayout.addRow("", createmethodsetup_button)
        formlayout.addRow("", QtWidgets.QLabel(""))
        #
        hbox1 = QtWidgets.QHBoxLayout()
        #         hbox1.addStretch(10)
        hbox1.addWidget(QtWidgets.QLabel("Select default method setup:"))
        hbox1.addWidget(self._default_methods_setups)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(updatemethodsetup_button)
        #
        hbox3 = QtWidgets.QHBoxLayout()
        #         hbox3.addStretch(10)
        hbox3.addWidget(QtWidgets.QLabel("New default method setup name:"))
        hbox3.addWidget(self._new_default_method_edit)
        #
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addStretch(10)
        hbox4.addWidget(createmethodsetup_button)
        #
        hbox5 = QtWidgets.QHBoxLayout()
        hbox5.addStretch(10)
        hbox5.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)
        layout.addLayout(hbox5)
        #
        return layout

    def _load_data(self):
        """ """
        try:
            defaultmethods = (
                plankton_core.PlanktonCounterMethods().get_default_method_list()
            )
            defaultmethods = ["<select>"] + sorted(defaultmethods)
            self._default_methods_setups.addItems(defaultmethods)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _update(self):
        """ """
        try:
            self._new_name = str(self._default_methods_setups.currentText())
            #
            if self._new_name != "<select>":
                self.accept()  # Close dialog box and process the update after.
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Default method setup.\n",
                    'No "default method setup" is selected. Please try again.',
                )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _save(self):
        """ """
        try:
            self._new_name = str(self._new_default_method_edit.text())
            #
            if self._new_name:
                self.accept()  # Close dialog box and process the update after.
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Default method setup.\n",
                    'New name for the "default method setup" is missing. Please try again.',
                )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))


# class NewSampleDialog(QtWidgets.QDialog):
#     """ This dialog is allowed to access private parts in the parent widget. """
#     def __init__(self, parentwidget, dataset):
#         """ """
#         self._current_dataset = dataset
#         super(NewSampleDialog, self).__init__(parentwidget)
#         self._parentwidget = parentwidget
#         self.setWindowTitle("New sample")
#         self.setLayout(self._content())
#         self._load_dataset_data()
#
#     def _content(self):
#         """ """
#         self._dataset_list = QtWidgets.QComboBox(self)
#         self._samplename_edit = QtWidgets.QLineEdit('')
#         self._samplename_edit.setMinimumWidth(400)
#         createsample_button = QtWidgets.QPushButton('Create sample')
#         createsample_button.clicked.connect(self._create_sample)
#         cancel_button = QtWidgets.QPushButton('Cancel')
#         cancel_button.clicked.reject) # Close dialog box.
#         # Layout widgets.
#         formlayout = QtWidgets.QFormLayout()
# #         formlayout.addRow('Sample id:', self._sampleid_edit)
#         formlayout.addRow('Dataset:', self._dataset_list)
#         formlayout.addRow('Sample name:', self._samplename_edit)
#         formlayout.addRow('', QtWidgets.QLabel('Example: Släggö_2016-06-01_0-10m_Net'))
#         #
#         hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(10)
#         hbox1.addWidget(createsample_button)
#         hbox1.addWidget(cancel_button)
#         #
#         layout = QtWidgets.QVBoxLayout()
#         layout.addLayout(formlayout, 10)
#         layout.addLayout(hbox1)
#         #
#         return layout
#
#     def _load_dataset_data(self):
#         """ """
#         for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
#             self._dataset_list.addItem(datasetname)
#         #
#         if self._current_dataset:
#             currentindex = self._dataset_list.findText(self._current_dataset, QtCore.Qt.MatchFlag.MatchFixedString)
#             if currentindex >= 0:
#                 self._dataset_list.setCurrentIndex(currentindex)
#
#     def _create_sample(self):
#         """ """
#         datasetname = str(self._dataset_list.currentText())
#         samplename = str(self._samplename_edit.text())
# #         if len(samplename) == 0:
# #             samplename = str(self._sampleid_edit.text()) # Use id.
#         #
#         plankton_core.PlanktonCounterManager().create_sample(datasetname, samplename)
#         #
#         self._parentwidget._emit_change_notification()
#         #
#         self.accept() # Close dialog box.


class DeleteDefaultMethodDialog(QtWidgets.QDialog):
    """ """

    def __init__(self, parentwidget):
        """ """
        self._parentwidget = parentwidget
        super(DeleteDefaultMethodDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete default method(s)")
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()

    def _content(self):
        """ """
        default_methods_listview = QtWidgets.QListView()
        self._default_methods_model = QtGui.QStandardItemModel()
        default_methods_listview.setModel(self._default_methods_model)

        clearall_button = app_framework.ClickableQLabel("Clear all")
        clearall_button.label_clicked.connect(self._uncheck_all_default_methods)
        markall_button = app_framework.ClickableQLabel("Mark all")
        markall_button.label_clicked.connect(self._check_all_default_methods)
        delete_button = QtWidgets.QPushButton("Delete marked sample(s)")
        delete_button.clicked.connect(self._delete_marked_default_methods)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close dialog box.
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(default_methods_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

        return layout

    def _load_data(self):
        """ """
        try:
            defaultmethods = (
                plankton_core.PlanktonCounterMethods().get_default_method_list()
            )

            self._default_methods_model.clear()
            for defaultmethod in defaultmethods:
                item = QtGui.QStandardItem(defaultmethod)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                item.setCheckable(True)
                self._default_methods_model.appendRow(item)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _check_all_default_methods(self):
        """ """
        try:
            for rowindex in range(self._default_methods_model.rowCount()):
                item = self._default_methods_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.CheckState.Checked)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _uncheck_all_default_methods(self):
        """ """
        try:
            for rowindex in range(self._default_methods_model.rowCount()):
                item = self._default_methods_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))

    def _delete_marked_default_methods(self):
        """ """
        try:
            for rowindex in range(self._default_methods_model.rowCount()):
                item = self._default_methods_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    selectedname = str(item.text())
                    plankton_core.PlanktonCounterMethods().delete_counting_method(
                        selectedname
                    )
            #
            self.accept()  # Close dialog box.
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
