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
"""

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync

import mmfw

class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self.__datasettabledata = DatasetTableData()
        self.__lastusedphytowinfilename = u''
        # Initialize parent.
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self.__activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self.__activityheader.setTextFormat(QtCore.Qt.RichText)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self.__activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self.__contentLoadDataset())
        contentLayout.addWidget(self.__contentLoadedDatasets(), 10)
#        contentLayout.addStretch(5)
        # Style.
        self.__activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
#        self.setStyleSheet(""" 
#            QLabel#self.__activityheader { color: white; background-color: #00677f; }
#            """)
    
    def __contentLoadDataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Load dataset", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.__contentTextfile(), "Text files (*.txt)")
        tabWidget.addTab(self.__contentXlsx(), "Excel files (*.xlsx)")
#        tabWidget.addTab(self.__contentPhytowin(), "Phytowin files (*.csv)")
#        tabWidget.addTab(self.__contentSharkweb(), "Sharkweb (http://sharkweb.smhi.se)")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== TEXT FILES ======
    def __contentTextfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        
        
        
        
        
#        self.__textfile_edit = QtGui.QLineEdit("C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/2009_SMHI_PP_version-2010-11-16_data.txt")
        self.__textfile_edit = QtGui.QLineEdit("2009_SMHI_PP_version-2010-11-16_data.txt")
        
        
        
        
        
        self.__textfilebrowse_button = QtGui.QPushButton("Browse...")
        self.__textfileload_button = QtGui.QPushButton("Load dataset")
        #
        self.connect(self.__textfilebrowse_button, QtCore.SIGNAL("clicked()"), self.__textFileBrowse)              
        self.connect(self.__textfileload_button, QtCore.SIGNAL("clicked()"), self.__loadTextFile)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__textfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__textfilebrowse_button, gridrow, 10, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__textfileload_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget
        
    def __textFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__textfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__textfile_edit.setText(filepath)

    def __loadTextFile(self):
        """ """
        
        # TODO: MMFW:
        dataset = mmfw.DatasetNode()
        # TODO: Should be replaced by call to "export_matrix.xlsx".
#        exporttablecolumns = \
#            [{"Header": "YEAR", "Node": "Visit", "Key": "Visit year"},
#             {"Header": "SDATE", "Node": "Visit", "Key": "Visit date"},
#             {"Header": "MXDEP", "Node": "Sample", "Key": "Sample max depth"}]
#        dataset.setExportTableColumns(exporttablecolumns)
        
        
#        dataset.loadExportTableInfo(u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/mmfw/data/templates/pp_export_matrix.xlsx',
#                                    u'PP export')
        dataset.loadImportExportMatrix(u'mmfw_data/matrices/pp_matrix.xlsx',
                                       u'PP import',
                                       u'PP export')
        
        
        
        
        
        
        
        #
        dataset.addMetadata(u'File name', os.path.basename(unicode(self.__textfile_edit.text())))
        dataset.addMetadata(u'File path', unicode(self.__textfile_edit.text()))
        #
        impMgr = mmfw.ImportManager()
        impMgr.importFileToDataset(dataset, unicode(self.__textfile_edit.text()))
        # Note: Not mmfw datasets.
        toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        
        
        
        
        
        
        
        
        
        
#        dataset = monitoring_files.TextFile()
#        dataset.readFile(unicode(self.__textfile_edit.text()))
#        toolbox_datasets.ToolboxDatasets().addDataset(dataset)        

    # ===== EXCEL FILES ======
    def __contentXlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        # Intro:
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        # Select import/export matrix:
        self.__excel_matrix_list = QtGui.QComboBox()
        self.__excel_matrix_list.addItems(["<select>"])
