#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import app_framework
import app_tools

@app_framework.singleton
class ToolManager(object):
    """
    The tool manager is used to set up available tools. 
    """
    def __init__(self):
        """ """
        self._parent = None
        self._toollist = [] # List of tools derived from ToolsBase.

    def set_parent(self, parentwidget):
        """ """
        self._parent = parentwidget

    def init_tools(self):
        """ Tool activator. """
        self._toollist.append(app_tools.DatasetViewerTool('Dataset viewer', self._parent))
        self._toollist.append(app_tools.GraphPlotterTool('Graph plotter', self._parent))
        self._toollist.append(app_tools.LogTool('Toolbox logging', self._parent))

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
