#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import toolbox_utils
import plankton_core

@toolbox_utils.singleton
class ScreeningManager(object):
    """ """
    def __init__(self,
                 codelist_filenames = ['toolbox_data/code_lists/screening_code_list.xlsx']):
        # Parameters.
        self._codelist_filenames = codelist_filenames 
        # Local storage.
        self._codelist = {} # Main dictionary.
        # Run (only done once because the class is declared as singleton).
        self._load_all_data()

    def get_code_types(self):
        """ """
        return self._codelist.keys() 
    
    def get_codes(self, code_type):
        """ """
        if code_type in self._codelist.keys():
            return self._codelist[code_type]
        return []
    
    def _clear(self):
        """ """
        self._codelist = {} # Main dictionary.

    def _load_all_data(self):
        """ """
        try:
            self._clear()
            # Create codelist from files.
            for excelfilename in self._codelist_filenames:
                self._load_code_lists(excelfilename)                
        #
        except Exception as e:
            toolbox_utils.Logging().error('Failed when loading code lists. Exception: ' + unicode(e))
#        # Used for DEBUG:
#        import locale
#        import codecs
#        import json
#        fileencoding = locale.getpreferredencoding()
#        out = codecs.open('DEBUG_codelist.txt', mode = 'w', encoding = fileencoding)
#        out.write(json.dumps(self._codelist, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()
#        # end DEBUG.
        
    def _load_code_lists(self, excel_file_name):
        """ """
        # Get data from Excel file.
        tabledataset = plankton_core.DatasetTable()
        toolbox_utils.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.get_rows():
            codetype = row[0]
            # Internally code types are lowercase and words are separated by underscore.
            codetype = codetype.lower().replace(' ', '_')
            code = row[1]
            #
            if codetype:
                if codetype not in self._codelist:
                    self._codelist[codetype] = []
                self._codelist[codetype].append(code)

    def code_list_screening(self, datasets):
        """ """
        # Checked code types should be returned to caller.
        checked_codetypes_set = set()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.get_children():
                #
                data_dict = visitnode.get_data_dict()
                for key in data_dict:
                    if key in self.get_code_types():
                        checked_codetypes_set.add(key)
                        if data_dict[key] not in self.get_codes(key):
                            toolbox_utils.Logging().warning('Visit level. Code is not valid.  Code type: ' + unicode(key) + '  Code: ' + unicode(data_dict[key]))
                #
                for samplenode in visitnode.get_children():
                    #
                    data_dict = samplenode.get_data_dict()
                    for key in data_dict:
                        if key in self.get_code_types():
                            checked_codetypes_set.add(key)
                            if data_dict[key] not in self.get_codes(key):
                                toolbox_utils.Logging().warning('Sample level. Code is not valid.  Code type: ' + unicode(key) + '  Code: ' + unicode(data_dict[key]))
                    #                        
                    for variablenode in samplenode.get_children():
                        #
                        data_dict = variablenode.get_data_dict()
                        for key in data_dict:
                            if key in self.get_code_types():
                                checked_codetypes_set.add(key)
                                if data_dict[key] not in self.get_codes(key):
                                    toolbox_utils.Logging().warning('Variable level. Code is not valid.  Code type: ' + unicode(key) + '  Code: ' + unicode(data_dict[key]))
        # Returns set of checked code types.
        return checked_codetypes_set

    def species_screening(self, datasets):
        """ """
        species = plankton_core.Species()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.get_children():
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        data_dict = variablenode.get_data_dict()
                        if 'scientific_name' in data_dict:
                            if data_dict['scientific_name'] not in species.get_taxa_lookup_dict():
                                toolbox_utils.Logging().warning('Taxon name not in species list.  Taxon name: ' + unicode(data_dict['scientific_name']))
     
    def bvol_species_screening(self, datasets):
        """ """
        species = plankton_core.Species()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.get_children():
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        data_dict = variablenode.get_data_dict()
                        if ('scientific_name' in data_dict) and ('size_class' in data_dict):
                            taxonname = data_dict['scientific_name']
                            sizeclass = data_dict['size_class'] 
                            
                            if species.get_bvol_value(taxonname, sizeclass, 'bvol_size_class') == None:
                                toolbox_utils.Logging().warning('Taxon name/size clas not in BVOL list.  Taxon name: ' + unicode(taxonname) + '  Size class: ' + unicode(sizeclass))
     

