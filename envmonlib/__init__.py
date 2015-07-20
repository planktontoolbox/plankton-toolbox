#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
from toolbox_utils.patterns import singleton
from toolbox_utils.logging import Logging
from utils.viewformats import ViewFormats
from utils.excelfiles import ExcelFiles
from utils.textfiles import TextFiles
from utils.zipfiles import ZipFileReader
from utils.zipfiles import ZipFileWriter
# from toolbox_utils.graphplotter import GraphPlotData
# from toolbox_utils.graphplotter import ChartBase
# from toolbox_utils.graphplotter import LineChart
# from toolbox_utils.graphplotter import BarChart
# from toolbox_utils.graphplotter import ScatterChart
# from toolbox_utils.graphplotter import PieChart
# from toolbox_utils.graphplotter import BoxPlotChart
# from toolbox_utils.graphplotter import MapChart

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
 
# Module dataanalysis: 
from dataanalysis.analysisdata import AnalysisData
from dataanalysis.analysisprepare import AnalysisPrepare
from dataanalysis.reportdata import ReportData
from dataanalysis.statisticaldata import StatisticalData

