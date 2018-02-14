#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from matplotlib import path
from matplotlib import pyplot
import numpy as np
 
# import cartopy.crs as ccrs
# from cartopy.io.img_tiles import OSM

import app_framework

class TemplateTool(app_framework.ToolBase):
    """
    Template class for new tools.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(TemplateTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | 
                             QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)        
        # Default position. Hide as default.
        self._parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.hide()

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_person_info())
        contentLayout.addLayout(self._content_buttons())
        contentLayout.addStretch(5)

    def _content_person_info(self):
        """ """
        # Active widgets and connections.
        self._nameedit = QtWidgets.QLineEdit('<Name>')
        self._emailedit = QtWidgets.QLineEdit('<Email>')
        self._customerlist = QtWidgets.QListWidget()
        # Layout.
        layout = QtWidgets.QFormLayout()
        layout.addRow('&Name:', self._nameedit)
        layout.addRow('&Email:', self._emailedit)
        layout.addRow('&Projects:', self._customerlist)
        # Test data.
        self._customerlist.addItem('<First project.>')
        self._customerlist.addItem('<Second project.>')
        #
        return layout

    def _content_buttons(self):
        """ """
        # Active widgets and connections.
        self._testbutton = QtWidgets.QPushButton('Write to log')
        self._testbutton.clicked._test)                
        # Layout.
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self._testbutton)
        #
        return layout

    def _test(self):
        """ """
        app_framework.Logging().log('Name: ' + str(self._emailedit.text()))

