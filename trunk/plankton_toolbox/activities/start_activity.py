#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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
import envmonlib
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.toolbox.help_texts as help_texts

class StartActivity(activity_base.ActivityBase):
    """
    This activity is "a welcome page" with some possibilities to set up the environment.
    """
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(StartActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addLayout(self._contentWelcome())
        contentLayout.addLayout(self._contentUsage())
        contentLayout.addLayout(self._contentPreloaded())
        contentLayout.addLayout(self._contentUnderDevelopment())
        contentLayout.addStretch(5)

    def _contentWelcome(self):
        """ """
        # Active widgets and connections.
        label = utils_qt.RichTextQLabel()
        label.setText(help_texts.HelpTexts().getText(u'StartActivity_intro_1'))
#         label.setText("""
#         <br/>
#         <h3>Welcome to the Plankton Toolbox</h3>
#         <p>
#         The Plankton Toolbox is a free tool for aquatic scientists, and others, 
#         working with environmental monitoring related to phyto- and zooplankton.
#         With the Plankton Toolbox you can:
#         <ul>
#         <li><b>Load plankton and hydrography datasets</b> from text or Excel files. 
#         Parsers are provided for reading some predefined formats. 
#         You can create your own parser if needed.
#         </li>
#         <li><b>Screen your data</b> for inconsistences regarding code values, species names, etc. The taxonomic hierarchy in 
#         <a href="http://nordicmicroalgae.org">http://nordicmicroalgae.org</a> is used as a reference.
#         </li>
#         <li><b>Analyse your data.</b> Select a subset of data found in your loaded data. 
#         Aggregate data, e.g. from species level to class level.
#         </li>
#         <li><b>Export data</b> for use with other software.
#         </li>
#         <li><b>Plot data</b> and save your plots.
#         </li>
#         </ul>
#         </p>
#         """)
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
        #
        return layout

    def _contentUsage(self):
        """ """
        # Active widgets and connections.
        label1 = QtGui.QLabel()
        label1.setTextFormat(QtCore.Qt.RichText)
        label1.setWordWrap(True)
        label1.setText(help_texts.HelpTexts().getText(u'StartActivity_intro_2'))
#         label1.setText("""
#         <h4>Usage instructions</h4>
#         <p>
#         From the main menu you can select between activities and view tools. 
#         Selected activity is always shown at the center and tools can be placed to the right,
#         bottom or as floating windows. Double-click or click-and-drag in the title bar to move 
#         them around. The toolbox will remember window positions when closing down.
#         </p>        
#         <p>
#         When using the toolbox information, warnings and errors are logged to the 
#         "Toolbox logging"-tool. The same information is always written to the file 
#         "plankton_toolbox_log.txt". The log file is cleared each time you starts the 
#         Plankton Toolbox.       
#         </p>        
#         """)
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label1, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
        #
        return layout

    def _contentPreloaded(self):
        """ """
        # Active widgets and connections.
        label = utils_qt.RichTextQLabel()
        label.setText(help_texts.HelpTexts().getText(u'StartActivity_intro_3'))
#         label.setText("""
#         <h4>Preloaded data</h4>
#         <p>
#         To run the Plankton Toolbox there should be a folder named "toolbox_data" in the 
#         same folder as the executable file. It contains species lists, parsers used when 
#         importing data files and code-lists for screening. These files can be modified 
#         by the user and new files can be added if the default set of files can't be used.
#         </p>
#         """)
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
        #
        return layout

    def _contentUnderDevelopment(self):
        """ """
        # Active widgets and connections.
        label = utils_qt.RichTextQLabel()
        label.setText(help_texts.HelpTexts().getText(u'StartActivity_intro_4'))
#         label.setText("""
#         <h4>Under development...</h4>
#         <p>
#         The Plankton Toolbox is under development.
#         In this release the Screening activity is added on a basic level. Feedback from users is needed. 
#         The Graph plotter tool is in early development and contains a lot of bugs.
#         Planned functionality for future releases include better support for zooplankton data, the inclusion 
#         of statistical tools and a module for counting plankton at the microscope.
#         </p>
#         <p>
#         Comments, bug reports and requests 
#         for new functionality are welcome and can be sent to 
#         <a href="mailto:info@nordicmicroalgae.org">info@nordicmicroalgae.org</a>
#         </p>
#         """)
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        #
        return layout

