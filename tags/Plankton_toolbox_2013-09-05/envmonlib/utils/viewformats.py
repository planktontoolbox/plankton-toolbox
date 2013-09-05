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



