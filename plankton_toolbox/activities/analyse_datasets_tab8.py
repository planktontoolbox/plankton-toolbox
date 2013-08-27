#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute 
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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab8(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab8, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        
    def update(self):
        """ """

    # ===== TAB: Reports ===== 
    def contentReports(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab8_intro'))
        # Select type of data object.
#         self._numberofvariables_list = QtGui.QComboBox()
#         self._numberofvariables_list.addItems(["One variable (Y)", "Two variables (X and Y)", "Three variables (X, Y and Z)"])
#         self.connect(self._numberofvariables_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._clearPlotData)                
#         # - Select column for x-axis:
#         self._x_axis_column_list = QtGui.QComboBox()
#         self._x_axis_column_list.setMinimumContentsLength(20)
#         self._x_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._x_axis_parameter_list = QtGui.QComboBox()        
#         self._x_axis_parameter_list.setMinimumContentsLength(20)
#         self._x_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._x_axistype_list = QtGui.QComboBox()
#         self._x_axistype_list.addItems(self._type_list_values)
#         self.connect(self._x_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
#         # - Select column for y-axis:
#         self._y_axis_column_list = QtGui.QComboBox()
#         self._y_axis_column_list.setMinimumContentsLength(20)
#         self._y_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._y_axis_parameter_list = QtGui.QComboBox()
#         self._y_axis_parameter_list.setMinimumContentsLength(20)
#         self._y_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._y_axistype_list = QtGui.QComboBox()
#         self._y_axistype_list.addItems(self._type_list_values)
#         self.connect(self._y_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
#         # - Select column for z-axis:
#         self._z_axis_column_list = QtGui.QComboBox()
#         self._z_axis_column_list.setMinimumContentsLength(20)
#         self._z_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._z_axis_parameter_list = QtGui.QComboBox()
#         self._z_axis_parameter_list.setMinimumContentsLength(20)
#         self._z_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self._z_axistype_list = QtGui.QComboBox()
#         self._z_axistype_list.addItems(self._type_list_values)
#         self.connect(self._z_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
#         # Clear data object.
#         self._newgraph_button = QtGui.QPushButton("New graph")
#         self.connect(self._newgraph_button, QtCore.SIGNAL("clicked()"), self._newGraphAndPlotData)                
#         # Add subplot data to the Graph plotter tool.
#         self._addsubplotdata_button = QtGui.QPushButton("Add subplot to graph")
#         self.connect(self._addsubplotdata_button, QtCore.SIGNAL("clicked()"), self._addSubplotData)                
# 
#         # Layout widgets.
#         #
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addWidget(QtGui.QLabel("Select number of variables in each plot:"))
#         hbox1.addWidget(self._numberofvariables_list)
#         hbox1.addStretch(10)
#         #
#         form1 = QtGui.QGridLayout()
#         gridrow = 0
#         label1 = QtGui.QLabel("Select x-axis:")
#         label2 = QtGui.QLabel("Parameter:")
#         label3 = QtGui.QLabel("Type:")
#         stretchlabel = QtGui.QLabel("")
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._x_axis_column_list, gridrow, 1, 1, 1)
#         form1.addWidget(label2, gridrow, 2, 1, 1)
#         form1.addWidget(self._x_axis_parameter_list, gridrow, 3, 1, 1)
#         form1.addWidget(label3, gridrow, 4, 1, 1)
#         form1.addWidget(self._x_axistype_list, gridrow, 5, 1, 1)
#         form1.addWidget(stretchlabel, gridrow,6, 1, 20)
#         gridrow += 1
#         label1 = QtGui.QLabel("Select y-axis:")
#         label2 = QtGui.QLabel("Parameter:")
#         label3 = QtGui.QLabel("Type:")
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._y_axis_column_list, gridrow, 1, 1, 1)
#         form1.addWidget(label2, gridrow, 2, 1, 1)
#         form1.addWidget(self._y_axis_parameter_list, gridrow, 3, 1, 1)
#         form1.addWidget(label3, gridrow, 4, 1, 1)
#         form1.addWidget(self._y_axistype_list, gridrow, 5, 1, 1)
#         form1.addWidget(stretchlabel, gridrow,6, 1, 20)
#         gridrow += 1
#         label1 = QtGui.QLabel("Select z-axis:")
#         label2 = QtGui.QLabel("Parameter:")
#         label3 = QtGui.QLabel("Type:")
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._z_axis_column_list, gridrow, 1, 1, 1)
#         form1.addWidget(label2, gridrow, 2, 1, 1)
#         form1.addWidget(self._z_axis_parameter_list, gridrow, 3, 1, 1)
#         form1.addWidget(label3, gridrow, 4, 1, 1)
#         form1.addWidget(self._z_axistype_list, gridrow, 5, 1, 1)
#         form1.addWidget(stretchlabel, gridrow,6, 1, 20)
#         #
#         hbox2 = QtGui.QHBoxLayout()
#         hbox2.addStretch(10)
#         hbox2.addWidget(self._newgraph_button)
#         hbox2.addWidget(self._addsubplotdata_button)
#         #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
#         layout.addLayout(hbox1)
#         layout.addLayout(form1)
        layout.addStretch(10)
#         layout.addLayout(hbox2)
        self.setLayout(layout)                
#         #
#         self._updateEnabledDisabledAndTypes()
        #
        return self
        

