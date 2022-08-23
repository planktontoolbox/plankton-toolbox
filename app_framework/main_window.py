#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import time
import pathlib
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

import plankton_core
import app_framework
import app_activities
import app_tools
import toolbox_utils


class MainWindow(QtWidgets.QMainWindow):
    """
    Main window for the Desktop application.

    The layout is an activity area in the middle, activity-and-tool-selector to the
    left and movable tools to the right and bottom. Activites are handled as stacked widgets
    and tools are dockable widgets. The activity-and-tool-selector can also be dockable by
    is currently locked.

    Note: Camel case method names are used since the class is inherited from a Qt class.
    """

    def __init__(self):
        """ """
        # Initialize parent.
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr("Plankton Toolbox - Desktop application"))
        # Version.
        self._version = ""
        # Note: Tools menu is public.
        self.toolsmenu = None

    def initialise(self):
        # Load app settings.
        self._ui_settings = QtCore.QSettings()
        # Logging. Always log to plankton_toolbox_log.txt. Use the Log tool when
        # it is available.

        root_dir = app_framework.ToolboxUserSettings().home_for_mac()
        log_path = pathlib.Path(root_dir, "plankton_toolbox_log.txt")
        with log_path.open("w", encoding="cp1252") as f:
            f.write("Plankton Toolbox. " + time.strftime("%Y-%m-%d %H:%M:%S"))
            f.write("\n\n")

        # self._logfile = codecs.open(
        #     "plankton_toolbox_log.txt", mode="w", encoding="cp1252"
        # )
        # self._logfile.write("Plankton Toolbox. " + time.strftime("%Y-%m-%d %H:%M:%S"))
        # self._logfile.write("")

        self._logtool = None  # Should be initiated later.

        toolbox_utils.Logging().set_log_target(self)
        # Setup main window.
        self._createActions()
        self._createMenu()
        self._createStatusBar()
        self._activity = None
        self._createCentralWidget()
        # Set up activities and tools.
        self._toolmanager = app_tools.ToolManager()
        self._toolmanager.set_parent(self)
        self._toolmanager.init_tools()
        #
        toolbox_utils.Logging().log("Plankton Toolbox. Version: " + self._version + ".")
        # Log if user _settings.txt is used.
        data_path = (
            app_framework.ToolboxUserSettings().get_path_to_plankton_toolbox_data()
        )
        counter_path = (
            app_framework.ToolboxUserSettings().get_path_to_plankton_toolbox_counter()
        )
        if (data_path != "plankton_toolbox_data") or (
            counter_path != "plankton_toolbox_counter"
        ):
            toolbox_utils.Logging().log("")
            toolbox_utils.Logging().log(
                'User settings in "plankton_toolbox_data/user_settings.txt": '
            )
            toolbox_utils.Logging().log("- Path to data dictionary: " + str(data_path))
            toolbox_utils.Logging().log(
                "- Path to counter dictionary: " + str(counter_path)
            )
        #
        self._activitymanager = app_activities.ActivityManager()
        self._activitymanager.set_parent(self)
        self._activitymanager.init_activities()
        # Add tools to selector.
        self._create_contentSelectors()
        # Load last used window positions.
        size = self._ui_settings.value(
            "MainWindow/Size", QtCore.QSize(900, 600)
        )  # .toSize()
        position = self._ui_settings.value(
            "MainWindow/Position", QtCore.QPoint(100, 80)
        )  # .toPoint()

        # Check if outside windows. New, including Windows 10.
        # print("DEBUG position x: ", position.x())
        # print("DEBUG position y: ", position.y())
        # print("DEBUG size w: ", size.width())
        # print("DEBUG size h: ", size.height())
        fit_in_screen = False
        screen_x = 0
        screen_y = 0
        screen_width = 1920
        screen_height = 1020
        for screen in QtWidgets.QApplication.screens():
            # print("DEBUG: ", screen.name())
            # print("DEBUG x: ", screen.availableGeometry().x())
            # print("DEBUG y: ", screen.availableGeometry().y())
            # print("DEBUG w: ", screen.availableGeometry().width())
            # print("DEBUG h: ", screen.availableGeometry().height())
            screen_x = screen.availableGeometry().x()
            screen_y = screen.availableGeometry().y()
            screen_width = screen.availableGeometry().width()
            screen_height = screen.availableGeometry().height()
            screen_x_max = screen_x + screen_width
            screen_y_max = screen_y + screen_height

            if ((position.x() + size.width()) <= (screen_x_max + 20)) and (
                (position.y() + size.height()) <= (screen_y_max + 20)
            ):

                if (position.x() >= (screen_x - 20)) and (
                    position.y() >= (screen_y - 20)
                ):
                    fit_in_screen = True
                    break

        if fit_in_screen == False:
            size.setWidth(900)
            size.setHeight(600)
            position.setX(100)
            position.setY(80)

        try:
            self.setGeometry(self._ui_settings.value("MainWindow/Geometry"))
            self.restoreState(self._ui_settings.value("MainWindow/State"))
        except:
            pass  # May contain None at first start on new computer.

        self.resize(size)
        self.move(position)
        # Tell the user.
        app_tools.ToolManager().show_tool_by_name(
            "Toolbox logging"
        )  # Show the log tool if hidden.

        # Load resources when the main event loop has started.
        #         if app_framework.ToolboxSettings().get_value('Resources:Load at startup'):
        #             QtCore.QTimer.singleShot(10, app_framework.ToolboxResources().loadAllResources)
        QtCore.QTimer.singleShot(1000, self._loadResources)

    #        self._loadResources()

    def closeEvent(self, event):
        """Called on application shutdown."""
        # Stores current window positions.
        self._ui_settings.setValue("MainWindow/Size", QtCore.QVariant(self.size()))
        self._ui_settings.setValue("MainWindow/Position", QtCore.QVariant(self.pos()))
        self._ui_settings.setValue("MainWindow/State", self.saveState())
        self._ui_settings.setValue("MainWindow/Geometry", self.geometry())

        # self._logfile.close

    def _createMenu(self):
        """
        The  main menu of the application.
        Note: The Tools menu will be populated by the tool base class. Search
        for 'toggleViewAction' to see the implementation.
        """
        self._filemenu = self.menuBar().addMenu(self.tr("&File"))
        self._filemenu.addSeparator()
        self._filemenu.addAction(self._quitaction)
        #         self._viewmenu = self.menuBar().addMenu(self.tr('&View'))
        self.toolsmenu = self.menuBar().addMenu(
            self.tr("&Extra tools")
        )  # Note: Public.
        self._helpmenu = self.menuBar().addMenu(self.tr("&Help"))
        self._helpmenu.addAction(self._aboutaction)
        # Add sub-menu in the tools menu to hide all tools.
        self._hidealltools = QtGui.QAction(self.tr("Hide all"), self)
        self._hidealltools.setStatusTip(self.tr("Makes all extra tools invisible."))
        self._hidealltools.triggered.connect(self._hideAllTools)
        self.toolsmenu.addAction(self._hidealltools)
        #
        self.toolsmenu.addSeparator()

    def _hideAllTools(self):
        """ """
        tools = self._toolmanager.get_tool_list()
        for tool in tools:
            tool.close()

    def _createStatusBar(self):
        """
        The status bar is located at the bottom of the main window. Tools can
        write messages here by calling <i>_writeToStatusBar</i> located in the
        tool base class.
        """
        self.statusBar().showMessage(self.tr("Plankton Toolbox."))

    def _create_contentSelectors(self):
        """
        The user should be able to choose one activity and a number of tools.
        """
        # Dock widgets can be tabbed with vertical tabs.
        self.setDockOptions(
            QtWidgets.QMainWindow.DockOption.AnimatedDocks
            | QtWidgets.QMainWindow.DockOption.AllowTabbedDocks
            | QtWidgets.QMainWindow.DockOption.VerticalTabs
        )
        # Create left dock widget and dock to main window.
        #         dock = QtWidgets.QDockWidget(self.tr(' Tool selector '), self)
        dock = QtWidgets.QDockWidget(self.tr(" Activities: "), self)
        dock.setObjectName("Activities and tools selector")
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        # dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
        #                  QtWidgets.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        # Widget to create space and layout for two groupboxes.
        content = QtWidgets.QWidget()
        widget = QtWidgets.QWidget()
        widget.setStyleSheet(
            """        
            QDockWidget .QWidget { background-color: white; }
            """
        )
        dock.setWidget(widget)
        # Add scroll.
        mainscroll = QtWidgets.QScrollArea()
        ### mainscroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)

        self.test_mainscroll = mainscroll

        widget.setLayout(mainlayout)
        grid1 = QtWidgets.QVBoxLayout()
        content.setLayout(grid1)
        # Frame for activites.
        activitiesgroup = QtWidgets.QFrame()
        grid1.addWidget(activitiesgroup)
        activitiesvbox = QtWidgets.QVBoxLayout()
        activitiesgroup.setLayout(activitiesvbox)
        # Groupbox for tools.
        toolsgroup = QtWidgets.QGroupBox("Extra tools:")
        grid1.addWidget(toolsgroup)
        toolsvbox = QtWidgets.QVBoxLayout()
        toolsgroup.setLayout(toolsvbox)
        grid1.addStretch(5)

        # Add one button for each activity. Create stacked widgets.
        for activity in self._activitymanager.get_activity_list():
            button = app_framework.ActivityMenuQLabel(" " + activity.objectName())
            activity.set_main_menu_button(button)
            activitiesvbox.addWidget(button)  # Adds to stack.
            # The activity is called to select stack item by object, not index.
            button.activity_menu_label_clicked.connect(button.markAsSelected)
            button.activity_menu_label_clicked.connect(activity.show_in_main_window)
            # Create one layer in the stacked activity widget.
            self._activitystack.addWidget(activity)
        #
        activitiesvbox.addStretch(5)
        # Add one button for each tool.
        for tool in self._toolmanager.get_tool_list():
            button = app_framework.ClickableQLabel(" " + tool.objectName())
            button_hide = app_framework.ClickableQLabel(" (hide)")
            showhidehbox = QtWidgets.QHBoxLayout()
            showhidehbox.addWidget(button)
            showhidehbox.addWidget(button_hide)
            showhidehbox.addStretch(10)
            toolsvbox.addLayout(showhidehbox)
            button.label_clicked.connect(tool.show_tool)
            button_hide.label_clicked.connect(tool.hide_tool)
        #
        # Button to hide all tools.
        button = app_framework.ClickableQLabel(" (Hide all)")
        toolsvbox.addWidget(button)
        button.label_clicked.connect(self._hideAllTools)
        #
        toolsvbox.addStretch(10)
        # Activate startup activity. Select the first one in list.
        activities = self._activitymanager.get_activity_list()
        if len(activities) > 0:
            activities[0].show_in_main_window()

        # DEBUG: During development...

    ###        activities[1].show_in_main_window()

    def showActivity(self, activity):
        """ """
        ###        self._activityheader.setText('<b>' + activity.objectName() + '</b>')
        self._activitystack.setCurrentWidget(activity)
        # Mark left menu item as  active.
        if activity.get_main_menu_button():
            activity.get_main_menu_button().markAsSelected()

    def show_activity_by_name(self, activity_name):
        """ """
        for activity in self._activitymanager.get_activity_list():
            if activity.objectName() == activity_name:
                self.showActivity(activity)
                return

    def _createCentralWidget(self):
        """
        The central widget contains the selected activity. It is implemented as
        stacked layout, QStackedLayout, where the pages are selected from
        the activities group box.
        """
        ###        self._activityheader = QtWidgets.QLabel('<b>Activity not selected...</b>", self)
        ###        self._activityheader.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self._activitystack = QtWidgets.QStackedLayout()
        # Layout widgets.
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        ###        layout.addWidget(self._activityheader)
        layout.addLayout(self._activitystack)
        # Dummy stack content.
        dummy = QtWidgets.QWidget(self)
        self._activitystack.addWidget(dummy)

    def _createActions(self):
        """Common application related actions."""
        self._quitaction = QtGui.QAction(self.tr("&Quit"), self)
        self._quitaction.setShortcut(self.tr("Ctrl+Q"))
        self._quitaction.setStatusTip(self.tr("Quit the application"))
        self._quitaction.triggered.connect(self.close)
        #
        self._aboutaction = QtGui.QAction(self.tr("&About"), self)
        self._aboutaction.setStatusTip(self.tr("Show the application's About box"))
        self._aboutaction.triggered.connect(self._about)

    def write_to_log(self, message):
        """Log to file and to the log tool when available."""
        #        self.console.addItem(message)
        try:

            root_dir = app_framework.ToolboxUserSettings().home_for_mac()
            log_path = pathlib.Path(root_dir, "plankton_toolbox_log.txt")
            with log_path.open("a", encoding="cp1252") as f:
                f.write(message + "\r\n")
            # self._logfile.write(message + "\r\n")
            # self._logfile.flush()

            # Search for the console tool. Note: Not available during startup.
            if not self._logtool:
                for tool in self._toolmanager.get_tool_list():
                    if type(tool) == app_tools.LogTool:
                        self._logtool = tool
            # Log message.
            if self._logtool:
                self._logtool.write_to_log(message)
        #
        except Exception as e:
            print("Exception (write_to_log):", str(e))

    def _loadResources(self):
        """ """
        try:
            # Load resources here.
            self.statusBar().showMessage(self.tr("Loading species lists..."))
            plankton_core.Species()

        finally:
            self.statusBar().showMessage(self.tr(""))

    def setVersion(self, version):
        """ """
        self._version = version

    def _about(self):
        """ """
        about_text = app_framework.HelpTexts().get_text("about")
        about_text = about_text.replace("###version###", " Version: " + self._version)

        QtWidgets.QMessageBox.about(self, self.tr("About"), self.tr(about_text))
