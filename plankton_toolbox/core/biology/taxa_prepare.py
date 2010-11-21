#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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

"""
This module is used for preparation of resource files. Resource files are 
stored in the json format, but they can be prepared from various sources.

Simplejson. For Python(x,y) users, add from:
http://code.google.com/p/pythonxy/wiki/StandardPlugins
"""

#import date
from abc import abstractmethod
import datetime
import simplejson as json

class PrepareDataSources(object):
    """
    Abstract base class. 
    """
    def __init__(self, taxaObject):
        self._taxaObject = taxaObject

    @abstractmethod
    def importTaxa(self):
        """ Abstract method. """
#        raise UserWarning('Abstract method not implemented.')
        
    @abstractmethod
    def exportTaxa(self):
        """ Abstract method. """
#        raise UserWarning('Abstract method not implemented.')


class PrepareDyntaxaDbTablesAsTextFiles(DataSources):
    """
    Imports from text files.  
    """
    def __init__(self, taxaObject = None):
        """ """
        super(PrepareDyntaxaDbTablesAsTextFiles, self).__init__(taxaObject)

    def importTaxa(self, dir = None):
        """ """
        self.__taxonHeader = []
        self.__hierHeader = []
        self.__namesHeader = []
        self.__taxonTypeDict = None
        self.__nameTypeDict = None
        # These parts of the Taxa object will be modified during import.
        self.__taxa = self._taxaObject.getTaxonList()
        self.__idToTaxon = self._taxaObject.getIdToTaxonMap()
        
        self.__createTaxonTypeDict() # Maps from taxon type id to taxon type.
        self.__createNameTypeDict() # Maps from name type id to name type.
        
        # === TAXON file ===
        taxonFile = open(dir + 'species_dyntaxa_taxon.txt', 'r')
        separator = '\t' # Tab as separator.
        for line in taxonFile:
            if len(self.__taxonHeader) == 0:
                # Store header columns.
                self.__taxonHeader = line.split(separator)
            else:
                 # Split row and trim each item.
                columns = map(self.__cleanUpString, line.split(separator))
                if len(columns) < 2:
                    continue # Don't handle short rows.
                # Extract used column values:
                # 0, idnr    
                taxonid = int(columns[1]) # 1, taxonid
                taxontypid = int(columns[2]) # 2, taxontypid
                # 3, referensid
                # 4, person
                # 5, datum
                datum0 = columns[6] # 6, datum0
                datum1 = columns[7] # 7, datum1
                # 8, andringid
                # 9, taxondummy
                # 10, leaf
                exportkat = int(columns[11]) # 11, exportkat
                # 12, lista
                # 13, text
                
                # Check if data is in a valid time span, related to "now".
                dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
                dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
                nowDate = datetime.date.today()           
                now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
                if (exportkat == 0) and (dateFrom <= now) and (now <= dateTo):
                    taxonDict = {}
                    taxonDict['Taxon id'] = taxonid
                    taxonDict['Taxon type id'] = taxontypid
                    taxonDict['Taxon type'] = self.__taxonTypeDict[str(taxontypid)]
                    taxonDict['Valid from'] = datum0
                    taxonDict['Valid to'] = datum1
                self.__taxa.append(taxonDict) # Updates Taxa object.
                if not(taxonid in self.__idToTaxon):
                    self.__idToTaxon[taxonid] = taxonDict # Updates Taxa object.
                else:
                    print ("Duplicate taxon id: " + str(taxonid) )
        taxonFile.close()
        
        # === HIER file ===
        hierFile = open(dir + 'species_dyntaxa_hier.txt', 'r')
        separator = '\t' # Tab as separator.
        for line in hierFile:
            if len(self.__hierHeader) == 0:
                # Store header columns.
                self.__hierHeader = line.split(separator)
            else:
                 # Split row and trim each item.
                columns = map(self.__cleanUpString, line.split(separator))
                if len(columns) < 2:
                    continue # Don't handle short rows.
                # Extract used column values:
                # 0, idnr
                agarid = int(columns[1]) # 1, agarid
                underid = int(columns[2]) # 2, underid
                relationid = int(columns[3]) # 3, relationid
                # 4, relation
                # 5, referensid
                # 6, person
                # 7, datum
                datum0 = columns[8] # 9, datum0
                datum1 = columns[9] # 9, datum1
                # 10, lista
                # 11, dublett
                # 12, text
                
                # Check if data is in a valid time span, related to "now".
                dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
                dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
                nowDate = datetime.date.today() # Note: includes day and time.           
                now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
                if (dateFrom <= now) and (now <= dateTo):
                     if underid in self.__idToTaxon:
                        taxon = self.__idToTaxon[underid]
                        if relationid == '0':
                            taxon['Parent id'] = ''
                        elif relationid == '2':
                            taxon['Parent id'] = agarid
                     else:
                        print('Can not find Taxon id(hier): ' + underid)
        hierFile.close()
        
        # === NAMES file ===
        namesFile = open(dir + 'species_dyntaxa_names.txt', 'r')
        separator = '\t' # Tab as separator.
        for line in namesFile:
            if len(self.__namesHeader) == 0:
                # Store header columns.
                self.__namesHeader = line.split(separator)
            else:
                 # Split row and trim each item.
                columns = map(self.__cleanUpString, line.split(separator))
                if len(columns) < 2:
                    continue # Don't handle short rows.
                # Extract used column values:
                # 0, idnr
                taxonid = int(columns[1]) # 1, taxonid
                # 2, taxontypid
                # 3, taxondummy
                namn = columns[4] # 4, namn
                auktor = columns[5] # 5, auktor
                namntypid = int(columns[6]) # 6, namntypid
                # 7, obsrek
                # 8, referensid
                # 9, person
                # 10, datum
                datum0 = columns[11] # 11, datum0
                datum1 = columns[12] # 12, datum1
                exportkat = int(columns[13]) # 13, exportkat
                # 14, lista
                # 15, text
                                
                # Check if data is in a valid time span, related to "now".
                dateFrom = datetime.datetime.strptime(datum0, '%Y-%m-%d')
                dateTo = datetime.datetime.strptime(datum1, '%Y-%m-%d')
                nowDate = datetime.date.today() # Note: includes day and time.           
                now = datetime.datetime(nowDate.year, nowDate.month, nowDate.day)                
                if (exportkat == 0) and (dateFrom <= now) and (now <= dateTo):
                    if taxonid in self.__idToTaxon:
                        taxon = self.__idToTaxon[taxonid]    
                        nameDict = {}
                        nameDict['Name type id'] = namntypid
                        nameDict['Name type'] = self.__nameTypeDict[str(namntypid)]
                        nameDict['Name'] = namn
                        nameDict['Author'] = auktor
                        nameDict['Valid from'] = datum0
                        nameDict['Valid to'] = datum1                        
                        if not ('Names' in taxon):
                            taxon['Names'] = [] # Create list for names.
                        taxon['Names'].append(nameDict)
                        # Create valid name/author for easy access.
                        if namntypid == 0:
                            taxon['Valid name'] = namn
                            taxon['Valid author'] = auktor
                    else:
                        print('Can not find Taxon id(name): ' + str(underid))                
        namesFile.close()
        
    def __cleanUpString(self,value):
        """ """
        return value.strip()

    def __createTaxonTypeDict(self):
        """ """
        self.__taxonTypeDict = {        
            "1": "Kingdom",
            "2": "Phylum",
            "3": "Subphylum",
            "4": "Superclass",
            "5": "Class",
            "6": "Subclass",
            "7": "Superorder",
            "8": "Order",
            "9": "Suborder",
            "10": "Superfamily",
            "11": "Family",
            "12": "Subfamily",
            "13": "Tribe",
            "14": "Genus",
            "15": "Subgenus",
            "16": "Section",
            "17": "Species",
            "18": "Subspecies",
            "19": "Variety",
            "20": "Form",
            "21": "Hybrid",
            "22": "Cultural variety",
            "23": "Population",
            "24": "Group of families",
            "25": "Infraclass",
            "26": "Parvclass",
            "27": "Sensu lato",
            "28": "Species pair",
            "-2": "Group",
            "-1": "Group of lichens",
            "29": "Infraorder",
            "30": "Avdelning",
            "31": "Underavdelning"}
        
    def __createNameTypeDict(self):
        """ """
        self.__nameTypeDict = {
            "0": "Scientific",
            "1": "Swedish",
            "2": "English",
            "3": "Danish",
            "4": "Norwegian",
            "5": "Finnish",
            "6": "Icelandic",
            "7": "American english",
            "8": "NNkod",
            "9": "ITIS-name",
            "10": "ITIS-number",
            "11": "ERMS-name",
            "12": "Geman",
            "13": "Original name",
            "14": "Faeroe",
            "15": "Anamorf name"}


