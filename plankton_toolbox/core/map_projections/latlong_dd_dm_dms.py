#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""


TODO: Should be integrated with toolbox_utils.


"""


"""
Converts latitude and longitude from/to text representation. Formats: 
- DD, Decimal degree.
- DM, Degree/minute.
- DMS, Degree/minute/second.
  
The text value parsing is implemented by use of regexp.
"""

import math
import re

def convert_lat_from_dd(value):
    """ Converts latitude from DD (Decimal degree) input format. """
    regex = re.compile(
        r"""^\s*([NS\-\+]?)\s*(\d{1,3})([\.\,]\d*)?\s*([NS]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
        if ((match.group(2) != '') and (match.group(2) != None)):
            latitude = float(match.group(2))
        if ((match.group(3) != '') and (match.group(3) != None) and (match.group(3).replace(',', '.') != '.')):
            latitude += float(match.group(3).replace(',', '.'))
        if (latitude > 90):
            latitude = None
            return latitude
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'S') or (match.group(1) == '-'))):
            latitude *= -1
        else:
            if ((match.group(4) != '') and (match.group(4) != None) and ((match.group(4) == 'S'))):
                latitude *= -1    
        return latitude
    else:
        return None     

def convert_long_from_dd(value):
    """ Converts from input format. """
##    value = value.replace(/[E]/gi, 'E') # Note: Ö=Öst for swedish users.
##    value = value.replace(/[WV]/gi, 'W') # Note: V=Väst for swedish users.
#    value = regexp.compile('/[E]/gi').sub('E', value)
#    value = regexp.compile('/[WV]/gi').sub('W', value)
    regex = re.compile(
        r"""^\s*([EW\-\+]?)\s*(\d{1,3})([\.\,]\d*)?\s*([EW]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
#        print('MATCH:')
#        print('1: ' + str(match.group(1)))
#        print('2: ' + str(match.group(2)))
#        print('3: ' + str(match.group(3)))
#        print('4: ' + str(match.group(4)))
        if ((match.group(2) != '') and (match.group(2) != None)):
            longitude = float(match.group(2))
        if ((match.group(3) != '') and (match.group(3) != None) and (match.group(3).replace(',', '.') != '.')):
            longitude += float(match.group(3).replace(',', '.'))
        if (longitude > 180):
            longitude = None
            return longitude
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'W') or (match.group(1) == '-'))):
            longitude *= -1
        else:
            if ((match.group(4) != '') and (match.group(4) != None) and ((match.group(4) == 'W'))):
                longitude *= -1    
        return longitude
    else:
        return None     

def convert_lat_from_dm(value):
    """ Converts from input format. """
##    value = value.replace(/[N]/gi, 'N')
##    value = value.replace(/[S]/gi, 'S')
#    value = regexp.compile('/[N]/gi').sub('N', value)
#    value = regexp.compile('/[S]/gi').sub('S', value)
    regex = re.compile(
        r"""^\s*([NS\-\+]?)\s*(\d{1,3})\??\s*([0-5]?[0-9])?([\.\,]\d*)?\'?\s*([NS]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
        if ((match.group(2) != '') and (match.group(2) != None)):
            latitude = float(match.group(2))
        if ((match.group(3) != '') and (match.group(3) != None)):
            latitude += float(match.group(3)) / 60
        if ((match.group(4) != '') and (match.group(4) != None) and (match.group(4).replace(',', '.') != '.')):
            latitude += float(match.group(4).replace(',', '.')) / 60
        if (latitude > 90):
            latitude = None
            return latitude
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'S') or (match.group(1) == '-'))):
            latitude *= -1
        else:
            if ((match.group(5) != '') and (match.group(5) != None) and ((match.group(5) == 'S'))):
                latitude *= -1
        return latitude
    else:
        return None     

def convert_long_from_dm(value):
    """ Converts from input format. """
##    value = value.replace(/[E]/gi, 'E')
##    value = value.replace(/[WV]/gi, 'W')
#    value = regexp.compile('/[E]/gi').sub('E', value)
#    value = regexp.compile('/[WV]/gi').sub('W', value)
    regex = re.compile(
        r"""^\s*([EW\-\+]?)\s*(\d{1,3})\??\s*([0-5]?[0-9])?([\.\,]\d*)?\'?\s*([EW]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
        if ((match.group(2) != '') and (match.group(2) != None)):
            longitude = float(match.group(2))
        if ((match.group(3) != '') and (match.group(3) != None)):
            longitude += float(match.group(3)) / 60
        if ((match.group(4) != '') and (match.group(4) != None) and (match.group(4).replace(',', '.') != '.')):
            longitude += float(match.group(4).replace(',', '.')) / 60
        if (longitude > 180):
            longitude = None
            return longitude
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'W') or (match.group(1) == '-'))):
            longitude *= -1
        else:
            if ((match.group(5) != '') and (match.group(5) != None) and ((match.group(5) == 'W'))):
                longitude *= -1
        return longitude
    else:
        return None     

def convert_lat_from_dms(value):
    """ Converts latitude from input format. """
##    value = value.replace(/[N]/gi, 'N')
##    value = value.replace(/[S]/gi, 'S')
#    value = regexp.compile('/[N]/gi').sub('N', value)
#    value = regexp.compile('/[S]/gi').sub('S', value)
    regex = re.compile(
        r"""^\s*([NS\-\+]?)\s*(\d{1,3})\??\s*([0-5]?[0-9])?\'?\s*([0-5]?[0-9])?([\.\,]\d*)?\"?\s*([NS]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
        if ((match.group(2) != '') and (match.group(2) != None)):
            latitude = float(match.group(2))
        if ((match.group(3) != '') and (match.group(3) != None)):
            latitude += float(match.group(3)) / 60
        if ((match.group(4) != '') and (match.group(4) != None)):
            latitude += float(match.group(4)) / 3600
        if ((match.group(5) != '') and (match.group(5) != None) and (match.group(5).replace(',', '.') != '.')):
            latitude += float(match.group(5).replace(',', '.')) / 3600
        if (latitude > 90):
            latitude = None
            return latitude            
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'S') or (match.group(1) == '-'))):
            latitude *= -1
        else:
            if ((match.group(6) != '') and (match.group(6) != None) and ((match.group(6) == 'S'))):
                latitude *= -1    
        return latitude
    else:
        return None     

