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
Activity manager.
"""

import plankton_toolbox.activities.start_activity as start_activity
import plankton_toolbox.activities.create_dataset_activity as create_dataset_activity
import plankton_toolbox.activities.load_datasets_activity as load_datasets_activity
import plankton_toolbox.activities.screening_activity as screening_activity
import plankton_toolbox.activities.analyse_datasets_activity as analyse_datasets_activity
import plankton_toolbox.activities.create_reports_activity as create_reports_activity
import plankton_toolbox.activities.manage_species_lists_activity as manage_species_lists_activity

import plankton_toolbox.activities.load_datasets_OLD_activity as load_datasets_OLD_activity
import plankton_toolbox.activities.create_reports_OLD_activity as create_reports_OLD_activity
#import plankton_toolbox.activities.template_activity as template_activity

class ActivityManager(object):
    """ 
    The activity manager is used to set up available activites. 
    """
    
    def __init__(self, parentwidget):
        """ """
        self._parent = parentwidget
        self.__activitylist = [] # List of activities derived from ActivityBase.        

    def initActivities(self):
        """ Activity activator. """
#        self.__activitylist.append(start_activity.StartActivity("Start", self._parent))
#        self.__activitylist.append(create_dataset_activity.CreateDatasetActivity("(Create dataset)", self._parent))
        self.__activitylist.append(load_datasets_activity.LoadDatasetsActivity("Load datasets", self._parent))
#        self.__activitylist.append(screening_activity.ScreeningActivity("Screening", self._parent))
        self.__activitylist.append(analyse_datasets_activity.AnalyseDatasetsActivity("Analyse datasets", self._parent))
#        self.__activitylist.append(create_reports_activity.CreateReportsActivity("(Create reports)", self._parent))
#        self.__activitylist.append(manage_species_lists_activity.ManageSpeciesListsActivity("Manage species lists", self._parent))

#        self.__activitylist.append(load_datasets_OLD_activity.LoadDatasetsActivity("Load datasets (OLD)", self._parent))
#        self.__activitylist.append(create_reports_OLD_activity.CreateReportsActivity("Create reports (OLD)", self._parent))
#        self.__activitylist.append(template_activity.TemplateActivity("(Activity template)", self._parent))
        
    def getActivityList(self):
        """ """
        return self.__activitylist
