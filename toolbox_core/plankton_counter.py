#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import shutil

import shark_archive
import toolbox_utils

class PlanktonCounterManager(shark_archive.SharkArchive):
    """ """
    def __init__(self,
                 dataset_dir_path = 'toolbox_data/plankton_counter',
                 ):
        """ """
        self._dataset_dir_path = dataset_dir_path
        # Check if exists. Create if not.
        if (self._dataset_dir_path) and (not os.path.exists(self._dataset_dir_path)):
            try:
                os.makedirs(self._dataset_dir_path)
                print('Directories created for this path: ' + self._dataset_dir_path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + self._dataset_dir_path + '. Exception: ' + e)
        #
        self.clear() # Init.
    
    def clear(self):
        """ """
        self._current_dataset_metadata = []
        self._current_sample_metadata = []
        self._current_sample_header = []
        self._current_sample_rows = []
       
    # === Dataset ===
    def get_dataset_names(self):
        """ """
        datasetnames = []
        if (self._dataset_dir_path) and (os.path.exists(self._dataset_dir_path)):
            for dir in os.listdir(self._dataset_dir_path):
                if os.path.isdir(os.path.join(self._dataset_dir_path, dir)):
                    datasetnames.append(dir)
            return sorted(datasetnames)
        else:
            raise UserWarning('The directory toolbox_data/plankton_counter does not exists.')

    def create_dataset(self, dataset_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if (path) and (not os.path.exists(path)):
            try:
                os.makedirs(path)
                print('Directories created for this path: ' + path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + path + '. Exception: ' + e)
        else:
            raise UserWarning('Dataset already exists, create failed. Dataset name: ' + dataset_name)

    def delete_dataset(self, dataset_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if path and os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise UserWarning('Can\'t delete directory. Path: ' + path + '. Exception: ' + e)
        else:
            raise UserWarning('Dataset did not exist, delete failed. Dataset name: ' + dataset_name)

    # === Sample ===
    def get_sample_names(self, dataset_name):
        """ """
        samplenames = []
        path = os.path.join(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if (path) and (os.path.exists(path)):
            for dir in os.listdir(path):
                if os.path.isdir(os.path.join(path, dir)):
                    samplenames.append(dir)
            return sorted(samplenames)
        else:
            raise UserWarning('Dataset does not exist. Dataset name: ' + dataset_name)

    def create_sample(self, dataset_name, sample_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name, sample_name)
        # Check if exists.
        if (path) and (not os.path.exists(path)):
            try:
                os.makedirs(path)
                print('Directories created for this path: ' + path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + path + '. Exception: ' + e)
        else:
            raise UserWarning('Sample already exists, create failed. Dataset name: ' + dataset_name)

    def delete_sample(self, dataset_name, sample_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name, sample_name)
        # Check if exists.
        if path and os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise UserWarning('Can\'t delete sample. Path: ' + path + '. Exception: ' + e)
        else:
            raise UserWarning('Sample does not exist, delete failed. Dataset name: ' + dataset_name)

    def load_sample_data(self, dataset_name, sample_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name, sample_name)
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = path,
                    text_file_name = 'sample_data.txt',                 
                    )
        #
        self._current_sample_header = tablefilereader.header()
        self._current_sample_rows = tablefilereader.rows()
        print('Header: ' + unicode(self._current_sample_header))
        print('Rows:   ' + unicode(self._current_sample_rows))

    def write_sample_data(self, dataset_name, sample_name):
        """ """

    # === Metadata ===
    def load_dataset_metadata(self, dataset_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name)
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = path,
                    text_file_name = 'dataset_metadata.txt',                 
                    )
        # Merge header and rows.
        self._current_dataset_metadata = [tablefilereader.header()] + tablefilereader.rows()
        print('Dataset metadata: ' + unicode(self._current_dataset_metadata))

    def write_dataset_metadata(self, dataset_name):
        """ """

    def load_sample_metadata(self, dataset_name, sample_name):
        """ """
        path = os.path.join(self._dataset_dir_path, dataset_name, sample_name)
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = path,
                    text_file_name = 'sample_metadata.txt',                 
                    )
        # Merge header and rows.
        self._current_sample_metadata = [tablefilereader.header()] + tablefilereader.rows()
        print('Sample metadata: ' + unicode(self._current_sample_metadata))

    def write_sample_metadata(self, dataset_name):
        """ """

    # === Orderer/sampling info ===
    def load_orderer_info(self, dataset_name):
        """ """

    def load_sampling_info(self, dataset_name):
        """ """

    # === Import/Export ===
    def import_dataset(self, source_path, source_file_name, dataset_name):
        """ """

    def export_dataset(self, dataset_name, target_path, target_file_name):
        """ """

    def import_orderer_info(self, source_path, source_file_name, dataset_name):
        """ """

    def import_sampling_info(self, source_path, source_file_name, dataset_name):
        """ """


# ===== TEST =====
if __name__ == "__main__":
    """ Used during development. """
    
    planktoncountermanager = PlanktonCounterManager()
    
    datasetnames = planktoncountermanager.get_dataset_names()
    print('DEBUG: Datasets: ' + unicode(datasetnames))
    
#     try: planktoncountermanager.create_dataset('Test-4')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     datasetnames = planktoncountermanager.get_dataset_names()
#     print('DEBUG: Datasets: ' + unicode(datasetnames))
# 
#     try: planktoncountermanager.delete_dataset('Test-4')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     datasetnames = planktoncountermanager.get_dataset_names()
#     print('DEBUG: Datasets: ' + unicode(datasetnames))

#     try: planktoncountermanager.create_sample('Test-1', 'Sample-1')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     try: planktoncountermanager.create_sample('Test-1', 'Sample-2')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     try: planktoncountermanager.create_sample('Test-1', 'Sample-3')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     samplenames = planktoncountermanager.get_sample_names('Test-1')
#     print('DEBUG: Samples in ' + 'Test-1' + ': ' + unicode(samplenames))
# 
#     try: planktoncountermanager.create_sample('Test-2', 'Sample-A')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     try: planktoncountermanager.create_sample('Test-2', 'Sample-B')
#     except Exception as e: print ('Exception: ' + unicode(e))
#     try: planktoncountermanager.create_sample('Test-2', 'Sample-C')
#     except Exception as e: print ('Exception: ' + unicode(e))
    samplenames = planktoncountermanager.get_sample_names('Test-2')
    print('DEBUG: Samples in ' + 'Test-2' + ': ' + unicode(samplenames))
    
    try: planktoncountermanager.load_dataset_metadata('Test-1')
    except Exception as e: print ('Exception: ' + unicode(e))

    try: planktoncountermanager.load_sample_metadata('Test-1', 'Sample-1')
    except Exception as e: print ('Exception: ' + unicode(e))

    try: planktoncountermanager.load_sample_data('Test-1', 'Sample-1')
    except Exception as e: print ('Exception: ' + unicode(e))


