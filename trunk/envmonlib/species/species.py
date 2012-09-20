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
import os.path

@envmonlib.singleton
class Species(object):
    """ 
    
    Rules.
    Filenames:
    - Species files must be in the Excel (xlsx) format.
    - Taxa files must contain the string '_species'.
    - BVOL files must contain the string '_bvol'.
    - Harmful species files must contain the string '_harmful'.
    - Translations files must begin with 'translate_to_'.
    File columns:
    - Species files must contain the columns: ......
    - BVOL files must follow the PEG BVOL format.
    - Translation files for species must... 
    - Translation files for BVOL must... 
    
    """
    def __init__(self,
                 taxa_filenames = [u'toolbox_data/species/nordicmicroalgae_species.xlsx',
                                   u'toolbox_data/species/smhi_species.xlsx'], 
                 bvol_filenames = [u'toolbox_data/species/peg_bvol_2011.xlsx',
                                   u'toolbox_data/species/smhi_bvol_2011.xlsx'], 
                 harmful_filenames = [u'toolbox_data/species/smhi_harmful.xlsx']):
        # Parameters.
        self._taxa_filenames = taxa_filenames 
        self._bvol_filenames = bvol_filenames
        self._harmful_filenames = harmful_filenames
        # Local storage.
        self._taxa = {} # Main dictionary for taxa.
        self._taxa_lookup = {} # Includes both taxon names and synonyms.
        self._plankton_group_phylum_dict = None
        self._plankton_group_class_dict = None
        # Run.
        try:
            self._loadAllData()
        except:
            print(u'Failed to load species data.')

    def getTaxaDict(self):
        """ """
        return self._taxa 
    
    def getTaxonValue(self, taxon_name, key):
        """ """
        if taxon_name in self._taxa:
            return self._taxa[taxon_name].get(key, u'')
        return u''
    
    def getBvolValue(self, key, taxon_name, size_class):
        """ """
        if taxon_name in self._taxa_lookup:
            speciesobject = self._taxa_lookup[taxon_name]
            if u'Size classes' in speciesobject:
                for sizeclassobject in speciesobject[u'Size classes']:
                    if sizeclassobject.get(u'Size class', u'') == size_class:
                        return sizeclassobject.get(key, u'')
        return None 
    
    def _clear(self):
        """ """
        self._taxa = {}
        self._taxa_synonyms = {}
#        self._bvol_name_lookup = {}
#        self._harmful_name_lookup = {}

    def _loadAllData(self):
        """ """
        try:
            self._clear()
            # Create taxa.
            for excelfilename in self._taxa_filenames:
                self._loadTaxa(excelfilename)                
            # Add synonyms to taxa. Note: 'translate_to_' will be added to filenames.
            for excelfilename in self._taxa_filenames:
                self._loadSynonyms(excelfilename)                            
            self._updateLookupDictionaries()
            
            # Load harmful species.
            for excelfilename in self._harmful_filenames:
                self._loadHarmful(excelfilename)

            # Load BVOL species data.
            for excelfilename in self._bvol_filenames:
                self._loadBvol(excelfilename)            
            # Add BVOL translations.
            ### TODO: ....
            
            # Perform some useful pre-calculations.
            self._precalculateData()
        #
        except Exception, e:
            envmonlib.Logging().error(u"Failed when loading species data: " + unicode(e))
            print(u"Failed when loading species data: " + unicode(e))

        #
        # Used for DEBUG:
        import locale
        import codecs
        import json
        fileencoding = locale.getpreferredencoding()
        out = codecs.open(u'DEBUG_species_list.txt', mode = 'w', encoding = fileencoding)
        out.write(json.dumps(self._taxa, encoding = 'utf8', sort_keys=True, indent=4))
        out.close()
        #
        #
        
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

    def _loadSynonyms(self, excel_file_name):
        """ Add synonyms from the corresponding 'translate_to_' file. """
        dirname = os.path.dirname(excel_file_name)        
        basename = os.path.basename(excel_file_name)
        translate_file_name = dirname + u'/translate_to_' + basename
        # 
        if os.path.exists(translate_file_name):
            tabledataset = envmonlib.DatasetTable()
            envmonlib.ExcelFiles().readToTableDataset(tabledataset, translate_file_name)
            for row in tabledataset.getRows():
                toname = row[1]
                fromname = row[0]
                if toname in self._taxa:
                    taxon = self._taxa[toname]
                    if not u'Synonyms' in self._taxa[toname]:
                        taxon[u'Synonyms'] = []
                    taxon[u'Synonyms'].append(fromname)
                else:
                    print(translate_file_name + u': Species missing ' + toname)
                    
    def _loadHarmful(self, excel_file_name):
        """ Adds info about harmfulness to the species objects. """
        # Get data from Excel file.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
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

    def _updateLookupDictionaries(self):
        """ """
        self._taxa_lookup = {}
        for taxonobject in self._taxa.values():
            # Add the taxon itself.
            self._taxa_lookup[taxonobject[u'Scientific name']] = taxonobject 
            if u'Synonyms' in taxonobject:
                for synonym in taxonobject[u'Synonyms']:
                    # Add synonyms.
                    self._taxa_lookup[synonym] = taxonobject
        
    def _precalculateData(self):
        """ Calculates data from loaded datasets. I.e. phylum, class and order info. """
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

    def _loadBvol(self, excel_file_name):
        """ Adds BVOL data to species objects. Creates additional species objects if missing 
            (i.e. for Unicell, Flagellates). """
        # Import size class data.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        # Create header list for mapping and translations.
        header = []
        for columnname in tabledataset.getHeader(): 
            header.append(self._translateBvolHeader(columnname.strip()))
        #
        for row in tabledataset.getRows():
            taxondict = {}
            sizeclassdict = {}
            column = 0
            for value in row:
                if len(value.strip()) > 0:
                    # Separate columns containing taxon and 
                    # size-class related info.                
                    if self._isBvolTaxonRelated(header, column):
                        taxondict[header[column]] = value.strip()
                    else:
                        if (header[column] == u'Size class'):
                            try:
                                # Convert from float to int. Excel related problem.
                                sizeclassdict[header[column]] = unicode(int(float(value)))
                            except:
                                sizeclassdict[header[column]] = u''
                                print(u'_loadBvol, Size class: ' + row[1])
                        elif self._isBvolColumnNumeric(header, column):
                            sizeclassdict[header[column]] = value.strip().replace(',', '.')
                        else:
                            sizeclassdict[header[column]] = value.strip()
                column += 1
            # Check if exists in self._taxa
            scientificname = taxondict[u'Species']
            if scientificname in self._taxa_lookup:
                speciesobject = self._taxa_lookup[scientificname]
            else:
                continue # Only add BVOL info if taxon exists in taxa.
