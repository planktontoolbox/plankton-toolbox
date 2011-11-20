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

