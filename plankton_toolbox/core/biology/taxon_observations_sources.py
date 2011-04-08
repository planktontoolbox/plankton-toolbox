#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

"""


#    new Ajax.Request('shark_php.php?action=get_sample_table', {
#        method: 'post',
#
#{"bounds": "", 
#"year_from": "2007", 
#"year_to": "2008", 
#"month": "06", 
#"datatype": "Phytoplankton", 
#"parameter": "COUNTNR", 
#"station_name": "sl%C3%A4gg%C3%B6", 
#"station_name_option": "station_list", 
#"taxon_name": "Dinophyceae%20", 
#"taxon_name_option": 
#"class", "project_code": "", 
#"orderer": "", 
#"deliverer": "", 
#"sample_table_view": 
#"sample_col_bio", 
#"limit": "2000", 
#"headerlang": "sv"}

#import urllib
#
#url = 'http://test.mellifica.org/sharkweb/shark_php.php'
#params = urllib.urlencode({
#    "action":"get_sample_table", 
#    "year_to": "2008", 
#    "month": "06", 
#    "datatype": "Phytoplankton", 
#    "parameter": "COUNTNR", 
#    "taxon_name": "Dinophyceae", 
#    "taxon_name_option": "class", 
##    "station_name": "sl%C3%A4gg%C3%B6", # OK
#    "station_name": "släggö", # OK
#    "station_name_option": "station_list", 
#    "limit": "2000", 
#    "headerlang": "sv"})
#    
#f = urllib.urlopen(url, params)
#out = open('result.txt', 'w')
#for line in f.readlines():
#    print(line)
#    out.write(line)
#f.close()
#out.close()
