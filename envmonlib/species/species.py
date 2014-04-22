#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

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
                 species_directory_path = u'toolbox_data/species/'):
        # Parameters.
        self._species_directory_path = species_directory_path
        # Taxa files.
        self._taxa_filenames = self._getFilesByPrefix(u'taxa_')
        # Translate files.
        self._taxatranslate_filenames = self._getFilesByPrefix(u'translate_')
        # Synonyms files.
        self._taxasynonyms_filenames = self._getFilesByPrefix(u'synonyms_')
        # Biovolume, mapping information for used columns.
        self._bvolcolumns_filenames = self._getFilesByPrefix(u'bvolcolumns_')
        # Biovolume files.
        self._bvol_filenames = self._getFilesByPrefix(u'bvol_')
        # Plankton groups definition. Useful grouping that differ from 
        self._planktongroups_filenames = self._getFilesByPrefix(u'planktongroups_')
        # Harmful algae files.
        self._harmful_filenames = self._getFilesByPrefix(u'harmful_')

        # Defines local storage by calling clear().
        self._clear()
                
        try:
            # Only done once since the class is declared as singleton.
            self._loadAllData()
        except Exception, e:
            envmonlib.Logging().error(u"Failed when loading species related files: " + unicode(e))            
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
            return self._taxa_lookup[scientific_name].get(key, u'')
        return u''
    
    def getBvolValue(self, scientific_name, size_class, key):
        """ """
        if scientific_name in self._taxa_lookup:
            speciesobject = self._taxa_lookup[scientific_name]
            if u'Size classes' in speciesobject:
                for sizeclassobject in speciesobject[u'Size classes']:
                    if sizeclassobject.get(u'Size class', u'') == unicode(size_class):
                        return sizeclassobject.get(key, u'')
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
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log(u"Loading species lists (located in " +self._species_directory_path + "'):")
            
            # Load taxa.
            for excelfilename in self._taxa_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log(u"- " + os.path.basename(excelfilename) + u" (Species and other taxa)")
                    self._loadTaxa(excelfilename)
                                    
            # Add translated scientific names to taxa.
            for excelfilename in self._taxatranslate_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log(u"- " + os.path.basename(excelfilename) + u" (Misspellings etc.)")
                    self._loadSynonyms(excelfilename) # Synonyms and translated names are handled the same way.                           
            
            # Add synonyms to taxa. Note: 'translate_to_' will be added to filenames.
            for excelfilename in self._taxasynonyms_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log(u"- " + os.path.basename(excelfilename) + u" (Synonyms for taxa)")
                    self._loadSynonyms(excelfilename)                            
            
            # Load biovolume column mapping information.
            for excelfilename in self._bvolcolumns_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log("- " + os.path.basename(excelfilename) + u" (Biovolume column mapping)")
                    self._loadBvolColumns(excelfilename)        

            # Load BVOL species data.
            for excelfilename in self._bvol_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log("- " + os.path.basename(excelfilename) + u" (Biovolumes etc. for sizeclasses)")
                    self._loadBvol(excelfilename)        

            # Load harmful species.
            for excelfilename in self._harmful_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log(u"- " + os.path.basename(excelfilename) + u" (Harmful organisms)")
                    self._loadHarmful(excelfilename)

            # Load plankton group definition.
            for excelfilename in self._planktongroups_filenames:
                if os.path.exists(excelfilename):
                    envmonlib.Logging().log(u"- " + os.path.basename(excelfilename) + u" (Plankton group definition)")
                    self._loadPlanktonGroupDefinition(excelfilename)

            
            # Perform some useful pre-calculations.
            self._precalculateData()
        #
        except Exception, e:
            envmonlib.Logging().error(u"Failed when loading species data: " + unicode(e))            
            raise
            
