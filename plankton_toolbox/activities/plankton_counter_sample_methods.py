#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import time
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_core
# import toolbox_utils

class PlanktonCounterSampleMethods(QtGui.QWidget):
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
        self._selectanalysismethod_list = None
        self._selectmethod_list = None
        self._selectmethod_table = None
        self._selectmethodstep_table = None
        #
        self.setLayout(self._create_content_methods())
        #
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(200, self.load_data)
#         self.load_data()
        
    def load_data(self):
        """ Load data from method stored in sample. """
        self._update_analysis_method_list()
        self._update_counting_species_list()
        self._load_current_sample_method()
#         self._select_analysis_method_changed()
        self._reset_analysis_method_values()
        
    def save_data(self):
        """ Save data to method stored in sample. """
        self._save_method_to_current_sample()
        
    def _load_current_sample_method(self):
        """ """
        sample_path = self._current_sample_object.get_dir_path()
        if os.path.exists(os.path.join(sample_path, 'counting_method.txt')):
            header, rows = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                                                sample_path, 'counting_method.txt')        
            self._current_sample_method = plankton_core.PlanktonCounterMethod(header, rows)
        else:
            self._current_sample_method = plankton_core.PlanktonCounterMethod([], [])
        
    def _save_method_to_current_sample(self):
        """ """
        if self._current_sample_method is None:
            return
        #
        sample_path = self._current_sample_object.get_dir_path()
        self._current_sample_method.save_method_config_to_file(sample_path, 'counting_method.txt')
        
    def _create_content_methods(self):
        """ """
        # Stored analysis methods.
        self._selectanalysismethod_list = QtGui.QComboBox(self)
#         self._selectanalysismethod_list.addItems(['<method for current sample>']) 
        self._selectanalysismethod_list.addItems(['<select>']) 
#         self._selectanalysismethod_list.currentIndexChanged.connect(self._select_analysis_method_changed)
        self._analysismethod_copy_button = QtGui.QPushButton('Copy values from selected setup')
        self._analysismethod_copy_button.clicked.connect(self._copy_analysis_method_values)
        self._analysismethod_reset_button = QtGui.QPushButton('Reset to used values for this sample')
        self._analysismethod_reset_button.clicked.connect(self._reset_analysis_method_values)
        # Stored methods.
        self._selectmethod_table = QtGui.QListWidget(self) # utils_qt.ToolboxQTableView(self)
        self._selectmethod_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._selectmethod_table.setStyleSheet("QListWidget::item:hover{background-color:#cccccc;}")
#         self._selectmethod_table.itemSelectionChanged.connect(self._select_method_changed)
        self._selectmethod_table.itemClicked.connect(self._select_method_changed)
        # Stored method steps.
        self._selectmethodstep_table = QtGui.QListWidget(self) # utils_qt.ToolboxQTableView(self)
        self._selectmethodstep_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._selectmethodstep_table.setStyleSheet("QListWidget::item:hover{background-color:#cccccc;}")
        self._selectmethodstep_table.itemSelectionChanged.connect(self._select_method_step_changed)
