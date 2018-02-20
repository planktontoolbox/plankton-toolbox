#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework

class AnalyseDatasetsTab4(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab4, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        try:
            self._main_activity = main_activity
            self._analysisdata = main_activity.get_analysis_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
                
    def clear(self):
        """ """
        try:
            self._startdate_edit.clear()
            self._enddate_edit.clear()
            self._stations_listview.clear()
            self._months_listview.clear()
            self._visits_listview.clear()
            self._minmaxdepth_listview.clear()
            self._taxon_listview.clear()
            self._trophic_type_listview.clear()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def update(self):
        """ """
        try:
            self.clear()        
            self._update_filter_alternatives()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def update_filter(self):
        """ Call this before filtered analysis data is created. 
            (It is too complicated to implement automatic update on each change in the filter.)
        """
        try:
            self._update_filter()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    # ===== TAB: Select data ===== 
    def content_select_data(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab4_intro'))
        # Start date and end date.
        self._startdate_edit = QtWidgets.QLineEdit('')
        self._enddate_edit = QtWidgets.QLineEdit('')
        # Stations
        self._stations_listview = app_framework.SelectableQListView()
#        self._stations_listview.setMaximumHeight(100)
        self._months_listview = app_framework.SelectableQListView()
#        self._stations_listview.setMaximumHeight(100)
        self._visits_listview = app_framework.SelectableQListView()
#         self._visits_listview.setMaximumHeight(100)
        # Min-max depth.
        self._minmaxdepth_listview = app_framework.SelectableQListView()
#         self._minmaxdepth_listview.setMaximumHeight(100)
        # Taxon.
        self._taxon_listview = app_framework.SelectableQListView()
#         self._taxon_listview.setMaximumHeight(100)
        # Trophic type.
        self._trophic_type_listview = app_framework.SelectableQListView()
#         self._trophic_type_listview.setMaximumHeight(100)
        # Life stage.
        self._lifestage_listview = app_framework.SelectableQListView()
#         self._lifestage_listview.setMaximumHeight(100)
        #
        clicklabel1 = app_framework.ClickableQLabel('Clear all')
        clicklabel2 = app_framework.ClickableQLabel('Mark all')
        clicklabel3 = app_framework.ClickableQLabel('Clear all')
        clicklabel4 = app_framework.ClickableQLabel('Mark all')
        clicklabel5 = app_framework.ClickableQLabel('Clear all')
        clicklabel6 = app_framework.ClickableQLabel('Mark all')
        clicklabel7 = app_framework.ClickableQLabel('Clear all')
        clicklabel8 = app_framework.ClickableQLabel('Mark all')
        clicklabel9 = app_framework.ClickableQLabel('Clear all')
        clicklabel10 = app_framework.ClickableQLabel('Mark all')
        clicklabel11 = app_framework.ClickableQLabel('Clear all')
        clicklabel12 = app_framework.ClickableQLabel('Mark all')
        clicklabel13 = app_framework.ClickableQLabel('Clear all')
        clicklabel14 = app_framework.ClickableQLabel('Mark all')
        clicklabel1.label_clicked.connect(self._stations_listview.uncheckAll)                
        clicklabel2.label_clicked.connect(self._stations_listview.checkAll)                
        clicklabel3.label_clicked.connect(self._months_listview.uncheckAll)                
        clicklabel4.label_clicked.connect(self._months_listview.checkAll)                
        clicklabel5.label_clicked.connect(self._visits_listview.uncheckAll)                
        clicklabel6.label_clicked.connect(self._visits_listview.checkAll)                
        clicklabel7.label_clicked.connect(self._minmaxdepth_listview.uncheckAll)                
        clicklabel8.label_clicked.connect(self._minmaxdepth_listview.checkAll)                
        clicklabel9.label_clicked.connect(self._taxon_listview.uncheckAll)                
        clicklabel10.label_clicked.connect(self._taxon_listview.checkAll)                
        clicklabel11.label_clicked.connect(self._trophic_type_listview.uncheckAll)                
        clicklabel12.label_clicked.connect(self._trophic_type_listview.checkAll)                
        clicklabel13.label_clicked.connect(self._lifestage_listview.uncheckAll)                
        clicklabel14.label_clicked.connect(self._lifestage_listview.checkAll)                
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Date from:')
        label2 = QtWidgets.QLabel('Stations:')
        label3 = QtWidgets.QLabel('Sampling months:')
        label4 = QtWidgets.QLabel('Sampling events:')
        label5 = QtWidgets.QLabel('Min-max depth:')
        label6 = QtWidgets.QLabel('Scientific name:')
        label7 = QtWidgets.QLabel('Trophic type:')
        label8 = QtWidgets.QLabel('Life stage:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 3)
        form1.addWidget(label3, gridrow, 4, 1, 3)
        form1.addWidget(label4, gridrow, 7, 1, 3)
        form1.addWidget(label5, gridrow, 10, 1, 3)
        form1.addWidget(label6, gridrow, 13, 1, 3)
        form1.addWidget(label7, gridrow, 16, 1, 3)
        form1.addWidget(label8, gridrow, 19, 1, 3)
        gridrow += 1
        form1.addWidget(self._startdate_edit, gridrow, 0, 1, 1)
        form1.addWidget(self._stations_listview, gridrow, 1, 10, 3)
        form1.addWidget(self._months_listview, gridrow, 4, 10, 3)
        form1.addWidget(self._visits_listview, gridrow, 7, 10, 3)
        form1.addWidget(self._minmaxdepth_listview, gridrow, 10, 10, 3)
        form1.addWidget(self._taxon_listview, gridrow, 13, 10, 3)
        form1.addWidget(self._trophic_type_listview, gridrow, 16, 10, 3)
        form1.addWidget(self._lifestage_listview, gridrow, 19, 10, 3)
        gridrow += 1
        label1 = QtWidgets.QLabel('Date to:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._enddate_edit, gridrow, 0, 1, 1)
        gridrow += 10
        form1.addWidget(clicklabel1, gridrow, 1, 1, 1)
        form1.addWidget(clicklabel2, gridrow, 2, 1, 1)
        form1.addWidget(clicklabel3, gridrow, 4, 1, 1)
        form1.addWidget(clicklabel4, gridrow, 5, 1, 1)
        form1.addWidget(clicklabel5, gridrow, 7, 1, 1)
        form1.addWidget(clicklabel6, gridrow, 8, 1, 1)
        form1.addWidget(clicklabel7, gridrow, 10, 1, 1)
        form1.addWidget(clicklabel8, gridrow, 11, 1, 1)
        form1.addWidget(clicklabel9, gridrow, 13, 1, 1)
        form1.addWidget(clicklabel10, gridrow, 14, 1, 1)
        form1.addWidget(clicklabel11, gridrow, 16, 1, 1)
        form1.addWidget(clicklabel12, gridrow, 17, 1, 1)
        form1.addWidget(clicklabel13, gridrow, 19, 1, 1)
        form1.addWidget(clicklabel14, gridrow, 20, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
#         layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self

    def _update_filter_alternatives(self):
        """ """
        try:
            analysisdata = self._analysisdata.get_data()
            if not analysisdata:
                return # Empty data.
            #
            startdate = '9999-99-99'
            enddate = '0000-00-00'
            station_set = set()
            visitmonth_set = set()
            visit_set = set()
            minmaxdepth_set = set()
            taxon_set = set()
            trophic_type_set = set()
            lifestage_set = set()
            #
            for visitnode in analysisdata.get_children():
                station_set.add(visitnode.get_data('station_name'))
                visitmonth_set.add(visitnode.get_data('visit_month'))
                visit_set.add(str(visitnode.get_data('station_name')) + ' : ' + str(visitnode.get_data('sample_date')))
                startdate = min(startdate, visitnode.get_data('sample_date'))
                enddate = max(enddate, visitnode.get_data('sample_date'))
                for samplenode in visitnode.get_children():
                    depthstring = str(samplenode.get_data('sample_min_depth_m')) + '-' + str(samplenode.get_data('sample_max_depth_m'))
                    minmaxdepth_set.add(depthstring)
                    for variablenode in samplenode.get_children():
                        taxon_set.add(variablenode.get_data('scientific_name'))
                        #
                        trophic_type_set.add(variablenode.get_data('trophic_type'))
                        #
                        lifestage = variablenode.get_data('stage')
                        if variablenode.get_data('sex'):
                            lifestage += '/' + variablenode.get_data('sex')
                        lifestage_set.add(lifestage)
            # Start date and end date.
            self._startdate_edit.setText(startdate)
            self._enddate_edit.setText(enddate)
            # Selection lists.
            self._stations_listview.setList(sorted(station_set))
            self._months_listview.setList(sorted(visitmonth_set))
            self._visits_listview.setList(sorted(visit_set))
            self._minmaxdepth_listview.setList(sorted(minmaxdepth_set))
            self._taxon_listview.setList(sorted(taxon_set))
            self._trophic_type_listview.setList(sorted(trophic_type_set))
            self._lifestage_listview.setList(sorted(lifestage_set))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _update_filter(self):
        """ """
        try:
            self._analysisdata.clear_filter()
            self._analysisdata.set_filter_item('start_date', str(self._startdate_edit.text()))
            self._analysisdata.set_filter_item('end_date', str(self._enddate_edit.text()))
            self._analysisdata.set_filter_item('stations', self._stations_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('visit_months', self._months_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('visits', self._visits_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('min_max_depth_m', self._minmaxdepth_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('scientific_name', self._taxon_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('trophic_type', self._trophic_type_listview.getSelectedDataList())
            self._analysisdata.set_filter_item('life_stage', self._lifestage_listview.getSelectedDataList())
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
