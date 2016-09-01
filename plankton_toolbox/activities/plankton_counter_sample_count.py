#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import string
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_core

class PlanktonCounterSampleCount(QtGui.QWidget):
    """ """
    def __init__(self, parentwidget, dataset, sample, current_sample_object):
        """ """        
        self._parentwidget = parentwidget
        self._current_dataset = dataset
        self._current_sample = sample
        self._current_sample_object = current_sample_object
        #
        self._current_sample_method = None
        self._current_sample_method_step_fields = {}
        self._dont_update_flag = False # Control flow flag. (Note: control flags are dirty coding, but...)
        self._dont_get_sample_row_flag = False # Control flow flags.
        #
        super(PlanktonCounterSampleCount, self).__init__()
        #
        self.setLayout(self._create_content_species_count())
        #
        self.load_data()
                         
    def load_data(self):
        """ """
        # Load common parts.
        self._update_select_specieslist_combo()             
        self._update_selected_specieslist(None) 
        # Load from files.
        self._load_counting_method()
        self._current_sample_object.load_sample_info()
        self._current_sample_object.load_sample_data()
        # Get sample info and set state as last time.
        sample_info_dict = self._current_sample_object.get_sample_info()
        methodstep = sample_info_dict.get('last_used_method_step', '')
        self.update_method_step(methodstep)
        # Summary.
        self._update_summary()
 
    def save_data(self):
        """ """
        self._current_sample_object.save_sample_data()
        # Update info method steps and counting areas.
        methodstep = unicode(self._selectmethodstep_list.currentText())
        maxcountarea = unicode(self._countareanumber_list.count())
        info_dict = {}
        if methodstep:
            info_dict['last_used_method_step'] = methodstep
        if maxcountarea:
            info_dict['max_count_area<+>' + methodstep] = maxcountarea
        #
        self._current_sample_object.update_sample_info(info_dict)
        self._current_sample_object.save_sample_info()
 
    def _create_content_species_count(self):
        """ """
        # Column 1: Species lists for counting.
        self._selectspecieslist_list = KeyPressQComboBox(self)
        self._selectspecieslist_list.addItems(['<select>'])
        self._selectspecieslist_list.currentIndexChanged.connect(self._selected_species_list_changed)
        # 
        self._species_tableview = KeyPressToolboxQTableView(self, filter_column_index = 0)
        self._species_tableview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._species_tableview.setStyleSheet("QTableView::item:hover{background-color:#cccccc;}")
        self._species_tableview.getSelectionModel().selectionChanged.connect(self._selected_species_in_table_changed)
        # Filter for specieslist.
        self._speciesfilter_edit = KeyPressQLineEdit(self)
        self._speciesfilter_edit.textChanged.connect(self._species_tableview.onFilterTextChanged)
        self._speciesfilterclear_button = KeyPressQPushButton('Clear', self)
        self._speciesfilterclear_button.clicked.connect(self._species_filter_clear)
        # Checkbox for sizeclass info.
        self._viewsizeclassinfo_checkbox = QtGui.QCheckBox('View sizeclass info')
        self._viewsizeclassinfo_checkbox.setChecked(True)
        self._viewsizeclassinfo_checkbox.stateChanged.connect(self._selected_species_list_changed)
         
        # Column 2: Counting.
        # - Method steps.
        self._selectmethodstep_list = QtGui.QComboBox(self)
        self._selectmethodstep_list.addItems(['<not available>']) 
        self._selectmethodstep_list.currentIndexChanged.connect(self._select_method_step_changed)
        self._nextmethodstep_button = KeyPressQPushButton('Next step', self)
        self._nextmethodstep_button.clicked.connect(self._next_method_step)
        # Transects or views.
        self._countareatype_edit = KeyPressQLineEdit(self)
        self._countareatype_edit.setEnabled(False)
        self._countareanumber_list = QtGui.QComboBox(self)
        self._countareanumber_list.setMinimumWidth(60)
        self._countareanumber_list.addItems(['1']) 
        self._addcountarea_button = KeyPressQPushButton('Add count area', self)
        self._addcountarea_button.clicked.connect(self._add_count_area)
        self._locktaxa_button = KeyPressQPushButton('Lock taxa...', self)
        self._locktaxa_button.clicked.connect(self._lock_taxa)
        self._coefficient_edit = KeyPressQLineEdit(self)
        self._coefficient_edit.setEnabled(False)

        # Species.
        self._selectedspecies_edit = KeyPressQLineEdit(self)
        self._selectedspecies_edit.textChanged.connect(self._selected_species_changed)
        self._selectedspecies_edit.textChanged.connect(self._update_scientific_full_name)
        self._speciesfullname_edit = KeyPressQLineEdit(self)
        self._speciesfullname_edit.setEnabled(False)
