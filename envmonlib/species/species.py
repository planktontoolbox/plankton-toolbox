#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import envmonlib
import os.path

@envmonlib.singleton
class Species(object):
    """ 
    Loads all species related files used in the toolbox.
    More information can be found on the wiki pages at http://plankton-toolbox.org
    Rules:
    - Files must be in the new Excel (*.xlsx) format.
    - Taxa files must start with 'taxa_'.
    - Biovolume files must start with 'bvol_'.
    - Translation files must start with 'translate_'.
    - Synonym files must start with 'synonyms_'.
    - Column mapping file for Biovolume files must start with 'bvolcolumns_'.
    - Harmful files must start with 'harmful_'.
    
    File columns:
    - Taxa files columns: scientific_name, rank, parent_name.
    - etc. (Documented on the wiki pages mentioned above.)
    
    """
    def __init__(self,
                 species_directory_path = 'toolbox_data/species/'):
        # Parameters.
        self._species_directory_path = species_directory_path
        # Taxa files.
        self._taxa_filenames = self._getFilesByPrefix('taxa_')
        # Translate files.
        self._taxatranslate_filenames = self._getFilesByPrefix('translate_')
        # Synonyms files.
        self._taxasynonyms_filenames = self._getFilesByPrefix('synonyms_')
        # Biovolume, mapping information for used columns.
        self._bvolcolumns_filenames = self._getFilesByPrefix('bvolcolumns_')
        # Biovolume files.
        self._bvol_filenames = self._getFilesByPrefix('bvol_')
        # Plankton groups definition. Useful grouping that differ from 
        self._planktongroups_filenames = self._getFilesByPrefix('planktongroups_')
        # Harmful algae files.
        self._harmful_filenames = self._getFilesByPrefix('harmful_')

        # Defines local storage by calling clear().
        self._clear()
                
        try:
            # Only done once since the class is declared as singleton.
            self._loadAllData()
        except Exception as e:
            envmonlib.Logging().error('Failed when loading species related files: ' + unicode(e))            
            raise

    def getTaxaDict(self):
        """ """
        return self._taxa 
    
    def getTaxaLookupDict(self):
        """ """
        return self._taxa_lookup 
    
    def getTaxonValue(self, scientific_name, key):
        """ """
        if scientific_name in self._taxa_lookup:
            
#             print('DEBUG: '+ scientific_name + ' - ' + key + ' - ' + self._taxa_lookup[scientific_name].get(key, ''))
            
            
            return self._taxa_lookup[scientific_name].get(key, '')
        return ''
    
    def getBvolValue(self, scientific_name, size_class, key):
        """ """
        if scientific_name in self._taxa_lookup:
            speciesobject = self._taxa_lookup[scientific_name]
            if 'Size classes' in speciesobject:
                for sizeclassobject in speciesobject['Size classes']:
                    if sizeclassobject.get('Size class', '') == unicode(size_class):
                        return sizeclassobject.get(key, '')
        return None 
    
    def _clear(self):
        """ """
        # Local storage.
        self._taxa = {} # Main dictionary for taxa. Also includes bvol.
        self._taxa_lookup = {} # Includes both taxon names, translated names and synonyms.
        self._planktongroups_ranks_set = set()
        self._planktongroups_rank_dict = {}
        self._planktongroups_lookup = {}
        self._bvolcolumns_dict = {}        
        self._harmful = {}

    def _loadAllData(self):
        """ """
        try:
            self._clear()
            envmonlib.Logging().log('') # Empty line.
            envmonlib.Logging().log('Loading species lists (located in "' + self._species_directory_path + '"):')
            
            # Load taxa.
            for excelfilename in self._taxa_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Species and other taxa)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadTaxa(excelfilename)
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    
                                    
            # Add translated scientific names to taxa.
            for excelfilename in self._taxatranslate_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Misspellings etc.)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadSynonyms(excelfilename) # Synonyms and translated names are handled the same way.                           
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    
            
            # Add synonyms to taxa. Note: 'translate_to_' will be added to filenames.
            for excelfilename in self._taxasynonyms_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Synonyms for taxa)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadSynonyms(excelfilename)                            
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    
            
            # Load biovolume column mapping information.
            for excelfilename in self._bvolcolumns_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Biovolume column mapping)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadBvolColumns(excelfilename)        
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    

            # Load BVOL species data.
            for excelfilename in self._bvol_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Biovolumes etc. for sizeclasses)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadBvol(excelfilename)        
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    

            # Load harmful species.
            for excelfilename in self._harmful_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Harmful organisms)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadHarmful(excelfilename)
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    

            # Load plankton group definition.
            for excelfilename in self._planktongroups_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log('- ' + os.path.basename(excelfilename) + ' (Plankton group definition)')
                    try:
                        envmonlib.Logging().startAccumulatedLogging()
                        #
                        self._loadPlanktonGroupDefinition(excelfilename)
                    finally:
                        envmonlib.Logging().logAllAccumulatedRows()    
            
            # Perform some useful pre-calculations.
            self._precalculateData()
        #
        except Exception as e:
            envmonlib.Logging().error('Failed when loading species data: ' + unicode(e))            
            raise
            
