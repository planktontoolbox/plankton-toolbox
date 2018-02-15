#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework

class AnalyseDatasetsTab1(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab1, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.get_analysis_data()
                
    def clear(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        
    def update(self):
        """ """        

    # ===== TAB: Select dataset(s) ===== 
    def content_select_datasets(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab1_intro'))
        #
        loaded_datasets_listview = QtWidgets.QListView()
#         loaded_datasets_listview.setMaximumHeight(80)
#        view.setMinimumWidth(500)
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        # Listen for changes in the toolbox dataset list.
        app_framework.ToolboxDatasets().datasetListChanged.connect(self._update_imported_dataset_list)
        #
        self._clearanalysisdata_button = QtWidgets.QPushButton('Clear analysis data')
        self._clearanalysisdata_button.clicked.connect(self._clear_analysis_data)                
        self._copydatasets_button = QtWidgets.QPushButton('Load marked dataset(s) for analysis')
        self._copydatasets_button.clicked.connect(self._copy_datasets_for_analysis)                
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._clearanalysisdata_button)
        hbox1.addWidget(self._copydatasets_button)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addWidget(loaded_datasets_listview, 10)
#         layout.addStretch(5)
        layout.addLayout(hbox1)
        self.setLayout(layout)                
        #
        return self

    def _update_imported_dataset_list(self):
        """ """
        self._loaded_datasets_model.clear()        
        for rowindex, dataset in enumerate(app_framework.ToolboxDatasets().get_datasets()):
            item = QtGui.QStandardItem('Import-' + str(rowindex + 1) + 
                                       '.   Source: ' + dataset.get_metadata('file_name'))
            item.setCheckState(QtCore.Qt.Checked)
#            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._loaded_datasets_model.appendRow(item)

    def _clear_analysis_data(self):
        """ """
        self._main_activity.view_analysis_data()
#         self._analysisdata.set_data(None)    
        self._main_activity.get_analysis_data().clear_data()    
        self._main_activity.get_statistical_data().clear_data()    
        self._main_activity.get_report_data().clear_data()    
        self._main_activity.update_viewed_data_and_tabs() 

    def _copy_datasets_for_analysis(self):
        """ """
        try:
            toolbox_utils.Logging().log('Copy datasets for analysis...')
            toolbox_utils.Logging().start_accumulated_logging()
            #
            self._main_activity.view_analysis_data()
            # Clear analysis data
            self._analysisdata.clear_data()
            self._main_activity.update_viewed_data_and_tabs() 
            # Create a list of selected datasets.        
            datasets = []
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    datasets.append(plankton_core.Datasets().get_datasets()[rowindex])
            # Use the datasets for analysis.
            self._analysisdata.copy_datasets_to_analysis_data(datasets)  
            # Check.
            if (self._analysisdata.get_data() == None) or (len(self._analysisdata.get_data().get_children()) == 0):
                toolbox_utils.Logging().log('Selected datasets are empty.')
                raise UserWarning('Selected datasets are empty.')
            self._main_activity.update_viewed_data_and_tabs() 
        #
        except UserWarning as e:
            toolbox_utils.Logging().error('Failed to copy data for analysis. ' + str(e))
            QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', 'Failed to copy data for analysis. ' + str(e))
        finally:
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Copy datasets for analysis is done.')