#         self._speciesfullname_edit.textChanged.connect(self._update_scientific_full_name)
        self._taxon_sflag_list = QtGui.QComboBox(self)
        self._taxon_sflag_list.addItems(['', 'sp.', 'spp.', 'GRP', 'CPX']) 
        self._taxon_sflag_list.currentIndexChanged.connect(self._update_species_flag)
        self._taxon_cf_list = QtGui.QComboBox(self)
        self._taxon_cf_list.addItems(['', 'cf. (species)', 'cf. (genus)']) 
        self._taxon_cf_list.currentIndexChanged.connect(self._update_species_cf_flag)
        # Sizeclass.
        self._speciessizeclass_list = QtGui.QComboBox(self)
        self._speciessizeclass_list.addItems(['']) 
        self._speciessizeclass_list.currentIndexChanged.connect(self._selected_size_class_changed)
        # Count number.
        self._countedunits_edit = KeyPressQSpinBox(self)
        self._countedunits_edit.setRange(0, 999999999)
        self._countedunits_edit.valueChanged.connect(self._update_counted_value_in_core)
        self._counted_clear_button = KeyPressQPushButton('Clear', self)
        self._counted_add1_button = KeyPressQPushButton('+1', self)
        self._counted_sub1_button = KeyPressQPushButton('-1', self)
        self._counted_add10_button = KeyPressQPushButton('+10', self)
        self._counted_sub10_button = KeyPressQPushButton('-10', self)
        self._counted_add100_button = KeyPressQPushButton('+100', self)
        self._counted_sub100_button = KeyPressQPushButton('-100', self)
        self._counted_clear_button.setMaximumWidth(45)
        self._counted_add1_button.setMaximumWidth(35)
        self._counted_add1_button.setToolTip('Shortcut: Space bar')
        self._counted_sub1_button.setMaximumWidth(35)
        self._counted_sub1_button.setToolTip('Shortcut: Backspace')
        self._counted_add10_button.setMaximumWidth(40)
        self._counted_sub10_button.setMaximumWidth(40)
        self._counted_add100_button.setMaximumWidth(45)
        self._counted_sub100_button.setMaximumWidth(45)
        self._counted_clear_button.clicked.connect(self._counted_clear)
        self._counted_add1_button.clicked.connect(self._add_1)
        self._counted_sub1_button.clicked.connect(self._sub_1)
        self._counted_add10_button.clicked.connect(self._add_10)
        self._counted_sub10_button.clicked.connect(self._sub_10)
        self._counted_add100_button.clicked.connect(self._add_100)
        self._counted_sub100_button.clicked.connect(self._sub_100)
        # Dummy button used to catch key press events.
        self._resumecounting_button = KeyPressQPushButton('Resume counting', self) 
        # Comments.
        self._variable_comment_edit = QtGui.QLineEdit()
        self._variable_comment_edit.textChanged.connect(self._update_sample_row)
         
        # Column 3: Summary.
        self._summarytype_list = KeyPressQComboBox(self)
        self._summarytype_list.addItems(['Counted per taxa/sizes', 
                                         'Counted per taxa', 
                                         'Counted per classes',
                                         ])
        self._summarytype_list.currentIndexChanged.connect(self._update_summary)
         
        self._summary_listview = KeyPressQListWidget(self)
        self._summary_listview.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._summary_listview.setStyleSheet("QListWidget::item:hover{background-color:#cccccc;}")
        self._summary_listview.itemSelectionChanged.connect(self._selected_species_in_summary_changed)
 
        self._mostcountedsorted_checkbox = QtGui.QCheckBox('Sort on most counted')
        self._mostcountedsorted_checkbox.setChecked(False)
        self._mostcountedsorted_checkbox.stateChanged.connect(self._update_summary) 
        self._currentmethodstep_checkbox = QtGui.QCheckBox('Current method step only')
        self._currentmethodstep_checkbox.setChecked(True)
        self._currentmethodstep_checkbox.stateChanged.connect(self._update_summary) 
        self._saveasspecieslist_button = KeyPressQPushButton('Save as counting species list...', self) 
        self._saveasspecieslist_button.clicked.connect(self._save_as_species_list)
        self._deletespecieslists_button = KeyPressQPushButton('Delete counting species lists...', self) 
        self._deletespecieslists_button.clicked.connect(self._delete_species_lists)
 
 
        # Layout widgets.
        vboxspecies = QtGui.QVBoxLayout()
        vboxspecies.addWidget(utils_qt.CenterAlignedQLabel('<b>Species</b>'))
        vboxspecies.addWidget(QtGui.QLabel('Select counting species list:'))
        vboxspecies.addWidget(self._selectspecieslist_list)
        #
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel('Filter, part of name:'))
        hbox.addWidget(self._speciesfilter_edit)
        hbox.addWidget(self._speciesfilterclear_button)
        vboxspecies.addLayout(hbox)
        #
        vboxspecies.addWidget(self._species_tableview)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self._viewsizeclassinfo_checkbox)
        hbox.addWidget(self._deletespecieslists_button)
        hbox.addStretch(5)
        vboxspecies.addLayout(hbox)
        #
        vboxcount = QtGui.QVBoxLayout()
        vboxcount.addWidget(utils_qt.CenterAlignedQLabel('<b>Count</b>'))
        #
        vboxsummary = QtGui.QVBoxLayout()
        vboxsummary.addWidget(utils_qt.CenterAlignedQLabel('<b>Summary</b>'))
        vboxsummary.addWidget(QtGui.QLabel('Select summary type:'))
        vboxsummary.addWidget(self._summarytype_list)
        vboxsummary.addWidget(self._mostcountedsorted_checkbox)
        vboxsummary.addWidget(self._currentmethodstep_checkbox)
        vboxsummary.addWidget(self._summary_listview)
        vboxsummary.addWidget(self._saveasspecieslist_button)
        # Grid 1. Methods.
        grid_1 = QtGui.QGridLayout()
        gridrow = 0
        space_label = QtGui.QLabel(' ')
        space_label.setMinimumWidth(130)
        grid_1.addWidget(space_label, gridrow, 10, 1, 1) # Add space.
        grid_1.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 7) # Add space.
        gridrow += 1
        grid_1.addWidget(QtGui.QLabel(''), gridrow, 10, 1, 1) # Add space.
        gridrow += 1
        grid_1.addWidget(utils_qt.RightAlignedQLabel('Method step:'), gridrow, 10, 1, 1)
        grid_1.addWidget(self._selectmethodstep_list, gridrow, 11, 1, 3)
        grid_1.addWidget(self._nextmethodstep_button, gridrow, 14, 1, 1)
        gridrow += 1
        grid_1.addWidget(utils_qt.RightAlignedQLabel('Count area type:'), gridrow, 10, 1, 1)
        grid_1.addWidget(self._countareatype_edit, gridrow, 11, 1, 3)
        gridrow += 1
        grid_1.addWidget(utils_qt.RightAlignedQLabel('Count area number:'), gridrow, 10, 1, 1)
        grid_1.addWidget(self._countareanumber_list, gridrow, 11, 1, 1)
        grid_1.addWidget(self._addcountarea_button, gridrow, 12, 1, 1)
        grid_1.addWidget(self._locktaxa_button, gridrow, 13, 1, 1)
        gridrow += 1
        grid_1.addWidget(utils_qt.RightAlignedQLabel('Coefficient:'), gridrow, 10, 1, 1)
        grid_1.addWidget(self._coefficient_edit, gridrow, 11, 1, 2)
        # Grid 2. Species and count. 
        grid_2 = QtGui.QGridLayout()
        gridrow = 0
