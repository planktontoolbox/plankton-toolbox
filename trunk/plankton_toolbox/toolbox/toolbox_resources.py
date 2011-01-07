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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

@utils.singleton
class ToolboxResources(QtCore.QObject):
    """
    """
    def __init__(self):
        """ """
        self.__dyntaxa = taxa.Dyntaxa() 
        self.__peg = taxa.Peg()
        self.__ioc = taxa.Ioc()
        # 
        ###super(ToolboxResources, self).__init__(None)
        QtCore.QObject.__init__(self) # TODO: Check...
        
    def loadResources(self):
        """ """
        self.__loadDyntaxa()
        self.__loadPeg()
        self.__loadIoc()

    def __loadDyntaxa(self):
        """ """
        self.__dyntaxa.clear()
        importer = taxa_sources.JsonFile(taxaObject = self.__dyntaxa)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self.emit(QtCore.SIGNAL('dyntaxaResourceLoaded'))
        utils.Logger().info('Toolbox resources: Dyntaxa loaded (' +  
                            unicode(len(self.__dyntaxa.getTaxonList())) + ' taxon).')
        
    def __loadPeg(self):
        """ """
        self.__peg.clear()
        importer = taxa_sources.JsonFile(taxaObject = self.__peg)
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self.emit(QtCore.SIGNAL('pegResourceLoaded'))
        utils.Logger().info('Toolbox resources: PEG loaded (' +  
                            unicode(len(self.__peg.getNameAndSizeList())) + ' sizeclasses).')

    def __loadIoc(self):
        """ """
#        if not self.__ioc_resource:
#            self.__ioc_resource =  
        
    def getResourceDyntaxa(self):
        """ """
        return self.__dyntaxa
        
    def getResourcePeg(self):
        """ """
        return self.__peg
        
    def getResourceIoc(self):
        """ """
        return self.__ioc

