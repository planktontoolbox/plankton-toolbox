#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework
import app_tools

class ScreeningActivity(app_framework.ActivityBase):
    """ Used for screening of content of loaded datasets. """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(ScreeningActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        app_framework.ToolboxDatasets().datasetListChanged.connect(self.update)
        # Data object used for plotting.
        self._graph_plot_data = None

    def update(self):
        """ """
        try:
            # Selectable list of loaded datasets.
            self._loaded_datasets_model.clear()        
            for rowindex, dataset in enumerate(app_framework.ToolboxDatasets().get_datasets()):
                item = QtGui.QStandardItem('Import-' + str(rowindex + 1) + 
                                           '.   Source: ' + dataset.get_metadata('file_name'))
                item.setCheckState(QtCore.Qt.Checked)
    #            item.setCheckState(QtCore.Qt.Unchecked)
                item.setCheckable(True)
                self._loaded_datasets_model.appendRow(item)
            #
            self.update_column_list()
            self.update_parameter_list()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_screening_tabs())

    def _content_screening_tabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtWidgets.QGroupBox('', self)
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(self._content_select_datasets(), 'Select datasets')
        tabWidget.addTab(self._content_structure_screening(), 'Check structure')
        tabWidget.addTab(self._content_codes_species_screening(), 'Check species') # 'Check code lists and species')
        tabWidget.addTab(self._content_check_column_values(), 'Check column values')
        tabWidget.addTab(self._content_plot_parameters(), 'Plot parameters')
        # Layout widgets.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # === Select datasets ===
    def _content_select_datasets(self):
        """ """
        widget = QtWidgets.QWidget()
        #
        loaded_datasets_listview = QtWidgets.QListView()
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        #
        self._clear_metadata_button = app_framework.ClickableQLabel('Clear all')
        self._clear_metadata_button.label_clicked.connect(self._uncheck_all_datasets)                
        self._markall_button = app_framework.ClickableQLabel('Mark all')
        self._markall_button.label_clicked.connect(self._check_all_datasets)                
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._clear_metadata_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(loaded_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _check_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Checked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _uncheck_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Unchecked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # === Content structure ===
    def _content_structure_screening(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_0'))
        #
        self._checkdatasets_button = QtWidgets.QPushButton('View\ndatasets')
        self._checkdatasets_button.clicked.connect(self._check_datasets)                
        self._checkvisits_button = QtWidgets.QPushButton('View\nsampling events')
        self._checkvisits_button.clicked.connect(self._check_visits) 
        self._checksamples_button = QtWidgets.QPushButton('View\nsamples')
        self._checksamples_button.clicked.connect(self._check_samples) 
        #                
        self._checkduplicates_button = QtWidgets.QPushButton('Scan for\nduplicates')
        self._checkduplicates_button.clicked.connect(self._scan_for_duplicates)                

        # Result content.
        self._structureresult_list = QtWidgets.QTextEdit()
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Result:')
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
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def _check_datasets(self):
        """ """
        try:
            self._structureresult_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                        row = '   - Sampling events: ' + str(countvisits) + \
                              ', samples: ' + str(countsamples) + \
                              ', variable rows: ' + str(countvariables) 
                        self._structureresult_list.append(row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _check_visits(self):
        """ """
        try:
            self._structureresult_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                                  ', ' + visitnode.get_data('sample_date')
                            self._structureresult_list.append(row)
                            countsamples = 0
                            countvariables = 0
                            for samplenode in visitnode.get_children():
                                countsamples += 1
                                countvariables += len(samplenode.get_children())
                            #
                            row = '      - Samples: ' + str(countsamples) + \
                              ', variable rows: ' + str(countvariables) 
                            self._structureresult_list.append(row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _check_samples(self):
        """ """
        try:
            self._structureresult_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                                  str(visitnode.get_data('station_name')) + ' ' + \
                                  str(visitnode.get_data('sample_date'))
                            self._structureresult_list.append(row)
                            for samplenode in visitnode.get_children():
                                row = '      - Sample: ' + \
                                      str(samplenode.get_data('sample_min_depth_m')) + '-' + \
                                      str(samplenode.get_data('sample_max_depth_m'))
                                self._structureresult_list.append(row)
                                countvariables = len(samplenode.get_children())
                                #
                                row = '         - Variable rows: ' + str(countvariables) 
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
                                row = '         - Unique parameters/units: ' + str(len(parameter_set)) 
                                self._structureresult_list.append(row)
                                row = '         - Unique taxon names: ' + str(len(taxonname_set)) 
                                self._structureresult_list.append(row)
                                row = '         - Unique taxon-names/size-classes/stages/sex: ' + str(len(taxonsizestagesex_set)) 
                                self._structureresult_list.append(row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _scan_for_duplicates(self):
        """ """
        try:
            self._structureresult_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                            visit_descr = str(visitnode.get_data('station_name')) + ', ' + \
                                          str(visitnode.get_data('sample_date'))
                            for samplenode in visitnode.get_children():
                                sample_descr = str(samplenode.get_data('sample_min_depth_m')) + '-' + \
                                               str(samplenode.get_data('sample_max_depth_m'))
                                check_duplicates_list = [] # Duplicates can occur inside one sample.
                                sample_description = dataset_descr + ', ' + visit_descr + ', ' + sample_descr
                                for variablenode in samplenode.get_children():
                                    scientific_name = str(variablenode.get_data('scientific_name'))
                                    size_class = str(variablenode.get_data('size_class'))
                                    stage = str(variablenode.get_data('stage'))
                                    sex = str(variablenode.get_data('sex'))
                                    parameter = str(variablenode.get_data('parameter'))
                                    unit = str(variablenode.get_data('unit'))
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # === Content code lists and species ===
    def _content_codes_species_screening(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
#         introlabel_1 = app_framework.RichTextQLabel()
#         introlabel_1.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_1'))
#         introlabel_2 = app_framework.RichTextQLabel()
#         introlabel_2.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_2'))
#         introlabel_3 = app_framework.RichTextQLabel()
#         introlabel_3.setText(help_texts.HelpTexts().getText('ScreeningActivity_species'))
#         introlabel_4 = app_framework.RichTextQLabel()
#         introlabel_4.setText(help_texts.HelpTexts().getText('ScreeningActivity_sizeclasses'))
        #
#         self._checkcodes_button = QtWidgets.QPushButton('Check\ncode lists')
#         self._checkcodes_button.clicked.connect(self._code_list_screening)                
        self._checkspecies_button = QtWidgets.QPushButton('Check\nspecies')
        self._checkspecies_button.clicked.connect(self._species_screening) 
        self._checksizeclasses_button = QtWidgets.QPushButton('Check\nsize classes')
        self._checksizeclasses_button.clicked.connect(self._bvol_screening) 

        # Result content.
        self._codesspeciesresult_list = QtWidgets.QTextEdit()
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Result:')
        form1.addWidget(label1, gridrow, 1, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._checkcodes_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkspecies_button, gridrow, 0, 1, 1)
        form1.addWidget(self._codesspeciesresult_list, gridrow, 1, 30, 1)
        gridrow += 1
        form1.addWidget(self._checksizeclasses_button, gridrow, 0, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel_1)
#         layout.addWidget(introlabel_2)
#         layout.addWidget(introlabel_3)
#         layout.addWidget(introlabel_4)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

#     def _code_list_screening(self):
#         """ """
#         # Screening results is also shown in the toolbox log.
#         tool_manager.ToolManager().show_tool_by_name('Toolbox logging')
#         #
#         self._codesspeciesresult_list.clear()
#         #
#         try:
#             toolbox_utils.Logging().log('') # Empty line.
#             toolbox_utils.Logging().log('Code list screening started...')
#             toolbox_utils.Logging().start_accumulated_logging()
#             self._write_to_status_bar('Code list screening in progress...')
#             # Perform screening.
#             codetypes_set = plankton_core.ScreeningManager().code_list_screening(app_framework.ToolboxDatasets().get_datasets())
#         finally:
#             # Log in result window.
#             self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
#                                               str(sorted(codetypes_set)))
#             self._codesspeciesresult_list.append('')
#             #
#             inforows = toolbox_utils.Logging().get_all_info_rows()
#             if inforows:
#                 for row in inforows:
#                     self._codesspeciesresult_list.append('- ' + row)                
#             warningrows = toolbox_utils.Logging().getAllWarnings()
#             if warningrows:
#                 for row in warningrows:
#                     self._codesspeciesresult_list.append('- ' + row)
#             errorrows = toolbox_utils.Logging().get_all_errors()
#             if errorrows:
#                 for row in errorrows:
#                     self._codesspeciesresult_list.append('- ' + row)
#             # Also add to the logging tool.
#             toolbox_utils.Logging().log_all_accumulated_rows()
#             toolbox_utils.Logging().log('Screening was done on these code types: ' + 
#                                     str(sorted(codetypes_set)))
#             toolbox_utils.Logging().log('Code list screening done.')
#             self._write_to_status_bar('')

    def _species_screening(self):
        """ """
        try:
            # Screening results is also shown in the toolbox log.
            app_tools.ToolManager().show_tool_by_name('Toolbox logging')
            #
            self._codesspeciesresult_list.clear()
            #
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Species screening started...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('Species screening in progress...')
                # Perform screening.
                plankton_core.ScreeningManager().species_screening(app_framework.ToolboxDatasets().get_datasets())
            finally:
                # Log in result window.
    #             self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
    #                                               str(sorted(codetypes_set)))
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _bvol_screening(self):
        """ """
        try:
            # Screening results is also shown in the toolbox log.
            app_tools.ToolManager().show_tool_by_name('Toolbox logging')
            #
            self._codesspeciesresult_list.clear()
            #
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('BVOL Species screening started...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('BVOL Species screening in progress...')
                # Perform screening.
                plankton_core.ScreeningManager().bvol_species_screening(app_framework.ToolboxDatasets().get_datasets())
            finally:
                # Log in result window.
    #             self._codesspeciesresult_list.append('Screening was done on these code types: ' + 
    #                                               str(sorted(codetypes_set)))
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # === Content column values ===
    def _content_check_column_values(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_intro_3'))
        #
        self._column_list = QtWidgets.QComboBox()
        self._column_list.setMinimumContentsLength(30)
        self._column_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._column_list.setEnabled(False)
        #
        self._column_list.currentIndexChanged.connect(self._update_column_content)                
        # Column content.
##        self._content_list = app_framework.SelectableQListView()
##        self._content_list = QtWidgets.QListWidget()
        self._content_list = QtWidgets.QTextEdit()
#        self._content_list.setMaximumHeight(200)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Column:')
        label2 = QtWidgets.QLabel('Content:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_list, gridrow, 1, 30, 1)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def update_column_list(self):
        """ """
        try:
            self._column_list.clear()
            self._content_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
                               
    def _update_column_content(self, selected_row):
        """ """
        try:
            datasets = app_framework.ToolboxDatasets().get_datasets()
            self._content_list.clear()
            if not (datasets and (len(datasets) > 0)):        
                return # Empty data.
            #
            columncontent_set = set()
            selectedcolumn = str(self._column_list.currentText())
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
                            columncontent_set.add(str(dataset.get_data(key)))
                        else:
                            columncontent_set.add('') # Add empty field.
                    #
                    for visitnode in dataset.get_children():
                        if nodelevel == 'visit':
                            if key in visitnode.get_data_dict().keys():
                                columncontent_set.add(str(visitnode.get_data(key)))
                            else:
                                columncontent_set.add('') # Add empty field.
                            continue    
                        #
                        for samplenode in visitnode.get_children():
                            if nodelevel == 'sample':
                                if key in samplenode.get_data_dict().keys():
                                    columncontent_set.add(str(samplenode.get_data(key)))
                                else:
                                    columncontent_set.add('') # Add empty field.
                                continue    
                            #
                            for variablenode in samplenode.get_children():
                                if nodelevel == 'variable':
                                    if key in variablenode.get_data_dict().keys():
                                        columncontent_set.add(str(variablenode.get_data(key)))
                                    else:
                                        columncontent_set.add('') # Add empty field.
                                    continue    
            # Content list.
    #        self._content_list.addItems(sorted(columncontent_set))
            for row in sorted(columncontent_set): 
                self._content_list.append(row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # === Content plot ===
    def _content_plot_parameters(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('ScreeningActivity_plotting'))
        #
        self._parameter_list = app_framework.SelectableQListView()       
        #
        clearall_label = app_framework.ClickableQLabel('Clear all')
        markall_label = app_framework.ClickableQLabel('Mark all')
        clearall_label.label_clicked.connect(self._parameter_list.uncheckAll)                
        markall_label.label_clicked.connect(self._parameter_list.checkAll)                
        #
        self._plotparameters_button = QtWidgets.QPushButton('Plot parameter values')
        self._plotparameters_button.clicked.connect(self._plot_screening)                
        self._plotparameterperdate_button = QtWidgets.QPushButton('Plot parameters values per date')
        self._plotparameterperdate_button.clicked.connect(self._plot_screening_per_date)                
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Parameters:')
        form1.addWidget(label1, gridrow, 0, 1, 2)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 30)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 0, 1, 1)
        form1.addWidget(markall_label, gridrow, 1, 1, 1)
        #
        hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(10)
        hbox1.addWidget(self._plotparameters_button)
        hbox1.addWidget(self._plotparameterperdate_button)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def update_parameter_list(self):
        """ """
        try:
            self._parameter_list.clear()
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _plot_screening(self):
        """ """
        try:
            # Show the Graph plotter tool if hidden. 
            app_tools.ToolManager().show_tool_by_name('Graph plotter')
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _add_plot(self, parameter):
        """ """
        try:
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                QtWidgets.QMessageBox.warning(self, "Warning", str(e))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _plot_screening_per_date(self):
        """ """
        try:
            # Show the Graph plotter tool if hidden. 
            app_tools.ToolManager().show_tool_by_name('Graph plotter')
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _add_plot_per_date(self, parameter):
        """ """
        try:
            datasets = app_framework.ToolboxDatasets().get_datasets()
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
                            date = visitnode.get_data('sample_date')
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
            self._graph_plot_data.add_plot(plot_name = parameter, x_array = xarray, y_array = yarray)
        #
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Warning", str(e))
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

