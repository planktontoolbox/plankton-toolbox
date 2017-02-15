#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_toolbox.toolbox.toolbox_app as toolbox_app
import plankton_toolbox.toolbox.utils_qt as utils_qt

__version__ = '1.2.2' # Plankton Toolbox version.

if __name__ == "__main__":
    toolbox_app.set_version(__version__)
    utils_qt.set_version(__version__)
    toolbox_app.plankton_toolbox_application()
