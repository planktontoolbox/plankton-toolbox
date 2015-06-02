#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
#         contentLayout.addLayout(self._contentUsage())
#         contentLayout.addLayout(self._contentPreloaded())
#         contentLayout.addLayout(self._contentUnderDevelopment())
        contentLayout.addStretch(5)

    def _contentWelcome(self):
        """ """
        # Active widgets and connections.
        label = utils_qt.RichTextQLabel()
#         label.setText(help_texts.HelpTexts().getText('StartActivity_intro_1'))
        label.setText(help_texts.HelpTexts().getText('StartActivity_intro'))
        # Layout.
        layout = QtGui.QGridLayout()
        gridrow = 0
        layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
        layout.addWidget(label, gridrow, 1, 1, 20)
        gridrow += 1
        layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
        #
        return layout

#     def _contentUsage(self):
#         """ """
#         # Active widgets and connections.
#         label = utils_qt.RichTextQLabel()
#         label.setText(help_texts.HelpTexts().getText('StartActivity_intro_2'))
#         # Layout.
#         layout = QtGui.QGridLayout()
#         gridrow = 0
#         layout.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
#         layout.addWidget(label, gridrow, 1, 1, 20)
#         gridrow += 1
#         layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
#         #
#         return layout
# 
#     def _contentPreloaded(self):
#         """ """
#         # Active widgets and connections.
#         label = utils_qt.RichTextQLabel()
#         label.setText(help_texts.HelpTexts().getText('StartActivity_intro_3'))
#         # Layout.
#         layout = QtGui.QGridLayout()
#         gridrow = 0
#         layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
#         layout.addWidget(label, gridrow, 1, 1, 20)
#         gridrow += 1
#         layout.addWidget(QtGui.QLabel(''), gridrow, 1, 1, 20)
#         #
#         return layout
# 
#     def _contentUnderDevelopment(self):
#         """ """
#         # Active widgets and connections.
#         label = utils_qt.RichTextQLabel()
#         label.setText(help_texts.HelpTexts().getText('StartActivity_intro_4'))
#         # Layout.
#         layout = QtGui.QGridLayout()
#         gridrow = 0
#         layout.addWidget( QtGui.QLabel(''), gridrow, 0, 1, 1) # Add space to the left.
#         layout.addWidget(label, gridrow, 1, 1, 20)
#         #
#         return layout