class PreparePegTextFile(DataSources):
    """ 
    """
    def __init__(self, taxaObject = None):
        """ """
        super(PreparePegTextFile, self).__init__(taxaObject)

    def importTaxa(self, file = None):
        """ """
        self.__header = []
        self.__taxa = self._taxaObject.getTaxonList()
        
        pegFile = open(file, 'r')
        separator = '\t' # Tab as separator.
        for line in pegFile:
            if len(self.__header) == 0:
                # Store header columns. They will be used as keys i the taxon dictionary.
                importFileHeader = line.split(separator)
                for columnName in importFileHeader: 
                    self.__header.append(self.__translateHeader(columnName.strip()))
            else:
                taxonDict = {}
                sizeClassDict = {}
                column = 0
                for value in line.split(separator):
                    if len(value.strip()) > 0:
                        # Separate columns containing taxon and 
                        # size-class related info.                
                        if self.__isTaxonRelated(column):
                            taxonDict[self.__header[column]] = value.strip()
                        else:
                            if self.__isColumnNumeric(column):
                                try:
                                    float_value = float(value.strip().replace(',', '.').replace(' ', ''))
                                    sizeClassDict[self.__header[column]] = float_value
                                    if self.__header[column] == 'Size class':  # Covert SIZECLASS to integer.
                                        sizeClassDict[self.__header[column]] = int(float_value)
                                except:
                                    # Use string format if not valid numeric. 
                                    sizeClassDict[self.__header[column]] = value.strip()
                                    
