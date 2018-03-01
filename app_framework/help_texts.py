#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

class HelpTexts(object):  
    """ Help texts for the desktop application. 
        Mostly displayed in util_qt.RichTextQLabel labels, basic HTML tags can be used. 
    """
    
    def __init__(self, parent = None):  
        """ """
        self._texts = {}
        self._add_texts()
    
    def get_text(self, key):
        """ """
        try:          
            return self._texts[key]
        except:
            pass
        return ''
    
    def _add_texts(self):
        """ """          

        # Start activity..

        self._texts['start_activity'] = """
        <p>&nbsp;</p>

        
        """
        
        # About.
        
        self._texts['about'] = """
        <p>


        </p>
        """