#        self.connect(self.__excel_matrix_list, QtCore.SIGNAL("currentIndexChanged(int)"), self.__matrixSelected())                
        
        # Select import column:
        self.__excel_importcolumn_list = QtGui.QComboBox()
        self.__excel_importcolumn_list.addItems(["<select>"])
        
        # Select export column:
        self.__excel_exportcolumn_list = QtGui.QComboBox()
        self.__excel_exportcolumn_list.addItems(["<select>"])
        
        # Load dataset.
        self.__excel_getdataset_button = QtGui.QPushButton("Load dataset")
        self.connect(self.__excel_getdataset_button, QtCore.SIGNAL("clicked()"), self.__getExcelFile)                
        
        
        
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select matrix:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_matrix_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel("Select import column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel("Select export column:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__excel_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__excel_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(7)
        layout.addLayout(hbox1)
        widget.setLayout(layout)        
        
#        self.__xlsxfile_edit = QtGui.QLineEdit("")
#        self.__xlsxfilebrowse_button = QtGui.QPushButton("Browse...")
#        self.__xlsxfilegetdata_button = QtGui.QPushButton("Load dataset")
#        #
#        self.connect(self.__xlsxfilebrowse_button, QtCore.SIGNAL("clicked()"), self.__xlsxFileBrowse)              
#        self.connect(self.__xlsxfilegetdata_button, QtCore.SIGNAL("clicked()"), self.__getXlsxFile)                
#        # Layout widgets.
#        form1 = QtGui.QGridLayout()
#        gridrow = 0
#        label1 = QtGui.QLabel("From file (.xlsx):")
#        form1.addWidget(label1, gridrow, 0, 1, 1)
#        form1.addWidget(self.__xlsxfile_edit, gridrow, 1, 1, 9)
#        form1.addWidget(self.__xlsxfilebrowse_button, gridrow, 10, 1, 1)
#        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
#        hbox1.addWidget(self.__xlsxfilegetdata_button)
#        #
#        layout = QtGui.QVBoxLayout()
#        layout.addWidget(introlabel)
#        layout.addLayout(form1)
#        layout.addStretch(7)
#        layout.addLayout(hbox1)
#        widget.setLayout(layout)
        #
        return widget


    def __getExcelFile(self):
        """ """
        dataset = mmfw.DatasetNode()
        #
        #
        #
        dataset.loadImportExportMatrix(u'mmfw_data/matrices/hyd_matrix.xlsx',
                                       u'HYD Excel import',
                                       u'HYD export short')
        #
        #
        #
        excelfile = u'Y_lan_Format_hydrografi_regionaladata_2006.xlsx'
        
        
        
        #
        dataset.addMetadata(u'File name', os.path.basename(unicode(excelfile)))
        dataset.addMetadata(u'File path', unicode(excelfile))
        #
        impMgr = mmfw.ImportManager()
        impMgr.importExcelFileToDataset(dataset, unicode(excelfile))
        # Note: Not mmfw datasets.
        toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
        
        
#    def __xlsxFileBrowse(self):
#        """ """
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setDirectory(unicode(self.__xlsxfile_edit.text()))
#        filepath = dirdialog.getOpenFileName()
#        if filepath:
#            self.__xlsxfile_edit.setText(filepath)
#
#    def __getXlsxFile(self):
#        """ """
#        dataset = monitoring_files.ExcelXlsxFile()
#        dataset.readFile(unicode(self.__xlsxfile_edit.text()))
#        toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
    
#    # =====PHYTOWIN FILES ======
#    def __contentPhytowin(self):
#        """ """
#        introlabel = utils_qt.RichTextQLabel()
#        introlabel.setText("""
#        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
#        tempor incididunt ut labore et dolore magna aliqua.
#        """)
#        # Active widgets and connections.
##        self.__pwfromdirectory_edit = QtGui.QLineEdit("") # TODO: Use toolbox settings.
###        self.__pwfromdirectory_edit = QtGui.QLineEdit("../../../../data/planktondata/phytowin_files") # TODO: Use toolbox settings.
##        self.__pwfromdirectory_button = QtGui.QPushButton("Browse...")
##        #
##        self.__datasets_table = QtGui.QTableWidget()
##        self.__datasets_table.setAlternatingRowColors(True)
##        self.__datasets_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
##        self.__datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
##        self.__datasets_table.verticalHeader().setDefaultSectionSize(18)
##        self.__datasets_table.setColumnCount(1)
##        self.__datasets_table.horizontalHeader().setStretchLastSection(True)
##        self.__datasets_table.setHorizontalHeaderLabels(["File"])
##        self.__getpwdata_button = QtGui.QPushButton("Get data")
#        self.__loadphytowindata_button = QtGui.QPushButton("Load dataset(s)")
#        #
##        self.connect(self.__pwfromdirectory_button, QtCore.SIGNAL("clicked()"), self.__pwFromDirectoryBrowse)                
##        self.connect(self.__getpwdata_button, QtCore.SIGNAL("clicked()"), self.__getPwData)                
#
#        
#        self.connect(self.__loadphytowindata_button, QtCore.SIGNAL("clicked()"), self.__loadPhytowinDatasets)                
#        
#        
#        
#        # Layout widgets.
##        form1 = QtGui.QGridLayout()
##        gridrow = 0
##        label1 = QtGui.QLabel("From directory:")
##        form1.addWidget(label1, gridrow, 0, 1, 1)
##        form1.addWidget(self.__pwfromdirectory_edit, gridrow, 1, 1, 9)
##        form1.addWidget(self.__pwfromdirectory_button, gridrow, 10, 1, 1)
##        gridrow += 1
##        label2 = QtGui.QLabel("Files (CSV):")
##        form1.addWidget(label2, gridrow, 0, 1, 1)
##        form1.addWidget(self.__datasets_table, gridrow, 1, 10, 10)
#        #
#        hbox1 = QtGui.QHBoxLayout()
#        hbox1.addStretch(5)
##        hbox1.addWidget(self.__getpwdata_button)
#        hbox1.addWidget(self.__loadphytowindata_button)
#        #
#        widget = QtGui.QWidget()        
#        layout = QtGui.QVBoxLayout()
#        widget.setLayout(layout)
##        layout.addLayout(form1)
#        layout.addWidget(introlabel)
#        layout.addStretch(5)
#        layout.addLayout(hbox1)
#        #
#        return widget
#        
#    def __pwFromDirectoryBrowse(self):
#        """ """
#        # Show directory dialog box.
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
#        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
#        dirdialog.setDirectory(unicode(self.__pwfromdirectory_edit.text()))
#        dirpath = dirdialog.getExistingDirectory()
#        # Check if user pressed ok or cancel.
#        if dirpath:
#            self.__pwfromdirectory_edit.setText(dirpath)
#            toolbox_datasets.ToolboxDatasets.clear()
#            # Add files in selected directory to QTableWidget.
#            for row, filename in enumerate(sorted(os.listdir(unicode(self.__pwfromdirectory_edit.text())))):
#                if os.path.splitext(unicode(filename))[1] in ['.csv', '.CSV']:
#                    self.__datasets_table.setRowCount(row + 1)
#                    item = QtGui.QTableWidgetItem(unicode(filename))
#                    item.setCheckState(QtCore.Qt.Unchecked)
#                    self.__datasets_table.setItem(row, 0, item)            
#        
#    def __getPwData(self):
#        """ """
#        self.__dataset.clear()
#        self.__refreshResultTable()
#        QtGui.QApplication.processEvents()
#        #
#        self.__dataset = monitoring_files.PwCsvTable()
#        self.__model.setDataset(self.__dataset)
#        #
#        for index in range(self.__datasets_table.rowCount()):
#            item = self.__datasets_table.item(index, 0)
#            if item.checkState(): # Check if selected by user.
#                # When reading from a table the display rule must be used.
#                filename = unicode(item.data(QtCore.Qt.DisplayRole).toString())
#                print(unicode(self.__pwfromdirectory_edit.text()))
#                print(filename)
#                self.__dataset.readFile(self.__pwfromdirectory_edit.text() + '/' + filename)
#        #        
#        self.__refreshResultTable()
#
#    def __loadPhytowinDatasets(self):
#        """ """
#
#        # Show select file dialog box. Multiple files can be selected.
#        namefilter = 'Phytowin files (*.csv);;All files (*.*)'
#        filenames = QtGui.QFileDialog.getOpenFileNames(
#                            self,
#                            'Load Phytowin dataset(s)',
#                            self.__lastusedphytowinfilename,
#                            namefilter)
#        filenames = unicode(filenames) # QString to unicode.
#        # Check if user pressed ok or cancel.
#        if filenames:
#            for filename in filenames:
#                self.__lastusedphytowinfilename = filename
#                dataset = monitoring_files.PwCsvTable()
#                dataset.readFile(filename)
#                toolbox_datasets.ToolboxDatasets().addDataset(dataset)        
#        
#        
#        
##        self.__dataset = monitoring_files.PwCsvTable()
##        self.__model.setDataset(self.__dataset)
##        #
##        for index in range(self.__datasets_table.rowCount()):
##            item = self.__datasets_table.item(index, 0)
##            if item.checkState(): # Check if selected by user.
##                # When reading from a table the display rule must be used.
##                filename = unicode(item.data(QtCore.Qt.DisplayRole).toString())
##                print(self.__pwfromdirectory_edit.text())
##                print(filename)
##                self.__dataset.readFile(self.__pwfromdirectory_edit.text() + '/' + filename)
#        #        

#    # ===== SHARKWEB ======
#    def __contentSharkweb(self):
#        """ 
#        Code sample from Javascript:
#            var action = 'download_sample';
#            var url = "shark_save.php?action=" + action + 
#                "&bounds=" + encodeURIComponent(getBounds()) +
#                "&year_from=" + encodeURIComponent($('sample_select_year_from').value) +
#                "&year_to=" + encodeURIComponent($('sample_select_year_to').value) +
#                "&month=" + encodeURIComponent(get_selected_month_list()) +
#                "&datatype=" + encodeURIComponent($('sample_select_datatype').value) +
#                "&parameter=" + encodeURIComponent($('sample_select_parameter').value) +
#                "&project_code=" + encodeURIComponent($('sample_select_project_code').value) +
#                "&orderer=" + encodeURIComponent($('sample_select_orderer').value) +
#                "&station_name=" + encodeURIComponent($('sample_select_station_name').value) +
#                "&station_name_option=" + encodeURIComponent($('sample_select_station_name_option').value) +
#                "&taxon_name=" + encodeURIComponent($('sample_select_taxon').value) +
#                "&taxon_name_option=" + encodeURIComponent($('sample_select_taxon_option').value) +
#                "&sample_table_view=" + encodeURIComponent($('sample_select_table_view').value) +
#                "&delimiters=" + encodeURIComponent($('misc_download_delimiters').value) +
#                "&lineend=" + encodeURIComponent($('misc_download_lineend').value) +
#                "&headerlang=" + encodeURIComponent($('misc_settings_header_language').value);
#                // sample_table_view alternatives:
#                // "sample_std",
#                // "sample_hyd",
#                // "sample_martrans",
#                // "sample_bio_agg",
#        """
#        # Active widgets and connections.
#        introlabel = utils_qt.RichTextQLabel()
#        introlabel.setText("""
#        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
#        tempor incididunt ut labore et dolore magna aliqua.
#        """)
#        self.__bounds_edit = QtGui.QLineEdit("")
#        self.__year_from_edit = QtGui.QLineEdit("2008")
#        self.__year_to_edit = QtGui.QLineEdit("2008")
#        self.__month_edit = QtGui.QLineEdit("06")
#        self.__datatype_edit = QtGui.QLineEdit("Phytoplankton")
#        self.__parameter_edit = QtGui.QLineEdit("CONC")
##        self.__project_code_edit = QtGui.QLineEdit("")
##        self.__orderer_edit = QtGui.QLineEdit("")
##        self.__deliverer_edit = QtGui.QLineEdit("")
##        self.__station_name_edit = QtGui.QLineEdit(u'släggö, by15')
##        self.__station_name_option_edit = QtGui.QLineEdit("station_list")
##        self.__taxon_name_edit = QtGui.QLineEdit("Dinophyceae")
##        self.__taxon_name_option_edit = QtGui.QLineEdit("class")
###        self.__sample_table_view_edit = QtGui.QLineEdit("sample_std")
##        self.__sample_table_view_edit = QtGui.QLineEdit("sample_col_bio")
##        self.__delimiters_edit = QtGui.QLineEdit("point-tab")
##        self.__lineend_edit = QtGui.QLineEdit("unix")
##        self.__limit_edit = QtGui.QLineEdit("2000")
##        self.__headerlang_edit = QtGui.QLineEdit("sv")
#        #
#        self.__get_data_button = QtGui.QPushButton("Load dataset")
#        self.connect(self.__get_data_button, QtCore.SIGNAL("clicked()"), self.__getSharkwebData)                
#        # Layout widgets.
#        form1 = QtGui.QGridLayout()
#        gridrow = 0
#        label00 = QtGui.QLabel("Year")
#        label01 = QtGui.QLabel("-")
#        label02 = QtGui.QLabel("Datatype")
##        label03 = QtGui.QLabel("Project")
#        label04 = QtGui.QLabel("Month")
#        label05 = QtGui.QLabel("Parameter")
##        label06 = QtGui.QLabel("Orderer")
##        label07 = QtGui.QLabel("Deliverer")
##        label08 = QtGui.QLabel("Station")
##        label09 = QtGui.QLabel("Species/taxon")
##        label10 = QtGui.QLabel("Header language")
##        label11 = QtGui.QLabel("Column set")
#        gridrow += 1
#        form1.addWidget(label00, gridrow, 0, 1, 3)
#        form1.addWidget(label02, gridrow, 3, 1, 1)
##        form1.addWidget(label03, gridrow, 4, 1, 2)
#        gridrow += 1
#        form1.addWidget(self.__year_from_edit, gridrow, 0, 1, 1)
#        form1.addWidget(label01, gridrow, 1, 1, 1)
#        form1.addWidget(self.__year_to_edit, gridrow, 2, 1, 1)        
#        form1.addWidget(self.__datatype_edit, gridrow, 3, 1, 1)        
##        form1.addWidget(self.__project_code_edit, gridrow, 4, 1, 2)
#        gridrow += 1
#        form1.addWidget(label04, gridrow, 0, 1, 1)
#        form1.addWidget(label05, gridrow, 3, 1, 1)
##        form1.addWidget(label06, gridrow, 4, 1, 1)
##        form1.addWidget(label07, gridrow, 5, 1, 1)
#        gridrow += 1
#        form1.addWidget(self.__month_edit, gridrow, 0, 1, 3)
#        form1.addWidget(self.__parameter_edit, gridrow, 3, 1, 1)
##        form1.addWidget(self.__orderer_edit, gridrow, 4, 1, 1)
##        form1.addWidget(self.__deliverer_edit, gridrow, 5, 1, 1)
##        gridrow += 1
##        form1.addWidget(label08, gridrow, 3, 1, 1)
##        gridrow += 1
##        form1.addWidget(self.__station_name_edit, gridrow, 3, 1, 2)
##        form1.addWidget(self.__station_name_option_edit, gridrow, 5, 1, 1)
##        gridrow += 1
##        form1.addWidget(label10, gridrow, 0, 1, 1)
##        form1.addWidget(label11, gridrow, 2, 1, 1)
##        form1.addWidget(label09, gridrow, 3, 1, 1)
##        gridrow += 1
##        form1.addWidget(self.__headerlang_edit, gridrow, 0, 1, 1)
##        form1.addWidget(self.__sample_table_view_edit, gridrow, 2, 1, 1)
##        form1.addWidget(self.__taxon_name_edit, gridrow, 3, 1, 2)
##        form1.addWidget(self.__taxon_name_option_edit, gridrow, 5, 1, 1)
#        gridrow += 1
#        form1.addWidget(self.__get_data_button, gridrow, 5, 1, 1)
#        #
##        hbox1 = QtGui.QHBoxLayout()
##        hbox1.addStretch(5)
##        hbox1.addWidget(self.__get_data_button)
#        # Layout widgets.
#        widget = QtGui.QWidget()        
#        layout = QtGui.QVBoxLayout()
#        layout.addWidget(introlabel)
#        widget.setLayout(layout)
#        layout.addLayout(form1)
##        layout.addLayout(hbox1)
#        #
#        return widget
#
#    def __getSharkwebData(self):
#        """ """
#        dataset = monitoring_files.SharkwebDownload()
#        #
#        parameters = {}
##        parameters['action'] = unicode('download_sample') # Not json
###        parameters['action'] = unicode('get_sample_table') # Json
##        parameters['bounds'] = unicode('')
#        parameters['year_from'] = unicode(self.__year_from_edit.text())
#        parameters['year_to'] = unicode(self.__year_to_edit.text())
#        parameters['month'] = unicode(self.__month_edit.text())
#        parameters['datatype'] = unicode(self.__datatype_edit.text())
#        parameters['parameter'] = unicode(self.__parameter_edit.text())
##        parameters['project_code'] = unicode(self.__project_code_edit.text())
##        parameters['orderer'] = unicode(self.__orderer_edit.text())
###        parameters['deliverer'] = unicode(self.__deliverer_edit.text()
##        parameters['station_name'] = unicode(self.__station_name_edit.text())
##        parameters['station_name_option'] = unicode(self.__station_name_option_edit.text())
##        parameters['taxon_name'] = unicode(self.__taxon_name_edit.text())
##        parameters['taxon_name_option'] = unicode(self.__taxon_name_option_edit.text())
##        parameters['sample_table_view'] = unicode(self.__sample_table_view_edit.text())
##        parameters['delimiters'] = unicode(self.__delimiters_edit.text())
##        parameters['lineend'] = unicode(self.__lineend_edit.text())
##        parameters['limit'] = unicode(self.__limit_edit.text())
##        parameters['headerlang'] = unicode(self.__headerlang_edit.text())
#        # Get data.
#        dataset.getData(parameters)
#
#        toolbox_datasets.ToolboxDatasets().addDataset(dataset)   
#        
#             
##        self.__dataset.clear()
##        self.__refreshResultTable()
##        QtGui.QApplication.processEvents()
##        #
##        self.__dataset = monitoring_files.SharkwebDownload()
##        self.__model.setDataset(self.__dataset)
##        #
##        parameters = {}
##        parameters['action'] = unicode('download_sample') # Not json
###        parameters['action'] = unicode('get_sample_table') # Json
##        parameters['bounds'] = unicode('')
##        parameters['year_from'] = unicode(self.__year_from_edit.text())
##        parameters['year_to'] = unicode(self.__year_to_edit.text())
##        parameters['month'] = unicode(self.__month_edit.text())
##        parameters['datatype'] = unicode(self.__datatype_edit.text())
##        parameters['parameter'] = unicode(self.__parameter_edit.text())
##        parameters['project_code'] = unicode(self.__project_code_edit.text())
##        parameters['orderer'] = unicode(self.__orderer_edit.text())
###        parameters['deliverer'] = unicode(self.__deliverer_edit.text()
##        parameters['station_name'] = unicode(self.__station_name_edit.text())
##        parameters['station_name_option'] = unicode(self.__station_name_option_edit.text())
##        parameters['taxon_name'] = unicode(self.__taxon_name_edit.text())
##        parameters['taxon_name_option'] = unicode(self.__taxon_name_option_edit.text())
##        parameters['sample_table_view'] = unicode(self.__sample_table_view_edit.text())
##        parameters['delimiters'] = unicode(self.__delimiters_edit.text())
##        parameters['lineend'] = unicode(self.__lineend_edit.text())
##        parameters['limit'] = unicode(self.__limit_edit.text())
##        parameters['headerlang'] = unicode(self.__headerlang_edit.text())
##        # Get data.
##        self.__dataset.getData(parameters)
##        self.__refreshResultTable()


    # ===== LOADED DATASETS =====    
    def __contentLoadedDatasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Loaded datasets", self)
        #
        self.__datasets_table = utils_qt.ToolboxQTableView()
        self.__datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        
        
        self.__datasettabledata.clear()
        self.__datasettabledata.setHeader([u'Dataset      ', 
                                           u'Type         ', 
                                           u'Content      ', 
                                           u'File         ', 
                                           u'File path    ',
                                           u'Matrix       ',
                                           u'Import column',
                                           u'Export column'])
        self.__datasets_table.tablemodel.setModeldata(self.__datasettabledata)
        self.__datasets_table.resizeColumnsToContents()
        
        self.__datasets_table.selectionModel.Rows
        
        
        
#        self.__datasets_table = QtGui.QTableWidget()
#        self.__datasets_table.setAlternatingRowColors(True)
#        self.__datasets_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self.__datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        self.__datasets_table.verticalHeader().setDefaultSectionSize(18)
#        self.__datasets_table.setColumnCount(1)
#        self.__datasets_table.horizontalHeader().setStretchLastSection(True)
#        self.__datasets_table.setHorizontalHeaderLabels(["Dataset filename"])
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL("datasetListChanged"), 
             self.__updateDatasetList)
        # Connection for selected row.
        self.connect(self.__datasets_table.selectionModel, 
                     QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), 
                     self.__selectionChanged)                
        # Buttons.
        self.__unloadalldatasets_button = QtGui.QPushButton("Unload all datasets")
        self.__unloadmarkeddatasets_button = QtGui.QPushButton("Unload marked dataset(s)")
        # Button connections.
        self.connect(self.__unloadalldatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadAllDatasets)                
        self.connect(self.__unloadmarkeddatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadMarkedDatasets)                
        # Layout widgets.
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self.__unloadalldatasets_button)
        buttonlayout.addWidget(self.__unloadmarkeddatasets_button)
        buttonlayout.addStretch(5)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self.__datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def __unloadAllDatasets(self):
        """ """
