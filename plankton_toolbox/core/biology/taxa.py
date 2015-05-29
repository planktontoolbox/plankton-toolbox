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
from abc import abstractmethod

class Taxa(object):
    """
    Abstract base class for lists of taxon. 
    """
    def __init__(self):
        """ """
        self._metadata = {} # Metadata for the dataset.
        self._data = [] # List of taxon objects in the dataset.
        self._idToTaxonDict = {} # For fast lookup.
        self._nameToTaxonDict = {} # For fast lookup.
        
    def clear(self):
        """ """
        self._metadata.clear()
        self._metadata.clear()
        del self._data[:] # Clear the list.
        self._idToTaxonDict.clear()
        self._nameToTaxonDict.clear()
        
    def getMetadata(self):
        """ """
        return self._metadata
        
    def getTaxonList(self):
        """ """
        return self._data
        
    def getIdToTaxonDict(self):
        """ Note: No loading on demand. Use getTaxonById() instead. """
        return self._idToTaxonDict
        
    def getTaxonListSortedBy(self, sortField):
        """ """
        raise UserWarning('Not implemented: getTaxonListSortedBy.')
        
    def getTaxonById(self, taxonId):
        """ """
        if len(self._idToTaxonDict) == 0:
            self._createIdToTaxonLookup() # On demand. Should be implemented in subclasses.
        if self._idToTaxonDict.has_key(taxonId):
            return self._idToTaxonDict[taxonId]
        else:
            return None
    
    def getTaxonByName(self, taxonName):
        """ """
        if len(self._nameToTaxonDict) == 0:
            self._createNameToTaxonDict() # On demand. Should be implemented in subclasses.
        if self._nameToTaxonDict.has_key(taxonName):
            return self._nameToTaxonDict[taxonName]
        return None
    
    @abstractmethod
    def _createIdToTaxonLookup(self):
        """ Note: Abstract. """

    @abstractmethod
    def _createNameToTaxonDict(self):
        """ Note: Abstract. """

        
