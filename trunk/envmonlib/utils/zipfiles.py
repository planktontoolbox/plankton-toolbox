#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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

TODO: Under development. Not used.

"""

import zipfile

class ZipFileReader(object):
    """
    This class ...  
    """
    def __init__(self, zip_file_name):
        """ """
        super(ZipFileReader, self).__init__()
        #
        self._zip = None
        if not zipfile.is_zipfile(zip_file_name):
            raise UserWarning('Selected file is not a valid zip file: ' + zip_file_name)
        #
        self._zip = zipfile.ZipFile(zip_file_name, 'r')

    def __del__(self):
        """ """
        self.close()

    def close(self):
        """ """
        if self._zip:
            self._zip.close()
        self._zip = None

    def listContent(self):
        """ """
        if self._zip:
            return self._zip.namelist()
        else:
            return {}

    def readEntryToTableDataset(self, 
                                target_dataset, 
                                zip_entry,
                                encoding = None):
        """ """
    
    
#    def openZipEntry(self, entry_name):
#        """ """
#        if self._zip:
#            return self._zip.open(entry_name, 'r')
#        else:
#            return None

    def getMetadataAsDict(self):
        """ """
        # TODO:
        return {}

class ZipFileWriter(object):
    """
    This class ...  
    """
    def __init__(self, zip_file_name):
        """ """
        super(ZipFileWriter, self).__init__()
        #

