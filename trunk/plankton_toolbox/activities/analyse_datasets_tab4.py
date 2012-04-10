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

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
#import datetime
import copy
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
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
        self.__select_stations_model.clear()
        self.__selected_minmaxdepth_model.clear()
#        self.__selected_taxon_model.clear()
        self.__selected_trophy_model.clear()
        
    def update(self):
        """ """
        self.clear()        
        self.__updateSelectDataAlternatives()
        
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
        stations_listview = QtGui.QListView()
        stations_listview.setMaximumHeight(100)
        self.__select_stations_model = QtGui.QStandardItemModel()
        stations_listview.setModel(self.__select_stations_model)
#        stations_listview.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        # Min-max depth.
        minmaxdepth_listview = QtGui.QListView()
        minmaxdepth_listview.setMaximumHeight(100)
        self.__selected_minmaxdepth_model = QtGui.QStandardItemModel()
        minmaxdepth_listview.setModel(self.__selected_minmaxdepth_model)
        # Trophy.
        trophy_listview = QtGui.QListView()
        trophy_listview.setMaximumHeight(100)
        self.__selected_trophy_model = QtGui.QStandardItemModel()
        trophy_listview.setModel(self.__selected_trophy_model)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Date from:")
        label2 = QtGui.QLabel("Stations:")
        label3 = QtGui.QLabel("Min-max depth:")
        label4 = QtGui.QLabel("Trophy:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(label3, gridrow, 4, 1, 3)
        form1.addWidget(label4, gridrow, 7, 1, 3)
        gridrow += 1
        form1.addWidget(self.__startdate_edit, gridrow, 0, 1, 1)
        form1.addWidget(stations_listview, gridrow, 1, 4, 3)
        form1.addWidget(minmaxdepth_listview, gridrow, 4, 4, 3)
        form1.addWidget(trophy_listview, gridrow, 7, 4, 3)
        gridrow += 1
        label1 = QtGui.QLabel("Date to:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self.__enddate_edit, gridrow, 0, 1, 1)
        gridrow += 1
        gridrow += 1
        label1 = utils_qt.ClickableQLabel("Clear all") # TODO:
        label2 = utils_qt.ClickableQLabel("Mark all") # TODO:
        label3 = utils_qt.ClickableQLabel("Clear all") # TODO:
        label4 = utils_qt.ClickableQLabel("Mark all") # TODO:
        label5 = utils_qt.ClickableQLabel("Clear all") # TODO:
        label6 = utils_qt.ClickableQLabel("Mark all") # TODO:
        form1.addWidget(label1, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(label4, gridrow, 5, 1, 1)
        form1.addWidget(label5, gridrow, 7, 1, 1)
        form1.addWidget(label6, gridrow, 8, 1, 1)
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
                    trophyset.add(variablenode.getData(u'Trophy'))
        #
        stationlist = sorted(stationset)
        minmaxdepthlist = sorted(minmaxdepthset)
        trophylist = sorted(trophyset)
        #
        # Start date and end date.
        self.__startdate_edit.setText(startdate)
        self.__enddate_edit.setText(enddate)
        # Stations.
        self.__select_stations_model.clear()        
        for station in stationlist:
            item = QtGui.QStandardItem(station)
            item.setCheckState(QtCore.Qt.Checked)
            item.setCheckable(True)
            self.__select_stations_model.appendRow(item)
        # Min-max depth.
        self.__selected_minmaxdepth_model.clear()
        for minmaxdepth in minmaxdepthlist:
            item = QtGui.QStandardItem(minmaxdepth)
            item.setCheckState(QtCore.Qt.Checked)
            item.setCheckable(True)
            self.__selected_minmaxdepth_model.appendRow(item)
        # Trophy.
        self.__selected_trophy_model.clear()
        for trophy in trophylist:
            item = QtGui.QStandardItem(trophy)
            item.setCheckState(QtCore.Qt.Checked)
            item.setCheckable(True)
            self.__selected_trophy_model.appendRow(item)
            
            
        # TEST
        self. __checkSelectDataAlternatives()    


    def __checkSelectDataAlternatives(self):
        """ """        
        self._selected_start_date = None
        self._selected_end_date =None
        self._selected_stations = []
        self._selected_minmaxdepth = []
        self._selected_trophy = []

        # Start date and end date.
        self._selected_start_date = unicode(self.__startdate_edit.text())
        self._selected_end_date = unicode(self.__enddate_edit.text())
        # Stations.
        for rowindex in range(self.__select_stations_model.rowCount()):
            item = self.__select_stations_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self._selected_stations.append(unicode(item.text()))
        # Min-max depth.
        for rowindex in range(self.__selected_minmaxdepth_model.rowCount()):
            item = self.__selected_minmaxdepth_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self._selected_minmaxdepth.append(unicode(item.text()))
        # Trophy.
        for rowindex in range(self.__selected_trophy_model.rowCount()):
            item = self.__selected_trophy_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self._selected_trophy.append(unicode(item.text()))

        # TEST
        print('DEBUG: _selected_stations: ' + ', '.join(self._selected_stations))
        print('DEBUG: _selected_minmaxdepth: ' + ', '.join(self._selected_minmaxdepth))
        print('DEBUG: _selected_trophy: ' + ', '.join(self._selected_trophy))


