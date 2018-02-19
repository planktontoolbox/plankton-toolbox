#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import toolbox_utils
import os.path
from numpy import rank

@toolbox_utils.singleton
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
                 species_directory_path = 'plankton_toolbox_data/species/'):
        # Parameters.
        self._species_directory_path = species_directory_path
        # Taxa files.
        self._taxa_filenames = self._get_files_by_prefix('taxa_')
        # Translate files.
        self._taxatranslate_filenames = self._get_files_by_prefix('translate_')
        # Synonyms files.
        self._taxasynonyms_filenames = self._get_files_by_prefix('synonyms_')
        # Biovolume, mapping information for used columns.
        self._bvolcolumns_filenames = self._get_files_by_prefix('bvolcolumns_')
        # Biovolume files.
        self._bvol_filenames = self._get_files_by_prefix('bvol_')
        # Plankton groups definition. Useful grouping that differ from 
        self._planktongroups_filenames = self._get_files_by_prefix('planktongroups_')
        # Trophic type files.
        self._trophictype_filenames = self._get_files_by_prefix('trophictype_')
        # Harmful algae files.
        self._harmful_filenames = self._get_files_by_prefix('harmful_')

        # Defines local storage by calling clear().
        self._clear()
                
        try:
            # Only done once since the class is declared as singleton.
            self._load_all_data()
        except Exception as e:
            toolbox_utils.Logging().error('Failed when loading species related files: ' + str(e))            
            raise

    def get_taxa_dict(self):
        """ """
        return self._taxa 
    
    def get_taxa_lookup_dict(self):
        """ """
        return self._taxa_lookup 
    
    def get_taxon_dict(self, scientific_name):
        """ """
        if scientific_name in self._taxa_lookup:
            return self._taxa_lookup[scientific_name]
        #
        return {} 
    
    def get_taxon_value(self, scientific_name, key):
        """ """
        key_lower = key.lower()
        if scientific_name in self._taxa_lookup:
            return self._taxa_lookup[scientific_name].get(key_lower, '')
        #
        return ''
    
    def get_bvol_dict(self, scientific_name, size_class):
        """ """
        if scientific_name in self._taxa_lookup:
            speciesobject = self._taxa_lookup[scientific_name]
            if 'size_classes' in speciesobject:
                for sizeclassobject in speciesobject['size_classes']:
                    if sizeclassobject.get('bvol_size_class', '') == str(size_class):
                        return sizeclassobject
        #
        return {}

    def get_bvol_value(self, scientific_name, size_class, key):
        """ """
        if scientific_name in self._taxa_lookup:
            speciesobject = self._taxa_lookup[scientific_name]
            if 'size_classes' in speciesobject:
                for sizeclassobject in speciesobject['size_classes']:
                    if sizeclassobject.get('bvol_size_class', '') == str(size_class):
                        return sizeclassobject.get(key, '')
        #
        return '' 
    
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

    def _load_all_data(self):
        """ """
        try:
            self._clear()
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Loading species lists (located in "' + self._species_directory_path + '"):')
            
            # Load taxa.
            for excelfilename in self._taxa_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Species and other taxa)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_taxa(excelfilename)
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    
                                    
            # Add translated scientific names to taxa.
            for excelfilename in self._taxatranslate_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Misspellings etc.)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_synonyms(excelfilename) # Synonyms and translated names are handled the same way.                           
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    
            
            # Add synonyms to taxa. Note: 'translate_to_' will be added to filenames.
            for excelfilename in self._taxasynonyms_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Synonyms for taxa)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_synonyms(excelfilename)                            
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    
            
            # Load biovolume column mapping information.
            for excelfilename in self._bvolcolumns_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Biovolume column mapping)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_bvol_columns(excelfilename)        
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    

            # Load BVOL species data.
            for excelfilename in self._bvol_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Biovolumes etc. for sizeclasses)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_bvol(excelfilename)        
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    

            # Load trophic types.
            for excelfilename in self._trophictype_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Trophic types)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_trophic_types(excelfilename)
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    

            # Load harmful species.
            for excelfilename in self._harmful_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Harmful organisms)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_harmful(excelfilename)
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows()    

            # Load plankton group definition.
            for excelfilename in self._planktongroups_filenames:
                if os.path.exists(excelfilename):
                    toolbox_utils.Logging().log('') # Empty line.
                    toolbox_utils.Logging().log('- ' + os.path.basename(excelfilename) + ' (Plankton group definition)')
                    try:
                        toolbox_utils.Logging().start_accumulated_logging()
                        #
                        self._load_plankton_group_definition(excelfilename)
                    finally:
                        toolbox_utils.Logging().log_all_accumulated_rows() 
            
            # Perform some useful pre-calculations.
            self._precalculate_data()
        #
        except Exception as e:
            toolbox_utils.Logging().error('Failed when loading species data: ' + str(e))            
            raise
            
    def _load_trophic_types(self, excel_file_name):
        """ Adds trophic type info to the species objects. """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        for row in tablefilereader.rows():
            scientificname = ''
            try:
                scientificname = row[0].strip() # Scientific name.
                sizeclass = row[1].strip() # Size class.
                trophictype = row[2].strip() # Trophic type.
                #
                if scientificname in self._taxa_lookup:
                    taxon = self._taxa_lookup[scientificname]
                    #
                    if sizeclass:
