#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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


TODO: Not used in current version. Should be rewritten and integrated with envmonlib.


"""



import codecs
import envmonlib
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources


class PwReports(object):
    """ 
    """
    def __init__(self):
        """ """
        self._metadata = {} # Metadata for the dataset.
        
class PwReportMJ1(PwReports):
    """ 
    This report has one row for each species and one column for each sample.
    """
    def __init__(self):
        """ """
#        self._peg = None
#        self._translationFileName = None
        # Initialize parent.
        super(PwReportMJ1, self).__init__()
        
    def createReport(self, samplefiles_dict = None, reportFileName = None):
        """ 
        """
        # Check indata.
        if samplefiles_dict == None:
            raise UserWarning('Samples are missing.')
        if reportFileName == None:
            raise UserWarning('File name is missing.')
        # Load resources, if not loaded before.
        toolbox_resources.ToolboxResources().loadUnloadedResources()
        pegresource = toolbox_resources.ToolboxResources().getResourcePeg()
        dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        harmfulresource = toolbox_resources.ToolboxResources().getResourceHarmfulPlankton()
        # Prepare lookup dictionary for PW-names in the PEG resource.
        pwnametopegtaxon_dict = {}
        for species in pegresource.getTaxonList():
            pwname = species.get('Species PW', None)
            if pwname:
                pwnametopegtaxon_dict[species['Species PW']] = species
        #
        # Part 1: Create header rows with columns for sample related data.
        #
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort() # Filenames in alphabetic sort order is used to set up column order.           
        # 
        numberofcolumns = 3 + len(samplefilenames)
        header_row_1 = [unicode()] * numberofcolumns 
        header_row_2 = [unicode()] * numberofcolumns 
        header_row_3 = [unicode()] * numberofcolumns 
        header_row_4 = [unicode()] * numberofcolumns 
        header_row_1[2] = u'Station:'
        header_row_2[2] = u'Provtagningsdatum:'
        header_row_3[2] = u'Datum för analys:'
        header_row_4[2] = u'Analys utförd av:'
        # Iterate over file to create columns.
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
            header_row_1[3 + filenameindex] = pw_samplefile._sample_info.get('StatName', '')
            header_row_2[3 + filenameindex] = pw_samplefile._sample_info.get('Date', '')
            header_row_3[3 + filenameindex] = pw_samplefile._sample_info.get('Counted on', '')
            header_row_4[3 + filenameindex] = pw_samplefile._sample_info.get('Counted by', '')
        #
        # Part 2: Iterate over all rows in all samples. Create a dictionary with 
        #         species as keys and lists of abundances for each sample.
        #         Example: "Incertae sedis": [1234.5, 1234.5, 1234.5, 1234.5]
        species_sample_dict = {}
        # Iterate over sample files.
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort()           
        for filenameindex, samplefilename in enumerate(samplefilenames):
            pw_samplefile = samplefiles_dict[samplefilename]
            # Iterate over the data rows
            for pw_datarow in pw_samplefile._rows:
                # Species name
                pw_speciesname = pw_datarow[0]
                # Abundance.     
                coeff = pw_datarow[5].replace(',', '.')
                units = pw_datarow[4].replace(',', '.')        
                abundance = unicode(float(coeff) * float(units)).replace('.', ',')
                #         
                if species_sample_dict.has_key(pw_speciesname):
                    species_sample_dict[pw_speciesname][filenameindex] = abundance
                else:
                    species_sample_dict[pw_speciesname] = [unicode()] * len(samplefilenames)
                    species_sample_dict[pw_speciesname][filenameindex] = abundance
        #
        # Part 3: Create the species rows in the report.        
        #
        species_rows = []
        # Iterate over species in the dictionary.
        for pw_species in species_sample_dict.keys():
            # Get PEG item.
            speciesname = 'PW-name: ' + pw_species # Only used if PEG item is missing.
            pegtaxon = pwnametopegtaxon_dict.get(pw_species, None)
            taxonomicclass = ''
            if pegtaxon:
                speciesname = pegtaxon.get('Species', '-') # Only used if Dyntaxa item is missing.
                # Get 'taxonomic class' from Dyntaxa.
                dyntaxataxon = dyntaxaresource.getTaxonById(pegtaxon.get('Dyntaxa id', '--'))
                if dyntaxataxon:
                    speciesname = dyntaxataxon.get('Scientific name', '---')
                    # Iterate upwards until taxonomic class level is reached.
                    while dyntaxataxon and (taxonomicclass == ''):
                        if dyntaxataxon.get('Taxon type', '') == 'Class':
                            taxonomicclass = dyntaxataxon.get('Scientific name', '----') 
                        parentid = dyntaxataxon.get('Parent id', None)
                        dyntaxataxon = dyntaxaresource.getTaxonById(parentid)
                if taxonomicclass == '': 
                    taxonomicclass = 'PEG: ' + pegtaxon.get('Class', '') # Only used if Dyntaxa item is missing.
            # Put the row together.
            row = [unicode()] * numberofcolumns
            row[0] = taxonomicclass
            row[1] = '' # Pot. harmful. TODO: Read from IOC resource.
            row[2] = speciesname
            for index, abund in enumerate(species_sample_dict[pw_species]):
                row[3 + index] = abund
            # Add the row the report.
            species_rows.append(row)
        # Sort the outdata list before writing to file. 
        species_rows.sort(pw_report_1_sort) # Sort function defined below.
        #
        # Part 4: Put all parts together and write to file.
        #
        out = None
        try:
            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
            out = codecs.open(reportFileName, mode = 'w', encoding = txtencode)
            separator = '\t' # Use tab as item separator.
            rowseparator = '\r\n' # Use CR/LF as row delimiter.
            # Header rows for sample part.
            out.write('\t'.join(map(unicode, header_row_1)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_2)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_3)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_4)) + rowseparator)
            # Header for species part.
            headerrow = u'Klass' + separator + \
                        u'Pot. giftig' + separator + \
                        u'Art'# Index 2.
            for filenameindex, samplefilename in enumerate(samplefilenames):
                headerrow += separator + u'Förekomst' 
            out.write(headerrow + rowseparator)
            # Species data.
            for row in species_rows:
                # Use tab as column separator and CR/LF as row delimiter.
                out.write(separator.join(map(unicode, row)) + rowseparator)
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

# Sort function for PW report.
def pw_report_1_sort(s1, s2):
    """ """
    # Class.
    # Empty strings should be at the end.
    if (s1[0] != '') and (s2[0] == ''): return -1
    if (s1[0] == '') and (s2[0] != ''): return 1
    if s1[0] < s2[0]: return -1
    if s1[0] > s2[0]: return 1
    # Scientific name
    if s1[2] < s2[2]: return -1
    if s1[2] > s2[2]: return 1
    #
    return 0 # Both are equal.


class PwReportMJ2(PwReports):
    """ 
    """
    def __init__(self):
        """ """
#        self._peg = None
#        self._translationFileName = None
        # Initialize parent.
        super(PwReportMJ2, self).__init__()
        
    def createReport(self, samplefiles_dict = None, reportFileName = None):
        """ 
        This report has one row for each species and one column for each sample.
        """
        # Check indata.
        if samplefiles_dict == None:
            raise UserWarning('Samples are missing.')
        if reportFileName == None:
            raise UserWarning('File name is missing.')
        # Load resources, if not loaded before.
        # Load resources, if not loaded before.
        toolbox_resources.ToolboxResources().loadUnloadedResources()
        pegresource = toolbox_resources.ToolboxResources().getResourcePeg()
        dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        harmfulresource = toolbox_resources.ToolboxResources().getResourceHarmfulPlankton()
        # Prepare lookup dictionary for PW-names in the PEG resource.
        pwnametopegtaxon_dict = {}
        for species in pegresource.getTaxonList():
            pwname = species.get('Species PW', None)
            if pwname:
                pwnametopegtaxon_dict[species['Species PW']] = species
        #
        # Part 1: Create header rows with columns for sample related data.
        #
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort() # Filenames used to set up column order.           
        # 
        numberofcolumns = 3 + len(samplefilenames)
        header_row_1 = [unicode()] * numberofcolumns 
        header_row_2 = [unicode()] * numberofcolumns 
        header_row_3 = [unicode()] * numberofcolumns 
        header_row_4 = [unicode()] * numberofcolumns 
        header_row_1[2] = u'Station:'
        header_row_2[2] = u'Provtagningsdatum:'
        header_row_3[2] = u'Datum för analys:'
        header_row_4[2] = u'Analys utförd av:'
        # Iterate over file to create columns.
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
            header_row_1[3 + filenameindex] = pw_samplefile._sample_info.get('StatName', '')
            header_row_2[3 + filenameindex] = pw_samplefile._sample_info.get('Date', '')
            header_row_3[3 + filenameindex] = pw_samplefile._sample_info.get('Counted on', '')
            header_row_4[3 + filenameindex] = pw_samplefile._sample_info.get('Counted by', '')
        #
        # Part 2: Iterate over all rows in all samples. Create a dictionary with 
        #         species as keys and lists of abundances for each sample.
        #         Example: "Incertae sedis": [1234.5, 1234.5, 1234.5, 1234.5]
        species_sample_dict = {}
        # Iterate over sample files.
        samplefilenames = samplefiles_dict.keys()
        samplefilenames.sort()           
        for filenameindex, samplefilename in enumerate(samplefilenames):
            pw_samplefile = samplefiles_dict[samplefilename]
            # Iterate over the data rows
            for pw_datarow in pw_samplefile._rows:
                # Species name
                pw_speciesname = pw_datarow[0]
                # Abundance.     
                coeff = pw_datarow[5].replace(',', '.')
                units = pw_datarow[4].replace(',', '.')
                try:        
                    abundance = unicode(float(coeff) * float(units)).replace('.', ',')
                except Exception, e:
                    abundance = '<error>'
                    envmonlib.Logging().error('Wrong format for coeff or units: ' + 
                                         'coeff: ' + unicode(coeff) + 
                                         'units: ' + unicode(units))
                #         
                if species_sample_dict.has_key(pw_speciesname):
                    species_sample_dict[pw_speciesname][filenameindex] = abundance
                else:
                    species_sample_dict[pw_speciesname] = [unicode()] * len(samplefilenames)
                    species_sample_dict[pw_speciesname][filenameindex] = abundance
        #
        # Part 3: Create the species rows in the report.        
        #
        species_rows = []
        # Iterate over species in the dictionary.
        for pw_species in species_sample_dict.keys():
            # Get PEG item.
            speciesname = 'PW-name: ' + pw_species # Only used if PEG item is missing.
            pegtaxon = pwnametopegtaxon_dict.get(pw_species, None)
            taxonomicclass = ''
            if pegtaxon:
                speciesname = pegtaxon.get('Species', '-') # Only used if Dyntaxa item is missing.
                # Get 'taxonomic class' from Dyntaxa.
                dyntaxataxon = dyntaxaresource.getTaxonById(pegtaxon.get('Dyntaxa id', '--'))
                if dyntaxataxon:
                    speciesname = dyntaxataxon.get('Scientific name', '---')
                    # Iterate upwards until taxonomic class level is reached.
                    while dyntaxataxon and (taxonomicclass == ''):
                        if dyntaxataxon.get('Taxon type', '') == 'Class':
                            taxonomicclass = dyntaxataxon.get('Scientific name', '----') 
                        parentid = dyntaxataxon.get('Parent id', None)
                        dyntaxataxon = dyntaxaresource.getTaxonById(parentid)
                if taxonomicclass == '': 
                    taxonomicclass = 'PEG: ' + pegtaxon.get('Class', '') # Only used if Dyntaxa item is missing.
            # Put the row together.
            row = [unicode()] * numberofcolumns
            row[0] = taxonomicclass
            row[1] = '' # Pot. harmful. TODO: Read from IOC resource.
            row[2] = speciesname
            for index, abund in enumerate(species_sample_dict[pw_species]):
                row[3 + index] = abund
            # Add the row the report.
            species_rows.append(row)
        # Sort the outdata list before writing to file. 
        species_rows.sort(pw_report_2_sort) # Sort function defined below.
        #
        # Part 4: Put all parts together and write to file.
        #
        out = None
        try:
            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
            out = codecs.open(reportFileName, mode = 'w', encoding = txtencode)
            separator = '\t' # Use tab as item separator.
            rowseparator = '\r\n' # Use CR/LF as row delimiter.
            # Header rows for sample part.
            out.write('\t'.join(map(unicode, header_row_1)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_2)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_3)) + rowseparator)
            out.write('\t'.join(map(unicode, header_row_4)) + rowseparator)
            # Header for species part.
            headerrow = u'Klass' + separator + \
                        u'Pot. giftig' + separator + \
                        u'Art'# Index 2.
            for filenameindex, samplefilename in enumerate(samplefilenames):
                headerrow += separator + u'Förekomst' 
            out.write(headerrow + rowseparator)
            # Species data.
            for row in species_rows:
                # Use tab as column separator and CR/LF as row delimiter.
                out.write(separator.join(map(unicode, row)) + rowseparator)
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

# Sort function for PW report.
def pw_report_2_sort(s1, s2):
    """ """
    # Class.
    if s1[0] < s2[0]: return -1
    if s1[0] > s2[0]: return 1
    # Scientific name
    if s1[2] < s2[2]: return -1
    if s1[2] > s2[2]: return 1
    #
    return 0 # Both are equal.


class PwReportATS1(PwReports):
    """ 
    """
    def __init__(self):
        """ """
#        self._peg = None
#        self._translationFileName = None
        # Initialize parent.
        super(PwReportATS1, self).__init__()
        
    def createReport(self, samplefiles_dict = None, reportFileName = None):
        """ """
        # Check indata.
        if samplefiles_dict == None:
            raise UserWarning('Samples are missing.')
        if reportFileName == None:
            raise UserWarning('File name is missing.')
        # Load resources, if not loaded before.
        # Load resources, if not loaded before.
        toolbox_resources.ToolboxResources().loadUnloadedResources()
        pegresource = toolbox_resources.ToolboxResources().getResourcePeg()
        dyntaxaresource = toolbox_resources.ToolboxResources().getResourceDyntaxa()
        harmfulresource = toolbox_resources.ToolboxResources().getResourceHarmfulPlankton()
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
            for pw_datarow in pw_samplefile._rows:
                # Keywords in the PW sample data rows:
                #    'Species', 'A/H', 'Size', 'Descr', 'Units', 
                #    'Coeff', 'Units/l', 'ww mg/m3', '\xb5gC/m3']
                #
                # Clear one row.
                out_row = [unicode()]*15 # 15 columns.
                #
                out_row[0] = pw_samplefile._sample_info.get('StatName', '') # To column: Station        
                out_row[1] = pw_samplefile._sample_info.get('Date', '') # To column: Date         
                out_row[2] = pw_samplefile._sample_info.get('Counted on', '') # To column: Analysis date         
                out_row[3] = pw_samplefile._sample_info.get('Min. Depth', '') # To column: Min depth m         
                out_row[4] = pw_samplefile._sample_info.get('Max. Depth', '') # To column: Max depth m                    
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
                if pegtaxon: out_row[10] = pegtaxon.get('Species PW SFLAG', '') # SFLAG   
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
                        envmonlib.Logging().error('Biovolume mm3/L: ' + unicode(e))
                # Add the row the report.
                out_rows.append(out_row)
        # Sort the outdata list before writing to file. 
        
        # Sort.
        out_rows.sort(pw_report_3_sort) # Sort function defined below.

        # Write to file.
        out = None
        try:
            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
            out = codecs.open(reportFileName, mode = 'w', encoding = txtencode)
            separator = '\t' # Use tab as item separator.
            #
            out.write(  u'Station' + separator + # Index 0.
                        u'Date' + separator + # Index 1.
                        u'Analysis date' + separator + # Index 2.
                        u'Min depth m' + separator + # Index 3.
                        u'Max depth m' + separator + # Index 4.
                        u'Order' + separator + # Index 5.
                        u'Trophy' + separator + # Index 6.
                        u'Pot Harmful' + separator + # Index 7.
                        u'Author' + separator + # Index 8.
                        u'Species' + separator + # Index 9.
                        u'SFLAG (sp., spp., cf., group, complex, cyst)' + separator + # Index 10.
                        u'Size class No' + separator + # Index 11.
#                        'Cells/L, RED= 100-um pieces/L' + separator + # Index 12.
                        u'Cells/L' + separator + # Index 12.
                        u'100-um pieces/L' + separator + # Index 13.
                        u'Biovolume mm3/L' + separator + # Index 14.
                        u'\r\n'
                    )
            
            for row in out_rows:
                # Use tab as column separator and CR/LF as row delimiter.
                out.write('\t'.join(map(unicode, row)) + '\r\n')
        except (IOError, OSError):
            raise
        finally:
            if out: out.close()

# Sort function for PW report.
def pw_report_3_sort(s1, s2):
    """ """
    # Station.
    if s1[0] < s2[0]: return -1
    if s1[0] > s2[0]: return 1
    # Date
    if s1[1] < s2[1]: return -1
    if s1[1] > s2[1]: return 1
    # Scientific name.
    # Empty strings should be at the end.
    if (s1[9] != '') and (s2[9] == ''): return -1
    if (s1[9] == '') and (s2[9] != ''): return 1
    if s1[9] < s2[9]: return -1
    if s1[9] > s2[9]: return 1
    # Size class No.
    if s1[11] < s2[11]: return -1
    if s1[11] > s2[11]: return 1
    #
    return 0 # Both are equal.
        
        
