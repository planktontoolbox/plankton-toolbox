#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).


# TODO: Activate this code later.


# from SOAPpy import WSDL
#
# class WormsWebservice(object):
#     """ SOAP calls to the web service at WoRMS, World Register of Marine Species.
#         More info at: http://www.marinespecies.org/aphia.php?p=webservice.
#     """
#     def __init__(self):
#         """ """
#         self._wsdl_object = WSDL.Proxy('http://www.marinespecies.org/aphia.php?p=soap&wsdl=1')
#
#     def get_aphia_id(self, scientific_name,
#                            marine_only = 'false'):
#         """ Get the (first) exact matching AphiaID for a given name.
#             Parameters:
#                 marine_only: limit to marine taxa. Default=true.
#         """
#         aphia_id = self._wsdl_object.getAphiaID(scientific_name,
#                                                 marine_only)
#         return aphia_id # Integer or None.
#
#     def get_aphia_records(self, scientific_name,
#                                 like = 'false', # Exact match by default.
#                                 fuzzy = 'false', # Exact match by default.
#                                 marine_only = 'false', # Brackish species wanted.
#                                 offset = 1): # Note: Iterate if len(aphia_records) = 50.
#         """ Get one or more matching (max. 50) AphiaRecords for a given name.
#             Parameters:
#                 like: add a '%'-sign added after the ScientificName (SQL LIKE function). Default=true.
#                 fuzzy: fuzzy matching. Default=true.
#                 marine_only: limit to marine taxa. Default=true.
#                 offset: starting recordnumber, when retrieving next chunck of (50) records. Default=1.
#         """
#         worms_records = self._wsdl_object.getAphiaRecords(scientific_name,
#                                               like, fuzzy, marine_only, offset)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if worms_records:
#             for aphia_record in worms_records:
#                 record = dict((key, getattr(aphia_record, key)) for key in aphia_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_aphia_name_by_id(self, aphia_id):
#         """ Get the correct name for a given AphiaID. """
#         scientific_name = self._wsdl_object.getAphiaNameByID(aphia_id)
#         return str(scientific_name) # String
#
#     def get_aphia_record_by_id(self, aphia_id):
#         """ Get the complete Aphia Record for a given AphiaID. """
#         worms_record = self._wsdl_object.getAphiaRecordByID(aphia_id)
#         # Convert from SOAPs structType to Python.
#         record = None
#         if worms_record:
#             record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#         #
#         return record
#
#     def get_aphia_record_by_ext_id(self, ext_id, ext_type = 'tsn'):
#         """ Get the Aphia Record for a given external identifier.
#             type: Should have one of the following values:
#                 'bold': Barcode of Life Database (BOLD) TaxID
#                 'dyntaxa': Dyntaxa ID
#                 'eol': Encyclopedia of Life (EoL) page identifier
#                 'fishbase': FishBase species ID
#                 'iucn': IUCN Red List Identifier
#                 'lsid': Life Science Identifier
#                 'ncbi': NCBI Taxonomy ID (Genbank)
#                 'tsn': ITIS Taxonomic Serial Number
#         """
#         worms_record = self._wsdl_object.getAphiaRecordByExtID(ext_id, ext_type)
#         # Convert from SOAPs structType to Python.
#         record = None
#         if worms_record:
#             record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#         #
#         return record
#
#     def get_aphia_records_by_names(self, scientific_names,
#                                          like = 'true',
#                                          fuzzy = 'true',
#                                          marine_only = 'false'):
#         """ For each given scientific name, try to find one or more AphiaRecords.
#             This allows you to match multiple names in one call. Limited to 500 names at once for performance reasons.
#             Parameters:
#                 like: add a '%'-sign after the ScientificName (SQL LIKE function). Default=false.
#                 fuzzy: fuzzy matching. Default=true.
#                 marine_only: limit to marine taxa. Default=true.
#         """
#         worms_records = self._wsdl_object.getAphiaRecordsByNames(
#                                                     scientific_names,
#                                                     like = 'false', # Exact match by default.
#                                                     fuzzy= 'false', # Exact match by default.
#                                                     marine_only= 'false', # Brackish species wanted.
#                                                     )
#         # Convert from SOAPs structType to Python.
#         name_records = []
#         if worms_records:
#             for name_record in worms_records:
#                 records = []
#                 for worms_record in name_record:
#                     record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                     records.append(record)
#                 name_records.append(records)
#         #
#         return name_records
#
#     def get_aphia_records_by_vernacular(self, vernacular,
#                                               like = 'true',
#                                               offset = 1):
#         """ Get one or more Aphia Records (max. 50) for a given vernacular.
#             Parameters:
#                 like: add a '%'-sign before and after the input (SQL LIKE '%vernacular%' function). Default=false.
#                 offset: starting record number, when retrieving next chunck of (50) records. Default=1.
#         """
#         worms_records = self._wsdl_object.getAphiaRecordsByVernacular(vernacular, like, offset)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if worms_records:
#             for worms_record in worms_records:
#                 record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_aphia_classification_by_id(self, aphia_id):
#         """ Get the complete classification for one taxon. This also includes any sub or super ranks. """
#         worms_classification = self._wsdl_object.getAphiaClassificationByID(aphia_id)
#         # Convert from SOAPs structType to Python. List instead of hierarchy.
#         records = []
#         if worms_classification:
#             child_record = worms_classification
#             while child_record['child'] != '':
#                 record = {}
#                 for key in child_record._keys():
#                     if key != 'child':
#                         record[key] = getattr(child_record, key)
#                 records.append(record)
#                 child_record = child_record['child']
#         #
#         return records # Classification as list of records.
#
#     def get_sources_by_aphia_id(self, aphia_id):
#         """ Get one or more sources/references including links, for one AphiaID. """
#         worms_sources = self._wsdl_object.getSourcesByAphiaID(aphia_id)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if worms_sources:
#             for worms_record in worms_sources:
#                 record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_aphia_synonyms_by_id(self, aphia_id):
#         """ Get all synonyms for a given AphiaID. """
#         worms_records = self._wsdl_object.getAphiaSynonymsByID(aphia_id)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if worms_records:
#             for worms_record in worms_records:
#                 record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_aphia_vernaculars_by_id(self, aphia_id):
#         """ Get all vernaculars for a given AphiaID. """
#         vernaculars = self._wsdl_object.getAphiaVernacularsByID(aphia_id)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if vernaculars:
#             for worms_record in vernaculars:
#                 record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_aphia_children_by_id(self, aphia_id,
#                                        offset = 1,
#                                        marine_only = 'false'):
#         """ Get the direct children (max. 50) for a given AphiaID.
#             Parameters:
#                 offset: starting record number, when retrieving next chunck of (50) records. Default=1.
#                 marine_only: limit to marine taxa. Default=true.
#         """
#         worms_records = self._wsdl_object.getAphiaChildrenByID(aphia_id, offset, marine_only)
#         # Convert from SOAPs structType to Python.
#         records = []
#         if worms_records:
#             for worms_record in worms_records:
#                 record = dict((key, getattr(worms_record, key)) for key in worms_record._keys())
#                 records.append(record)
#         #
#         return records
#
#     def get_value(self, worms_dict, key):
#         """ Clean values by removing unwanted characters. """
#         try:
#             if worms_dict[key]:
#                 return str(worms_dict[key]).replace('\n', ' ').replace('\r', ' ') # Remove new lines.
#         except:
#             print('Error when reading WORMS value for: ' + key + '.')
#         return ''
#
#
#
# # ===== TEST =====
# if __name__ == "__main__":
#     """ Used for testing. """
#
#     # === Test WormsWebservice. ===
#     print('\n=== Test WormsWebservice ===')
#
#     worms_ws = WormsWebservice()
#
#     worms_result = worms_ws.get_aphia_id('Nitzschia frustulum')
#     print('\nget_aphia_id: ' + str(worms_result))
#
#     worms_result = worms_ws.get_aphia_records('Ctenophora')
#     print('\nget_aphia_records: ' + str(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record.keys():
#             print(key + ':' + str(record[key]))
#
#     worms_result = worms_ws.get_aphia_name_by_id(145422)
#     print('\nget_aphia_name_by_id: ' + worms_result)
#
#     worms_result = worms_ws.get_aphia_record_by_id(145422)
#     print('\nget_aphia_record_by_id: ' + str(worms_result))
#     for key in worms_result.keys():
#         print(key + ':' + str(worms_result[key]))
#
#     worms_result = worms_ws.get_aphia_record_by_ext_id('85257', ext_type = 'tsn')
#     print('\nget_aphia_record_by_tsn: ' + str(worms_result))
#
#     worms_result = worms_ws.get_aphia_records_by_names(['Nitzschia frustulum'])
#     print('\nget_aphia_records_by_names: ' + str(worms_result))
#     for name_record in worms_result:
#         for record in name_record:
#             print('---')
#             for key in record.keys():
#                 print(key + ':' + str(record[key]))
#
#     worms_result = worms_ws.get_aphia_classification_by_id(145422)
#     print('\nget_aphia_classification_by_id: ' + str(worms_result))
#     for record in worms_result:
#             print(str(record))
#
#     worms_result = worms_ws.get_sources_by_aphia_id(145422)
#     print('\nget_sources_by_aphia_id: ' + str(worms_result))
#     for record in worms_result:
#             print(str(record))
#
#     worms_result = worms_ws.get_aphia_synonyms_by_id(145422)
#     print('\nget_aphia_synonyms_by_id: ' + str(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record.keys():
#             print(key + ':' + str(record[key]))
#
#     worms_result = worms_ws.get_aphia_children_by_id(144101)
#     print('\nget_aphia_children_by_id: ' + str(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record.keys():
#             print(key + ':' + str(record[key]))
#
#     worms_result = worms_ws.get_aphia_records_by_vernacular('copepods')
#     print('\nget_aphia_records_by_vernacular: ' + str(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record.keys():
#             print(key + ':' + str(record[key]))
#
#     worms_result = worms_ws.get_aphia_vernaculars_by_id(1080)
#     print('\nget_aphia_vernaculars_by_id: ' + str(worms_result))
#     for record in worms_result:
#         print('---')
#         for key in record.keys():
#             print(key + ':' + str(record[key]))
