#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
Envmonlib, Environmental monitoring library.

Envmonlib contains functionality to be used when working with biologically 
environmental monitoring data. Envmonlib is developed in Python 2.7 and released 
under the MIT-license.

Envmonlib is the core module in the application "Plankton Toolbox". 
More information can be found here: http://plankton-toolbox.org

Main modules:
- datasets 
- dataimports 
- dataimportformats 
- dataexports 
- datascreening 
- datareports 
- species
- utils

"""

# Module utils:
from utils.patterns import singleton
from utils.logging import Logging
from utils.fieldformats import FieldTypes
from utils.excelfiles import ExcelFiles
from utils.textfiles import TextFiles
from utils.zipfiles import ZipFileReader
from utils.zipfiles import ZipFileWriter
from utils.graphplotter import GraphPlotData
from utils.graphplotter import ChartBase
from utils.graphplotter import LineChart
from utils.graphplotter import BarChart
from utils.graphplotter import ScatterChart
from utils.graphplotter import PieChart

# Module species:
from species.species import Species

# Module datasets:
from datasets.dataset_base import DatasetBase
from datasets.dataset_table import DatasetTable
from datasets.dataset_tree import (
                                   DataNode,
                                   DatasetNode,     
                                   VisitNode,   
                                   SampleNode,
                                   VariableNode)
from datasets.datasets import Datasets

# Module dataimports:
from dataimports.format_base import FormatBase
from dataimports.parsed_format import ParsedFormat
from dataimports.import_manager import ImportManager

# Module dataimportformats:
from dataimportformats.format_singlefile import FormatSingleFile
 
# Module dataexports:
from dataexports.export_manager import ExportManager
 
# Module datascreening:
from datascreening.screening_manager import ScreeningManager
 
# Module datareports: 
from datareports.reports_manager import ReportsManager
