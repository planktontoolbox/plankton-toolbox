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
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import envmonlib

class ScreeningActivity(activity_base.ActivityBase):
    """ Used for screening of loaded datasets content. """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(ScreeningActivity, self).__init__(name, parentwidget)

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
        contentLayout.addWidget(self._contentScreeningTabs())

    def _contentScreeningTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._contentCodeListScreening(), "Code lists")
        tabWidget.addTab(self._contentSpeciesScreening(), "Species")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def _contentCodeListScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._codelistscreening_button = QtGui.QPushButton("Code list screening")
        self.connect(self._codelistscreening_button, QtCore.SIGNAL("clicked()"), self._codeListScreening)                
        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._codelistscreening_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def _contentSpeciesScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._speciesscreening_button = QtGui.QPushButton("Species screening")
        self.connect(self._speciesscreening_button, QtCore.SIGNAL("clicked()"), self._speciesScreening)                
        self._bvolscreening_button = QtGui.QPushButton("BVOL screening")
        self.connect(self._bvolscreening_button, QtCore.SIGNAL("clicked()"), self._bvolScreening)                
        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._speciesscreening_button)
        hbox1.addWidget(self._bvolscreening_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def _codeListScreening(self):
        """ """
        #
        screeningmanager = envmonlib.ScreeningManager()
        #
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log("Screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Screening in progress...")
            #
            codetypes_set = set()
            #
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                self._writeToStatusBar(u"Screening in progress (" + dataset.getMetadata(u'File name') + u")...")
                #
                for visitnode in dataset.getChildren():
                    #
                    data_dict = visitnode.getDataDict()
                    for key in data_dict:
                        if key in screeningmanager.getCodeTypes():
                            codetypes_set.add(key)
                            if data_dict[key] not in screeningmanager.getCodes(key):
                                envmonlib.Logging().warning(u"Visit level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
#                                print(u"Visit level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
                    #
                    for samplenode in visitnode.getChildren():
                        #
                        data_dict = samplenode.getDataDict()
                        for key in data_dict:
                            if key in screeningmanager.getCodeTypes():
                                codetypes_set.add(key)
                                if data_dict[key] not in screeningmanager.getCodes(key):
                                    envmonlib.Logging().warning(u"Visit level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
#                                    print(u"Sample level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
                        #                        
                        for variablenode in samplenode.getChildren():
                            #
                            data_dict = variablenode.getDataDict()
                            for key in data_dict:
                                if key in screeningmanager.getCodeTypes():
                                    codetypes_set.add(key)
                                    if data_dict[key] not in screeningmanager.getCodes(key):
                                        envmonlib.Logging().warning(u"Visit level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
#                                        print(u"Variable level. Code is not valid. Code type: " + unicode(key) + u" Code: " + unicode(data_dict[key]))
     
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log("Screening was done on these code types: " + 
                                    unicode(sorted(codetypes_set)))
            envmonlib.Logging().log("Screening done.\r\n")
            self._writeToStatusBar("")

    def _speciesScreening(self):
        """ """
        #
        species = envmonlib.Species()
        #
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log("Screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Screening in progress...")
            #
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                self._writeToStatusBar(u"Screening in progress (" + dataset.getMetadata(u'File name') + u")...")
                #
                for visitnode in dataset.getChildren():
                    #
                    for samplenode in visitnode.getChildren():
                        #
                        for variablenode in samplenode.getChildren():
                            #
                            data_dict = variablenode.getDataDict()
                            if u'Taxon name' in data_dict:
                                if data_dict[u'Taxon name'] not in species.getTaxaLookupDict():
                                    envmonlib.Logging().warning(u"Taxon name not in species list. Taxon name: " + unicode(data_dict[u'Taxon name']))
     
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"Screening done.\r\n")
            self._writeToStatusBar("")

    def _bvolScreening(self):
        """ """
        #
        species = envmonlib.Species()
        #
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log("Screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Screening in progress...")
            #
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                self._writeToStatusBar(u"Screening in progress (" + dataset.getMetadata(u'File name') + u")...")
                #
                for visitnode in dataset.getChildren():
                    #
                    for samplenode in visitnode.getChildren():
                        #
                        for variablenode in samplenode.getChildren():
                            #
                            data_dict = variablenode.getDataDict()
                            if (u'Taxon name' in data_dict) and (u'Size class' in data_dict):
                                taxonname = data_dict[u'Taxon name']
                                sizeclass = data_dict[u'Size class'] 
                                
                                if species.getBvolValue(taxonname, sizeclass, u'Size class') == None:
                                    envmonlib.Logging().warning(u"Taxon name/size clas not in BVOL list. Taxon name: " + unicode(taxonname) + u" Size class: " + unicode(sizeclass))
     
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"Screening done.\r\n")
            self._writeToStatusBar("")

