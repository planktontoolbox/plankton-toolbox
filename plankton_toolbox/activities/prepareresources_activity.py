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
import plankton_toolbox.activities.activity_base as activity_base

class PrepareResourcesActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(PrepareResourcesActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        # === GroupBox: dyntaxabox === 
        dyntaxabox = QtGui.QGroupBox("Dynamic taxa", self)
        # Active widgets and connections.
        self.__source_list = QtGui.QComboBox()
        self.__source_list.addItems(["<select source>",
                                     "Dyntaxa, SOAP",
                                     "Dyntaxa, REST",
                                     "Dyntaxa, DB-tables as text files"])
        self.__fromdirectory_edit = QtGui.QLineEdit("../../data/dyntaxa")
        self.__tofile_edit = QtGui.QLineEdit("../data/resources/dyntaxa_2009.json")
        self.__preparedyntaxa_button = QtGui.QPushButton("Create resource")
        self.connect(self.__preparedyntaxa_button, QtCore.SIGNAL("clicked()"), self.__prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Source:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__source_list, 0, 1, 1, 1);
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__fromdirectory_edit, 1, 1, 1, 10)
        label3 = QtGui.QLabel("To file:")
        form1.addWidget(label3, 2, 0, 1, 1)
        form1.addWidget(self.__tofile_edit, 2, 1, 1, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__preparedyntaxa_button)
        dyntaxalayout = QtGui.QVBoxLayout()
        dyntaxalayout.addLayout(form1)
        dyntaxalayout.addLayout(hbox1)
        dyntaxabox.setLayout(dyntaxalayout)

        # === GroupBox: pegbox === 
        pegbox = QtGui.QGroupBox("PEG, Plankton Expert Group", self)
        # Active widgets and connections.
        self.__fromfile_edit = QtGui.QLineEdit("../../data/peg.txt")
        self.__tofile_edit = QtGui.QLineEdit("../data/resources/peg_2010.json")
        self.__preparepeg_button = QtGui.QPushButton("Create resource")
        self.connect(self.__preparepeg_button, QtCore.SIGNAL("clicked()"), self.__preparePeg)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__fromfile_edit, 0, 1, 1, 10);
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__tofile_edit, 1, 1, 1, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__preparepeg_button)
        peglayout = QtGui.QVBoxLayout()
        peglayout.addLayout(form1)
        peglayout.addLayout(hbox1)
        pegbox.setLayout(peglayout)
         
        # === Main level layout. ===
        content = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addWidget(dyntaxabox)
        contentLayout.addWidget(pegbox)
        contentLayout.addStretch(5)
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)

    def __prepareDyntaxa(self):
        """ """
#        self._writeToLog("Name: " + self.__nameedit.text())

    def __preparePeg(self):
        """ """
#        self._writeToLog("Name: " + self.__nameedit.text())


