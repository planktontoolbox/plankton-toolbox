#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework

class AnalyseDatasetsTab3(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab3, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        try:
            self._main_activity = main_activity
            self._analysisdata = main_activity.get_analysis_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def clear(self):
        """ """
        try:
            self._trophic_type_listview.clear()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def update(self):
        """ """
        try:
            self.clear()        
            self._update_select_data_alternatives()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    # ===== TAB: Aggregate data ===== 
    def content_aggregate_data(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab3_intro'))
        # Active widgets and connections.
        # Aggregate over taxonomic rank.
        self._aggregate_rank_list = QtWidgets.QComboBox()
        self._aggregate_rank_list.addItems([
            'Biota (all levels)',
            'Plankton group',
            'Kingdom',
            'Phylum',
            'Class',
            'Order',
            'Family',
            'Genus',
            'Species',
            'Scientific name', 
            'Kingdom (from dataset)',
            'Phylum (from dataset)',
            'Class (from dataset)',
            'Order (from dataset)',
            'Family (from dataset)',
            'Genus (from dataset)',
            'Species (from dataset)', 
            ])
        self._aggregate_rank_list.setCurrentIndex(4) # Default: Class.
        #  Aggregate over trophic_type.
        self._trophic_type_listview = app_framework.SelectableQListView()
#         self._trophic_type_listview.setMaximumHeight(80)
        #  Aggregate over life stage.
        self._lifestage_listview = app_framework.SelectableQListView()
#         self._lifestage_listview.setMaximumHeight(80)
        # Buttons.
        self._aggregatedata_button = QtWidgets.QPushButton('Aggregate data')
        self._aggregatedata_button.clicked.connect(self._aggregate_data)
        #
        self._reloaddata_button = QtWidgets.QPushButton('Reload analysis data (no clean up)')
        self._reloaddata_button.clicked.connect(self._main_activity._tab1widget._copy_datasets_for_analysis)
        #               
        self._addmissingtaxa_button = QtWidgets.QPushButton('Add 0 for not observed')
        self._addmissingtaxa_button.clicked.connect(self._add_missing_taxa)
        
        
        
        self._addmissingtaxa_trophictype_checkbox = QtWidgets.QCheckBox('Include trophic types')
        self._addmissingtaxa_trophictype_checkbox.setChecked(False)
        self._addmissingtaxa_stagesex_checkbox = QtWidgets.QCheckBox('Include development stage/sex')
        self._addmissingtaxa_stagesex_checkbox.setChecked(False)
        
        
        
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Aggregate over:')
        form1.addWidget(label1, gridrow, 0, 1, 4)
        label2 = QtWidgets.QLabel('Complement data:')
        form1.addWidget(label2, gridrow, 9, 1, 4)
        gridrow += 1
        label1 = QtWidgets.QLabel('Taxon level (rank):               ')
        label2 = QtWidgets.QLabel('Trophic type:')
        label3 = QtWidgets.QLabel('Life stage:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(label3, gridrow, 4, 1, 3)
        form1.addWidget(QtWidgets.QLabel(''), gridrow, 3, 1, 6) # Stretch.
        gridrow += 1
        form1.addWidget(self._aggregate_rank_list, gridrow, 0, 1, 1)
        form1.addWidget(self._trophic_type_listview, gridrow, 1, 4, 3)
        form1.addWidget(self._lifestage_listview, gridrow, 4, 4, 3)
        form1.addWidget(self._addmissingtaxa_button, gridrow, 9, 1, 1)
        gridrow += 1
        form1.addWidget(self._addmissingtaxa_trophictype_checkbox, gridrow, 9, 1, 1)
        gridrow += 1
        form1.addWidget(self._addmissingtaxa_stagesex_checkbox, gridrow, 9, 1, 1)
        gridrow += 3
        form1.addWidget(self._reloaddata_button, gridrow, 0, 1, 1)
        form1.addWidget(self._aggregatedata_button, gridrow, 1, 1, 1)
        #
#        hbox1 = QtWidgets.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self._aggregatedata_button)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
#         layout.addStretch(5)
#        layout.addLayout(hbox1)
        self.setLayout(layout)                
        #
        return self

    def _aggregate_data(self):
        """ """
        try:
            try:
    #             if self._aggregate_rank_list.currentIndex() == 0:
    #                 toolbox_utils.Logging().log('Taxon level is not selected. Please try again.')
    #                 raise UserWarning('Taxon level is not selected. Please try again.')
                if not self._analysisdata.get_data():
                    toolbox_utils.Logging().log('No data is loaded for analysis. Please try again.')
                    raise UserWarning('No data is loaded for analysis. Please try again.')                
                #
                toolbox_utils.Logging().log('Aggregating data...')
                toolbox_utils.Logging().start_accumulated_logging()
                try:
                #
                    selected_taxon_rank = str(self._aggregate_rank_list.currentText())
                    selected_trophic_type_list = self._trophic_type_listview.getSelectedDataList()
                    selected_trophic_type_text = '-'.join(selected_trophic_type_list) 
                    selected_lifestage_list = self._lifestage_listview.getSelectedDataList()
                    selected_lifestage_text = '-'.join(selected_lifestage_list) 
                    #
                    for visitnode in self._analysisdata.get_data().get_children()[:]: 
                        for samplenode in visitnode.get_children()[:]:
                            aggregatedvariables = {}
                            trophic_type_set_dict = {} ### TEST
                            for variablenode in samplenode.get_children()[:]:
                                newtaxon = None
                                value = variablenode.get_data('value')
                                try:
                                    value = value.replace(',', '.').replace(' ', '') # Try/except if already float.
                                except: 
                                    pass
                                # Use values containing valid float data.
                                try:
                                    value = float(value) 
                                    #
                                    if selected_taxon_rank == 'Biota (all levels)':
                                        newtaxon = 'Biota' # Biota is above kingdom in the taxonomic hierarchy.
                                    elif selected_taxon_rank == 'Plankton group':
                                        newtaxon = plankton_core.Species().get_plankton_group_from_taxon_name(variablenode.get_data('scientific_name'))
                                    elif selected_taxon_rank == 'Kingdom':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_kingdom')
                                    elif selected_taxon_rank == 'Phylum':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_phylum')
                                    elif selected_taxon_rank == 'Class':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_class')
                                    elif selected_taxon_rank == 'Order':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_order')
                                    elif selected_taxon_rank == 'Family':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_family')
                                    elif selected_taxon_rank == 'Genus':
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_genus')
                                    elif selected_taxon_rank == 'Species': 
                                        newtaxon = plankton_core.Species().get_taxon_value(variablenode.get_data('scientific_name'), 'taxon_species')
                                    elif selected_taxon_rank == 'Scientific name': 
                                        newtaxon = variablenode.get_data('scientific_name')
                                    elif selected_taxon_rank == 'Kingdom (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_kingdom')
                                    elif selected_taxon_rank == 'Phylum (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_phylum')
                                    elif selected_taxon_rank == 'Class (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_class')
                                    elif selected_taxon_rank == 'Order (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_order')
                                    elif selected_taxon_rank == 'Family (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_family')
                                    elif selected_taxon_rank == 'Genus (from dataset)':
                                        newtaxon = variablenode.get_data('taxon_genus')
                                    elif selected_taxon_rank == 'Species (from dataset)': 
                                        newtaxon = variablenode.get_data('taxon_species')
                                    # If not found in classification, then use scientific_name. 
                                    # This is valid for taxon with rank above the selected rank.  
                                    if not newtaxon:
                                        newtaxon = variablenode.get_data('scientific_name')
                                    # 
                                    if not newtaxon:
                                        toolbox_utils.Logging().warning('Not match for selected rank. "not-designated" assigned for: ' + variablenode.get_data('scientific_name'))
                                        newtaxon = 'not-designated' # Use this if empty.
                                    #
                                    taxontrophic_type = variablenode.get_data('trophic_type')
                                    if taxontrophic_type in selected_trophic_type_list:
                                        taxontrophic_type = selected_trophic_type_text # Concatenated string of ranks.
                                        ### TEST
                                        if newtaxon not in trophic_type_set_dict: ### TEST
                                            trophic_type_set_dict[newtaxon] = set() ### TEST
                                        trophic_type_set_dict[newtaxon].add(variablenode.get_data('trophic_type')) ### TEST
                                    else:
                                        continue # Phytoplankton only: Use selected trophic_type only, don't use others.  
                                    #
                                    stage = variablenode.get_data('stage')
                                    sex = variablenode.get_data('sex')
                                    checkstage = stage
                                    if sex:
                                        checkstage += '/' + sex
                                    if checkstage in selected_lifestage_list:
                                        stage = selected_lifestage_text
                                        sex = ''
        #                             else:
        #                                 continue # Note: Don't skip for zooplankton.                 
                                    #
                                    parameter = variablenode.get_data('parameter')
                                    unit = variablenode.get_data('unit')
                                     
                                    agg_tuple = (newtaxon, taxontrophic_type, stage, sex, parameter, unit)
                                    if agg_tuple in aggregatedvariables:
                                        aggregatedvariables[agg_tuple] = value + aggregatedvariables[agg_tuple]
                                    else:
                                        aggregatedvariables[agg_tuple] = value
                                except:
                                    if variablenode.get_data('value'):
                                        toolbox_utils.Logging().warning('Value is not a valid float: ' + str(variablenode.get_data('value')))
                            #Remove all variables for this sample.
                            samplenode.remove_all_children()
                            # Add the new aggregated variables instead.  
                            for variablekeytuple in aggregatedvariables:
                                newtaxon, taxontrophic_type, stage, sex, parameter, unit = variablekeytuple
                                #
                                newvariable = plankton_core.VariableNode()
                                samplenode.add_child(newvariable)    
                                #
                                newvariable.add_data('scientific_name', newtaxon)
                                ### TEST. newvariable.add_data('trophic_type', taxontrophic_type)
                                newvariable.add_data('trophic_type', '-'.join(sorted(trophic_type_set_dict.get(newtaxon, [])))) ### TEST
                                newvariable.add_data('stage', stage)
                                newvariable.add_data('sex', sex)
                                newvariable.add_data('parameter', parameter)
                                newvariable.add_data('unit', unit)
                                newvariable.add_data('value', aggregatedvariables[variablekeytuple])
                                # Add taxon class, etc. based on taxon name.
                                newvariable.add_data('taxon_kingdom', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_kingdom'))
                                newvariable.add_data('taxon_phylum', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_phylum'))
                                newvariable.add_data('taxon_class', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_class'))
                                newvariable.add_data('taxon_order', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_order'))
                                newvariable.add_data('taxon_family', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_family'))
                                newvariable.add_data('taxon_genus', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_genus'))
                                newvariable.add_data('taxon_species', plankton_core.Species().get_taxon_value(newtaxon, 'taxon_species'))
                    #
                    self._main_activity.update_viewed_data_and_tabs()    
                except UserWarning as e:
                    toolbox_utils.Logging().error('Failed to aggregate data. ' + str(e))
                    QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', 'Failed to aggregate data. ' + str(e))
            finally:
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Aggregation of data is done.')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            

    def _update_select_data_alternatives(self):
        """ """
        try:
            analysisdata = self._analysisdata.get_data()
            if not analysisdata:
                return # Empty data.
            #
            trophic_type_set = set()
            lifestageset = set()
            for visitnode in analysisdata.get_children():
                for samplenode in visitnode.get_children():
                    for variablenode in samplenode.get_children():
                        #
                        trophic_type_set.add(str(variablenode.get_data('trophic_type')))
                        #
                        lifestage = variablenode.get_data('stage')
                        if variablenode.get_data('sex'):
                            lifestage += '/' + variablenode.get_data('sex')
                        lifestageset.add(lifestage)
            # Selection lists.
            self._trophic_type_listview.setList(sorted(trophic_type_set))
            self._lifestage_listview.setList(sorted(lifestageset))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _add_missing_taxa(self):
        """ """
        try:
            try:
                toolbox_utils.Logging().log('Adding 0 for not observed...')
                toolbox_utils.Logging().start_accumulated_logging()
                #
                analysisdata = self._analysisdata.get_data()
                if not analysisdata:        
                    return
                #
                
                
                
                include_trophictypes = self._addmissingtaxa_trophictype_checkbox.isChecked()
                include_stagesex = self._addmissingtaxa_stagesex_checkbox.isChecked()
                
                
                
                plankton_core.AnalysisPrepare().add_missing_taxa(analysisdata, include_trophictypes, include_stagesex)
                #
                self._main_activity.update_viewed_data_and_tabs()    
            except UserWarning as e:
                toolbox_utils.Logging().error('Failed to add 0 for not observed. ' + str(e))
                QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', 'Failed to add 0 for not observed. ' + str(e))
            finally:
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Add 0 for not observed is done.')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

