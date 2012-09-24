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


TODO: Not used in current version. Should be rewritten and integrated with envmonlib.


"""


import pickle
import copy
import PyQt4.QtCore as QtCore
import envmonlib

@envmonlib.singleton
class ToolboxSettings(QtCore.QObject):
    """
    Contains settings for the Plankton Toolbox application. 
    """
    def __init__(self):
        """ """
        self._default_settings = {
            "General": {
                "Character encoding, txt-files": "cp1252",
                "Character encoding, json-files": "cp1252",
                "Decimal delimiter": ","
            },
            "Resources": {
                "Dyntaxa": {
                    "Filepath": "../planktondata/resources/smhi_dv_dyntaxa.json",
                },
                "PEG": {
                    "Filepath": "../planktondata/resources/smhi_extended_peg.json",
                    "PW to PEG filepath": "../planktondata/resources/translate_pw_to_smhi_extended_peg.txt",
                    "PEG to Dyntaxa filepath": "../planktondata/resources/smhi_peg_to_dyntaxa.txt"
                },
                "Harmful plankton": {
                    "Filepath": "../planktondata/resources/smhi_harmful_plankton.json"
                },
                "Load at startup": True 
            },
            "Datasets": {
                "Dataset types": {
                    "PW": {
                    },
                    "Generic table": {
                    },
                    "Sharkweb": {
                        "URL": "",
                        "Header language": "en"
                    }
                }
            }
        }
        self._settings = self._default_settings
        #
        QtCore.QObject.__init__(self) # TODO: Check...
        
    def loadSettings(self, ui_settings):
        """ Load settings from QtCore.QSettings object. """
        serialized_settings = ui_settings.value('Toolbox settings', QtCore.QVariant('')).toByteArray()
        if len(serialized_settings) == 0:
            self._settings = self._default_settings # Use default if not stored earlier.
        else:
            self._settings = pickle.loads(serialized_settings)
        # Emit signal.
        self.emit(QtCore.SIGNAL('settingsChanged'))

    def saveSettings(self, ui_settings):
        """ Store settings to QtCore.QSettings object."""
        serialized_settings = pickle.dumps(self._settings)
        ui_settings.setValue('Toolbox settings', QtCore.QVariant(serialized_settings))

    def restoreDefault(self):
        """ """
        # Deep copy needed.
        self._settings = copy.deepcopy(self._default_settings)
        # Emit signal.
        self.emit(QtCore.SIGNAL('settingsChanged'))

    def getValue(self, compoundkey, default = ''):
        """ Use compound key with field delimiter ':'. """
        current_level_item = self._settings
        # Split the key and walk down in dictionary hierarchy..
        # Current_level_item will became value at last level.
        for keypart in compoundkey.split(':'):
            if current_level_item:
                current_level_item = current_level_item.get(keypart, None)
        if current_level_item:
            return current_level_item
        else:
            return default

    def setValue(self, compoundkey, value):
        """ Use compound key with field delimiter ':'. """
        current_level_item = self._settings
        last_used_dict = current_level_item
        # Split the key and walk down in dictionary hierarchy.
        # Current_level_item will became value at final level.
        for keypart in compoundkey.split(':'):
            last_used_dict = current_level_item
            current_level_item = current_level_item.get(keypart, None)
            if not current_level_item:
                last_used_dict[keypart] = {}
                current_level_item = last_used_dict[keypart]
        last_used_dict[keypart] = value
#        # Emit signal.
#        self.emit(QtCore.SIGNAL('settingsChanged'))
       
