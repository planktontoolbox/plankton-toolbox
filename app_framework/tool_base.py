#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt6 import QtWidgets


class ToolBase(QtWidgets.QDockWidget):
    """
    Abstract base class for tools.
    """

    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(ToolBase, self).__init__(name, parentwidget)
        self._parent = parentwidget
        #
        self._write_to_status_bar("Loading " + name + "...")
        #
        self.setObjectName(name)
        #
        #        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea |
        #                             QtCore.Qt.BottomDockWidgetArea)
        #        self.setBaseSize(600,600)
        # Add specific content. Abstract, implemented by subclasses.
        self._create_content()
        #         # Default position to the right. Hide as default.
        #         self._parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        #         self.hide()
        #  Toggles show/hide from the Tools menu in the main window.
        self._parent.toolsmenu.addAction(self.toggleViewAction())
        #
        self._write_to_status_bar("")

    def _create_content(self):
        """
        Used to create the content of the tool window.
        Note: Abstract. Should be implemented by subclasses.
        """
        pass

    def _create_scrollable_content(self):
        """
        Creates the scrollable part of the tool content.
        Used by subclasses, if needed.
        """
        content = QtWidgets.QWidget()
        widget = QtWidgets.QWidget()
        widget.setMinimumSize(250, 200)
        self.setWidget(widget)
        # Add scroll.
        mainscroll = QtWidgets.QScrollArea()
        ### mainscroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)
        widget.setLayout(mainlayout)

        return content

    def _write_to_status_bar(self, message):
        """Used to write short messages to the main window status bar."""
        self._parent.statusBar().showMessage(message)

    def _write_to_log(self, message):
        """
        Used to write log messages. Depending on the main window
        settings they will appear on different locations, for example
        in log file and/or in the log tool window.
        """
        self._parent.write_to_log(message)

    def show_tool(self):
        """ """
        self.show()
        self.raise_()  # Bring to front.

    def hide_tool(self):
        """ """
        self.hide()