#        # Used for DEBUG:
#        import locale
#        import codecs
#        import json
#        fileencoding = locale.getpreferredencoding()
#        out = codecs.open(u'DEBUG_species_list.txt', mode = 'w', encoding = fileencoding)
#        out.write(json.dumps(self._taxa, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()
#        # DEBUG end.

    def _loadTaxa(self, excel_file_name):
        """ Creates one data object for each taxon. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
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
                    envmonlib.Logging().warning(u"Scientific name added twice: " + scientificname + u"   (Source: " + excel_file_name + u")")
                #    
                speciesobject = self._taxa[scientificname]
                speciesobject[u'Scientific name'] = scientificname
                speciesobject[u'Author'] = author
                speciesobject[u'Rank'] = rank
                speciesobject[u'Parent name'] = parentname

    def _loadSynonyms(self, excel_file_name):
        """ Add synonyms from 'translate_' or 'synonyms_' files. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            toname = row[1].strip()
            fromname = row[0].strip()
            #
            if toname in self._taxa_lookup:
                taxon = self._taxa_lookup[toname]
                if not u'Synonyms' in self._taxa[toname]:
                    taxon[u'Synonyms'] = []
                taxon[u'Synonyms'].append(fromname)
                # Lookup dictionary.
                self._taxa_lookup[fromname] = self._taxa[toname]
            else:
                envmonlib.Logging().warning(u"Scientific name is missing: " + toname + u"   (Source: " + excel_file_name + u")")
                    
    def _loadHarmful(self, excel_file_name):
        """ Adds info about harmfulness to the species objects. """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = row[0].strip() # Scientific name.
            aphiaid = row[1] if row[1].strip() != 'NULL' else '' # Aphia id.
            #
            if scientificname in self._taxa_lookup:
                taxon = self._taxa_lookup[scientificname]
                taxon[u'Harmful name'] = scientificname
                taxon[u'Harmful'] = True 
                taxon[u'Aphia id'] = aphiaid
            else:
                envmonlib.Logging().warning(u"Scientific name is missing: " + scientificname + u"   (Source: " + excel_file_name + u")")

    def _loadPlanktonGroupDefinition(self, excel_file_name):
        """ """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = row[0].strip() # Scientific name.
            rank = row[1].strip() # Rank.
            planktongroup = row[2].strip() # Plankton group.
            #
            if scientificname and planktongroup:
                used_rank = rank
                if not used_rank:
                    used_rank = u'scientific_name'
                self._planktongroups_ranks_set.add(used_rank)
                #
                if used_rank not in self._planktongroups_rank_dict:
                    self._planktongroups_rank_dict[used_rank] = {}
                self._planktongroups_rank_dict[used_rank][scientificname] = planktongroup
    
    def _precalculateData(self):
        """ Calculates data from loaded datasets. I.e. phylum, class and order info. """
        for speciesobject in self._taxa.values():
            counter = 0
            parentobject = speciesobject
            while parentobject:
                counter += 1
                if counter > 20:
                    parentobject = None # Too many levels, or infinite loop.
                    print(u'DEBUG: Species._precalculateData(): Too many levels, or infinite loop.')
                    continue
                if u'Rank' in parentobject:
                    if parentobject[u'Rank'] == u'Species':
                        speciesobject[u'Species'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Genus':
                        speciesobject[u'Genus'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Order':
                        speciesobject[u'Order'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Class':
                        speciesobject[u'Class'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Phylum':
                        speciesobject[u'Phylum'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Kingdom':
                        speciesobject[u'Kingdom'] = parentobject[u'Scientific name']
                        parentobject = None # Done. Continue with next.
                        continue
                # One step up in hierarchy.
                if u'Parent name' in parentobject:
                    if parentobject[u'Parent name'] in self._taxa:
                        parentobject = self._taxa[parentobject[u'Parent name']] if parentobject[u'Parent name'] else None
                    else:
                        if parentobject[u'Scientific name'] != u'Biota':
                            envmonlib.Logging().warning(u"Parent taxon is missing for : " + parentobject[u'Scientific name'])
                        parentobject = None
                else:
                    parentobject = None

    def _loadBvolColumns(self, excel_file_name):
        """ """
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            # Header: Column name, Used on level, Numeric, Internal toolbox name.
            columnname = row[0].strip()
            level = row[1].strip()
            numeric = row[2].strip()
            internalname = row[3].strip()
            #
            if columnname and level and internalname:
                self._bvolcolumns_dict[columnname] = (level, numeric, internalname) 
        
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
###            for column, value in enumerate(row):
            for columnindex, columnname, level, numeric, internalname in headerinfo:
                value = row[columnindex].strip()
                
                if len(value) > 0:
                    # Separate columns contains taxon and size-class related info.                
                    if level == u'Taxon':
                        taxondict[internalname] = value
                    else:
                        if (internalname == u'Size class'):
                            try:
                                # Convert from float to integer and back to unicode. Excel related problem.
                                sizeclassdict[internalname] = unicode(int(float(value)))
                            except:
                                sizeclassdict[internalname] = u''
                        elif numeric == u'Numeric':
                            sizeclassdict[internalname] = value.replace(',', '.')
                        else:
                            sizeclassdict[internalname] = value
            # Check if exists in self._taxa
            if u'BVOL Species' in taxondict: 
                scientificname = taxondict[u'BVOL Species']
                if scientificname in self._taxa_lookup:
                    speciesobject = self._taxa_lookup[scientificname]
                else:
                    size = sizeclassdict.get(u'Size class', u'')
                    envmonlib.Logging().warning(u"Scientific name is missing: " + scientificname + u"   Size: " + size + u"   (Source: " + excel_file_name + u")")
                    continue # Only add BVOL info if taxon exists in taxa.
                #
                speciesobject[u'BVOL name'] = scientificname
                #
                if u'Size classes' not in speciesobject:
                    speciesobject[u'Size classes'] = []
                    # Add other bvol data to taxon.
                    for key in taxondict.keys():
                        speciesobject[key] = taxondict[key]
                #
                speciesobject[u'Size classes'].append(sizeclassdict)
        #
        # Trophy is set on sizeclass level. Should also be set on species level  
        # if all sizeclasses have the same trophy.
        for taxon in self._taxa.values():
            trophyset = set() 
            if u'Size classes' in taxon:
                for sizeclass in taxon[u'Size classes']:
                    trophyset.add(sizeclass.get(u'Trophy', u''))
            if len(trophyset) == 1:
                taxon[u'Trophy'] = list(trophyset)[0]

                    
#     def _translateBvolHeader(self, importFileHeader):
#         """ Convert import file column names to key names used in dictionary. """        
#     #        if (importFileHeader == u'Division'): return u'Division'
#     #        if (importFileHeader == u'Class'): return u'Class'
#     #        if (importFileHeader == u'Order'): return u'Order'
#     #        if (importFileHeader == u'Species'): return u'Species'
#         if (importFileHeader == u'SFLAG (sp., spp., cf., complex, group)'): return u'SFLAG' # Modified
#         if (importFileHeader == u'STAGE (cyst, naked)'): return u'Stage' # Modified
#     #        if (importFileHeader == u'Author'): return u'Author'
#     #        if (importFileHeader == u'AphiaID'): return u'AphiaID'
#     #        if (importFileHeader == u'Trophy'): return u'Trophy'
#     #        if (importFileHeader == u'Geometric shape'): return u'Geometric shape'
#         if (importFileHeader == u'FORMULA'): return u'Formula' # Modified
#         if (importFileHeader == u'Size class No'): return u'Size class' # Modified
#         if (importFileHeader == u'SizeClassNo'): return u'Size class' # Modified
#         if (importFileHeader == u'Nonvalid_SIZCL'): return u'Nonvalid size class' # Modified
#         if (importFileHeader == u'Not_accepted'): return u'Not accepted' # Modified
#     #        if (importFileHeader == u'Unit'): return u'Unit'
#         if (importFileHeader == u'size range,'): return u'Size range' # Modified
#         if (importFileHeader == u'Length (l1), µm'): return u'Length(l1), µm' # Modified
#         if (importFileHeader == u'Length(l1)µm'): return u'Length(l1), µm' # Modified
#         if (importFileHeader == u'Length (l2), µm'): return u'Length(l2), µm' # Modified
#         if (importFileHeader == u'Length(l2)µm'): return u'Length(l2), µm' # Modified
#         if (importFileHeader == u'Width (w), µm'): return u'Width(w), µm' # Modified
#         if (importFileHeader == u'Width(w)µm'): return u'Width(w), µm' # Modified
#         if (importFileHeader == u'Height (h), µm'): return u'Height(h), µm' # Modified
#         if (importFileHeader == u'Height(h)µm'): return u'Height(h), µm' # Modified
#         if (importFileHeader == u'Diameter (d1), µm'): return u'Diameter(d1), µm' # Modified
#         if (importFileHeader == u'Diameter(d1)µm'): return u'Diameter(d1), µm' # Modified
#         if (importFileHeader == u'Diameter (d2), µm'): return u'Diameter(d2), µm' # Modified
#         if (importFileHeader == u'Diameter(d2)µm'): return u'Diameter(d2), µm' # Modified
#         if (importFileHeader == u'No. of cells/ counting unit'): return u'No. of cells/counting unit' # Modified
#         if (importFileHeader == u'Calculated  volume, µm3'): return u'Calculated volume, µm3' # Modified
#         if (importFileHeader == u'Calculated  volume µm3'): return u'Calculated volume, µm3' # Modified
#         if (importFileHeader == u'Comment'): return u'Comment'
#         if (importFileHeader == u'Filament: length of cell (µm)'): return u'Filament: length of cell, µm' # Modified
#         if (importFileHeader == u'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return u'Calculated Carbon pg/counting unit' # Modified
#         if (importFileHeader == u'Calculated Carbon pg/counting unit'): return u'Calculated Carbon pg/counting unit' # Modified
#     #    if (importFileHeader == u'Comment on Carbon calculation'): return u'Comment on Carbon calculation'
#         if (importFileHeader == u'CORRECTION / ADDITION                            2009'): return u'Correction/addition 2009' # Modified
#         if (importFileHeader == u'CORRECTION / ADDITION                            2010'): return u'Correction/addition 2010' # Modified
#         if (importFileHeader == u'CORRECTION / ADDITION                            2011'): return u'Correction/addition 2011' # Modified
#         if (importFileHeader == u'Corrections/Additions 2013'): return u'Corrections/additions 2013' # Modified
#         return importFileHeader     
#         
#     def _isBvolTaxonRelated(self, header, column):
#         """ Used when importing BVOL data. """        
#         if (header[column] == u'Division'): return True
#         if (header[column] == u'Class'): return True
#         if (header[column] == u'Order'): return True
#         if (header[column] == u'Species'): return True
#         if (header[column] == u'Author'): return True
#         if (header[column] == u'SFLAG'): return True
#         if (header[column] == u'Stage'): return True
#         ###if (header[column] == u'Trophy'): return True
#         if (header[column] == u'Geometric shape'): return True
#         if (header[column] == u'Formula'): return True
#         return False # Related to size class.     
#         
#     def _isBvolColumnNumeric(self, header, column):
#         """ Used when importing BVOL data. """        
#         if (header[column] == u'Size class'): return False # Note: Should be handled as unicode. Could be empty string.
#         if (header[column] == u'Length(l1), µm'): return True
#         if (header[column] == u'Length(l2), µm'): return True
#         if (header[column] == u'Width(w), µm'): return True
#         if (header[column] == u'Height(h), µm'): return True
#         if (header[column] == u'Diameter(d1), µm'): return True
#         if (header[column] == u'Diameter(d2), µm'): return True
#         if (header[column] == u'No. of cells/counting unit'): return True
#         if (header[column] == u'Calculated volume, µm3'): return True
#         if (header[column] == u'Filament: length of cell, µm'): return True
#         if (header[column] == u'Calculated Carbon pg/counting unit'): return True
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
                if rank == u'scientific_name':
                    taxon_on_rank = scientific_name
                else:
                    taxon_on_rank = self.getTaxonValue(scientific_name, rank)
                #
                if taxon_on_rank in self._planktongroups_rank_dict[rank]:
                    planktongroup = self._planktongroups_rank_dict[rank][taxon_on_rank]
                    self._planktongroups_lookup[scientific_name] = planktongroup
                    return planktongroup
        #                            
#        return u'plankton-group-not-designated'
        envmonlib.Logging().warning(u"Not match for Plankton group. 'Others' assigned for: " + scientific_name)
        #
        return u'Others'

    def _getFilesByPrefix(self, prefix):
        """ """
        xslx_files = {}
        # Search for all files starting with the prefix value and ends with '.xslx'.
        for root, dirs, files in os.walk(self._species_directory_path):
            for filename in files:
                if filename.startswith(prefix) and \
                   filename.endswith(u'.xlsx'):
#                     print (u'DEBUG: ' + os.path.join(root, filename))
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
        parts = filename.split(u'version')
        name = parts[0].strip(u'_').strip()
        version = parts[1].strip(u'_').strip() if len(parts) > 1 else u''
        #
        return name, version

