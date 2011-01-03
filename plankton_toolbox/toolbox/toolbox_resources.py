#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
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

"""

"""

import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

@utils.singleton
class ToolboxResources(object):
    """
    """
    def __init__(self):
        """ """
        self.__taxa_resource = None
        self.__peg_resource = None
        self.__ioc_resource = None 
        
    def loadResources(self):
        """ """
        self.__loadTaxaResource()
        self.__loadPegResource()
        self.__loadIocResource()

    def __loadTaxaResource(self):
        """ """

        
    def __loadPegResource(self):
        """ """
        self.__peg_resource = taxa.Peg()
        importer = taxa_sources.JsonFile(taxaObject = self.__peg_resource)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        importer.importTaxa(file = filepath)
        
    def __loadIocResource(self):
        """ """
        # TODO.
        
    def getTaxaResource(self):
        """ """
        return self.__taxa_resource
        
    def getPegResource(self):
        """ """
        return self.__peg_resource
        
    def getIocResource(self):
        """ """
        return self.__ioc_resource
