#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2012 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import envmonlib
#import codecs
#import json
#import locale

@envmonlib.singleton
class Species(object):
    """ """
    def __init__(self,
                 taxa_filenames = [u'toolbox_data/species/Dyntaxa_species.xlsx',
                                   u'toolbox_data/species/SMHI_species.xlsx'], 
                 sizeclasses_filenames = [u'toolbox_data/species/PEG_BVOL2011.xlsx',
                                          u'toolbox_data/species/SMHI_BVOL2011.xlsx'], 
                 sizeclasses_to_taxa_filename = u'toolbox_data/species/Translate_sizeclasses_to_dyntaxa.xlsx', 
                 harmful_filename = u'toolbox_data/species/SMHI_harmful_species.xlsx', 
                 harmful_to_taxa_filename = u'toolbox_data/species/translate_harmful_to_taxa.xlsx'):
        # Parameters.
        self._taxa_filenames = taxa_filenames 
        self._sizeclasses_filenames = sizeclasses_filenames
        self._sizeclasses_to_taxa_filename = sizeclasses_to_taxa_filename
        self._harmful_filename = harmful_filename
        self._harmful_to_taxa_filename = harmful_to_taxa_filename
        # Local storage.
        self._taxa = {} # Main dictionary for taxa.
        self._sizeclasses_name_lookup = {}
        self._harmful_name_lookup = {}
        # Run.
        self._loadAllData()

    def getTaxaDict(self):
        """ """
        return self._taxa 
    
    def getTaxonValue(self, key, taxon_name):
        """ """
        if taxon_name in self._taxa:
            return self._taxa[taxon_name].get(key, u'')
        return u''
    
    def getSizeclassValue(self, key, taxon_name, size_class):
        """ """
        if taxon_name in self._sizeclasses_name_lookup:
            speciesobject = self._sizeclasses_name_lookup[taxon_name]
            if u'Size classes' in speciesobject:
                for sizeclassobject in speciesobject[u'Size classes']:
                    if sizeclassobject.get(u'Size class', u'') == size_class:
                        return sizeclassobject.get(key, u'')
        return None 
    
    def _clear(self):
        """ """
        self._taxa = {}
        self._sizeclasses_name_lookup = {}
        self._harmful_name_lookup = {}

    def _loadAllData(self):
        """ """
        self._clear()
        for excelfilename in self._taxa_filenames:
            self._loadTaxa(excelfilename)
        for excelfilename in self._sizeclasses_filenames:
            self._loadSizeClassesData(excelfilename)
        self._loadHarmfulData()
        self._updateLookupDictionaries()
        self._precalculateData()
        #