#                         sizeclassfound = False
                        if 'size_classes' in taxon:
                            for sizeclassdict in taxon['size_classes']:
                                if sizeclassdict.get('bvol_size_class', '') == sizeclass:
                                    if sizeclassdict.get('trophic_type', ''):
                                        if scientificname == taxon['scientific_name']:
#                                             toolbox_utils.Logging().warning('Same taxon/size on multiple rows: ' + scientificname + ' Size: ' + sizeclass + '   (Source: ' + excel_file_name + ')')
#                                             sizeclassfound = True
                                            break
                                    #
                                    sizeclassdict['trophic_type'] = trophictype
#                                     sizeclassfound = True
                                    break
                        #
#                         if sizeclassfound == False:
#                             toolbox_utils.Logging().warning('Size class is missing: ' + scientificname + ' Size: ' + sizeclass + '   (Source: ' + excel_file_name + ')')
                    else:
                        # No sizeclass in indata file. Put on species level.                        
                        taxon['trophic_type'] = trophictype
                else:
#                     toolbox_utils.Logging().warning('Scientific name is missing: ' + scientificname + '   (Source: ' + excel_file_name + ')')
                    pass
            except:
                toolbox_utils.Logging().warning('Failed when loading trophic types. File:' + excel_file_name + '  Taxon: ' + scientificname)

    def _load_taxa(self, excel_file_name):
        """ Creates one data object for each taxon. """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        header = tablefilereader.header()
        for row in tablefilereader.rows():
            
            row_dict = dict(zip(header, row))
            
            scientificname = ''
            try:
#                 scientificname = row[0].strip() # ScientificName.
#                 author = row[1].strip() if row[1].strip() != 'NULL' else '' # Author.
#                 rank = row[2].strip() # Rank.
#                 parentname = row[3].strip() # Parent.
                scientificname = row_dict.get('scientific_name', '').strip() # ScientificName.
                author = row_dict.get('author', '').strip() # Author.
                rank = row_dict.get('rank', '').strip() # Rank.
                parentname = row_dict.get('parent_name', '').strip() # Parent.
                #
                if scientificname:
                    if scientificname not in self._taxa:
                        self._taxa[scientificname] = {}
                        # Lookup dictionary.
                        self._taxa_lookup[scientificname] = self._taxa[scientificname]
                    else:
                        toolbox_utils.Logging().warning('Scientific name added twice: ' + scientificname + '   (Source: ' + excel_file_name + ')')
                    #    
                    speciesobject = self._taxa[scientificname]
                    speciesobject['scientific_name'] = scientificname
                    speciesobject['author'] = author
                    speciesobject['rank'] = rank
                    speciesobject['parent_name'] = parentname
            except:
                toolbox_utils.Logging().warning('Failed when loading taxa. File:' + excel_file_name + '  Taxon: ' + scientificname)
                

    def _load_synonyms(self, excel_file_name):
        """ Add synonyms from 'translate_' or 'synonyms_' files. """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        for row in tablefilereader.rows():
            toname = ''
            fromname = ''
            try:
                toname = row[1].strip()
                fromname = row[0].strip()
                #
                
                
                # Check if from name is a valid name.
                if fromname in self._taxa_lookup:
                    toolbox_utils.Logging().warning('Invalid translate (valid taxa in first column): ' + fromname + '   (Source: ' + excel_file_name + ')')
                    continue
                
                
                #
                if toname in self._taxa_lookup:
                    taxon = self._taxa_lookup[toname]
                    if not 'synonyms' in self._taxa[toname]:
                        taxon['synonyms'] = []
                    taxon['synonyms'].append(fromname)
                    # Lookup dictionary.
                    self._taxa_lookup[fromname] = self._taxa[toname]
                else:
                    toolbox_utils.Logging().warning('Scientific name is missing: ' + toname + '   (Source: ' + excel_file_name + ')')
            except:
                toolbox_utils.Logging().warning('Failed when loading translates/synonyms. File:' + excel_file_name + '  From taxon: ' + toname)
                    
    def _load_harmful(self, excel_file_name):
        """ Adds info about harmfulness to the species objects. """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        header = tablefilereader.header()
        for row in tablefilereader.rows():
            scientific_name = ''
            accepted_name_usage = ''
            try:
                row_dict = dict(zip(header, row))
                scientific_name = row_dict.get('scientific_name', None).strip()
                accepted_name_usage = row_dict.get('accepted_name_usage', None).strip() # Valid scientific name. 
                #
                if scientific_name and (scientific_name in self._taxa_lookup):
                    # print('Harmful: scientific_name: ' + scientific_name)
                    taxon = self._taxa_lookup[scientific_name]
                    taxon['harmful_name'] = scientific_name
                    taxon['harmful'] = True
                if not (scientific_name == accepted_name_usage): 
                    if accepted_name_usage and (accepted_name_usage in self._taxa_lookup):
                        # print('Harmful: accepted_name_usage: ' + accepted_name_usage + ' ( scientific_name: ' + scientific_name + ')')
                        taxon = self._taxa_lookup[accepted_name_usage]
                        taxon['harmful_name'] = accepted_name_usage
                        taxon['harmful'] = True 
