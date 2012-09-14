#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
The Create reports activity contains the UI-part to be used when creating
reports based on datasets content. Implemented datsets/reports are:
- PW: PW-files (*.csv) can be imported and reports for MJ1, MJ2 and ATS1 can be 
      generated. These reports are stored as tab separated text files and can
      easily be edited in MS Excel or similar spreadsheet application.
       
       
"""

import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import envmonlib
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.biology.taxa as taxa
#import plankton_toolbox.core.biology.taxa_sources as taxa_sources
import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.core.monitoring.pw_reports_OLD as pw_reports_OLD

class CreateReportsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        self._samplefiles = {}
        # Initialize parent.
        super(CreateReportsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
#        self._activityheader.setStyleSheet(""" 
#            * { color: #00677f; background-color: #eaa97e; }
#            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(tabWidget)
        tabWidget.addTab(self._contentPwReport(), "PW")
        tabWidget.setTabToolTip(0, "Creates report from PW (*.csv) files.")
#        tabWidget.addTab(self._content???(), "???")

    def _contentPwReport(self):
        """ """
        # === GroupBox: databox === 
        databox = QtGui.QGroupBox("Select data files", self)
        # Active widgets and connections.
        self._fromdirectory_edit = QtGui.QLineEdit("")
        #
        self._fromdirectory_button = QtGui.QPushButton("Browse...")
        self._files_table = QtGui.QTableWidget()
        #
        self._files_table.setAlternatingRowColors(True)
        self._files_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self._files_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._files_table.verticalHeader().setDefaultSectionSize(18)
        self._files_table.setColumnCount(1)
        self._files_table.horizontalHeader().setStretchLastSection(True)
        self._files_table.setHorizontalHeaderLabels(["File"])
        #
        self.connect(self._fromdirectory_edit, QtCore.SIGNAL("editingFinished()"), self._fromDirectoryChanged)                
        self.connect(self._fromdirectory_button, QtCore.SIGNAL("clicked()"), self._fromDirectoryBrowse)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From directory:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._fromdirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._fromdirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Files (CSV):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._files_table, gridrow, 1, 10, 10)       
        datalayout = QtGui.QVBoxLayout()
        datalayout.addLayout(form1)
        databox.setLayout(datalayout)
        
        # === GroupBox: reportbox === 
        reportbox = QtGui.QGroupBox("Create report", self)
        # Active widgets and connections.
        self._report_list = QtGui.QComboBox()
        self._report_list.addItems(["<select>",
                                     "MJ Report 1 (H�vprover inom 24 timmar)",
                                     "MJ Report 2",
                                     "ATS Report 1"])

        self._todirectory_edit = QtGui.QLineEdit("")
        self._todirectory_button = QtGui.QPushButton("Browse...")
        self._tofile_edit = QtGui.QLineEdit("report.txt")
        self._createreport_button = QtGui.QPushButton("Create report")
        self.connect(self._todirectory_button, QtCore.SIGNAL("clicked()"), self._toDirectoryBrowse)                
        self.connect(self._createreport_button, QtCore.SIGNAL("clicked()"), self._createPwReport)   
        
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Report type:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._report_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To directory:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._todirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._todirectory_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("To file:")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._tofile_edit, gridrow, 1, 1, 9)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._createreport_button)
        #
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(form1)
        reportlayout.addLayout(hbox1)
        reportbox.setLayout(reportlayout)
        # === Main level layout. ===
        widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(databox)
        layout.addWidget(reportbox)
        layout.addStretch(5)
        #
        return widget
                
    def _fromDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._fromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self._fromdirectory_edit.setText(dirpath)
            self._fromDirectoryChanged()
                
    def _fromDirectoryChanged(self):
        """ """
        #
        self._files_table.clear()
        self._files_table.setHorizontalHeaderLabels(["File"])
        self._files_table.setRowCount(0)
        #
        dirpath = unicode(self._fromdirectory_edit.text())
        # Check if user pressed ok or cancel.
        if dirpath:
            self._fromdirectory_edit.setText(dirpath)
            # Add files in selected directory to QTableWidget.
            for row, filename in enumerate(os.listdir(unicode(self._fromdirectory_edit.text()))):
                if os.path.splitext(unicode(filename))[1] in ['.csv', '.CSV']:
                    self._files_table.setRowCount(row + 1)
                    item = QtGui.QTableWidgetItem(unicode(filename))
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self._files_table.setItem(row, 0, item)            
                
    def _toDirectoryBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._todirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self._todirectory_edit.setText(dirpath)
    
#    def _pegFileBrowse(self):
#        """ """
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setDirectory(unicode(self._pegfile_edit.text()))
#        filepath = dirdialog.getOpenFileName()
#        if filepath:
#            self._pegfile_edit.setText(filepath)
#
#    def _translateFileBrowse(self):
#        """ """
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setDirectory(unicode(self._translatefile_edit.text()))
#        filepath = dirdialog.getOpenFileName()
#        if filepath:
#            self._translatefile_edit.setText(filepath)
                
    def _createPwReport(self):
        """ """
        if self._report_list.currentIndex() == 0:
            QtGui.QMessageBox.information(self, "Info", 'Report type must be selected.')
            return        
        envmonlib.Logging().log("PW reports started...")
        envmonlib.Logging().startAccumulatedLogging()
        self._writeToStatusBar("Generating PW report...")
        try:
            # Add selected files to filelist.
            self._samplefiles.clear()                
            for index in range(self._files_table.rowCount()):
                item = self._files_table.item(index, 0)
                if item.checkState(): # Check if selected by user.
                    # When reading from a table the display rule must be used.
                    key = unicode(item.data(QtCore.Qt.DisplayRole).toString())
                    self._samplefiles[key] = None # With no data.
            # Read files and add data as values in the sample file list.        
            for samplefile in self._samplefiles:                
                envmonlib.Logging().log('Reading ' + samplefile + '...')        
                sampledata = monitoring_files.PwCsv()
                sampledata.readFile(unicode(self._fromdirectory_edit.text()) + '/' + samplefile)
                self._samplefiles[samplefile] = sampledata  # With data.
            # Filepath.            
            reportfilepath = ''
            if len(unicode(self._todirectory_edit.text())) > 0:
                reportfilepath = unicode(self._todirectory_edit.text()) + '/'
            reportfilepath += unicode(self._tofile_edit.text())
            # Check which report to generate.
            if self._report_list.currentIndex() == 1: # Report: MJ1
                # === Report: MJ1 ===
                envmonlib.Logging().log("Selected report: MJ1")
                report = pw_reports_OLD.PwReportMJ1()
                report.createReport(self._samplefiles, reportfilepath)
            elif self._report_list.currentIndex() == 2: # Report: MJ2
                # === Report: MJ1 ===
                envmonlib.Logging().log("Selected report: MJ2")
                report = pw_reports_OLD.PwReportMJ2()
                report.createReport(self._samplefiles, reportfilepath)
            elif self._report_list.currentIndex() == 3: # Report: ATS1
                # === Report: MJ1 ===
                envmonlib.Logging().log("Selected report: ATS1")
                report = pw_reports_OLD.PwReportATS1()
                report.createReport(self._samplefiles, reportfilepath)
            else:
                raise UserWarning('The selected report type is not implemented.')
        except UserWarning, e:
            envmonlib.Logging().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            envmonlib.Logging().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            envmonlib.Logging().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log("PW reports finished.\r\n")
            self._writeToStatusBar("")