#         self._selectmethodstep_table.itemClicked.connect(self._select_method_step_changed)
#         self._methodstepdescription_edit = QtGui.QLineEdit('')
#         self._methodstepdescription_edit.textEdited.connect(self._field_changed)


        # 'qualitative_quantitative'
        self._methodtype_list = QtGui.QComboBox()
        self._methodtype_list.addItems(['Quantitative', 
                                       'Qualitative', 
                                       'Quantitative and qualitative'])
        self._methodtype_list.setMaximumWidth(200)
        self._methodtype_list.currentIndexChanged.connect(self._field_changed)


        self._sampledvolume_edit = QtGui.QLineEdit('')
        self._sampledvolume_edit.setMaximumWidth(60)
        self._sampledvolume_edit.textEdited.connect(self._field_changed)
        self._countedvolume_edit = QtGui.QLineEdit('')
        self._countedvolume_edit.setMaximumWidth(60)
        self._countedvolume_edit.textEdited.connect(self._field_changed)
        self._chamber_filter_diameter_edit = QtGui.QLineEdit('')
        self._chamber_filter_diameter_edit.setMaximumWidth(60)
        self._chamber_filter_diameter_edit.textEdited.connect(self._field_changed)
        self._preservative_list = QtGui.QComboBox()
        self._preservative_list.setEditable(True)
        self._preservative_list.addItems([  '<select or edit>', 
                                            'ALU (Alkaline Lugol´s solution)', 
                                            'CLU (Acid Lugol´s solution)', 
                                            'LUG (Neutral Lugol´s solution)', 
                                            'NBF (Formalin - neutral buffered formalin 10%)', 
                                            'GLU (Glutaraldehyde)', 
                                                 ])
        self._preservative_list.setMaximumWidth(200)
        self._preservative_list.currentIndexChanged.connect(self._field_changed)
        #
        self._preservative_volume_edit = QtGui.QLineEdit('')
        self._preservative_volume_edit.setMaximumWidth(60)
        self._preservative_volume_edit.textEdited.connect(self._field_changed)
        # 
        self._magnification_edit = QtGui.QLineEdit('')
        self._magnification_edit.setMaximumWidth(60)
        self._magnification_edit.textEdited.connect(self._field_changed)
        self._microscope_edit = QtGui.QLineEdit('')
        self._microscope_edit.textEdited.connect(self._field_changed)
        self._countareatype_list = QtGui.QComboBox()
        self._countareatype_list.addItems(['<select>', 
                                           'Chamber/filter', 
                                           '1/2 Chamber/filter', 
                                           'Field of views', 
                                           'Transects',  
                                           'Rectangles'])
        self._countareatype_list.currentIndexChanged.connect(self._field_changed)
        self._viewdiameter_edit = QtGui.QLineEdit('')
        self._viewdiameter_edit.setMaximumWidth(60)
        self._viewdiameter_edit.textEdited.connect(self._field_changed)
        self._transectrectanglewidth_edit = QtGui.QLineEdit('')
        self._transectrectanglewidth_edit.setMaximumWidth(60)
        self._transectrectanglewidth_edit.textEdited.connect(self._field_changed)
        self._transectrectanglelength_edit = QtGui.QLineEdit('')
        self._transectrectanglelength_edit.setMaximumWidth(60)
        self._transectrectanglelength_edit.textEdited.connect(self._field_changed)
        self._coefficient_one_unit_edit = QtGui.QLineEdit()
        self._coefficient_one_unit_edit.setMaximumWidth(100)
        self._coefficient_one_unit_edit.setEnabled(False)

        self._counting_species_list = QtGui.QComboBox()
        self._counting_species_list.addItems(['<all species>'])
        self._counting_species_list.currentIndexChanged.connect(self._field_changed)
        self._viewsizeclassinfo_checkbox = QtGui.QCheckBox('View sizeclass info')
        self._viewsizeclassinfo_checkbox.setChecked(True) 
        self._viewsizeclassinfo_checkbox.stateChanged.connect(self._field_changed)

        # Buttons.
