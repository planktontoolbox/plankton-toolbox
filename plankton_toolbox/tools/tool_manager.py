#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_toolbox.tools.dev_test_tool as dev_test_tool
import plankton_toolbox.tools.toolbox_settings_tool as toolbox_settings_tool
import plankton_toolbox.tools.log_tool as log_tool
import plankton_toolbox.tools.dataset_viewer_tool as dataset_viewer_tool
import plankton_toolbox.tools.metadata_editor_tool as metadata_editor_tool
import plankton_toolbox.tools.dyntaxa_browser_tool as dyntaxa_browser_tool
import plankton_toolbox.tools.peg_browser_tool as peg_browser_tool
import plankton_toolbox.tools.harmful_plankton_browser_tool as harmful_plankton_browser_tool
import plankton_toolbox.tools.taxon_facts_tool as taxon_facts_tool
import plankton_toolbox.tools.taxon_images_tool as taxon_images_tool

import plankton_toolbox.tools.graphplotter_tool as graphplotter_tool

import toolbox_utils
import plankton_core

#import tools.template_tool as template_tool

@toolbox_utils.singleton
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
        self._parent = None
        self._toollist = [] # List of tools derived from ToolsBase.

    def set_parent(self, parentwidget):
        """ """
        self._parent = parentwidget

    def init_tools(self):
        """ Tool activator. """
        # The log tool should be loaded before other tools.
        self._toollist.append(dataset_viewer_tool.DatasetViewerTool('Dataset viewer', self._parent))
        self._toollist.append(graphplotter_tool.GraphPlotterTool('Graph plotter', self._parent))
#        self._toollist.append(dyntaxa_browser_tool.DyntaxaBrowserTool('Dyntaxa browser', self._parent))
#        self._toollist.append(peg_browser_tool.PegBrowserTool('PEG browser', self._parent))
#        self._toollist.append(harmful_plankton_browser_tool.HarmfulPlanktonBrowserTool('Harmful plankton', self._parent))
        
#         self._toollist.append(toolbox_settings_tool.ToolboxSettingsTool('Toolbox settings', self._parent))
        
        self._toollist.append(log_tool.LogTool('Toolbox logging', self._parent))
#         self._toollist.append(metadata_editor_tool.MetadataEditorTool('(Metadata editor)', self._parent))
#        self._toollist.append(taxon_facts_tool.TaxonFactsTool('(Taxon facts)', self._parent))
#        self._toollist.append(taxon_images_tool.TaxonImagesTool('(Taxon images)', self._parent))
#        self._toollist.append(template_tool.TemplateTool('(Tool template)', self._parent))

#         self._toollist.append(dev_test_tool.DevTestTool('REMOVE: Development', self._parent))


    def get_tool_by_name(self, object_name):
        """ Returns the tool. """
        for tool in self._toollist:
            if tool.objectName() == object_name: 
                return tool
        return None
        
    def show_tool_by_name(self, object_name):
        """ Makes a tool visible. """
        for tool in self._toollist:
            if tool.objectName() == object_name: 
                tool.show_tool()
                return
        
    def get_tool_list(self):
        """ """
        return self._toollist
