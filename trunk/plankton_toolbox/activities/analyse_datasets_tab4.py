#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
# import envmonlib

class AnalyseDatasetsTab4(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab4, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        self._startdate_edit.clear()
        self._enddate_edit.clear()
        self._stations_listview.clear()
        self._months_listview.clear()
        self._visits_listview.clear()
        self._minmaxdepth_listview.clear()
        self._taxon_listview.clear()
        self._trophic_level_listview.clear()
        
    def update(self):
        """ """
        self.clear()        
        self._updateFilterAlternatives()

    def updateFilter(self):
        """ Call this before filtered analysis data is created. 
            (It is too complicated to implement automatic update on each change in the filter.)
        """
        self._updateFilter()
        
    # ===== TAB: Select data ===== 
    def contentSelectData(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab4_intro'))
        # Start date and end date.
        self._startdate_edit = QtGui.QLineEdit("")
        self._enddate_edit = QtGui.QLineEdit("")
        # Stations
        self._stations_listview = utils_qt.SelectableQListView()
#        self._stations_listview.setMaximumHeight(100)
        self._months_listview = utils_qt.SelectableQListView()
#        self._stations_listview.setMaximumHeight(100)
        self._visits_listview = utils_qt.SelectableQListView()
#         self._visits_listview.setMaximumHeight(100)
        # Min-max depth.
        self._minmaxdepth_listview = utils_qt.SelectableQListView()
#         self._minmaxdepth_listview.setMaximumHeight(100)
        # Taxon.
        self._taxon_listview = utils_qt.SelectableQListView()
#         self._taxon_listview.setMaximumHeight(100)
        # Trophic_level.
        self._trophic_level_listview = utils_qt.SelectableQListView()
#         self._trophic_level_listview.setMaximumHeight(100)
        # Life stage.
        self._lifestage_listview = utils_qt.SelectableQListView()
#         self._lifestage_listview.setMaximumHeight(100)
        #
        clicklabel1 = utils_qt.ClickableQLabel("Clear all")
        clicklabel2 = utils_qt.ClickableQLabel("Mark all")
        clicklabel3 = utils_qt.ClickableQLabel("Clear all")
        clicklabel4 = utils_qt.ClickableQLabel("Mark all")
        clicklabel5 = utils_qt.ClickableQLabel("Clear all")
        clicklabel6 = utils_qt.ClickableQLabel("Mark all")
        clicklabel7 = utils_qt.ClickableQLabel("Clear all")
        clicklabel8 = utils_qt.ClickableQLabel("Mark all")
        clicklabel9 = utils_qt.ClickableQLabel("Clear all")
        clicklabel10 = utils_qt.ClickableQLabel("Mark all")
        clicklabel11 = utils_qt.ClickableQLabel("Clear all")
        clicklabel12 = utils_qt.ClickableQLabel("Mark all")
        clicklabel13 = utils_qt.ClickableQLabel("Clear all")
        clicklabel14 = utils_qt.ClickableQLabel("Mark all")
        self.connect(clicklabel1, QtCore.SIGNAL("clicked()"), self._stations_listview.uncheckAll)                
        self.connect(clicklabel2, QtCore.SIGNAL("clicked()"), self._stations_listview.checkAll)                
        self.connect(clicklabel3, QtCore.SIGNAL("clicked()"), self._months_listview.uncheckAll)                
        self.connect(clicklabel4, QtCore.SIGNAL("clicked()"), self._months_listview.checkAll)                
        self.connect(clicklabel5, QtCore.SIGNAL("clicked()"), self._visits_listview.uncheckAll)                
        self.connect(clicklabel6, QtCore.SIGNAL("clicked()"), self._visits_listview.checkAll)                
        self.connect(clicklabel7, QtCore.SIGNAL("clicked()"), self._minmaxdepth_listview.uncheckAll)                
        self.connect(clicklabel8, QtCore.SIGNAL("clicked()"), self._minmaxdepth_listview.checkAll)                
        self.connect(clicklabel9, QtCore.SIGNAL("clicked()"), self._taxon_listview.uncheckAll)                
        self.connect(clicklabel10, QtCore.SIGNAL("clicked()"), self._taxon_listview.checkAll)                
        self.connect(clicklabel11, QtCore.SIGNAL("clicked()"), self._trophic_level_listview.uncheckAll)                
        self.connect(clicklabel12, QtCore.SIGNAL("clicked()"), self._trophic_level_listview.checkAll)                
        self.connect(clicklabel13, QtCore.SIGNAL("clicked()"), self._lifestage_listview.uncheckAll)                
        self.connect(clicklabel14, QtCore.SIGNAL("clicked()"), self._lifestage_listview.checkAll)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Date from:")
        label2 = QtGui.QLabel("Stations:")
        label3 = QtGui.QLabel("Sampling months:")
        label4 = QtGui.QLabel("Sampling events:")
        label5 = QtGui.QLabel("Min-max depth:")
        label6 = QtGui.QLabel("Scientific name:")
        label7 = QtGui.QLabel("Trophic level:")
        label8 = QtGui.QLabel("Life stage:")
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
        form1.addWidget(self._trophic_level_listview, gridrow, 16, 10, 3)
        form1.addWidget(self._lifestage_listview, gridrow, 19, 10, 3)
        gridrow += 1
        label1 = QtGui.QLabel("Date to:")
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
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
#         layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self

    def _updateFilterAlternatives(self):
        """ """
        analysisdata = self._analysisdata.getData()
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
        trophic_level_set = set()
        lifestage_set = set()
        #
        for visitnode in analysisdata.getChildren():
            station_set.add(visitnode.getData(u'station_name'))
            visitmonth_set.add(visitnode.getData(u'month'))
            visit_set.add(unicode(visitnode.getData(u'station_name')) + u' : ' + unicode(visitnode.getData(u'date')))
            startdate = min(startdate, visitnode.getData(u'date'))
            enddate = max(enddate, visitnode.getData(u'date'))
            for samplenode in visitnode.getChildren():
                depthstring = unicode(samplenode.getData(u'sample_min_depth')) + '-' + unicode(samplenode.getData(u'sample_max_depth'))
                minmaxdepth_set.add(depthstring)
                for variablenode in samplenode.getChildren():
                    taxon_set.add(variablenode.getData(u'scientific_name'))
                    #
                    trophic_level_set.add(variablenode.getData(u'trophic_level'))
                    #
                    lifestage = variablenode.getData(u'stage')
                    if variablenode.getData(u'sex'):
                        lifestage += u'/' + variablenode.getData(u'sex')
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
        self._trophic_level_listview.setList(sorted(trophic_level_set))
        self._lifestage_listview.setList(sorted(lifestage_set))
            
    def _updateFilter(self):
        """ """
        self._analysisdata.clearFilter()
        
        self._analysisdata.setFilterItem(u'start_date', unicode(self._startdate_edit.text()))
        self._analysisdata.setFilterItem(u'end_date', unicode(self._enddate_edit.text()))
        self._analysisdata.setFilterItem(u'stations', self._stations_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'visit_months', self._months_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'visits', self._visits_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'min_max_depth', self._minmaxdepth_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'taxon', self._taxon_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'trophic_level', self._trophic_level_listview.getSelectedDataList())
        self._analysisdata.setFilterItem(u'life_stage', self._lifestage_listview.getSelectedDataList())
        
