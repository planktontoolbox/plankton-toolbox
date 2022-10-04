#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import app_framework
import app_activities
import toolbox_utils


@toolbox_utils.singleton
class ActivityManager(object):
    """
    The activity manager is used to set up available activites.
    """

    def __init__(self):
        """ """
        self._parent = None
        self._activitylist = []  # List of activities derived from ActivityBase.

    def set_parent(self, parentwidget):
        """ """
        self._parent = parentwidget

    def init_activities(self):
        """Activity activator."""
        self._activitylist.append(app_activities.StartActivity("Welcome", self._parent))
        self._activitylist.append(
            app_activities.PlanktonCounterActivity("Plankton counter", self._parent)
        )
        self._activitylist.append(
            app_activities.LoadDatasetsActivity("Dataset manager", self._parent)
        )
        self._activitylist.append(
            app_activities.ScreeningActivity("Dataset screening", self._parent)
        )
        self._activitylist.append(
            app_activities.CreateReportsActivity("Dataset reports", self._parent)
        )
        self._activitylist.append(
            app_activities.AnalyseDatasetsActivity("Dataset analysis", self._parent)
        )

    #         self._activitylist.append(template_activity.TemplateActivity('(Activity template)', self._parent))
    #         self._activitylist.append(app_activities.TestActivity('Test activity (template)', self._parent))

    def show_activity_by_name(self, object_name):
        """Makes an activity visible."""
        for activity in self._activitylist:
            if activity.objectName() == object_name:
                activity._parent.showActivity(activity)
                return

    def get_activity_list(self):
        """ """
        return self._activitylist
