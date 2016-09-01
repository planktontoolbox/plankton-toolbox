#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtCore as QtCore
import toolbox_utils
import plankton_core

@toolbox_utils.singleton
class ToolboxSync(QtCore.QObject):
    """ """
    def __init__(self):
        """ """
        self._source_count_dict = {} 
        # 
        QtCore.QObject.__init__(self)

    def clear_all(self):
        """ """
        c = {} 
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emit_selected_row_changed)
        
    def clear(self, source):
        """ """
        if source in self._source_count_dict:
            self._source_count_dict.pop(source) # Remove key and value. 
            # Emit signal after short delay.
            QtCore.QTimer.singleShot(100, self._emit_selected_row_changed)
        
    def set_row_index(self, source, row_index):
        """ """
        self._source_count_dict[source] = row_index 
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emit_selected_row_changed)
        
    def get_row_index(self, source):
        """ """
        return self._source_count_dict.get(source, None) 
        
    def _emit_selected_row_changed(self):
        """ """
        self.emit(QtCore.SIGNAL('toolboxSyncSelectedRow'))
