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
import plankton_toolbox.tools.tool_base as tool_base
import envmonlib

import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
#import plankton_toolbox.toolbox.toolbox_main_window as toolbox_main_window


class DevTestTool(tool_base.ToolBase):
    """
    For development and test only. Deactivate in public releases.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DevTestTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentButtons())
        contentLayout.addStretch(5)

    def _contentButtons(self):
        """ """
        # Active widgets and connections.
        self._testbutton_1 = QtGui.QPushButton("Test 1")
        self.connect(self._testbutton_1, QtCore.SIGNAL("clicked()"), self._test_1)                
        self._testbutton_2 = QtGui.QPushButton("Test 2")
        self.connect(self._testbutton_2, QtCore.SIGNAL("clicked()"), self._test_2)                
        self._testbutton_3 = QtGui.QPushButton("Test 3")
        self.connect(self._testbutton_3, QtCore.SIGNAL("clicked()"), self._test_3)                
        self._testbutton_4 = QtGui.QPushButton("Test 4")
        self.connect(self._testbutton_4, QtCore.SIGNAL("clicked()"), self._test_4)                
        self._testbutton_5 = QtGui.QPushButton("Test 5")
        self.connect(self._testbutton_5, QtCore.SIGNAL("clicked()"), self._test_5)                
        # Layout.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._testbutton_1)
        layout.addWidget(self._testbutton_2)
        layout.addWidget(self._testbutton_3)
        layout.addWidget(self._testbutton_4)
        layout.addWidget(self._testbutton_5)
        layout.addStretch(5)
        #
        return layout

    def _test_1(self):
        """ """
        envmonlib.Logging().log("Button Test 1")
        
        self._parent.showActivityByName(u'Load datasets')
        
       # Set up for import file parsing.
        impMgr = envmonlib.ImportManager(u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/' + 
                                         u'sharkweb_phytoplankton_parser.xlsx',
                                         u'PP Sharkweb download en',
                                         u'PP export 1')
        # Import and parse file.
        dataset = impMgr.importTextFile(u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/' +
                                        u'shark_data_å17_2008 maj-sept.txt',
                                        u'utf8')
        # Add metadata related to imported file.
        dataset.addMetadata(u'Parser', u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/' + 
                                       u'sharkweb_phytoplankton_parser.xlsx')
        dataset.addMetadata(u'File name', u'TEST')
        dataset.addMetadata(u'File path', u'TEST')
        dataset.addMetadata(u'Import column', u'PP Sharkweb download en')
        dataset.addMetadata(u'Export column', u'PP export 1')
        toolbox_datasets.ToolboxDatasets().addDataset(dataset)
        
        
#    def _loadTextFiles(self):
#        """ """
#        try:
#            envmonlib.Logging().log(u"") # Empty line.
#            envmonlib.Logging().log(u"Loading datasets...")
#            envmonlib.Logging().startAccumulatedLogging()
#            self._writeToStatusBar(u"Loading datasets...")
#            # Show select file dialog box. Multiple files can be selected.
#            namefilter = 'Text files (*.txt);;All files (*.*)'
#            filenames = QtGui.QFileDialog.getOpenFileNames(
#                                self,
#                                'Load dataset(s)',
#                                self._last_used_textfile_name,
#                                namefilter)
#            # From QString to unicode.
#            filenames = map(unicode, filenames)
#            # Check if user pressed ok or cancel.
#            self._tabledataset = envmonlib.DatasetTable()
#            if filenames:
#                for filename in filenames:
#                    # Store selected path. Will be used as default next time.
#                    self._last_used_textfile_name = filename
#                    # Text files may have strange encodings.
#                    if unicode(self._textfile_encoding_list.currentText()) == u'<platform default>':
#                        textfileencoding = locale.getpreferredencoding()
#                    else:
#                        textfileencoding = unicode(self._textfile_encoding_list.currentText())                        
#                    # Set up for import file parsing.
#                    impMgr = envmonlib.ImportManager(self._parser_path + unicode(self._textfile_parser_list.currentText()),
#                                                     unicode(self._textfile_importcolumn_list.currentText()),
#                                                     unicode(self._textfile_exportcolumn_list.currentText()))
#                    # Import and parse file.
#                    dataset = impMgr.importTextFile(filename, textfileencoding)
#                    # Add metadata related to imported file.
#                    dataset.addMetadata(u'Parser', self._parser_path + unicode(self._textfile_parser_list.currentText()))
#                    dataset.addMetadata(u'File name', os.path.basename(filename))
#                    dataset.addMetadata(u'File path', filename)
#                    dataset.addMetadata(u'Import column', unicode(self._textfile_importcolumn_list.currentText()))
#                    dataset.addMetadata(u'Export column', unicode(self._textfile_exportcolumn_list.currentText()))
#                    # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
#                    toolbox_datasets.ToolboxDatasets().addDataset(dataset)

        
        
        
        
        

    def _test_2(self):
        """ """
        envmonlib.Logging().log("Button Test 2")

    def _test_3(self):
        """ """
        envmonlib.Logging().log("Button Test 3")

    def _test_4(self):
        """ """
        envmonlib.Logging().log("Button Test 4")

    def _test_5(self):
        """ """
        envmonlib.Logging().log("Button Test 5")