#                                    print ('ERROR float:' + value + '     ' + value.strip().replace(',', '.').replace(' ', ''))
                                    
                            else:
                                sizeClassDict[self.__header[column]] = value.strip()
                    column += 1
                # Check if the taxon-related data already exists.
                taxonExists = False
                for taxon in self.__taxa:
                    if taxon['Species'] == taxonDict['Species']:
                        taxonExists = True
                        taxon['Size classes'].append(sizeClassDict)
                        continue
                # First time. Create the list and add dictionary for 
                # size classes. 
                if taxonExists == False:
                    self.__taxa.append(taxonDict)
                    taxonDict['Size classes'] = []
                    taxonDict['Size classes'].append(sizeClassDict)
                
        pegFile.close()
        
    def __translateHeader(self, importFileHeader):
        """ Convert import file column names to key names used in dictionary. """        
#        if (importFileHeader == 'Division'): return 'Division'
#        if (importFileHeader == 'Class'): return 'Class'
#        if (importFileHeader == 'Order'): return 'Order'
#        if (importFileHeader == 'Species'): return 'Species'
        if (importFileHeader == 'SFLAG (sp., spp., cf., complex, group)'): return 'SFLAG' # Modified
        if (importFileHeader == 'STAGE (cyst, naked)'): return 'Stage' # Modified
#        if (importFileHeader == 'Author'): return 'Author'
#        if (importFileHeader == 'Trophy'): return 'Trophy'
#        if (importFileHeader == 'Geometric shape'): return 'Geometric shape'
        if (importFileHeader == 'FORMULA'): return 'Formula' # Modified
        if (importFileHeader == 'Size class No'): return 'Size class' # Modified
