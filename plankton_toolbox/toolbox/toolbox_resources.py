#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""


TODO: Not used in current version. Should be rewritten and integrated with toolbox_utils.


"""

#import plankton_toolbox.PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
# import envmonlib
import toolbox_utils
import toolbox_core
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

@toolbox_utils.singleton
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
        
    def load_all_resources(self):
        """ """
#        self.load_resource_dyntaxa()
#        self.load_resource_peg()
#        self.load_resource_harmful_plankton()

    def load_unloaded_resources(self):
        """ """
        if not self._dyntaxaloaded:
            self.load_resource_dyntaxa()
        if not self._pegloaded:
            self.load_resource_peg()
        if not self._harmfulplanktonloaded:
            self.load_resource_harmful_plankton()

    def load_unloaded_resource_dyntaxa(self):
        """ """
        if not self._dyntaxaloaded:
            self.load_resource_dyntaxa()

    def load_resource_dyntaxa(self):
        """ """
        self._dyntaxa.clear()
        self._dyntaxaloaded = False 
        importer = taxa_sources.JsonFile(taxaObject = self._dyntaxa)
        filepath = toolbox_settings.ToolboxSettings().get_value('Resources:Dyntaxa:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._dyntaxaloaded = True 
        self.emit(QtCore.SIGNAL('dyntaxaResourceLoaded'))
        toolbox_utils.Logging().log('Toolbox resources: Dyntaxa loaded (' +  
                            unicode(len(self._dyntaxa.getTaxonList())) + ' taxon).')
        
    def load_unloaded_resource_peg(self):
        """ """
        if not self._pegloaded:
            self.load_resource_peg()
        
    def load_resource_peg(self):
        """ """
        self._peg.clear()
        self._pegloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self._peg)
        filepath = toolbox_settings.ToolboxSettings().get_value('Resources:PEG:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._pegloaded = True
        self.emit(QtCore.SIGNAL('pegResourceLoaded'))
        toolbox_utils.Logging().log('Toolbox resources: PEG loaded (' +  
                            unicode(len(self._peg.getNameAndSizeList())) + ' sizeclasses).')

    def load_unloaded_resource_harmful_plankton(self):
        """ """
        if not self._harmfulplanktonloaded:
            self.load_resource_harmful_plankton()

    def load_resource_harmful_plankton(self):
        """ """
        self._harmfulplankton.clear()
        self._harmfulplanktonloaded = False
        importer = taxa_sources.JsonFile(taxaObject = self._harmfulplankton)
        filepath = toolbox_settings.ToolboxSettings().get_value('Resources:Harmful plankton:Filepath')
        importer.importTaxa(file = filepath)
        # Emit signal.
        self._harmfulplanktonloaded = True
        self.emit(QtCore.SIGNAL('harmfulPlanktonResourceLoaded'))
        toolbox_utils.Logging().log('Toolbox resources: Harmful plankton loaded (' +  
                            unicode(len(self._harmfulplankton.getTaxonList())) + ' taxon).')
        
    def get_resource_dyntaxa(self):
        """ """
        return self._dyntaxa
        
    def get_resource_peg(self):
        """ """
        return self._peg
        
    def get_resource_harmful_plankton(self):
        """ """
        return self._harmfulplankton

