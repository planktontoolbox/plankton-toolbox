#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

from SOAPpy import WSDL

import table_file_reader

class WormsMarineSpecies(object):
    """ """
    def __init__(self):
        """ """
    def find_valid_taxon(self, scientific_name):
        """ """
        taxa = self.get_aphia_records(scientific_name, 
                                      param_like='false', 
                                      fuzzy='false',
                                      marine_only='false', 
                                      offset = 1,
                                            )
        accepted_taxon = None
        for taxon in taxa:
            print(taxon['scientificname'])
#             if self._get_value(taxon, 'status') == 'accepted':
#                 accepted_taxon = taxon
#                 
#                 break
#         
        return accepted_taxon

    def create_worms_dict(self, scientific_name, 
                                aphia_id = None):
        """ """
        worms_dict = {}        
        # GetAphia ID.
        if aphia_id is None:
            aphia_id = self.get_aphia_id(scientific_name, marine_only = 'false')
        #
        if not aphia_id:
            return worms_dict
        #          
        # Aphia record.
        aphia_dict = self.get_aphia_record_by_id(aphia_id)
        if not aphia_dict:
            return worms_dict           
        #
        worms_dict['worms_status'] = self._get_value(aphia_dict, 'status')
        worms_dict['worms_unaccept_reason'] = self._get_value(aphia_dict, 'unacceptreason')

        worms_dict['worms_valid name'] = self._get_value(aphia_dict, 'valid_name')
        worms_dict['worms_valid authority'] = self._get_value(aphia_dict, 'valid_authority')

        worms_dict['worms_rank'] = self._get_value(aphia_dict, 'rank')

        worms_dict['worms_kingdom'] = self._get_value(aphia_dict, 'kingdom')
        worms_dict['worms_phylum'] = self._get_value(aphia_dict, 'phylum')
        worms_dict['worms_class'] = self._get_value(aphia_dict, 'class')
        worms_dict['worms_order'] = self._get_value(aphia_dict, 'order')
        worms_dict['worms_family'] = self._get_value(aphia_dict, 'family')
        worms_dict['worms_genus'] = self._get_value(aphia_dict, 'genus')
        worms_dict['worms_sscientific name'] = self._get_value(aphia_dict, 'scientificname')
        worms_dict['worms_authority'] = self._get_value(aphia_dict, 'authority')

        worms_dict['worms_url'] = self._get_value(aphia_dict, 'url')
        worms_dict['worms_lsid'] = self._get_value(aphia_dict, 'lsid')
        worms_dict['worms_aphia_id'] = self._get_value(aphia_dict, 'AphiaID')
        worms_dict['worms_valid_aphia_id'] = self._get_value(aphia_dict, 'valid_AphiaID')
        
        worms_dict['worms_citation'] = self._get_value(aphia_dict, 'citation')
        
        # Classification.
        classification_string = ''
        classification = self.get_aphia_classification_by_id(aphia_id)
        if classification:    
            classification_string = unicode(classification.rank) + ': ' + unicode(classification.scientificname)
            while classification.child:
                classification = classification.child
                if (classification.rank and classification.scientificname):
                    classification_string += ' - ' + unicode(classification.rank) + ': ' + unicode(classification.scientificname)        
        worms_dict['worms_classification'] = classification_string
        
        # Synonyms.
        synonym_list = []
        synonyms = self.get_aphia_synonyms_by_id(aphia_id)
        if synonyms:
            for synonym in synonyms:
                if (synonym.scientificname and synonym.authority):
                    synonym_list.append(unicode(synonym.scientificname) + ' ' + unicode(synonym.authority))
        worms_dict['worms_synonym_list'] = synonym_list
        #        
        return worms_dict


