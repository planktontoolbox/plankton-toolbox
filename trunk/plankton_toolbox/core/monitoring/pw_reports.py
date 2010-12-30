#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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

import codecs
import plankton_toolbox.toolbox.utils as utils

class PwReports(object):
    """ 
    """
    def __init__(self):
        """ """
        self._metadata = {} # Metadata for the dataset.
        
class PwReportMJ1(PwReports):
    """ 
    """
    def __init__(self):
        """ """
        super(PwReportMJ1, self).__init__()
#        self.__peg = None
#        self.__translationFileName = None
        
    def setPeg(self, peg):
        """ """
        self.__peg = peg

    def setTaxonSizeClassTranslationFile(self, fileName):
        """ """
        self.__translationFileName = fileName

    def exportFile(self, pw_sample_dict = None, fileName = None, encoding = 'utf-8'):
        """ """
        if pw_sample_dict == None:
            raise UserWarning('Samples are missing.')
        if fileName == None:
            raise UserWarning('File name is missing.')
        
        # Load translation file between SmhiPhytoplanktonList and PEG list.  
        taxon_size_translation_dict = {}
###        translateFile = open(self.__translationFileName, 'r')
        translateFile = codecs.open(self.__translationFileName, mode = 'r', encoding = encoding)
        separator = '\t' # Tab as separator.
        for row in translateFile:
            row_list = row.split(separator)
            if len(row_list) >= 4: 
                taxon_size_translation_dict[row_list[0] + ':' + row_list[1]] = row_list[2] + ':' + row_list[3]            
        translateFile.close()

        
        out = None
        try:
            out = codecs.open(fileName, mode = 'w', encoding = encoding)
            separator = '\t' # Use tab as item separator.

            out.write( 'Station' + separator + # Index 0.
                        'Date' + separator + # Index 1.
                        'Analysis date' + separator + # Index 2.
                        'Min depth m' + separator + # Index 3.
                        'Max depth m' + separator + # Index 4.
                        'Order' + separator + # Index 5.
                        'Trophy' + separator + # Index 6.
                        'Pot Harmful' + separator + # Index 7.
                        'Author' + separator + # Index 8.
                        'Species' + separator + # Index 9.
                        'SFLAG (sp., spp., cf., group, complex, cyst)' + separator + # Index 10.
                        'Size class No' + separator + # Index 11.
#                        'Cells/L, RED= 100-um pieces/L' + separator + # Index 12.
                        'Cells/L' + separator + # Index 12.
                        '100-um pieces/L' + separator + # Index 13.
                        'Biovolume mm3/L' + separator + # Index 14.
                        '\r\n'
                        );
                        
            for pw_sample in pw_sample_dict.values():
                # Sample keys: 'Sample Id', 'Counted on', 'Chamber diam.', 
                #    'Sampler', 'Latitude', 'StatName', 'Sample by', 'Date', 
                #    'Sedim. time (hr)', 'No. Depths', 'Counted by', 
                #    'Max. Depth', 'Longitude', 'Project', 'Depth', 
                #    'Min. Depth', 'Time', 'Mixed volume', 'StatNo', 
                #    'Comment', 'Sample size', 'Amt. preservative', 
                #    'Sedim. volume', 'Ship', 'Preservative'
                for pw_datarow in pw_sample._data['rows']:
                    # Row header: ['Species', 'A/H', 'Size', 'Descr', 'Units', 
                    #     'Coeff', 'Units/l', 'ww mg/m3', '\xb5gC/m3']
                    out_columns = list('' for x in range(15))
                    out_columns[0] = pw_sample._sample.get('StatName', '') # Station        
                    out_columns[1] = pw_sample._sample.get('Date', '') # Date         
                    out_columns[2] = pw_sample._sample.get('Counted on', '') # Analysis date         
                    out_columns[3] = pw_sample._sample.get('Min. Depth', '') # Min depth m         
                    out_columns[4] = pw_sample._sample.get('Max. Depth', '') # Max depth m
                    
                    # Look up species and size in peg.
############                    pw_species_size = pw_datarow[0] + ':' + pw_datarow[2]



                    pw_species_size = pw_datarow[0] + ':' + '1' # TEST TEST TEST

                    
                    
                    peg_species, peg_size = taxon_size_translation_dict.get(pw_species_size, ':').split(':')
                    
                    pegobject = self.__peg.getTaxonByName(peg_species)
                    pegsizeclass = None
                    if pegobject:
                        for sizeclass in pegobject['Size classes']:
                            if peg_size != '':
                                if sizeclass['Size class'] == int(peg_size):
                                    pegsizeclass = sizeclass
                    
                    
                    
                             
                    if pegobject: out_columns[5] = pegobject.get('Order', '') # Order       
                    if pegobject: out_columns[6] =  pegobject.get('Thropy', '') # Trophy        
                    if pegobject: out_columns[7] = '' # Pot Harmful        
                    if pegobject: out_columns[8] = pegobject.get('Author', '')  # Author        
                    if pegobject: out_columns[9] = pegobject.get('Species', '') # Species        
                    if pegobject: out_columns[10] = '' # SFLAG   
                         
                    if pegsizeclass: out_columns[11] = str(pegsizeclass.get('Size class', '')) # Size class No
                    coeff = pw_datarow[5].replace(',', '.')
                    units = pw_datarow[4].replace(',', '.')        
                    out_columns[12] = str(float(coeff) * float(units)).replace('.', ',') # Cells/L        
                    if pegsizeclass: out_columns[13] = pegsizeclass.get('', '') # 100-um pieces/L
                    biovolume = 0.0
                    if pegsizeclass:
                        biovolume = pegsizeclass.get('Calculated volume, um3', '')
                        try:         
                            if pegsizeclass: out_columns[14] = str(biovolume * float(coeff) * float(units) / 1000000.0).replace('.', ',') # Biovolume mm3/L        
                        except Exception, e:
                            out_columns[14] = '<error>'
                            utils.Logger().error('Biovolume mm3/L: ' + unicode(e))
                        
    #                pegobject = self.peg.getTaxonByName(pw_data[sample])
    #                pegobject
    
                    out.write('\t'.join(map(unicode, out_columns)) + '\r\n')
            
                
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

