#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore
# import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts

import toolbox_utils
import plankton_core

class AnalyseDatasetsTab2(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab2, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.get_analysis_data()
                
    def clear(self):
        """ """
        self._column_list.clear()
        self._column_list.setEnabled(False)
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.get_data()
        if analysisdata:        
            # For tab "Generic graphs".        
            self._column_list.addItems([item['header'] for item in analysisdata.get_export_table_columns()])
            #  Make combo-boxes visible.
            self._column_list.setEnabled(True)

    # ===== TAB: Prepare data ===== 
    def content_prepare_data(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab2_intro'))
        #
        self._column_list = QtWidgets.QComboBox()
        self._column_list.setMinimumContentsLength(20)
        self._column_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._column_list.setEnabled(False)
        #
        self._column_list.currentIndexChanged(int)'), self._update_column_content)                
        # Column content.
        self._content_listview = app_framework.SelectableQListView()
#         self._content_listview.setMaximumHeight(100)
        #
        clearall_label = app_framework.ClickableQLabel('Clear all')
        markall_label = app_framework.ClickableQLabel('Mark all')
        clearall_label.clicked.connect(self._content_listview.uncheckAll)                
        markall_label.clicked.connect(self._content_listview.checkAll)                
        #
        self._keepdata_button = QtWidgets.QPushButton('Keep marked data')
        self._keepdata_button.clicked(self._keep_data)                
        self._removedata_button = QtWidgets.QPushButton('Remove marked data')
        self._removedata_button.clicked(self._remove_data)                
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Column:')
        label2 = QtWidgets.QLabel('Content:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_listview, gridrow, 1, 5, 2)
        form1.addWidget(self._keepdata_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._removedata_button, gridrow, 3, 1, 1)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 1, 1, 1)
        form1.addWidget(markall_label, gridrow, 2, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
#         layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self

    def _update_column_content(self, selected_row):
        """ """
        analysisdata = self._analysisdata.get_data()
        if not analysisdata:
            self._content_listview.clear()
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = ''
        key = ''
        for info_dict in analysisdata.get_export_table_columns():
            if info_dict['header'] == selectedcolumn:
                nodelevel = info_dict['node']
                key = info_dict['key']
                break # Break loop.
        #
        if nodelevel == 'dataset':
            if key in analysisdata.get_data_dict().keys():
                columncontent_set.add(unicode(analysisdata.get_data(key)))
            else:
                columncontent_set.add('') # Add empty field.
        #    
        for visitnode in analysisdata.get_children():
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
        self._content_listview.setList(sorted(columncontent_set))

    def _keep_data(self):
        """ """        
        self._remove_data(keep_data = True)

    def _remove_data(self, keep_data = False):
        """ """
        selectedcolumn = unicode(self._column_list.currentText())
        #
        if keep_data == False:
            markedcontent = self._content_listview.getSelectedDataList()
        else:
            markedcontent = self._content_listview.getNotSelectedDataList() # Note: "Not-selected" list.       
        #
        self._analysisdata.remove_data(selectedcolumn, markedcontent)
        #
        self._main_activity.update_viewed_data_and_tabs()    