#            else:
#                self._taxa[taxondict[u'Species']] = {}
#                speciesobject = self._taxa[scientificname] 
#                speciesobject[u'Scientific name'] = scientificname
#                if u'Author' in taxondict:
#                    speciesobject[u'Author'] = taxondict[u'Author']
            #
            speciesobject[u'BVOL name'] = scientificname
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

        
    def _translateBvolHeader(self, importFileHeader):
        """ Used when importing BVOL data.         
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
        if (importFileHeader == u'CORRECTION / ADDITION                            2012'): return u'Correction/addition 2012' # Modified
        return importFileHeader     
            
    def _isBvolTaxonRelated(self, header, column):
        """ Used when importing BVOL data. """        
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
        
    def _isBvolColumnNumeric(self, header, column):
        """ Used when importing BVOL data. """        
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
        """ This is another way to organize organisms into groups. """
        # TODO: Check this...
        if taxon_name == u'Unicell':
            return u'Unicell'
        # TODO: Check this...
        if taxon_name == u'Flagellates':
            return u'Flagellates'
        # Load dictionaries if not done before.
        if not self._plankton_group_phylum_dict:
            self._plankton_group_phylum_dict = {
                u'Cyanobacteria': u'Cyanobacteria',
                u'Bacillariophyta': u'Diatoms',
                u'Haptophyta': u'Other microalgae',
                u'Chlorophyta': u'Other microalgae',
                u'Glaucophyta': u'Other microalgae',
                u'Ciliophora': u'Ciliates',
                u'Cercozoa': u'Other protozoa',
                u'Protozoa, classes incertae sedis': u'Other protozoa'
                }
        if not self._plankton_group_class_dict:
            self._plankton_group_class_dict = {
                u'Dinophyceae': u'Dinoflagellates',
                u'Bacillariophyta': u'Diatoms',
                u'Cryptophyceae': u'Other microalgae',
                u'Bolidophyceae': u'Other microalgae',
                u'Chrysophyceae': u'Other microalgae',
                u'Dictyochophyceae': u'Other microalgae',
                u'Eustigmatophyceae': u'Other microalgae',
                u'Pelagophyceae': u'Other microalgae',
                u'Raphidophyceae': u'Other microalgae',
                u'Synurophyceae': u'Other microalgae',
                u'Coleochaetophyceae': u'Other microalgae',
                u'Klebsormidiophyceae': u'Other microalgae',
                u'Mesostigmatophyceae': u'Other microalgae',
                u'Zygnematophyceae': u'Other microalgae',
                u'Euglenophyceae': u'Other microalgae',
                u'Cryptophyta, ordines incertae sedis': u'Other protozoa',
                u'Bicosoecophyceae': u'Other protozoa',
                u'Bodonophyceae': u'Other protozoa',
                u'Heterokontophyta, ordines incertae sedis': u'Other protozoa',
                u'Craspedophyceae': u'Other protozoa',
                u'Ellobiopsea': u'Other protozoa'
                }
        # Check on phylym:
        taxonphylum = self.getTaxonValue(taxon_name, u'Phylum')
        if taxonphylum in self._plankton_group_phylum_dict:
            return self._plankton_group_phylum_dict[taxonphylum]
        # Check on class.
        taxonclass = self.getTaxonValue(taxon_name, u'Class')
        if taxonclass in self._plankton_group_class_dict:
            return self._plankton_group_class_dict[taxonclass]
        # Return this if plankton group not found.
        return u'group-not-designated'

