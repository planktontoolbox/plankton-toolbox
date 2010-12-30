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

#import date
#import datetime
from abc import abstractmethod
import codecs
import json
import plankton_toolbox.toolbox.utils as utils

class DataSources(object):
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


class JsonFile(DataSources):
    """ Mainly used to load resource files. """
    def __init__(self, taxaObject = None):
        """ """
        # Initialize parent.
        super(JsonFile, self).__init__(taxaObject)

    def importTaxa(self, file = None, encoding = 'utf-8'):
        """ """
        if file == None:
            raise UserWarning('File name is missing.')
###        indata = open(file, 'r')
        indata = codecs.open(file, mode = 'r', encoding = encoding)
        self._taxaObject.clearMetadata()
        self._taxaObject.clearTaxonList()
        jsonimport = json.loads(indata.read(), encoding = encoding)
        self._taxaObject.getMetadata().update(jsonimport['metadata'])
        self._taxaObject.getTaxonList().extend(jsonimport['data'])
# OLD:
#        self._taxaObject.getTaxonList().extend(
#                    json.loads(indata.read(), encoding = encoding))
        indata.close()

    def exportTaxa(self, file = None, encoding = 'utf-8'):
        """ """
        utils.Logger().info("Writes taxa to: " + file)
        if file == None:
            raise UserWarning('File name is missing.')
        outdata = open(file, 'w')
        
        jsonexport = {}
        jsonexport['metadata'] = self._taxaObject.getMetadata()
        jsonexport['data'] = self._taxaObject.getTaxonList()
        outdata.write(json.dumps(jsonexport, encoding = encoding, 
                                 sort_keys=True, indent=4))
# OLD:        
#        outdata.write(json.dumps(self._taxaObject.getTaxonList(), 
#                                 encoding = encoding, sort_keys=True, indent=4))
        outdata.close()


class DyntaxaRest(DataSources):
    """ For future use. """
    def __init__(self, taxaObject = None):
        """ """
        super(DyntaxaRest, self).__init__(taxaObject)

#    def importTaxa(self, url = None):
#        """ TODO """
        

class DyntaxaSoap(DataSources):
    """ For future use. """
    def __init__(self, taxaObject = None):
        """ """
        # Initialize parent.
        super(DyntaxaSoap, self).__init__(taxaObject)

#    def importTaxa(self, url = None):
#        """ TODO """
        

class MarineSpeciesSoap(DataSources):
    """ For future use. """
    def __init__(self, taxaObject = None):
        """ """
        # Initialize parent.
        super(MarineSpeciesSoap, self).__init__(taxaObject)

#    def importTaxa(self, url = None):
#        """ TODO """


class CouchDb(DataSources):
    """ Used for test. """
    def __init__(self, taxaObject = None):
        """ """
        # Initialize parent.
        super(CouchDb, self).__init__(taxaObject)

#    def importTaxa(self, url = None):
#        """ TODO """
#        
#    def exportTaxa(self, url = None):
#        """ TODO """
        

class GoogleAppEngine(DataSources):
    """ Used for test. """
    def __init__(self, taxaObject = None):
        """ """
        # Initialize parent.
        super(GoogleAppEngine, self).__init__(taxaObject)

#    def importTaxa(self, url = None):
#        """ TODO """
#        
#    def exportTaxa(self, url = None):
#        """ TODO """

