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

import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.utils as utils
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.monitoring.pw_monitoring_files as pw_monitoring_files
import plankton_toolbox.core.monitoring.pw_exports as pw_exports
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

class PwReportsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(PwReportsActivity, self).__init__(name, parentwidget)
        self._samplefiles = {}

    def _createContent(self):
        """ """
        # === GroupBox: databox === 
        databox = QtGui.QGroupBox("Select data files", self)
        # Active widgets and connections.
        self.__fromdirectory_edit = QtGui.QLineEdit("testdata/pwdata/")
        self.__fromdirectory_button = QtGui.QPushButton("Browse...")
        self.__files_table = QtGui.QTableWidget()
        self.connect(self.__fromdirectory_button, QtCore.SIGNAL("clicked()"), self.__fromDirectoryBrowse)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("From directory:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__fromdirectory_edit, 0, 1, 1, 9)
        form1.addWidget(self.__fromdirectory_button, 0, 10, 1, 1)
        label2 = QtGui.QLabel("Files (CSV):")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__files_table, 1, 1, 10, 10)       
        datalayout = QtGui.QVBoxLayout()
        datalayout.addLayout(form1)
        databox.setLayout(datalayout)
        
        # === GroupBox: resourcebox === 
        resourcebox = QtGui.QGroupBox("Select resources", self)
        # Active widgets and connections.
        self.__pegfile_edit = QtGui.QLineEdit("data/resources/peg.json")
        self.__pegfile_button = QtGui.QPushButton("Browse...")
        self.__translatefile_edit = QtGui.QLineEdit("data/resources/translate_pw_to_peg.json")
        self.__translatefile_button = QtGui.QPushButton("Browse...")
        self.connect(self.__pegfile_button, QtCore.SIGNAL("clicked()"), self.__pegFileBrowse)                
        self.connect(self.__translatefile_button, QtCore.SIGNAL("clicked()"), self.__translateFileBrowse)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("PEG:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__pegfile_edit, 0, 1, 1, 9)
        form1.addWidget(self.__pegfile_button, 0, 10, 1, 1)
        label2 = QtGui.QLabel("Translate PW to PEG:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__translatefile_edit, 1, 1, 1, 9)
        form1.addWidget(self.__translatefile_button, 1, 10, 1, 1)
        resourcelayout = QtGui.QVBoxLayout()
        resourcelayout.addLayout(form1)
        resourcebox.setLayout(resourcelayout)
        
        # === GroupBox: reportbox === 
        reportbox = QtGui.QGroupBox("Select report", self)
        # Active widgets and connections.
        self.__report_list = QtGui.QComboBox()
        self.__report_list.addItems(["<select>",
                                     "MJ Report 1",
                                     "MJ Report 2",
                                     "ATS Report 1"])
        self.__tofile_edit = QtGui.QLineEdit("report.txt")
        self.__createreport_button = QtGui.QPushButton("Create report")
        self.connect(self.__createreport_button, QtCore.SIGNAL("clicked()"), self.__createPwReport)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Report type:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__report_list, 0, 1, 1, 1)
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__tofile_edit, 1, 1, 1, 9)
        reportlayout = QtGui.QVBoxLayout()
        reportlayout.addLayout(form1)
        reportbox.setLayout(reportlayout)
        
        # === Button: Generate report ===
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__createreport_button)
        
        # === Main level layout. ===
        content = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addWidget(databox)
        contentLayout.addWidget(resourcebox)
        contentLayout.addWidget(reportbox)
        contentLayout.addLayout(hbox1)
        contentLayout.addStretch(5)
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)
                
    def __fromDirectoryBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self.__fromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self.__fromdirectory_edit.setText(dirpath)
            self._samplefiles.clear()
            self.__files_table.setColumnCount(1)
            self.__files_table.horizontalHeader().setStretchLastSection(True)
            for row, filename in enumerate(os.listdir(self.__fromdirectory_edit.text())):
                if os.path.splitext(filename)[1] in ['.csv', '.CSV']:
                    self.__files_table.setRowCount(row + 1)
                    item = QtGui.QTableWidgetItem(filename)
                    item.setCheckState(QtCore.Qt.Checked)
                    self.__files_table.setItem(row, 0, item)            
                
    def __pegFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegfile_edit.setText(filepath)

    def __translateFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__translatefile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__translatefile_edit.setText(filepath)
                
    def __createPwReport(self):
        """ """
        utils.Logger().info("DDD")
        try:
            self._writeToLog("Importing CSV files...")
            self._writeToStatusBar("Importing CSV files...")
            self._samplefiles.clear()
            self._samplefiles['Danafjord 2010-04-06_10-20 m.CSV'] = None
            self._samplefiles['Koljöfjord 2010--04-06-10_20m.CSV'] = None
            self._samplefiles['Kosterfjorden (NR16) 2010-04-06_10-20m.CSV'] = None
            self._samplefiles['Stretudden 2010-04-07_10-20m.CSV'] = None
            self._samplefiles['Åstol 2010-04-07_10-20m.CSV'] = None
            for samplefile in self._samplefiles:
                self._writeToLog('Reading ' + samplefile + '...')        
                sampledata = pw_monitoring_files.PwCsv()
                sampledata.importFile('testdata/pwdata/' + samplefile)
                self._samplefiles[samplefile] = sampledata
                self._writeToLog('')
        except UserWarning, e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        finally:    
            self._writeToLog("done.")
            self._writeToStatusBar("")

        """ """
        try:
            self._writeToLog("Exporting to test.csv...")
            self._writeToStatusBar("")
            # Load PEG.json
            peg = taxa.Peg()
            importer = taxa_sources.JsonFile(taxaObject = peg)
            importer.importTaxa(file = 'data/resources/peg.json')
            # Create exporter object.
            exportfile = pw_exports.ExportPw()
            exportfile.setPeg(peg)
            exportfile.exportFile(self._samplefiles, 'test_export.txt')
        except Warning, e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except StandardError, e:
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        finally:    
            self._writeToLog("done.")
            self._writeToStatusBar("")
        


