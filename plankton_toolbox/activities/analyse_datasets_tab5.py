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

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
#import datetime
import copy
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import mmfw

@mmfw.singleton
#class AnalyseDatasetsTab5(activity_base.ActivityBase):
class AnalyseDatasetsTab5(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """

    def setMainActivity(self, analyse_dataset_activity):
        """ """
        self.__analysedatasetactivity = analyse_dataset_activity
                
    def clear(self):
        """ """
        
    def update(self):
        """ """        

    # ===== TAB: Prepared graphs ===== 
    def contentPreparedGraphs(self):
        """ """
        # Active widgets and connections.

        # Layout.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
#        layout.addWidget(selectionbox)
#        layout.addWidget(resultbox)
        #
        return widget

