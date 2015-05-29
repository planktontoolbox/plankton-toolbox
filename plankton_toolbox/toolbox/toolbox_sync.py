#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtCore as QtCore
import envmonlib

@envmonlib.singleton
class ToolboxSync(QtCore.QObject):
    """ """
    def __init__(self):
        """ """
        self._test = None 
        # 
        QtCore.QObject.__init__(self)

    def clear(self):
        """ """
        self._test = None 
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitChangeNotification)
        
    def setRow(self, rowIndex):
        """ """
        self._test = rowIndex 
        # Emit signal after short delay.
        QtCore.QTimer.singleShot(100, self._emitSelectedRowChangedTEST)
        
    def getRow(self):
        """ """
        return self._test 
        
    def _emitSelectedRowChangedTEST(self):
        """ """
        self.emit(QtCore.SIGNAL('toolboxSyncSelectedRow'))