class NordicMicroalgae(Taxa):
    """ 
    NordicMicroalgae, http://nordicmicroalgae.org
    """
    def __init__(self):
        """ """
        self._sortedNameList = None
        # Initialize parent.
        super(NordicMicroalgae, self).__init__()

    def clear(self):
        """ """
        self._sortedNameList = None
        super(NordicMicroalgae, self).clear()
        
    def _createIdToTaxonLookup(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            id = taxon.get('Taxon id', None)
            if id:
                self._idToTaxonDict[id] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def _createNameToTaxonDict(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            name = taxon.get('Scientific name', None)
            if name:
                self._nameToTaxonDict[name] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def getSortedNameList(self):
        """ 
        Used when a sorted list of taxon is needed.
        Format: [taxon, ...]
        """
        if self._sortedNameList == None:
            self._sortedNameList = []
            for taxon in self._data:
                self._sortedNameList.append(taxon)
            # Sort.
            self._sortedNameList.sort(dyntaxaname_sort) # Sort function defined below.
        return self._sortedNameList
            
# Sort function for scientific name list.
def nordicmicroalgaename_sort(s1, s2):
    """ """
    # Check names first.
    name1 = s1.get('Scientific name', '')
    name2 = s2.get('Scientific name', '')
    if name1 < name2: return -1
    if name1 > name2: return 1
    return 0 # Both are equal.


class Dyntaxa(Taxa):
    """ 
    Dynamisk Taxa, delivered by ArtDatabanken: 
    http://artdatabanken.se or http://www.artdata.slu.se/english 
    """
    def __init__(self):
        """ """
        self._sortedNameList = None
        # Initialize parent.
        super(Dyntaxa, self).__init__()

    def clear(self):
        """ """
        self._sortedNameList = None
        super(Dyntaxa, self).clear()
        
    def _createIdToTaxonLookup(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            id = taxon.get('Taxon id', None)
            if id:
                self._idToTaxonDict[id] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def _createNameToTaxonDict(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            name = taxon.get('Scientific name', None)
            if name:
                self._nameToTaxonDict[name] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def getSortedNameList(self):
        """ 
        Used when a sorted list of taxon is needed.
        Format: [taxon, ...]
        """
        if self._sortedNameList == None:
            self._sortedNameList = []
            for taxon in self._data:
                self._sortedNameList.append(taxon)
            # Sort.
            self._sortedNameList.sort(dyntaxaname_sort) # Sort function defined below.
        return self._sortedNameList
            
# Sort function for scientific name list.
def dyntaxaname_sort(s1, s2):
    """ """
    # Check names first.
    name1 = s1.get('Scientific name', '')
    name2 = s2.get('Scientific name', '')
    if name1 < name2: return -1
    if name1 > name2: return 1
    return 0 # Both are equal.


class Peg(Taxa):
    """
    The Phytoplankton Expert Group plankton list.
    Responsible: http://www.helcom.fi
    Download from: http://www.ices.dk/env/repfor/index.asp
    """
    def __init__(self):
        """ """  
        self._nameAndSizeList = None
        # Initialize parent.
        super(Peg, self).__init__()

    def clear(self):
        """ """
        self._nameAndSizeList = None
        super(Peg, self).clear()
        
    def _createNameToTaxonDict(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            self._nameToTaxonDict[taxon['Species']] = taxon

    def getSizeclassItem(self, taxonName, size):
        """ """
        for sizeclass in self.getTaxonByName(taxonName)['Size classes']:
            if unicode(sizeclass['Size class']) == size:
                return sizeclass
        return None

    def getNameAndSizeList(self):
        """ 
        Used when a sorted list of taxon/size is needed.
        Format: [[taxon], [sizeclass], ...]
        """
        if self._nameAndSizeList == None:
            self._nameAndSizeList = []
            for taxon in self._data:
                for sizeclass in taxon['Size classes']:
                    self._nameAndSizeList.append([taxon, sizeclass])
            # Sort.
            self._nameAndSizeList.sort(pegnameandsize_sort) # Sort function defined below.
        return self._nameAndSizeList
            
# Sort function for name and size list.
def pegnameandsize_sort(s1, s2):
    """ """
    # Check names.
    name1 = s1[0]['Species']
    name2 = s2[0]['Species']
    if name1 > name2: return 1
    if name1 < name2: return -1
    # Names are equal, check sizes.
    size1 = s1[1]['Size class']
    size2 = s2[1]['Size class']
    if size1 < size2: return -1
    if size1 > size2: return 1
    return 0 # Both are equal.


class MarineSpecies(Taxa):
    """ 
    """
    def __init__(self):
        """ """
        # Initialize parent.
        super(MarineSpecies, self).__init__()


class HarmfulPlankton(Taxa):
    """ 
    """
    def __init__(self):
        """ """
        self._sortedNameList = None
        # Initialize parent.
        super(HarmfulPlankton, self).__init__()

    def clear(self):
        """ """
        self._sortedNameList = None
        super(HarmfulPlankton, self).clear()
        
    def _createIdToTaxonLookup(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            id = taxon.get('Taxon id', None)
            if id:
                self._idToTaxonDict[id] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def _createNameToTaxonDict(self):
        """ Note: Implementation of abstract method. """
        for taxon in self._data:
            name = taxon.get('Scientific name', None)
            if name:
                self._nameToTaxonDict[name] = taxon
            else:
                print('DEBUG: Name missing.')
            
    def getSortedNameList(self):
        """ 
        Used when a sorted list of taxon is needed.
        Format: [taxon, ...]
        """
        if self._sortedNameList == None:
            self._sortedNameList = []
            for taxon in self._data:
                self._sortedNameList.append(taxon)
            # Sort.
            self._sortedNameList.sort(harmfulplankton_sort) # Sort function defined below.
        return self._sortedNameList

# Sort function for scientific name list.
def harmfulplankton_sort(s1, s2):
    """ """
    # Check names first.
    name1 = s1.get('Scientific name', '')
    name2 = s2.get('Scientific name', '')
    if name1 < name2: return -1
    if name1 > name2: return 1
    return 0 # Both are equal.
