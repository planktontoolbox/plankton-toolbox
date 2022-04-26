#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore

import app_framework
import toolbox_utils


class TaxonImagesTool(app_framework.ToolBase):
    """ """

    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other
        # initialization since the base class calls _create_content().
        super(TaxonImagesTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
        self.setBaseSize(600, 600)

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_image())
        contentLayout.addStretch(5)

    def _content_image(self):
        """ """
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("<b><i>Incertae sedis</i></b>")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        imagelabel = QtWidgets.QLabel()
        imagelabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        image = QtGui.QImage("../planktondata/cache/images/Incertae_sedis.jpg")
        imagelabel.setPixmap(QtGui.QPixmap.fromImage(image))
        layout.addWidget(label)
        layout.addWidget(imagelabel)
        #
        return layout

    def _test(self):
        """ """
        try:
            self._write_to_log("Name: " + str(self._nameedit.text()))
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error("Exception: (" + debug_info + "): " + str(e))
