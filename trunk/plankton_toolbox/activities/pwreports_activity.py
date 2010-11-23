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

class PwReportsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(PwReportsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        # === GroupBox: databox === 
        databox = QtGui.QGroupBox("Select data files", self)
        # Active widgets and connections.
        self.__fromdirectory_edit = QtGui.QLineEdit("testdata/pwdata")
        self.__fromdirectory_button = QtGui.QPushButton("Browse...")
        self.__files_table = QtGui.QTableWidget()
        self.connect(self.__fromdirectory_button, QtCore.SIGNAL("clicked()"), self.__fromDirectoryBrowse)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("From directory:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__fromdirectory_edit, 0, 2, 1, 8)
        form1.addWidget(self.__fromdirectory_button, 0, 10, 1, 1)
        label2 = QtGui.QLabel("Files (CSV):")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__files_table, 1, 1, 10, 10)       
        datalayout = QtGui.QVBoxLayout()
        datalayout.addLayout(form1)
        databox.setLayout(datalayout)
        
        # === GroupBox: resourcebox === 
        resourcebox = QtGui.QGroupBox("Select resources", self)
        # Active widgets and connections.
        self.__pegfile_edit = QtGui.QLineEdit("../../data/resources/peg.json")
        self.__pegfile_button = QtGui.QPushButton("Browse...")
        self.__translatefile_edit = QtGui.QLineEdit("../../data/resources/translate_pw_to_peg.json")
        self.__translatefile_button = QtGui.QPushButton("Browse...")
        self.connect(self.__pegfile_button, QtCore.SIGNAL("clicked()"), self.__pegFileBrowse)                
        self.connect(self.__translatefile_button, QtCore.SIGNAL("clicked()"), self.__translateFileBrowse)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("PEG:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__pegfile_edit, 0, 1, 1, 8)
        form1.addWidget(self.__pegfile_button, 0, 10, 1, 1)
        label2 = QtGui.QLabel("Translate PW to PEG:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__translatefile_edit, 1, 1, 1, 8)
        form1.addWidget(self.__translatefile_button, 1, 10, 1, 1)
        resourcelayout = QtGui.QVBoxLayout()
        resourcelayout.addLayout(form1)
        resourcebox.setLayout(resourcelayout)
        
        # === GroupBox: reportbox === 
        reportbox = QtGui.QGroupBox("Select report", self)
        # Active widgets and connections.
        self.__report_list = QtGui.QComboBox()
        self.__report_list.addItems(["<select report>",
                                     "PW Report 1",
                                     "PW Report 2",
                                     "PW Report 3"])
        self.__tofile_edit = QtGui.QLineEdit("report.txt")
        self.__createreport_button = QtGui.QPushButton("Create report")
        self.connect(self.__createreport_button, QtCore.SIGNAL("clicked()"), self.__createPwReport)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Select report:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__report_list, 0, 2, 1, 1)
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__tofile_edit, 1, 2, 1, 8)
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(form1)
        reportbox.setLayout(reportlayout)
        
        # === Button: Generate report ===
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__createreport_button)
        
        # === Main level layout. ===
        content = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addWidget(databox)
        contentLayout.addWidget(resourcebox)
        contentLayout.addWidget(reportbox)
        contentLayout.addLayout(hbox1)
        contentLayout.addStretch(5)
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)
                
    def __fromDirectoryBrowse(self):
        """ """
        utils.Logger().info("AAA")
                
    def __pegFileBrowse(self):
        """ """
        utils.Logger().info("BBB")
                
    def __translateFileBrowse(self):
        """ """
        utils.Logger().info("CCC")
                
    def __createPwReport(self):
        """ """
        utils.Logger().info("DDD")

