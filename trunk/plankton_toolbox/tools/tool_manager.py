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

import plankton_toolbox.tools.template_tool as template_tool
import plankton_toolbox.tools.log_tool as log_tool

class ToolManager():
    """ 
    """
    
    def __init__(self, parentwidget):
        """ """
        self._parent = parentwidget
        self.__toollist = [] # List of tools derived from ToolsBase.        

    def initTools(self):
        """ Tool activator. """
        self.__toollist.append(template_tool.TemplateTool("Template tool", self._parent))
        self.__toollist.append(log_tool.LogTool("Log tool", self._parent))
        
    def showTool(self, index):
        """ Makes a tool visible. """
        self.__toollist[index].show()
        self.__toollist[index].raise_() # Bring to front.
        
    def getToolList(self):
        """ """
        return self.__toollist
