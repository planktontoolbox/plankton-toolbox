#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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


TODO: Not used in current version. Should be rewritten and integrated with envmonlib.


"""


#import plankton_toolbox.PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import envmonlib
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

@envmonlib.singleton
class ToolboxResources(QtCore.QObject):
    """
    Resources are datasets that are commonly used in the Plankton Toolbox.
    Datasets managed as resources are:
    - Dyntaxa. Taxa received from Artdatabanken.se
    - PEG. From HELCOM Phytoplankton Expert Group (HELCOM PEG). Contains sizeclass related information. 
    - Harmful plankton. From IOC.
    """
    def __init__(self):
        """ """
        self._dyntaxa = taxa.Dyntaxa() 
        self._peg = taxa.Peg()
        self._harmfulplankton = taxa.HarmfulPlankton()
        self._dyntaxaloaded = False 
        self._pegloaded = False
        self._harmfulplanktonloaded = False
        # 
        QtCore.QObject.__init__(self)
        
    def loadAllResources(self):
        """ """
#        self.loadResourceDyntaxa()
#        self.loadResourcePeg()
#        self.loadResourceHarmfulPlankton()

    def loadUnloadedResources(self):
        """ """
        if not self._dyntaxaloaded:
            self.loadResourceDyntaxa()
        if not self._pegloaded:
            self.loadResourcePeg()
        if not self._harmfulplanktonloaded:
            self.loadResourceHarmfulPlankton()

    def loadUnloadedResourceDyntaxa(self):
        """ """
        if not self._dyntaxaloaded:
            self.loadResourceDyntaxa()

    def loadResourceDyntaxa(self):
        """ """
        self._dyntaxa.clear()
        self._dyntaxaloaded = False 
        importer = taxa_sources.JsonFile(taxaObject = self._dyntaxa)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._dyntaxaloaded = True 
        self.emit(QtCore.SIGNAL('dyntaxaResourceLoaded'))
        envmonlib.Logging().log('Toolbox resources: Dyntaxa loaded (' +  
                            unicode(len(self._dyntaxa.getTaxonList())) + ' taxon).')
        
    def loadUnloadedResourcePeg(self):
        """ """
        if not self._pegloaded:
            self.loadResourcePeg()
        
    def loadResourcePeg(self):
        """ """
        self._peg.clear()
        self._pegloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self._peg)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._pegloaded = True
        self.emit(QtCore.SIGNAL('pegResourceLoaded'))
        envmonlib.Logging().log('Toolbox resources: PEG loaded (' +  
                            unicode(len(self._peg.getNameAndSizeList())) + ' sizeclasses).')

    def loadUnloadedResourceHarmfulPlankton(self):
        """ """
        if not self._harmfulplanktonloaded:
            self.loadResourceHarmfulPlankton()

    def loadResourceHarmfulPlankton(self):
        """ """
        self._harmfulplankton.clear()
        self._harmfulplanktonloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self._harmfulplankton)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._harmfulplanktonloaded = True
        self.emit(QtCore.SIGNAL('harmfulPlanktonResourceLoaded'))
        envmonlib.Logging().log('Toolbox resources: Harmful plankton loaded (' +  
                            unicode(len(self._harmfulplankton.getTaxonList())) + ' taxon).')
        
    def getResourceDyntaxa(self):
        """ """
        return self._dyntaxa
        
    def getResourcePeg(self):
        """ """
        return self._peg
        
    def getResourceHarmfulPlankton(self):
        """ """
        return self._harmfulplankton

