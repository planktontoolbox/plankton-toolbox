#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt6 import QtGui
from PyQt6 import QtWidgets

# from PyQt6 import QtCore
from abc import abstractmethod


class ActivityBase(QtWidgets.QWidget):
    """
    Abstract base class for activities.
    """

    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(ActivityBase, self).__init__(parentwidget)
        self._parent = parentwidget
        self._mainmenubutton = None
        #
        self._write_to_status_bar("Loading " + name + "...")
        #
        self.setObjectName(name)
        # Add specific content. Abstract, implemented by subclasses.
        self._create_content()
        #
        self._write_to_status_bar("")

    def set_main_menu_button(self, button):
        """ """
        self._mainmenubutton = button

    def get_main_menu_button(self):
        """ """
        return self._mainmenubutton

    def show_in_main_window(self):
        """ """
        self._parent.showActivity(self)

    @abstractmethod
    def _create_content(self):
        """
        Used to create the content of the activity window.
        Note: Abstract. Should be implemented by subclasses.
        """
        pass

    def _create_scrollable_content(self):
        """
        Creates the scrollable part of the activity content.
        Used by subclasses, if needed.
        """
        content = QtWidgets.QWidget()
        # Add scroll.
        mainscroll = QtWidgets.QScrollArea()
        ### mainscroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)
        return content

    def _write_to_status_bar(self, message):
        """Used to write short messages to the main window status bar."""
        self._parent.statusBar().showMessage(message)

    def _write_to_log(self, message):
        """
        Used to write log messages. Depending on the main window
        settings they will appear on different locations, for example
        in log file and/or in the Log tool window.
        """
        self._parent.write_to_log(message)
