#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab2(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab2, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        self._column_list.clear()
        self._column_list.setEnabled(False)
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.getData()
        if analysisdata:        
            # For tab "Generic graphs".        
            self._column_list.addItems([item[u'header'] for item in analysisdata.getExportTableColumns()])
            #  Make combo-boxes visible.
            self._column_list.setEnabled(True)

    # ===== TAB: Prepare data ===== 
    def contentPrepareData(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab2_intro'))
#         introlabel.setText("""
#         Prepare your data by removing unwanted rows from "Analysis data".
#         This may be useful if you want to use data from one or a few stations or data from a certain depth or time period.
#         """)
        #
        self._column_list = QtGui.QComboBox()
        self._column_list.setMinimumContentsLength(20)
        self._column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._column_list.setEnabled(False)
        #
        self.connect(self._column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateColumnContent)                
        # Column content.
        self._content_listview = utils_qt.SelectableQListView()
        self._content_listview.setMaximumHeight(100)
        #
        clearall_label = utils_qt.ClickableQLabel("Clear all")
        markall_label = utils_qt.ClickableQLabel("Mark all")
        self.connect(clearall_label, QtCore.SIGNAL("clicked()"), self._content_listview.uncheckAll)                
        self.connect(markall_label, QtCore.SIGNAL("clicked()"), self._content_listview.checkAll)                
        #
        self._keepdata_button = QtGui.QPushButton("Keep marked data")
        self.connect(self._keepdata_button, QtCore.SIGNAL("clicked()"), self._keepData)                
        self._removedata_button = QtGui.QPushButton("Remove marked data")
        self.connect(self._removedata_button, QtCore.SIGNAL("clicked()"), self._removeData)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Column:")
        label2 = QtGui.QLabel("Content:")
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
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self

    def _updateColumnContent(self, selected_row):
        """ """
        analysisdata = self._analysisdata.getData()
        if not analysisdata:
            self._content_listview.clear()
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = u''
        key = u''
        for info_dict in analysisdata.getExportTableColumns():
            if info_dict[u'header'] == selectedcolumn:
                nodelevel = info_dict[u'node']
                key = info_dict[u'key']
                break # Break loop.
        #
        if nodelevel == u'dataset':
            if key in analysisdata.getDataDict().keys():
                columncontent_set.add(unicode(analysisdata.getData(key)))
            else:
                columncontent_set.add(u'') # Add empty field.
        #    
        for visitnode in analysisdata.getChildren():
            if nodelevel == u'visit':
                if key in visitnode.getDataDict().keys():
                    columncontent_set.add(unicode(visitnode.getData(key)))
                else:
                    columncontent_set.add(u'') # Add empty field.
                continue    
            #
            for samplenode in visitnode.getChildren():
                if nodelevel == u'sample':
                    if key in samplenode.getDataDict().keys():
                        columncontent_set.add(unicode(samplenode.getData(key)))
                    else:
                        columncontent_set.add(u'') # Add empty field.
                    continue    
                #
                for variablenode in samplenode.getChildren():
                    if nodelevel == u'variable':
                        if key in variablenode.getDataDict().keys():
                            columncontent_set.add(unicode(variablenode.getData(key)))
                        else:
                            columncontent_set.add(u'') # Add empty field.
                        continue    
            # Content list.
        self._content_listview.setList(sorted(columncontent_set))

    def _keepData(self):
        """ """        
        self._removeData(keep_data = True)

    def _removeData(self, keep_data = False):
        """ """
        selectedcolumn = unicode(self._column_list.currentText())
        #
        if keep_data == False:
            markedcontent = self._content_listview.getSelectedDataList()
        else:
            markedcontent = self._content_listview.getNotSelectedDataList() # Note: "Not-selected" list.       
        #
        self._analysisdata.removeData(selectedcolumn, markedcontent)
        #
        self._main_activity.updateViewedDataAndTabs()    
