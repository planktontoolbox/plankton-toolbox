#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import envmonlib

@envmonlib.singleton
class AnalyseDatasetsTab2(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
                
    def clear(self):
        """ """
        self._column_list.clear()
        self._column_list.setEnabled(False)
        
    def update(self):
        """ """
        self.clear()
        currentdata = self._main_activity.getCurrentData()
        if currentdata:        
            # For tab "Generic graphs".        
            self._column_list.addItems([item[u'Header'] for item in currentdata.getExportTableColumns()])
            #  Make combo-boxes visible.
            self._column_list.setEnabled(True)

    # ===== TAB: Prepare data ===== 
    def contentPrepareData(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        #
        self._column_list = QtGui.QComboBox()
        self._column_list.setMinimumContentsLength(20)
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
        widget.setLayout(layout)                
        #
        return widget

    def _updateColumnContent(self, selected_row):
        """ """
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:
            self._content_listview.clear()
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = u''
        key = u''
        for info_dict in currentdata.getExportTableColumns():
            if info_dict[u'Header'] == selectedcolumn:
                nodelevel = info_dict[u'Node']
                key = info_dict[u'Key']
                break # Break loop.
        #
        for visitnode in currentdata.getChildren():
            if nodelevel == u'Visit':
                if key in visitnode.getDataDict().keys():
                    columncontent_set.add(visitnode.getData(key))
                else:
                    columncontent_set.add(u'') # Add empty field.
                continue    
            #
            for samplenode in visitnode.getChildren():
                if nodelevel == u'Sample':
                    if key in samplenode.getDataDict().keys():
                        columncontent_set.add(samplenode.getData(key))
                    else:
                        columncontent_set.add(u'') # Add empty field.
                    continue    
                #
                for variablenode in samplenode.getChildren():
                    if nodelevel == u'Variable':
                        if key in variablenode.getDataDict().keys():
                            columncontent_set.add(variablenode.getData(key))
                        else:
                            columncontent_set.add(u'') # Add empty field.
                        continue    
            # Content list.
        self._content_listview.setList(sorted(columncontent_set))

    def _keepData(self):
        """ """
        
        self._removeData(keep_data = True)
        
#        # TODO: Mostly the same as removeData()
#        
#        currentdata = self._main_activity.getCurrentData()
#        if not currentdata:
#            self._content_listview.clear()
#            return # Empty data.
#        #
#        selectedcolumn = unicode(self._column_list.currentText())
#        #
#        selectedcontent = self._content_listview.getNotSelectedDataList() # Note: "Not-selected" list.
#
#        # Search for export column corresponding model element.
#        for info_dict in currentdata.getExportTableColumns():
#            if info_dict[u'Header'] == selectedcolumn:
#                nodelevel = info_dict[u'Node']
#                key = info_dict[u'Key']
#                break # Break loop.
#        #
#        for visitnode in currentdata.getChildren()[:]:
#            if nodelevel == u'Visit':
#                if key in visitnode.getDataDict().keys():
#                    if visitnode.getData(key) in selectedcontent:
#                        currentdata.removeChild(visitnode)
#                        continue
#            #
#            for samplenode in visitnode.getChildren()[:]:
#                if nodelevel == u'Sample':
#                    if key in samplenode.getDataDict().keys():
#                        if samplenode.getData(key) in selectedcontent:
#                            visitnode.removeChild(samplenode)
#                            continue
#                #
#                for variablenode in samplenode.getChildren()[:]:
#                    if nodelevel == u'Variable':
#                        if key in variablenode.getDataDict().keys():
#                            if variablenode.getData(key) in selectedcontent:
#                                samplenode.removeChild(variablenode)
#        #
#        self._main_activity.updateCurrentData()    

    def _removeData(self, keep_data = False):
        """ """
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:
            self._content_listview.clear()
            return # Empty data.
        #
        selectedcolumn = unicode(self._column_list.currentText())
        #
        if keep_data == False:
            selectedcontent = self._content_listview.getSelectedDataList()
        else:
            selectedcontent = self._content_listview.getNotSelectedDataList() # Note: "Not-selected" list.       
        
        # Search for export column corresponding model element.
        for info_dict in currentdata.getExportTableColumns():
            if info_dict[u'Header'] == selectedcolumn:
                nodelevel = info_dict[u'Node']
                key = info_dict[u'Key']
                break # Break loop.
        #
        for visitnode in currentdata.getChildren()[:]:
            if nodelevel == u'Visit':
                if key in visitnode.getDataDict().keys():
                    if visitnode.getData(key) in selectedcontent:
                        currentdata.removeChild(visitnode)
                        continue
                else:
                    # Handle empty keys.
                    if u'' in selectedcontent:
                        currentdata.removeChild(visitnode)
                        continue
            #
            for samplenode in visitnode.getChildren()[:]:
                if nodelevel == u'Sample':
                    if key in samplenode.getDataDict().keys():
                        if samplenode.getData(key) in selectedcontent:
                            visitnode.removeChild(samplenode)
                            continue
                    else:
                        # Handle empty keys.
                        if u'' in selectedcontent:
                            visitnode.removeChild(samplenode)
                            continue
                #
                for variablenode in samplenode.getChildren()[:]:
                    if nodelevel == u'Variable':
                        if key in variablenode.getDataDict().keys():
                            if variablenode.getData(key) in selectedcontent:
                                samplenode.removeChild(variablenode)
                        else:
                            # Handle empty values.
                            if u'' in selectedcontent:
                                samplenode.removeChild(variablenode)
                                continue
                                
        #
        self._main_activity.updateCurrentData()    

