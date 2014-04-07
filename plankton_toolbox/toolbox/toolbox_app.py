#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

"""
Main module of the application Plankton Toolbox.

Organization name, domain and application name are used by QSettings. Settings
are stored in the register on Windows (path: "HKEY_CURRENT_USER/Software/SMHI/
Plankton Toolbox"), in $HOME/.config on Linux and in $HOME/Library/Preferences 
on Mac OS X.
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


###if __name__ == '__main__':
def plankton_toolbox_application():
    """
    Main application for the Plankton Toolbox.
    """

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("SMHI")
    app.setOrganizationDomain("smhi.se")
    app.setApplicationName("Plankton Toolbox")
    
    # Windows only (needed for application icon):
    try:
        if sys.platform.startswith('win'):    
            import ctypes
            myappid = 'smhi.se.plankton-toolbox'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

#     app.setWindowIcon(QtGui.QIcon(u'toolbox_data/img/plankton_toolbox_icon.ico'))
    app.setWindowIcon(QtGui.QIcon(u'toolbox_data/img/plankton_toolbox_icon.png'))
    
    utils_qt.setAppStyleSheet(app)
    
    window = toolbox_main_window.MainWindow()
    window.show()
    sys.exit(app.exec_())