#         grid_2.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 6) # Add space.
#         gridrow += 1
        grid_2.addWidget(utils_qt.RightAlignedQLabel('Scientific name:'), gridrow, 10, 1, 1)
        grid_2.addWidget(self._selectedspecies_edit, gridrow, 11, 1, 6)
        gridrow += 1
        grid_2.addWidget(utils_qt.RightAlignedQLabel('Full name:'), gridrow, 10, 1, 1)
        grid_2.addWidget(self._speciesfullname_edit, gridrow, 11, 1, 6)
        gridrow += 1
        sp_spp_hbox = QtGui.QHBoxLayout()
        sp_spp_hbox.addWidget(utils_qt.RightAlignedQLabel('Sp./spp.:'))
        sp_spp_hbox.addWidget(self._taxon_sflag_list)
        sp_spp_hbox.addWidget(utils_qt.RightAlignedQLabel('Cf.:'))
        sp_spp_hbox.addWidget(self._taxon_cf_list)
        sp_spp_hbox.addStretch(10)        
        grid_2.addLayout(sp_spp_hbox, gridrow, 11, 1, 3)
        gridrow += 1
        grid_2.addWidget(utils_qt.RightAlignedQLabel('Size class:'), gridrow, 10, 1, 1)
        grid_2.addWidget(self._speciessizeclass_list, gridrow, 11, 1, 1)
        #
        gridrow += 1
        grid_2.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 1) # Add space.
        gridrow += 1
        grid_2.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 1) # Add space.
        gridrow += 1
        grid_2.addWidget(utils_qt.RightAlignedQLabel('# counted:'), gridrow, 10, 1, 1)
        grid_2.addWidget(self._countedunits_edit, gridrow, 11, 1, 1)
        #
        countbuttons_hbox = QtGui.QHBoxLayout()
        countbuttons_hbox.addStretch(10)
        countbuttons_hbox.addWidget(self._counted_sub100_button)
        countbuttons_hbox.addWidget(self._counted_sub10_button)
        countbuttons_hbox.addWidget(self._counted_sub1_button)
        countbuttons_hbox.addWidget(self._counted_add1_button)
        countbuttons_hbox.addWidget(self._counted_add10_button)
        countbuttons_hbox.addWidget(self._counted_add100_button)
        countbuttons_hbox.addWidget(self._counted_clear_button)
        grid_2.addLayout(countbuttons_hbox, gridrow, 12, 1, 5)
        gridrow += 1
        grid_2.addWidget(self._resumecounting_button, gridrow, 11, 1, 6)
         
        gridrow += 1
        grid_2.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 1) # Add space.
        gridrow += 1
        grid_2.addWidget(QtGui.QLabel(''), gridrow, 11, 1, 1) # Add space.
        gridrow += 1
        grid_2.addWidget(utils_qt.RightAlignedQLabel('Comments:'), gridrow, 10, 1, 1)
        grid_2.addWidget(self._variable_comment_edit, gridrow, 11, 1, 6)
        #
        vboxcount.addLayout(grid_1)
        vboxcount.addStretch(3)
        vboxcount.addLayout(grid_2)
        vboxcount.addStretch(6)
        #
        vboxspecies_widget = QtGui.QWidget()
        vboxspecies_widget.setLayout(vboxspecies)
        vboxcount_widget = QtGui.QWidget()
        vboxcount_widget.setLayout(vboxcount)
        vboxsummary_widget = QtGui.QWidget()
        vboxsummary_widget.setLayout(vboxsummary)
        #
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(vboxspecies_widget)
        splitter.addWidget(vboxcount_widget)
        splitter.addWidget(vboxsummary_widget)  
        #
        splitter.setStretchFactor(0, 100)
        splitter.setStretchFactor(1, 40)
        splitter.setStretchFactor(2, 40)
        #
        layout = QtGui.QHBoxLayout()
        layout.addWidget(splitter)
        #
        return layout
     
    #===== Methods connected to widgets. ===== # TODO:

    def _species_filter_clear(self):
        """ """
        self._speciesfilter_edit.clear()
    
    def _selected_species_list_changed(self):
        """ """
        selectedlist = unicode(self._selectspecieslist_list.currentText())
        self._update_selected_specieslist(selectedlist)
    
    def _update_selected_specieslist(self, selected_list):
        """ """
        self._species_tableview.getTableModel().clear()
        self._species_tableview.resetModel()
        #
        if self._viewsizeclassinfo_checkbox.isChecked():
            tablemodel = self._species_tableview.getTableModel()
            tablemodel.set_header(['Scientific name                 ', 'Size class', 'Cells', 'Trophic type', 'Size info'])
            #
            if selected_list is not None:
                header, rows = plankton_core.PlanktonCounterMethods().get_counting_species_table(selected_list)
                for row in rows:
                    if (len(row) > 0) and (len(row[0]) > 0):
                        scientific_name = row[0]
                        # Reduce number of sizeclasses.
                        usedsizeclasses = None
                        if (len(row) > 1) and (len(row[1]) > 0):
                            usedsizeclasses = map(string.strip, row[1].split(','))
                        #
                        taxon_dict = plankton_core.Species().get_taxon_dict(scientific_name)
                        sizeclasses_list = taxon_dict.get('size_classes', [])
                        if len(sizeclasses_list) > 0:
                            for sizeclass_dict in sizeclasses_list:
                                size = sizeclass_dict.get('bvol_size_class', '')
                                if (usedsizeclasses is not None) and (size not in usedsizeclasses):
                                    continue
                                #
                                trophictype = sizeclass_dict.get('bvol_trophic_type', '')
                                cellsperunit = sizeclass_dict.get('bvol_cells_per_counting_unit', '')
