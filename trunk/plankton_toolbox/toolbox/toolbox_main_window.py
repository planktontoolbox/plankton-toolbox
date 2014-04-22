#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import time
import codecs
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import envmonlib
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.activities.activity_manager as activity_manager
import plankton_toolbox.tools.log_tool as log_tool
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
#import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

__version__ = '?? April 2014' # Plankton Toolbox version.

class MainWindow(QtGui.QMainWindow):
    """
    Main window for the Plankton Toolbox.
    
    The layout is an activity area in the middle, activity-and-tool-selector to the
    left and movable tools to the right and bottom. Activites are handled as stacked widgets 
    and tools are dockable widgets. The activity-and-tool-selector can also be dockable by 
    is currently locked.
    """
    def __init__(self):
        """ """
        # Initialize parent.
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr("Plankton Toolbox"))
        # Note: Tools menu is public.
        self.toolsmenu = None
        # Load toolbox settings.
        self._ui_settings = QtCore.QSettings()
        toolbox_settings.ToolboxSettings().loadSettings(self._ui_settings)
        # Logging. Always log to plankton_toolbox_log.txt. Use the Log tool when  
        # it is available.
        txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
        self._logfile = codecs.open('plankton_toolbox_log.txt', mode = 'w', encoding = txtencode)
        self._logfile.write(u"Plankton Toolbox. " +
                             time.strftime("%Y-%m-%d %H:%M:%S") )
        self._logfile.write(u"")
        self._logtool = None # Should be initiated later.
        envmonlib.Logging().setLogTarget(self)
        # Setup main window.
        self._createActions()
        self._createMenu()
        self._createStatusBar()
        self._activity = None
        self._createCentralWidget()
        # Set up activities and tools.
        self._toolmanager = tool_manager.ToolManager()
        self._toolmanager.setParent(self)
        self._toolmanager.initTools()
        self._activitymanager = activity_manager.ActivityManager()
        self._activitymanager.setParent(self)
        self._activitymanager.initActivities()
        # Add tools to selector.
        self._createContentSelectors()
        # Loads last used window positions.
        self.setGeometry(self._ui_settings.value("MainWindow/Geometry").toRect())
        self.restoreState(self._ui_settings.value("MainWindow/State").toByteArray())        
        size = self._ui_settings.value("MainWindow/Size", QtCore.QVariant(QtCore.QSize(900, 600))).toSize()
        position = self._ui_settings.value("MainWindow/Position", QtCore.QVariant(QtCore.QPoint(100, 50))).toPoint()
        self.resize(size)
        self.move(position)        
        # Tell the user.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging') # Show the log tool if hidden.
        envmonlib.Logging().log(u"Welcome to the Plankton Toolbox.")
        envmonlib.Logging().log(u"Note: Log rows are both sent to the 'Toolbox logging' tool and written to the text file 'plankton_toolbox_log.txt'.")
        # Load resources when the main event loop has started.
