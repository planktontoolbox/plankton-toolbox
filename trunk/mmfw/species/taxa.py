#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

import codecs
import json
import mmfw

@mmfw.singleton
class Taxa(object):
    """ """
    def __init__(self,
                 taxa_filename = u'mmfw_data/species/taxa_utf16.txt', 
                 sizeclasses_filename = u'mmfw_data/species/sizeclasses_utf16.txt', 
                 sizeclasses_to_taxa_filename = u'mmfw_data/species/translate_sizeclasses_to_taxa_utf16.txt', 
#                 harmful_filename = u'plankton_reports/data/species/harmful_utf16.txt', 
#                 harmful_to_taxa_filename = u'plankton_reports/data/species/translate_harmful_to_taxa_utf16.txt', 
                 file_encoding = u'utf16', # utf16 utf8 cp1252
                 field_separator = u'\t', 
                 row_delimiter = u'\r\n'):
        # Parameters.
        self.__taxa_filename = taxa_filename 
        self.__sizeclasses_filename = sizeclasses_filename
        self.__sizeclasses_to_taxa_filename = sizeclasses_to_taxa_filename
#        self.__harmful_filename = harmful_filename
#        self.__harmful_to_taxa_filename = harmful_to_taxa_filename
        self.__file_encoding = file_encoding
        self.__field_separator = field_separator
        self.__row_delimiter = row_delimiter
        # Local storage.
        self.__taxa = {} # Main dictionary for taxa.
        self.__sizeclasses_name_lookup = {}
#        self.__harmful_name_lookup = {}
        # Run.
        self.loadAllData()

    def loadAllData(self):
        """ """
        self.__clear()
        self.__loadTaxa()
        self.__loadPegData()
#        self.__loadHarmfulData()
        self.__updateLookupDictionaries()
        self.__precalculateData()
#        # Used for DEBUG:
#        fileencoding = self.__file_encoding
#        out = codecs.open(u'DEBUG_species_list.txt', mode = 'w', 
#                          encoding = fileencoding)
#        out.write(json.dumps(self.__taxa, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()

    def getTaxaDict(self):
        """ """
        return self.__taxa 
    
    def getTaxonValue(self, key, taxon_name):
        """ """
        if taxon_name in self.__taxa:
            return self.__taxa[taxon_name].get(key, u'')
        return u''
    
    def getSizeclassValue(self, key, taxon_name, size_class):
        """ """
        if taxon_name in self.__sizeclasses_name_lookup:
            speciesobject = self.__sizeclasses_name_lookup[taxon_name]
            if u'Size classes' in speciesobject:
                for sizeclassobject in speciesobject[u'Size classes']:
                    if sizeclassobject.get(u'Size class', u'') == size_class:
                        return sizeclassobject.get(key, u'')
        return None 
    
    def __clear(self):
        """ """
        self.__taxa = {}
        self.__sizeclasses_name_lookup = {}
#        self.__harmful_name_lookup = {}

    def __updateLookupDictionaries(self):
        """ """
        self.__sizeclasses_name_lookup = {}
#        self.__harmful_name_lookup = {}
        #
        for speciesobject in self.__taxa.values():
            if u'Size classes name' in speciesobject:
                self.__sizeclasses_name_lookup[speciesobject[u'Size classes name']] = speciesobject