#        # Used for DEBUG:
#        fileencoding = locale.getpreferredencoding()
#        out = codecs.open(u'DEBUG_species_list.txt', mode = 'w', 
#                          encoding = fileencoding)
#        out.write(json.dumps(self._taxa, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()
#        #
        #
        
    def _updateLookupDictionaries(self):
        """ """
        self._sizeclasses_name_lookup = {}
        self._harmful_name_lookup = {}
        #
        for speciesobject in self._taxa.values():
            if u'Size classes name' in speciesobject:
                self._sizeclasses_name_lookup[speciesobject[u'Size classes name']] = speciesobject
            if u'Harmful name' in speciesobject:
                self._harmful_name_lookup[speciesobject[u'Harmful name']] = speciesobject

    def _precalculateData(self):
        """ Calculates data from loaded datasets. I.e. class and order info. """
        for speciesobject in self._taxa.values():
            counter = 0
            parentobject = speciesobject
            while parentobject:
                counter += 1
                if counter > 10:
                    parentobject = None # Too many levels, or infinite loop.
                    continue
                if u'Rank' in parentobject:
                    if parentobject[u'Rank'] == u'Order':
                        speciesobject[u'Order'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Class':
                        speciesobject[u'Class'] = parentobject[u'Scientific name']
                    if parentobject[u'Rank'] == u'Phylum':
                        speciesobject[u'Phylum'] = parentobject[u'Scientific name']
                        parentobject = None # Done. Continue with next.
                        continue
                # One step up in hierarchy.
                if u'Parent name' in parentobject:
                    parentobject = self._taxa[parentobject[u'Parent name']] if parentobject[u'Parent name'] else None
                else:
                    parentobject = None

    def _loadTaxa(self, excel_file_name):
        """ Creates one data object for each taxon. """
        # Get data from Excel file.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            scientificname = row[0] # ScientificName
            author = row[1] if row[1] != 'NULL' else '' # Author
            rank = row[2] # Rank
            parentname = row[3]
            #
            if scientificname:
                if scientificname not in self._taxa:
                    self._taxa[scientificname] = {}
                speciesobject = self._taxa[scientificname] 
                speciesobject[u'Scientific name'] = scientificname
                speciesobject[u'Author'] = author
                speciesobject[u'Rank'] = rank
                speciesobject[u'Parent name'] = parentname
#        infile.close()
                    
    def _loadHarmfulData(self):
        """ Adds info about harmfulness to the species objects. """
        #
        #
        # TODO: Use self._harmful_to_taxa_filename if available.
        #
        #
        #
        # Get data from Excel file.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, self._harmful_filename)
        #
        for row in tabledataset.getRows():
            scientificname = row[0] # Scientific name
            aphiaid = row[1] if row[1] != 'NULL' else '' # Aphia id
            #
            if scientificname:
                if scientificname not in self._taxa:
                    self._taxa[scientificname] = {}
                    self._taxa[scientificname][u'Scientific name'] = scientificname
                speciesobject = self._taxa[scientificname] 
                speciesobject[u'Harmful name'] = scientificname
                speciesobject[u'Harmful'] = True 
                speciesobject[u'Aphia id'] = aphiaid
#        infile.close()

    def _loadSizeClassesData(self, excel_file_name):
        """ Adds PEG data to species objects. Creates additional species objects if missing 
            (i.e. for Unicell, Flagellates). """
        # Create mapping between PEG and Dyntaxa names.
        pegtodyntaxa = {}
        # Get data from Excel file.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, self._sizeclasses_to_taxa_filename)
        #
        for row in tabledataset.getRows():
                pegtodyntaxa[row[0]] = row[1]
        #
        # Import size class data.
        pegtodyntaxa = {}
        header = []
        #
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for columnname in tabledataset.getHeader(): 
            header.append(self._translatePegHeader(columnname.strip()))
        #
        for row in tabledataset.getRows():
            taxondict = {}
            sizeclassdict = {}
            column = 0
            for value in row:
                if len(value.strip()) > 0:
                    # Separate columns containing taxon and 
                    # size-class related info.                
                    if self._isPegTaxonRelated(header, column):
                        taxondict[header[column]] = value.strip()
                    else:
                        if (header[column] == u'Size class'):
                            try:
                                # Convert from float to int. Excel related problem.
                                sizeclassdict[header[column]] = unicode(int(float(value)))
                            except:
                                sizeclassdict[header[column]] = u''
                                print(u'_loadPegData, Size class: ' + row[1])
                        elif self._isPegColumnNumeric(header, column):
                            sizeclassdict[header[column]] = value.strip().replace(',', '.')
                        else:
                            sizeclassdict[header[column]] = value.strip()
                column += 1
            # Check if exists in self._taxa
            scientificname = taxondict[u'Species']
            if scientificname in pegtodyntaxa:
                scientificname = pegtodyntaxa[scientificname]
            if scientificname in self._taxa:
                speciesobject = self._taxa[scientificname]
            else:
                self._taxa[taxondict[u'Species']] = {}
                speciesobject = self._taxa[scientificname] 
                speciesobject[u'Scientific name'] = scientificname
                if u'Author' in taxondict:
                    speciesobject[u'Author'] = taxondict[u'Author']
            #
            speciesobject[u'Size classes name'] = scientificname
            #
            if u'Size classes' not in speciesobject:
                speciesobject[u'Size classes'] = []
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

        
    def _translatePegHeader(self, importFileHeader):
        """ Used when importing PEG data.         
            Converts import file column names to key names used in dictionary. """        
    #        if (importFileHeader == u'Division'): return u'Division'
    #        if (importFileHeader == u'Class'): return u'Class'
    #        if (importFileHeader == u'Order'): return u'Order'
    #        if (importFileHeader == u'Species'): return u'Species'
        if (importFileHeader == u'SFLAG (sp., spp., cf., complex, group)'): return u'SFLAG' # Modified
        if (importFileHeader == u'STAGE (cyst, naked)'): return u'Stage' # Modified
    #        if (importFileHeader == u'Author'): return u'Author'
    #        if (importFileHeader == u'Trophy'): return u'Trophy'
    #        if (importFileHeader == u'Geometric shape'): return u'Geometric shape'
        if (importFileHeader == u'FORMULA'): return u'Formula' # Modified
        if (importFileHeader == u'Size class No'): return u'Size class' # Modified
    #        if (importFileHeader == u'Unit'): return u'Unit'
        if (importFileHeader == u'size range,'): return u'Size range' # Modified
        if (importFileHeader == u'Length (l1), µm'): return u'Length(l1), µm' # Modified
        if (importFileHeader == u'Length (l2), µm'): return u'Length(l2), µm' # Modified
        if (importFileHeader == u'Width (w), µm'): return u'Width(w), µm' # Modified
        if (importFileHeader == u'Height (h), µm'): return u'Height(h), µm' # Modified
        if (importFileHeader == u'Diameter (d1), µm'): return u'Diameter(d1), µm' # Modified
        if (importFileHeader == u'Diameter (d2), µm'): return u'Diameter(d2), µm' # Modified
        if (importFileHeader == u'No. of cells/ counting unit'): return u'No. of cells/counting unit' # Modified
        if (importFileHeader == u'Calculated  volume, µm3'): return u'Calculated volume, µm3' # Modified
        if (importFileHeader == u'Comment'): return u'Comment'
        if (importFileHeader == u'Filament: length of cell (µm)'): return u'Filament: length of cell, µm' # Modified
        if (importFileHeader == u'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return u'Calculated Carbon pg/counting unit' # Modified
    #    if (importFileHeader == u'Comment on Carbon calculation'): return u'Comment on Carbon calculation'
        if (importFileHeader == u'CORRECTION / ADDITION                            2009'): return u'Correction/addition 2009' # Modified
        if (importFileHeader == u'CORRECTION / ADDITION                            2010'): return u'Correction/addition 2010' # Modified
        if (importFileHeader == u'CORRECTION / ADDITION                            2011'): return u'Correction/addition 2011' # Modified
        return importFileHeader     
            
    def _isPegTaxonRelated(self, header, column):
        """ Used when importing PEG data. """        
        if (header[column] == u'Division'): return True
        if (header[column] == u'Class'): return True
        if (header[column] == u'Order'): return True
        if (header[column] == u'Species'): return True
        if (header[column] == u'Author'): return True
        if (header[column] == u'SFLAG'): return True
        if (header[column] == u'Stage'): return True
        ###if (header[column] == u'Trophy'): return True
        if (header[column] == u'Geometric shape'): return True
        if (header[column] == u'Formula'): return True
        return False # Related to size class.     
        
    def _isPegColumnNumeric(self, header, column):
        """ Used when importing PEG data. """        
        if (header[column] == u'Size class'): return False # Note: Should be handled as unicode. Could be empty string.
        if (header[column] == u'Length(l1), µm'): return True
        if (header[column] == u'Length(l2), µm'): return True
        if (header[column] == u'Width(w), µm'): return True
        if (header[column] == u'Height(h), µm'): return True
        if (header[column] == u'Diameter(d1), µm'): return True
        if (header[column] == u'Diameter(d2), µm'): return True
        if (header[column] == u'No. of cells/counting unit'): return True
        if (header[column] == u'Calculated volume, µm3'): return True
        if (header[column] == u'Filament: length of cell, µm'): return True
        if (header[column] == u'Calculated Carbon pg/counting unit'): return True
        return False

    def getPlanktonGroupFromTaxonName(self, taxon_name):
        """ """
        taxon_phylum = self.getTaxonValue(u'Phylum', taxon_name)
        taxon_class = self.getTaxonValue(u'Class', taxon_name)
        #
        plankton_group = u'group-not-designated' # Use this if not found.
        # - GROUPS OF ORGANISMS: Cyanobacteria.
        #   (Cyanobacteria)
        if taxon_phylum in [u'Cyanobacteria']:
            plankton_group = u'Cyanobacteria'      
        # - GROUPS OF ORGANISMS: Diatoms.
        #   (Bacillariophyta)
        if taxon_phylum in [u'Bacillariophyta']:
            plankton_group = u'Diatoms'        
        # - GROUPS OF ORGANISMS: Dinoflagellates.
        #   (Dinophyceae)
        if taxon_class in [u'Dinophyceae']:
            plankton_group = u'Dinoflagellates'        
        # - GROUPS OF ORGANISMS: Other microalgae.
        #   (Cryptophyceae + Haptophyta + Bolidophyceae + Chrysophyceae + Dictyochophyceae + 
        #   Eustigmatophyceae + Pelagophyceae  + Raphidophyceae  + Synurophyceae  + Chlorophyta + 
        #   Glaucophyta + Coleochaetophyceae + Klebsormidiophyceae + Mesostigmatophyceae + 
        #   Zygnematophyceae + Euglenophyceae)
        if taxon_phylum in [
                            u'Haptophyta', # Phylum
                            u'Chlorophyta', # Phylum
                            u'Glaucophyta',  # Phylum
                            ]:
            plankton_group = u'Other microalgae'
        else:
            if taxon_class in [
                                u'Cryptophyceae', # Class
                                u'Bolidophyceae', # Class 
                                u'Chrysophyceae', # Class 
                                u'Dictyochophyceae', # Class
                                u'Eustigmatophyceae',  # Class
                                u'Pelagophyceae',  # Class
                                u'Raphidophyceae',  # Class
                                u'Synurophyceae',  # Class
                                u'Coleochaetophyceae',  # Class
                                u'Klebsormidiophyceae',  # Class
                                u'Mesostigmatophyceae', # Class
                                u'Zygnematophyceae',  # Class
                                u'Euglenophyceae' # Class
                                ]:
                plankton_group = u'Other microalgae'
        # - GROUPS OF ORGANISMS: Ciliates.
        #   (Ciliophora)
        if taxon_phylum in [u'Ciliophora']:
            plankton_group = u'Ciliates'        
        # - GROUPS OF ORGANISMS: Other protozoa.
        #   (Cryptophyta, ordines incertae sedis + Bicosoecophyceae + Bodonophyceae + 
        #   Heterokontophyta, ordines incertae sedis + Cercozoa + Craspedophyceae + 
        #   Ellobiopsea + Protozoa, classes incertae sedis)
        if taxon_phylum in ['Cercozoa', # Phylum
                            'Protozoa, classes incertae sedis']: # Phylum
            plankton_group = u'Other protozoa'
        else:
            if taxon_class in [
                               'Cryptophyta, ordines incertae sedis', # Class
                               'Bicosoecophyceae', # Class
                               'Bodonophyceae', # Class
                               'Heterokontophyta, ordines incertae sedis', # Class
                               'Craspedophyceae', # Class
                               'Ellobiopsea' # Class
                               ]:
                plankton_group = u'Other protozoa'
        #
        return plankton_group




        