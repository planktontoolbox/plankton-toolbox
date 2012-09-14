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
"""

import PyQt4.QtCore as QtCore
import envmonlib

@envmonlib.singleton
class ToolboxDatasets(QtCore.QObject):
    """ Wrapper for envmonlib.Datasets. Emitted signals for change notifications are added. """
    def __init__(self):
        """ """
        envmonlib.Datasets()
        # 
        QtCore.QObject.__init__(self)

    def clear(self):
        """ """
        envmonlib.Datasets().clear()
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)
        
    def getDatasets(self):
        """ """
        return envmonlib.Datasets().getDatasets()
        
    def getDatasetByIndex(self, index):
        """ """
        return envmonlib.Datasets().getDatasetByIndex(index)
        
    def addDataset(self, dataset):
        """ """
        envmonlib.Datasets().addDataset(dataset)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)
        
    def removeDatasetByIndex(self, index):
        """ """
        envmonlib.Datasets().removeDatasetByIndex(index)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)

    def _emitChangeNotification(self):
        """ """
        self.emit(QtCore.SIGNAL('datasetListChanged'))