class WormsWebservice(object):
    """ Calls to the web service at WoRMS, World Register of Marine Species.
        More info at: http://www.marinespecies.org/aphia.php?p=webservice. 
    """
    def __init__(self):
        """ """
        self._wsdl_object = WSDL.Proxy('http://www.marinespecies.org/aphia.php?p=soap&wsdl=1')
        
    def get_aphia_id(self, scientific_name,
                           marine_only = 'false'):
        """ Get the (first) exact matching AphiaID for a given name.
            Parameters:
                marine_only: limit to marine taxa. Default=true.
        """
        aphia_id = self._wsdl_object.getAphiaID(scientific_name, 
                                         marine_only)
        return aphia_id # Integer.

    def get_aphia_records(self, scientific_name, 
                                like = 'false', # Exact match by default.
                                fuzzy = 'false', # Exact match by default.
                                marine_only = 'false', # Brackish species wanted.
                                offset = 1): # Note: Iterate if len(aphia_records) = 50.
        """ Get one or more matching (max. 50) AphiaRecords for a given name.
            Parameters:
                like: add a '%'-sign added after the ScientificName (SQL LIKE function). Default=true.
                fuzzy: fuzzy matching. Default=true.
                marine_only: limit to marine taxa. Default=true.
                offset: starting recordnumber, when retrieving next chunck of (50) records. Default=1.
        """
        aphia_records = self._wsdl_object.getAphiaRecords(scientific_name, 
                                              like, fuzzy, marine_only, offset)
        
        
        
        
        
        
        #### struct_as_a_dict = dict((key, getattr(struct, key)) for key in struct._keys())
        
        
        
        
        
        
        return aphia_records # AphiaRecords
        
    def get_aphia_name_by_id(self, aphia_id):
        """ Get the correct name for a given AphiaID. """
        scientific_name = self._wsdl_object.getAphiaNameByID(aphia_id)
        return unicode(scientific_name) # String

    def get_aphia_record_by_id(self, aphia_id):
        """ Get the complete Aphia Record for a given AphiaID. """
        aphia_record = self._wsdl_object.getAphiaRecordByID(aphia_id)
        return aphia_record # AphiaRecord
        
    def get_aphia_record_by_tsn(self, tns_id):
        """ Get the Aphia Record for a given TSN (ITIS Taxonomic Serial Number). """
        aphia_record = self._wsdl_object.getAphiaRecordByTSN(tns_id)
        return aphia_record # AphiaRecord.

    def get_aphia_records_by_names(self, scientific_names, 
                                         like = 'true', 
                                         fuzzy = 'true',
                                         marine_only = 'false'):
        """ For each given scientific name, try to find one or more AphiaRecords.
            This allows you to match multiple names in one call. Limited to 500 names at once for performance reasons. 
            Parameters:
                like: add a '%'-sign after the ScientificName (SQL LIKE function). Default=false.
                fuzzy: fuzzy matching. Default=true.
                marine_only: limit to marine taxa. Default=true.
        """
        aphia_records = self._wsdl_object.getAphiaRecordsByNames(
                                                    scientific_names,
                                                    like = 'false', # Exact match by default.
                                                    fuzzy= 'false', # Exact match by default.
                                                    marine_only= 'false', # Brackish species wanted.
                                                    )
        return aphia_records # Aphia matches.
        
    def get_aphia_records_by_vernacular(self, vernacular, 
                                              like = 'true', 
                                              offset = 1):
        """ Get one or more Aphia Records (max. 50) for a given vernacular.
            Parameters:
                like: add a '%'-sign before and after the input (SQL LIKE '%vernacular%' function). Default=false.
                offset: starting record number, when retrieving next chunck of (50) records. Default=1.
        """
        aphia_records = self._wsdl_object.getAphiaRecordsByVernacular(vernacular, like, offset)
        return aphia_records # AphiaRecords
        
    def get_aphia_classification_by_id(self, aphia_id):
        """ Get the complete classification for one taxon. This also includes any sub or super ranks. """
        classification = self._wsdl_object.getAphiaClassificationByID(aphia_id)
        return classification # Classification.

    def get_sources_by_aphia_id(self, aphia_id):
        """ Get one or more sources/references including links, for one AphiaID. """
        sources = self._wsdl_object.getSourcesByAphiaID(aphia_id)
        return sources # Sources.

    def get_aphia_synonyms_by_id(self, aphia_id):
        """ Get all synonyms for a given AphiaID. """
        aphia_records = self._wsdl_object.getAphiaSynonymsByID(aphia_id)
        return aphia_records # AphiaRecords.

    def get_aphia_vernaculars_by_id(self, aphia_id):
        """ Get all vernaculars for a given AphiaID. """
        vernaculars = self._wsdl_object.getAphiaVernacularsByID(aphia_id)
        return vernaculars # Vernaculars.

    def get_aphia_children_by_id(self, aphia_id, 
                                       offset = 1, 
                                       marine_only = 'false'):
        """ Get the direct children (max. 50) for a given AphiaID.
            Parameters:
                offset: starting record number, when retrieving next chunck of (50) records. Default=1.
                marine_only: limit to marine taxa. Default=true.
        """
        records = self._wsdl_object.getAphiaChildrenByID(aphia_id, offset, marine_only)
        return records # Aphia records.
       
    def get_value(self, worms_dict, key):
        """ Clean values by removing unwanted characters. """
        try:
            if worms_dict[key]:
                return unicode(worms_dict[key]).replace('\n', ' ').replace('\r', ' ') # Remove new lines.
        except:
            print('Error when reading WORMS value for: ' + key + '.')
        return ''



