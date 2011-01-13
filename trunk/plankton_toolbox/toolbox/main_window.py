#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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
Main window for the Plankton toolbox.

The layout is an activity area in the middle, activity and tool selector to the
left and movable tools to the right and at the bottom. Activites are handled as 
stacked widgets and tools are dockable widgets. The activity and tool selector
is also dockable.
"""

import time
import codecs
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.activities.activity_manager as activity_manager
import plankton_toolbox.tools.log_tool as log_tool
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

__version__ = '0.0.1' # Plankton-toolbox version.

class MainWindow(QtGui.QMainWindow):
    """ 
    Main window for the Plankton toolbox application.
    """
    def __init__(self):
        """ """
        # Initialize parent.
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr("Plankton toolbox"))
        # Note: Tools menu is public.
        self.toolsmenu = None
        # Load toolbox settings.
        self.__ui_settings = QtCore.QSettings()
        toolbox_settings.ToolboxSettings().loadSettings(self.__ui_settings)
        # Logging. Always log to plankton_toolbox_log.txt. Use the Log tool when  
        # it is available.
        self.__logfile = codecs.open('plankton_toolbox_log.txt', mode = 'w', encoding = 'iso-8859-1')
        self.__logfile.write('Plankton-toolbox. ' +
                             time.strftime("%Y-%m-%d %H:%M:%S") +'\r\n\r\n')
        self.__logtool = None # Should be initiated later.
        utils.Logger().setLogTarget(self) # Logger should log here (to self.writeToLog()). 
        # Setup main window.
        self.__createActions()
        self.__createMenu()
        self.__createStatusBar()
        self.__activity = None
        self.__createCentralWidget()
        # Set up activities and tools.
        self.__toolmanager = tool_manager.ToolManager(self)
        self.__toolmanager.initTools()
        self.__activitymanager = activity_manager.ActivityManager(self)
        self.__activitymanager.initActivities()
        # Add tools to selector.
        self.__createContentSelectors()
        # Loads last used window positions.
        self.setGeometry(self.__ui_settings.value("MainWindow/Geometry").toRect())
        self.restoreState(self.__ui_settings.value("MainWindow/State").toByteArray())        
        size = self.__ui_settings.value("MainWindow/Size", QtCore.QVariant(QtCore.QSize(900, 400))).toSize()
        position = self.__ui_settings.value("MainWindow/Position", QtCore.QVariant(QtCore.QPoint(100, 50))).toPoint()
        self.resize(size)
        self.move(position)        
        # Load resources when the main event loop has started.
        if toolbox_settings.ToolboxSettings().getValue('Resources:Load at startup'):
            QtCore.QTimer.singleShot(10, toolbox_resources.ToolboxResources().loadAllResources)
        #
        utils.Logger().info('Plankton toolbox started.')

        
    def closeEvent(self, event):
        """ Called on application shutdown. """
        # Stores current window positions.
        self.__ui_settings.setValue("MainWindow/Size", QtCore.QVariant(self.size()))
        self.__ui_settings.setValue("MainWindow/Position", QtCore.QVariant(self.pos()))
        self.__ui_settings.setValue("MainWindow/State", self.saveState())
        self.__ui_settings.setValue("MainWindow/Geometry", self.geometry())
        self.__logfile.close
        # Save toolbox settings.
        toolbox_settings.ToolboxSettings().saveSettings(self.__ui_settings)
    
    def __createMenu(self):
        """ 
        The  main menu of the application. 
        Note: The Tools menu will be populated by the tool base class. Search
        for 'toggleViewAction' to see the implementation.
        """
        self.__filemenu = self.menuBar().addMenu(self.tr("&File"))
        self.__filemenu.addSeparator()
        self.__filemenu.addAction(self.__quitaction)
        self.__viewmenu = self.menuBar().addMenu(self.tr("&View"))
        self.toolsmenu = self.menuBar().addMenu(self.tr("&Tools")) # Note: Public.
        self.__helpmenu = self.menuBar().addMenu(self.tr("&Help"))
        self.__helpmenu.addAction(self.__aboutaction)

    def __createStatusBar(self):
        """ 
        The status bar is located at the bottom of the main window. Tools can
        write messages here by calling <i>_writeToStatusBar</i> located in the 
        tool base class.
        """
        self.statusBar().showMessage(self.tr("Plankton toolbox."))

    def __createContentSelectors(self):
        """ 
        The user should be able to choose one activity and a number of tools.
        """
        # Create left dock widget and dock to main window.
        dock = QtGui.QDockWidget(self.tr("Activities and tools"), self)
        dock.setObjectName("Activities and tools selector")
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | 
                             QtGui.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        # Widget to create space and layout for two groupboxes.
        widget1 = QtGui.QWidget()
        dock.setWidget(widget1)
        grid1 = QtGui.QVBoxLayout()
        widget1.setLayout(grid1)        
#        grid1.setMargin(0)
#        grid1.setSpacing(0)
        # For activites.        
        activitiesgroup = QtGui.QGroupBox("Activities")
        grid1.addWidget(activitiesgroup)
        activitiesvbox = QtGui.QVBoxLayout()
        activitiesgroup.setLayout(activitiesvbox)
#        activitiesvbox.setMargin(0)
#        activitiesvbox.setSpacing(0)
        
### TODO:        
#        activitiestree = QtGui.QTreeWidget()
#        activitiesvbox.addWidget(activitiestree)
#        activitiestree.setHeaderHidden(True)
###
        # For tools.
        toolsgroup = QtGui.QGroupBox("Tools")
        grid1.addWidget(toolsgroup)        
        toolsvbox = QtGui.QVBoxLayout()
        toolsgroup.setLayout(toolsvbox)
        grid1.addStretch(5)
#        toolsvbox.setMargin(0)
#        toolsvbox.setSpacing(0)

        # Add one button for each activity. Create stacked widgets.
        for activity in self.__activitymanager.getActivityList():
            button = QtGui.QPushButton(activity.objectName())
            activitiesvbox.addWidget(button) # Adds to stack.                  
### TODO:
#            treeitem = QtGui.QTreeWidgetItem(activitiestree, [activity.objectName()])            
#            treeitem = QtGui.QTreeWidgetItem(treeitem, [activity.objectName()])
###         
            # The activity is called to select stack item by object, not index.
            self.connect(button, QtCore.SIGNAL("clicked()"), activity.showInMainWindow)
### TODO:          
#            self.connect(activitiestree, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *, int)"), activity.showInMainWindow)
###            
            # Create one layer in the stacked activity widget.
            self.__activitystack.addWidget(activity)
        activitiesvbox.addStretch(5)

        # Add one button for each tool.
        for tool in self.__toolmanager.getToolList():
            button = QtGui.QPushButton(tool.objectName())
            toolsvbox.addWidget(button)
            self.connect(button, QtCore.SIGNAL("clicked()"), tool.show) # Show if hidden.
            self.connect(button, QtCore.SIGNAL("clicked()"), tool.raise_) # Bring to front.
        toolsvbox.addStretch(5)
           
    def showActivity(self, activity):
        """ """
        self.__activityheader.setText('<b>' + activity.objectName() + '</b>')
        self.__activitystack.setCurrentWidget(activity)
    
    def __createCentralWidget(self):
        """ 
        The central widget contains the selected activity. It is implemented as
        stacked layout, QStackedLayout, where the pages are selected from
        the activities group box. 
        """
        self.__activityheader = QtGui.QLabel("<b>Activity not selected...</b>", self)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self.__activitystack = QtGui.QStackedLayout()        
#        self.__activitystack.setMargin(0)
#        self.__activitystack.setSpacing(0)
        # Layout widgets.
        widget = QtGui.QWidget(self) 
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
#        layout.setMargin(0)
#        layout.setSpacing(0)
        self.setCentralWidget(widget)
        layout.addWidget(self.__activityheader)
        layout.addLayout(self.__activitystack)
        # Dummy stack content.
        dummy = QtGui.QWidget(self)
        self.__activitystack.addWidget(dummy)
       
    def __createActions(self):
        """ Common application related actions. """
        self.__quitaction = QtGui.QAction(self.tr("&Quit"), self)
        self.__quitaction.setShortcut(self.tr("Ctrl+Q"))
        self.__quitaction.setStatusTip(self.tr("Quit the application"))
        self.__quitaction.triggered.connect(self.close)
        #
        self.__aboutaction = QtGui.QAction(self.tr("&About"), self)
        self.__aboutaction.setStatusTip(self.tr("Show the application's About box"))
        self.__aboutaction.triggered.connect(self.__about)

    def writeToLog(self, message):
        """ Log to file and to the log tool when available. """
#        self.console.addItem(message)
        self.__logfile.write(message + '\r\n')
        self.__logfile.flush()        
        # Search for the console tool. Note: Not available during startup.
        if not self.__logtool:
            for tool in self.__toolmanager.getToolList():
                if type(tool) == log_tool.LogTool:
                    self.__logtool = tool
        # Log message.                   
        if self.__logtool: self.__logtool.writeToLog(message)

    def __about(self):
        """ """
        QtGui.QMessageBox.about(self, self.tr("About Plankton toolbox"),
                self.tr(
"""
<p>
<b>Plankton toolbox</b> version %s
</p>
<p>
Plankton toolbox is an application... (TODO:)  
</p>
<p>
Developed in Python 2.6 and Qt/PyQt4. Released under the MIT license.
</p>
<p>
More info at 
<a href="http://plankton-toolbox.org">http://plankton-toolbox.org</a>
</p>
""" % (__version__)))
        