#            if u'Harmful name' in speciesobject:
#                self.__harmful_name_lookup[speciesobject[u'Harmful name']] = speciesobject

    def __precalculateData(self):
        """ Calculates data from loaded datasets. I.e. class and order info. """
        for speciesobject in self.__taxa.values():
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
                        parentobject = None # Done. Continue with next.
                        continue
                # One step up in hierarchy.
                if u'Parent name' in parentobject:
                    parentobject = self.__taxa[parentobject[u'Parent name']] if parentobject[u'Parent name'] else None
                else:
                    parentobject = None

    def __loadTaxa(self):
        """ Creates one data object for each taxon. """
        # Open file for reading.
        fileencoding = self.__file_encoding
        infile = codecs.open(self.__taxa_filename, mode = 'r', 
                             encoding = fileencoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: Scientific name    Author    Rank    Parent name
                pass
            else:
                row = [unicode(item.strip()) for item in row.split(self.__field_separator)] 
                #
                scientificname = row[0] # ScientificName
                author = row[1] if row[1] != 'NULL' else '' # Author
                rank = row[2] # Rank
                parentname = row[3]
                #
                if scientificname:
                    if scientificname not in self.__taxa:
                        self.__taxa[scientificname] = {}
                    speciesobject = self.__taxa[scientificname] 
                    speciesobject[u'Scientific name'] = scientificname
                    speciesobject[u'Author'] = author
                    speciesobject[u'Rank'] = rank
                    speciesobject[u'Parent name'] = parentname
        infile.close()
                    
#    def __loadHarmfulData(self):
#        """ Adds info about harmfulness to the species objects. """
#        #
#        #
#        # TODO: Use self.__harmful_to_taxa_filename if available.
#        #
#        #
#        fileencoding = self.__file_encoding
#        infile = codecs.open(self.__harmful_filename, mode = 'r', 
#                             encoding = fileencoding)    
#        # Iterate over rows in file.
#        for rowindex, row in enumerate(infile):
#            if rowindex == 0:
#                pass # Header: Scientific name    Aphia id
#            else:
#                row = [unicode(item.strip()) for item in row.split(self.__field_separator)] 
#                #
#                scientificname = row[0] # Scientific name
#                aphiaid = row[1] if row[1] != 'NULL' else '' # Aphia id
#                #
#                if scientificname:
#                    if scientificname not in self.__taxa:
#                        self.__taxa[scientificname] = {}
#                        self.__taxa[scientificname][u'Scientific name'] = scientificname
#                    speciesobject = self.__taxa[scientificname] 
#                    speciesobject[u'Harmful name'] = scientificname
#                    speciesobject[u'Harmful'] = True
#                    speciesobject[u'Aphia id'] = aphiaid
#        infile.close()

    def __loadPegData(self):
        """ Adds PEG data to species objects. Creates additional species objects if missing 
            (i.e. for Unicell, Flagellates). """
        # Create mapping between PEG and Dyntaxa names.
        pegtodyntaxa = {}
        fileencoding = self.__file_encoding
        infile = codecs.open(self.__sizeclasses_to_taxa_filename, mode = 'r', 
                             encoding = fileencoding) 
        for rowindex, row in enumerate(infile):
            if rowindex == 0:
                pass # Header: PEG taxon name    DynTaxa taxon name
            else:
                row = [unicode(item.strip()) for item in row.split(self.__field_separator)] 
                pegtodyntaxa[row[0]] = row[1]
        infile.close()
        #
        # Import size class data.
        pegtodyntaxa = {}
        header = []
        fileencoding = self.__file_encoding
        infile = codecs.open(self.__sizeclasses_filename, mode = 'r', 
                             encoding = fileencoding)    
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = [unicode(item.strip()) for item in row.split(self.__field_separator)] 
                # Translate headers.
                for columnname in headers: 
                    header.append(self.__translatePegHeader(columnname.strip()))
            else:
                row = [unicode(item.strip()) for item in row.split(self.__field_separator)] 
                taxondict = {}
                sizeclassdict = {}
                column = 0
                for value in row:
                    if len(value.strip()) > 0:
                        # Separate columns containing taxon and 
                        # size-class related info.                
                        if self.__isPegTaxonRelated(header, column):
                            taxondict[header[column]] = value.strip()
                        else:
                            if self.__isPegColumnNumeric(header, column):
                                sizeclassdict[header[column]] = value.strip().replace(',', '.')
                            else:
                                sizeclassdict[header[column]] = value.strip()
                    column += 1

                # Check if exists in self.__taxa
                scientificname = taxondict[u'Species']
                if scientificname in pegtodyntaxa:
                    scientificname = pegtodyntaxa[scientificname]
                if scientificname in self.__taxa:
                    speciesobject = self.__taxa[scientificname]
                else:
                    self.__taxa[taxondict[u'Species']] = {}
                    speciesobject = self.__taxa[scientificname] 
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
        infile.close()
        #
        # Trophy is set on sizeclass level. Should also be set on species level  
        # if all sizeclasses have the same trophy.
        for taxon in self.__taxa.values():
            trophyset = set() 
            if u'Size classes' in taxon:
                for sizeclass in taxon[u'Size classes']:
                    trophyset.add(sizeclass.get(u'Trophy', u''))
            if len(trophyset) == 1:
                taxon[u'Trophy'] = list(trophyset)[0]

        
    def __translatePegHeader(self, importFileHeader):
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
            
    def __isPegTaxonRelated(self, header, column):
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
        
    def __isPegColumnNumeric(self, header, column):
        """ Used when importing PEG data. """        
        if (header[column] == u'Size class'): return True
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

