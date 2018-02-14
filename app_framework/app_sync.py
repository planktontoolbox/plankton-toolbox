#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtCore
import app_framework

@app_framework.singleton
class AppSync(QtCore.QObject):
    """ """
    selected_row_changed = QtCore.pyqtSignal()
    
    def __init__(self):
        """ """
        self._source_count_dict = {} 
        # 
        QtCore.QObject.__init__(self)

    def clear_all(self):
        """ """
        self._source_count_dict = {} 
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
        self.selected_row_changed.emit()
