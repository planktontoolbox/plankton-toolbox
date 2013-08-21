#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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

import copy

import envmonlib

class AnalysisData(object):
    """
    Contains a concatenated dataset for analysis. Main steps when working with analysis are:
    - Load datasets to the concatenated dataset.
    - Clean up data, i.e. remove values with bad quality, etc. This will remove data from the 
      concatenated dataset.
    - Filter data. This will not affect the concatenated dataset, it just creates a temporary 
      filtered dataset.
      
    Note: Other actions, for example aggregation over taxonomical level are not handled here.
    """
    def __init__(self):
        """ """
        # Tree dataset used for analysis. 
        self._data = None
        # Initialize parent.
        super(AnalysisData, self).__init__()


    def clearData(self):
        """ """
        self._data = None
        
    def setData(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def getData(self):
        """ """
        return self._data
    
#     def loadDatasetsByName(self, datasets_names):
#         """ """
#         return self._currentdata
    
    def loadDatasets(self, datasets):
        """ """
        # Clear current data.
        self.clearData()    
        # Check if all the selected datasets contains the same columns.
        compareheaders = None
        for dataset in datasets:
            if compareheaders == None:
                compareheaders = dataset.getExportTableColumns()
            else:
                newheader = dataset.getExportTableColumns()
                if len(compareheaders)==len(newheader) and \
                   all(compareheaders[i] == newheader[i] for i in range(len(compareheaders))):
                    pass # OK since export columns are equal.
                else:
                    envmonlib.Logging().log("Can't analyse datasets with different column names.")
                    raise UserWarning("Can't analyse datasets with different export column names.")
        # Concatenate selected datasets.        
        analysis_dataset = None
        for dataset in datasets:
            if analysis_dataset == None:
                # Deep copy of the first dataset.
                analysis_dataset = copy.deepcopy(dataset)
            else:
                # Append top node data and children. Start with a deep copy.
                tmp_dataset = copy.deepcopy(dataset)
                for key, value in analysis_dataset.getDataDict():
                    analysis_dataset.addData(key, value)
                for child in tmp_dataset.getChildren():
                    analysis_dataset.addChild(child)
        # Check.
        if (analysis_dataset == None) or (len(analysis_dataset.getChildren()) == 0):
            envmonlib.Logging().log("The selected datasets are empty.")
            raise UserWarning("The selected datasets are empty.")
        # Use the concatenated dataset for analysis.
        self.setData(analysis_dataset)    
    
    def removeData(self, selectedcolumn, selectedcontent):
        """ """        
        # Search for export column corresponding model element.
        for info_dict in self._data.getExportTableColumns():
            if info_dict[u'header'] == selectedcolumn:
                nodelevel = info_dict[u'node']
                key = info_dict[u'key']
                break # Break loop.
        #
        for visitnode in self._data.getChildren()[:]:
            if nodelevel == u'visit':
                if key in visitnode.getDataDict().keys():
                    if unicode(visitnode.getData(key)) in selectedcontent:
                        self._data.removeChild(visitnode)
                        continue
                else:
                    # Handle empty keys.
                    if u'' in selectedcontent:
                        self._data.removeChild(visitnode)
                        continue
            #
            for samplenode in visitnode.getChildren()[:]:
                if nodelevel == u'sample':
                    if key in samplenode.getDataDict().keys():
                        if unicode(samplenode.getData(key)) in selectedcontent:
                            visitnode.removeChild(samplenode)
                            continue
                    else:
                        # Handle empty keys.
                        if u'' in selectedcontent:
                            visitnode.removeChild(samplenode)
                            continue
                #
                for variablenode in samplenode.getChildren()[:]:
                    if nodelevel == u'variable':
                        if key in variablenode.getDataDict().keys():
                            if unicode(variablenode.getData(key)) in selectedcontent:
                                samplenode.removeChild(variablenode)
                        else:
                            # Handle empty values.
                            if u'' in selectedcontent:
                                samplenode.removeChild(variablenode)
                                continue

    def createFilteredDataset(self, filterdict):
        """ """
        # Create a tree dataset for filtered data.
        filtereddata = envmonlib.DatasetNode() 
        #
        analysisdata = self.getData()
        if not analysisdata:        
            return filtereddata
        # Export info needed to convert from tree to table.
        filtereddata.setExportTableColumns(analysisdata.getExportTableColumns())        
        # Get selected data info.
        filter_startdate = filterdict[u'start_date']
        filter_enddate = filterdict[u'end_date']
#        filter_stations = filterdict[u'Stations']
        filter_visits = filterdict[u'visits']
        filter_minmaxdepth =  filterdict[u'min_max_depth']
        filter_taxon = filterdict[u'taxon']
        filter_trophy = filterdict[u'trophy']
        #
        for visitnode in analysisdata.getChildren():
            if filter_startdate > visitnode.getData(u'date'):
                continue
            if filter_enddate < visitnode.getData(u'date'):
                continue
            if (unicode(visitnode.getData(u'station_name')) + u' : ' + 
                unicode(visitnode.getData(u'date'))) not in filter_visits:
                continue
            # Create node and copy node data.            
            filteredvisit = envmonlib.VisitNode()
            filteredvisit.setDataDict(visitnode.getDataDict())
            filtereddata.addChild(filteredvisit)    
            #
            for samplenode in visitnode.getChildren():
                minmax = unicode(samplenode.getData(u'sample_min_depth')) +  u'-' + \
                         unicode(samplenode.getData(u'sample_max_depth'))
                if minmax not in filter_minmaxdepth:
                    continue
                #
                # Create node and copy node data.            
                filteredsample = envmonlib.SampleNode()
                filteredsample.setDataDict(samplenode.getDataDict())
                filteredvisit.addChild(filteredsample)    
                #
                for variablenode in samplenode.getChildren():
                    if variablenode.getData(u'taxon_name') not in filter_taxon:
                        continue
                    if variablenode.getData(u'trophy') not in filter_trophy:
                        continue
                    # Create node and copy node data.            
                    filteredvariable = envmonlib.VariableNode()
                    filteredvariable.setDataDict(variablenode.getDataDict())
                    filteredsample.addChild(filteredvariable)
        #
        return filtereddata    

