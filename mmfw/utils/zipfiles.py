#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

