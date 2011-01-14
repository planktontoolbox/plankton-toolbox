#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
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

import codecs
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources


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
#        self.__peg = None
#        self.__translationFileName = None
        # Initialize parent.
        super(PwReportMJ1, self).__init__()
        
    def createReport(self, samplefiles_dict = None, reportFileName = None, encode = 'utf-8'):
        """ """
        # Check indata.
        if samplefiles_dict == None:
            raise UserWarning('Samples are missing.')
        if reportFileName == None:
            raise UserWarning('File name is missing.')
        # Load resources, of not loaded before.
        if not toolbox_resources.ToolboxResources().isResourcePegLoaded():
            toolbox_resources.ToolboxResources().loadResourcePeg()
        pegresource = toolbox_resources.ToolboxResources().getResourcePeg()
        if not toolbox_resources.ToolboxResources().isResourceDyntaxaLoaded():
            toolbox_resources.ToolboxResources().loadResourceDyntaxa()
        dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        if not toolbox_resources.ToolboxResources().isResourceIocLoaded():
            toolbox_resources.ToolboxResources().loadResourceIoc()
        iocresource = toolbox_resources.ToolboxResources().getResourceIoc()
        # Prepare lookup dictionary for PW-names in the PEG resource.
        pwnametopegtaxon_dict = {}
        for species in pegresource.getTaxonList():
            pwname = species.get('Species PW', None)
            if pwname:
                pwnametopegtaxon_dict[species['Species PW']] = species
                
        # Create dictionary. Key = species and value = list .
        # For each station abundance is stored.
        species_stations_dict = {}
        # Iterate over sample files.
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort()           
        for filenameindex, samplefilename in enumerate(samplefilenames):
            pw_samplefile = samplefiles_dict[samplefilename]
            # Iterate over the data rows
            for pw_datarow in pw_samplefile._data['rows']:
                # Species name
                pw_species = pw_datarow[0]
                # Abundance.     
                coeff = pw_datarow[5].replace(',', '.')
                units = pw_datarow[4].replace(',', '.')        
                abundance = unicode(float(coeff) * float(units)).replace('.', ',')
                #         
                if species_stations_dict.has_key(pw_species):
                    species_stations_dict[pw_species][filenameindex] = abundance
                else:
                    species_stations_dict[pw_species] = [unicode()] * len(samplefilenames)
                    species_stations_dict[pw_species][filenameindex] = abundance
                
        # === Second iteration. ===
        numberofcolumns = 3 + len(samplefilenames)
        row_1 = [unicode()] * numberofcolumns 
        row_2 = [unicode()] * numberofcolumns 
        row_3 = [unicode()] * numberofcolumns 
        row_4 = [unicode()] * numberofcolumns 
        #
        for filenameindex, samplefilename in enumerate(samplefilenames):
            # Keywords in the PW sample dictionary: 
            #    'Sample Id', 'Counted on', 'Chamber diam.', 
            #    'Sampler', 'Latitude', 'StatName', 'Sample by', 'Date', 
            #    'Sedim. time (hr)', 'No. Depths', 'Counted by', 
            #    'Max. Depth', 'Longitude', 'Project', 'Depth', 
            #    'Min. Depth', 'Time', 'Mixed volume', 'StatNo', 
            #    'Comment', 'Sample size', 'Amt. preservative', 
            #    'Sedim. volume', 'Ship', 'Preservative'
            pw_samplefile = samplefiles_dict[samplefilename]
            row_1[2] = u'Station:'
            row_1[3 + filenameindex] = pw_samplefile._sample.get('StatName', '')
            row_2[2] = u'Provtagningsdatum:'
            row_2[3 + filenameindex] = pw_samplefile._sample.get('Date', '')
            row_3[2] = u'Datum för analys:'
            row_3[3 + filenameindex] = pw_samplefile._sample.get('Counted on', '')
            row_4[2] = u'Analys utförd av:'
            row_4[3 + filenameindex] = pw_samplefile._sample.get('Counted by', '')
                



        # Create list of rows.
        out_rows = []
        #
        for pw_species in species_stations_dict.keys():
            #
            pegtaxon = pwnametopegtaxon_dict.get(pw_species, None)
            if pegtaxon:
                speciesname = pegtaxon.get('Species', '---')
            else:
                speciesname = 'PW-name: ' + pw_species
            #
            # Get 'taxonomic class' from Dyntaxa. Use PEG if not found in Dyntaxa.
            taxonomicclass = ''
            if pegtaxon: 
                dyntaxataxon = dyntaxaresource.getTaxonById(pegtaxon.get('Dyntaxa id', ''))
                # Iterate upwards until order level is reached.
                while dyntaxataxon and (taxonomicclass == ''):
                    if dyntaxataxon.get('Taxon type', '') == 'Class':
                        taxonomicclass = dyntaxataxon.get('Scientific name', '') 
                    parentid = dyntaxataxon.get('Parent id', None)
                    dyntaxataxon = dyntaxaresource.getTaxonById(parentid)
            # Taxonomic class.
            if taxonomicclass == '':                
                if pegtaxon: 
                    taxonomicclass = 'PEG: ' + pegtaxon.get('Order', '') # To column: Order # TODO: remove....  
            #         

            row = [unicode()] * numberofcolumns
            row[0] = taxonomicclass
            row[1] = speciesname
            for index, abund in enumerate(species_stations_dict[pw_species]):
                row[3 + index] = abund
            # Add the row the report.
            out_rows.append(row)
        # Sort the outdata list before writing to file. 
        out_rows.sort(pw_report_1_sort) # Sort function defined below.

        # Write to file.
        out = None
        try:
