#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# Version for "Plankton toolbox - desktop application".
__version__ = "1.4.0-Development"

# Matplotlib for PyQt6.
# Backend must be defined before other matplotlib imports.
import matplotlib

matplotlib.use("QtAgg")
# Import to make PyInstaller be aware of the libs.
import openpyxl
import numpy

# Plankton toolbox desktop application framework.
import app_framework

if __name__ == "__main__":
    app_framework.set_version(__version__)
    app_framework.desktop_application()
