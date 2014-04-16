#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

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
        self._filter = {}
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

    def clearFilter(self):
        """ """
        self._filter ={}
        
    def setFilterItem(self, key, value):
        """ """
        self._filter[key] = value        

    def getFilterItem(self, key):
        """ """
        return self._filter.get(key, u'')        

    def getFilterDict(self):
        """ """
        return self._filter

#     def loadDatasetsByName(self, datasets_names):
#         """ """
#         return self._analysisdata
    
    def copyDatasetsToAnalysisData(self, datasets):
        """ """
        # Clear analysis data.
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
                for key, value in analysis_dataset.getDataDict().iteritems():
                    analysis_dataset.addData(key, value)
                for child in tmp_dataset.getChildren():
                    analysis_dataset.addChild(child)
        # Check.
        if (analysis_dataset == None) or (len(analysis_dataset.getChildren()) == 0):
            envmonlib.Logging().log("Selected datasets are empty.")
            raise UserWarning("Selected datasets are empty.")
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

    def createFilteredDataset(self):
        """ Used filter items are:
            - 'start_date'
            - 'end_date'
            - 'visits': Contains <station_name> : <date>
            - 'min_max_depth': Contains <sample_min_depth>-<sample_max_depth>
            - 'taxon'
            - 'trophy'
            - 'life_stage'
        """
        # Create a tree dataset for filtered data.
        filtereddata = envmonlib.DatasetNode() 
        #
        analysisdata = self.getData()
        if not analysisdata:        
            return filtereddata
        # Export info needed to convert from tree to table.
        filtereddata.setExportTableColumns(analysisdata.getExportTableColumns())        
        # Get selected data info.
        filter_startdate = self._filter[u'start_date']
        filter_enddate = self._filter[u'end_date']
#        filter_stations = self._filte[u'Stations']
        filter_visits = self._filter[u'visits']
        filter_minmaxdepth =  self._filter[u'min_max_depth']
        filter_taxon = self._filter[u'taxon']
        filter_trophy = self._filter[u'trophy']
        filter_lifestage = self._filter[u'life_stage']
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
                    if variablenode.getData(u'scientific_name') not in filter_taxon:
                        continue
                    #
                    if variablenode.getData(u'trophy') not in filter_trophy:
                        continue
                    #
                    lifestage = variablenode.getData(u'stage')
                    if variablenode.getData(u'sex'):
                        lifestage += u'/' + variablenode.getData(u'sex')
                    if lifestage not in filter_lifestage:
                        continue
                    # Create node and copy node data.            
                    filteredvariable = envmonlib.VariableNode()
                    filteredvariable.setDataDict(variablenode.getDataDict())
                    filteredsample.addChild(filteredvariable)
        #
        return filtereddata    

