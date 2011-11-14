#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
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
This module contains GUI-related utilities for the Plankton Toolbox project.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
class ClickableQLabel(QtGui.QLabel):  
    """ Customized QLabel. Emits signal when clicked, and change color when hovering. """
    def __init__(self, parent):  
        QtGui.QLabel.__init__(self, parent)  
        # Set style.
        self.setProperty("ActivityStatus", "Unselected")  ### TODO: Remove this when stylesheet fixed.
        self.updateStyleSheet()
  
    def mouseReleaseEvent(self, ev):  
        self.emit(QtCore.SIGNAL('clicked()'))  
  
    def enterEvent(self, ev):        
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color: #d1581c; background-color: #eaa97e; }
            * [ActivityStatus="Unselected"] { color: #d1581c; background-color: #dddddd; }
            """)
  
    def leaveEvent(self, ev):  
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color: #00677f; background-color: #eaa97e; }
            * [ActivityStatus="Unselected"] { color: #00677f; background-color: #dddddd; }
            """)

    def updateStyleSheet(self):  
        self.setStyleSheet(""" 
            * [ActivityStatus="Selected"] { color:  #00677f; background-color: #eaa97e; }
            * [ActivityStatus="Unselected"] { color:  #00677f; background-color: #dddddd; }
            """)


class ActivityMenuQLabel(ClickableQLabel):  
    """ Customized QLabel. Contains a list of all ActivityMenuQLabel objects. Only one is marked as active.  """
    # Static variable:
    activityitems = []
    
    def __init__(self, parent):  
        ClickableQLabel.__init__(self, parent)
        # Add to static variable:
        self.activityitems.append(self)
        self.markAsUnselected()
        
    def markAsSelected(self):
        """ """
        # Mark all others as unselected.
        for label in self.activityitems:
            label.markAsUnselected() 
        # Mark this as selected.
        self.setProperty("ActivityStatus", "Selected")
        self.updateStyleSheet()
          
    def markAsUnselected(self):
        """ """
        self.setProperty("ActivityStatus", "Unselected")
        self.updateStyleSheet()
          

# === Style sheets: ===

    # Nordic Microalgae colors:
    #    Red: #d1581c
    #    Blue: #00677f
    #    Green: #89a45e
    #    Red 50%: #eaa97e
    #    Blue 50%: (#6da88d) #6da8bd 
    #    Green 50%: #cbd1aa
    #    Red 25%: #f5d5bd
    #    Blue 25%: #b7d3de
    #    Green 30%: #e0e3cd

def setAppStyleSheet(app):
    app.setStyleSheet("""
        /* Default for all dock widgets.*/
        QDockWidget, QDockWidget *  { color: black; background-color: #dddddd; }
        QDockWidget QPushButton:hover { color: #eaa97e; }

        /* Default for all widgets used in tools. */        
        ToolBase, ToolBase * { color: black; background-color: #dddddd; } 
        ToolBase QPushButton:hover { color: #eaa97e; } 

        /* Default for all widgets used in activities. */        
        ActivityBase, ActivityBase * { color: black; background-color: #dddddd; } 
        ActivityBase QPushButton:hover { color: #eaa97e; } 
        
        QStatusBar { background-color: #dddddd; }
    """)

#        ClickableQLabel { color: #00677f;  }
#
#        ClickableQLabel[ClickableQLabelHover="Highlight"] { color: black;}
#        ClickableQLabel[ClickableQLabelHover="Normal"] { color: #00677f; }
#
#        ActivityMenuQLabel[ClickableQLabelStatus="Selected"] { color: red; background-color: orange; }
#        ActivityMenuQLabel[ClickableQLabelStatus="Unselected"] { color: green; background-color: white; }
#    """)

#    app.setStyleSheet("""
#        /* Default for all dock widgets.*/
#        QDockWidget, QDockWidget *  { color: white; background-color: black; }
#        QDockWidget QPushButton:hover { color: #d1581c }
#
#        /* Default for all widgets used in tools. */        
#        ToolBase, ToolBase * { color: white; background-color: black; } 
#        ToolBase QPushButton:hover { color: #d1581c; } 
#
#        /* Default for all widgets used in activities. */        
#        ActivityBase, ActivityBase * { color: white; background-color: black; } 
#        ActivityBase QPushButton:hover { color: #d1581c; } 
#        
#        QStatusBar { background-color: #999999 }
#
#        ClickableQLabel { color: #00677f;  }
#    """)

