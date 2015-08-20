#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_toolbox.toolbox.toolbox_app as toolbox_app

__version__ = '1.1.1' # Plankton Toolbox version.

if __name__ == "__main__":
    toolbox_app.set_version(__version__)
    toolbox_app.plankton_toolbox_application()
