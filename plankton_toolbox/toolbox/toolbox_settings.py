#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""


TODO: Not used in current version. Should be rewritten and integrated with toolbox_utils.


"""

import pickle
import copy
import PyQt4.QtCore as QtCore
# import envmonlib
import toolbox_utils
import toolbox_core

@toolbox_utils.singleton
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
       
