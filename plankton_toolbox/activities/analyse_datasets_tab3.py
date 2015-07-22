#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib
import toolbox_utils
import toolbox_core

class AnalyseDatasetsTab3(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab3, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()

    def clear(self):
        """ """
        self._trophic_type_listview.clear()
        
    def update(self):
        """ """
        self.clear()        
        self._updateSelectDataAlternatives()
        
    # ===== TAB: Aggregate data ===== 
    def contentAggregateData(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab3_intro'))
        # Active widgets and connections.
        # Aggregate over taxonomic rank.
        self._aggregate_rank_list = QtGui.QComboBox()
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
        self._trophic_type_listview = utils_qt.SelectableQListView()
#         self._trophic_type_listview.setMaximumHeight(80)
        #  Aggregate over life stage.
        self._lifestage_listview = utils_qt.SelectableQListView()
#         self._lifestage_listview.setMaximumHeight(80)
        # Buttons.
        self._aggregatedata_button = QtGui.QPushButton('Aggregate data')
        self.connect(self._aggregatedata_button, QtCore.SIGNAL('clicked()'), self._aggregateData)
        #
        self._reloaddata_button = QtGui.QPushButton('Reload analysis data (no clean up)')
        self.connect(self._reloaddata_button, QtCore.SIGNAL('clicked()'), self._main_activity._tab1widget._copyDatasetsForAnalysis)
        #               
        self._addmissingtaxa_button = QtGui.QPushButton('Add 0 for not observed')
        self.connect(self._addmissingtaxa_button, QtCore.SIGNAL('clicked()'), self._addMissingTaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Aggregate over:')
        form1.addWidget(label1, gridrow, 0, 1, 4)
        label2 = QtGui.QLabel('Complement data:')
        form1.addWidget(label2, gridrow, 9, 1, 4)
        gridrow += 1
        label1 = QtGui.QLabel('Taxon level (rank):               ')
        label2 = QtGui.QLabel('Trophic type:')
        label3 = QtGui.QLabel('Life stage:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(label3, gridrow, 4, 1, 3)
        form1.addWidget(QtGui.QLabel(''), gridrow, 3, 1, 6) # Stretch.
        gridrow += 1
        form1.addWidget(self._aggregate_rank_list, gridrow, 0, 1, 1)
        form1.addWidget(self._trophic_type_listview, gridrow, 1, 4, 3)
        form1.addWidget(self._lifestage_listview, gridrow, 4, 4, 3)
        form1.addWidget(self._addmissingtaxa_button, gridrow, 9, 1, 1)
        gridrow += 4
        form1.addWidget(self._reloaddata_button, gridrow, 0, 1, 1)
        form1.addWidget(self._aggregatedata_button, gridrow, 6, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self._aggregatedata_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
#         layout.addStretch(5)
#        layout.addLayout(hbox1)
        self.setLayout(layout)                
        #
        return self

    def _aggregateData(self):
        """ """
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
                selected_taxon_rank = unicode(self._aggregate_rank_list.currentText())
                selected_trophic_type_list = self._trophic_type_listview.getSelectedDataList()
                selected_trophic_type_text = '-'.join(selected_trophic_type_list) 
                selected_lifestage_list = self._lifestage_listview.getSelectedDataList()
                selected_lifestage_text = '-'.join(selected_lifestage_list) 
                #
                for visitnode in self._analysisdata.get_data().getChildren()[:]: 
                    for samplenode in visitnode.getChildren()[:]:
                        aggregatedvariables = {}
                        for variablenode in samplenode.getChildren()[:]:
                            newtaxon = None
                            value = variablenode.get_data('value')
                            # Use values containing valid float data.
                            try:
    #                            value = value.replace(',', '.').replace(' ', '')
                                value = float(value) 
                                #
                                if selected_taxon_rank == 'Biota (all levels)':
                                    newtaxon = 'Biota' # Biota is above kingdom in the taxonomic hierarchy.
                                elif selected_taxon_rank == 'Plankton group':
                                    newtaxon = envmonlib.Species().getPlanktonGroupFromTaxonName(variablenode.get_data('scientific_name'))
                                elif selected_taxon_rank == 'Kingdom':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Kingdom')
                                elif selected_taxon_rank == 'Phylum':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Phylum')
                                elif selected_taxon_rank == 'Class':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Class')
                                elif selected_taxon_rank == 'Order':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Order')
                                elif selected_taxon_rank == 'Family':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Family')
                                elif selected_taxon_rank == 'Genus':
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Genus')
                                elif selected_taxon_rank == 'Species': 
                                    newtaxon = envmonlib.Species().getTaxonValue(variablenode.get_data('scientific_name'), 'Species')
                                elif selected_taxon_rank == 'Scientific name': 
                                    newtaxon = variablenode.get_data('scientific_name')
                                elif selected_taxon_rank == 'Kingdom (from dataset)':
                                    newtaxon = variablenode.get_data('kingdom')
                                elif selected_taxon_rank == 'Phylum (from dataset)':
                                    newtaxon = variablenode.get_data('phylum')
                                elif selected_taxon_rank == 'Class (from dataset)':
                                    newtaxon = variablenode.get_data('class')
                                elif selected_taxon_rank == 'Order (from dataset)':
                                    newtaxon = variablenode.get_data('order')
                                elif selected_taxon_rank == 'Family (from dataset)':
                                    newtaxon = variablenode.get_data('family')
                                elif selected_taxon_rank == 'Genus (from dataset)':
                                    newtaxon = variablenode.get_data('genus')
                                elif selected_taxon_rank == 'Species (from dataset)': 
                                    newtaxon = variablenode.get_data('species')
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
                                    toolbox_utils.Logging().warning('Value is not a valid float: ' + unicode(variablenode.get_data('Value')))
                        #Remove all variables for this sample.
                        samplenode.removeAllChildren()
                        # Add the new aggregated variables instead.  
                        for variablekeytuple in aggregatedvariables:
                            newtaxon, taxontrophic_type, stage, sex, parameter, unit = variablekeytuple
                            #
                            newvariable = toolbox_core.VariableNode()
                            samplenode.addChild(newvariable)    
                            #
                            newvariable.addData('scientific_name', newtaxon)
                            newvariable.addData('trophic_type', taxontrophic_type)
                            newvariable.addData('stage', stage)
                            newvariable.addData('sex', sex)
                            newvariable.addData('parameter', parameter)
                            newvariable.addData('unit', unit)
                            newvariable.addData('value', aggregatedvariables[variablekeytuple])
                            # Add taxon class, etc. based on taxon name.
                            newvariable.addData('kingdom', envmonlib.Species().getTaxonValue(newtaxon, 'Kingdom'))
                            newvariable.addData('phylum', envmonlib.Species().getTaxonValue(newtaxon, 'Phylum'))
                            newvariable.addData('class', envmonlib.Species().getTaxonValue(newtaxon, 'Class'))
                            newvariable.addData('order', envmonlib.Species().getTaxonValue(newtaxon, 'Order'))
                            newvariable.addData('family', envmonlib.Species().getTaxonValue(newtaxon, 'Family'))
                            newvariable.addData('genus', envmonlib.Species().getTaxonValue(newtaxon, 'Genus'))
                            newvariable.addData('species', envmonlib.Species().getTaxonValue(newtaxon, 'Species'))
                #
                self._main_activity.updateViewedDataAndTabs()    
            except UserWarning as e:
                toolbox_utils.Logging().error('Failed to aggregate data. ' + unicode(e))
                QtGui.QMessageBox.warning(self._main_activity, 'Warning', 'Failed to aggregate data. ' + unicode(e))
        finally:
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Aggregation of data is done.')
            

    def _updateSelectDataAlternatives(self):
        """ """
        analysisdata = self._analysisdata.get_data()
        if not analysisdata:
            return # Empty data.
        #
        trophic_type_set = set()
        lifestageset = set()
        for visitnode in analysisdata.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    #
                    trophic_type_set.add(unicode(variablenode.get_data('trophic_type')))
                    #
                    lifestage = variablenode.get_data('stage')
                    if variablenode.get_data('sex'):
                        lifestage += '/' + variablenode.get_data('sex')
                    lifestageset.add(lifestage)
        # Selection lists.
        self._trophic_type_listview.setList(sorted(trophic_type_set))
        self._lifestage_listview.setList(sorted(lifestageset))
            
    def _addMissingTaxa(self):
        """ """
        try:
            toolbox_utils.Logging().log('Adding 0 for not observed...')
            toolbox_utils.Logging().start_accumulated_logging()
            #
            analysisdata = self._analysisdata.get_data()
            if not analysisdata:        
                return
            # 
            toolbox_core.AnalysisPrepare().addMissingTaxa(analysisdata)
            #
            self._main_activity.updateViewedDataAndTabs()    
        except UserWarning as e:
            toolbox_utils.Logging().error('Failed to add 0 for not observed. ' + unicode(e))
            QtGui.QMessageBox.warning(self._main_activity, 'Warning', 'Failed to add 0 for not observed. ' + unicode(e))
        finally:
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Add 0 for not observed is done.')

