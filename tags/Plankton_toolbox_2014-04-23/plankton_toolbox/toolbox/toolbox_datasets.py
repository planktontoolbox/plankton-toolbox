#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtCore as QtCore
import envmonlib

@envmonlib.singleton
class ToolboxDatasets(QtCore.QObject):
    """ Toolbox wrapper for envmonlib.Datasets. Emitted signals for change notifications are added. """
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
