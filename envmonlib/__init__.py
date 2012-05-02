#!/usr/bin/env python

"""
envmonlib, Environmental monitoring library.

Main modules:
- datasets 
- dataimports 
- dataexports 
- datascreening 
- datareports 
- utils

Test:

Data:
- testdata
- templates

"""

# Module utils:
from utils.patterns import singleton
from utils.logging import Logging
from utils.excelfiles import ExcelFiles
from utils.textfiles import TextFiles
from utils.zipfiles import ZipFileReader
from utils.zipfiles import ZipFileWriter

# Module species:
from species.taxa import Taxa

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
from dataimports.import_manager import ImportManager

# Module dataimportformats:
from dataimportformats.format_singlefile import FormatSingleFile
 
# Module dataexports:
from dataexports.export_manager import ExportManager
 
# Module datascreening:
from datascreening.screening_manager import ScreeningManager
 
# Module datareports: 
from datareports.reports_manager import ReportsManager
 
# Module tests: 
from tests.tests_manager import TestsManager