def convert_long_from_dms(value):
    """ Converts longitude from input format. """
##    value = value.replace(/[E]/gi, 'E')
##    value = value.replace(/[WV]/gi, 'W')
#    value = regexp.compile('/[E]/gi').sub('E', value)
#    value = regexp.compile('/[WV]/gi').sub('W', value)
    regex = re.compile(
        r"""^\s*([EW\-\+]?)\s*(\d{1,3})\??\s*([0-5]?[0-9])?\'?\s*([0-5]?[0-9])?([\.\,]\d*)?\"?\s*([EW]?)\s*$""") 
    match = regex.match(value.upper())
    if match:
        if ((match.group(2) != '') and (match.group(2) != None)):
            longitude = float(match.group(2))    
        if ((match.group(3) != '') and (match.group(3) != None)):
            longitude += float(match.group(3)) / 60
        if ((match.group(4) != '') and (match.group(4) != None)):
            longitude += float(match.group(4)) / 3600
        if ((match.group(5) != '') and (match.group(5) != None) and (match.group(5).replace(',', '.') != '.')):
            longitude += float(match.group(5).replace(',', '.')) / 3600
        if (longitude > 180):
            longitude = None
            return longitude
        if ((match.group(1) != '') and (match.group(1) != None) and ((match.group(1) == 'W') or (match.group(1) == '-'))):
            longitude *= -1
        else:
            if ((match.group(6) != '') and (match.group(6) != None) and ((match.group(6) == 'W'))):
                longitude *= -1
        return longitude
    else:
        return None     

def convert_lat_to_dd(value):
    """ Converts latitude to the DD (Decimal degree) display format. """  
    if (value == None):
        return ''
    return "%09.6f" % value # Round.

def convert_long_to_dd(value):
    """ Converts longitude to the DD (Decimal degree) display format. """  
    if (value == None):
        return ''
    return "%09.6f" % value # Round.

def convert_lat_to_dm(value):
    """ Converts latitude to the DM (Degree/minute) display format. """  
    if (value == None):
        return ''
    value += 0.0000008 # Round (= 0.5 min).
    degrees = math.floor(abs(value))
    minutes = (abs(value) - degrees) * 60
    if (value >= 0):
        return "N %02d %07.4f'" % (degrees, (math.floor(minutes*10000)/10000))
    else:
        return "S %02d %07.4f'" % (degrees, (math.floor(minutes*10000)/10000)) 

def convert_long_to_dm(value):
    """ Converts longitude to the DM (Degree/minute) display format. """  
    if (value == None):
        return ''
    value += 0.0000008 # Round (= 0.5 min).
    degrees = math.floor(abs(value))
    minutes = (abs(value) - degrees) * 60
    if (value >= 0):
        return "E %02d %07.4f'" % (degrees, (math.floor(minutes*10000)/10000))
    else:
        return "W %02d %07.4f'" % (degrees, (math.floor(minutes*10000)/10000)) 

def convert_lat_to_dms(value):
    """ Converts latitude to the DMS (Degree/minute/second) display format. """  
    if (value == None):
        return ''
    value += 0.0000014 # Round (= 0.5 sec).
    degrees = math.floor(abs(value))
    minutes = math.floor((abs(value) - degrees) * 60)
    seconds = (abs(value) - degrees - minutes / 60) * 3600
    if (value >= 0):
        return "N %02d %02d' %05.2f\"" % (degrees, minutes, (math.floor(seconds*100)/100)) 
    else:
        return "S %02d %02d' %05.2f\"" % (degrees, minutes, (math.floor(seconds*100)/100)) 

def convert_long_to_dms(value):
    """ Converts longitude to the DMS (Degree/minute/second) display format. """  
    if (value == None):
        return ''
    value += 0.0000014 # Round (= 0.5 sec).
    degrees = math.floor(abs(value))
    minutes = math.floor((abs(value) - degrees) * 60)
    seconds = (abs(value) - degrees - minutes / 60) * 3600
    if (value >= 0):
        return "E %02d %02d' %05.2f\"" % (degrees, minutes, (math.floor(seconds*100)/100)) 
    else:
        return "W %02d %02d' %05.2f\"" % (degrees, minutes, (math.floor(seconds*100)/100)) 
