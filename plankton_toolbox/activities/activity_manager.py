#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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
"""

import plankton_toolbox.activities.getdatasets_activity as getdatasets_activity
import plankton_toolbox.activities.analysedata_activity as analysedata_activity
import plankton_toolbox.activities.pwreports_activity as pwreports_activity
import plankton_toolbox.activities.prepareresources_activity as prepareresources_activity
import plankton_toolbox.activities.template_activity as template_activity

class ActivityManager():
    """ 
    """
    
    def __init__(self, parentwidget):
        """ """
        self._parent = parentwidget
        self.__activitylist = [] # List of activities derived from ActivityBase.        

    def initActivities(self):
        """ Activity activator. """
        self.__activitylist.append(getdatasets_activity.GetDatasetsActivity("Get datasets", self._parent))
        self.__activitylist.append(analysedata_activity.AnalyseDataActivity("Analyse data", self._parent))
        self.__activitylist.append(pwreports_activity.PwReportsActivity("PW reports", self._parent))
        self.__activitylist.append(prepareresources_activity.PrepareResourcesActivity("Prepare resources", self._parent))
        self.__activitylist.append(template_activity.TemplateActivity("(Activity template)", self._parent))
        
    def getActivityList(self):
        """ """
        return self.__activitylist
