#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtCore as QtCore
# import envmonlib
import toolbox_utils
import toolbox_core

@toolbox_utils.singleton
class ToolboxDatasets(QtCore.QObject):
    """ Toolbox wrapper for toolbox_core.Datasets. Emitted signals for change notifications are added. """
    def __init__(self):
        """ """
        toolbox_core.Datasets()
        # 
        QtCore.QObject.__init__(self)

    def clear(self):
        """ """
        toolbox_core.Datasets().clear()
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)
        
    def getDatasets(self):
        """ """
        return toolbox_core.Datasets().getDatasets()
        
    def getDatasetByIndex(self, index):
        """ """
        return toolbox_core.Datasets().getDatasetByIndex(index)
        
    def addDataset(self, dataset):
        """ """
        toolbox_core.Datasets().addDataset(dataset)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)
        
    def removeDatasetByIndex(self, index):
        """ """
        toolbox_core.Datasets().removeDatasetByIndex(index)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)

    def _emitChangeNotification(self):
        """ """
        self.emit(QtCore.SIGNAL('datasetListChanged'))