#        if toolbox_settings.ToolboxSettings().getValue('Resources:Load at startup'):
#            QtCore.QTimer.singleShot(10, toolbox_resources.ToolboxResources().loadAllResources)
        QtCore.QTimer.singleShot(100, self._loadResources)
        
    def closeEvent(self, event):
        """ Called on application shutdown. """
        # Stores current window positions.
        self._ui_settings.setValue("MainWindow/Size", QtCore.QVariant(self.size()))
        self._ui_settings.setValue("MainWindow/Position", QtCore.QVariant(self.pos()))
        self._ui_settings.setValue("MainWindow/State", self.saveState())
        self._ui_settings.setValue("MainWindow/Geometry", self.geometry())
        self._logfile.close
        # Save toolbox settings.
        toolbox_settings.ToolboxSettings().saveSettings(self._ui_settings)
    
    def _createMenu(self):
        """ 
        The  main menu of the application. 
        Note: The Tools menu will be populated by the tool base class. Search
        for 'toggleViewAction' to see the implementation.
        """
        self._filemenu = self.menuBar().addMenu(self.tr("&File"))
        self._filemenu.addSeparator()
        self._filemenu.addAction(self._quitaction)
        self._viewmenu = self.menuBar().addMenu(self.tr("&View"))
        self.toolsmenu = self.menuBar().addMenu(self.tr("&Tools")) # Note: Public.
        self._helpmenu = self.menuBar().addMenu(self.tr("&Help"))
        self._helpmenu.addAction(self._aboutaction)
        # Add sub-menu in the tools menu to hide all tools.
        self._hidealltools = QtGui.QAction(self.tr("Hide all tools"), self)
        self._hidealltools.setStatusTip(self.tr("Make all tools invisible."))
        self._hidealltools.triggered.connect(self._hideAllTools)
        self.toolsmenu.addAction(self._hidealltools)
        #
        self.toolsmenu.addSeparator()
        
    def _hideAllTools(self):
        """ """
        tools = self._toolmanager.getToolList()
        for tool in tools:
            tool.close()

    def _createStatusBar(self):
        """ 
        The status bar is located at the bottom of the main window. Tools can
        write messages here by calling <i>_writeToStatusBar</i> located in the 
        tool base class.
        """
        self.statusBar().showMessage(self.tr("Plankton Toolbox."))

    def _createContentSelectors(self):
        """ 
        The user should be able to choose one activity and a number of tools.
        """
        # Dock widgets can be tabbed with vertical tabs.
        self.setDockOptions(QtGui.QMainWindow.AnimatedDocks | 
                            QtGui.QMainWindow.AllowTabbedDocks | 
                            QtGui.QMainWindow.VerticalTabs)
        # Create left dock widget and dock to main window.
        dock = QtGui.QDockWidget(self.tr(" Main menu "), self)
        dock.setObjectName("Activities and tools selector")
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        # dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | 
        #                  QtGui.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        # Widget to create space and layout for two groupboxes.
        content = QtGui.QWidget()
        widget = QtGui.QWidget()
        widget.setStyleSheet("""        
            QDockWidget .QWidget { background-color: white; }
            """)
        dock.setWidget(widget)        
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        ### mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.setMargin(0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)
        
        self.test_mainscroll = mainscroll
        
        widget.setLayout(mainlayout)
        grid1 = QtGui.QVBoxLayout()
        content.setLayout(grid1)        
        # Frame for activites.        
        activitiesgroup = QtGui.QFrame()
        grid1.addWidget(activitiesgroup)
        activitiesvbox = QtGui.QVBoxLayout()
        activitiesgroup.setLayout(activitiesvbox)
        # Groupbox for tools.
        toolsgroup = QtGui.QGroupBox("Tools")
        grid1.addWidget(toolsgroup)        
        toolsvbox = QtGui.QVBoxLayout()
        toolsgroup.setLayout(toolsvbox)
        grid1.addStretch(5)
        # Add one button for each activity. Create stacked widgets.
        for activity in self._activitymanager.getActivityList():
            button = utils_qt.ActivityMenuQLabel(u' ' + activity.objectName())
            activity.setMainMenuButton(button)
            activitiesvbox.addWidget(button) # Adds to stack.                  
            # The activity is called to select stack item by object, not index.
            self.connect(button, QtCore.SIGNAL("clicked()"), button.markAsSelected)
            self.connect(button, QtCore.SIGNAL("clicked()"), activity.showInMainWindow)
            # Create one layer in the stacked activity widget.
            self._activitystack.addWidget(activity)
        activitiesvbox.addStretch(5)
        # Add one button for each tool.
        for tool in self._toolmanager.getToolList():
            button = utils_qt.ClickableQLabel(u' ' + tool.objectName())
            toolsvbox.addWidget(button)
            self.connect(button, QtCore.SIGNAL("clicked()"), tool.show) # Show if hidden.
            self.connect(button, QtCore.SIGNAL("clicked()"), tool.raise_) # Bring to front.
        toolsvbox.addStretch(5)
        # Activate startup activity. Select the first one in list.
        activities = self._activitymanager.getActivityList()
        if len(activities) > 0:
            activities[0].showInMainWindow()

    def showActivity(self, activity):
        """ """
