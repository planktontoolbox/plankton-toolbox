#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals



# TODO: Activate this code later. 



# import toolbox_utils
# import plankton_core
# 
# class WormsMarineSpecies(object):
#     """ Utility for WoRMS access. 
#         WoRMS, World Register of Marine Species. http://marinespecies.org """
#         
#     def __init__(self):
#         """ """
#         self._worms_ws = plankton_core.WormsWebservice()
#         
#     def generate_tree_from_species_list(self,
#                                        in_file_path = '../test_data',
#                                        in_file_name = 'worms_indata.txt',
#                                        out_file_path = '../test_data',
#                                        out_file_name = 'worms_outdata.txt',
#                                        in_scientific_name_column = 'NOMAC Scientific name',
#                                        in_rank_column = 'NOMAC Rank',
#                                        in_taxon_id_column = 'NOMAC AphiaID', # To be used for homonym problems.
#                                        ):
#         """ """
#         # Indata file.
#         tablefilereader = toolbox_utils.TableFileReader(
#             file_path = in_file_path,
#             text_file_name = in_file_name,
#             select_columns_by_name = [in_scientific_name_column, in_rank_column, in_taxon_id_column]                 
#             )
#         # Outdata file.
#         tablefilewriter = toolbox_utils.TableFileWriter(
#             file_path = out_file_path,
#             text_file_name = out_file_name,
#             )
#         #
#         taxa_dict = {} # taxon_id: {taxon_id: '', scientific_name: '', rank: '', parent_id: '', etc.}
#         #
#         for row in tablefilereader.rows():
#             scientific_name = row[0]
#             rank = row[1]
#             taxon_id = row[2]
#             #
#             if rank == 'Species':
#                 #
#                 species_dict = None
#                 try:
#                     species_dict = self.find_valid_taxon(scientific_name, rank)
#                 except Exception as e:
#                     print('Exception: ' + unicode(e))
#                 #
#                 if species_dict is None:
#                     if taxon_id:
#                         species_dict = self.get_aphia_name_by_id(taxon_id.replace('AphiaID:', '').strip())
#                 #
#                 if species_dict is None:
#                     print('Species not in WoRMS: ' + scientific_name)
#                     
#                 else:
#                     species_id = species_dict['AphiaID']
#                     taxa_dict[species_id] = species_dict
#                     # Iterate over classification. Create taxa and classification info string.
#                     worms_classification_list = self._worms_ws.get_aphia_classification_by_id(species_id)
#                     parent_id = None
#                     classification_strings = []
#                     for taxon in worms_classification_list:
#                         taxon_id = taxon['AphiaID']
#                         classification_strings.append('[' + taxon['rank'] +'] ' + taxon['scientificname'])
#                         if taxon_id not in taxa_dict:
#                             taxa_dict[taxon_id] = taxon
#                             taxa_dict[taxon_id]['classification'] = ' - '.join(classification_strings)
#                             if parent_id:
#                                 taxa_dict[taxon_id]['parent_id'] = parent_id
#                         parent_id = taxon['AphiaID']
#                     # The last one is the species parent.
#                     taxa_dict[species_id]['parent_id'] = parent_id
#                     # Note: This is not a part of the classification, but useful.
#                     classification_strings.append('[' + species_dict['rank'] +'] ' + species_dict['scientificname'])
#                     taxa_dict[species_id]['classification'] = ' - '.join(classification_strings)
# 
#         # Add info.
#         for taxon in taxa_dict.values():
#             taxon_class = None
#             taxon_class_id = ''
#             parent_id = taxon.get('AphiaID', None)
#             while parent_id:
#                 parent_taxon = taxa_dict[parent_id]
#                 if parent_taxon.get('rank', '') == 'Class':
#                     taxon_class = parent_taxon['scientificname']
#                     taxon_class_id = 'AphiaID:' + unicode(parent_taxon['AphiaID'])
#                 #
#                 parent_id = parent_taxon.get('parent_id', None)
#             #
#             if taxon_class:
#                 taxon['class'] =  taxon_class
#                 taxon['class_id'] =  taxon_class_id
#         #
#         table_header = ['scientific_name', 'rank', 'taxon_id', 'parent_id', 'class', 'class_id', 'classification']
#         table_rows = []
#         for row in taxa_dict.values():
#             outrow = []
#             for item in ['scientificname', 'rank', 'AphiaID', 'parent_id', 'class', 'class_id', 'classification']:
#                 outrow.append(unicode(row.get(item, '')))
#             table_rows.append(outrow)
#         #
#         tablefilewriter.write_file(table_header, table_rows)
# 
# 
#     def find_valid_taxon(self, 
#                          scientific_name, 
#                          rank = None): # Used to reduce some homonym problems.
#         """ """
#         worms_records = self._worms_ws.get_aphia_records(scientific_name, 
#                                                         like='false', 
#                                                         fuzzy='false', 
#                                                         marine_only='false', 
#                                                         offset = 1, 
#                                                         )
#         number_of_matches = 0
#         accepted_taxon = None
#         for taxon in worms_records:
#             if taxon.get('status', '') == 'accepted':
#                 if rank:
#                     if taxon.get('rank', '') == rank:
#                         accepted_taxon = taxon
#                         number_of_matches += 1
#                 else:
#                     accepted_taxon = taxon
#                     number_of_matches += 1
#         #
#         if number_of_matches == 0:
#             raise UserWarning('No taxa matched. Scientific name: ' + scientific_name)
#         if number_of_matches > 1:
#             raise UserWarning('Multiple taxa matched. Scientific name: ' + scientific_name)
#         #
#         return accepted_taxon
# 
# #     def create_worms_dict(self, scientific_name, 
# #                                 aphia_id = None):
# #         """ """
# #         worms_dict = {}        
# #         # GetAphia ID.
# #         if aphia_id is None:
# #             aphia_id = self.get_aphia_id(scientific_name, marine_only = 'false')
# #         #
# #         if not aphia_id:
# #             return worms_dict
# #         #          
# #         # Aphia record.
# #         aphia_dict = self.get_aphia_record_by_id(aphia_id)
# #         if not aphia_dict:
# #             return worms_dict           
# #         #
# #         worms_dict['worms_status'] = self._get_value(aphia_dict, 'status')
# #         worms_dict['worms_unaccept_reason'] = self._get_value(aphia_dict, 'unacceptreason')
# # 
# #         worms_dict['worms_valid name'] = self._get_value(aphia_dict, 'valid_name')
# #         worms_dict['worms_valid authority'] = self._get_value(aphia_dict, 'valid_authority')
# # 
# #         worms_dict['worms_rank'] = self._get_value(aphia_dict, 'rank')
# # 
# #         worms_dict['worms_kingdom'] = self._get_value(aphia_dict, 'kingdom')
# #         worms_dict['worms_phylum'] = self._get_value(aphia_dict, 'phylum')
# #         worms_dict['worms_class'] = self._get_value(aphia_dict, 'class')
# #         worms_dict['worms_order'] = self._get_value(aphia_dict, 'order')
# #         worms_dict['worms_family'] = self._get_value(aphia_dict, 'family')
# #         worms_dict['worms_genus'] = self._get_value(aphia_dict, 'genus')
# #         worms_dict['worms_sscientific name'] = self._get_value(aphia_dict, 'scientificname')
# #         worms_dict['worms_authority'] = self._get_value(aphia_dict, 'authority')
# # 
# #         worms_dict['worms_url'] = self._get_value(aphia_dict, 'url')
# #         worms_dict['worms_lsid'] = self._get_value(aphia_dict, 'lsid')
# #         worms_dict['worms_aphia_id'] = self._get_value(aphia_dict, 'AphiaID')
# #         worms_dict['worms_valid_aphia_id'] = self._get_value(aphia_dict, 'valid_AphiaID')
# #         
# #         worms_dict['worms_citation'] = self._get_value(aphia_dict, 'citation')
# #         
# #         # Classification.
# #         classification_string = ''
# #         classification = self.get_aphia_classification_by_id(aphia_id)
# #         if classification:    
# #             classification_string = unicode(classification.rank) + ': ' + unicode(classification.scientificname)
# #             while classification.child:
# #                 classification = classification.child
# #                 if (classification.rank and classification.scientificname):
# #                     classification_string += ' - ' + unicode(classification.rank) + ': ' + unicode(classification.scientificname)        
# #         worms_dict['worms_classification'] = classification_string
# #         
# #         # Synonyms.
# #         synonym_list = []
# #         synonyms = self.get_aphia_synonyms_by_id(aphia_id)
# #         if synonyms:
# #             for synonym in synonyms:
# #                 if (synonym.scientificname and synonym.authority):
# #                     synonym_list.append(unicode(synonym.scientificname) + ' ' + unicode(synonym.authority))
# #         worms_dict['worms_synonym_list'] = synonym_list
# #         #        
# #         return worms_dict
# 
# 
# 
# # ===== TEST =====
# if __name__ == "__main__":
#     """ Used for testing. """
# 
#     # === Test WormsMarineSpecies. ===
# 
#     print('\n=== Test WormsMarineSpecies ===')
# 
#     marinespecies = WormsMarineSpecies()
#     
# #     try:
# #         print('\nTest. WormsMarineSpecies: find_valid_taxon:')
# #         worms_result = marinespecies.find_valid_taxon('Ctenophora')
# #         for key in worms_result.keys():
# #             print(key + ':' + unicode(worms_result[key]))
# #     except Exception as e:
# #         print('Test failed: ' + unicode(e))
# #  
# #     try:
# #         print('\nTest. WormsMarineSpecies: find_valid_taxon:')
# #         worms_result = marinespecies.find_valid_taxon('Ctenophora', rank = 'Phylum')
# #         for key in worms_result.keys():
# #             print(key + ':' + unicode(worms_result[key]))
# #     except Exception as e:
# #         print('Test failed: ' + unicode(e))
# 
#     try:
#         print('\nTest. WormsMarineSpecies: generate_tree_from_species_list:')
#         worms_result = marinespecies.generate_tree_from_species_list()
#     except Exception as e:
#         print('Test failed: ' + unicode(e))
#         raise

