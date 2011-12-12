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

"""
Resources are datasets that are commonly used in the Plankton Toolbox.
Datasets managed as resources are:
- Dyntaxa. Taxa received from Artdatabanken.se
- PEG. From HELCOM Phytoplankton Expert Group (HELCOM PEG). Contains sizeclass related information. 
- Harmful plankton. From IOC.
"""

#import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import toolbox.utils as utils
import toolbox.toolbox_settings as toolbox_settings
import core.biology.taxa as taxa
import core.biology.taxa_sources as taxa_sources

@utils.singleton
class ToolboxResources(QtCore.QObject):
    """
    Resources are datasets that are commonly used in the Plankton Toolbox.
    """
    def __init__(self):
        """ """
        self.__dyntaxa = taxa.Dyntaxa() 
        self.__peg = taxa.Peg()
        self.__harmfulplankton = taxa.HarmfulPlankton()
        self.__dyntaxaloaded = False 
        self.__pegloaded = False
        self.__harmfulplanktonloaded = False
        # 
        QtCore.QObject.__init__(self)
        
    def loadAllResources(self):
        """ """
        self.loadResourceDyntaxa()
        self.loadResourcePeg()
        self.loadResourceHarmfulPlankton()

    def loadUnloadedResources(self):
        """ """
        if not self.__dyntaxaloaded:
            self.loadResourceDyntaxa()
        if not self.__pegloaded:
            self.loadResourcePeg()
        if not self.__harmfulplanktonloaded:
            self.loadResourceHarmfulPlankton()

    def loadUnloadedResourceDyntaxa(self):
        """ """
        if not self.__dyntaxaloaded:
            self.loadResourceDyntaxa()

    def loadResourceDyntaxa(self):
        """ """
        self.__dyntaxa.clear()
        self.__dyntaxaloaded = False 
        importer = taxa_sources.JsonFile(taxaObject = self.__dyntaxa)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self.__dyntaxaloaded = True 
        self.emit(QtCore.SIGNAL('dyntaxaResourceLoaded'))
        utils.Logger().log('Toolbox resources: Dyntaxa loaded (' +  
                            unicode(len(self.__dyntaxa.getTaxonList())) + ' taxon).')
        
    def loadUnloadedResourcePeg(self):
        """ """
        if not self.__pegloaded:
            self.loadResourcePeg()
        
    def loadResourcePeg(self):
        """ """
        self.__peg.clear()
        self.__pegloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self.__peg)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self.__pegloaded = True
        self.emit(QtCore.SIGNAL('pegResourceLoaded'))
        utils.Logger().log('Toolbox resources: PEG loaded (' +  
                            unicode(len(self.__peg.getNameAndSizeList())) + ' sizeclasses).')

    def loadUnloadedResourceHarmfulPlankton(self):
        """ """
        if not self.__harmfulplanktonloaded:
            self.loadResourceHarmfulPlankton()

    def loadResourceHarmfulPlankton(self):
        """ """
        self.__harmfulplankton.clear()
        self.__harmfulplanktonloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self.__harmfulplankton)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self.__harmfulplanktonloaded = True
        self.emit(QtCore.SIGNAL('harmfulPlanktonResourceLoaded'))
        utils.Logger().log('Toolbox resources: Harmful plankton loaded (' +  
                            unicode(len(self.__harmfulplankton.getTaxonList())) + ' taxon).')
        
    def getResourceDyntaxa(self):
        """ """
        return self.__dyntaxa
        
    def getResourcePeg(self):
        """ """
        return self.__peg
        
    def getResourceHarmfulPlankton(self):
        """ """
        return self.__harmfulplankton

