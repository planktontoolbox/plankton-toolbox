#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
        try:          
            return self._texts[key]
        except:
            pass
        return ''
  
    def _addTexts(self):
        """ """          
        self._texts['StartActivity_intro'] = """
        <br/>
        <h3>Welcome to the Plankton Toolbox</h3>
        <p>
        The Plankton Toolbox is a free tool for aquatic scientists, and others, 
        working with environmental monitoring related to phyto- and zooplankton. 
        </p>
        <p>
        Features include:
        <ul>        
            <li>Imports phyto- or zooplankton data in .txt and .xlsx files in different formats (configurable)
            </li>
            <li>Work with data on abundance, biovolume and carbon content
            </li>
            <li>Data screening - quality control of data
            </li>
            <li>Aggregate data, e.g. from species level to class level
            </li>
            <li>Plotting tools
            </li>
            <li>Statistics (in early development)
            </li>
            <li>Export data in .txt or .xlsx for further analysis or plotting
            </li>
        </ul>
        </p>
        
        <h4>Usage instructions</h4>
        <p>
        A User Guide is available at: 
        <a href="http://wiki.plankton-toolbox.org">http://wiki.plankton-toolbox.org</a>.
        </p>

        <h4>Preloaded data</h4>
        <p>
        To run the Plankton Toolbox there should be a folder named <b>toolbox_data</b> in the 
        same folder as the executable file. It contains species lists, parsers (used for dataset imports)
        and code-lists for screening. These files can be modified by the user and new files can be added 
        if the default set of files can't be used.
        </p>
        <p>
        More information about the content in the toolbox_data folder is available at: 
        <a href="http://wiki.plankton-toolbox.org">http://wiki.plankton-toolbox.org</a>.
        </p>
        
        <h4>Under development</h4>
        <p>
        The Plankton Toolbox  is under development and provided free with no guarantees regarding functionality. 
        Comments, bug reports and requests for new functionality are welcome and can be sent to 
        <a href="mailto:info@nordicmicroalgae.org">info@nordicmicroalgae.org</a>
        </p>

        """

