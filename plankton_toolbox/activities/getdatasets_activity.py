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
Test version of the 'get dataset activity'. Data is fetched from
the website test.mellifica.org/sharkweb, which should be replaced
by www.mellifica.se/sharkweb later. Search options is based on the 
layout of the corresponding page on the website.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.monitoring.pw_monitoring_files as pw_monitoring_files

class GetDatasetsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(GetDatasetsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        """ """
        # === GroupBox: selectionbox === 
        selectionbox = QtGui.QGroupBox("Selection", self)
        # Active widgets and connections.
        self.__bounds_edit = QtGui.QLineEdit("")
        self.__year_from_edit = QtGui.QLineEdit("2008")
        self.__year_to_edit = QtGui.QLineEdit("2008")
        self.__month_edit = QtGui.QLineEdit("06")
        self.__datatype_edit = QtGui.QLineEdit("Phytoplankton")
        self.__parameter_edit = QtGui.QLineEdit("COUNTNR")
        self.__project_code_edit = QtGui.QLineEdit("")
        self.__orderer_edit = QtGui.QLineEdit("")
        self.__deliverer_edit = QtGui.QLineEdit("")
        self.__station_name_edit = QtGui.QLineEdit("släggö, by15")
        self.__station_name_option_edit = QtGui.QLineEdit("station_list")
        self.__taxon_name_edit = QtGui.QLineEdit("Dinophyceae")
        self.__taxon_name_option_edit = QtGui.QLineEdit("class")
        self.__sample_table_view_edit = QtGui.QLineEdit("sample_std")
        self.__delimiters_edit = QtGui.QLineEdit("point-tab")
        self.__lineend_edit = QtGui.QLineEdit("unix")
        self.__limit_edit = QtGui.QLineEdit("2000")
        self.__headerlang_edit = QtGui.QLineEdit("sv")
        
        self.__get_data_button = QtGui.QPushButton("Get data")
        self.connect(self.__get_data_button, QtCore.SIGNAL("clicked()"), self.__getData)
                
#function download_sample() {
#    var action = '';
#    if ($('sample_select_table_view').value == 'map') {
#        action = 'download_sample_position';
#    } else {
#        action = 'download_sample';
#    }
#    var url = "shark_save.php?action=" + action + 
#        "&bounds=" + encodeURIComponent(getBounds()) +
#        "&year_from=" + encodeURIComponent($('sample_select_year_from').value) +
#        "&year_to=" + encodeURIComponent($('sample_select_year_to').value) +
#        "&month=" + encodeURIComponent(get_selected_month_list()) +
#        "&datatype=" + encodeURIComponent($('sample_select_datatype').value) +
#        "&parameter=" + encodeURIComponent($('sample_select_parameter').value) +
#        "&project_code=" + encodeURIComponent($('sample_select_project_code').value) +
#        "&orderer=" + encodeURIComponent($('sample_select_orderer').value) +
#        "&station_name=" + encodeURIComponent($('sample_select_station_name').value) +
#        "&station_name_option=" + encodeURIComponent($('sample_select_station_name_option').value) +
#        "&taxon_name=" + encodeURIComponent($('sample_select_taxon').value) +
#        "&taxon_name_option=" + encodeURIComponent($('sample_select_taxon_option').value) +
#        "&sample_table_view=" + encodeURIComponent($('sample_select_table_view').value) +
#        "&delimiters=" + encodeURIComponent($('misc_download_delimiters').value) +
#        "&lineend=" + encodeURIComponent($('misc_download_lineend').value) +
#        "&headerlang=" + encodeURIComponent($('misc_settings_header_language').value);
        
#"sample_std",
#"sample_hyd",
#"sample_martrans",
#"sample_bio_agg",

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        # Labels
        label00 = QtGui.QLabel("Year")
        label01 = QtGui.QLabel("-")
        label02 = QtGui.QLabel("Datatype")
        label03 = QtGui.QLabel("Project")
        label04 = QtGui.QLabel("Month")
        label05 = QtGui.QLabel("Parameter")
        label06 = QtGui.QLabel("Orderer")
        label07 = QtGui.QLabel("Deliverer")
        label08 = QtGui.QLabel("Station")
        label09 = QtGui.QLabel("Species/taxon")
        label10 = QtGui.QLabel("Header language")
        label11 = QtGui.QLabel("Column set")
        # Row 1
        form1.addWidget(label00, 0, 0, 1, 3)
        form1.addWidget(label02, 0, 3, 1, 1)
        form1.addWidget(label03, 0, 4, 1, 2)
        # Row 2
        form1.addWidget(self.__year_from_edit, 1, 0, 1, 1)
        form1.addWidget(label01, 1, 1, 1, 1)
        form1.addWidget(self.__year_to_edit, 1, 2, 1, 1)        
        form1.addWidget(self.__datatype_edit, 1, 3, 1, 1)        
        form1.addWidget(self.__project_code_edit, 1, 4, 1, 2)
        # Row 3
        form1.addWidget(label04, 2, 0, 1, 1)
#        form1.addWidget(, 2, 0, 1, 1)
#        form1.addWidget(, 2, 0, 1, 1)
        form1.addWidget(label05, 2, 3, 1, 1)
        form1.addWidget(label06, 2, 4, 1, 1)
        form1.addWidget(label07, 2, 5, 1, 1)
        # Row 4
        form1.addWidget(self.__month_edit, 3, 0, 1, 3)
        form1.addWidget(self.__parameter_edit, 3, 3, 1, 1)
        form1.addWidget(self.__orderer_edit, 3, 4, 1, 1)
        form1.addWidget(self.__deliverer_edit, 3, 5, 1, 1)
        # Row 5
        form1.addWidget(label08, 4, 3, 1, 1)
        # Row 6
        form1.addWidget(self.__station_name_edit, 5, 3, 1, 2)
        form1.addWidget(self.__station_name_option_edit, 5, 5, 1, 1)
        # Row 7
        form1.addWidget(label09, 6, 3, 1, 1)
        # Row 8
        form1.addWidget(self.__taxon_name_edit, 7, 3, 1, 2)
        form1.addWidget(self.__taxon_name_option_edit, 7, 5, 1, 1)
        # Row 9
        form1.addWidget(label10, 8, 4, 1, 1)
        form1.addWidget(label11, 8, 5, 1, 1)
        # Row 10
        form1.addWidget(self.__headerlang_edit, 9, 4, 1, 1)
        form1.addWidget(self.__sample_table_view_edit, 9, 5, 1, 1)
        # Row 10
        form1.addWidget(self.__get_data_button, 10, 5, 1, 1)

#        datalayout = QtGui.QVBoxLayout()
#        datalayout.addLayout(form1)
#        selectionbox.setLayout(datalayout)
        selectionbox.setLayout(form1)
        
        # === GroupBox: resultbox === 
        resultbox = QtGui.QGroupBox("Result table", self)
        # Active widgets and connections.
        self.__tableView = QtGui.QTableView()
        self.__tableView.setAlternatingRowColors(True)
        self.__tableView.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self.__tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # Model, data nad selection        
        self.__dataset = pw_monitoring_files.SharkwebDownload()
        self.__model = ResultTableModel(self.__dataset)
        self.__tableView.setModel(self.__model)        
        selectionModel = QtGui.QItemSelectionModel(self.__model, self.__tableView)
        self.__tableView.setSelectionModel(selectionModel)
#        self.__tableView.resizeColumnsToContents()
#        self.__tableView.resizeRowsToContents()
        #
        self.connect(selectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.__test)
        self.connect(selectionModel, QtCore.SIGNAL("selectionChanged(QModelIndex, QModelIndex)"), self.__test2)
        
        # Layout widgets.
        resultlayout = QtGui.QVBoxLayout()
#        resultlayout.addLayout(self.__tableView)
        resultlayout.addWidget(self.__tableView)
        resultbox.setLayout(resultlayout)

        
        # === Main level layout. ===
        content = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addWidget(selectionbox)
        contentLayout.addWidget(resultbox)
#        contentLayout.addStretch(5)
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)

    def __refreshTable(self):
        """ """
        self.__model.reset() # Model data has changed.