#        # Used for DEBUG:
#        import locale
#        import codecs
#        import json
#        fileencoding = locale.getpreferredencoding()
#        out = codecs.open('DEBUG_species_list.txt', mode = 'w', encoding = fileencoding)
#        out.write(json.dumps(self._taxa, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()
#        # DEBUG end.

    def _loadTaxa(self, excel_file_name):
        """ Creates one data object for each taxon. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = ''
            try:
                scientificname = row[0].strip() # ScientificName.
                author = row[1].strip() if row[1].strip() != 'NULL' else '' # Author.
                rank = row[2].strip() # Rank.
                parentname = row[3].strip() # Parent.
                #
                if scientificname:
                    if scientificname not in self._taxa:
                        self._taxa[scientificname] = {}
                        # Lookup dictionary.
                        self._taxa_lookup[scientificname] = self._taxa[scientificname]
                    else:
                        envmonlib.Logging().warning('Scientific name added twice: ' + scientificname + '   (Source: ' + excel_file_name + ')')
                    #    
                    speciesobject = self._taxa[scientificname]
                    speciesobject['Scientific name'] = scientificname
                    speciesobject['Author'] = author
                    speciesobject['Rank'] = rank
                    speciesobject['Parent name'] = parentname
            except:
                envmonlib.Logging().warning('Failed when loading taxa. File:' + excel_file_name + '  Taxon: ' + scientificname)
                

    def _loadSynonyms(self, excel_file_name):
        """ Add synonyms from 'translate_' or 'synonyms_' files. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            toname = ''
            fromname = ''
            try:
                toname = row[1].strip()
                fromname = row[0].strip()
                #
                if toname in self._taxa_lookup:
                    taxon = self._taxa_lookup[toname]
                    if not 'Synonyms' in self._taxa[toname]:
                        taxon['Synonyms'] = []
                    taxon['Synonyms'].append(fromname)
                    # Lookup dictionary.
                    self._taxa_lookup[fromname] = self._taxa[toname]
                else:
                    envmonlib.Logging().warning('Scientific name is missing: ' + toname + '   (Source: ' + excel_file_name + ')')
            except:
                envmonlib.Logging().warning('Failed when loading synonym. File:' + excel_file_name + '  From taxon: ' + toname)
                    
    def _loadHarmful(self, excel_file_name):
        """ Adds info about harmfulness to the species objects. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = ''
            try:
                scientificname = row[0].strip() # Scientific name.
                aphiaid = row[1] if row[1].strip() != 'NULL' else '' # Aphia id.
                #
                if scientificname in self._taxa_lookup:
                    taxon = self._taxa_lookup[scientificname]
                    taxon['Harmful name'] = scientificname
                    taxon['Harmful'] = True 
                    taxon['Aphia id'] = aphiaid
                else:
                    envmonlib.Logging().warning('Scientific name is missing: ' + scientificname + '   (Source: ' + excel_file_name + ')')
            except:
                envmonlib.Logging().warning('Failed when loading harmful algae. File:' + excel_file_name + '  Taxon: ' + scientificname)

    def _loadPlanktonGroupDefinition(self, excel_file_name):
        """ """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = ''
            try:
                scientificname = row[0].strip() # Scientific name.
                rank = row[1].strip() # Rank.
                planktongroup = row[2].strip() # Plankton group.
                #
                if scientificname and planktongroup:
                    used_rank = rank
                    if not used_rank:
                        used_rank = 'scientific_name'
                    self._planktongroups_ranks_set.add(used_rank)
                    #
                    if used_rank not in self._planktongroups_rank_dict:
                        self._planktongroups_rank_dict[used_rank] = {}
                    self._planktongroups_rank_dict[used_rank][scientificname] = planktongroup
            except:
                envmonlib.Logging().warning('Failed when loading plankton group def. File:' + excel_file_name + '  Taxon: ' + scientificname)
    
    def _precalculateData(self):
        """ Calculates data from loaded datasets. I.e. phylum, class and order info. """
        for speciesobject in self._taxa.values():
            scientificname = ''
            try:
                scientificname = speciesobject['Scientific name']
                counter = 0
                parentobject = speciesobject
                while parentobject:
                    counter += 1
                    if counter > 20:
                        parentobject = None # Too many levels, or infinite loop.
                        print('DEBUG: Species._precalculateData(): Too many levels, or infinite loop.')
                        continue
                    if 'Rank' in parentobject:
                        if parentobject['Rank'] == 'Species':
                            speciesobject['Species'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Genus':
                            speciesobject['Genus'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Family':
                            speciesobject['Family'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Order':
                            speciesobject['Order'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Class':
                            speciesobject['Class'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Phylum':
                            speciesobject['Phylum'] = parentobject['Scientific name']
                        if parentobject['Rank'] == 'Kingdom':
                            speciesobject['Kingdom'] = parentobject['Scientific name']
                            parentobject = None # Done. Continue with next.
                            continue
                    # One step up in hierarchy.
                    if 'Parent name' in parentobject:
                        if parentobject['Parent name'] in self._taxa:
                            parentobject = self._taxa[parentobject['Parent name']] if parentobject['Parent name'] else None
                        else:
                            if parentobject['Scientific name'] != 'Biota':
                                envmonlib.Logging().warning('Parent taxon is missing for : ' + parentobject['Scientific name'])
                            parentobject = None
                    else:
                        parentobject = None
            except:
                envmonlib.Logging().warning('Failed when creating classification. Taxon: ' + scientificname)

    def _loadBvolColumns(self, excel_file_name):
        """ """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            columnname = ''
            try:
                # Header: Column name, Used on level, Numeric, Internal toolbox name.
                columnname = row[0].strip()
                level = row[1].strip()
                numeric = row[2].strip()
                internalname = row[3].strip()
                #
                if columnname and level and internalname:
                    self._bvolcolumns_dict[columnname] = (level, numeric, internalname) 
            except:
                envmonlib.Logging().warning('Failed when loading BVOL columns. Column name: ' + columnname)
        
    def _loadBvol(self, excel_file_name):
        """ Adds BVOL data to species objects. Creates additional species objects if missing 
            (i.e. for Unicell, Flagellates). """
        # Import size class data.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        # Create header list for mapping and translations.
        headerinfo = [] # Contains used columns only.
        for columnindex, columnname in enumerate(tabledataset.getHeader()): 
            # Use loaded information on used columns.
            if columnname in self._bvolcolumns_dict:
                level, numeric, internalname = self._bvolcolumns_dict[columnname]
                headerinfo.append((columnindex, columnname, level, numeric, internalname))
        #
        for row in tabledataset.getRows():
            taxondict = {}
            sizeclassdict = {}
            try:
###                for column, value in enumerate(row):
                for columnindex, columnname, level, numeric, internalname in headerinfo:
                    value = row[columnindex].strip()
                    
                    if len(value) > 0:
                        # Separate columns contains taxon and size-class related info.                
                        if level == 'Taxon':
                            taxondict[internalname] = value
                        else:
                            if (internalname == 'Size class'):
                                try:
                                    # Convert from float to integer and back to unicode. Excel related problem.
                                    sizeclassdict[internalname] = unicode(int(float(value)))
                                except:
                                    sizeclassdict[internalname] = ''
                            elif numeric == 'Numeric':
                                sizeclassdict[internalname] = value.replace(',', '.')
                            else:
                                sizeclassdict[internalname] = value
                # Check if exists in self._taxa
                if 'BVOL Species' in taxondict: 
                    scientificname = taxondict['BVOL Species']
                    if scientificname in self._taxa_lookup:
                        speciesobject = self._taxa_lookup[scientificname]
                    else:
                        size = sizeclassdict.get('Size class', '')
                        envmonlib.Logging().warning('Scientific name is missing: ' + scientificname + '   Size: ' + size + '   (Source: ' + excel_file_name + ')')
                        continue # Only add BVOL info if taxon exists in taxa.
                    #
                    speciesobject['BVOL name'] = scientificname
                    #
                    if 'Size classes' not in speciesobject:
                        speciesobject['Size classes'] = []
                        # Add other bvol data to taxon.
                        for key in taxondict.keys():
                            speciesobject[key] = taxondict[key]
                    #
                    speciesobject['Size classes'].append(sizeclassdict)
            except:
                envmonlib.Logging().warning('Failed when loading BVOL data.')
        #
        # Trophic_type is set on sizeclass level. Should also be set on species level  
        # if all sizeclasses have the same trophic_type.
        for taxon in self._taxa.values():
            try:
                trophic_type_set = set() 
                if 'Size classes' in taxon:
                    for sizeclass in taxon['Size classes']:
                        trophic_type_set.add(sizeclass.get('Trophic type', ''))
                if len(trophic_type_set) == 1:
                    taxon['Trophic type'] = list(trophic_type_set)[0]

            except:
                envmonlib.Logging().warning('Failed when loading BVOL data (the trophic type part).')
                    
#     def _translateBvolHeader(self, importFileHeader):
#         """ Convert import file column names to key names used in dictionary. """        
#     #        if (importFileHeader == 'Division'): return 'Division'
#     #        if (importFileHeader == 'Class'): return 'Class'
#     #        if (importFileHeader == 'Order'): return 'Order'
#     #        if (importFileHeader == 'Species'): return 'Species'
#         if (importFileHeader == 'SFLAG (sp., spp., cf., complex, group)'): return 'SFLAG' # Modified
#         if (importFileHeader == 'STAGE (cyst, naked)'): return 'Stage' # Modified
#     #        if (importFileHeader == 'Author'): return 'Author'
#     #        if (importFileHeader == 'AphiaID'): return 'AphiaID'
#     #        if (importFileHeader == 'Trophic type'): return 'Trophic type'
#     #        if (importFileHeader == 'Geometric shape'): return 'Geometric shape'
#         if (importFileHeader == 'FORMULA'): return 'Formula' # Modified
#         if (importFileHeader == 'Size class No'): return 'Size class' # Modified
#         if (importFileHeader == 'SizeClassNo'): return 'Size class' # Modified
#         if (importFileHeader == 'Nonvalid_SIZCL'): return 'Nonvalid size class' # Modified
#         if (importFileHeader == 'Not_accepted'): return 'Not accepted' # Modified
#     #        if (importFileHeader == 'Unit'): return 'Unit'
#         if (importFileHeader == 'size range,'): return 'Size range' # Modified
#         if (importFileHeader == 'Length (l1), µm'): return 'Length(l1), µm' # Modified
#         if (importFileHeader == 'Length(l1)µm'): return 'Length(l1), µm' # Modified
#         if (importFileHeader == 'Length (l2), µm'): return 'Length(l2), µm' # Modified
#         if (importFileHeader == 'Length(l2)µm'): return 'Length(l2), µm' # Modified
#         if (importFileHeader == 'Width (w), µm'): return 'Width(w), µm' # Modified
#         if (importFileHeader == 'Width(w)µm'): return 'Width(w), µm' # Modified
#         if (importFileHeader == 'Height (h), µm'): return 'Height(h), µm' # Modified
#         if (importFileHeader == 'Height(h)µm'): return 'Height(h), µm' # Modified
#         if (importFileHeader == 'Diameter (d1), µm'): return 'Diameter(d1), µm' # Modified
#         if (importFileHeader == 'Diameter(d1)µm'): return 'Diameter(d1), µm' # Modified
#         if (importFileHeader == 'Diameter (d2), µm'): return 'Diameter(d2), µm' # Modified
#         if (importFileHeader == 'Diameter(d2)µm'): return 'Diameter(d2), µm' # Modified
#         if (importFileHeader == 'No. of cells/ counting unit'): return 'No. of cells/counting unit' # Modified
#         if (importFileHeader == 'Calculated  volume, µm3'): return 'Calculated volume, µm3' # Modified
#         if (importFileHeader == 'Calculated  volume µm3'): return 'Calculated volume, µm3' # Modified
#         if (importFileHeader == 'Comment'): return 'Comment'
#         if (importFileHeader == 'Filament: length of cell (µm)'): return 'Filament: length of cell, µm' # Modified
#         if (importFileHeader == 'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return 'Calculated Carbon pg/counting unit' # Modified
#         if (importFileHeader == 'Calculated Carbon pg/counting unit'): return 'Calculated Carbon pg/counting unit' # Modified
#     #    if (importFileHeader == 'Comment on Carbon calculation'): return 'Comment on Carbon calculation'
#         if (importFileHeader == 'CORRECTION / ADDITION                            2009'): return 'Correction/addition 2009' # Modified
#         if (importFileHeader == 'CORRECTION / ADDITION                            2010'): return 'Correction/addition 2010' # Modified
#         if (importFileHeader == 'CORRECTION / ADDITION                            2011'): return 'Correction/addition 2011' # Modified
#         if (importFileHeader == 'Corrections/Additions 2013'): return 'Corrections/additions 2013' # Modified
#         return importFileHeader     
#         
#     def _isBvolTaxonRelated(self, header, column):
#         """ Used when importing BVOL data. """        
#         if (header[column] == 'Division'): return True
#         if (header[column] == 'Class'): return True
#         if (header[column] == 'Order'): return True
#         if (header[column] == 'Species'): return True
#         if (header[column] == 'Author'): return True
#         if (header[column] == 'SFLAG'): return True
#         if (header[column] == 'Stage'): return True
#         ###if (header[column] == 'Trophic type'): return True
#         if (header[column] == 'Geometric shape'): return True
#         if (header[column] == 'Formula'): return True
#         return False # Related to size class.     
#         
#     def _isBvolColumnNumeric(self, header, column):
#         """ Used when importing BVOL data. """        
#         if (header[column] == 'Size class'): return False # Note: Should be handled as unicode. Could be empty string.
#         if (header[column] == 'Length(l1), µm'): return True
#         if (header[column] == 'Length(l2), µm'): return True
#         if (header[column] == 'Width(w), µm'): return True
#         if (header[column] == 'Height(h), µm'): return True
#         if (header[column] == 'Diameter(d1), µm'): return True
#         if (header[column] == 'Diameter(d2), µm'): return True
#         if (header[column] == 'No. of cells/counting unit'): return True
#         if (header[column] == 'Calculated volume, µm3'): return True
#         if (header[column] == 'Filament: length of cell, µm'): return True
#         if (header[column] == 'Calculated Carbon pg/counting unit'): return True
#         return False

    def getPlanktonGroupFromTaxonName(self, scientific_name):
        """ This is another way to organize organisms into groups. Other than the traditional classification. """
        #
        if scientific_name in self._planktongroups_lookup:
            # Fast lookup. Don't do the heavy work more than needed.
            return self._planktongroups_lookup[scientific_name]
        else:
            for rank in self._planktongroups_ranks_set:
                #
                if rank == 'scientific_name':
                    taxon_on_rank = scientific_name
                else:
                    taxon_on_rank = self.getTaxonValue(scientific_name, rank)
                #
                if taxon_on_rank in self._planktongroups_rank_dict[rank]:
                    planktongroup = self._planktongroups_rank_dict[rank][taxon_on_rank]
                    self._planktongroups_lookup[scientific_name] = planktongroup
                    return planktongroup
        #                            
#        return 'plankton-group-not-designated'
        envmonlib.Logging().warning('Not match for Plankton group. "Others" assigned for: ' + scientific_name)
        #
        return 'Others'

    def _getFilesByPrefix(self, prefix):
        """ """
        xslx_files = {}
        # Search for all files starting with the prefix value and ends with '.xslx'.
        for root, dirs, files in os.walk(self._species_directory_path):
            for filename in files:
                if filename.startswith(prefix) and \
                   filename.endswith('.xlsx'):
#                     print ('DEBUG: ' + os.path.join(root, filename))
                    xslx_files[filename] = os.path.join(root, filename)
        # If versions of files is used, only get the latest one.
        latest_files = {}
        for key in sorted(xslx_files.keys()):
            name_without_version, version = self._splitFilenameOnVersion(key)
            # Overwrite if a later version exists. Note: The keys are sorted.
            latest_files[name_without_version] = xslx_files[key]
        # 
        return latest_files.values()

    def _splitFilenameOnVersion(self, file_name):
        """ """
        filename = os.path.splitext(file_name)[0]
        parts = filename.split('version')
        name = parts[0].strip('_').strip()
        version = parts[1].strip('_').strip() if len(parts) > 1 else ''
        #
        return name, version

