#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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
This activity is "a welcome page" with some possibilities to set up the environment.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base

class StartActivity(activity_base.ActivityBase):
    """
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
        self.__activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self.__activityheader.setTextFormat(QtCore.Qt.RichText)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self.__activityheader.setStyleSheet(""" 
            * { color: #00677f; background-color: #eaa97e; }
            """)
        contentLayout.addWidget(self.__activityheader)
        # Add content to the activity.
        contentLayout.addLayout(self.__contentWelcome())
        contentLayout.addLayout(self.__contentActivities())
        contentLayout.addLayout(self.__contentGetDataFromNordicMicroalgae())
        contentLayout.addStretch(5)

    def __contentWelcome(self):
        """ """
        # Active widgets and connections.
        label = QtGui.QLabel()
        label.setTextFormat(QtCore.Qt.RichText)
        label.setText("""
        <br/>
        <h3>Welcome to the Plankton Toolbox.</h3>
        Plankton Toolbox contains a set of tool to be used when working with aquatic micro-organism.
        <br/>
        The Plankton Toolbox is still under development.
        """)

        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        gridrow += 1

        #
        return layout

    def __contentActivities(self):
        """ """
        # Active widgets and connections.
        label1 = QtGui.QLabel()
        label1.setTextFormat(QtCore.Qt.RichText)
        label1.setText("""
        <br/>
        <h4>Activities</h4>
        Activities are... 
         
        """)
        
        createdatasetbutton = utils_qt.ClickableQLabel("- Create dataset.")
        loaddatasetsbutton = utils_qt.ClickableQLabel("- Load datasets.")
        analysedatasetsbutton = utils_qt.ClickableQLabel("- Analyse datasets.")
        createreportsbutton = utils_qt.ClickableQLabel("- Create reports.")
        managespecieslistsbutton = utils_qt.ClickableQLabel("- Prepare resources.")
            
        self.connect(createdatasetbutton, QtCore.SIGNAL("clicked()"), self.__gotoCreateDataset)
        self.connect(loaddatasetsbutton, QtCore.SIGNAL("clicked()"), self.__gotoLoadDatasets)
        self.connect(analysedatasetsbutton, QtCore.SIGNAL("clicked()"), self.__gotoAnalyseDatasets)
        self.connect(createreportsbutton, QtCore.SIGNAL("clicked()"), self.__gotoCreateReports)
        self.connect(managespecieslistsbutton, QtCore.SIGNAL("clicked()"), self.__gotoManageSpeciesLists)

        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label1, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(createdatasetbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(loaddatasetsbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(analysedatasetsbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(createreportsbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(managespecieslistsbutton, gridrow, 1, 1, 20)
        gridrow += 1
        #
        return layout

    def __gotoCreateDataset(self):
        self._parent.showActivityByName('(Create dataset)')
    
    def __gotoLoadDatasets(self):
        self._parent.showActivityByName('Load datasets')
    
    def __gotoAnalyseDatasets(self):
        self._parent.showActivityByName('(Analyse datasets)')
    
    def __gotoCreateReports(self):
        self._parent.showActivityByName('Create reports')
    
    def __gotoManageSpeciesLists(self):
        self._parent.showActivityByName('Manage species lists')
    
    def __contentGetDataFromNordicMicroalgae(self):
        """ """
        # Active widgets and connections.
        label1 = QtGui.QLabel()
        label1.setTextFormat(QtCore.Qt.RichText)
        label1.setOpenExternalLinks(True) 
        label1.setText("""
        <br/>
        <h4>Nordic Microalgae.</h4>
        Species lists and other data can automatically be imported from the web application <br/>
        Nordic Microalgae, 
        <a href="http://nordicmicroalgae.org">http://nordicmicroalgae.org</a> 
        """)
        label2 = QtGui.QLabel()
        label2.setTextFormat(QtCore.Qt.RichText)
        label2.setOpenExternalLinks(True) 
        label2.setText("""
        Currently there are no species data or images loaded.</a> 
        """)
        
        clearspeciesbutton = utils_qt.ClickableQLabel("- Clear loaded species data.")
        loadspeciesbutton = utils_qt.ClickableQLabel("- Load species from Nordic Microalgae.")
        clearimagesbutton = utils_qt.ClickableQLabel("- Clear loaded image data.")
        loadimagesbutton = utils_qt.ClickableQLabel("- Load species images from Nordic Microalgae.")
        
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label1, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(label2, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(clearspeciesbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(loadspeciesbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(clearimagesbutton, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(loadimagesbutton, gridrow, 1, 1, 20)
        gridrow += 1

        #
        return layout

    def __test(self):
        """ """
        utils.Logger().log("Name: " + unicode(self.__emailedit.text()))
        