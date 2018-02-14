#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.toolbox.help_texts as help_texts

import toolbox_utils
import plankton_core

class StartActivity(activity_base.ActivityBase):
    """
    This activity is "a welcome page" with some possibilities to set up the environment.
    """
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(StartActivity, self).__init__(name, parentwidget)

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addLayout(self._content_welcome())
        contentLayout.addStretch(5)

    def _content_welcome(self):
        """ """
        # Active widgets and connections.
        label = app_framework.RichTextQLabel()
#         label.setText(help_texts.HelpTexts().get_text('StartActivity_intro_1'))
        label.setText(help_texts.HelpTexts().get_text('start_activity_intro'))
        # Layout.
        layout = QtWidgets.QGridLayout()
        gridrow = 0
        layout.addWidget( QtWidgets.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(QtWidgets.QLabel(''), gridrow, 1, 1, 20)
        #
        return layout