#                                 volume = sizeclass_dict.get('bvol_calculated_volume_um3', '')
#                                 carbon = sizeclass_dict.get('bvol_calculated_carbon_pg', '')
                                sizeinfo = self.generate_size_info_from_dict(sizeclass_dict)
                                #
                                tablemodel.append_row([scientific_name, size, cellsperunit, trophictype, sizeinfo])
                        else:
                                tablemodel.append_row([scientific_name, '', '', '', ''])
        else:
            tablemodel = self._species_tableview.getTableModel()
            tablemodel.set_header(['Scientific name                 ', 'Trophic type'])
            #
            if selected_list is not None:
                try:
                    header, rows = plankton_core.PlanktonCounterMethods().get_counting_species_table(selected_list)
                    for row in rows:
                        if (len(row) >= 1) and (len(row[0]) > 0):
                            scientific_name = row[0]
                            #
                            taxon_dict = plankton_core.Species().get_taxon_dict(scientific_name)
                            trophictype = taxon_dict.get('bvol_trophic_type', '')
                            #
                            tablemodel.append_row([scientific_name, trophictype])
                except:
                    pass
        #
        self._species_tableview.resetModel()
        self._species_tableview.resizeColumnsToContents()
        
    def generate_size_info_from_dict(self, sizeclass_dict):
        """ """
        sizeinfolist = []
        keylist = ['bvol_size_range', 'bvol_length_1_um', 'bvol_length_2_um', 'bvol_width_um', 
                   'bvol_height_um', 'bvol_diameter_1_um', 'bvol_diameter_2_um']
        outkeylist = ['Range', 'L1', 'L2', 'bvol_width_um', 
                      'H', 'D1', 'D2']
        for index, key in enumerate(keylist):
            if key in sizeclass_dict and sizeclass_dict[key]:
                sizeinfolist.append(outkeylist[index]+ ': ' + sizeclass_dict[key])
        #
        return ', '.join(sizeinfolist)

    def _selected_species_in_table_changed(self):
        """ """
        # Clear.
        self._selectedspecies_edit.setText('')
#         self._speciesfullname_edit.setText('')
        #
        scientific_name = ''
        self._speciessizeclass_list.setCurrentIndex(0)
        self._taxon_sflag_list.setCurrentIndex(0)
        self._taxon_cf_list.setCurrentIndex(0)
        # Get selected rows as indexes. Convert to base model if proxy model is used.
        proxyindexes = self._species_tableview.selectedIndexes()
        if len(proxyindexes) > 0:
            proxyindex = proxyindexes[0]
            index = self._species_tableview.model().mapToSource(proxyindex)
            # Info from species table.
            species_index = self._species_tableview._tablemodel.createIndex(index.row(), 0)
            sizeclass_index = self._species_tableview._tablemodel.createIndex(index.row(), 1)
#             sflag_index = self._species_tableview._tablemodel.createIndex(index.row(), 2)
            scientific_name = unicode(self._species_tableview._tablemodel.data(species_index).toString())
            size_class = unicode(self._species_tableview._tablemodel.data(sizeclass_index).toString())
