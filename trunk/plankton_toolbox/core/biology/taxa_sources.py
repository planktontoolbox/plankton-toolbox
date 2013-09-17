#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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


# #import date
# #import datetime
# from abc import abstractmethod
# import codecs
# import json
# import envmonlib
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
#         envmonlib.Logging().log("Writes taxa to: " + file)
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

