#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
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

import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources
import plankton_toolbox.core.monitoring.pw_monitoring_files as pw_monitoring_files
import plankton_toolbox.core.monitoring.pw_reports as pw_reports

###class PwReportsActivity(activity_base.ActivityBase):
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
        # === GroupBox: databox === 
        databox = QtGui.QGroupBox("Select data files", self)
        # Active widgets and connections.
        
        
        
#        self.__fromdirectory_edit = QtGui.QLineEdit("")
        self.__fromdirectory_edit = QtGui.QLineEdit("../../../../data/planktondata/phytowin_files")

        
        
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
        self.__pegfile_edit = QtGui.QLineEdit("planktondata/resources/smhi_extended_peg.json")
        self.__pegfile_button = QtGui.QPushButton("Browse...")
        self.__translatefile_edit = QtGui.QLineEdit("planktondata/resources/smhi_pw_to_extended_peg.txt")
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
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self.__fromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self.__fromdirectory_edit.setText(dirpath)
            self._samplefiles.clear()
            self.__files_table.setColumnCount(1)
            self.__files_table.horizontalHeader().setStretchLastSection(True)
            # Add files in selected directory to QTableWidget.
            for row, filename in enumerate(os.listdir(unicode(self.__fromdirectory_edit.text()))):
                if os.path.splitext(unicode(filename))[1] in ['.csv', '.CSV']:
                    self.__files_table.setRowCount(row + 1)
                    item = QtGui.QTableWidgetItem(unicode(filename))
                    item.setCheckState(QtCore.Qt.Unchecked)
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
        if self.__report_list.currentIndex() == 0:
            QtGui.QMessageBox.information(self, "Info", 'Report type must be selected.')
            return        
        utils.Logger().info("PW reports. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Generating PW report.")
        try:
            # Add selected files to filelist.
            self._samplefiles.clear()                
            for index in range(self.__files_table.rowCount() - 1):
#            for item in self.__files_table.items():
                item = self.__files_table.item(index, 0)
                if item.checkState(): # Check if selected by user.
                    # When reading from a table the display rule must be used.
                    key = unicode(item.data(QtCore.Qt.DisplayRole).toString())
                    self._samplefiles[key] = None # With no data.
            # Read files and add data as values in the sample file list.        
            for samplefile in self._samplefiles:                
                utils.Logger().info('Reading ' + samplefile + '...')        
                sampledata = pw_monitoring_files.PwCsv()
                sampledata.importFile(unicode(self.__fromdirectory_edit.text()) + '/' + samplefile, encoding = 'iso-8859-1')
                self._samplefiles[samplefile] = sampledata  # With data.
            # Check which report to generate.        
            if self.__report_list.currentIndex() == 1:
                # === Report: MJ1 ===
                utils.Logger().info("Selected report: MJ1")
#                peg = taxa.Peg()
#                importer = taxa_sources.JsonFile(taxaObject = peg)
#                importer.importTaxa(file = unicode(self.__pegfile_edit.text()))
                # Create exporter object.
                report = pw_reports.PwReportMJ1()
#                utils.Logger().info("Used PEG list: " + unicode(self.__pegfile_edit.text()))
#                utils.Logger().info("Used translation file: " + unicode(self.__translatefile_edit.text()))
#                report.setPeg(peg)
#                report.setTaxonSizeClassTranslationFile(unicode(self.__translatefile_edit.text()))
                report.exportFile(self._samplefiles, unicode(self.__tofile_edit.text()))
            elif self.__report_list.currentIndex() == 2:
                # === Report: MJ1 ===
                utils.Logger().info("Selected report: MJ2")
#                peg = taxa.Peg()
#                importer = taxa_sources.JsonFile(taxaObject = peg)
#                importer.importTaxa(file = unicode(self.__pegfile_edit.text()))
                # Create exporter object.
                report = pw_reports.PwReportMJ1()
#                utils.Logger().info("Used PEG list: " + unicode(self.__pegfile_edit.text()))
#                utils.Logger().info("Used translation file: " + unicode(self.__translatefile_edit.text()))
#                report.setPeg(peg)
#                report.setTaxonSizeClassTranslationFile(unicode(self.__translatefile_edit.text()))
                report.exportFile(self._samplefiles, unicode(self.__tofile_edit.text()))
            elif self.__report_list.currentIndex() == 3:
                # === Report: MJ1 ===
                utils.Logger().info("Selected report: ATS1")
#                peg = taxa.Peg()
#                importer = taxa_sources.JsonFile(taxaObject = peg)
#                importer.importTaxa(file = unicode(self.__pegfile_edit.text()))
                # Create exporter object.
                report = pw_reports.PwReportMJ1()
#                utils.Logger().info("Used PEG list: " + unicode(self.__pegfile_edit.text()))
#                utils.Logger().info("Used translation file: " + unicode(self.__translatefile_edit.text()))
#                report.setPeg(peg)
#                report.setTaxonSizeClassTranslationFile(unicode(self.__translatefile_edit.text()))
                report.exportFile(self._samplefiles, unicode(self.__tofile_edit.text()), encoding = 'iso-8859-1')
            else:
                raise UserWarning('The selected report type is not implemented.')
        except UserWarning, e:
            utils.Logger().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            utils.Logger().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            utils.Logger().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            utils.Logger().logAllWarnings()    
            utils.Logger().logAllErrors()    
            utils.Logger().info("PW reports. Ended.")
            self._writeToStatusBar("")


