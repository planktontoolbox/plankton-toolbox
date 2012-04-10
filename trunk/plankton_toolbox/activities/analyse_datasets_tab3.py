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
class AnalyseDatasetsTab3(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """

    def setMainActivity(self, analyse_dataset_activity):
        """ """
        self.__analysedatasetactivity = analyse_dataset_activity

    def clear(self):
        """ """
        
    def update(self):
        """ """
        
    # ===== TAB: Aggregate data ===== 
    def contentAggregateData(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)



        # Active widgets and connections.
        self.__aggregate_taxon_list = QtGui.QComboBox()
        #
        self.__aggregate_taxon_list.addItems([
            "<none>",
            "Class",
            "Order",
            "Family",
            "Species"
            ])
        self.__aggregatecurrentdata_button = QtGui.QPushButton("Aggregate current data")
        self.connect(self.__aggregatecurrentdata_button, QtCore.SIGNAL("clicked()"), self.__aggregateCurrentData)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(QtGui.QLabel("Aggregate over taxon level:"))
        hbox1.addWidget(self.__aggregate_taxon_list)
        hbox1.addWidget(self.__aggregatecurrentdata_button)
        
        
        
        
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addStretch(5)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def __aggregateCurrentData(self):
        """ """
        #
        for visitnode in self.__analysedatasetactivity.getCurrentData().getChildren(): 
            for samplenode in visitnode.getChildren():
                aggregatedvariables = {}
                for variablenode in samplenode.getChildren():
                    value = variablenode.getData(u'Value')
                    # Use values containing valid float data.
                    try:
                        value = float(value) 
                        taxonclass = variablenode.getData(u'Dyntaxa class')
                        taxontrophy = variablenode.getData(u'PEG trophy')
                        parameter = variablenode.getData(u'Parameter')
                        unit = variablenode.getData(u'Unit')
                        
                        agg_tuple = (taxonclass, taxontrophy, parameter, unit)
                        if agg_tuple in aggregatedvariables:
                            aggregatedvariables[agg_tuple] = value + aggregatedvariables[agg_tuple]
                        else:
                            aggregatedvariables[agg_tuple] = value
                    except:
                        print('DEBUG: Value not valid float.')
                #Remove all variables for this sample.
                samplenode.removeAllChildren()
                # Add the new aggregated variables instead.  
                for variablekeytuple in aggregatedvariables:
                    taxonclass, taxontrophy, parameter, unit = variablekeytuple
                    #
                    newvariable = mmfw.VariableNode()
                    samplenode.addChild(newvariable)    
                    #
                    newvariable.addData(u'Reported taxon name', taxonclass)
                    newvariable.addData(u'PEG trophy', taxontrophy)
                    newvariable.addData(u'Parameter', parameter)
                    newvariable.addData(u'Unit', unit)
                    newvariable.addData(u'Value', aggregatedvariables[variablekeytuple])
        #
        self.__analysedatasetactivity.updateCurrentData()    

