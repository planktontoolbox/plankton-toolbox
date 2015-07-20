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

# #import date
# #import datetime
# from abc import abstractmethod
# import codecs
# import json
# import envmonlib
import toolbox_utils
import toolbox_core
# import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
# 
# class DataSources(object):
#     """
#     Abstract base class. 
#     """
#     def __init__(self, taxaObject):
#         self._taxaObject = taxaObject
# 
#     @abstractmethod
#     def importTaxa(self):
#         """ Abstract method. """
# #        raise UserWarning('Abstract method not implemented.')
#         
#     @abstractmethod
#     def exportTaxa(self):
#         """ Abstract method. """
# #        raise UserWarning('Abstract method not implemented.')
# 
# 
# class JsonFile(DataSources):
#     """ Mainly used to load resource files. """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(JsonFile, self).__init__(taxaObject)
# 
#     def importTaxa(self, file = None):
#         """ """
#         if file == None:
#             raise UserWarning('File name is missing.')
#         jsonencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, json-files', 'cp1252')
#         indata = codecs.open(file, mode = 'r', encoding = jsonencode)
#         self._taxaObject.clear()
#         jsonimport = json.loads(indata.read(), encoding = jsonencode)
#         self._taxaObject.getMetadata().update(jsonimport['metadata'])
#         self._taxaObject.getTaxonList().extend(jsonimport['data'])
#         indata.close()
# 
#     def exportTaxa(self, file = None):
#         """ """
#         toolbox_utils.Logging().log('Writes taxa to: ' + file)
#         if file == None:
#             raise UserWarning('File name is missing.')
#         jsonencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, json-files', 'cp1252')
#         outdata = open(file, 'w')
#         jsonexport = {}
#         jsonexport['metadata'] = self._taxaObject.getMetadata()
#         jsonexport['data'] = self._taxaObject.getTaxonList()
#         outdata.write(json.dumps(jsonexport, encoding = jsonencode, 
#                                  sort_keys=True, indent=4))
#         outdata.close()
# 
# 
# class NordicMicroalgaeApi(DataSources):
#     """ Mainly used to load resource files. """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(JsonFile, self).__init__(taxaObject)
# 
#     def importTaxa(self, file = None):
#         """ """
# #        if file == None:
# #            raise UserWarning('File name is missing.')
# #        jsonencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, json-files', 'cp1252')
# #        indata = codecs.open(file, mode = 'r', encoding = jsonencode)
# #        self._taxaObject.clear()
# #        jsonimport = json.loads(indata.read(), encoding = jsonencode)
# #        self._taxaObject.getMetadata().update(jsonimport['metadata'])
# #        self._taxaObject.getTaxonList().extend(jsonimport['data'])
# #        indata.close()
# 
# 
# 
# class DyntaxaRest(DataSources):
#     """ For future use. """
#     def __init__(self, taxaObject = None):
#         """ """
#         super(DyntaxaRest, self).__init__(taxaObject)
# 
# #    def importTaxa(self, url = None):
# #        """ TODO: """
#         
# 
# class DyntaxaSoap(DataSources):
#     """ For future use. """
#     def __init__(self, taxaObject = None):
#         """ """
#         # Initialize parent.
#         super(DyntaxaSoap, self).__init__(taxaObject)
# 
# #    def importTaxa(self, url = None):
# #        """ TODO: """
#         

