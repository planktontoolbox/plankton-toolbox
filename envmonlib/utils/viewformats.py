#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

# import envmonlib
import toolbox_utils
import toolbox_core

@toolbox_utils.singleton
class ViewFormats(object):
    """
    Utility class for formatting field content for viewing.
    """
    def __init__(self):
        """ """
        
    def cleanup(self, value, fieldtype):
        """  Formats are Text, Date, Time, Datetime, Integer and Float. """
        #
        if not value:
            return ''
        #
        viewformat = None
        if ':' in fieldtype:
            formatparts = fieldtype.split(':')
            fieldtype = formatparts[0]
            viewformat = formatparts[1] if len(formatparts) > 1 else None
        #
        value = value.trim()
        #
        if fieldtype == 'Text':
            return value 
        #
        elif fieldtype == 'Date':
            try:
                return value
            except:
                toolbox_utils.Logging().warning('Failed to parse integer value: ')
            return ''
        #
        elif fieldtype == 'Time':
            try:
                return value
            except:
                toolbox_utils.Logging().warning('Failed to parse integer value: ')
            return ''
        #
        elif fieldtype == 'Datetime':
            try:
                return value
            except:
                toolbox_utils.Logging().warning('Failed to parse integer value: ')
            return ''
        #
        elif fieldtype == 'Integer':
            try:
                value = value.replace(' ', '').replace(',', '.')
                return unicode(int(round(value)))
            except:
                toolbox_utils.Logging().warning('Failed to parse integer value: ')
            return ''
        #
        elif fieldtype == 'Float':
            try:
                cleanedvalue = value.replace(' ', '').replace(',', '.')
                return unicode(float(cleanedvalue))
            except:
                toolbox_utils.Logging().warning('Failed to parse float value: ')
            return ''
        #
        else:
            toolbox_utils.Logging().warning('Invalid import format: ' + fieldtype)
            return value



