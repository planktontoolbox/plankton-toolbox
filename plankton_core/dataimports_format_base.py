#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import toolbox_utils
import plankton_core

class FormatBase(object):
    """ """
    def __init__(self):
        """ Abstract class for import formats. """
        super(FormatBase, self).__init__()
        #
        self._dataset = None
        self._header = []
        self._row = None

    def _set_header(self, header):
        """ """
        self._header = header

    def _set_row(self, row):
        """ """
        self._row = row

    def reorganize_dataset(self):
        """ Generic method to be used when a dataset is divided into multiple files. """

    def reformat_dataset(self):
        """ Generic method to be used when a dataset is divided into multiple files. """

    def basic_screening(self):
        """ """

