#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import envmonlib

@envmonlib.singleton
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
            return u''
        #
        viewformat = None
        if u':' in fieldtype:
            formatparts = fieldtype.split(u':')
            fieldtype = formatparts[0]
            viewformat = formatparts[1] if len(formatparts) > 1 else None
        #
        value = value.trim()
        #
        if fieldtype == u'Text':
            return value 
        #
        elif fieldtype == u'Date':
            try:
                return value
            except:
                envmonlib.Logging().warning(u"Failed to parse integer value: ")
            return u''
        #
        elif fieldtype == u'Time':
            try:
                return value
            except:
                envmonlib.Logging().warning(u"Failed to parse integer value: ")
            return u''
        #
        elif fieldtype == u'Datetime':
            try:
                return value
            except:
                envmonlib.Logging().warning(u"Failed to parse integer value: ")
            return u''
        #
        elif fieldtype == u'Integer':
            try:
                value = value.replace(u' ', u'').replace(u',', u'.')
                return unicode(int(round(value)))
            except:
                envmonlib.Logging().warning(u"Failed to parse integer value: ")
            return u''
        #
        elif fieldtype == u'Float':
            try:
                cleanedvalue = value.replace(u' ', u'').replace(u',', u'.')
                return unicode(float(cleanedvalue))
            except:
                envmonlib.Logging().warning(u"Failed to parse float value: ")
            return u''
        #
        else:
            envmonlib.Logging().warning(u"Invalid import format: " + fieldtype)
            return value