#         self._addmethod_button = QtGui.QPushButton('Add method...')
#         self._addmethod_button.clicked.connect(self._add_method)

        self._addmethodstep_button = QtGui.QPushButton('Add method/method step...')
        self._addmethodstep_button.clicked.connect(self._add_method_step)
        self._deletemethodsteps_method_button = QtGui.QPushButton('Delete method step(s)...')
        self._deletemethodsteps_method_button.clicked.connect(self._delete_method_steps)
        
        self._saveanalysis_method_button = QtGui.QPushButton('Save changes to selected default method setup')
        self._saveanalysis_method_button.clicked.connect(self._save_analysis_method)
        self._saveasanalysis_method_button = QtGui.QPushButton('Save method setup as...')
        self._saveasanalysis_method_button.clicked.connect(self._save_as_analysis_method)
        self._deleteanalysis_method_button = QtGui.QPushButton('Delete default method setup(s)...')
        self._deleteanalysis_method_button.clicked.connect(self._analysis_method_delete)

        # Layout widgets.
        
        # ===== GRID 1. =====
        grid1 = QtGui.QGridLayout()
        gridrow = 0
        grid1.addWidget(utils_qt.LeftAlignedQLabel('<b>Counting methods</b>'), gridrow, 0, 1, 10)
        gridrow += 1
        grid1.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.
        gridrow += 1
        grid1.addWidget(utils_qt.RightAlignedQLabel('Default method setup:'), gridrow, 0, 1, 1)
        grid1.addWidget(self._selectanalysismethod_list, gridrow, 1, 1, 2)
        gridrow += 1
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._analysismethod_copy_button)
        hbox.addWidget(self._analysismethod_reset_button)
        hbox.addStretch(10)
        grid1.addLayout(hbox, gridrow, 1, 1, 2)
        gridrow += 1
        grid1.setRowStretch(gridrow, 10)
        gridrow += 1
        grid1.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.

        # ===== GRID 2. =====
        grid2 = QtGui.QGridLayout()
        gridrow = 0
        grid2.addWidget(utils_qt.LeftAlignedQLabel('<b>Methods:</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        grid2.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.
        gridrow += 1
        grid2.addWidget(self._selectmethod_table, gridrow, 0, 10, 1)

        # ===== GRID 3. =====
        grid3 = QtGui.QGridLayout()
        gridrow = 0
        grid3.addWidget(utils_qt.LeftAlignedQLabel('<b>Method values:</b>'), gridrow, 0, 1, 2)
        gridrow += 1
        grid3.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.
        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Sampled volume (mL):'), gridrow, 0, 1, 1)
        grid3.addWidget(self._sampledvolume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Preservative:'), gridrow, 0, 1, 1)
        grid3.addWidget(self._preservative_list, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Preservative volume (mL):'), gridrow, 0, 1, 1)
        grid3.addWidget(self._preservative_volume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Counted volume (mL):'), gridrow, 0, 1, 1)
        grid3.addWidget(self._countedvolume_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Chamber/filter diameter (mm):'), gridrow, 0, 1, 1)
        grid3.addWidget(self._chamber_filter_diameter_edit, gridrow, 1, 1, 1)

        gridrow += 1
        grid3.addWidget(utils_qt.RightAlignedQLabel('Method type:'), gridrow, 0, 1, 1)
        grid3.addWidget(self._methodtype_list, gridrow, 1, 1, 1)
        
        gridrow += 1
        grid3.setRowStretch(gridrow, 10)

        # ===== GRID 4. =====
        grid4 = QtGui.QGridLayout()
        gridrow = 0
        grid4.addWidget(utils_qt.LeftAlignedQLabel('<b>Method steps:</b>'), gridrow, 0, 1, 1)
        gridrow += 1
        grid4.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.
        gridrow += 1
        grid4.addWidget(self._selectmethodstep_table, gridrow, 0, 10, 1)

        # ===== GRID 5. =====
        grid5 = QtGui.QGridLayout()
        gridrow = 0
        grid5.addWidget(utils_qt.LeftAlignedQLabel('<b>Method step values:</b>'), gridrow, 0, 1, 2)
        gridrow += 1
        grid5.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 1) # Add space.
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Magnification:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._magnification_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Microscope:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._microscope_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Count area type:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._countareatype_list, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Diameter of view (mm):'), gridrow, 0, 1, 1)
        grid5.addWidget(self._viewdiameter_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Transect/rectangle width (mm):'), gridrow, 0, 1, 1)
        grid5.addWidget(self._transectrectanglewidth_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Transect/rectangle length (mm):'), gridrow, 0, 1, 1)
        grid5.addWidget(self._transectrectanglelength_edit, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(utils_qt.LeftAlignedQLabel('Calculated coefficient for one area:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._coefficient_one_unit_edit, gridrow, 1, 1, 1)     
        gridrow += 1
        grid5.addWidget(utils_qt.RightAlignedQLabel('Default counting species list:'), gridrow, 0, 1, 1)
        grid5.addWidget(self._counting_species_list, gridrow, 1, 1, 1)
        gridrow += 1
        grid5.addWidget(self._viewsizeclassinfo_checkbox, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addLayout(grid2, 10)
        hbox1.addLayout(grid3, 5)
        hbox1.addStretch(5)
        hbox1.addLayout(grid4, 10)
        hbox1.addLayout(grid5, 10)
        hbox1.addStretch(20)
        # 
        hbox2 = QtGui.QHBoxLayout()
#         hbox2.addWidget(self._addmethod_button)
        hbox2.addWidget(self._addmethodstep_button)
        hbox2.addWidget(self._deletemethodsteps_method_button)
        hbox2.addStretch(1)
        hbox2.addWidget(self._saveanalysis_method_button)
        hbox2.addWidget(self._saveasanalysis_method_button)
        hbox2.addWidget(self._deleteanalysis_method_button)
        hbox2.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        layout.addWidget(utils_qt.LeftAlignedQLabel('<b>Manage counting method setups:</b>'))
        layout.addLayout(hbox2)
        #
        return layout       
        
    def _update_analysis_method_list(self):
        """ """
        self._selectanalysismethod_list.clear()
        #
        analysismethods = plankton_core.PlanktonCounterMethods().get_analysis_method_list()
        if len(analysismethods) > 0:
            self._selectanalysismethod_list.addItems(['<select>'] + analysismethods)
#             self._selectanalysismethod_list.addItems(analysismethods)
        else:
            self._selectanalysismethod_list.addItems(['<not available>'])            
            
    def _update_counting_species_list(self):
        """ """
        self._counting_species_list.clear()
        specieslists = plankton_core.PlanktonCounterMethods().get_counting_species_lists()
        if len(specieslists) > 0:
            self._counting_species_list.addItems(['<all species>'] + specieslists)
        else:
            self._counting_species_list.addItems(['<not available>'])        
        
    def _copy_analysis_method_values(self):
        """ """
        self._selectmethod_table.clear()
        self._selectmethodstep_table.clear()
        self._update_method_step_fields({}) # Clear.
        #
        if self._selectanalysismethod_list.currentIndex() == 0:
            self._load_current_sample_method()
        else:
            selectedanalysismethod = unicode(self._selectanalysismethod_list.currentText())
            try:
                path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                header, rows = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                                                                    path, selectedanalysismethod + '.txt')      
                self._current_sample_method = plankton_core.PlanktonCounterMethod(header, rows)
            except:
                self._current_sample_method = plankton_core.PlanktonCounterMethod([], [])
        #
        self._update_method_table()
        self._update_method_step_table()
#####        
    def _update_method_table(self):
        """ """
        self._selectmethod_table.clear()
        #
        countingmethods = self._current_sample_method.get_counting_methods_list()
        if len(countingmethods) > 0:
            self._selectmethod_table.addItems(countingmethods)
            self._selectmethod_table.setCurrentRow(0)
        else:
            self._selectmethod_table.addItems(['<not available>'])
            self._selectmethod_table.setCurrentRow(0)

    def _update_method_step_table(self):
        """ """
        self._selectmethodstep_table.clear()
        #
        currentmethod = unicode(self._selectmethod_table.currentItem().text())
        countingmethods = self._current_sample_method.get_counting_method_steps_list(currentmethod)
        if len(countingmethods) > 0:
            self._selectmethodstep_table.addItems(countingmethods)
            self._selectmethodstep_table.setCurrentRow(0)
        else:
            self._selectmethodstep_table.addItems(['<not available>'])
            self._selectmethodstep_table.setCurrentRow(0)

    def _reset_analysis_method_values(self):
        """ """
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
            self._selectmethod_table.addItems(['<not available>'])
            self._selectmethod_table.setCurrentRow(0)
        #
        currentmethod = unicode(self._selectmethod_table.currentItem().text())
        countingmethods = self._current_sample_method.get_counting_method_steps_list(currentmethod)
        if len(countingmethods) > 0:
            self._selectmethodstep_table.addItems(countingmethods)
            self._selectmethodstep_table.setCurrentRow(0)
        else:
            self._selectmethodstep_table.addItems(['<not available>'])
            self._selectmethodstep_table.setCurrentRow(0)
#####
    def _update_method_fields(self, fields_dict):
        """ """
        try:
            self._dont_update_current_sample_method_flag = True
            #
#             self._methodstepdescription_edit.setText(fields_dict.get('method_description', ''))

            #
            methodtype = fields_dict.get('qualitative_quantitative', '')
            currentindex = self._methodtype_list.findText(methodtype, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._methodtype_list.setCurrentIndex(currentindex)
            else:
                self._methodtype_list.setCurrentIndex(0)


            
            self._sampledvolume_edit.setText(fields_dict.get('sampled_volume_ml', ''))
            #
            preservative = fields_dict.get('preservative', '')
            currentindex = self._preservative_list.findText(preservative, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._preservative_list.setCurrentIndex(currentindex)
            else:
                self._preservative_list.setCurrentIndex(0, preservative)
            #
            self._preservative_volume_edit.setText(fields_dict.get('preservative_volume_ml', ''))
            self._countedvolume_edit.setText(fields_dict.get('counted_volume_ml', ''))
            self._chamber_filter_diameter_edit.setText(fields_dict.get('chamber_filter_diameter_mm', ''))
            #
            self._magnification_edit.setText(fields_dict.get('magnification', ''))
            self._microscope_edit.setText(fields_dict.get('microscope', ''))
            #
            comboindex = self._countareatype_list.findText(fields_dict.get('count_area_type', '<select>'))
            self._countareatype_list.setCurrentIndex(comboindex)
            #
            self._viewdiameter_edit.setText(fields_dict.get('diameter_of_view_mm', ''))
            self._transectrectanglelength_edit.setText(fields_dict.get('transect_rectangle_length_mm', ''))
            self._transectrectanglewidth_edit.setText(fields_dict.get('transect_rectangle_width_mm', ''))
            self._coefficient_one_unit_edit.setText(fields_dict.get('coefficient_one_unit', ''))
            #
            comboindex = self._counting_species_list.findText(fields_dict.get('counting_species_list', '<all species>'))
            self._counting_species_list.setCurrentIndex(comboindex)
            #
            combostate = fields_dict.get('view_sizeclass_info', 'FALSE')
            if combostate.upper() == 'TRUE':
                self._viewsizeclassinfo_checkbox.setChecked(True)
            else:
                self._viewsizeclassinfo_checkbox.setChecked(False)
            #
##             self._calculate_coefficient_one_unit()
        finally:
            self._dont_update_current_sample_method_flag = False
#####
    def _select_method_changed(self):
        """ """
        if self._current_sample_method is None:
            return
        #
        self._update_method_fields({}) # Clear.
        #
        selectedmethod = unicode(self._selectmethod_table.currentItem().text())
        #
        fields_dict = self._current_sample_method.get_counting_method_fields(selectedmethod)
        self._update_method_fields(fields_dict)
        #
        self._update_method_step_table()

    def _select_method_step_changed(self):
        """ """
        if self._current_sample_method is None:
            return
        #
        self._update_method_step_fields({}) # Clear.
        #
        selectedmethodstep = unicode(self._selectmethodstep_table.currentItem().text())
        #
        fields_dict = self._current_sample_method.get_counting_method_step_fields(selectedmethodstep)
        self._update_method_step_fields(fields_dict)

    def _update_method_step_fields(self, fields_dict):
        """ """
        try:
            self._dont_update_current_sample_method_flag = True
            #
#             self._methodstepdescription_edit.setText(fields_dict.get('method_step_description', ''))


            #
            methodtype = fields_dict.get('qualitative_quantitative', '')
            currentindex = self._methodtype_list.findText(methodtype, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._methodtype_list.setCurrentIndex(currentindex)
            else:
                self._methodtype_list.setCurrentIndex(0)


            
            self._sampledvolume_edit.setText(fields_dict.get('sampled_volume_ml', ''))
            #
            preservative = fields_dict.get('preservative', '')
            currentindex = self._preservative_list.findText(preservative, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._preservative_list.setCurrentIndex(currentindex)
            else:
                self._preservative_list.setItemText(0, preservative)
            #
            self._preservative_volume_edit.setText(fields_dict.get('preservative_volume_ml', ''))
            self._countedvolume_edit.setText(fields_dict.get('counted_volume_ml', ''))
            self._chamber_filter_diameter_edit.setText(fields_dict.get('chamber_filter_diameter_mm', ''))
            #
            self._magnification_edit.setText(fields_dict.get('magnification', ''))
            self._microscope_edit.setText(fields_dict.get('microscope', ''))
            #
            comboindex = self._countareatype_list.findText(fields_dict.get('count_area_type', '<select>'))
            self._countareatype_list.setCurrentIndex(comboindex)
            #
            self._viewdiameter_edit.setText(fields_dict.get('diameter_of_view_mm', ''))
            self._transectrectanglelength_edit.setText(fields_dict.get('transect_rectangle_length_mm', ''))
            self._transectrectanglewidth_edit.setText(fields_dict.get('transect_rectangle_width_mm', ''))
            self._coefficient_one_unit_edit.setText(fields_dict.get('coefficient_one_unit', ''))
            #
            comboindex = self._counting_species_list.findText(fields_dict.get('counting_species_list', '<all species>'))
            self._counting_species_list.setCurrentIndex(comboindex)
            #
            combostate = fields_dict.get('view_sizeclass_info', 'FALSE')
            if combostate.upper() == 'TRUE':
                self._viewsizeclassinfo_checkbox.setChecked(True)
            else:
                self._viewsizeclassinfo_checkbox.setChecked(False)
            #
##             self._calculate_coefficient_one_unit()
        finally:
            self._dont_update_current_sample_method_flag = False

    def _field_changed(self):
        """ """
##         self._calculate_coefficient_one_unit()
        self._update_current_sample_method()
#         # If any field changed, then go back to sample method.
#         self._selectanalysismethod_list.setCurrentIndex(0)

    def _update_current_sample_method(self):
        """ Get info for both method and method step. """
        if self._dont_update_current_sample_method_flag:
            return
        # Method.
        if not self._current_sample_method:
            return 
        #
        fields_dict = {}
        fields_dict['counting_method'] = unicode(self._selectmethod_table.currentItem().text())
        fields_dict['counting_method_step'] = unicode(self._selectmethodstep_table.currentItem().text())
#         fields_dict['method_step_description'] = unicode(self._methodstepdescription_edit.text())


        fields_dict['qualitative_quantitative'] = unicode(self._methodtype_list.currentText())
        
        
        fields_dict['sampled_volume_ml'] = unicode(self._sampledvolume_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['preservative'] = unicode(self._preservative_list.currentText())
        fields_dict['preservative_volume_ml'] = unicode(self._preservative_volume_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['counted_volume_ml'] = unicode(self._countedvolume_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['chamber_filter_diameter_mm'] = unicode(self._chamber_filter_diameter_edit.text()).replace(',', '.').replace(' ', '')
        # 
        fields_dict['magnification'] = unicode(self._magnification_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['microscope'] = unicode(self._microscope_edit.text())
          
        fields_dict['count_area_type'] = unicode(self._countareatype_list.currentText())
          
        fields_dict['diameter_of_view_mm'] = unicode(self._viewdiameter_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['transect_rectangle_length_mm'] = unicode(self._transectrectanglelength_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['transect_rectangle_width_mm'] = unicode(self._transectrectanglewidth_edit.text()).replace(',', '.').replace(' ', '')
        fields_dict['coefficient_one_unit'] = unicode(self._coefficient_one_unit_edit.text()).replace(',', '.').replace(' ', '')
        
        fields_dict['counting_species_list'] = unicode(self._counting_species_list.currentText())
        if self._viewsizeclassinfo_checkbox.isChecked():
            fields_dict['view_sizeclass_info'] = 'TRUE'
        else:
            fields_dict['view_sizeclass_info'] = 'FALSE'
        #
        counting_method = fields_dict['counting_method']
        counting_method_step = fields_dict['counting_method_step']
        self._current_sample_method.update_counting_method_step_fields(counting_method, counting_method_step, fields_dict)
        # Update coefficient field.
        self._current_sample_method.calculate_coefficient_one_unit(fields_dict)
        self._coefficient_one_unit_edit.setText(fields_dict.get('coefficient_one_unit', '0'))
 

## Moved to plankton_counte_methods.py
#     def _calculate_coefficient_one_unit(self, fields_dict):
#         """ """
#         # Clear result.
#         self._coefficient_one_unit_edit.setText('0')
#         #
#         try:
#             # From analysis method.
# #             sampledvolume_ml = unicode(self._sampledvolume_edit.text())
# #             preservative_volume_ml = unicode(self._preservative_volume_edit.text())
# #             counted_volume_ml = unicode(self._countedvolume_edit.text())
# #             chamber_filter_diameter_mm = unicode(self._chamber_filter_diameter_edit.text())
# #             # From analysis method step.
# #             countareatype = unicode(self._countareatype_list.currentText())
# #             diameterofview_mm = unicode(self._viewdiameter_edit.text())
# #             transectrectanglelength_mm = unicode(self._transectrectanglelength_edit.text())
# #             transectrectanglewidth_mm = unicode(self._transectrectanglewidth_edit.text())
#             sampledvolume_ml = fields_dict.get('sampled_volume_ml', 0.0)
#             preservative_volume_ml = fields_dict.get('preservative_volume_ml', 0.0)
#             counted_volume_ml = fields_dict.get('counted_volume_ml', 0.0)
#             chamber_filter_diameter_mm = fields_dict.get('chamber_filter_diameter_mm', 0.0)
#             # From analysis method step.
#             countareatype = fields_dict.get('count_area_type', 0.0)
#             diameterofview_mm = fields_dict.get('diameter_of_view_mm', 0.0)
#             transectrectanglelength_mm = fields_dict.get('transect_rectangle_length_mm', 0.0)
#             transectrectanglewidth_mm = fields_dict.get('transect_rectangle_width_mm', 0.0)
#             #
#             if not chamber_filter_diameter_mm:
#                 return
#             if not sampledvolume_ml:
#                 return
#             if not counted_volume_ml:
#                 return
#             #
#             chamber_filter_area = ((float(chamber_filter_diameter_mm) / 2) ** 2) * math.pi # r2*pi.
#             sampledvolume = float(sampledvolume_ml)
#             counted_volume = float(counted_volume_ml)
#             #
#             try: preservative_volume = float(preservative_volume_ml)
#             except: preservative_volume = 0.0
#             singlearea = 1.0
#             #
#             if countareatype == 'Chamber/filter':
#                 singlearea = chamber_filter_area
#             if countareatype == '1/2 Chamber/filter':
#                 singlearea = chamber_filter_area * 0.5
#             if countareatype == 'Field of views':
#                 singlearea = ((float(diameterofview_mm) / 2) ** 2) * math.pi # r2*pi.
#             if countareatype == 'Transects':
#                 singlearea = float(transectrectanglelength_mm) * float(transectrectanglewidth_mm) # l * w.
#             if countareatype == 'Rectangles':
#                 singlearea = float(transectrectanglelength_mm) * float(transectrectanglewidth_mm) # l * w.
#             
#             # Calculate coeff.
#             onelitre_ml = 1000.0
#             coeffoneunit = chamber_filter_area * sampledvolume * onelitre_ml / (singlearea * counted_volume * (sampledvolume + preservative_volume))
#             coeffoneunit = int(coeffoneunit + 0.5) # Round.
# #             self._coefficient_one_unit_edit.setText(unicode(coeffoneunit))
#             fields_dict['coefficient_one_unit'] = unicode(coeffoneunit)
#         #
#         except:
#             fields_dict['coefficient_one_unit'] = unicode(coeffoneunit)
        
    def _save_analysis_method(self):
        """ """
        if self._current_sample_method is None:
            return
        #
        self._update_current_sample_method()
        #
        if self._selectanalysismethod_list.currentIndex() == 0:
            self._save_method_to_current_sample()
        else:
            selectedanalysismethod = unicode(self._selectanalysismethod_list.currentText())
            path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
            self._current_sample_method.save_method_config_to_file(path, selectedanalysismethod + '.txt')
            # Also save to current sample.
            self._save_method_to_current_sample()
#####
#     def _add_method(self):
#         """ """
#         old_method = ''
#         if self._selectanalysismethod_list.currentIndex() > 0:
#             old_method = unicode(self._selectanalysismethod_list.currentText())
#         current_method = unicode(self._selectmethod_table.currentItem().text())
#         #
#         dialog = AddMethodDialog(self, self._current_sample_method, current_method)
#         if dialog.exec_():
#             if old_method:
#                 path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
#                 self._current_sample_method.save_method_config_to_file(path, old_method + '.txt')
#             #
#             self._update_analysis_method_list()
#             #
#             currentindex = self._selectanalysismethod_list.findText(old_method, QtCore.Qt.MatchFixedString)
#             if currentindex >= 0:
#                 self._selectanalysismethod_list.setCurrentIndex(currentindex)
#             #
#             self._update_method_table()
            
    def _add_method_step(self):
        """ """
        old_method = ''
        if self._selectanalysismethod_list.currentIndex() > 0:
            old_method = unicode(self._selectanalysismethod_list.currentText())
        current_method = unicode(self._selectmethod_table.currentItem().text())
        current_method_step = unicode(self._selectmethodstep_table.currentItem().text())
        #
        dialog = AddMethodStepDialog(self, self._current_sample_method, current_method, current_method_step)
        if dialog.exec_():
            if old_method:
                path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                self._current_sample_method.save_method_config_to_file(path, old_method + '.txt')
            #
            self._update_analysis_method_list()
            #
            currentindex = self._selectanalysismethod_list.findText(old_method, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._selectanalysismethod_list.setCurrentIndex(currentindex)
            #
            self._update_method_table()
            self._update_method_step_table()

    def _delete_method_steps(self):
        """ """
        old_method = ''
        if self._selectanalysismethod_list.currentIndex() > 0:
            old_method = unicode(self._selectanalysismethod_list.currentText())
        #
        dialog = DeleteMethodStepsDialog(self, self._current_sample_method)
        if dialog.exec_():
            if old_method:
                path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                self._current_sample_method.save_method_config_to_file(path, old_method + '.txt')
            #
            self._update_analysis_method_list()
            #
            currentindex = self._selectanalysismethod_list.findText(old_method, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._selectanalysismethod_list.setCurrentIndex(currentindex)
            #
            self._update_method_table()
            self._update_method_step_table()
            
    def _save_as_analysis_method(self):
        """ """
        if self._current_sample_method is None:
            return
        #
        self._update_current_sample_method()
        #
        old_name = ''
        if self._selectanalysismethod_list.currentIndex() > 0:
            old_name = unicode(self._selectanalysismethod_list.currentText())
        #
        dialog = SaveAnalysismethodAsDialog(self, old_name)
        if dialog.exec_():
            new_name = dialog.get_new_name()
            if new_name:
                path = plankton_core.PlanktonCounterMethods().get_methods_dir_path()
                self._current_sample_method.save_method_config_to_file(path, new_name + '.txt')
                #
                self._update_analysis_method_list()
                #
                currentindex = self._selectanalysismethod_list.findText(new_name, QtCore.Qt.MatchFixedString)
                if currentindex >= 0:
                    self._selectanalysismethod_list.setCurrentIndex(currentindex)

    def _analysis_method_delete(self):
        """ """
        dialog = DeleteAnalysisMethodDialog(self)
        if dialog.exec_():
            self._update_analysis_method_list()


#####
# class AddMethodDialog(QtGui.QDialog):
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
#         self._new_method_edit = QtGui.QLineEdit(self._current_method)
#         self._new_method_edit.setMinimumWidth(400)
# #         self._copycontent_checkbox = QtGui.QCheckBox('Copy content')
# #         self._copycontent_checkbox.setChecked(True) 
# 
#         save_button = QtGui.QPushButton('Save')
#         save_button.clicked.connect(self._save)               
#         cancel_button = QtGui.QPushButton('Cancel')
#         cancel_button.clicked.connect(self.reject) # Close dialog box.               
#         # Layout widgets.
#         formlayout = QtGui.QFormLayout()
#         formlayout.addRow('New method:', self._new_method_edit)
# #         formlayout.addRow('', self._copycontent_checkbox)
#          
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addStretch(10)
#         hbox1.addWidget(save_button)
#         hbox1.addWidget(cancel_button)
#         #
#         layout = QtGui.QVBoxLayout()
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
#         new_method_dict['counting_method'] = unicode(self._new_method_edit.text())
#         self._current_sample_method.add_method(new_method_dict)          
#         #            
#         self.accept() # Close dialog box.
  
class AddMethodStepDialog(QtGui.QDialog):
    """ """
    def __init__(self, parentwidget, current_sample_method, current_method, current_method_step):
        """ """
        self._parentwidget = parentwidget
        self._current_sample_method = current_sample_method
        self._current_method = current_method
        self._current_method_step = current_method_step
        super(AddMethodStepDialog, self).__init__(parentwidget)
        self.setWindowTitle('Add method or method step')
        self.setLayout(self._content())
 
    def get_new_method_step(self):
        """ """
        return self._new_method_step
 
    def _content(self):
        """ """
        self._new_method_edit = QtGui.QLineEdit(self._current_method)
        self._new_method_edit.setMinimumWidth(400)
        self._new_method_step_edit = QtGui.QLineEdit(self._current_method_step)
        self._new_method_step_edit.setMinimumWidth(400)
        self._copycontent_checkbox = QtGui.QCheckBox('Copy content')
        self._copycontent_checkbox.setChecked(True) 

        save_button = QtGui.QPushButton('Save')
        save_button.clicked.connect(self._save)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
        formlayout.addRow('New method:', self._new_method_edit)
        formlayout.addRow('New method step:', self._new_method_step_edit)
        formlayout.addRow('', self._copycontent_checkbox)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(save_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                
 
    def _save(self):
        """ """
        new_method_step_dict = {}
        if self._copycontent_checkbox.isChecked():
            new_method_step_dict.update(self._current_sample_method.get_counting_method_step_fields(self._current_method_step))
        #
        new_method_step_dict['counting_method'] = unicode(self._new_method_edit.text())
        new_method_step_dict['counting_method_step'] = unicode(self._new_method_step_edit.text())
        self._current_sample_method.add_method_step(new_method_step_dict)          
        #            
        self.accept() # Close dialog box.
 
 
class DeleteMethodStepsDialog(QtGui.QDialog):
    """  """
    def __init__(self, parentwidget, current_sample_method):
        """ """
        self._parentwidget = parentwidget
        self._current_sample_method = current_sample_method
        super(DeleteMethodStepsDialog, self).__init__(parentwidget)
        self.setWindowTitle('Delete marked method(s)')
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()
 
    def _content(self):
        """ """  
        methodsteps_listview = QtGui.QListView()
        self._methodsteps_model = QtGui.QStandardItemModel()
        methodsteps_listview.setModel(self._methodsteps_model)
 
        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_rows)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_rows)                
        delete_button = QtGui.QPushButton('Delete marked method step(s)')
        delete_button.clicked.connect(self._delete_marked_rows)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(methodsteps_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
         
        return layout                
 
    def _load_data(self):
        """ """
        methodstepslists = self._current_sample_method.get_counting_method_steps_list()
 
        self._methodsteps_model.clear()        
        for methodstep in methodstepslists:
            item = QtGui.QStandardItem(methodstep)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._methodsteps_model.appendRow(item)
             
    def _check_all_rows(self):
        """ """
        for rowindex in range(self._methodsteps_model.rowCount()):
            item = self._methodsteps_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
             
    def _uncheck_all_rows(self):
        """ """
        for rowindex in range(self._methodsteps_model.rowCount()):
            item = self._methodsteps_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
 
    def _delete_marked_rows(self):
        """ """
        for rowindex in range(self._methodsteps_model.rowCount()):
            item = self._methodsteps_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedname = unicode(item.text())
                self._current_sample_method.delete_method_step(selectedname)
        #            
        self.accept() # Close dialog box.
 
class SaveAnalysismethodAsDialog(QtGui.QDialog):
    """ """
    def __init__(self, parentwidget, old_name):
        """ """
        self._old_name = old_name
        self._new_name = ''
        super(SaveAnalysismethodAsDialog, self).__init__(parentwidget)
        self.setWindowTitle("Save analysis method as")
        self.setLayout(self._content())

    def get_new_name(self):
        """ """
        return self._new_name

    def _content(self):
        """ """
        self._new_name_edit = QtGui.QLineEdit(self._old_name)
        self._new_name_edit.setMinimumWidth(400)
        save_button = QtGui.QPushButton('Save')
        save_button.clicked.connect(self._save)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
        formlayout.addRow('New analysis method name:', self._new_name_edit)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(save_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _save(self):
        """ """
        self._new_name = unicode(self._new_name_edit.text())
        #            
        self.accept() # Close dialog box.


class DeleteAnalysisMethodDialog(QtGui.QDialog):
    """  """
    def __init__(self, parentwidget):
        """ """
        self._parentwidget = parentwidget
        super(DeleteAnalysisMethodDialog, self).__init__(parentwidget)
        self.setWindowTitle('Delete analysis method(s)')
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()

    def _content(self):
        """ """  
        analysis_methods_listview = QtGui.QListView()
        self._analysis_methods_model = QtGui.QStandardItemModel()
        analysis_methods_listview.setModel(self._analysis_methods_model)

        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_analysis_methods)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_analysis_methods)                
        delete_button = QtGui.QPushButton('Delete marked sample(s)')
        delete_button.clicked.connect(self._delete_marked_analysis_methods)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(analysis_methods_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        
        return layout                

    def _load_data(self):
        """ """
        analysismethods = plankton_core.PlanktonCounterMethods().get_analysis_method_list()

        self._analysis_methods_model.clear()        
        for analysismethod in analysismethods:
            item = QtGui.QStandardItem(analysismethod)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._analysis_methods_model.appendRow(item)
            
    def _check_all_analysis_methods(self):
        """ """
        for rowindex in range(self._analysis_methods_model.rowCount()):
            item = self._analysis_methods_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_analysis_methods(self):
        """ """
        for rowindex in range(self._analysis_methods_model.rowCount()):
            item = self._analysis_methods_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _delete_marked_analysis_methods(self):
        """ """
        for rowindex in range(self._analysis_methods_model.rowCount()):
            item = self._analysis_methods_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedname = unicode(item.text())
                plankton_core.PlanktonCounterMethods().delete_counting_method(selectedname)
        #            
        self.accept() # Close dialog box.