#        if (importFileHeader == 'Unit'): return 'Unit'
        if (importFileHeader == 'size range,'): return 'Size range' # Modified
        if (importFileHeader == 'Length (l1), \xb5m'): return 'Length(l1), um' # Modified
        if (importFileHeader == 'Length (l2), \xb5m'): return 'Length(l2), um' # Modified
        if (importFileHeader == 'Width (w), \xb5m'): return 'Width(w), um' # Modified
        if (importFileHeader == 'Height (h), \xb5m'): return 'Height(h), um' # Modified
        if (importFileHeader == 'Diameter (d1), \xb5m'): return 'Diameter(d1), um' # Modified
        if (importFileHeader == 'Diameter (d2), \xb5m'): return 'Diameter(d2), um' # Modified
        if (importFileHeader == 'No. of cells/ counting unit'): return 'No. of cells/counting unit' # Modified
        if (importFileHeader == 'Calculated  volume, \xb5m3'): return 'Calculated volume, um3' # Modified
        if (importFileHeader == 'Comment'): return 'Comment'
        if (importFileHeader == 'Filament: length of cell (\xb5m)'): return 'Filament: length of cell, um' # Modified
        if (importFileHeader == 'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return 'Calculated Carbon pg/counting unit' # Modified
        if (importFileHeader == 'Comment on Carbon calculation'): return 'Comment on Carbon calculation'
        if (importFileHeader == 'CORRECTION / ADDITION                            2009'): return 'CORRECTION/ADDITION 2009' # Modified
        return importFileHeader     
        
    def __isTaxonRelated(self, column):
        """ """        
        if (self.__header[column] == 'Division'): return True
        if (self.__header[column] == 'Class'): return True
        if (self.__header[column] == 'Order'): return True
        if (self.__header[column] == 'Species'): return True
        if (self.__header[column] == 'SFLAG'): return True
        if (self.__header[column] == 'Author'): return True
        return False # Related to size class.     
        
    def __isColumnNumeric(self, column):
        """ """        
        if (self.__header[column] == 'Size class'): return True
        if (self.__header[column] == 'Length(l1), um'): return True
        if (self.__header[column] == 'Length(l2), um'): return True
        if (self.__header[column] == 'Width(w), um'): return True
        if (self.__header[column] == 'Height(h), um'): return True
        if (self.__header[column] == 'Diameter(d1), um'): return True
        if (self.__header[column] == 'Diameter(d2), um'): return True
        if (self.__header[column] == 'No. of cells/counting unit'): return True
        if (self.__header[column] == 'Calculated volume, um3'): return True
        if (self.__header[column] == 'Filament: length of cell, um'): return True
        if (self.__header[column] == 'Calculated Carbon pg/counting unit'): return True
        return False     

class PrepareSmhiPwSpecies(DataSources):
    """ 
    """
    def __init__(self, taxaObject = None):
        """ """
        super(PreparePegTextFile, self).__init__(taxaObject)

    def importTaxa(self, file = None):
        """ """
        self.__header = []
        self.__taxa = self._taxaObject.getTaxonList()
        
        pegFile = open(file, 'r')
        separator = '\t' # Tab as separator.
        for line in pegFile:
            if len(self.__header) == 0:
                # Store header columns. They will be used as keys i the taxon dictionary.
                importFileHeader = line.split(separator)
                for columnName in importFileHeader: 
                    self.__header.append(self.__translateHeader(columnName.strip()))
            else:
                taxonDict = {}
                sizeClassDict = {}
                column = 0
                for value in line.split(separator):
                    if len(value.strip()) > 0:
                        # Separate columns containing taxon and 
                        # size-class related info.                
                        if self.__isTaxonRelated(column):
                            taxonDict[self.__header[column]] = value.strip()
                        else:
                            if self.__isColumnNumeric(column):
                                try:
                                    sizeClassDict[self.__header[column]] = float(value.strip().replace(',', '.').replace(' ', ''))
                                except:
                                    # Use string format if not valid numeric. 
                                    sizeClassDict[self.__header[column]] = value.strip()
                                    
#                                    print ('ERROR float:' + value + '     ' + value.strip().replace(',', '.').replace(' ', ''))
                                    
                            else:
                                sizeClassDict[self.__header[column]] = value.strip()
                    column += 1
                # Check if the taxon-related data already exists.
                taxonExists = False
                for taxon in self.__taxa:
                    if taxon['Species'] == taxonDict['Species']:
                        taxonExists = True
                        taxon['Size classes'].append(sizeClassDict)
                        continue
                # First time. Create the list and add dictionary for 
                # size classes. 
                if taxonExists == False:
                    self.__taxa.append(taxonDict)
                    taxonDict['Size classes'] = []
                    taxonDict['Size classes'].append(sizeClassDict)
                
        pegFile.close()
        
    def __translateHeader(self, importFileHeader):
        """ Convert import file column names to key names used in dictionary. """        
#        if (importFileHeader == 'Division'): return 'Division'
#        if (importFileHeader == 'Class'): return 'Class'
#        if (importFileHeader == 'Order'): return 'Order'
#        if (importFileHeader == 'Species'): return 'Species'
        if (importFileHeader == 'SFLAG (sp., spp., cf., complex, group)'): return 'SFLAG' # Modified
        if (importFileHeader == 'STAGE (cyst, naked)'): return 'Stage' # Modified
#        if (importFileHeader == 'Author'): return 'Author'
#        if (importFileHeader == 'Trophy'): return 'Trophy'
#        if (importFileHeader == 'Geometric shape'): return 'Geometric shape'
        if (importFileHeader == 'FORMULA'): return 'Formula' # Modified
        if (importFileHeader == 'Size class No'): return 'Size class' # Modified
#        if (importFileHeader == 'Unit'): return 'Unit'
        if (importFileHeader == 'size range,'): return 'Size range' # Modified
        if (importFileHeader == 'Length (l1), \xb5m'): return 'Length(l1), um' # Modified
        if (importFileHeader == 'Length (l2), \xb5m'): return 'Length(l2), um' # Modified
        if (importFileHeader == 'Width (w), \xb5m'): return 'Width(w), um' # Modified
        if (importFileHeader == 'Height (h), \xb5m'): return 'Height(h), um' # Modified
        if (importFileHeader == 'Diameter (d1), \xb5m'): return 'Diameter(d1), um' # Modified
        if (importFileHeader == 'Diameter (d2), \xb5m'): return 'Diameter(d2), um' # Modified
        if (importFileHeader == 'No. of cells/ counting unit'): return 'No. of cells/counting unit' # Modified
        if (importFileHeader == 'Calculated  volume, \xb5m3'): return 'Calculated volume, um3' # Modified
        if (importFileHeader == 'Comment'): return 'Comment'
        if (importFileHeader == 'Filament: length of cell (\xb5m)'): return 'Filament: length of cell, um' # Modified
        if (importFileHeader == 'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return 'Calculated Carbon pg/counting unit' # Modified
        if (importFileHeader == 'Comment on Carbon calculation'): return 'Comment on Carbon calculation'
        if (importFileHeader == 'CORRECTION / ADDITION                            2009'): return 'CORRECTION/ADDITION 2009' # Modified
        return importFileHeader     
        
    def __isTaxonRelated(self, column):
        """ """        
        if (self.__header[column] == 'Division'): return True
        if (self.__header[column] == 'Class'): return True
        if (self.__header[column] == 'Order'): return True
        if (self.__header[column] == 'Species'): return True
        if (self.__header[column] == 'SFLAG'): return True
        if (self.__header[column] == 'Author'): return True
        return False # Related to size class.     
        
    def __isColumnNumeric(self, column):
        """ """        
        if (self.__header[column] == 'Length(l1), um'): return True
        if (self.__header[column] == 'Length(l2), um'): return True
        if (self.__header[column] == 'Width(w), um'): return True
        if (self.__header[column] == 'Height(h), um'): return True
        if (self.__header[column] == 'Diameter(d1), um'): return True
        if (self.__header[column] == 'Diameter(d2), um'): return True
        if (self.__header[column] == 'No. of cells/counting unit'): return True
        if (self.__header[column] == 'Calculated volume, um3'): return True
        if (self.__header[column] == 'Filament: length of cell, um'): return True
        if (self.__header[column] == 'Calculated Carbon pg/counting unit'): return True
        return False     

class PrepareSmhiPhytoplanktonList(DataSources):
    """
    The PEG (Plankton Expert Group)-list does not cover all planktons found on
    the Swedish west coast and a special list has to be maintained for the
    datasets managed by SMHI. The sources for the SMHI Phytoplankton list is
    the planktonlist used in PW at SMHI, the PEG-list and two translation
    lists. One translation list from the PW list to PEG, and one from 
    PEG to Dyntaxa.
    The result of this plaktonlist preparation is a Json file containing one 
    Json object for each taxon. Example:
    {
    ...
    } 
    """
    def __init__(self, taxaObject = None):
        """ """
        super(PrepareSmhiPhytoplanktonList, self).__init__(taxaObject)

    def importTaxa(self, file = None, encoding = 'utf-8'):
        """ """
        self.__header = []
        self.__taxa = self._taxaObject.getTaxonList()
        
#        // 0 NOP    
#        // 1 DIVISION
#        // 2 CLASS
#        // 3 ORDER
#        // 4 GENUS
#        // 5 SPECIESNAME
#        // 6 SUBTYPE
#        // 7 SUBNAME
#        // 8 THROPHY
#        // 9 SIZECLASS
#        // 10 RUBINCODE
#        // 11 DESCRIPTION
#        // 12 LENGTH
#        // 13 WIDTH
#        // 14 VOLUME
#        // 15 NOTUSED
#        // 16 VOLUME2
#        // 17 AUTHOR
#        // 18 UPLOADED_BY

        pwFile = open(file, 'r')
        separator = '\t' # Tab as separator.
        for line in pwFile:
            if len(self.__header) == 0:
                # Store header columns. They will be used as keys i the dictionary.
                importFileHeader = line.split(separator)
                for columnName in importFileHeader: 
                    self.__header.append(self.__translateHeader(columnName.strip().strip('"').strip()))
            else:
                taxonDict = {}
                sizeClassDict = {}
                column = 0
                for value in line.split(separator):
                    value = value.strip().strip('"').strip()
                    if column >= len(self.__header):
                        print 'ERROR: index out of range' + value.strip()
                        continue
                    # Separate columns containing taxon and 
                    # size-class related info.                
                    if self.__isTaxonRelated(column):
                        taxonDict[self.__header[column]] = value.strip()
                    else:
                        if self.__isColumnNumeric(column):
                            try:
                                float_value = float(value.strip().replace(',', '.').replace(' ', ''))
                                sizeClassDict[self.__header[column]] = float_value
                                if self.__header[column] == 'SIZECLASS':  # Covert SIZECLASS to integer.
                                    sizeClassDict[self.__header[column]] = int(float_value)
                            except:
                                # Use string format if not valid numeric. 
                                sizeClassDict[self.__header[column]] = value.strip()
                        else:
                            sizeClassDict[self.__header[column]] = value.strip()
                    column += 1
                                
                # Create Species name.
                taxonName = taxonDict['GENUS'] + ' ' + \
                            taxonDict['SPECIESNAME'] + ' ' + \
                            taxonDict['SUBTYPE'] + ' ' + \
                            taxonDict['SUBNAME']
                taxonDict['Species'] = taxonName.strip()
                # Check if the taxon-related data already exists.
                taxonExists = False
                for taxon in self.__taxa:
                    if  taxon['Species'] == taxonDict['Species']:
                        taxonExists = True
                        taxon['Size classes'].append(sizeClassDict)
                        continue
                # First time. Create the list and add dictionary for 
                # size classes. 
                if taxonExists == False:
                    self.__taxa.append(taxonDict)
                    taxonDict['Size classes'] = []
                    taxonDict['Size classes'].append(sizeClassDict)

                
        pwFile.close()
        
    def __translateHeader(self, importFileHeader):
        """ Convert import file column names to key names used in dictionary. """        
#        if (importFileHeader == 'PW-Taxon att behålla trots ej i PEG'): return 'PW-Taxon not in PEG'
#        if (importFileHeader == 'PW-sizeClass att beh'): return 'PW-SizeClass not in PEG'
        return importFileHeader   

    def __isTaxonRelated(self, column):
        """ """        
        if (self.__header[column] == 'NOP'): return True
        if (self.__header[column] == 'DIVISION'): return True
        if (self.__header[column] == 'CLASS'): return True
        if (self.__header[column] == 'ORDER'): return True
        if (self.__header[column] == 'GENUS'): return True
        if (self.__header[column] == 'SPECIESNAME'): return True
        if (self.__header[column] == 'SUBTYPE'): return True
        if (self.__header[column] == 'SUBNAME'): return True
        if (self.__header[column] == 'THROPHY'): return True
        if (self.__header[column] == 'RUBINCODE'): return True
        if (self.__header[column] == 'AUTHOR'): return True
        return False # Related to size class.     
        
    def __isColumnNumeric(self, column):
        """ """        
        if (self.__header[column] == 'SIZECLASS'): return True
        if (self.__header[column] == 'LENGTH'): return True
        if (self.__header[column] == 'WIDTH'): return True
        if (self.__header[column] == 'VOLUME'): return True
        if (self.__header[column] == 'VOLUME2'): return True
        return False