#    app.setStyleSheet("""
#        /* TEST. */
#        * { background-color: orange; }
#        *:hover { color: green; font-weight: bold; }
#    """)

#    app.setStyleSheet("""
#        /* Default for all widgets. */
#/*        * { background-color: #b7d3de; }
#*/      
#        /* Default for all dock widgets.*/
#/*        QDockWidget, QDockWidget *  { background-color: #b7d3de; }
#        QDockWidget *:hover { color: #00677f; }
#*/
#        QDockWidget, QDockWidget *  { color: white; background-color: #00677f; }
#        QDockWidget *:hover { color: #b7d3de; }
#
#        /* Default for all widgets used in tools. */        
#        ToolBase, ToolBase * { color: black; background-color: #e0e3cd; } 
#        ToolBase *:hover { color: #89a45e; } 
#
#        /* Default for all widgets used in activities. */        
#/*        ActivityBase, ActivityBase * { color: black; background-color: #f5d5bd; } 
#        ActivityBase *:hover { color: #d1581c; } 
#*/
#        ActivityBase, ActivityBase * { color: black; background-color: #b7d3de; } 
#        ActivityBase *:hover { color: #00677f; }    
#    """)

#    app.setStyleSheet("""
#        /* Default for all widgets. */
#/*        * { background-color: #b7d3de; }
#*/      
#        /* Default for all dock widgets.*/
#/*        QDockWidget, QDockWidget *  { background-color: #b7d3de; }
#        QDockWidget *:hover { color: #00677f; }
#*/
#        QDockWidget, QDockWidget *  { color: white; background-color: #00677f; }
#        QDockWidget *:hover { color: #b7d3de; }
#
#        /* Default for all widgets used in tools. */        
#        ToolBase, ToolBase * { color: black; background-color: #e0e3cd; } 
#        ToolBase *:hover { color: #89a45e; } 
#
#        /* Default for all widgets used in activities. */        
#/*        ActivityBase, ActivityBase * { color: black; background-color: #f5d5bd; } 
#        ActivityBase *:hover { color: #d1581c; } 
#*/
#        ActivityBase, ActivityBase * { color: black; background-color: #b7d3de; } 
#        ActivityBase *:hover { color: #00677f; } 
#
#/*
#ClickableQLabel { background-color: #e0e3cd; color: #89a45e;  }
#
#*:hover { color: blue; }
#
#QPushButton:hover { color: white }
#QMenuBar::item { background-color: lightblue; }
#QMenu {
#     background-color: #171512;
#     color: #B8C1C6;
#     font-family: Arial;
#     font-size: 11px;
#     border: 1px solid black; }
#QMenu::item {
#     background-color: transparent; }
#QMenu::item:selected {
#     background-color: red;
#}
#        
#QDockWidget {
#     border: 1px solid lightgray;
#     titlebar-close-icon: url(close.png);
#     titlebar-normal-icon: url(undock.png);
# }
#
# QDockWidget::title {
#     text-align: left;
#     background: lightgray;
#     padding-left: 5px;
# }
#
# QDockWidget::close-button, QDockWidget::float-button {
#     border: 1px solid transparent;
#     background: darkgray;
#     padding: 0px;
# }
#
# QDockWidget::close-button:hover, QDockWidget::float-button:hover {
#     background: gray;
# }
#
# QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
#     padding: 1px -1px -1px 1px;
# }
#        
# 
# QTabWidget::pane {
#     border-top: 2px solid #C2C7CB;
# }
#
# QTabWidget::tab-bar {
#     left: 5px;
# }
#
# QTabBar::tab {
#     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
#                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
#     border: 2px solid #C4C4C3;
#     border-bottom-color: #C2C7CB;
#     border-top-left-radius: 4px;
#     border-top-right-radius: 4px;
#     min-width: 8ex;
#     padding: 2px;
# }
#
# QTabBar::tab:selected, QTabBar::tab:hover {
#     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                                 stop: 0 #fafafa, stop: 0.4 #f4f4f4,
#                                 stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
# }
#
# QTabBar::tab:selected {
#     border-color: #9B9B9B;
#     border-bottom-color: #C2C7CB;
# }
#
# QTabBar::tab:!selected {
#     margin-top: 2px;
# }
# 
# 
#QTableView {
#     selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
#                                 stop: 0 #FF92BB, stop: 1 white);
# }
# */
#
#    """)
  