# ===== TEST =====
if __name__ == "__main__":
    """ Used for testing. """
    
    # Test WormsWebservice.
    worms_ws = WormsWebservice()
    
#     worms_result = worms_ws.get_aphia_id('Nitzschia frustulum')
#     print('\nget_aphia_id: ' + unicode(worms_result))
# 
#     worms_result = worms_ws.get_aphia_records('Ctenophora')
#     print('\nget_aphia_records: ' + unicode(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record._keys(): # Note: '_keys' for SOAPs structType.
#             print(key + ':' + unicode(record[key]))
# 
#     worms_result = worms_ws.get_aphia_name_by_id(145422)
#     print('\nget_aphia_name_by_id: ' + worms_result)
# 
#     worms_result = worms_ws.get_aphia_record_by_id(145422)
#     print('\nget_aphia_record_by_id: ' + unicode(worms_result))
#     for key in worms_result._keys(): # Note: '_keys' for SOAPs structType.
#         print(key + ':' + unicode(worms_result[key]))
# 
# #     worms_result = worms_ws.get_aphia_record_by_tsn('tns_id')
# #     print('\nget_aphia_record_by_tsn: ' + unicode(worms_result))
# 
#     worms_result = worms_ws.get_aphia_records_by_names(['Nitzschia frustulum'])
#     print('\nget_aphia_records_by_names: ' + unicode(worms_result))
#     for record in worms_result:
#         for key in record._keys(): # Note: '_keys' for SOAPs structType.
#             print(key + ':' + unicode(record[key]))

#     worms_result = worms_ws.get_aphia_records_by_vernacular('vernacular') 
#     print('\nget_aphia_records_by_vernacular: ' + unicode(worms_result))

    worms_result = worms_ws.get_aphia_classification_by_id(145422)
    print('\nget_aphia_classification_by_id: ' + unicode(worms_result))
    for record in worms_result:
        for key in record._keys(): # Note: '_keys' for SOAPs structType.
            print(key + ':' + unicode(record[key]))

    worms_result = worms_ws.get_sources_by_aphia_id(145422)
    print('\nget_sources_by_aphia_id: ' + unicode(worms_result))

    worms_result = worms_ws.get_aphia_synonyms_by_id(145422)
    print('\nget_aphia_synonyms_by_id: ' + unicode(worms_result))
    for record in worms_result:
        for key in record._keys(): # Note: '_keys' for SOAPs structType.
            print(key + ':' + unicode(record[key]))

    worms_result = worms_ws.get_aphia_vernaculars_by_id(145422)
    print('\nget_aphia_vernaculars_by_id: ' + unicode(worms_result))
    for record in worms_result:
        for key in record._keys(): # Note: '_keys' for SOAPs structType.
            print(key + ':' + unicode(record[key]))

    worms_result = worms_ws.get_aphia_children_by_id(145422)
    print('\nget_aphia_children_by_id: ' + unicode(worms_result))
    for record in worms_result:
        for key in record._keys(): # Note: '_keys' for SOAPs structType.
            print(key + ':' + unicode(record[key]))
        
    # Test WormsMarineSpecies.
    
    marinespecies = WormsMarineSpecies
    marinespecies.find_valid_taxon('Ctenophora')
#    worms_dict = worms_ws.createWormsDictByScientificName('Nitzschia frustulum')
#    worms_dict = worms_ws.createWormsDictByScientificName('Nitzschia frustulum var. bulnheimiana')    
#     worms_dict = worms_ws.create_worms_dict('Herponema desmarestiae')
#     worms_dict = worms_ws.create_worms_dict('', aphia_id = 145422)
#     print('worms_dict: ')
#     for key in worms_dict.keys():
#         print(key + ':' + unicode(worms_dict[key]))

