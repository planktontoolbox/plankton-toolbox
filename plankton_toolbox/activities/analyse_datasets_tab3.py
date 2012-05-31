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
import plankton_toolbox.toolbox.utils_qt as utils_qt
import envmonlib

@envmonlib.singleton
class AnalyseDatasetsTab3(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity

    def clear(self):
        """ """
        self._trophy_listview.clear()
        
    def update(self):
        """ """
        self.clear()        
        self._updateSelectDataAlternatives()
        
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
        # Aggregate over taxonomic rank.
        self._aggregate_rank_list = QtGui.QComboBox()
        self._aggregate_rank_list.addItems([
            "Biota",
            "Kingdom",
            "Phylum",
            "Class",
            "Order",
            "Family",
            "Genus",
            "Species" ])
        self._aggregate_rank_list.setCurrentIndex(3) # Default: Class
        #  Aggregate over trophy.
        self._trophy_listview = utils_qt.SelectableQListView()
        self._trophy_listview.setMaximumHeight(80)
        # Button.
        self._aggregatedata_button = QtGui.QPushButton("Aggregate data")
        self.connect(self._aggregatedata_button, QtCore.SIGNAL("clicked()"), self._aggregateData)                
        self._addmissingtaxa_button = QtGui.QPushButton("Add missing taxa in each sample")
        self.connect(self._addmissingtaxa_button, QtCore.SIGNAL("clicked()"), self._addMissingTaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Aggregate over:")
        form1.addWidget(label1, gridrow, 0, 1, 4)
        gridrow += 1
        label1 = QtGui.QLabel("Taxon level (rank):               ")
        label2 = QtGui.QLabel("Trophy:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(QtGui.QLabel(""), gridrow, 2, 1, 6) # Stretch.
        gridrow += 1
        form1.addWidget(self._aggregate_rank_list, gridrow, 0, 1, 1)
        form1.addWidget(self._trophy_listview, gridrow, 1, 4, 3)
        gridrow += 4
        form1.addWidget(self._aggregatedata_button, gridrow, 3, 1, 1)
        form1.addWidget(self._addmissingtaxa_button, gridrow, 10, 1, 1)
        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self._aggregatedata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
#        layout.addStretch(5)
#        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _aggregateData(self):
        """ """
        try:
#            if self._aggregate_rank_list.currentIndex() == 0:
#                envmonlib.Logging().log("Taxon level is not selected. Please try again.")
#                raise UserWarning("Taxon level is not selected. Please try again.")
            if not self._main_activity.getCurrentData():
                envmonlib.Logging().log("No data is selected for analysis. Please try again.")
                raise UserWarning("No data is selected for analysis. Please try again.")                
            #
            selected_taxon_rank = unicode(self._aggregate_rank_list.currentText())
            selected_trophy_list = self._trophy_listview.getSelectedDataList()
            selected_trophy_text = u'-'.join(selected_trophy_list) 
            #
            for visitnode in self._main_activity.getCurrentData().getChildren(): 
                for samplenode in visitnode.getChildren():
                    aggregatedvariables = {}
                    for variablenode in samplenode.getChildren():
                        value = variablenode.getData(u'Value')
                        # Use values containing valid float data.
                        try:
                            value = value.replace(u',', u'.').replace(u' ', u'', 100)
                            value = float(value) 
                            #
                            if selected_taxon_rank == u'Biota':
                                newtaxon = u'Biota' # Biota is above kingdom in the taxonomic hierarchy. 
                            else:
                                newtaxon = variablenode.getData(selected_taxon_rank) # Get taxon name for the selected rank.
                            #
                            taxontrophy = variablenode.getData(u'Trophy')
                            if taxontrophy in selected_trophy_list:
                                taxontrophy = selected_trophy_text # Concatenated string of ranks.
                            else:
                                continue # New: Use selected trophy only, don't use others.  
                            #
                            parameter = variablenode.getData(u'Parameter')
                            unit = variablenode.getData(u'Unit')
                            
                            agg_tuple = (newtaxon, taxontrophy, parameter, unit)
                            if agg_tuple in aggregatedvariables:
                                aggregatedvariables[agg_tuple] = value + aggregatedvariables[agg_tuple]
                            else:
                                aggregatedvariables[agg_tuple] = value
                        except:
                            if variablenode.getData(u'Value'):
                                print('DEBUG: Value not valid float: ' + unicode(variablenode.getData(u'Value')))
                    #Remove all variables for this sample.
                    samplenode.removeAllChildren()
                    # Add the new aggregated variables instead.  
                    for variablekeytuple in aggregatedvariables:
                        newtaxon, taxontrophy, parameter, unit = variablekeytuple
                        #
                        newvariable = envmonlib.VariableNode()
                        samplenode.addChild(newvariable)    
                        #
                        newvariable.addData(u'Taxon name', newtaxon)
                        newvariable.addData(u'Trophy', taxontrophy)
                        newvariable.addData(u'Parameter', parameter)
                        newvariable.addData(u'Unit', unit)
                        newvariable.addData(u'Value', aggregatedvariables[variablekeytuple])
            #
            self._main_activity.updateCurrentData()    
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

    def _updateSelectDataAlternatives(self):
        """ """
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:
            return # Empty data.
        #
        trophyset = set()
        #
        for visitnode in currentdata.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    trophyset.add(variablenode.getData(u'Trophy'))
        # Selection lists.
        self._trophy_listview.setList(sorted(trophyset))
            
    def _addMissingTaxa(self):
        """ """
        try:
            currentdata = self._main_activity.getCurrentData()
            if not currentdata:        
                return
            # Step 1: Create lists of taxa (name and trophy) and parameters (parameter and unit).
            parameter_set = set()
            taxon_set = set()
            for visitnode in currentdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameter = variablenode.getData(u"Parameter")
                        unit = variablenode.getData(u"Unit")
                        if parameter:
                            parameter_set.add((parameter, unit))
                        taxonname = variablenode.getData(u"Taxon name")
                        trophy = variablenode.getData(u"Trophy")
                        if taxonname:
                            taxon_set.add((taxonname, trophy))
            # Step 2: Create list with parameter-taxon pairs.
            parameter_taxon_list = []
            for parameterpair in parameter_set:
                for taxonpair in taxon_set:
                    parameter_taxon_list.append((parameterpair, taxonpair))
            # Step 3: Iterate over samples. 
            parameter_set = set()
            taxon_set = set()
            #
            for visitnode in currentdata.getChildren():
                #
                for samplenode in visitnode.getChildren():
                    sample_parameter_taxon_list = []
                    for variablenode in samplenode.getChildren():
                        parameter = variablenode.getData(u"Parameter")
                        unit = variablenode.getData(u"Unit")
                        taxon = variablenode.getData(u"Taxon name")
                        trophy = variablenode.getData(u"Trophy")
                        sample_parameter_taxon_list.append(((parameter, unit), (taxon, trophy)))
                    # Add missing variables.
                    for itempairs in parameter_taxon_list:
                        if itempairs not in sample_parameter_taxon_list:
                            variable = envmonlib.VariableNode()
                            samplenode.addChild(variable)
                            variable.addData(u"Taxon name", itempairs[1][0])
                            variable.addData(u"Trophy", itempairs[1][1])
                            variable.addData(u"Parameter", itempairs[0][0])
                            variable.addData(u"Value", u'0.0')
                            variable.addData(u"Unit", itempairs[0][1])
            #
            self._main_activity.updateCurrentData()    
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

