#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

#import envmonlib

class FormatBase(object):
    """ """
    def __init__(self):
        """ Abstract class for import formats. """
        super(FormatBase, self).__init__()
        #
        self._dataset = None
        self._header = []
        self._row = None

    def _setHeader(self, header):
        """ """
        self._header = header

    def _setRow(self, row):
        """ """
        self._row = row

    def reorganizeDataset(self):
        """ Generic method to be used when a dataset is divided into multiple files. """

    def reformatDataset(self):
        """ Generic method to be used when a dataset is divided into multiple files. """

    def basicScreening(self):
        """ """

