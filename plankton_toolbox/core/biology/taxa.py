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

"""

from abc import abstractmethod

class Taxa(object):
    """
    Abstract base class for lists of taxon. 
    """
    def __init__(self):
        self._metadata = {} # Metadata for the dataset.
        self._data = [] # List of taxon objects.
        self._idToTaxonMap = {} # For fast lookup.
        self._nameToTaxonMap = {} # For fast lookup.
        
    def clearMetadata(self):
        """ """
        self._metadata.clear()
        
    def getMetadata(self):
        """ """
        return self._metadata
        
    def clearTaxonList(self):
        """ """
        del self._data[:]
        
    def getTaxonList(self):
        """ """
        return self._data
        
    def getIdToTaxonMap(self):
        """ """
        return self._idToTaxonMap
        
    def getNameToTaxonMap(self):
        """ """
        return self._nameToTaxonMap
        
    def getTaxonListSortedBy(self, sortField):
        """ """
        raise UserWarning('Not implemented: getTaxonListSortedBy.')
        
    def getTaxonById(self, taxonId):
        """ """
        if len(self._idToTaxonMap) == 0:
            self._createIdToTaxonLookup() # On demand
        if self._idToTaxonMap.has_key(taxonId):
            return self._idToTaxonMap[taxonId]
        else:
            return None
    
    def getTaxonByName(self, taxonName):
        """ """
        if len(self._nameToTaxonMap) == 0:
            self._createNameToTaxonMap() # On demand
        if self._nameToTaxonMap.has_key(taxonName):
            return self._nameToTaxonMap[taxonName]
        else:
            return None
    
    @abstractmethod
    def _createIdToTaxonLookup(self):
        """ """
#        raise UserWarning('Not implemented: _createNameToTaxonMap.')

    @abstractmethod
    def _createNameToTaxonMap(self):
        """ """
#        raise UserWarning('Not implemented: _createNameToTaxonMap.')

        
class Dyntaxa(Taxa):
    """ 
    Dynamisk Taxa, delivered by ArtDatabanken: 
    http://artdatabanken.se or http://www.artdata.slu.se/english 
    """
    def __init__(self):
        """ """
        super(Dyntaxa, self).__init__()


class Peg(Taxa):
    """
    The Phytoplankton Expert Group plankton list.
    Responsible: http://www.helcom.fi
    Download from: http://www.ices.dk/env/repfor/index.asp
    """
    def __init__(self):
        """ """
        super(Peg, self).__init__()

    def _createNameToTaxonMap(self):
        """ """
        for taxon in self._data:
            self._nameToTaxonMap[taxon['Species']] = taxon


class MarineSpecies(Taxa):
    """ 
    """
    def __init__(self):
        """ """
        super(MarineSpecies, self).__init__()


class Ioc(Taxa):
    """ 
    """
    def __init__(self):
        """ """
        super(Ioc, self).__init__()