#        # TODO: MMFW:
#        mmfw.Datasets().clear()

        
        toolbox_datasets.ToolboxDatasets().clear()

    def __unloadMarkedDatasets(self):
        """ """
        
        ###self.columnView.selectionModel().selection().indexes()
        ###tableView->currentIndex()
        ###tableView->selectionModel()->currentIndex()

        # Remove datasets, start with the last one. 
        rowcount = self.__datasets_table.tablemodel.rowCount()
        for rowindex in range(rowcount):
#            item = self.__datasets_table.item(rowcount - rowindex - 1, 0)
#            if item.checkState(): # Check if selected by user.
            if self.__datasets_table.selectionModel.isSelected(self.__datasets_table.tablemodel.createIndex(rowindex, 0)): # Check if selected by user.
                # TODO: MMFW:
                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

                
#                toolbox_datasets.ToolboxDatasets().removeDatasetByIndex(rowcount - rowindex - 1)

    def __updateDatasetList(self):
        """ """
        
        
        # TODO: MMFW:
        self.__datasettabledata.clearRows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            # Get content info depending on dataset type.
            datasettype = u'',
            contentinfo = u''
            if isinstance(dataset, mmfw.DatasetTable):
                datasettype = u'Table dataset'
                contentinfo = u'Rows: ' + unicode(len(dataset.getRows())) + u'. '
            elif isinstance(dataset, mmfw.DatasetNode):
                datasettype = u'Tree dataset'
                visitcount, samplecound, variablecount = dataset.getCounters()
                contentinfo = u'Visits: ' + unicode(visitcount) + u', ' + \
                              u'samples: ' + unicode(samplecound) + u', ' + \
                              u'variables: ' + unicode(variablecount) + u'. '
            else:
                datasettype = u'Unspecified'

            # Add row 
            self.__datasettabledata.addRow(
                [u'Dataset - ' + unicode(rowindex),
                 datasettype,
                 contentinfo,
                 dataset.getMetadata(u'File name'),
                 dataset.getMetadata(u'File path'),
                 dataset.getMetadata(u'Matrix'),
                 dataset.getMetadata(u'Import column'),
                 dataset.getMetadata(u'Export column')])
            #
        self.__datasets_table.tablemodel.reset()
        self.__datasets_table.resizeColumnsToContents()





#        self.__datasettabledata.clearRows()
#        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
#            self.__datasettabledata.addRow([u'Dataset - ' + unicode(rowindex) + '                                       '])
#        self.__datasets_table.tablemodel.reset()
#        self.__datasets_table.resizeColumnsToContents()
    
    def __selectionChanged(self, modelIndex):
        """ """
        if modelIndex.isValid():
            print('TEST Selected row: ' + unicode(modelIndex.row()))
            toolbox_sync.ToolboxSync().setRowTest(modelIndex.row())

    
class DatasetTableData(object):
    """ """
    def __init__(self):
        """ """
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def clearRows(self):
        """ """
        self._rows = []

    def setHeader(self, header):
        """ """
        self._header = header

    def addRow(self, row):
        """ """
        self._rows.append(row)

    def getHeaderItem(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def getDataItem(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def getColumnCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return ''

    def getRowCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return ''
