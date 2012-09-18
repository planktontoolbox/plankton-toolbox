#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
    
# TEST for windows:    
    import ctypes
    myappid = 'smhi.se.plankton-toolbox'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("SMHI")
    app.setOrganizationDomain("smhi.se")
    
    app.setApplicationName("Plankton Toolbox")
    app.setWindowIcon(QtGui.QIcon(u'plankton_toolbox_icon.jpg'))
    
    utils_qt.setAppStyleSheet(app)
    
    window = toolbox_main_window.MainWindow()
    window.show()
    sys.exit(app.exec_())