#            out = codecs.open(reportFileName, mode = 'w', encoding = encode)
            out = codecs.open(reportFileName, mode = 'w', encoding = 'iso-8859-1')
            separator = '\t' # Use tab as item separator.
            #
            # Use tab as column separator and CR/LF as row delimiter.
            out.write('\t'.join(map(unicode, row_1)) + '\r\n')
            out.write('\t'.join(map(unicode, row_2)) + '\r\n')
            out.write('\t'.join(map(unicode, row_3)) + '\r\n')
            out.write('\t'.join(map(unicode, row_4)) + '\r\n')
            
            out.write( 'Station' + separator + # Index 0.
                        'Date' + separator + # Index 1.
                        'Analysis date' + separator + # Index 2.
                        'Min depth m' + separator + # Index 3.
#                        'Max depth m' + separator + # Index 4.
#                        'Order' + separator + # Index 5.
#                        'Trophy' + separator + # Index 6.
#                        'Pot Harmful' + separator + # Index 7.
#                        'Author' + separator + # Index 8.
#                        'Species' + separator + # Index 9.
#                        'SFLAG (sp., spp., cf., group, complex, cyst)' + separator + # Index 10.
#                        'Size class No' + separator + # Index 11.
##                        'Cells/L, RED= 100-um pieces/L' + separator + # Index 12.
#                        'Cells/L' + separator + # Index 12.
#                        '100-um pieces/L' + separator + # Index 13.
#                        'Biovolume mm3/L' + separator + # Index 14.
                        '\r\n'
                        )
            
            for row in out_rows:
                # Use tab as column separator and CR/LF as row delimiter.
                out.write('\t'.join(map(unicode, row)) + '\r\n')
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

# Sort function for PW report.
def pw_report_1_sort(s1, s2):
    """ """
    # Class.
    if s1[0] < s2[0]: return -1
    if s1[0] > s2[0]: return 1
    # Scientific name
    if s1[1] < s2[1]: return -1
    if s1[1] > s2[1]: return 1
    #
    return 0 # Both are equal.
        
class PwReportMJ2(PwReports):
    """ 
    """
    def __init__(self):
        """ """
#        self.__peg = None
#        self.__translationFileName = None
        # Initialize parent.
        super(PwReportMJ2, self).__init__()
        
    def createReport(self, samplefiles_dict = None, reportFileName = None, encode = 'utf-8'):
        """ """
        # Check indata.
        if samplefiles_dict == None:
            raise UserWarning('Samples are missing.')
        if reportFileName == None:
            raise UserWarning('File name is missing.')
        # Load resources, of not loaded before.
        if not toolbox_resources.ToolboxResources().isResourcePegLoaded():
            toolbox_resources.ToolboxResources().loadResourcePeg()
        pegresource = toolbox_resources.ToolboxResources().getResourcePeg()
        if not toolbox_resources.ToolboxResources().isResourceDyntaxaLoaded():
            toolbox_resources.ToolboxResources().loadResourceDyntaxa()
        dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        if not toolbox_resources.ToolboxResources().isResourceIocLoaded():
            toolbox_resources.ToolboxResources().loadResourceIoc()
        iocresource = toolbox_resources.ToolboxResources().getResourceIoc()
        # Prepare lookup dictionary for PW-names in the PEG resource.
        pwnametopegtaxon_dict = {}
        for species in pegresource.getTaxonList():
            pwname = species.get('Species PW', None)
            if pwname:
                pwnametopegtaxon_dict[species['Species PW']] = species
        # Create list of rows.
        out_rows = []
        # Iterate over sample files.
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort()           
        for samplefilename in samplefilenames:
            pw_samplefile = samplefiles_dict[samplefilename]
            # Keywords in the PW sample dictionary: 
            #    'Sample Id', 'Counted on', 'Chamber diam.', 
            #    'Sampler', 'Latitude', 'StatName', 'Sample by', 'Date', 
            #    'Sedim. time (hr)', 'No. Depths', 'Counted by', 
            #    'Max. Depth', 'Longitude', 'Project', 'Depth', 
            #    'Min. Depth', 'Time', 'Mixed volume', 'StatNo', 
            #    'Comment', 'Sample size', 'Amt. preservative', 
            #    'Sedim. volume', 'Ship', 'Preservative'
            #
            # Iterate over the data rows
            for pw_datarow in pw_samplefile._data['rows']:
                # Keywords in the PW sample data rows:
                #    'Species', 'A/H', 'Size', 'Descr', 'Units', 
                #    'Coeff', 'Units/l', 'ww mg/m3', '\xb5gC/m3']
                #
                # Clear one row.
                out_row = [unicode()]*15 # 15 columns.
                #
                out_row[0] = pw_samplefile._sample.get('StatName', '') # To column: Station        
                out_row[1] = pw_samplefile._sample.get('Date', '') # To column: Date         
                out_row[2] = pw_samplefile._sample.get('Counted on', '') # To column: Analysis date         
                out_row[3] = pw_samplefile._sample.get('Min. Depth', '') # To column: Min depth m         
                out_row[4] = pw_samplefile._sample.get('Max. Depth', '') # To column: Max depth m                    
                # Look up species and size in peg.
                pw_species = pw_datarow[0]
                pw_size = pw_datarow[2]
                
                
