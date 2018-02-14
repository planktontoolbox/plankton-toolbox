#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# import codecs
# import dateutil
# import toolbox_utils
# import plankton_core
# 
# class ImportPhytowin(plankton_core.DataImportPreparedBase):
#     """ Class for parsing Phytowin CSV files. """
#     def __init__(self):
#         """ """
#         # Initialize parent.
#         super(ImportPhytowin, self).__init__()
# 
#         # Information needed for parsing. List of lists with: 
#         #   Column 0: node level. 
#         #   Column 1: internal key. 
#         #   Column 2: view format. 
#         #   Column 3: source file column name. Multiple alternatives should be separated by '<or>'. 
#         #   Column 4: export column name. None = not used, empty string ('') = same as column 1 (internal key).
#         self._parsing_info = [
#             
#             # Metadata:
#             ['visit', 'station_name', 'text', 'StatName', ''], 
#             ['visit', 'sample_date', 'text', 'Date', ''], 
#             ['visit', 'time', 'text', 'Time', ''], 
#             ['visit', 'reported_latitude', 'text', 'Latitude', ''], 
#             ['visit', 'reported_longitude', 'text', 'Longitude', ''], 
#             ['sample', 'sample_min_depth_m', 'float', 'Min. Depth', ''], 
#             ['sample', 'sample_max_depth_m', 'float', 'Max. Depth', ''], 
#             ['visit', 'water_depth_m', 'float', 'Depth', ''], 
# 
#             # Header: "Species","A/H","Size","Descr","Units","Coeff","Units/l","ww mg/m3","µgC/m3"
#             ['variable', 'reported_scientific_name', 'text', 'Species', None], # Internal use only. 
#             ['variable', 'scientific_name', 'text', 'Species', ''], 
#             ['variable', 'species_flag_code', 'text', '', ''], 
#             ['variable', 'reported_trophic_type', 'text', 'A/H', None], # Internal use only. 
#             ['variable', 'trophic_type', 'text', '', ''], # Will be calculated later.
#             ['variable', 'reported_size_class', 'text', 'Size', None], # Internal use only. 
#             ['variable', 'size_class', 'text', 'Size', ''], 
#             ['variable', 'description', 'text', 'Descr', ''], 
#             ['variable', 'coefficient', 'text', 'Coeff', ''], 
# 
#             # Param/value/unit. (Added later from "copy parameters".)
#             ['variable', 'parameter', 'text', 'parameter', ''],
#             ['variable', 'value', 'float', 'value', ''], 
#             ['variable', 'unit', 'text', 'unit', ''], 
# 
#             # Copy parameters.
#             ['copy_parameter', '# counted:ind', 'text', 'Units'], 
#             ['copy_parameter', 'Abundance:ind/l', 'text', 'Units/l'], 
#             ['copy_parameter', 'Wet weight:mg/m3', 'text', 'ww mg/m3'], 
#             ['copy_parameter', 'Carbon content:µgC/m3', 'text', 'µgC/m3'], 
#             ['copy_parameter', 'Abundance class:abu_class', 'text', 'Abundance (scale 1 to 5)'],# NET sample.
#             
#             # More metadata:
#             ['dataset', 'sample_id', 'text', 'Sample Id', ''], 
#             ['dataset', 'project_code', 'text', 'Project', ''], 
#             ['visit', 'platform_code', 'text', 'Ship', ''], 
#             ['visit', 'station_number', 'text', 'StatNo', ''], 
#             ['variable', 'taxon_class', 'text', '', ''], # Will be calculated later.
#             ['variable', 'magnification', 'text', 'Magnification', ''], 
#             ['variable', 'counted_units', 'text', 'Units', ''], 
#             ['sample', 'number_of_depths', 'text', 'No. Depths', ''], 
#             ['sample', 'sampler_type_code', 'text', 'Sampler', ''], 
#             ['sample', 'sample_size', 'text', 'Sample size', ''], 
#             ['sample', 'sampled_by', 'text', 'Sample by', ''], 
#             ['sample', 'sample_comment', 'text', 'Comment', ''], 
#             ['variable', 'mixed_volume', 'text', 'Mixed volume', ''], 
#             ['variable', 'preservative', 'text', 'Preservative', ''], 
#             ['variable', 'sedimentation_volume', 'text', 'Sedim. volume', ''], 
#             ['variable', 'preservative_amount', 'text', 'Amt. preservative', ''], 
#             ['variable', 'sedimentation_time_h', 'text', 'Sedim. time (hr)', ''], 
#             ['variable', 'chamber_diameter', 'text', 'Chamber diam.', ''], 
#             ['variable', 'analysis_date', 'text', 'Counted on', ''], 
#             ['variable', 'analysed_by', 'text', 'Counted by', ''], 
#         ]
#         #
#         self.clear() # 
#         #
#         self._phytowin_to_peg_filename = 'plankton_toolbox_data/species/phytowin_translate_sizeclasses.xlsx'
#         try:
#             self._load_phytowin_species_and_sizes_mapping()
#         except:
#             print('Failed to load: ' + self._phytowin_to_peg_filename)
#         
# 
#     def clear(self):
#         """ """
#         self._phytowin_metadata = {}
#         self._phytowin_header = []
#         self._phytowin_rows = []
#         self._phytowin_coeff2magni_dict = {}
#         #
#         self._phytowin_sample_info = {} # Information related to sample.
#         self._phytowin_aggregated_rows = [] # Pre-calculated aggregations of data.
#         #
#         self._pythowin_peg_mapping = {}
# 
#     def read_file(self, file_name = None):
#         """ """
#         if file_name == None:
#             raise UserWarning('File name is missing.')
#         file = None
#         try:
# ###            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
#             txtencode = 'cp1252'
#             file = codecs.open(file_name, mode = 'r', encoding = txtencode)
#             
#             # Read data header. Same header used for data and aggregated data.
#             
#             separator = ',' # Use ',' as default item separator.
#             first_row = file.readline()
#             if ';' in first_row:
#                 separator = ';' # Use ';' as item separator.
#                 
#             self._phytowin_header = []
#             for headeritem in first_row.strip(separator).split(separator):
#                 item = headeritem.strip().strip('"').strip()
#                 self._phytowin_header.append(item)
#                 
#             # Empty line.
#             file.readline().strip(separator)
#             
#             # Read data rows. Continue until empty line occurs.
#             self._phytowin_rows = []
#             row = file.readline().strip(separator)
#             while len(row.replace(separator, '').strip()) > 0:
#                 rowitems = []
#                 for item in row.split(separator):
#                     rowitems.append(item.strip().strip('"').strip())
#                 self._phytowin_rows.append(rowitems) 
#                 row = file.readline().strip(separator)
#             
#             # Read aggregated data rows. Continue until empty line occurs.
#             self._phytowin_aggregated_rows = []
#             row = file.readline().strip(separator)
#             while len(row.replace(separator, '').strip()) > 0:
#                 rowitems = []
#                 for item in row.split(separator):
#                     rowitems.append(item.strip().strip('"').strip())
#                 self._phytowin_aggregated_rows.append(rowitems) 
#                 row = file.readline().strip(separator)
#                          
#             if self._phytowin_header[1] not in ['Abundance (scale 1 to 5)']:
#                 # Read total counted.
#                 row = file.readline().strip(separator) # Not used.
#                 row = file.readline().strip(separator) # Empty.
#                 
#                 # Read total counted.
#                 row = file.readline().strip(separator) # Not used.
#                 row = file.readline().strip(separator) # Empty.
#             
#             # Read chamber and magnification info.
#             # Put result in self._phytowin_coeff2magni_dict for later use.
#             row = file.readline().strip(separator)
#             while len(row.replace(separator, '').strip()) > 0:
#                 rowitems = []
#                 for item in row.split(separator):
#                     rowitems.append(item.strip().strip('"').strip())
#                 if (len(rowitems) > 4) and (rowitems[3] == u"COEFF="):
#                     self._phytowin_coeff2magni_dict[rowitems[4]] = rowitems[0]
#                 row = file.readline().strip(separator)
#                          
#             # Read info related to sample.
#             row = file.readline()
#             while len(row.replace(separator, '').strip()) > 0:
#                 key, value = row.split(separator, 1) # Don't split values (maxsplit = 1).
#                 self._phytowin_sample_info[key.strip().strip('"').strip()] = value.replace(separator, '').strip().strip('"').strip()
#                 row = file.readline()
#         #                       
#         except (IOError, OSError):
#             raise
#         finally:
#             if file: file.close()
# 
# 
#     def create_tree_dataset(self, dataset_top_node):    
#         """ """
#         # Add data to dataset node.
#         for parsinginforow in self._parsing_info:
#             if parsinginforow[0] == 'dataset':
#                 dataset_top_node.add_data(parsinginforow[1], self._phytowin_sample_info[parsinginforow[3]])        
#         
#         # Create visit node and add data. Note: Only one visit in each file. 
#         visitnode = plankton_core.VisitNode()
#         dataset_top_node.add_child(visitnode)
#         
#         for parsinginforow in self._parsing_info:
#             if parsinginforow[0] == 'visit':
# 
#                 
#                                 
#                 if parsinginforow[1] == 'sample_date':
#                     sample_date = self._phytowin_sample_info[parsinginforow[3]]
#                     sample_date = sample_date                                  
#                     try:
#                         value = dateutil.parser.parse(sample_date)
#                         if value:
#                             sample_date = unicode(value.strftime('%Y-%m-%d'))
#                     except:
#                         toolbox_utils.Logging().warning('Parser: Failed to convert to date: ' + sample_date)
#                     #
#                     visitnode.add_data(parsinginforow[1], sample_date) 
#                     
#                     # Add visit_year and visit_month.
#                     try:
#                         visitnode.add_data('visit_year', sample_date[0:4])
#                     except: pass      
#                     try:
#                         visitnode.add_data('visit_month', sample_date[5:7])        
#                     except: pass      
#                 else:
#                     visitnode.add_data(parsinginforow[1], self._phytowin_sample_info[parsinginforow[3]])        
#         
#         # Create sample node and add data. Note: Only one sample in each file. 
#         samplenode = plankton_core.SampleNode()
#         visitnode.add_child(samplenode)
#         
#         for parsinginforow in self._parsing_info:
#             if parsinginforow[0] == 'sample':
#                 samplenode.add_data(parsinginforow[1], self._phytowin_sample_info[parsinginforow[3]])        
#         
#         # Create variable nodes.
#         for row in self._phytowin_rows:
#             variablenode = plankton_core.VariableNode()
#             samplenode.add_child(variablenode)
#             #
#             for parsinginforow in self._parsing_info:
#                 if parsinginforow[0] == 'variable':
#                     value = self._phytowin_sample_info.get(parsinginforow[3], '')
#                     variablenode.add_data(parsinginforow[1], value)        
#             #
#             row_dict = dict(zip(self._phytowin_header, row))
#             #
#             for parsinginforow in self._parsing_info:
#                 if parsinginforow[0] == 'variable':
#                     value = row_dict.get(parsinginforow[3], '')
#                     if len(value) > 0: # Don't overwrite from previous step.
#                         variablenode.add_data(parsinginforow[1], value)        
#                 
#                         # Add text field with magnification info. Use coeff as key.
#                         if parsinginforow[1] == 'coefficient':
#                             if value in self._phytowin_coeff2magni_dict:
#                                 value = self._phytowin_coeff2magni_dict[value].replace('Part counted with ', '')
#                                 variablenode.add_data('magnification', value)
#                     
#             # Copy to new variable nodes for parameters.
#             for parsinginforow in self._parsing_info:
#                 if parsinginforow[0] == 'copy_parameter':
#                     paramunit = parsinginforow[1].split(':')
#                     parameter = paramunit[0]
#                     if len(paramunit) > 1:
#                         unit = paramunit[1]
#                     else: 
#                         unit = ''
#                     value = row_dict.get(parsinginforow[3], '')
#                     if len(value.strip()) > 0:
#                         self.copy_variable(variablenode, p = parameter, v = value, u = unit)
# 
#     ### Special conversions of PhytoWin species and size classes. ###
#     def update_species_and_sizes(self, dataset_top_node):
#         """ """
#         for visit in dataset_top_node.get_children():
#             for sample in visit.get_children():
#                 for variable in sample.get_children():
#                     scientificname = variable.get_data('reported_scientific_name')
#                     sizeclass = variable.get_data('reported_size_class')
#                     sflag = variable.get_data('species_flag_code')
#                     # Fix 'cf.' and 'sp.''.
#                     scientificname, sflag = plankton_core.DataImportUtils().cleanup_scientific_name_cf(scientificname, sflag)
#                     scientificname, sflag = plankton_core.DataImportUtils().cleanup_scientific_name_sp(scientificname, sflag)
#                     # Translate base on translation file.
#                     name, size, pw_sflag = self._convert_phytowin_species_and_sizes(scientificname, sizeclass)
#                     #
#                     if ('spp' in sflag) and ('spp' in pw_sflag):
#                         pass
#                     else:
#                         if pw_sflag: sflag += ' '+ pw_sflag  
#                     #
#                     if name: variable.add_data('scientific_name', name)
#                     if size: variable.add_data('size_class', size)
#                     if sflag: variable.add_data('species_flag_code', sflag.strip())
#                     #
#                     # Get trophic level from peg.
#                     value = plankton_core.Species().get_bvol_value(name, size, 'bvol_trophic_type')
#                     if value:
#                         variable.add_data('trophic_type', value)
#                     else:
#                         variable.add_data('trophic_type', variable.get_data('reported_trophic_type'))
#                     # Get taxonomic class from peg.
#                     value = plankton_core.Species().get_taxon_value(name, 'taxon_class')
#                     variable.add_data('taxon_class', value)
# 
#     
#     def _convert_phytowin_species_and_sizes(self, phytowin_name, phytowin_size_class):
#         """ Returns 'PEG name', 'PEG size' and 'SFLAG' as tuple. """
#         if phytowin_name in self._pythowin_peg_mapping:
#             nameobject = self._pythowin_peg_mapping[phytowin_name]
#             if phytowin_size_class in nameobject[u'Sizes']:
#                 sizeobject = self._pythowin_peg_mapping[phytowin_name][u'Sizes'][phytowin_size_class]
#                 return (sizeobject[u'PEG name'], sizeobject[u'PEG size'], sizeobject[u'SFLAG'])
#             else:
# #                 return (None, None, None)
#                 # Don't convert if not in translation list. Return parameters. 
#                 return (phytowin_name, phytowin_size_class, '')
#         else:
# #             return (None, None, None)
#             # Don't convert if not in translation list. Return parameters. 
#             return (phytowin_name, phytowin_size_class, '')
#              
#     def _load_phytowin_species_and_sizes_mapping(self):
#         """ """
#         self._pythowin_peg_mapping = {} 
#         # Read data from Excel file.
#         tablefilereader = toolbox_utils.TableFileReader(
#                                 file_path = '',
#                                 excel_file_name = self._phytowin_to_peg_filename,
#                                 )
#         #
#         for row in tablefilereader.rows():
#             if len(row) < 2:
#                 continue 
#             #
#             phytowinname = row[0]
#             phytowinsize = row[1]
#             if phytowinsize:
#                 try:
#                     # Convert from float to int. Excel related problem.
#                     phytowinsize = unicode(int(float(phytowinsize.replace(',', '.'))))
#                 except:
#                     phytowinsize = u''
#                     print(u'loadPhytowinPegMapping, phytowinsize: ' + row[1])
#             pegname = row[2]
#             pegsize = row[3]
#             if pegsize:
#                 try:
#                     # Convert from float to int. Excel related problem.
#                     pegsize = unicode(int(float(pegsize.replace(',', '.'))))
#                 except:
#                     pegsize = u''
#                     print(u'loadPhytowinPegMapping, pegsize: ' + row[3])
#             sflag = row[4]
#             #
#             if phytowinname:
#                 if phytowinname not in self._pythowin_peg_mapping:
#                     self._pythowin_peg_mapping[phytowinname] = {}
#                     self._pythowin_peg_mapping[phytowinname][u'Sizes'] = {}
#                 phytowinobject = self._pythowin_peg_mapping[phytowinname]
#                 #
#                 phytowinobject[u'SFLAG'] = sflag
#                 #
#                 sizeobject = {u'PEG name': pegname, u'PEG size': pegsize, u'SFLAG': sflag}
#                 phytowinobject[u'Sizes'][phytowinsize] = sizeobject
# 
# 
# ############################### From reports ##################################################
# 
# #         # Iterate over species in the dictionary.
# #         for phytowinnameandsize in species_sample_dict.keys():
# #             # NET samples:            
# #             ## Extract useful part from Species-column.
# #             ## Example: "Protoperidinium steinii HET 32 (cell: 32-37µm)"
# #             #parts = phytowinname.split(u' ')
# #             #speciesname = u''
# #             #for part in parts:
# #             #    if part not in [u'cf.', u'HET', u'32', u'(cell:', u'(width:', u'(no']:
# #             #        speciesname += part + u' '
# #             #    else:
# #             #        if part not in [u'cf.']:
# #             #            break # Break loop.
# #             #speciesname = speciesname.strip()
# #             #
# #             # Counted samples:
# #             namesize = phytowinnameandsize.split(':')
# #             phytowinname = namesize[0]
# #             # Remove 'cf.'
# #             if u'cf.' in phytowinname:  
# #                 parts = phytowinname.split(u' ')
# #                 speciesname = u''
# #                 for part in parts:
# #                     if part not in [u'cf.']:
# #                         speciesname += part + u' '
# #                 phytowinname = speciesname.strip()
# #             #
# #             sizeclass = namesize[1]
# #             #
# # #             if self._taxaphytowin is not None:
# # #                 pegname, pegsize, sflag = self._taxaphytowin.TaxaPhytowin().convert_from_phytowin_to_peg(phytowinname, phytowin_size_class = sizeclass)
# # #             else:
# # #                 pegname = phytowinname
# # #                 pegsize = sizeclass
# # #                 sflag = ''
# #             pegname = phytowinname
# #             pegsize = sizeclass
# #             sflag = ''
# # 
# #             # Check if 'cf.' was included in name. Add to Sflag.
# #             if u'cf.' in variablenode.get_data('scientific_name'):
# #                 if sflag:
# #                     sflag = 'cf., ' + sflag
# #                 else:
# #                     sflag = 'cf.'
# 
# 
# #             # Remove 'cf.'
# #             if u'cf.' in phytowinname:  
# #                 parts = phytowinname.split(u' ')
# #                 speciesname = u''
# #                 for part in parts:
# #                     if part not in [u'cf.']:
# #                         speciesname += part + u' '
# #                 phytowinname = speciesname.strip()
# 
# 
# #             # Check if 'cf.' was included in name. Add to Sflag.
# #             if u'cf.' in variablenode.get_data('scientific_name'):
# #                 if sflag:
# #                     sflag = 'cf., ' + sflag
# #                 else:
# #                     sflag = 'cf.'