#        self.__tableView.resizeColumnsToContents()
#        self.__tableView.resizeRowsToContents()

    def __getData(self):
        """ """
        self.__dataset.clear()
        self.__refreshTable()
        QtGui.QApplication.processEvents()
        
        parameters = {}
        parameters['action'] = unicode('download_sample') # Not json
#        parameters['action'] = unicode('get_sample_table') # Json
        parameters['bounds'] = unicode('')
        parameters['year_from'] = unicode(self.__year_from_edit.text())
        parameters['year_to'] = unicode(self.__year_to_edit.text())
        parameters['month'] = unicode(self.__month_edit.text())
        parameters['datatype'] = unicode(self.__datatype_edit.text())
        parameters['parameter'] = unicode(self.__parameter_edit.text())
        parameters['project_code'] = unicode(self.__project_code_edit.text())
        parameters['orderer'] = unicode(self.__orderer_edit.text())
#        parameters['deliverer'] = unicode(self.__deliverer_edit.text()
        parameters['station_name'] = unicode(self.__station_name_edit.text())
        parameters['station_name_option'] = unicode(self.__station_name_option_edit.text())
        parameters['taxon_name'] = unicode(self.__taxon_name_edit.text())
        parameters['taxon_name_option'] = unicode(self.__taxon_name_option_edit.text())
        parameters['sample_table_view'] = unicode(self.__sample_table_view_edit.text())
        parameters['delimiters'] = unicode(self.__delimiters_edit.text())
        parameters['lineend'] = unicode(self.__lineend_edit.text())
        parameters['limit'] = unicode(self.__limit_edit.text())
        parameters['headerlang'] = unicode(self.__headerlang_edit.text())
        # Get data.
        self.__dataset.readData(parameters)
        self.__refreshTable()

    def __test(self, index):
        """ """
        print("TEST..." + "%f" % index.row())

    def __test2(self, index, index2):
        """ """
        print("TEST2..." + "%f" % index.row() + " %f" % index.column())


class ResultTableModel(QtCore.QAbstractTableModel):
    def __init__(self, dataset):
        super(ResultTableModel, self).__init__()
        self.__dataset = dataset
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self.__dataset.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        return self.__dataset.getColumnCount() + 1 # First column for row number.

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section > 0: # First column for row number.
                return QtCore.QVariant(self.__dataset.getHeader(section - 1))
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                if index.column() == 0: # First column for row number.
                    return  QtCore.QVariant(index.row() + 1)
                return QtCore.QVariant(self.__dataset.getData(index.row(), index.column() - 1))
        return QtCore.QVariant()
