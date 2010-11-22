#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.utils as utils
import plankton_toolbox.activities.activity_base as activity_base

class TemplateActivity(activity_base.ActivityBase):
    """
    This is a template for new activities.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(TemplateActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        # === GroupBox: templatebox === 
        # Active widgets and connections.
        self.__nameedit = QtGui.QLineEdit("<Name>")
        self.__emailedit = QtGui.QLineEdit("<Email>")
        self.__customerlist = QtGui.QListWidget()
        self.__testbutton = QtGui.QPushButton("Write email to log")
        self.connect(self.__testbutton, QtCore.SIGNAL("clicked()"), self.__test)                
        # Layout widgets.
        templatebox = QtGui.QGroupBox("Member info", self)
        #
        form1 = QtGui.QFormLayout()
        form1.addRow("&Name:", self.__nameedit);
        form1.addRow("&Email:", self.__emailedit);
        form1.addRow("&Projects:", self.__customerlist);
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(self.__testbutton)
        #
        templatelayout = QtGui.QVBoxLayout()
        templatelayout.addLayout(form1)
        templatelayout.addLayout(hbox1)
        templatelayout.addStretch()
        templatebox.setLayout(templatelayout)
        # === Main level layout. ===
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(templatebox)
        mainlayout.addStretch()
        self.setLayout(mainlayout)
        # Test data.
        self.__customerlist.addItems(QtCore.QStringList()
            << "First project."
            << "Second project.")
        # 
        self._writeToLog("The template activity was successfully created.")

    def __test(self):
        """ """
#        self._writeToLog("Name: " + self.__emailedit.text())
        utils.Logger().info("Name: " + self.__emailedit.text())
        
