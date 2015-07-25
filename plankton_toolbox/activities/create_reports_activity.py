#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

"""


TODO: Under development.


"""


"""
The Create reports activity contains the UI-part to be used when creating
reports based on datasets content. Implemented datsets/reports are:
- PW: PW-files (*.csv) can be imported and reports for MJ1, MJ2 and ATS1 can be 
      generated. These reports are stored as tab separated text files and can
      easily be edited in MS Excel or similar spreadsheet application.
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
# import envmonlib
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.biology.taxa as taxa
#import plankton_toolbox.core.biology.taxa_sources as taxa_sources
# import plankton_toolbox.toolbox.help_texts as help_texts
import toolbox_utils
import toolbox_core

class CreateReportsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
#         self._reportdata = monitoring_files.MonitoringFiles()
        
        # Initialize parent.
        super(CreateReportsActivity, self).__init__(name, parentwidget)

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = utils_qt.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
#         tabWidget = QtGui.QTabWidget()
#         contentLayout.addWidget(tabWidget)
#         tabWidget.addTab(self._contentPwReport(), 'Phytowin')
#         tabWidget.setTabToolTip(0, 'Creates report from Phytowin files (*.csv).')
#         contentLayout.addWidget(self._contentPreview(), 10) # Stretch.
#         contentLayout.addWidget(self._contentSaveResult())
###        contentLayout.addStretch(5)
        
#     def _contentPwReport(self):
#         """ """
#         widget = QtGui.QWidget()
#         # Active widgets and connections.
# #         introlabel = utils_qt.RichTextQLabel()
# #         introlabel.setText(help_texts.HelpTexts().getText('CreateReportsActivity_intro'))
# 
#         self._report_list = QtGui.QComboBox()
#         self._report_list.addItems(['<select>',
#                                      'Combine datasets',
#                                      'Prepare for data delivery',
#                                      'MJ Report 1 (Håvprover inom 24 timmar)',
#                                      'MJ Report 2',
#                                      'ATS Report 1'])
#         self._createreport_button = QtGui.QPushButton('Create report')
#         self.connect(self._createreport_button, QtCore.SIGNAL('clicked()'), self._createPwReport)                
#         # Layout widgets.
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addWidget(QtGui.QLabel('Report type:'))
#         hbox1.addWidget(self._report_list)
#         hbox1.addStretch(5)
#         #
#         hbox2 = QtGui.QHBoxLayout()
#         hbox2.addStretch(5)
#         hbox2.addWidget(self._createreport_button)
#         #
#         reportlayout = QtGui.QVBoxLayout()
# #         reportlayout.addWidget(introlabel)
#         reportlayout.addLayout(hbox1)
#         reportlayout.addLayout(hbox2)
#         #
#         widget.setLayout(reportlayout)
#         #
#         return widget
# 
#     def _contentPreview(self):
#         """ """
#         # === GroupBox: reportbox === 
#         previewbox = QtGui.QGroupBox('Preview", self)        
#         # Active widgets and connections.
#         self._tableview = utils_qt.ToolboxQTableView()
#         # Layout widgets.
#         layout = QtGui.QVBoxLayout()
#         layout.addWidget(self._tableview)
#         previewbox.setLayout(layout)
#         #
#         return previewbox
# 
#     def _contentSaveResult(self):
#         """ """
#         saveresultbox = QtGui.QGroupBox('Save report", self)
#         # Active widgets and connections.
#         self._saveformat_list = QtGui.QComboBox()
#         #
#         self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
#                                          "Excel file (*.xlsx)"])
#         self._savedataset_button = QtGui.QPushButton('Save...')
# ###        self.connect(self._savedataset_button, QtCore.SIGNAL('clicked()'), self._saveData)                
#         # Layout widgets.
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addStretch(5)
#         hbox1.addWidget(QtGui.QLabel('File format:'))
#         hbox1.addWidget(self._saveformat_list)
#         hbox1.addWidget(self._savedataset_button)
#         #
#         saveresultbox.setLayout(hbox1)
#         #
#         return saveresultbox
# 
#     def _createPwReport(self):
#         """ """
#         if self._report_list.currentIndex() == 0:
#             QtGui.QMessageBox.information(self, "Info", 'Report type must be selected.')
#             return        
#         toolbox_utils.Logging().log('') # Empty line.
#         toolbox_utils.Logging().log('PW reports started...')
#         toolbox_utils.Logging().start_accumulated_logging()
#         self._writeToStatusBar('Generating PW report...')
#         try:
#             self._reportdata.clear()
#             # Check which report to generate.
#             if self._report_list.currentIndex() == 3: # Report: MJ1
#                 # === Report: MJ1 ===
#                 toolbox_utils.Logging().log('Selected report: MJ1')
#                 report = pw_reports.PwReportMJ1()
#                 report.createReport(self._reportdata)
#                 # Preview result.
#                 self._tableview.tablemodel.setModeldata(self._reportdata)
#                 self._refreshResultTable()
#             elif self._report_list.currentIndex() == 4: # Report: MJ2
#                 # === Report: MJ1 ===
#                 toolbox_utils.Logging().log('Selected report: MJ2')
#                 report = pw_reports.PwReportMJ2()
#                 report.createReport(self._reportdata)
#                 # Preview result.
#                 self._tableview.tablemodel.setModeldata(self._reportdata)
#                 self._refreshResultTable()
#             elif self._report_list.currentIndex() == 5: # Report: ATS1
#                 # === Report: MJ1 ===
#                 toolbox_utils.Logging().log('Selected report: ATS1')
#                 report = pw_reports.PwReportATS1()
#                 report.createReport(self._reportdata)
#                 # Preview result.
#                 self._tableview.tablemodel.setModeldata(self._reportdata)
#                 self._refreshResultTable()
#             else:
#                 raise UserWarning('The selected report type is not implemented.')
#         except UserWarning as e:
#             toolbox_utils.Logging().error('UserWarning: ' + unicode(e))
#             QtGui.QMessageBox.warning(self, "Warning", unicode(e))
#         except (IOError, OSError) as e:
#             toolbox_utils.Logging().error('Error: ' + unicode(e))
#             QtGui.QMessageBox.warning(self, "Error", unicode(e))
#         except Exception as e:
#             toolbox_utils.Logging().error('Failed on exception: ' + unicode(e))
#             QtGui.QMessageBox.warning(self, "Exception", unicode(e))
#             raise
#         finally:
#             toolbox_utils.Logging().log_all_accumulated_rows()
#             toolbox_utils.Logging().log('PW reports finished.\r\n')
#             self._writeToStatusBar('')

