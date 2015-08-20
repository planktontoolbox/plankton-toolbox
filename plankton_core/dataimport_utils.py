#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import string
# import toolbox_utils
# import plankton_core

class DataImportUtils(object):
    """ """
    def __init__(self):
        """ """

    def cleanup_scientific_name_cf(self, scientific_name, species_flag):
        """ """
        new_scientific_name = scientific_name
        new_species_flag = species_flag
        # Remove 'cf.'
        if ' cf. '.upper() in (' ' + new_scientific_name + ' ').upper():  
            parts = new_scientific_name.split(' ')
            parts = map(string.strip, parts) # Remove white characters.
            speciesname = ''
            for part in parts:
                if part not in ['cf.', 'CF.', 'cf', 'CF']:
                    speciesname += part + ' '
            #
            new_scientific_name = speciesname.strip()
            #
            if len(new_species_flag) > 0:
                new_species_flag = 'cf., ' + new_species_flag
            else:
                new_species_flag = 'cf.'
        #
        return new_scientific_name, new_species_flag
        
    def cleanup_scientific_name_sp(self, scientific_name, species_flag):
        """ """
        new_scientific_name = scientific_name
        new_species_flag = species_flag
        # Remove 'sp.'
        if (' sp.'.upper() in (new_scientific_name + ' ').upper()) or \
           (' sp '.upper() in (new_scientific_name + ' ').upper()):  
            parts = new_scientific_name.split(' ')
            parts = map(string.strip, parts) # Remove white characters.
            speciesname = ''
            for part in parts:
                if part not in ['sp.', 'SP.', 'sp', 'SP']:
                    speciesname += part + ' '
            #
            new_scientific_name = speciesname.strip()
            #
            if len(new_species_flag) > 0:
                new_species_flag = 'sp., ' + new_species_flag
            else:
                new_species_flag = 'sp.'
        #
        return new_scientific_name, new_species_flag
        
    def cleanup_scientific_name_spp(self, scientific_name, species_flag):
        """ """
        new_scientific_name = scientific_name
        new_species_flag = species_flag
        # Remove 'spp.'
        if (' spp.'.upper() in (new_scientific_name + ' ').upper()) or \
           (' spp '.upper() in (new_scientific_name + ' ').upper()):  
            parts = new_scientific_name.split(' ')
            parts = map(string.strip, parts) # Remove white characters.
            speciesname = ''
            for part in parts:
                if part not in ['spp.', 'SPP.', 'spp', 'SPP']:
                    speciesname += part + ' '
            #
            new_scientific_name = speciesname.strip()
            #
            if len(new_species_flag) > 0:
                new_species_flag = 'spp., ' + new_species_flag
            else:
                new_species_flag = 'spp.'
        #
        return new_scientific_name, new_species_flag
        