###                pw_size = 1
                
                
                # Find the corresponding sizeclass in PEG.
                pegtaxon = pwnametopegtaxon_dict.get(pw_species, None)
                pegsizeclass = None
                order = ''
                if pegtaxon:
                    # Find the corresponding sizeclass in PEG.
                    for sizeclass in pegtaxon['Size classes']:
                        sizeclasspw = sizeclass.get('Size class PW')
                        if sizeclasspw and (pw_size != ''):
                            if sizeclass['Size class PW'] == int(pw_size):
                                pegsizeclass = sizeclass
                    # Get 'taxonomic order' from Dyntaxa. Use PEG if not found in Dyntaxa. 
                    dyntaxataxon = dyntaxaresource.getTaxonById(pegtaxon.get('Dyntaxa id', ''))
                    # Iterate upwards until order level is reached.
                    while dyntaxataxon and (order == ''):
                        if dyntaxataxon.get('Taxon type', '') == 'Order':
                            order = dyntaxataxon.get('Scientific name', '') 
                        parentid = dyntaxataxon.get('Parent id', None)
                        dyntaxataxon = dyntaxaresource.getTaxonById(parentid)
                # Taxonomic order.
                if order == '':                
                    if pegtaxon: 
                        out_row[5] = 'PEG: ' + pegtaxon.get('Order', '') # To column: Order # TODO: remove....  
                else:
                    out_row[5] = order # To column: Order
                #         
                if pegsizeclass: out_row[6] =  pegsizeclass.get('Trophy', '') # To column: Trophy 
                # Get harmfulness from IOC.       
                if pegtaxon: out_row[7] = '' # Pot harmful. TODO:...         
                if pegtaxon: out_row[8] = pegtaxon.get('Author', '')  # To column: Author        
                if pegtaxon: out_row[9] = pegtaxon.get('Species', '') # To column: Species
                if out_row[9] == '': 
                    out_row[9] = 'PW-name: ' + pw_species # Use PW name if not found in PEG.         
                if pegtaxon: out_row[10] = '' # SFLAG   
                #     
                if pegsizeclass: out_row[11] = str(pegsizeclass.get('Size class', '')) # To column: Size class No
                coeff = pw_datarow[5].replace(',', '.')
                units = pw_datarow[4].replace(',', '.')        
                out_row[12] = str(float(coeff) * float(units)).replace('.', ',') # To column: Cells/L        
                if pegsizeclass: out_row[13] = pegsizeclass.get('', '') # To column: 100-um pieces/L
                biovolume = 0.0
                if pegsizeclass:
                    biovolume = pegsizeclass.get('Calculated volume, um3', '')
                    try:         
                        if pegsizeclass: out_row[14] = str(biovolume * float(coeff) * float(units) / 1000000.0).replace('.', ',') # To column: Biovolume mm3/L        
                    except Exception, e:
                        out_row[14] = '<error>'
                        utils.Logger().error('Biovolume mm3/L: ' + unicode(e))
                # Add the row the report.
                out_rows.append(out_row)
        # Sort the outdata list before writing to file. 
        
        # Sort.
        out_rows.sort(pw_report_2_sort) # Sort function defined below.

        # Write to file.
        out = None
        try:
#            out = codecs.open(reportFileName, mode = 'w', encoding = encode)
            out = codecs.open(reportFileName, mode = 'w', encoding = 'iso-8859-1')
            separator = '\t' # Use tab as item separator.
            #
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
                        )
            
            for row in out_rows:
                # Use tab as column separator and CR/LF as row delimiter.
                out.write('\t'.join(map(unicode, row)) + '\r\n')
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

# Sort function for PW report.
def pw_report_2_sort(s1, s2):
    """ """
    # Station.
    if s1[0] < s2[0]: return -1
    if s1[0] > s2[0]: return 1
    # Date
    if s1[1] < s2[1]: return -1
    if s1[1] > s2[1]: return 1
    # Scientific name.
    if s1[9] < s2[9]: return -1
    if s1[9] > s2[9]: return 1
    # Size class No.
    if s1[11] < s2[11]: return -1
    if s1[11] > s2[11]: return 1
    #
    return 0 # Both are equal.
        
        
