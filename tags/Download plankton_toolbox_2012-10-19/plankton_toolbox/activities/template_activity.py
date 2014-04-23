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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import envmonlib

class TemplateActivity(activity_base.ActivityBase):
    """
    Template class for new activities.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(TemplateActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
#        self._activityheader.setStyleSheet(""" 
#            * { color: white; background-color: #00677f; }
#            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addLayout(self._contentPersonInfo())
        contentLayout.addLayout(self._contentButtons())
        contentLayout.addStretch(5)

    def _contentPersonInfo(self):
        """ """
        # Active widgets and connections.
        self._nameedit = QtGui.QLineEdit("<Name>")
        self._emailedit = QtGui.QLineEdit("<Email>")
        self._customerlist = QtGui.QListWidget()
        # Layout.
        layout = QtGui.QFormLayout()
        layout.addRow("&Name:", self._nameedit)
        layout.addRow("&Email:", self._emailedit)
        layout.addRow("&Projects:", self._customerlist)
        # Test data.
        self._customerlist.addItems(QtCore.QStringList()
            << "<First project.>"
            << "<Second project.>")
        #
        return layout

    def _contentButtons(self):
        """ """
        # Active widgets and connections.
        self._testbutton = QtGui.QPushButton("Write name to log")
        self.connect(self._testbutton, QtCore.SIGNAL("clicked()"), self._test)                
        # Layout.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self._testbutton)
        #
        return layout

    def _test(self):
        """ """
        envmonlib.Logging().log("Name: " + unicode(self._emailedit.text()))
        