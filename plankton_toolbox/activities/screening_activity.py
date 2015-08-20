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
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
# import plankton_toolbox.toolbox.help_texts as help_texts

import toolbox_utils
import plankton_core

class ScreeningActivity(activity_base.ActivityBase):
    """ Used for screening of content of loaded datasets. """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(ScreeningActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL('datasetListChanged'), 
                     self.update)
        # Data object used for plotting.
        self._graph_plot_data = None

    def update(self):
        """ """
        # Selectable list of loaded datasets.
        self._loaded_datasets_model.clear()        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            item = QtGui.QStandardItem('Dataset-' + unicode(rowindex + 1) + 
                                       '.   Source: ' + dataset.get_metadata('file_name'))
            item.setCheckState(QtCore.Qt.Checked)
#            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._loaded_datasets_model.appendRow(item)
        #
        self.update_column_list()
        self.update_parameter_list()
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = utils_qt.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_screening_tabs())

    def _content_screening_tabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_select_datasets(), 'Select datasets')
        tabWidget.addTab(self._content_structure_screening(), 'Check structure')
        tabWidget.addTab(self._content_codes_species_screening(), 'Check code lists and species')
        tabWidget.addTab(self._content_check_column_values(), 'Check column values')
        tabWidget.addTab(self._content_plot_parameters(), 'Plot parameters')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # === Select datasets ===
    def _content_select_datasets(self):
        """ """
        widget = QtGui.QWidget()
        #
        loaded_datasets_listview = QtGui.QListView()
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        #
        self._cleara_metadata_button = QtGui.QPushButton('Clear all')
        self.connect(self._cleara_metadata_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_datasets)                
        self._markall_button = QtGui.QPushButton('Mark all')
        self.connect(self._markall_button, QtCore.SIGNAL('clicked()'), self._check_all_datasets)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._cleara_metadata_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(loaded_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _check_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    # === Content structure ===
    def _content_structure_screening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_0'))
        #
        self._checkdatasets_button = QtGui.QPushButton('View\ndatasets')
        self.connect(self._checkdatasets_button, QtCore.SIGNAL('clicked()'), self._check_datasets)                
        self._checkvisits_button = QtGui.QPushButton('View\nsampling events')
        self.connect(self._checkvisits_button, QtCore.SIGNAL('clicked()'), self._check_visits) 
        self._checksamples_button = QtGui.QPushButton('View\nsamples')
        self.connect(self._checksamples_button, QtCore.SIGNAL('clicked()'), self._check_samples) 
        #                
        self._checkduplicates_button = QtGui.QPushButton('Scan for\nduplicates')
        self.connect(self._checkduplicates_button, QtCore.SIGNAL('clicked()'), self._scan_for_duplicates)                

        # Result content.
        self._structureresult_list = QtGui.QTextEdit()
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Result:')
        form1.addWidget(label1, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkdatasets_button, gridrow, 0, 1, 1)
        form1.addWidget(self._structureresult_list, gridrow, 1, 30, 1)
        gridrow += 1
        form1.addWidget(self._checkvisits_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checksamples_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkduplicates_button, gridrow, 0, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def _check_datasets(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        countvisits = 0
        countsamples = 0
        countvariables = 0
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    row = 'Dataset: ' + dataset.get_metadata('file_name')
                    self._structureresult_list.append(row)
                    countvisits = 0
                    countsamples = 0
                    countvariables = 0
                    for visitnode in dataset.get_children():
                        countvisits += 1
                        for samplenode in visitnode.get_children():
                            countsamples += 1
                            countvariables += len(samplenode.get_children())
                    #
                    row = '   - Sampling events: ' + unicode(countvisits) + \
                          ', samples: ' + unicode(countsamples) + \
                          ', variable rows: ' + unicode(countvariables) 
                    self._structureresult_list.append(row)

    def _check_visits(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        countsamples = 0
        countvariables = 0
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    row = 'Dataset: ' + dataset.get_metadata('file_name')
                    self._structureresult_list.append(row)
                    countsamples = 0
                    countvariables = 0
                    for visitnode in dataset.get_children():
                        row = '   - Sampling event: ' + visitnode.get_data('station_name') + \
                              ', ' + visitnode.get_data('date')
                        self._structureresult_list.append(row)
                        countsamples = 0
                        countvariables = 0
                        for samplenode in visitnode.get_children():
                            countsamples += 1
                            countvariables += len(samplenode.get_children())
                        #
                        row = '      - Samples: ' + unicode(countsamples) + \
                          ', variable rows: ' + unicode(countvariables) 
                        self._structureresult_list.append(row)

    def _check_samples(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    row = 'Dataset: ' + dataset.get_metadata('file_name')
                    self._structureresult_list.append(row)
                    for visitnode in dataset.get_children():
                        row = '   - Sampling event: ' + \
                              unicode(visitnode.get_data('station_name')) + ' ' + \
                              unicode(visitnode.get_data('date'))
                        self._structureresult_list.append(row)
                        for samplenode in visitnode.get_children():
                            row = '      - Sample: ' + \
                                  unicode(samplenode.get_data('sample_min_depth_m')) + '-' + \
                                  unicode(samplenode.get_data('sample_max_depth_m'))
                            self._structureresult_list.append(row)
                            countvariables = len(samplenode.get_children())
                            #
                            row = '         - Variable rows: ' + unicode(countvariables) 
                            self._structureresult_list.append(row)
                            #
                            parameter_set = set()
                            taxonname_set = set()
                            taxonsizestagesex_set = set()
                            for variablenode in samplenode.get_children():
                                parameter = variablenode.get_data('parameter')
                                unit = variablenode.get_data('unit')
                                taxonname = variablenode.get_data('scientific_name')
                                sizeclass = variablenode.get_data('size_class')
                                stage = variablenode.get_data('stage')
                                sex = variablenode.get_data('sex')
                                if parameter:
                                    parameter_set.add(parameter + '+' + unit)
                                if taxonname:
                                    taxonname_set.add(taxonname)
                                    taxonsizestagesex_set.add(taxonname + '+' + sizeclass + '+' + stage + '+' + sex)
                            row = '         - Unique parameters/units: ' + unicode(len(parameter_set)) 
                            self._structureresult_list.append(row)
                            row = '         - Unique taxon names: ' + unicode(len(taxonname_set)) 
                            self._structureresult_list.append(row)
                            row = '         - Unique taxon-names/size-classes/stages/sex: ' + unicode(len(taxonsizestagesex_set)) 
                            self._structureresult_list.append(row)

    def _scan_for_duplicates(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        dataset_descr = ''
        visit_descr = ''
        sample_descr = ''
        #
        check_duplicates_list = []
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    dataset_descr = dataset.get_metadata('file_name')
                    for visitnode in dataset.get_children():
                        visit_descr = unicode(visitnode.get_data('station_name')) + ', ' + \
                                      unicode(visitnode.get_data('date'))
                        for samplenode in visitnode.get_children():
                            sample_descr = unicode(samplenode.get_data('sample_min_depth_m')) + '-' + \
                                           unicode(samplenode.get_data('sample_max_depth_m'))
                            check_duplicates_list = [] # Duplicates can occur inside one sample.
                            sample_description = dataset_descr + ', ' + visit_descr + ', ' + sample_descr
                            for variablenode in samplenode.get_children():
                                scientific_name = unicode(variablenode.get_data('scientific_name'))
                                size_class = unicode(variablenode.get_data('size_class'))
                                stage = unicode(variablenode.get_data('stage'))
                                sex = unicode(variablenode.get_data('sex'))
                                parameter = unicode(variablenode.get_data('parameter'))
                                unit = unicode(variablenode.get_data('unit'))
                                #
                                unique_items = (scientific_name, size_class, stage, sex, parameter, unit)
                                if unique_items in check_duplicates_list:
                                    if sample_description:
                                        # Print first time for sample.
                                        self._structureresult_list.append(sample_description)
                                        sample_description = ''
                                    row = '   - Duplicate found: ' + \
                                          scientific_name + ', ' + \
                                          size_class + ', ' + \
                                          stage + ', ' + \
                                          sex + ', ' + \
                                          parameter + ', ' + \
                                          unit                                        
                                    self._structureresult_list.append(row)
                                else:
                                    check_duplicates_list.append(unique_items)

    # === Content code lists and species ===
    def _content_codes_species_screening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel_1 = utils_qt.RichTextQLabel()
#         introlabel_1.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_1'))
#         introlabel_2 = utils_qt.RichTextQLabel()
#         introlabel_2.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_2'))
#         introlabel_3 = utils_qt.RichTextQLabel()
#         introlabel_3.setText(help_texts.HelpTexts().getText('ScreeningActivity_species'))
#         introlabel_4 = utils_qt.RichTextQLabel()
#         introlabel_4.setText(help_texts.HelpTexts().getText('ScreeningActivity_sizeclasses'))
        #
        self._checkcodes_button = QtGui.QPushButton('Check\ncode lists')
        self.connect(self._checkcodes_button, QtCore.SIGNAL('clicked()'), self._code_list_screening)                
        self._checkspecies_button = QtGui.QPushButton('Check\nspecies')
        self.connect(self._checkspecies_button, QtCore.SIGNAL('clicked()'), self._species_screening) 
        self._checksizeclasses_button = QtGui.QPushButton('Check\nsize classes')
        self.connect(self._checksizeclasses_button, QtCore.SIGNAL('clicked()'), self._bvol_screening) 

        # Result content.
        self._codesspeciesresult_list = QtGui.QTextEdit()
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Result:')
        form1.addWidget(label1, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkcodes_button, gridrow, 0, 1, 1)
        form1.addWidget(self._codesspeciesresult_list, gridrow, 1, 30, 1)
        gridrow += 1
        form1.addWidget(self._checkspecies_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checksizeclasses_button, gridrow, 0, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel_1)
#         layout.addWidget(introlabel_2)
#         layout.addWidget(introlabel_3)
#         layout.addWidget(introlabel_4)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def _code_list_screening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().show_tool_by_name('Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Code list screening started...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Code list screening in progress...')
            # Perform screening.
            codetypes_set = toolbox_utils.ScreeningManager().code_list_screening(toolbox_datasets.ToolboxDatasets().get_datasets())
        finally:
            # Log in result window.
            self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
                                              unicode(sorted(codetypes_set)))
            self._codesspeciesresult_list.append('')
            #
            inforows = toolbox_utils.Logging().get_all_info_rows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append('- ' + row)                
            warningrows = toolbox_utils.Logging().getAllWarnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append('- ' + row)
            errorrows = toolbox_utils.Logging().get_all_errors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append('- ' + row)
            # Also add to the logging tool.
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Screening was done on these code types: ' + 
                                    unicode(sorted(codetypes_set)))
            toolbox_utils.Logging().log('Code list screening done.')
            self._write_to_status_bar('')

    def _species_screening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().show_tool_by_name('Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Species screening started...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Species screening in progress...')
            # Perform screening.
            toolbox_utils.ScreeningManager().species_screening(toolbox_datasets.ToolboxDatasets().get_datasets())
        finally:
            # Log in result window.
#             self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
#                                               unicode(sorted(codetypes_set)))
#             self._codesspeciesresult_list.append('')
            #
            inforows = toolbox_utils.Logging().get_all_info_rows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append('- ' + row)                
            warningrows = toolbox_utils.Logging().get_all_warnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append('- ' + row)
            errorrows = toolbox_utils.Logging().get_all_errors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append('- ' + row)
            # Also add to the logging tool.
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Species screening done.')
            self._write_to_status_bar('')

    def _bvol_screening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().show_tool_by_name('Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('BVOL Species screening started...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('BVOL Species screening in progress...')
            # Perform screening.
            toolbox_utils.ScreeningManager().bvol_species_screening(toolbox_datasets.ToolboxDatasets().get_datasets())
        finally:
            # Log in result window.
#             self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
#                                               unicode(sorted(codetypes_set)))
#             self._codesspeciesresult_list.append('')
            #
            inforows = toolbox_utils.Logging().get_all_info_rows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append('- ' + row)                
            warningrows = toolbox_utils.Logging().get_all_warnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append('- ' + row)
            errorrows = toolbox_utils.Logging().get_all_errors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append('- ' + row)
            # Also add to the logging tool.
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('BVOL Species screening done.')
            self._write_to_status_bar('')

    # === Content column values ===
    def _content_check_column_values(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_3'))
        #
        self._column_list = QtGui.QComboBox()
        self._column_list.setMinimumContentsLength(30)
        self._column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._column_list.setEnabled(False)
        #
        self.connect(self._column_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._update_column_content)                
        # Column content.
##        self._content_list = utils_qt.SelectableQListView()
##        self._content_list = QtGui.QListWidget()
        self._content_list = QtGui.QTextEdit()
#        self._content_list.setMaximumHeight(200)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Column:')
        label2 = QtGui.QLabel('Content:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_list, gridrow, 1, 30, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def update_column_list(self):
        """ """
        self._column_list.clear()
        self._content_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        if datasets and (len(datasets) > 0):        
            columns_set = set()
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    for column in dataset.get_export_table_columns():
                        columns_set.add(column['header']) 
            #    
            self._column_list.addItems(sorted(columns_set))
            self._column_list.setEnabled(True)
        else:
            self._column_list.clear()
            self._column_list.setEnabled(False)
                               
    def _update_column_content(self, selected_row):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        self._content_list.clear()
        if not (datasets and (len(datasets) > 0)):        
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = ''
        key = ''
        for rowindex, dataset in enumerate(datasets):
            #
            item = self._loaded_datasets_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:        
                #
                for info_dict in dataset.get_export_table_columns():
                    if info_dict['header'] == selectedcolumn:
                        nodelevel = info_dict['node']
                        key = info_dict['key']
                        break # Break loop.
            if nodelevel:
                break # Also break next loop.
        #
        for rowindex, dataset in enumerate(datasets):
            #
            item = self._loaded_datasets_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:        
                #
                if nodelevel == 'dataset':
                    if key in dataset.get_data_dict().keys():
                        columncontent_set.add(unicode(dataset.get_data(key)))
                    else:
                        columncontent_set.add('') # Add empty field.
                #
                for visitnode in dataset.get_children():
                    if nodelevel == 'visit':
                        if key in visitnode.get_data_dict().keys():
                            columncontent_set.add(unicode(visitnode.get_data(key)))
                        else:
                            columncontent_set.add('') # Add empty field.
                        continue    
                    #
                    for samplenode in visitnode.get_children():
                        if nodelevel == 'sample':
                            if key in samplenode.get_data_dict().keys():
                                columncontent_set.add(unicode(samplenode.get_data(key)))
                            else:
                                columncontent_set.add('') # Add empty field.
                            continue    
                        #
                        for variablenode in samplenode.get_children():
                            if nodelevel == 'variable':
                                if key in variablenode.get_data_dict().keys():
                                    columncontent_set.add(unicode(variablenode.get_data(key)))
                                else:
                                    columncontent_set.add('') # Add empty field.
                                continue    
        # Content list.
#        self._content_list.addItems(sorted(columncontent_set))
        for row in sorted(columncontent_set): 
            self._content_list.append(row)

    # === Content plot ===
    def _content_plot_parameters(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_plotting'))
        #
        self._parameter_list = utils_qt.SelectableQListView()       
        #
        clearall_label = utils_qt.ClickableQLabel('Clear all')
        markall_label = utils_qt.ClickableQLabel('Mark all')
        self.connect(clearall_label, QtCore.SIGNAL('clicked()'), self._parameter_list.uncheckAll)                
        self.connect(markall_label, QtCore.SIGNAL('clicked()'), self._parameter_list.checkAll)                
        #
        self._plotparameters_button = QtGui.QPushButton('Plot parameter values')
        self.connect(self._plotparameters_button, QtCore.SIGNAL('clicked()'), self._plot_screening)                
        self._plotparameterperdate_button = QtGui.QPushButton('Plot parameters values per date')
        self.connect(self._plotparameterperdate_button, QtCore.SIGNAL('clicked()'), self._plot_screening_per_date)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Parameters:')
        form1.addWidget(label1, gridrow, 0, 1, 2)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 30)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 0, 1, 1)
        form1.addWidget(markall_label, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._plotparameters_button)
        hbox1.addWidget(self._plotparameterperdate_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def update_parameter_list(self):
        """ """
        self._parameter_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        if datasets and (len(datasets) > 0):        
            parameter_set = set()
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    for visitnode in dataset.get_children():
                        for samplenode in visitnode.get_children():
                            for variablenode in samplenode.get_children():
                                parameter_set.add(variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')')
                self._parameter_list.setList(sorted(parameter_set))

    def _plot_screening(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().show_tool_by_name('Graph plotter')
        graphtool = tool_manager.ToolManager().get_tool_by_name('Graph plotter')
        graphtool.clear_plot_data()
        # Set up plot data for this type.
        self._graph_plot_data = toolbox_utils.GraphPlotData(
                        title = 'Parameter values in sequence', 
                        y_type = 'float',
                        x_label = 'Sequence position in dataset(s)',
                        y_label = 'Value')        
        # One plot for each selected parameter.
        for parameter in self._parameter_list.getSelectedDataList():
            self._add_plot(parameter)
        # View in the graph-plot tool.    
        graphtool.set_chart_selection(chart = 'Line chart',
                                    combined = True, stacked = False, y_log_scale = True)
        graphtool.set_plot_data(self._graph_plot_data)   

    def _add_plot(self, parameter):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        yarray = []
#        unit_set = set() # In case of different units on the same parameter.
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    for visitnode in dataset.get_children():
                        for samplenode in visitnode.get_children():
                            for variablenode in samplenode.get_children():
                                if (variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')') == parameter:
    #                                 unit_set.add(variablenode.get_data('unit'))
                                    value = variablenode.get_data('value')
                                    yarray.append(value)                  
        #
#         units = ' --- '.join(sorted(unit_set))
#         parameter_unit = parameter + ' (' + units + ')' 
        #
#         self._graph_plot_data.add_plot(plot_name = parameter_unit, y_array = yarray)
        try:
            self._graph_plot_data.add_plot(plot_name = parameter, y_array = yarray)
        except UserWarning as e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))

    def _plot_screening_per_date(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().show_tool_by_name('Graph plotter')
        graphtool = tool_manager.ToolManager().get_tool_by_name('Graph plotter')
        graphtool.clear_plot_data()
        # Set up plot data for this type.
        self._graph_plot_data = toolbox_utils.GraphPlotData(
                        title = 'Parameter values per date', 
                        x_type = 'date',
                        y_type = 'float',
                        y_label = 'Value')        
        # One plot for each selected parameter.
        for parameter in self._parameter_list.getSelectedDataList():
            self._add_plot_per_date(parameter)
        # View in the graph-plot tool.    
        graphtool.set_chart_selection(chart = 'Scatter chart',
                                    combined = True, stacked = False, y_log_scale = True)
        graphtool.set_plot_data(self._graph_plot_data)   

    def _add_plot_per_date(self, parameter):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().get_datasets()
        #
        xarray = []
        yarray = []
#        unit_set = set() # In case of different units on the same parameter.
        #
        if datasets and (len(datasets) > 0):
            for rowindex, dataset in enumerate(datasets):
                #
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    #
                    for visitnode in dataset.get_children():
                        date = visitnode.get_data('date')
                        for samplenode in visitnode.get_children():
                            for variablenode in samplenode.get_children():
                                if (variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')') == parameter:
    #                                 unit_set.add(variablenode.get_data('unit'))
                                    value = variablenode.get_data('value')
                                    xarray.append(date)                  
                                    yarray.append(value)                  
            #
#         units = ' --- '.join(sorted(unit_set))
#         parameter_unit = parameter + ' (' + units + ')' 
        #
#         self._graph_plot_data.add_plot(plot_name = parameter_unit, y_array = yarray)
        try:
            self._graph_plot_data.add_plot(plot_name = parameter, x_array = xarray, y_array = yarray)
        except UserWarning as e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))