#             species_flag = unicode(self._species_tableview._tablemodel.data(sflag_index).toString())
            #
            # Update name and size in pair.
            try:
                self._dont_get_sample_row_flag = True
                #
                self._selectedspecies_edit.setText(scientific_name)
                # Species sizeclass list.
                currentindex = self._speciessizeclass_list.findText(size_class, QtCore.Qt.MatchFixedString)
                if currentindex >= 0:
                    self._speciessizeclass_list.setCurrentIndex(currentindex)
            finally:
                self._dont_get_sample_row_flag = False
                self._get_sample_row()            

    def _select_method_step_changed(self):
        """ """
        if not self._current_sample_method:
            return
         
        selectedmethodstep = unicode(self._selectmethodstep_list.currentText())
        self._current_sample_method_step_fields = self._current_sample_method.get_counting_method_step_fields(selectedmethodstep)
        #
        self.update_method_step(selectedmethodstep)
        #
        self._counting_species_list = self._current_sample_method_step_fields.get('counting_species_list', '')
        self._view_sizeclass_info = self._current_sample_method_step_fields.get('view_sizeclass_info', '')
        # View sizeclasses.
        combostate = self._current_sample_method_step_fields.get('view_sizeclass_info', 'FALSE')
        if combostate.upper() == 'TRUE':
            self._viewsizeclassinfo_checkbox.setChecked(True)
        else:
            self._viewsizeclassinfo_checkbox.setChecked(False)        
        # Species list. 
        if self._counting_species_list:
            currentindex = self._selectspecieslist_list.findText(self._counting_species_list, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._selectspecieslist_list.setCurrentIndex(currentindex)
        # Clear fields.
        self._selectedspecies_edit.setText('')
        #
        countareatype = self._current_sample_method_step_fields.get('count_area_type', '')
        self._countareatype_edit.setText(countareatype)
        # Alternatives: 'Chamber','1/2 chamber','Field of views','Transects','Rectangles'
        if (countareatype == 'Field of views') or (countareatype == 'Transects') or (countareatype == 'Filters'):
            self._countareanumber_list.setEnabled(True)
            self._addcountarea_button.setEnabled(True)
            self._locktaxa_button.setEnabled(True)
        else:
            self._countareanumber_list.setEnabled(False)
            self._addcountarea_button.setEnabled(False)
            self._locktaxa_button.setEnabled(False)
        #
        self._calculate_coefficient()
        #
        self._update_summary()
         
    def _next_method_step(self):
        """ """
        currentindex = self._selectmethodstep_list.currentIndex()
        listlength = self._selectmethodstep_list.count()
        if (currentindex + 1) < listlength: 
            self._selectmethodstep_list.setCurrentIndex(currentindex + 1)
        else:
            QtGui.QMessageBox.information(self, "Information", 
                                          "No more method steps are available.")
        # Update last used method step.
        self.save_data()
    
    def _add_count_area(self):
        """ """
        numberofcountareas = self._countareanumber_list.count()
        self._countareanumber_list.clear()
        for index in range(numberofcountareas + 1):
            countarea = index + 1
            self._countareanumber_list.addItem(unicode(countarea))
        #
        self._countareanumber_list.setCurrentIndex(numberofcountareas)
        #
        self._calculate_coefficient()
        # Update coefficient for all taxa in this method step.
        currentmethodstep = unicode(self._selectmethodstep_list.currentText())
        coefficient = unicode(self._coefficient_edit.text())
        countareanumber = unicode(self._countareanumber_list.currentText())
        self._current_sample_object.update_coeff_for_sample_rows(currentmethodstep, 
                                                                 countareanumber, 
                                                                 coefficient)
        # Save max count area for method step.
        self.save_data()
         
    def _lock_taxa(self):
        """ """   
        currentmethodstep = unicode(self._selectmethodstep_list.currentText())
        countareanumber = unicode(self._countareanumber_list.currentText())
        dialog = LockTaxaListDialog(self, self._current_sample_object, currentmethodstep, countareanumber)
        dialog.exec_()
        # Update sample row since rows have been locked. 
        self._get_sample_row()
        
    def _selected_species_changed(self, new):
        """ """
        scientific_name = unicode(self._selectedspecies_edit.text())
        # Get alternatives for size classes.
        taxon_dict = plankton_core.Species().get_taxon_dict(scientific_name)
        sizes = []
        for sizeclass in taxon_dict.get('size_classes', {}):
            size = sizeclass.get('bvol_size_class', '')
            if size:
                sizes.append(size)
        self._speciessizeclass_list.clear()
        self._speciessizeclass_list.addItems([''] + sizes)
        
    def _selected_size_class_changed(self, new):
        """ """
#         print('DEBUG _selected_size_class_changed.')

        self._get_sample_row()
        
    def _get_sample_row(self):
        """ """
        if self._dont_get_sample_row_flag == True:
            return 
        #
        scientific_name = unicode(self._selectedspecies_edit.text())
        size_class = unicode(self._speciessizeclass_list.currentText())
        
#         print('DEBUG _get_sample_row: ' + scientific_name + ' : ' + size_class)
         
        # Clear fields with no updates.
        try:
            self._dont_update_flag = True
            self._taxon_sflag_list.setCurrentIndex(0)
            self._taxon_cf_list.setCurrentIndex(0)
            self._speciesfullname_edit.setText(scientific_name)
        finally:
            self._dont_update_flag = False
        
        # Don't ask if empty.
        if scientific_name == '':
            return
        # Get data from core.
        sample_row_dict = {}
        info_dict = {}
        info_dict['scientific_name'] = scientific_name
        info_dict['size_class'] = size_class
        sample_row_dict = self._current_sample_object.get_sample_row_dict(info_dict)
        # counted_units

#         print('DEBUG: _countedunits_edit:' + sample_row_dict.get('counted_units', '0'))
        
        self._countedunits_edit.setValue(int(sample_row_dict.get('counted_units', '0')))
        # Species flag (sflag).
        species_flag = unicode(sample_row_dict.get('species_flag', ''))
        if species_flag:
            currentindex = self._taxon_sflag_list.findText(species_flag, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._taxon_sflag_list.setCurrentIndex(currentindex)
        # Cf.
        cf = unicode(sample_row_dict.get('cf', ''))
        if cf:
            currentindex = self._taxon_cf_list.findText(cf, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._taxon_cf_list.setCurrentIndex(currentindex)
        # Comments.
        self._variable_comment_edit.setText(sample_row_dict.get('variable_comment', ''))
        #
        # Disable counting for taxa/sizes counted in another method step.
        currentmethodstep = unicode(self._selectmethodstep_list.currentText())
        storedmethodstep = sample_row_dict.get('method_step', currentmethodstep)
        lockedatarea = sample_row_dict.get('locked_at_area', '')
        #
#         print('DEBUG: currentmethodstep:' + currentmethodstep)
#         print('DEBUG: storedmethodstep: ' + sample_row_dict.get('method_step', '???'))
#         print('DEBUG: lockedatarea:' + lockedatarea)
#         print('DEBUG: sample_row_dict:' + unicode(sample_row_dict))
        #
        if (storedmethodstep == currentmethodstep) and (lockedatarea == ''):
            self._countedunits_edit.setEnabled(True)
            self._resumecounting_button.setEnabled(True)
            self._counted_add1_button.setEnabled(True)
            self._counted_sub1_button.setEnabled(True)
            self._counted_add10_button.setEnabled(True)
            self._counted_sub10_button.setEnabled(True)
            self._counted_add100_button.setEnabled(True)
            self._counted_sub100_button.setEnabled(True)
        else:
            self._countedunits_edit.setEnabled(False)  
            self._resumecounting_button.setEnabled(False)
            self._counted_add1_button.setEnabled(False)
            self._counted_sub1_button.setEnabled(False)
            self._counted_add10_button.setEnabled(False)
            self._counted_sub10_button.setEnabled(False)
            self._counted_add100_button.setEnabled(False)
            self._counted_sub100_button.setEnabled(False)
         
    def _update_scientific_full_name(self):
        """ """
        if self._dont_update_flag == True:
            return
        #
        scientific_name = unicode(self._selectedspecies_edit.text())
        size_class = unicode(self._speciessizeclass_list.currentText())

#         print('DEBUG _update_scientific_full_name: ' + scientific_name + ' : ' + size_class)

        if scientific_name == '':
            return
        #
        cf = unicode(self._taxon_cf_list.currentText())
        sflag = unicode(self._taxon_sflag_list.currentText())
        #
        scientificfullname = scientific_name
        #
        if cf == 'cf. (species)':
            scientificnameparts = scientific_name.split(' ')
            if len(scientificnameparts) >= 2:
                scientificfullname = scientificnameparts[0] + ' cf. ' + scientificnameparts[1]
        elif cf == 'cf. (genus)':
            scientificfullname = 'cf. ' + scientific_name
        #
        if sflag:
            scientificfullname = scientificfullname + ' ' + sflag
        #
        self._speciesfullname_edit.setText(scientificfullname)
        # 
        sample_row_dict = {}
        sample_row_dict['scientific_name'] = scientific_name
        sample_row_dict['size_class'] = size_class
        sample_row_dict['scientific_full_name'] = scientificfullname
        self._current_sample_object.update_sample_row(sample_row_dict)
             
    def _update_species_flag(self):
        """ """
        if self._dont_update_flag == True:
            return
        #
        scientific_name = unicode(self._selectedspecies_edit.text())
        size_class = unicode(self._speciessizeclass_list.currentText())

#         print('DEBUG _update_species_flag: ' + scientific_name + ' : ' + size_class)

        if scientific_name == '':
            return
        #
        self._update_scientific_full_name()
        #
        sample_row_dict = {}
        sample_row_dict['scientific_name'] = scientific_name
        sample_row_dict['size_class'] = size_class
        sflag = unicode(self._taxon_sflag_list.currentText()) 
        sample_row_dict['species_flag'] = sflag
        self._current_sample_object.update_sample_row(sample_row_dict)
        
    def _update_species_cf_flag(self):
        """ """
        if self._dont_update_flag == True:
            return
        #
        scientific_name = unicode(self._selectedspecies_edit.text())
        size_class = unicode(self._speciessizeclass_list.currentText())

#         print('DEBUG _update_species_cf_flag: ' + scientific_name + ' : ' + size_class)

        if scientific_name == '':
            return
        #
        self._update_scientific_full_name()
        #
        sample_row_dict = {}
        sample_row_dict['scientific_name'] = scientific_name
        sample_row_dict['size_class'] = size_class
        cf = unicode(self._taxon_cf_list.currentText())
        sample_row_dict['cf'] = cf
        self._current_sample_object.update_sample_row(sample_row_dict)
        
    def _update_sample_row(self):
        """ """
        if self._dont_update_flag == True:
            return
        #
        scientific_name = unicode(self._selectedspecies_edit.text())
        size_class = unicode(self._speciessizeclass_list.currentText())

#         print('DEBUG _update_sample_row: ' + scientific_name + ' : ' + size_class)

        if scientific_name == '':
            return
        #
        sample_row_dict = {}
        sample_row_dict['scientific_name'] = scientific_name
        sample_row_dict['size_class'] = size_class
        #
        scientificfullname = unicode(self._speciesfullname_edit.text())
        cf = unicode(self._taxon_cf_list.currentText())
        sflag = unicode(self._taxon_sflag_list.currentText()) 
        sample_row_dict['scientific_full_name'] = scientificfullname
        sample_row_dict['cf'] = cf
        sample_row_dict['species_flag'] = sflag
        #
        sample_row_dict['variable_comment'] = unicode(self._variable_comment_edit.text())
        #
        self._current_sample_object.update_sample_row(sample_row_dict)
         
    def _update_counted_value_in_core(self, value):
        """ """
        info_dict = self._current_sample_method_step_fields
        # From fields in this tab widget.
        info_dict['scientific_name'] = unicode(self._selectedspecies_edit.text())
        info_dict['size_class'] = unicode(self._speciessizeclass_list.currentText())
        info_dict['method_step'] = unicode(self._selectmethodstep_list.currentText())
        info_dict['count_area_number'] = unicode(self._countareanumber_list.currentText())
        info_dict['coefficient'] = unicode(self._coefficient_edit.text())
        #
        value = unicode(self._countedunits_edit.value())
        self._current_sample_object.update_counted_value_in_core(info_dict, value)
        #
        self._update_summary()
         
    def _counted_clear(self, value):
        """ """
        self._countedunits_edit.setValue(0)
        #
        self._get_sample_row()
         
    def _counted_add(self, value):
        """ """
        if self._countedunits_edit.isEnabled():
            oldvalue = self._countedunits_edit.value()
            newvalue = oldvalue + value
            self._countedunits_edit.setValue(newvalue)
         
    def _add_1(self): self._counted_add(1)
    def _sub_1(self): self._counted_add(-1)
    def _add_10(self): self._counted_add(10)
    def _sub_10(self): self._counted_add(-10)
    def _add_100(self): self._counted_add(100)
    def _sub_100(self): self._counted_add(-100)
 
    def _update_summary(self):
        """ """
        summarytype = 'Counted taxa'
        if self._summarytype_list.currentText() == 'Counted per taxa':
            summarytype = 'Counted species report'
        elif self._summarytype_list.currentText() == 'Counted per taxa/sizes':
            summarytype = 'Counted taxa/sizes report'
        elif self._summarytype_list.currentText() == 'Counted per classes':
            summarytype = 'Counted per class report'
        mostcountedsorting = False
        if self._mostcountedsorted_checkbox.isChecked():
            mostcountedsorting = True
        method_step = None
        if self._currentmethodstep_checkbox.isChecked():
            method_step = unicode(self._selectmethodstep_list.currentText())
        # 
        summary_data = self._current_sample_object.get_taxa_summary(summary_type = summarytype,
                                                                    most_counted_sorting = mostcountedsorting,
                                                                    method_step = method_step)
        # Update summary list.
        self._summary_listview.clear()
        self._summary_listview.addItems(summary_data)
 
    def _selected_species_in_summary_changed(self):
        """ """
        # Clear.
        self._selectedspecies_edit.setText('')
#         self._speciesfullname_edit.setText('')
        # Clear the other species list.
        self._species_tableview.clearSelection()
        # Get name and size. 
        size_class = ''
        if not self._summary_listview.currentItem():
            return
        speciesandsizeclass = unicode(self._summary_listview.currentItem().text())
        parts = speciesandsizeclass.split(':')
        parts = parts[0].split('[')
        scientific_name = parts[0].strip()
        if len(parts) > 1:
            size_class = parts[1].strip().strip(']')
        # Update name and size in pair.
        try:
            self._dont_get_sample_row_flag = True
            #
            self._selectedspecies_edit.setText(scientific_name)
            # Species sizeclass list.
            currentindex = self._speciessizeclass_list.findText(size_class, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._speciessizeclass_list.setCurrentIndex(currentindex)
        finally:
            self._dont_get_sample_row_flag = False
            self._get_sample_row()            

    def _save_as_species_list(self):
        """ """
        dialog = SaveAsCountingSpeciesListDialog(self)
        if dialog.exec_():
            specieslistname = dialog.get_new_name()
            if specieslistname:
                currentmethodstep = None
                if self._currentmethodstep_checkbox.isChecked():
                    currentmethodstep = unicode(self._selectmethodstep_list.currentText())
                #
                species_list_rows = self._current_sample_object.get_taxa_summary(summary_type = 'Counted taxa',
                                                                                 most_counted_sorting = False,
                                                                                 method_step = currentmethodstep)
                #
                rows = []
                for row in species_list_rows:
                    if len(row) > 0:
                        rows.append([row])
                #   
                plankton_core.PlanktonCounterMethods().create_counting_species_list(specieslistname,
                                                                                rows)
        #
        self._update_select_specieslist_combo()             
        self._update_selected_specieslist(None) 
             
    def _delete_species_lists(self):
        """ """
        dialog = DeleteCountingSpeciesListDialog(self)
        if dialog.exec_():
            self._update_select_specieslist_combo()             
            self._update_selected_specieslist(None) 
        #
        self._update_select_specieslist_combo()             
        self._update_selected_specieslist(None)
        
         

    #===== Local methods. ===== # TODO:

    def _load_counting_method(self):
        """ """
        self._selectmethodstep_list.clear()
        #
        sample_path = self._current_sample_object.get_dir_path()
        if os.path.exists(os.path.join(sample_path, 'counting_method.txt')):
            header, rows = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                                                sample_path, 'counting_method.txt')        
            self._current_sample_method = plankton_core.PlanktonCounterMethod(header, rows)
            #
            countingmethodsteps = self._current_sample_method.get_counting_method_steps_list()
            if len(countingmethodsteps) > 0:
                self._selectmethodstep_list.addItems(countingmethodsteps)
                self._selectmethodstep_list.setCurrentIndex(0)
            else:
                self._selectmethodstep_list.addItems(['<not available>'])
        else:
            self._selectmethodstep_list.addItems(['<not available>'])
  
    def update_method_step(self, selected_method_step):
        """ """
        if self._selectmethodstep_list and selected_method_step:
            currentindex = self._selectmethodstep_list.findText(selected_method_step, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._selectmethodstep_list.setCurrentIndex(currentindex)
        #
        sample_info_dict = self._current_sample_object.get_sample_info()
        maxcountarea = sample_info_dict.get('max_count_area<+>' + selected_method_step, '1')
        maxareanumber = int(maxcountarea)
        self._countareanumber_list.clear()
        for index in range(maxareanumber):
            countarea = index + 1
            self._countareanumber_list.addItem(unicode(countarea))
        self._countareanumber_list.setCurrentIndex(maxareanumber - 1)
        #
        self._calculate_coefficient()
        # Update sample row since counting method step changed. 
        self._get_sample_row()

    def _update_select_specieslist_combo(self):
        """ """
        self._selectspecieslist_list.clear()
        specieslists = plankton_core.PlanktonCounterMethods().get_counting_species_lists()
        self._selectspecieslist_list.addItems(['<select>'] + specieslists)
 
    def _calculate_coefficient(self):
        """ """
        # Coefficient.
        valuetxt = unicode(self._countareanumber_list.currentText())
        value = int(valuetxt)
        method_dict = self._current_sample_method_step_fields
        coeffoneunittext = method_dict.get('coefficient_one_unit', '0')
        try:
            coeffoneunit = float(coeffoneunittext)
            coeff = int((coeffoneunit / value) + 0.5)
            self._coefficient_edit.setText(unicode(coeff))
        except:
            self._coefficient_edit.setText('0')
 
    # ===== For key press events. ===== # TODO:
 
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(PlanktonCounterSampleCount, self).keyPressEvent(qKeyEvent)
 
    def handle_key_press_event(self, qKeyEvent):
        """ """
        if qKeyEvent.key() == QtCore.Qt.Key_Space: 
            self._counted_add(1)  
            return True
        elif qKeyEvent.key() == QtCore.Qt.Key_Backspace: 
            self._counted_add(-1)
            return True
        elif qKeyEvent.key() == QtCore.Qt.Key_Escape: 
#             print('Key_Escape...')
            self._parentwidget.close()  
            return True
        #
        return False
 
 
# === Subclasses of Qt widgets. ===
 
class KeyPressQWidget(QtGui.QWidget):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQWidget, self).__init__()
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQWidget, self).keyPressEvent(qKeyEvent)
 
 
class KeyPressQComboBox(QtGui.QComboBox):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQComboBox, self).__init__()
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQComboBox, self).keyPressEvent(qKeyEvent)
 
 
class KeyPressQListView(QtGui.QListView):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQListView, self).__init__()
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQListView, self).keyPressEvent(qKeyEvent)
 
  
class KeyPressQListWidget(QtGui.QListWidget):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQListWidget, self).__init__()
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQListWidget, self).keyPressEvent(qKeyEvent)
 
  
class KeyPressQLineEdit(QtGui.QLineEdit):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQLineEdit, self).__init__()
         
