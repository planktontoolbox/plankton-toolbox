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
Tool manager.
"""

import plankton_toolbox.tools.log_tool as log_tool
import plankton_toolbox.tools.toolbox_settings_tool as toolbox_settings_tool
import plankton_toolbox.tools.species_browser_tool as species_browser_tool
import plankton_toolbox.tools.peg_browser_tool as peg_browser_tool
import plankton_toolbox.tools.metadata_editor_tool as metadata_editor_tool
import plankton_toolbox.tools.taxon_facts_tool as taxon_facts_tool
import plankton_toolbox.tools.taxon_images_tool as taxon_images_tool
import plankton_toolbox.tools.latlong_tool as latlong_tool
#import plankton_toolbox.tools.template_tool as template_tool

class ToolManager(object):
    """
    The tool manager is used to set up available tools. 
    """
    
    def __init__(self, parentwidget):
        """ """
        # Initialize parent.
        self._parent = parentwidget
        self.__toollist = [] # List of tools derived from ToolsBase.        

    def initTools(self):
        """ Tool activator. """
        # The log tool should be loaded before other tools.
        self.__toollist.append(log_tool.LogTool("Log tool", self._parent))
        self.__toollist.append(toolbox_settings_tool.ToolboxSettingsTool("Toolbox settings", self._parent))
        self.__toollist.append(species_browser_tool.SpeciesBrowserTool("Species browser", self._parent))
        self.__toollist.append(peg_browser_tool.PegBrowserTool("PEG browser", self._parent))
        self.__toollist.append(metadata_editor_tool.MetadataEditorTool("Metadata editor", self._parent))
        self.__toollist.append(taxon_facts_tool.TaxonFactsTool("Taxon facts", self._parent))
        self.__toollist.append(taxon_images_tool.TaxonImagesTool("Taxon images", self._parent))
        self.__toollist.append(latlong_tool.LatLongTool("Latlong", self._parent))
#        self.__toollist.append(template_tool.TemplateTool("(Tool template)", self._parent))
        
    def showTool(self, index):
        """ Makes a tool visible. """
        self.__toollist[index].show()
        self.__toollist[index].raise_() # Bring to front.
        
    def getToolList(self):
        """ """
        return self.__toollist
