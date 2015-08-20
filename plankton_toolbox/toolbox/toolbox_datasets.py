#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtCore as QtCore
import toolbox_utils
import plankton_core

@toolbox_utils.singleton
class ToolboxDatasets(QtCore.QObject):
    """ Toolbox wrapper for plankton_core.Datasets. Emitted signals for change notifications are added. """
    def __init__(self):
        """ """
        plankton_core.Datasets()
        # 
        QtCore.QObject.__init__(self)

    def clear(self):
        """ """
        plankton_core.Datasets().clear()
        # Emit signal.
        self._emit_change_notification()
        
    def get_datasets(self):
        """ """
        return plankton_core.Datasets().get_datasets()
        
    def get_dataset_by_index(self, index):
        """ """
        return plankton_core.Datasets().get_dataset_by_index(index)
        
    def add_dataset(self, dataset):
        """ """
        plankton_core.Datasets().add_dataset(dataset)
        # Emit signal.
        self._emit_change_notification()
        
    def remove_dataset_by_index(self, index):
        """ """
        plankton_core.Datasets().remove_dataset_by_index(index)
        # Emit signal.
        self._emit_change_notification()

    def emit_change_notification(self):
        """ Public. """
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emit_change_notification)

    def _emit_change_notification(self):
        """ Internal. """
        self.emit(QtCore.SIGNAL('datasetListChanged'))