###        self._activityheader.setText('<b>' + activity.objectName() + '</b>')
        self._activitystack.setCurrentWidget(activity)
        # Mark left menu item as  active. 
        if activity.getMainMenuButton():
            activity.getMainMenuButton().markAsSelected()

    def showActivityByName(self, activity_name):
        """ """
        for activity in self._activitymanager.getActivityList():
            if activity.objectName() == activity_name:
                self.showActivity(activity)
                return
    
    def _createCentralWidget(self):
        """ 
        The central widget contains the selected activity. It is implemented as
        stacked layout, QStackedLayout, where the pages are selected from
        the activities group box. 
        """
###        self._activityheader = QtGui.QLabel("<b>Activity not selected...</b>", self)
###        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self._activitystack = QtGui.QStackedLayout()        
        # Layout widgets.
        widget = QtGui.QWidget(self) 
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
###        layout.addWidget(self._activityheader)
        layout.addLayout(self._activitystack)
        # Dummy stack content.
        dummy = QtGui.QWidget(self)
        self._activitystack.addWidget(dummy)
       
    def _createActions(self):
        """ Common application related actions. """
        self._quitaction = QtGui.QAction(self.tr("&Quit"), self)
        self._quitaction.setShortcut(self.tr("Ctrl+Q"))
        self._quitaction.setStatusTip(self.tr("Quit the application"))
        self._quitaction.triggered.connect(self.close)
        #
        self._aboutaction = QtGui.QAction(self.tr("&About"), self)
        self._aboutaction.setStatusTip(self.tr("Show the application's About box"))
        self._aboutaction.triggered.connect(self._about)

    def writeToLog(self, message):
        """ Log to file and to the log tool when available. """
#        self.console.addItem(message)
        self._logfile.write(message + '\r\n')
        self._logfile.flush()        
        # Search for the console tool. Note: Not available during startup.
        if not self._logtool:
            for tool in self._toolmanager.getToolList():
                if type(tool) == log_tool.LogTool:
                    self._logtool = tool
        # Log message.                   
        if self._logtool: self._logtool.writeToLog(message)

    def _loadResources(self):
        """ """
        try:
            self.statusBar().showMessage(self.tr("Loading species lists..."))
            envmonlib.Species() # Load species files.
        finally:
            self.statusBar().showMessage(self.tr(""))            

    def _about(self):
        """ """
        QtGui.QMessageBox.about(self, self.tr("About Plankton Toolbox"),
                self.tr(
"""
<p>
<b>Plankton Toolbox</b> version %s
</p>
<p>
The Plankton Toolbox is a free tool for aquatic scientists, and others, 
working with environmental monitoring related to phyto- and zooplankton.
</p>
<p>
The software is under development and provided free with no 
guarantees regarding functionality. Comments, bug reports and requests 
for new functionality are welcome and can be sent to 
<a href="mailto:info@nordicmicroalgae.org">info@nordicmicroalgae.org</a>
</p>
<p>
Plankton Toolbox can be run on Windows, Mac OS X and Ubuntu (UNIX). No installation is needed.
The latest version can be found at: 
<a href="http://downloads.plankton-toolbox.org">http://downloads.plankton-toolbox.org</a>.
</p>
<p>
Plankton Toolbox is developed by the oceanographic unit of the 
<a href="http://smhi.se">Swedish Meterological and Hydrological Institute (SMHI)</a>.
The software is a product of the 
<a href="http://svenskalifewatch.se">Swedish LifeWatch project</a> 
funded by the 
<a href="http://www.vr.se">Swedish Science Council</a>.
</p>
<p>
Developed in Python 2.7 and Qt/PyQt4. Released under the MIT license. <br/>
Source code and info for developers at: 
<a href="http://plankton-toolbox.org">http://plankton-toolbox.org</a>.
</p>
""" % (__version__)))
        
