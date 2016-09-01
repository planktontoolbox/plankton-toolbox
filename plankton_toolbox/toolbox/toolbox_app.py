#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals


"""
Main module of the application Plankton Toolbox.

Organization name, domain and application name are used by QSettings. Settings
are stored in the register on Windows (path: "HKEY_CURRENT_USER/Software/
Plankton Toolbox/Plankton Toolbox'), in $HOME/.config on Linux and in 
$HOME/Library/Preferences on Mac OS X.
"""

# Matplotlib for Qt4. 
# Backend must be defined before some other matplotlib imports.
import matplotlib
matplotlib.use('Qt4Agg')
#
import sys
import PyQt4.QtGui as QtGui
import plankton_toolbox.toolbox.toolbox_main_window as toolbox_main_window
import plankton_toolbox.toolbox.utils_qt as utils_qt

__version__ = '' 

def plankton_toolbox_application():
    """
    Main application for the Plankton Toolbox.
    """

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Plankton Toolbox')
    app.setOrganizationDomain('plankton-toolbox.org')
    app.setApplicationName('Plankton Toolbox')
    
    # Windows only (needed for application icon):
    try:
        if sys.platform.startswith('win'):    
            import ctypes
            myappid = 'plankton-toolbox'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

#     app.setWindowIcon(QtGui.QIcon('toolbox_data/img/plankton_toolbox_icon.ico'))
    app.setWindowIcon(QtGui.QIcon('toolbox_data/img/plankton_toolbox_icon.png'))
    # Style, colours, etc.
    utils_qt.set_app_style_sheet(app)
    # Create application and start the main event loop. 
    window = toolbox_main_window.MainWindow()
    window.setVersion(__version__)
    window.show()
    sys.exit(app.exec_())

def set_version(version):
        """ """
        global __version__
        __version__ = version