class KeyPressQPushButton(QtGui.QPushButton):
    """ """
    def __init__(self, name, parent):
        """ """
        self._parent = parent
        super(KeyPressQPushButton, self).__init__(name)
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQPushButton, self).keyPressEvent(qKeyEvent)
 
   
class KeyPressToolboxQTableView(utils_qt.ToolboxQTableView):
    """ """
    def __init__(self, parent, filter_column_index = 0):
        """ """
        self._parent = parent
        super(KeyPressToolboxQTableView, self).__init__(parent, filter_column_index)
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressToolboxQTableView, self).keyPressEvent(qKeyEvent)
 
 
class KeyPressQSpinBox(QtGui.QSpinBox):
    """ """
    def __init__(self, parent):
        """ """
        self._parent = parent
        super(KeyPressQSpinBox, self).__init__(parent)
         
    def keyPressEvent(self, qKeyEvent):
        """ """
        result = self._parent.handle_key_press_event(qKeyEvent)
        if result == True:
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(KeyPressQSpinBox, self).keyPressEvent(qKeyEvent)
 
 
class SaveAsCountingSpeciesListDialog(QtGui.QDialog):
    """ """
    def __init__(self, parentwidget):
        """ """
        self._new_name = ''
        super(SaveAsCountingSpeciesListDialog, self).__init__(parentwidget)
        self.setWindowTitle("Save species list as")
        self.setLayout(self._content())
 
    def get_new_name(self):
        """ """
        return self._new_name
 
    def _content(self):
        """ """
        self._new_name_edit = QtGui.QLineEdit('')
        self._new_name_edit.setMinimumWidth(400)
        save_button = QtGui.QPushButton('Save')
        save_button.clicked.connect(self._save)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
        formlayout.addRow('Counting specis list name:', self._new_name_edit)
         
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
 
 
class DeleteCountingSpeciesListDialog(QtGui.QDialog):
    """  """
    def __init__(self, parentwidget):
        """ """
        self._parentwidget = parentwidget
        super(DeleteCountingSpeciesListDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete counting specis list type(s)")
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()
 
    def _content(self):
        """ """  
        counting_species_listview = QtGui.QListView()
        self._counting_species_model = QtGui.QStandardItemModel()
        counting_species_listview.setModel(self._counting_species_model)
 
        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_rows)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_rows)                
        delete_button = QtGui.QPushButton('Delete marked counting specis list(s)')
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
        layout.addWidget(counting_species_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        #
        return layout                
 
    def _load_data(self):
        """ """
        countingspecieslists = plankton_core.PlanktonCounterMethods().get_counting_species_lists()
 
        self._counting_species_model.clear()        
        for countingspecieslist in countingspecieslists:
            item = QtGui.QStandardItem(countingspecieslist)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._counting_species_model.appendRow(item)
             
    def _check_all_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
             
    def _uncheck_all_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
 
    def _delete_marked_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedname = unicode(item.text())
                plankton_core.PlanktonCounterMethods().delete_counting_species_list(selectedname)
        #            
        self.accept() # Close dialog box.
 
 
class LockTaxaListDialog(QtGui.QDialog):
    """  """
    def __init__(self, parentwidget, current_sample_object, current_method_step, count_area):
        """ """
        self._parentwidget = parentwidget
        self._current_sample_object = current_sample_object
        self._current_method_step = current_method_step
        self._count_area = count_area
        super(LockTaxaListDialog, self).__init__(parentwidget)
        self.setWindowTitle("Lock/unlock taxa")
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()
 
    def _content(self):
        """ """  
        counting_species_listview = QtGui.QListView()
        self._counting_species_model = QtGui.QStandardItemModel()
        counting_species_listview.setModel(self._counting_species_model)
 
        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_rows)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_rows)                
        delete_button = QtGui.QPushButton('Lock marked taxa')
        delete_button.clicked.connect(self._execute_marked_rows)               
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
        layout.addWidget(counting_species_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        #
        return layout                
 
    def _load_data(self):
        """ """
        species_list_rows = self._current_sample_object.get_taxa_summary(summary_type = 'Counted taxa/sizes',
                                                                         most_counted_sorting = False,
                                                                         method_step = self._current_method_step)
        #
        self._counting_species_model.clear()        
        for species_list_row in species_list_rows:
            item = QtGui.QStandardItem(species_list_row)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._counting_species_model.appendRow(item)
             
    def _check_all_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
             
    def _uncheck_all_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
 
    def _execute_marked_rows(self):
        """ """
        for rowindex in range(self._counting_species_model.rowCount()):
            item = self._counting_species_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                selectedrow = unicode(item.text())
                #
                scientific_name = ''
                size_class = ''
                parts = selectedrow.split(':')
                parts = parts[0].split('[')
                scientific_name = parts[0].strip()
                if len(parts) > 1:
                    size_class = parts[1].strip().strip(']')
                #
                self._current_sample_object.lock_taxa(scientific_name, size_class, self._count_area)
        #            
        self.accept() # Close dialog box.

