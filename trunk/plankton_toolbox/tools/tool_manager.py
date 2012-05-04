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
Tool manager.
"""

import plankton_toolbox.tools.toolbox_settings_tool as toolbox_settings_tool
import plankton_toolbox.tools.log_tool as log_tool
import plankton_toolbox.tools.dataset_viewer_tool as dataset_viewer_tool
import plankton_toolbox.tools.metadata_editor_tool as metadata_editor_tool
import plankton_toolbox.tools.dyntaxa_browser_tool as dyntaxa_browser_tool
import plankton_toolbox.tools.peg_browser_tool as peg_browser_tool
import plankton_toolbox.tools.harmful_plankton_browser_tool as harmful_plankton_browser_tool
import plankton_toolbox.tools.taxon_facts_tool as taxon_facts_tool
import plankton_toolbox.tools.taxon_images_tool as taxon_images_tool
import plankton_toolbox.tools.latlong_tool as latlong_tool

import plankton_toolbox.tools.graphplot_tool as graphplot_tool

import envmonlib

#import tools.template_tool as template_tool

@envmonlib.singleton
class ToolManager(object):
    """
    The tool manager is used to set up available tools. 
    """
    
#    def __init__(self, parentwidget):
#        """ """
#        # Initialize parent.
#        self._parent = parentwidget
#        self._toollist = [] # List of tools derived from ToolsBase.        

    def __init__(self):
        """ """
        # Initialize parent.
        self._parent = None
        self._toollist = [] # List of tools derived from ToolsBase.        

    def setParent(self, parentwidget):
        """ """
        self._parent = parentwidget

    def initTools(self):
        """ Tool activator. """
        # The log tool should be loaded before other tools.
        self._toollist.append(dataset_viewer_tool.DatasetViewerTool("Dataset viewer", self._parent))
        self._toollist.append(graphplot_tool.GraphPlotTool("Graph plot", self._parent))
#        self._toollist.append(dyntaxa_browser_tool.DyntaxaBrowserTool("Dyntaxa browser", self._parent))
#        self._toollist.append(peg_browser_tool.PegBrowserTool("PEG browser", self._parent))
#        self._toollist.append(harmful_plankton_browser_tool.HarmfulPlanktonBrowserTool("Harmful plankton", self._parent))
        self._toollist.append(latlong_tool.LatLongTool("Latitude-longitude", self._parent))
#        self._toollist.append(toolbox_settings_tool.ToolboxSettingsTool("Toolbox settings", self._parent))
        self._toollist.append(log_tool.LogTool("Toolbox logging", self._parent))
#        self._toollist.append(metadata_editor_tool.MetadataEditorTool("(Metadata editor)", self._parent))
#        self._toollist.append(taxon_facts_tool.TaxonFactsTool("(Taxon facts)", self._parent))
#        self._toollist.append(taxon_images_tool.TaxonImagesTool("(Taxon images)", self._parent))
#        self._toollist.append(template_tool.TemplateTool("(Tool template)", self._parent))
        
    def getToolByName(self, object_name):
        """ Makes a tool visible. """
        for tool in self._toollist:
            if tool.objectName() == object_name: 
                return tool
        
    def showToolByIndex(self, index):
        """ Makes a tool visible. """
        self._toollist[index].show()
        self._toollist[index].raise_() # Bring to front.
        
    def showToolByName(self, object_name):
        """ Makes a tool visible. """
        for index, tool in enumerate(self._toollist):
            if tool.objectName() == object_name: 
                self._toollist[index].show()
                self._toollist[index].raise_() # Bring to front.
                return
        
    def getToolList(self):
        """ """
        return self._toollist
