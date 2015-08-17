#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_toolbox.activities.start_activity as start_activity

import plankton_toolbox.activities.plankton_counter_activity as counter_activity

import plankton_toolbox.activities.load_datasets_activity as load_datasets_activity
import plankton_toolbox.activities.screening_activity as screening_activity
import plankton_toolbox.activities.analyse_datasets_activity as analyse_datasets_activity
import plankton_toolbox.activities.create_reports_activity as create_reports_activity

import plankton_toolbox.activities.manage_species_lists_activity as manage_species_lists_activity

#import plankton_toolbox.activities.load_datasets_OLD_activity as load_datasets_OLD_activity
#import plankton_toolbox.activities.create_reports_OLD_activity as create_reports_OLD_activity
# import plankton_toolbox.activities.template_activity as template_activity

# import envmonlib
import toolbox_utils
import toolbox_core

@toolbox_utils.singleton
class ActivityManager(object):
    """ 
    The activity manager is used to set up available activites. 
    """
    
#     def __init__(self, parentwidget):
#         """ """
#         self._parent = parentwidget
#         self._activitylist = [] # List of activities derived from ActivityBase.        

    def __init__(self):
        """ """
        self._parent = None
        self._activitylist = [] # List of activities derived from ActivityBase.        

    def set_parent(self, parentwidget):
        """ """
        self._parent = parentwidget

    def init_activities(self):
        """ Activity activator. """
        self._activitylist.append(counter_activity.PlanktonCounterActivity('Plankton counter', self._parent))

        self._activitylist.append(start_activity.StartActivity('Welcome', self._parent))

        self._activitylist.append(load_datasets_activity.LoadDatasetsActivity('Dataset manager', self._parent))
        self._activitylist.append(screening_activity.ScreeningActivity('Dataset screening', self._parent))
        self._activitylist.append(analyse_datasets_activity.AnalyseDatasetsActivity('Dataset analysis', self._parent))
        self._activitylist.append(create_reports_activity.CreateReportsActivity('Report generator', self._parent))

        self._activitylist.append(manage_species_lists_activity.ManageSpeciesListsActivity('REMOVE: Manage species lists', self._parent))
#         self._activitylist.append(template_activity.TemplateActivity('(Activity template)', self._parent))
        
#     def get_activity_by_name(self, object_name):
#         """ Returns the activity. """
#         for activity in self._activitylist:
#             if activity.objectName() == object_name: 
#                 return activity
#         return None
#         
#     def show_activity_by_index(self, index):
#         """ Makes an activity visible. """
#         self._activitylist[index]._parent.showActivity(self._activitylist[index])

        
    def show_activity_by_name(self, object_name):
        """ Makes an activity visible. """
        for activity in self._activitylist:
            if activity.objectName() == object_name: 
                activity._parent.showActivity(activity)
                return
        
    def get_activity_list(self):
        """ """
        return self._activitylist