#                 else:
#                     toolbox_utils.Logging().warning('Scientific name is missing: ' + scientific_name + '   (Source: ' + excel_file_name + ')')
            except:
                toolbox_utils.Logging().warning('Failed when loading harmful algae. File:' + excel_file_name + '  Taxon: ' + scientific_name)

    def _load_plankton_group_definition(self, excel_file_name):
        """ """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        for row in tablefilereader.rows():
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
                toolbox_utils.Logging().warning('Failed when loading plankton group def. File:' + excel_file_name + '  Taxon: ' + scientificname)
    
    def _precalculate_data(self):
        """ Calculates data from loaded datasets. I.e. phylum, class and order info. """
        for speciesobject in self._taxa.values():
            scientificname = ''
            try:
                scientificname = speciesobject['scientific_name']
                counter = 0
                parentobject = speciesobject
                while parentobject:
                    counter += 1
                    if counter > 20:
                        parentobject = None # Too many levels, or infinite loop.
#                         print('DEBUG: Species._precalculate_data(): Too many levels, or infinite loop.')
                        continue
                    if 'rank' in parentobject:
                        if parentobject['rank'] == 'Species':
                            speciesobject['taxon_species'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Genus':
                            speciesobject['taxon_genus'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Family':
                            speciesobject['taxon_family'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Order':
                            speciesobject['taxon_order'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Class':
                            speciesobject['taxon_class'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Phylum':
                            speciesobject['taxon_phylum'] = parentobject['scientific_name']
                        if parentobject['rank'] == 'Kingdom':
                            speciesobject['taxon_kingdom'] = parentobject['scientific_name']
                            parentobject = None # Done. Continue with next.
                            continue
                    # One step up in hierarchy.
                    if 'parent_name' in parentobject:
                        if parentobject['parent_name'] in self._taxa:
                            parentobject = self._taxa[parentobject['parent_name']] if parentobject['parent_name'] else None
                        else:
                            if parentobject['scientific_name'] != 'Biota':
                                toolbox_utils.Logging().warning('Parent taxon is missing for : ' + parentobject['scientific_name'])
                            parentobject = None
                    else:
                        parentobject = None
            except:
                toolbox_utils.Logging().warning('Failed when creating classification. Taxon: ' + scientificname)

    def _load_bvol_columns(self, excel_file_name):
        """ """
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        for row in tablefilereader.rows():
            columnname = ''
            try:
                # Header: column_name, used_on_rank_level, numeric, internal_toolbox_name.
                columnname = row[0].strip()
                level = row[1].strip()
                numeric = row[2].strip()
                internalname = row[3].strip()
                #
                if columnname and level and internalname:
                    self._bvolcolumns_dict[columnname] = (level, numeric, internalname) 
            except:
                toolbox_utils.Logging().warning('Failed when loading BVOL columns. Column name: ' + columnname)
        
    def _load_bvol(self, excel_file_name):
        """ Adds BVOL data to species objects. Creates additional species objects if missing 
            (i.e. for Unicell, Flagellates). """
        # Import size class data.
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = excel_file_name)
        #
        # Create header list for mapping and translations.
        headerinfo = [] # Contains used columns only.
        for columnindex, columnname in enumerate(tablefilereader.header()): 
            # Use loaded information on used columns.
            if columnname in self._bvolcolumns_dict:
                level, numeric, internalname = self._bvolcolumns_dict[columnname]
                headerinfo.append((columnindex, columnname, level, numeric, internalname))
        #
        for row in tablefilereader.rows():
            taxondict = {}
            sizeclassdict = {}
            try:
###                for column, value in enumerate(row):
                for columnindex, columnname, level, numeric, internalname in headerinfo:
                    value = row[columnindex].strip()
                    
                    if len(value) > 0:
                        # Separate columns contains taxon and size-class related info.                
                        if level == 'taxon':
#                         if level == 'scientific_name':
                            taxondict[internalname] = value
                        elif level == 'size_class':
                            if (internalname == 'bvol_size_class'):
                                try:
                                    # Convert from float to integer and back to str. Excel related problem.
                                    sizeclassdict[internalname] = str(int(float(value)))
                                except:
                                    sizeclassdict[internalname] = '<ERROR>'
                            #        
                            if numeric == 'numeric':
                                try:
                                    value = value.replace(',', '.').replace(' ', '') # Try/except if already float.
                                except: 
                                    pass
                                sizeclassdict[internalname] = value
                            else:
                                sizeclassdict[internalname] = value
                # Check if exists in self._taxa
                if 'bvol_species' in taxondict: 
                    scientificname = taxondict['bvol_species']
                    if scientificname in self._taxa_lookup:
                        speciesobject = self._taxa_lookup[scientificname]
                    else:
                        size = sizeclassdict.get('bvol_size_class', '')
                        toolbox_utils.Logging().warning('Scientific name is missing: ' + scientificname + '   Size: ' + size + '   (Source: ' + excel_file_name + ')')
                        continue # Only add BVOL info if taxon exists in taxa.
                    #
                    speciesobject['bvol_name'] = scientificname
                    #
                    if 'size_classes' not in speciesobject:
                        speciesobject['size_classes'] = []
                        # Add other bvol data to taxon.
                        for key in taxondict.keys():
                            speciesobject[key] = taxondict[key]
                    #
                    
                    # Check if size class already exists.
                    for old_sizeclassdict in speciesobject['size_classes']:
                        if old_sizeclassdict.get('bvol_size_class', '') == sizeclassdict.get('bvol_size_class', ''):
                            toolbox_utils.Logging().warning('Size-class already exists for: ' + scientificname + '   Size: ' + sizeclassdict.get('bvol_size_class', '') + '   (Source: ' + excel_file_name + ')')
                    #
                    speciesobject['size_classes'].append(sizeclassdict)
            except:
                toolbox_utils.Logging().warning('Failed when loading BVOL data.')

    def get_plankton_group_from_taxon_name(self, scientific_name):
        """ This is another way to organize organisms into groups. Other than the traditional classification. """
        #
        if scientific_name in self._planktongroups_lookup:
            # Fast lookup. Don't do the heavy work more than needed.
            return self._planktongroups_lookup[scientific_name]
        else:
            try:
                # Check classification.
                taxon_name = scientific_name
                limit_counter = 0
                while taxon_name and (limit_counter < 20):
                    limit_counter += 1
                    taxon_dict = self.get_taxon_dict(taxon_name)
                    taxon_name = taxon_dict.get('scientific_name', '')
                    taxon_rank = taxon_dict.get('rank', '')
                    parent_name = taxon_dict.get('parent_name', '')
                    #
                    if taxon_rank in self._planktongroups_rank_dict.keys():
                        if taxon_name in self._planktongroups_rank_dict[taxon_rank].keys():
                            planktongroup = self._planktongroups_rank_dict[taxon_rank][taxon_name]
                            self._planktongroups_lookup[scientific_name] = planktongroup
                            return planktongroup
                    #
                    if (parent_name == '') or (taxon_name == parent_name):
                        break
                    else:
                        taxon_name = parent_name
            #
            except: 
                pass
        #                            
        toolbox_utils.Logging().warning('Not match for Plankton group. "OTHERS" assigned for: ' + scientific_name)
        self._planktongroups_lookup[scientific_name] = 'OTHERS'
        return 'OTHERS'

    def _get_files_by_prefix(self, prefix):
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
            name_without_version, version = self._split_filename_on_version(key)
            # Overwrite if a later version exists. Note: The keys are sorted.
            latest_files[name_without_version] = xslx_files[key]
        # 
        return latest_files.values()

    def _split_filename_on_version(self, file_name):
        """ """
        filename = os.path.splitext(file_name)[0]
        parts = filename.split('version')
        name = parts[0].strip('_').strip()
        version = parts[1].strip('_').strip() if len(parts) > 1 else ''
        #
        return name, version

