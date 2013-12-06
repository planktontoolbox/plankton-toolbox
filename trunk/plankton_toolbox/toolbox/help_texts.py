#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute 
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
class HelpTexts(object):  
    """ Help texts for the toolbox. 
        Mostly displayed in util_qt.RichTextQLabel labels, basic HTML tags can be used. 
    """

    def __init__(self, parent = None):  
        """ """
        self._texts = {}
        self._addTexts()

    def getText(self, key):
        """ """
        
        # Waiting for new texts to ber written....
        return u''
        
#         try:          
#             return self._texts[key]
#         except:
#             print(u"DEBUG: HelpTexts.getText not available for the key: " + key)
#         return u'Note: Help text is missing.'

  
    def _addTexts(self):
        """ """          

        self._texts[u'AnalyseDatasetsTab1_intro'] = """
        Select dataset(s) to be analyzed. 
        Note that "Analysis data" contains a working copy of one or several loaded datasets. 
        Rows in "Analysis data" can be removed, added or aggregated during the analysis.
        """

        self._texts[u'AnalyseDatasetsTab2_intro'] = """
        Prepare your data by removing unwanted rows from "Analysis data".
        This may be useful if you want to use data from one or a few stations or data from a certain depth or time period.
        """

        self._texts[u'AnalyseDatasetsTab3_intro'] = """
        You may want to aggregate abundance or biovolume data from the level of size group or 
        species level to a higher taxonomic level. 
        A common task is to aggregate to genus or class level. 
        Also a level termed Algal groups with fewer classes is available. 
        Here you can also select only autotrophs (AU), mixotrophs (MX), heterotrophs (HT) or 
        organisms with trophic type not specified (NS). 
        For phytoplankton most often a combination is used, e.g. AU + MX for all organisms with photosynthesis.
        """

        self._texts[u'AnalyseDatasetsTab4_intro'] = """
        Select parts of "Analysis data".
        This is only a filter and the content of "Analysis data" is not changed. To view and save the filtered data select "View: Selected data" below.
        """

        self._texts[u'AnalyseDatasetsTab5_intro'] = """
        Plot your data. A number of pre-defined types of graphs are available.
        """ 

        self._texts[u'AnalyseDatasetsTab6_intro'] = """
        Plot almost any combination of data you like. 
        These graphs are in general not as nice looking as the pre-defined graphs but are more flexible.
        """        

        self._texts[u'CreateReportsActivity_intro'] = """
        Creates reports from Phytowin files (*.csv). 
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """

        self._texts[u'LoadDatasetsActivity_text_intro'] = """
        Choose the Excel-tab or the Text-tab to load one or several files with your 
        plankton or hydrography data as text files or Excel-files. 
        Before loading data you need to set up the import and export formats by selecting parsers. 
        The parsers are Excel-files with information on how to interpret the data you import in 
        txt-format or in xlsx format. 
        Note that the xls-format in older versions of Excel is not supported.
        """        

        self._texts[u'LoadDatasetsActivity_excel_intro'] = """
        Choose the Excel-tab or the Text-tab to load one or several files with your plankton or hydrography data as text files or Excel-files. 
        Before loading data you need to set up the import and export formats by selecting parsers. 
        The parsers are Excel-files with information on how to interpret the data you import in txt-format or in xlsx format. 
        Note that the xls-format in older versions of Excel is not supported.
        """

        self._texts[u'ScreeningActivity_intro_1'] = """
        Screen your data for inconsistences regarding code values etc. 
        Used lists of codes can be found in the folder "toolbox_data/code_lists". 
        """        

        self._texts[u'ScreeningActivity_intro_2'] = """
        Screen your data for inconsistences regarding species names etc.
        """
                
        self._texts[u'ScreeningActivity_species'] = """
        The taxonomic hierarchy in www.nordicmicroalgae.org is used as a reference. 
        This is based on www.algaebase.org and the Dyntaxa database at the Swedish Species Centre.
        """
               
        self._texts[u'ScreeningActivity_sizeclasses'] = """
        BVOL screening is for work with biovolumes of phytoplankton. 
        The HELCOM-PEG list of species and biovolumes is used as default. The latest version is available at www.ices.dk/
        """        

        self._texts[u'ScreeningActivity_intro_3'] = """
        Used for manual check of column values to find outliers or misspellings in the datasets.
        """        

        self._texts[u'ScreeningActivity_plotting'] = """
        Plot your raw data to find outliers or errors. Select parameters to plot.
        """        

        self._texts[u'StartActivity_intro_1'] = """
        <br/>
        <h3>Welcome to the Plankton Toolbox</h3>
        <p>
        The Plankton Toolbox is a free tool for aquatic scientists, and others, 
        working with environmental monitoring related to phyto- and zooplankton.
        With the Plankton Toolbox you can:
        <ul>
        <li><b>Load plankton and hydrography datasets</b> from text or Excel files. 
        Parsers are provided for reading some predefined formats. 
        You can create your own parser if needed.
        </li>
        <li><b>Screen your data</b> for inconsistences regarding code values, species names, etc. The taxonomic hierarchy in 
        <a href="http://nordicmicroalgae.org">http://nordicmicroalgae.org</a> is used as a reference.
        </li>
        <li><b>Analyse your data.</b> Select a subset of data found in your loaded data. 
        Aggregate data, e.g. from species level to class level.
        </li>
        <li><b>Export data</b> for use with other software.
        </li>
        <li><b>Plot data</b> and save your plots.
        </li>
        </ul>
        </p>
        """

        self._texts[u'StartActivity_intro_2'] = """
        <h4>Usage instructions</h4>
        <p>
        From the main menu you can select between activities and view tools. 
        Selected activity is always shown at the center and tools can be placed to the right,
        bottom or as floating windows. Double-click or click-and-drag in the title bar to move 
        them around. The toolbox will remember window positions when closing down.
        </p>        
        <p>
        When using the toolbox information, warnings and errors are logged to the 
        "Toolbox logging"-tool. The same information is always written to the file 
        "plankton_toolbox_log.txt". The log file is cleared each time you starts the 
        Plankton Toolbox.       
        </p>        
        """

        self._texts[u'StartActivity_intro_3'] = """
        <h4>Preloaded data</h4>
        <p>
        To run the Plankton Toolbox there should be a folder named "toolbox_data" in the 
        same folder as the executable file. It contains species lists, parsers used when 
        importing data files and code-lists for screening. These files can be modified 
        by the user and new files can be added if the default set of files can't be used.
        </p>
        """

        self._texts[u'StartActivity_intro_4'] = """
        <h4>Under development...</h4>
        <p>
        The Plankton Toolbox is under development.
        In this release the Screening activity is added on a basic level. Feedback from users is needed. 
        The Graph plotter tool is in early development and contains a lot of bugs.
        Planned functionality for future releases include better support for zooplankton data, the inclusion 
        of statistical tools and a module for counting plankton at the microscope.
        </p>
        <p>
        Comments, bug reports and requests 
        for new functionality are welcome and can be sent to 
        <a href="mailto:info@nordicmicroalgae.org">info@nordicmicroalgae.org</a>
        </p>
        """












