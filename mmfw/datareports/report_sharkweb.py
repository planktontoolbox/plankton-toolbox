#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Moray
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

#import plankton_reports.core.resources.taxa as taxa
#import plankton_reports.core.resources.taxa_phytowin as taxa_phytowin

#class ReportToSharkweb(object):
#    """ """
#    def __init__(self):
#        """ """
#        # Initialize parent.
#        super(ReportSharkweb, self).__init__()
#        #
#        self._header_items = [
#            u'MYEAR', # 0
#            u'PROJ', # 1
#            u'PROJ_NAME', # 2
#            u'ORDERER', # 3
#            u'SDATE', # 4
#            u'LATIT', # 5
#            u'LONGI', # 6
#            u'POSYS', # 7
#            u'STATN', # 8
#            u'WADEP', # 9
#            u'SHIPC', # 10
#            u'STNNO', # 11
#            u'COMNT_VISIT', # 12
#            u'SMPNO', # 13
#            u'MNDEP', # 14
#            u'MXDEP', # 15
#            u'SLABO', # 16
#            u'SMTYP', # 17
#            u'SMVOL', # 18
#            u'METFP', # 19
#            u'COMNT_SAMP', # 20
#            u'LATNM', # 21
#            u'SFLAG', # 22
#            u'TRPHY', # 23
#            u'COUNTNR', # 24
#            u'COEFF', # 25
#            u'SIZCL', # 26
#            u'SIZRF', # 27
#            u'QFLAG', # 28
#            u'TAXNM', # 29
#            u'SDVOL', # 30
#            u'SDTIM', # 31
#            u'MAGNI,' # 32
#            u'ALABO', # 33
#            u'METDC', # 34
#            u'COMNT_VAR' # 35          
#            ]
#        
#    def createReport(self, datasets, report_table,
#                     show_debug_info = False, 
#                     aggregate_rows = False):
#        """
#        Note:
#        - Datasets must be of the format used in the modules dataset_tree and datasets_tree. 
#        - The report_table object must contain self._header = [] and self._rows = [].
#        """
#        # Check indata.
#        if datasets == None:
#            raise UserWarning('Datasets are missing.')
#        if report_table == None:
#            raise UserWarning('Result table is missing.')
#        # Load Phytowin species translate list.
#        try:
#            taxa_phytowin.TaxaPhytowin()
#        except:
#            raise UserWarning('Failed when loading Phytowin translation list.')
#        # Set header.
#        report_table.setHeader(self._header_items)
#        # Iterate through datasets.
#        report_rows = [] # Local copy before sorting.
#        rowdict = {}
#        
#        # Add default values.
#        
#        
#        
#        
#        
#        for datasetnode in datasets:
#            #
####            rowdict[u'MYEAR'] = node.getData(u'')
#            rowdict[u'PROJ'] = datasetnode.getData(u'Project') # ???
#            rowdict[u'PROJ_NAME'] = datasetnode.getData(u'Project') # ???
####            rowdict[u'ORDERER'] = node.getData(u'')
#            rowdict[u'SMPNO'] = datasetnode.getData(u'Sample id')
#            #
#            visitnode = datasetnode.getChildren()[0] # Only one child.
#            #
#            rowdict[u'SDATE'] = visitnode.getData(u'Date')
#            rowdict[u'LATIT'] = visitnode.getData(u'Latitude')
#            rowdict[u'LONGI'] = visitnode.getData(u'Longitude')
####            rowdict[u'POSYS'] = node.getData(u'')
#            rowdict[u'STATN'] = visitnode.getData(u'Stat name')
#            rowdict[u'WADEP'] = visitnode.getData(u'Depth')
#            rowdict[u'SHIPC'] = visitnode.getData(u'Ship')
#            rowdict[u'STNNO'] = visitnode.getData(u'Stat no')
####            rowdict[u'COMNT_VISIT'] = node.getData(u'')
#            
####            rowdict[u'SLABO'] = node.getData(u'')
####            rowdict[u'SMTYP'] = node.getData(u'')
####            rowdict[u'SMVOL'] = node.getData(u'')
####            rowdict[u'METFP'] = node.getData(u'')
####            rowdict[u'COMNT_SAMP'] = node.getData(u'')         
#            
#            
#            #
#            samplenode = visitnode.getChildren()[0] # Only one child.
#            rowdict[u'MNDEP'] = samplenode.getData(u'Min. depth')
#            rowdict[u'MXDEP'] = samplenode.getData(u'Max. depth')
#            rowdict[u'TAXNM'] = samplenode.getData(u'Counted by')
#            rowdict[u'SDVOL'] = samplenode.getData(u'Sedim. volume')
#            rowdict[u'SDTIM'] = samplenode.getData(u'Sedim. time (hr)')
#            #
#            for variablenode in samplenode.getChildren():
#                # Species
#                phytowinname = variablenode.getData('Species')
#                # Remove 'cf.'
#                if u'cf.' in phytowinname:  
#                    parts = phytowinname.split(u' ')
#                    speciesname = u''
#                    for part in parts:
#                        if part not in [u'cf.']:
#                            speciesname += part + u' '
#                    phytowinname = speciesname.strip()
#                
#                phytowinsize = variablenode.getData('Size')
#                # Phytowin names and sizeclasses may differ from PEG. SFLAG is also handled.
#                pegname, pegsize, sflag = taxa_phytowin.TaxaPhytowin().convertFromPhytowinToPeg(phytowinname, phytowinsize)
#                # Check if 'cf.' was included in name. Add to Sflag.
#                if u'cf.' in variablenode.getData('Species'):
#                    if sflag:
#                        sflag = 'CF. ' + sflag
#                    else:
#                        sflag = 'CF.'
#                # 
#                taxonname = taxa.Taxa().getTaxonValue(u'Scientific name', pegname)
#                taxonclass = taxa.Taxa().getTaxonValue(u'Class', pegname)
#                author = taxa.Taxa().getTaxonValue(u'Author', pegname)
#                harmful = taxa.Taxa().getTaxonValue(u'Harmful', pegname)
#                trophy = taxa.Taxa().getSizeclassValue(u'Trophy', pegname, pegsize)
#                # If trophy not available for this sizeclass, get it from taxon.
#                trophy = taxa.Taxa().getTaxonValue(u'Trophy', pegname)
#                #
#                countedunits = variablenode.getData('Units')
#                coeff = variablenode.getData('Coeff')
#                volume = taxa.Taxa().getSizeclassValue(u'Calculated volume, µm3', pegname, pegsize)
#                carbon = taxa.Taxa().getSizeclassValue(u'Calculated Carbon pg/counting unit', pegname, pegsize)
#                #
#                
#### "Species","A/H","Size","Descr","Units","Coeff","Units/l","ww mg/m3","µgC/m3"                       
#                rowdict[u'LATNM'] = taxonname
#                rowdict[u'SFLAG'] = sflag
#                rowdict[u'TRPHY'] = trophy
#                rowdict[u'COUNTNR'] = variablenode.getData(u'Units')
#                rowdict[u'COEFF'] = variablenode.getData(u'Coeff')
#                rowdict[u'SIZCL'] = variablenode.getData(u'Size')
####                rowdict[u'SIZRF'] = variablenode.getData(u'')
####                rowdict[u'QFLAG'] = variablenode.getData(u'')
####                rowdict[u'MAGNI'] = variablenode.getData(u'')
####                rowdict[u'ALABO'] = variablenode.getData(u'')
####                rowdict[u'METDC'] = variablenode.getData(u'')
#                rowdict[u'COMNT_VAR'] = samplenode.getData(u'Comment')
#                
#                # Create row by using order in header row.
#                report_row = []
#                for item in self._header_items:
#                    report_row.append(rowdict[item]) 
#                
#                
#                
#                
#                #
#                report_rows.append(report_row[:]) # Clone
#        # Sort the rows in the report.
##        report_rows.sort(report_conc_table_sort)
##        # Aggregate values. Same species but different size classes will be aggregated.
##        if aggregate_rows:
##            oldrow = None
##            for row in report_rows:
##                if oldrow:
##                    if oldrow[0:8] == row[0:8]:
##                        if row[11] and oldrow[11]:
##                            row[11] = unicode(int(row[11]) + int(oldrow[11]))
##                        if row[12] and oldrow[12]:
##                            row[12] = unicode(float(row[12].replace(u',', u'.')) + float(oldrow[12].replace(u',', u'.'))).replace(u'.', u',')
##                        oldrow[0] = u'REMOVE AGGREGATED' # 
##                oldrow = row
##        # Write rows to preview table.
##        for row in report_rows:
##            # Remove None items, they may otherwise appear in reports.
##            row = [item if item else u'' for item in row]
##            if row[0] != u'REMOVE AGGREGATED':
##                # Move all to the report table.
##                report_table.appendRow(row)
##
### Sort function for the result table.
##def report_conc_table_sort(s1, s2):
##    """ """
##    # Sort order: Station, date min depth, max depth and scientific name.
##    columnsortorder = [0, 1, 3, 4, 5, 6] 
##    #
##    for index in columnsortorder:
##        s1item = s1[index]
##        s2item = s2[index]
##        # Empty strings should be at the end.
##        if (s1item != '') and (s2item == ''): return -1
##        if (s1item == '') and (s2item != ''): return 1
##        if s1item < s2item: return -1
##        if s1item > s2item: return 1
##    #
##    return 0 # All are equal.
