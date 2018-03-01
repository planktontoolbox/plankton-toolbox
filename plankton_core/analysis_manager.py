#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import toolbox_utils
import plankton_core

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


    def clear_data(self):
        """ """
        self._data = None
        
    def set_data(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def get_data(self):
        """ """
        return self._data

    def clear_filter(self):
        """ """
        self._filter ={}
        
    def set_filter_item(self, key, value):
        """ """
        self._filter[key] = value        

    def get_filter_item(self, key):
        """ """
        return self._filter.get(key, '')        

    def get_filter_dict(self):
        """ """
        return self._filter

#     def load_datasets_by_name(self, datasets_names):
#         """ """
#         return self._analysisdata
    
    def copy_datasets_to_analysis_data(self, datasets):
        """ """
        # Clear analysis data.
        self.clear_data()
        
        analysis_dataset = plankton_core.DatasetNode()
            
        columnsinfo = self.create_export_table_info()
        analysis_dataset.set_export_table_columns(columnsinfo)
                    
        visit_items = ['visit_year', 'sample_date', 'visit_month', 'station_name', 'sample_latitude_dd', 'sample_longitude_dd', 'water_depth_m']
        sample_items = ['sample', 'sample_id', 'sample_min_depth_m', 'sample_max_depth_m'] 
        variable_items = ['variable', 'scientific_name', 'species_flag_code', 'size_class', 'trophic_type', 'parameter', 'value', 'unit', 'plankton_group', 'taxon_kingdom', 'taxon_phylum', 'taxon_class', 'taxon_order', 'variable', 'taxon_family', 'taxon_genus', 'taxon_hierarchy']
        
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                analysis_visit = plankton_core.VisitNode()
                analysis_dataset.add_child(analysis_visit)
                #
                for item in visit_items:
                    analysis_visit.add_data(item, visitnode.get_data(item, ''))    
                #
                for samplenode in visitnode.get_children():
                    analysis_sample = plankton_core.SampleNode()
                    analysis_visit.add_child(analysis_sample)    
                    #
                    for item in sample_items:
                        analysis_sample.add_data(item, samplenode.get_data(item, ''))    
                    #
                    for variablenode in samplenode.get_children():
                        analysis_variable = plankton_core.VariableNode()
                        analysis_sample.add_child(analysis_variable)    
                        #
                        for item in variable_items:
                            analysis_variable.add_data(item, variablenode.get_data(item, ''))    
                        #
        
        # Check.
        if (analysis_dataset == None) or (len(analysis_dataset.get_children()) == 0):
            toolbox_utils.Logging().log('Selected datasets are empty.')
            raise UserWarning('Selected datasets are empty.')
        # Use the concatenated dataset for analysis.
        self.set_data(analysis_dataset)    


#         # Clear analysis data.
#         self.clear_data()    
#         # Check if all the selected datasets contains the same columns.
#         compareheaders = None
#         for dataset in datasets:
#             if compareheaders == None:
#                 compareheaders = dataset.get_export_table_columns()
#             else:
#                 newheader = dataset.get_export_table_columns()
#                 if len(compareheaders)==len(newheader) and \
#                    all(compareheaders[i] == newheader[i] for i in range(len(compareheaders))):
#                     pass # OK since export columns are equal.
#                 else:
#                     toolbox_utils.Logging().log('Can\'t analyse datasets with different column names.')
#                     raise UserWarning('Can\'t analyse datasets with different export column names.')
#         # Concatenate selected datasets.        
#         analysis_dataset = None
#         for dataset in datasets:
#             if analysis_dataset == None:
#                 # Deep copy of the first dataset.
#                 analysis_dataset = copy.deepcopy(dataset)
#             else:
#                 # Append top node data and children. Start with a deep copy.
#                 tmp_dataset = copy.deepcopy(dataset)
#                 for key, value in analysis_dataset.get_data_dict().iteritems():
#                     analysis_dataset.add_data(key, value)
#                 for child in tmp_dataset.get_children():
#                     analysis_dataset.add_child(child)
#         # Check.
#         if (analysis_dataset == None) or (len(analysis_dataset.get_children()) == 0):
#             toolbox_utils.Logging().log('Selected datasets are empty.')
#             raise UserWarning('Selected datasets are empty.')
#         # Use the concatenated dataset for analysis.
#         self.set_data(analysis_dataset)    




    def create_export_table_info(self):
        """ Used in tree datasets. """
        
        parsing_info = [
            ['visit', 'visit_year', 'integer', 'visit_year', ''], 
            ['visit', 'sample_date', 'date', 'sample_date', ''], 
            ['visit', 'visit_month', 'integer', '', ''], # Calculate. Code below.
            ['visit', 'station_name', 'text', 'station_name', ''], 
            ['visit', 'sample_latitude_dd', 'float', 'sample_latitude_dd', ''], 
            ['visit', 'sample_longitude_dd', 'float', 'sample_longitude_dd', ''], 
            ['visit', 'water_depth_m', 'float', 'water_depth_m', ''],
            # 
            ['sample', 'sample_id', 'text', 'sample_id', ''], 
            ['sample', 'sample_min_depth_m', 'float', 'sample_min_depth_m', ''], 
            ['sample', 'sample_max_depth_m', 'float', 'sample_max_depth_m', ''], 
            #
            ['variable', 'scientific_name', 'text', 'scientific_name', ''], 
            ['variable', 'species_flag_code', 'text', 'species_flag_code', ''], 
            ['variable', 'size_class', 'text', 'size_class', ''], 
            ['variable', 'trophic_type', 'text', 'trophic_type_code', ''], 
            #
            ['variable', 'parameter', 'text', 'parameter', ''], 
            ['variable', 'value', 'float', 'value', ''], 
            ['variable', 'unit', 'text', 'unit', ''], 
            #
            ['variable', 'plankton_group', 'text', '', ''], # Calculate. Code below.
            ['variable', 'taxon_kingdom', 'text', 'taxon_kingdom', ''], 
            ['variable', 'taxon_phylum', 'text', 'taxon_phylum', ''], 
            ['variable', 'taxon_class', 'text', 'taxon_class', ''], 
            ['variable', 'taxon_order', 'text', 'taxon_order', ''], 
            ['variable', 'taxon_family', 'text', 'taxon_family', ''], 
            ['variable', 'taxon_genus', 'text', 'taxon_genus', ''], 
            ['variable', 'taxon_hierarchy', 'text', 'taxon_hierarchy', ''], 
#             #
#             ['variable', 'sampling_laboratory', 'text', 'sampling_laboratory_name_sv', ''], 
#             ['variable', 'analytical_laboratory', 'text', 'analytical_laboratory_name_sv', ''], 
        ]
        
        export_table_info = []
        for parsinginforow in parsing_info:
            nodelevel = parsinginforow[0]
            key = parsinginforow[1]
            viewformat = parsinginforow[2]
            exportheader = parsinginforow[4] if len(parsinginforow) > 4 else None
            if exportheader == '':
                exportheader = key # Empty string means copy internal key.
            if nodelevel in ['dataset', 'visit', 'sample', 'variable']:
                if exportheader:
                    export_table_info.append({'header': exportheader, 'node': nodelevel, 'key': key, 'view_format': viewformat}) 
        #
        return export_table_info
    
    def remove_data(self, selectedcolumn, selectedcontent):
        """ """        
        # Search for export column corresponding model element.
        for info_dict in self._data.get_export_table_columns():
            if info_dict['header'] == selectedcolumn:
                nodelevel = info_dict['node']
                key = info_dict['key']
                break # Break loop.
        #
        for visitnode in self._data.get_children()[:]:
            if nodelevel == 'visit':
                if key in visitnode.get_data_dict().keys():
                    if str(visitnode.get_data(key)) in selectedcontent:
                        self._data.remove_child(visitnode)
                        continue
                else:
                    # Handle empty keys.
                    if '' in selectedcontent:
                        self._data.remove_child(visitnode)
                        continue
            #
            for samplenode in visitnode.get_children()[:]:
                if nodelevel == 'sample':
                    if key in samplenode.get_data_dict().keys():
                        if str(samplenode.get_data(key)) in selectedcontent:
                            visitnode.remove_child(samplenode)
                            continue
                    else:
                        # Handle empty keys.
                        if '' in selectedcontent:
                            visitnode.remove_child(samplenode)
                            continue
                #
                for variablenode in samplenode.get_children()[:]:
                    if nodelevel == 'variable':
                        if key in variablenode.get_data_dict().keys():
                            if str(variablenode.get_data(key)) in selectedcontent:
                                samplenode.remove_child(variablenode)
                        else:
                            # Handle empty values.
                            if '' in selectedcontent:
                                samplenode.remove_child(variablenode)
                                continue

    def create_filtered_dataset(self):
        """ Used filter items are:
            - 'start_date'
            - 'end_date'
            - 'station'
            - 'visit_month'
            - 'visits': Contains <station_name> : <date>
            - 'min_max_depth_m': Contains <sample_min_depth_m>-<sample_max_depth_m>
            - 'scientific_name'
            - 'trophic_type'
            - 'life_stage'
        """
        # Create a tree dataset for filtered data.
        filtereddata = plankton_core.DatasetNode() 
        #
        analysisdata = self.get_data()
        if not analysisdata:        
            return filtereddata
        # Export info needed to convert from tree to table.
        filtereddata.set_export_table_columns(analysisdata.get_export_table_columns())        
        # Get selected data info.
        filter_startdate = self._filter['start_date']
        filter_enddate = self._filter['end_date']
        filter_stations = self._filter['stations']
        filter_visit_months = self._filter['visit_months']
        filter_visits = self._filter['visits']
        filter_minmaxdepth =  self._filter['min_max_depth_m']
        filter_taxon = self._filter['scientific_name']
        filter_trophic_type = self._filter['trophic_type']
        filter_lifestage = self._filter['life_stage']
        #
        for visitnode in analysisdata.get_children():
            if filter_startdate > visitnode.get_data('sample_date'):
                continue
            if filter_enddate < visitnode.get_data('sample_date'):
                continue
            if visitnode.get_data('station_name') not in filter_stations:
                continue
            if visitnode.get_data('visit_month') not in filter_visit_months:
                continue
            if (str(visitnode.get_data('station_name')) + ' : ' + 
                str(visitnode.get_data('sample_date'))) not in filter_visits:
                continue
            # Create node and copy node data.            
            filteredvisit = plankton_core.VisitNode()
            filteredvisit.set_data_dict(visitnode.get_data_dict())
            filtereddata.add_child(filteredvisit)    
            #
            for samplenode in visitnode.get_children():
                minmax = str(samplenode.get_data('sample_min_depth_m')) +  '-' + \
                         str(samplenode.get_data('sample_max_depth_m'))
                if minmax not in filter_minmaxdepth:
                    continue
                #
                # Create node and copy node data.            
                filteredsample = plankton_core.SampleNode()
                filteredsample.set_data_dict(samplenode.get_data_dict())
                filteredvisit.add_child(filteredsample)    
                #
                for variablenode in samplenode.get_children():
                    if variablenode.get_data('scientific_name') not in filter_taxon:
                        continue
                    #
                    if variablenode.get_data('trophic_type') not in filter_trophic_type:
                        continue
                    #
                    lifestage = variablenode.get_data('stage')
                    if variablenode.get_data('sex'):
                        lifestage += '/' + variablenode.get_data('sex')
                    if lifestage not in filter_lifestage:
                        continue
                    # Create node and copy node data.            
                    filteredvariable = plankton_core.VariableNode()
                    filteredvariable.set_data_dict(variablenode.get_data_dict())
                    filteredsample.add_child(filteredvariable)
        #
        return filtereddata    

class AnalysisPrepare(object):
    """
    """
    def __init__(self):
        """ """
        # Initialize parent.
        super(AnalysisPrepare, self).__init__()


    def add_missing_taxa(self, analysisdata):
        """ """
        if not analysisdata:        
            return
        # Step 1: Create lists of taxa (name, trophic_type, stage and sex) and parameters (parameter and unit).
        parameter_set = set()
        taxon_set = set()
        for visitnode in analysisdata.get_children():
            for samplenode in visitnode.get_children():
                for variablenode in samplenode.get_children():
                    parameter = variablenode.get_data('parameter')
                    unit = variablenode.get_data('unit')
                    if parameter:
                        parameter_set.add((parameter, unit))
                    taxonname = variablenode.get_data('scientific_name')
                    trophic_type = variablenode.get_data('trophic_type')
                    stage = variablenode.get_data('stage')
                    sex = variablenode.get_data('sex')
                    if taxonname:
                        taxon_set.add((taxonname, trophic_type, stage, sex))
        # Step 2: Create list with parameter-taxon pairs.
        parameter_taxon_list = []
        for parameterpair in parameter_set:
            for taxonpair in taxon_set:
                parameter_taxon_list.append((parameterpair, taxonpair))
        # Step 3: Iterate over samples. 
        parameter_set = set()
        taxon_set = set()
        #
        for visitnode in analysisdata.get_children():
            #
            for samplenode in visitnode.get_children():
                sample_parameter_taxon_list = []
                for variablenode in samplenode.get_children():
                    parameter = variablenode.get_data('parameter')
                    unit = variablenode.get_data('unit')
                    taxon = variablenode.get_data('scientific_name')
                    trophic_type = variablenode.get_data('trophic_type')
                    stage = variablenode.get_data('stage')
                    sex = variablenode.get_data('sex')
                    sample_parameter_taxon_list.append(((parameter, unit), (taxon, trophic_type, stage, sex)))
                # Add missing variables.
                for itempairs in parameter_taxon_list:
                    if itempairs not in sample_parameter_taxon_list:
                        variable = plankton_core.VariableNode()
                        samplenode.add_child(variable)
                        variable.add_data('scientific_name', itempairs[1][0])
                        variable.add_data('trophic_type', itempairs[1][1])
                        variable.add_data('stage', itempairs[1][2])
                        variable.add_data('sex', itempairs[1][3])
                        variable.add_data('parameter', itempairs[0][0])
                        variable.add_data('value', float(0.0))
                        variable.add_data('unit', itempairs[0][1])


class StatisticalData(object):
    """
    Should contain table oriented data, see plankton_core.DatasetTable().
    """
    def __init__(self):
        """ """
        self._data = None
        # Initialize parent.
        super(StatisticalData, self).__init__()

    def clear_data(self):
        """ """
        self._data = None
        
    def set_data(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def get_data(self):
        """ """
        return self._data


class ReportData(object):
    """
    Should contain table oriented data, see plankton_core.DatasetTable().
    """
    def __init__(self):
        """ """
        self._data = None
        # Initialize parent.
        super(ReportData, self).__init__()

    def clear_data(self):
        """ """
        self._data = None
        
    def set_data(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def get_data(self):
        """ """
        return self._data

