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
        QtCore.QTimer.singleShot(100, self._emit_change_notification)
        
    def get_datasets(self):
        """ """
        return toolbox_core.Datasets().get_datasets()
        
    def get_dataset_by_index(self, index):
        """ """
        return toolbox_core.Datasets().get_dataset_by_index(index)
        
    def add_dataset(self, dataset):
        """ """
        toolbox_core.Datasets().add_dataset(dataset)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emit_change_notification)
        
    def remove_dataset_by_index(self, index):
        """ """
        toolbox_core.Datasets().remove_dataset_by_index(index)
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emit_change_notification)

    def _emit_change_notification(self):
        """ """
        self.emit(QtCore.SIGNAL('datasetListChanged'))
