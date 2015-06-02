#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""


TODO: Not used in current version. Should be rewritten and integrated with envmonlib.


"""

# """
# This module is used for preparation of resource files. Resource files are 
# stored in the json format, but they can be prepared from various sources.
# 
# """
# 
# #import date
# from abc import abstractmethod
# import datetime
# import codecs
# #import json
# import string
# import envmonlib
# import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
# import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources
# 
# 
# class PrepareDataSources(object):
#     """
#     Abstract base class. 
#     """
#     def __init__(self, taxaObject):
#         self._taxaObject = taxaObject
# 
#     @abstractmethod
#     def importTaxa(self):
#         """ Abstract method. """
# #        raise UserWarning('Abstract method not implemented.')
#         
#     @abstractmethod
#     def exportTaxa(self):
#         """ Abstract method. """
# #        raise UserWarning('Abstract method not implemented.')
# 
# 
# class PrepareDyntaxaDbTablesAsTextFiles(PrepareDataSources):
#     """
#     Imports from text files.  
#     """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(PrepareDyntaxaDbTablesAsTextFiles, self).__init__(taxaObject)
# 
#     def importTaxa(self, dir = None):
#         """ """
#         self._taxonHeader = []
#         self._hierHeader = []
#         self._namesHeader = []
#         self._taxonTypeDict = None
#         self._nameTypeDict = None
#         # These parts of the Taxa object will be modified during import.
#         self._taxa = self._taxaObject.getTaxonList()
#         self._idToTaxon = self._taxaObject.getIdToTaxonDict()
#         
#         self._createTaxonTypeDict() # Maps from taxon type id to taxon type.
#         self._createNameTypeDict() # Maps from name type id to name type.
#         
#         # === TAXON file ===
#         envmonlib.Logging().log('Reading: ' + dir + '/dyntaxa_taxon.txt')
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         taxonFile = codecs.open(dir + '/dyntaxa_taxon.txt', mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for line in taxonFile:
#             if len(self._taxonHeader) == 0:
#                 # Store header columns.
#                 self._taxonHeader = line.split(separator)
#             else:
#                 # Split row and trim each item.
#                 columns = map(self._cleanUpString, line.split(separator))
#                 if len(columns) < 2:
#                     continue # Don't handle short rows.
#                 # Extract used column values:
#                 # 0, idnr    
#                 taxonid = int(columns[1]) # 1, taxonid
#                 taxontypid = int(columns[2]) # 2, taxontypid
#                 # 3, referensid
#                 # 4, person
#                 # 5, datum
#                 datum0 = columns[6] # 6, datum0
#                 datum1 = columns[7] # 7, datum1
#                 # 8, andringid
#                 # 9, taxondummy
#                 # 10, leaf
#                 exportkat = int(columns[11]) # 11, exportkat
#                 # 12, lista
#                 # 13, text
#                 
#                 # Check if data is in a valid time span, related to "now".
#                 dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
#                 dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
#                 nowDate = datetime.date.today()           
#                 now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
#                 if (exportkat == 0) and (dateFrom <= now) and (now <= dateTo):
#                     taxonDict = {}
#                     taxonDict['Taxon id'] = taxonid
#                     taxonDict['Taxon type id'] = taxontypid
#                     taxonDict['Taxon type'] = self._taxonTypeDict[str(taxontypid)]
#                     taxonDict['Valid from'] = datum0
#                     taxonDict['Valid to'] = datum1
#                 self._taxa.append(taxonDict) # Updates Taxa object.
#                 if not(taxonid in self._idToTaxon):
#                     self._idToTaxon[taxonid] = taxonDict # Updates Taxa object.
#                 else:
#                     envmonlib.Logging().log('Duplicate taxon id: ' + str(taxonid) )
#         taxonFile.close()
#         
#         # === HIER file ===
#         envmonlib.Logging().log('Reading: ' + dir + '/dyntaxa_hier.txt')
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         hierFile = codecs.open(dir + '/dyntaxa_hier.txt', mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for line in hierFile:
#             if len(self._hierHeader) == 0:
#                 # Store header columns.
#                 self._hierHeader = line.split(separator)
#             else:
#                 # Split row and trim each item.
#                 columns = map(self._cleanUpString, line.split(separator))
#                 if len(columns) < 2:
#                     continue # Don't handle short rows.
#                 # Extract used column values:
#                 # 0, idnr
#                 agarid = int(columns[1]) # 1, agarid
#                 underid = int(columns[2]) # 2, underid
#                 relationid = int(columns[3]) # 3, relationid
#                 # 4, relation
#                 # 5, referensid
#                 # 6, person
#                 # 7, datum
#                 datum0 = columns[8] # 9, datum0
#                 datum1 = columns[9] # 9, datum1
#                 # 10, lista
#                 # 11, dublett
#                 # 12, text
#                 
#                 # Check if data is in a valid time span, related to "now".
#                 dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
#                 dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
#                 nowDate = datetime.date.today() # Note: includes day and time.           
#                 now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
#                 if (dateFrom <= now) and (now <= dateTo):
#                     if underid in self._idToTaxon:
#                         taxon = self._idToTaxon[underid]
#                         if relationid == 0:
#                             pass
# #                            taxon['Parent id'] = ''
#                         elif relationid == 2:
#                             taxon['Parent id'] = agarid
#                     else:
#                         envmonlib.Logging().info('Can not find Taxon id(hier): ' + underid)
#         hierFile.close()
#         
#         # === NAMES file ===
#         envmonlib.Logging().log('Reading: ' + dir + '/dyntaxa_names.txt')
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         namesFile = codecs.open(dir + '/dyntaxa_names.txt', mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for line in namesFile:
#             if len(self._namesHeader) == 0:
#                 # Store header columns.
#                 self._namesHeader = line.split(separator)
#             else:
#                 # Split row and trim each item.
#                 columns = map(self._cleanUpString, line.split(separator))
#                 if len(columns) < 2:
#                     continue # Don't handle short rows.
#                 # Extract used column values:
#                 # 0, idnr
#                 taxonid = int(columns[1]) # 1, taxonid
#                 # 2, taxontypid
#                 # 3, taxondummy
#                 namn = columns[4] # 4, namn
#                 auktor = columns[5] # 5, auktor
#                 namntypid = int(columns[6]) # 6, namntypid
#                 # 7, obsrek
#                 # 8, referensid
#                 # 9, person
#                 # 10, datum
#                 datum0 = columns[11] # 11, datum0
#                 datum1 = columns[12] # 12, datum1
#                 exportkat = int(columns[13]) # 13, exportkat
#                 # 14, lista
#                 # 15, text
#                                 
#                 # Check if data is in a valid time span, related to "now".
#                 dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
#                 dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
#                 nowDate = datetime.date.today() # Note: includes day and time.           
#                 now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
#                 if (exportkat == 0) and (dateFrom <= now) and (now <= dateTo):
#                     if taxonid in self._idToTaxon:
#                         taxon = self._idToTaxon[taxonid]    
#                         nameDict = {}
#                         nameDict['Name type id'] = namntypid
#                         nameDict['Name type'] = self._nameTypeDict[str(namntypid)]
#                         nameDict['Name'] = namn
#                         nameDict['Author'] = auktor
#                         nameDict['Valid from'] = datum0
#                         nameDict['Valid to'] = datum1                        
#                         if not ('Names' in taxon):
#                             taxon['Names'] = [] # Create list for names.
#                         taxon['Names'].append(nameDict)
#                         # Create Scientific name/author for easy access.
#                         if namntypid == 0:
#                             taxon['Scientific name'] = namn
#                             taxon['Scientific name author'] = auktor
#                     else:
#                         envmonlib.Logging().info('Can not find Taxon id(name): ' + str(underid))                
#         namesFile.close()
#         
#     def _cleanUpString(self,value):
#         """ """
#         return value.strip()
# 
#     def _createTaxonTypeDict(self):
#         """ """
#         self._taxonTypeDict = {        
#             "0": "Biota",
#             "1": "Kingdom",
#             "2": "Phylum",
#             "3": "Subphylum",
#             "4": "Superclass",
#             "5": "Class",
#             "6": "Subclass",
#             "7": "Superorder",
#             "8": "Order",
#             "9": "Suborder",
#             "10": "Superfamily",
#             "11": "Family",
#             "12": "Subfamily",
#             "13": "Tribe",
#             "14": "Genus",
#             "15": "Subgenus",
#             "16": "Section",
#             "17": "Species",
#             "18": "Subspecies",
#             "19": "Variety",
#             "20": "Form",
#             "21": "Hybrid",
#             "22": "Cultural variety",
#             "23": "Population",
#             "24": "Group of families",
#             "25": "Infraclass",
#             "26": "Parvclass",
#             "27": "Sensu lato",
#             "28": "Species pair",
#             "-2": "Group",
#             "-1": "Group of lichens",
#             "29": "Infraorder",
#             "30": "Avdelning",
#             "31": "Underavdelning"}
#         
#     def _createNameTypeDict(self):
#         """ """
#         self._nameTypeDict = {
#             "0": "Scientific",
#             "1": "Swedish",
#             "2": "English",
#             "3": "Danish",
#             "4": "Norwegian",
#             "5": "Finnish",
#             "6": "Icelandic",
#             "7": "American english",
#             "8": "NNkod",
#             "9": "ITIS-name",
#             "10": "ITIS-number",
#             "11": "ERMS-name",
#             "12": "Geman",
#             "13": "Original name",
#             "14": "Faeroe",
#             "15": "Anamorf name"}
# 
# 
# class PreparePegTextFile(PrepareDataSources):
#     """ 
#     """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(PreparePegTextFile, self).__init__(taxaObject)
# 
#     def importTaxa(self, file = None):
#         """ """
#         self._header = []
#         self._taxa = self._taxaObject.getTaxonList()
#         
#         envmonlib.Logging().log('Reading: ' + file)
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
# 
#         
#         
#         
# 
#         
#         
#         
#         txtencode = 'utf16'
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         
#         pegFile = codecs.open(file, mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for line in pegFile:
#             if len(self._header) == 0:
#                 # Store header columns. They will be used as keys i the taxon dictionary.
#                 importFileHeader = line.split(separator)
#                 for columnName in importFileHeader: 
#                     self._header.append(self._translateHeader(columnName.strip()))
#             else:
#                 taxonDict = {}
#                 sizeClassDict = {}
#                 column = 0
#                 for value in line.split(separator):
#                     if len(value.strip()) > 0:
#                         # Separate columns containing taxon and 
#                         # size-class related info.                
#                         if self._isTaxonRelated(column):
#                             taxonDict[self._header[column]] = value.strip()
#                         else:
#                             if self._isColumnNumeric(column):
#                                 try:
#                                     float_value = float(value.strip().replace(',', '.').replace(' ', ''))
#                                     sizeClassDict[self._header[column]] = float_value
#                                     if self._header[column] == 'Size class':  # Covert SIZECLASS to integer.
#                                         sizeClassDict[self._header[column]] = int(float_value)
#                                 except:
#                                     # Use string format if not valid numeric. 
#                                     sizeClassDict[self._header[column]] = value.strip()
#                                     
# #                                    envmonlib.Logging().info('ERROR float:' + value + '     ' + value.strip().replace(',', '.').replace(' ', ''))
#                                     
#                             else:
#                                 sizeClassDict[self._header[column]] = value.strip()
#                     column += 1
#                 # Check if the taxon-related data already exists.
#                 taxonExists = False
#                 for taxon in self._taxa:
#                     if taxon['Species'] == taxonDict['Species']:
#                         taxonExists = True
#                         taxon['Size classes'].append(sizeClassDict)
#                         continue
#                 # First time. Create the list and add dictionary for 
#                 # size classes. 
#                 if taxonExists == False:
#                     self._taxa.append(taxonDict)
#                     taxonDict['Size classes'] = []
#                     taxonDict['Size classes'].append(sizeClassDict)
#                 
#         pegFile.close()
#         
#     def _translateHeader(self, importFileHeader):
#         """ Convert import file column names to key names used in dictionary. """        
# #        if (importFileHeader == 'Division'): return 'Division'
# #        if (importFileHeader == 'Class'): return 'Class'
# #        if (importFileHeader == 'Order'): return 'Order'
# #        if (importFileHeader == 'Species'): return 'Species'
#         if (importFileHeader == 'SFLAG (sp., spp., cf., complex, group)'): return 'SFLAG' # Modified
#         if (importFileHeader == 'STAGE (cyst, naked)'): return 'Stage' # Modified
# #        if (importFileHeader == 'Author'): return 'Author'
# #        if (importFileHeader == 'Trophic type'): return 'Trophic type'
# #        if (importFileHeader == 'Geometric shape'): return 'Geometric shape'
#         if (importFileHeader == 'FORMULA'): return 'Formula' # Modified
#         if (importFileHeader == 'Size class No'): return 'Size class' # Modified
# #        if (importFileHeader == 'Unit'): return 'Unit'
#         if (importFileHeader == 'size range,'): return 'Size range' # Modified
# #        if (importFileHeader == 'Length (l1), \xb5m'): return 'Length(l1), um' # Modified
# #        if (importFileHeader == 'Length (l2), \xb5m'): return 'Length(l2), um' # Modified
# #        if (importFileHeader == 'Width (w), \xb5m'): return 'Width(w), um' # Modified
# #        if (importFileHeader == 'Height (h), \xb5m'): return 'Height(h), um' # Modified
# #        if (importFileHeader == 'Diameter (d1), \xb5m'): return 'Diameter(d1), um' # Modified
# #        if (importFileHeader == 'Diameter (d2), \xb5m'): return 'Diameter(d2), um' # Modified
#         if (importFileHeader == 'No. of cells/ counting unit'): return 'No. of cells/counting unit' # Modified
# #        if (importFileHeader == 'Calculated  volume, \xb5m3'): return 'Calculated volume, um3' # Modified
#         if (importFileHeader == 'Comment'): return 'Comment'
# #        if (importFileHeader == 'Filament: length of cell (\xb5m)'): return 'Filament: length of cell, um' # Modified
#         if (importFileHeader == 'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return 'Calculated Carbon pg/counting unit' # Modified
#         if (importFileHeader == 'Comment on Carbon calculation'): return 'Comment on Carbon calculation'
#         if (importFileHeader == 'CORRECTION / ADDITION                            2009'): return 'Correction/addition 2009' # Modified
#         if (importFileHeader == 'CORRECTION / ADDITION                            2010'): return 'Correction/addition 2010' # Modified
#         return importFileHeader     
#         
#     def _isTaxonRelated(self, column):
#         """ """        
#         if (self._header[column] == 'Division'): return True
#         if (self._header[column] == 'Class'): return True
#         if (self._header[column] == 'Order'): return True
#         if (self._header[column] == 'Species'): return True
#         if (self._header[column] == 'Author'): return True
#         if (self._header[column] == 'SFLAG'): return True
#         if (self._header[column] == 'Stage'): return True
#         if (self._header[column] == 'Trophic type'): return True
#         if (self._header[column] == 'Geometric shape'): return True
#         if (self._header[column] == 'Formula'): return True
#         return False # Related to size class.     
#         
#     def _isColumnNumeric(self, column):
#         """ """        
#         if (self._header[column] == 'Size class'): return True
#         if (self._header[column] == 'Length(l1), um'): return True
#         if (self._header[column] == 'Length(l2), um'): return True
#         if (self._header[column] == 'Width(w), um'): return True
#         if (self._header[column] == 'Height(h), um'): return True
#         if (self._header[column] == 'Diameter(d1), um'): return True
#         if (self._header[column] == 'Diameter(d2), um'): return True
#         if (self._header[column] == 'No. of cells/counting unit'): return True
#         if (self._header[column] == 'Calculated volume, um3'): return True
#         if (self._header[column] == 'Filament: length of cell, um'): return True
#         if (self._header[column] == 'Calculated Carbon pg/counting unit'): return True
#         return False     
# 
# 
#     def addPwToPeg(self, file = None):
#         """ """
#         if (not self._taxa) or (len(self._taxa) == 0):
#             print('DEBUG: __taxa is empty.')
#             return
#         if (not file) or (len(file) == 0):
#             print('DEBUG: file name is missing.')
#             return
#         print('DEBUG: Loading translation file: ' + file)
#         #
#         pw_name_dict = {}
#         pw_sizeclass_dict = {}
#         #
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         translateFile = codecs.open(file, mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for row in translateFile:
#             items = map(string.strip, row.split(separator))
#             pwname = ''
#             pwsize = '' 
#             pegname = ''
#             pegsize = ''
#             sflag = ''
# #            extendedpegname = ''
# #            extendedpegsize = ''
#             if len(items) > 3:
#                 pwname = items[0]
#                 pwsize = items[1] 
#                 pegname = items[2]
#                 pegsize = items[3]
#                 if len(items) > 4: sflag = items[4]                
# #                # Column 5 and 6 may be used for references to taxon/sizes in the extended part
# #                # of the PEG list.
# #                if len(items) > 4: extendedpegname = items[4]
# #                if len(items) > 5: extendedpegsize = items[5]
# #                if (len(pegname) == 0) and ((len(extendedpegname) > 0)):
# #                    pegname = extendedpegname
# #                    print('DEBUG: extendedpegname:' + extendedpegname)
# #                if (len(pegsize) == 0) and ((len(extendedpegsize) > 0)):
# #                    pegsize = extendedpegsize
# #                    print('DEBUG: extendedpegsize:' + extendedpegsize)
# #                #
#                 if (not pw_name_dict.has_key(pegname)) and (len(pwname) > 0):
#                     pw_name_dict[pegname] = pwname + ':' + sflag
#                 pw_sizeclass_dict[pegname + ':' + pegsize] = pwname + ':' + pwsize
# #                print('DEBUG: pw_sizeclass_dict: ' + pegname + ':' + pegsize + ' = ' + pwname + ':' + pwsize)           
#             else:
#                 print('DEBUG: TranslateFile, row to short: ' + unicode(row))
#         translateFile.close()
#         #
#         print('DEBUG: PW add to PEG.')
#         
#         for pegtaxon in self._taxa:
#             # Add PW name at taxon level.
#             pwnameandsflag = pw_name_dict.get(pegtaxon['Species'], '')
#             if pwnameandsflag:
#                 pwname, sflag = pwnameandsflag.split(':')
#                 pegtaxon['Species PW'] = pwname
#                 if sflag:
#                     pegtaxon['Species PW SFLAG'] = sflag
#             for pegsizeclass in pegtaxon['Size classes']:
#                 # Add PW sizeclass.
#                 pwnameandsize = pw_sizeclass_dict.get(pegtaxon['Species'] + ':' + str(pegsizeclass['Size class']), '')
#                 pwsize = pwnameandsize.split(':')
#                 if len(pwsize) > 1:
#                     try:
#                         pegsizeclass['Size class PW'] = int(pwsize[1])
#                     except:
#                         print('ERROR: Invalid sizeclass for: ' + pwnameandsize)
# 
#         print('DEBUG: PW added to PEG.')
# 
# 
#     def addDyntaxaToPeg(self, file = None):
#         """ """
#         if (not self._taxa) or (len(self._taxa) == 0):
#             print('DEBUG: __taxa is empty.')
#             return
#         if (not file) or (len(file) == 0):
#             print('DEBUG: file name is missing.')
#             return
#         
#         # Use the toolbox resource dyntaxa.
#         toolbox_resources.ToolboxResources().loadUnloadedResourceDyntaxa()
#         dyntaxa = toolbox_resources.ToolboxResources().getResourceDyntaxa()
#         
#         # Load translation file.
#         translate_dict = {}
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         translateFile = codecs.open(file, mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for row in translateFile:
#             items = map(string.strip, row.split(separator))
#             if len(items) > 1:
#                 pegname = items[0]
#                 dyntaxaname = items[1] 
#                 translate_dict[pegname] = dyntaxaname
#         translateFile.close()
#         
#         
#         print('DEBUG: Dyntaxa add to PEG.')
#         for pegtaxon in self._taxa:
#             # Add PW name at taxon level.
#             pegname = pegtaxon['Species']
#             pwname = pegtaxon.get('Species PW','')
#             
#             # Check if PEG-name match.
#             taxon = dyntaxa.getTaxonByName(pegname)
#             if taxon:
#                 pegtaxon['Dyntaxa id'] = taxon['Taxon id']
#                 pegtaxon['Dyntaxa name'] = taxon['Scientific name']
#                 continue
#             # Check if PW-name match.
#             taxon = dyntaxa.getTaxonByName(pwname)
#             if taxon:
#                 pegtaxon['Dyntaxa id'] = taxon['Taxon id']
#                 print('DEBUG: PWNAME MATCH............................................................')
#                 continue
#             # Check translatefile.
# #            print('DEBUG: TODO MATCH FILE... ' + pegname)
#             taxon = dyntaxa.getTaxonByName(translate_dict.get(pegname, ''))
#             if taxon:
#                 pegtaxon['Dyntaxa id'] = taxon['Taxon id']
#                 envmonlib.Logging().log('PEG to Dyntaxa translation file used. PEG name: ' + pegname)                           
#             
#         print('DEBUG: Dyntaxa added to PEG.')
#        
# 
# class PrepareHarmfulMicroAlgae(PrepareDataSources):
#     """ 
#     """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(PrepareHarmfulMicroAlgae, self).__init__(taxaObject)
# 
#     def importTaxa(self, file = None):
#         """ """
#         self._header = []
#         self._taxa = self._taxaObject.getTaxonList()
#         
#         # Load needed resources, if not loaded before.
#         toolbox_resources.ToolboxResources().loadUnloadedResourceDyntaxa()
#         dyntaxa = toolbox_resources.ToolboxResources().getResourceDyntaxa()
#         #
#         envmonlib.Logging().log('Reading: ' + file)
#         txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#         harmfulFile = codecs.open(file, mode = 'r', encoding = txtencode)
#         separator = '\t' # Tab as separator.
#         for row in harmfulFile:
#             if len(self._header) == 0:
#                 # Store header columns. They will be used as keys i the taxon dictionary.
#                 importFileHeader = map(string.strip, row.split(separator))
#                 for columnName in importFileHeader: 
#                     self._header.append(columnName.strip())
#             else:
#                 # Add each row as a taxon.
#                 taxonDict = {}
#                 for column, value in enumerate(map(string.strip, row.split(separator))):
#                     if len(value) > 0:
#                         if self._header[column] == 'Aphia id':
#                             taxonDict[self._header[column]] = int(value) # Integer value.
#                         else:
#                             taxonDict[self._header[column]] = value # String value.
#                 self._taxa.append(taxonDict)
#                 # Check if the scientific name exists in Dyntaxa. Add Taxon-id if it does.
#                 dyntaxataxon = dyntaxa.getTaxonByName(taxonDict.get('Scientific name', ''))
#                 if dyntaxataxon:
#                     dyntaxaid = dyntaxataxon.get('Taxon id', None)
#                     if dyntaxaid:
#                         taxonDict['Dyntaxa id'] = dyntaxaid # Integer value.
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 


