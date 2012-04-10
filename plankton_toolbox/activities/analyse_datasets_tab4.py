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

#import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
#import datetime
#import copy
#import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
#import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import mmfw

@mmfw.singleton
class AnalyseDatasetsTab4(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """

    def setMainActivity(self, analyse_dataset_activity):
        """ """
        self.__analysedatasetactivity = analyse_dataset_activity
                
    def clear(self):
        """ """
        self.__startdate_edit.clear()
        self.__enddate_edit.clear()
        self._stations_listview.clear()
        self._minmaxdepth_listview.clear()
        self._taxon_listview.clear()
        self._trophy_listview.clear()
        
    def update(self):
        """ """
        self.clear()        
        self.__updateSelectDataAlternatives()

    def getSelectDataDict(self):
        """ """
        selected_dict = {}        
        # Start date and end date.
        selected_dict[u'Start date'] = unicode(self.__startdate_edit.text())
        selected_dict[u'End date'] = unicode(self.__enddate_edit.text())
        # Selection lists.
        selected_dict[u'Stations'] = self._stations_listview.getSelectedDataList()
        selected_dict[u'Min max depth'] = self._minmaxdepth_listview.getSelectedDataList()
        selected_dict[u'Taxon'] = self._taxon_listview.getSelectedDataList()
        selected_dict[u'Trophy'] = self._trophy_listview.getSelectedDataList()
        # TEST
        print('DEBUG: Selected stations: ' + ', '.join(selected_dict[u'Stations']))
        print('DEBUG: Selected_min max depth: ' + ', '.join(selected_dict[u'Min max depth']))
        print('DEBUG: Selected taxon: ' + ', '.join(selected_dict[u'Taxon']))
        print('DEBUG: Selected trophy: ' + ', '.join(selected_dict[u'Trophy']))
        #
        return selected_dict
        
    # ===== TAB: Select data ===== 
    def contentSelectData(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        # Start date and end date.
        self.__startdate_edit = QtGui.QLineEdit("")
        self.__enddate_edit = QtGui.QLineEdit("")
        # Stations
        self._stations_listview = utils_qt.SelectableQListView()
        self._stations_listview.setMaximumHeight(100)
        # Min-max depth.
        self._minmaxdepth_listview = utils_qt.SelectableQListView()
        self._minmaxdepth_listview.setMaximumHeight(100)
        # Taxon.
        self._taxon_listview = utils_qt.SelectableQListView()
        self._taxon_listview.setMaximumHeight(100)
        # Trophy.
        self._trophy_listview = utils_qt.SelectableQListView()
        self._trophy_listview.setMaximumHeight(100)
        #
        clicklabel1 = utils_qt.ClickableQLabel("Clear all") # TODO:
        clicklabel2 = utils_qt.ClickableQLabel("Mark all") # TODO:
        clicklabel3 = utils_qt.ClickableQLabel("Clear all") # TODO:
        clicklabel4 = utils_qt.ClickableQLabel("Mark all") # TODO:
        clicklabel5 = utils_qt.ClickableQLabel("Clear all") # TODO:
        clicklabel6 = utils_qt.ClickableQLabel("Mark all") # TODO:
        clicklabel7 = utils_qt.ClickableQLabel("Clear all") # TODO:
        clicklabel8 = utils_qt.ClickableQLabel("Mark all") # TODO:
        self.connect(clicklabel1, QtCore.SIGNAL("clicked()"), self._stations_listview.uncheckAll)                
        self.connect(clicklabel2, QtCore.SIGNAL("clicked()"), self._stations_listview.checkAll)                
        self.connect(clicklabel3, QtCore.SIGNAL("clicked()"), self._minmaxdepth_listview.uncheckAll)                
        self.connect(clicklabel4, QtCore.SIGNAL("clicked()"), self._minmaxdepth_listview.checkAll)                
        self.connect(clicklabel5, QtCore.SIGNAL("clicked()"), self._taxon_listview.uncheckAll)                
        self.connect(clicklabel6, QtCore.SIGNAL("clicked()"), self._taxon_listview.checkAll)                
        self.connect(clicklabel7, QtCore.SIGNAL("clicked()"), self._trophy_listview.uncheckAll)                
        self.connect(clicklabel8, QtCore.SIGNAL("clicked()"), self._trophy_listview.checkAll)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Date from:")
        label2 = QtGui.QLabel("Stations:")
        label3 = QtGui.QLabel("Min-max depth:")
        label4 = QtGui.QLabel("Taxon:")
        label5 = QtGui.QLabel("Trophy:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(label3, gridrow, 4, 1, 3)
        form1.addWidget(label4, gridrow, 7, 1, 3)
        form1.addWidget(label5, gridrow, 10, 1, 3)
        gridrow += 1
        form1.addWidget(self.__startdate_edit, gridrow, 0, 1, 1)
        form1.addWidget(self._stations_listview, gridrow, 1, 4, 3)
        form1.addWidget(self._minmaxdepth_listview, gridrow, 4, 4, 3)
        form1.addWidget(self._taxon_listview, gridrow, 7, 4, 3)
        form1.addWidget(self._trophy_listview, gridrow, 10, 4, 3)
        gridrow += 1
        label1 = QtGui.QLabel("Date to:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self.__enddate_edit, gridrow, 0, 1, 1)
        gridrow += 1
        gridrow += 1
        form1.addWidget(clicklabel1, gridrow, 1, 1, 1)
        form1.addWidget(clicklabel2, gridrow, 2, 1, 1)
        form1.addWidget(clicklabel3, gridrow, 4, 1, 1)
        form1.addWidget(clicklabel4, gridrow, 5, 1, 1)
        form1.addWidget(clicklabel5, gridrow, 7, 1, 1)
        form1.addWidget(clicklabel6, gridrow, 8, 1, 1)
        form1.addWidget(clicklabel7, gridrow, 10, 1, 1)
        form1.addWidget(clicklabel8, gridrow, 11, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget


    def __updateSelectDataAlternatives(self):
        """ """
        currentdata = self.__analysedatasetactivity.getCurrentData()
        if not currentdata:
            return # Empty data.
        #
        startdate = '9999-99-99'
        enddate = '0000-00-00'
        stationset = set()
        minmaxdepthset = set()
        taxonset = set()
        trophyset = set()
        #
        for visitnode in currentdata.getChildren():
            stationset.add(visitnode.getData(u'Station.reported name'))
            startdate = min(startdate, visitnode.getData(u'Date'))
            enddate = max(enddate, visitnode.getData(u'Date'))
            for samplenode in visitnode.getChildren():
                depthstring = samplenode.getData(u'Sample min depth') + '-' + samplenode.getData(u'Sample max depth')
                minmaxdepthset.add(depthstring)
                for variablenode in samplenode.getChildren():
                    taxonset.add(variablenode.getData(u'Reported taxon name'))
                    trophyset.add(variablenode.getData(u'PEG trophy'))
        # Start date and end date.
        self.__startdate_edit.setText(startdate)
        self.__enddate_edit.setText(enddate)
        # Selection lists.
        self._stations_listview.setList(sorted(stationset))
        self._minmaxdepth_listview.setList(sorted(minmaxdepthset))
        self._taxon_listview.setList(sorted(taxonset))
        self._trophy_listview.setList(sorted(trophyset))
            
        # TEST
        self.getSelectDataDict()    

