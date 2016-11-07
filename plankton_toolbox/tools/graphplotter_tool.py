#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import json
import toolbox_utils
import plankton_core
import matplotlib.backends.backend_qt4agg as mpl_backend
import matplotlib.figure as mpl_figure

class GraphPlotterTool(tool_base.ToolBase):
    """
    """
    def __init__(self, name, parentwidget):
        """ """
        # Filename used when saving chart to file.
        self._lastuseddirectory = '.'
        self._plotdata = None
        self._current_chart = None 
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(GraphPlotterTool, self).__init__(name, parentwidget)
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)
        #
        
    def clear_plot_data(self):
        """ """
        self.set_plot_data(None)

    def set_plot_data(self, plot_data):
        """ """
        self._figure.clear()
        self._canvas.draw()
        #
        if plot_data:
            if isinstance(plot_data, toolbox_utils.GraphPlotData):
                self._plotdata = plot_data
            else:
                # Invalid type. 
                self._plotdata = None
        else:
            self._plotdata = None
        #
        self._reset_labels()
        self._draw_embedded_chart()

    def set_chart_selection(self, 
                          chart = 'Line chart', # Line chart, Bar chart, Scatter chart, Pie chart, Map chart.
                          combined = False,
                          stacked = False,
                          y_log_scale = False):
        """ """
        comboindex = self._charttype_list.findText(chart)
        if comboindex >= 0:  self._charttype_list.setCurrentIndex(comboindex)
        #
        self._combined_checkbox.setChecked(combined)
        self._stacked_checkbox.setChecked(stacked)
        self._ylogscale_checkbox.setChecked(y_log_scale)
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget. 
        self._tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(self._tabWidget)
        self._tabWidget.addTab(self._create_content_chart(), 'Chart')
        self._tabWidget.addTab(self._create_content_labels(), 'Labels')        
#        tabWidget.addTab(self._create_content_settings(), "Settings')        
#        tabWidget.addTab(self._create_contentEditDataJson(), "Edit data (JSON)')        

    def _create_content_chart(self):
        """ """
        widget = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        contentLayout.addLayout(self._create_content_select_chart())
        contentLayout.addLayout(self._create_content_chart_area(), 10)
        #
        widget.setLayout(contentLayout)
        #
        return widget

    def _create_content_settings(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._timeseriesforat_edit = QtGui.QLineEdit(""" bo, ro, g^, ys""")
        self._xyplotformat_edit = QtGui.QLineEdit(""" bo, ro, g^, ys""")
        #
        self._editable_listview = utils_qt.ToolboxEditableQTableView()
        data = plankton_core.DatasetTable()
        data.set_header(['X label     ', 'Y label     ', 'Z label     '])
        data.append_row(['a', 'b', 'c'])
        data.append_row(['1', '2', '3'])
        self._editable_listview.setTableModel(data)
        self._editable_listview.resetModel() # Model data has changed.
        self._editable_listview.resizeColumnsToContents()
        #                
        self._resetsettings_button = QtGui.QPushButton('Reset')
#        self.connect(self._resetsettings_button, QtCore.SIGNAL('clicked()'), self._resetSettings)                
        #                
        self._applysettings_button = QtGui.QPushButton('Apply')
#        self.connect(self._applysettings_button, QtCore.SIGNAL('clicked()'), self._applySettings)                
        # Layout.
        form = QtGui.QFormLayout()
        form.addRow('Test 1:', self._timeseriesforat_edit)
        form.addRow('Test 2', self._xyplotformat_edit)
        form.addRow('Plot labels', self._editable_listview)
        #
        hbox = QtGui.QHBoxLayout()
#         hbox.addStretch(5)
        hbox.addWidget(self._resetsettings_button)
        hbox.addWidget(self._applysettings_button)
        hbox.addStretch(10)
        #
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox, 10)
        # 
        widget.setLayout(vbox)
  
        # Under development...
        self._timeseriesforat_edit.setDisabled(True)
        self._xyplotformat_edit.setDisabled(True)
        self._editable_listview.setDisabled(True)
        self._resetsettings_button.setDisabled(True)
        self._applysettings_button.setDisabled(True)
        #
        return widget

    def _create_content_labels(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._title_edit = QtGui.QLineEdit()
        self._xlabel_edit = QtGui.QLineEdit()
        self._xtype_edit = QtGui.QLineEdit()
        self._xformat_edit = QtGui.QLineEdit()
        self._ylabel_edit = QtGui.QLineEdit()
        self._ytype_edit = QtGui.QLineEdit()
        self._yformat_edit = QtGui.QLineEdit()
        self._zlabel_edit = QtGui.QLineEdit()
        self._ztype_edit = QtGui.QLineEdit()
        self._zformat_edit = QtGui.QLineEdit()
        # 
        self._plotlabels_editable = utils_qt.ToolboxEditableQTableView()
        self._plotlabels_table = plankton_core.DatasetTable()
        self._plotlabels_table.set_header(['Plot name     ', 'X-label     ', 'Y-label     ', 'Z-label     '])
        self._plotlabels_table.append_row(['', '', '', ''])
        self._plotlabels_editable.setTableModel(self._plotlabels_table)
        #                
        self._labelsreset_button = QtGui.QPushButton('Reset')
        self.connect(self._labelsreset_button, QtCore.SIGNAL('clicked()'), self._reset_labels)                
        self._labelsapply_button = QtGui.QPushButton('Apply')
        self.connect(self._labelsapply_button, QtCore.SIGNAL('clicked()'), self._apply_labels)                
        # Layout.
        form0 = QtGui.QFormLayout()
        form0.addRow('Title:    ', self._title_edit)
        form1 = QtGui.QFormLayout()
        form1.addRow('X-label:', self._xlabel_edit)
        form1.addRow('Y-label:', self._ylabel_edit)
        form1.addRow('Z-label:', self._zlabel_edit)
        form2 = QtGui.QFormLayout()
        form2.addRow('X-type:', self._xtype_edit)
        form2.addRow('Y-type:', self._ytype_edit)
        form2.addRow('Z-type:', self._ztype_edit)
        form3 = QtGui.QFormLayout()
        form3.addRow('X-format:', self._xformat_edit)
        form3.addRow('Y-format:', self._yformat_edit)
        form3.addRow('Z-format:', self._zformat_edit)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addLayout(form0)
        hbox1.addStretch()
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addLayout(form1)
        hbox2.addLayout(form2)
        hbox2.addLayout(form3)
        hbox2.addStretch()
        #
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(QtGui.QLabel('          '))
        hbox3.addWidget(self._plotlabels_editable)
        hbox3.addStretch()
        #
        hbox4 = QtGui.QHBoxLayout()
#         hbox4.addStretch(5)
        hbox4.addWidget(self._labelsreset_button)
        hbox4.addWidget(self._labelsapply_button)
        hbox4.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel('Graph:'))
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QtGui.QLabel('Plots:'))
        layout.addLayout(hbox3, 10)
        layout.addLayout(hbox4)
        #
        widget.setLayout(layout)
        #
        return widget

#     def _create_contentEditDataJson(self):
#         """ """
#         widget = QtGui.QWidget()
#         # Active widgets and connections.
#         self.plotdatainfo_textedit = QtGui.QTextEdit()
#         self.plotdatalist_textedit = QtGui.QTextEdit()
#         self._resetplotdata_button = QtGui.QPushButton('Reset')
#         self.connect(self._resetplotdata_button, QtCore.SIGNAL('clicked()'), self._reset_labels)                
#         #                
#         self._applyplotdata_button = QtGui.QPushButton('Apply')
#         self.connect(self._applyplotdata_button, QtCore.SIGNAL('clicked()'), self._applyLabelsJson)                
#         # Layout.
#         hbox = QtGui.QHBoxLayout()
#         hbox.addStretch(5)
#         hbox.addWidget(self._resetplotdata_button)
#         hbox.addWidget(self._applyplotdata_button)
#         #
#         layout = QtGui.QVBoxLayout()
#         layout.addWidget(self.plotdatainfo_textedit, 5)
#         layout.addWidget(self.plotdatalist_textedit, 10)
#         layout.addLayout(hbox)
# 
#         widget.setLayout(layout)
#         #
#         return widget

    def _create_content_select_chart(self):
        """ """
        # Active widgets and connections.
        self._charttype_list = QtGui.QComboBox()
        self._charttype_list.addItems(['Line chart',
                                       'Bar chart',
                                       'Scatter chart',
                                       'Pie chart',
                                       'Boxplot chart'
#                                        'Map chart"  # Can't use BaseMap with PyInstaller, sorry...
                                       ])
#        self._charttype_list.setDisabled(True)
        self.connect(self._charttype_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._draw_embedded_chart)
        #
        self._combined_checkbox = QtGui.QCheckBox('Combined')
        self._combined_checkbox.setChecked(False) 
#        self._combined_checkbox.setDisabled(True)
        self.connect(self._combined_checkbox, QtCore.SIGNAL('stateChanged(int)'), self._draw_embedded_chart)
        #
        self._stacked_checkbox = QtGui.QCheckBox('Stacked')
        self._stacked_checkbox.setChecked(False) 
#        self._stacked_checkbox.setDisabled(True)
        self.connect(self._stacked_checkbox, QtCore.SIGNAL('stateChanged(int)'), self._draw_embedded_chart)
        #
        self._ylogscale_checkbox = QtGui.QCheckBox('Y log scale')
        self._ylogscale_checkbox.setChecked(False) 
#        self._ylogscale_checkbox.setDisabled(True)
        self.connect(self._ylogscale_checkbox, QtCore.SIGNAL('stateChanged(int)'), self._draw_embedded_chart)
        #                
        self._clear_button = QtGui.QPushButton('Clear')
        self.connect(self._clear_button, QtCore.SIGNAL('clicked()'), self.clear_plot_data)                
        #                
        self._savecharttofile_button = QtGui.QPushButton('Edit and save...')
        self.connect(self._savecharttofile_button, QtCore.SIGNAL('clicked()'), self._save_chart_to_file)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel('Chart type:'))
        layout.addWidget(self._charttype_list)
        layout.addWidget(self._combined_checkbox)
        layout.addWidget(self._stacked_checkbox)
        layout.addWidget(self._ylogscale_checkbox)
#         layout.addStretch(5)
        layout.addWidget(self._clear_button)
        layout.addWidget(self._savecharttofile_button)
        layout.addStretch(10)
        #
        return layout
        
    def _create_content_chart_area(self):
        """ """
        # Matplotlib figure and canvas for Qt4.
        self._figure = mpl_figure.Figure()
        self._canvas = mpl_backend.FigureCanvasQTAgg(self._figure)        
        self._canvas.show()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._canvas)
        #
        return layout
        
    def _draw_embedded_chart(self):
        """ """
        self._draw_chart(embedded = True)
        
    def _draw_chart(self, embedded = True):
        """ """
        try:
            if embedded:
                # Draw embedded in Qt.
                figure = self._figure
            else:
                # Use matplotlib.pyplot for drawing.
                figure = None
            # Adjust visibility of checkboxes, etc.
            if self._combined_checkbox.isChecked():
                self._stacked_checkbox.setEnabled(True)
            else:
                self._stacked_checkbox.setChecked(False)
                self._stacked_checkbox.setEnabled(False)
            if self._stacked_checkbox.isChecked():
                self._ylogscale_checkbox.setChecked(False)
                self._ylogscale_checkbox.setEnabled(False)
            else:
                self._ylogscale_checkbox.setEnabled(True)
            # User selections.
            selectedchart = unicode(self._charttype_list.currentText())
            combined = self._combined_checkbox.isChecked()
            stacked = self._stacked_checkbox.isChecked()
            ylogscale = self._ylogscale_checkbox.isChecked()
            #
            if embedded:
                self._figure.clear()
                self._canvas.draw()
            #
            if not self._plotdata:
                return
            # Draw selected chart.
            if selectedchart == 'Line chart':
                self._current_chart = toolbox_utils.LineChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart(combined = combined, stacked = stacked, y_log_scale = ylogscale)        
                self._canvas.draw()
            #
            if selectedchart == 'Bar chart':
                self._current_chart = toolbox_utils.BarChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart(combined = combined, stacked = stacked, y_log_scale = ylogscale)                
                self._canvas.draw()
            #
            if selectedchart == 'Scatter chart':
                self._current_chart = toolbox_utils.ScatterChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart(combined = combined, y_log_scale = ylogscale)                
                self._canvas.draw()
            #
            if selectedchart == 'Pie chart':
                self._current_chart = toolbox_utils.PieChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart()        
                self._canvas.draw()
            #
            if selectedchart == 'Boxplot chart':
                self._current_chart = toolbox_utils.BoxPlotChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart(y_log_scale = ylogscale)        
                self._canvas.draw()
            #
            if selectedchart == 'Map chart':
                self._current_chart = toolbox_utils.MapChart(self._plotdata, figure = figure)
                self._current_chart.plot_chart()        
                self._canvas.draw()
        #    
        except UserWarning, e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
            toolbox_utils.Logging().warning(unicode(e))
        except Exception, e:
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
            toolbox_utils.Logging().error(unicode(e))
            raise

    def _reset_labels(self):
        """ """
        self._plotlabels_table.clear_rows()
        if self._plotdata:
            # The graph part.
            plotdatainfo = self._plotdata.get_plot_data_info()
            self._title_edit.setText(plotdatainfo['title'])
            self._xlabel_edit.setText(plotdatainfo['x_label'])
            self._xtype_edit.setText(plotdatainfo['x_type'])
            self._xformat_edit.setText(plotdatainfo['x_format'])
            self._ylabel_edit.setText(plotdatainfo['y_label'])
            self._ytype_edit.setText(plotdatainfo['y_type'])
            self._yformat_edit.setText(plotdatainfo['y_format'])
            self._zlabel_edit.setText(plotdatainfo['z_label'])
            self._ztype_edit.setText(plotdatainfo['z_type'])
            self._zformat_edit.setText(plotdatainfo['z_format'])
            # Plots.             
            for plot in self._plotdata.get_plot_list():
                row = []
                row.append(plot['plot_name'])
                row.append(plot['x_label'])
                row.append(plot['y_label'])
                row.append(plot['z_label'])
                self._plotlabels_table.append_row(row)

#         self._plotlabels_editable.setTableModel(self._plotlabels_table)
        self._plotlabels_editable.resetModel() # Model data has changed.
        self._plotlabels_editable.resizeColumnsToContents()

            
#             # Tab: Edit data (JSON). For development.
#             self.plotdatainfo_textedit.setText(
#                        json.dumps(self._plotdata.get_plot_data_info(), 
#                                   encoding = 'utf8', 
#                                   sort_keys=True, indent=4))
#             self.plotdatalist_textedit.setText(
#                        json.dumps(self._plotdata.get_plot_list(), 
#                                   encoding = 'utf8', 
#                                   sort_keys=True, indent=4))
#         else:
#             # Tab: Edit data (JSON). For development. 
#             self.plotdatainfo_textedit.setText('')
#             self.plotdatalist_textedit.setText('')
            
    def _apply_labels(self):
        """ """
        # The graph part.
        plotdatainfo = self._plotdata.get_plot_data_info()
        plotdatainfo['title'] = unicode(self._title_edit.text())  
        plotdatainfo['x_label'] = unicode(self._xlabel_edit.text())
        plotdatainfo['x_type'] = unicode(self._xtype_edit.text())
        plotdatainfo['x_format'] = unicode(self._xformat_edit.text())
        plotdatainfo['y_label'] = unicode(self._ylabel_edit.text())
        plotdatainfo['y_type'] = unicode(self._ytype_edit.text())
        plotdatainfo['y_format'] = unicode(self._yformat_edit.text())
        plotdatainfo['z_label'] = unicode(self._zlabel_edit.text())
        plotdatainfo['z_type'] = unicode(self._ztype_edit.text())
        plotdatainfo['z_format'] = unicode(self._zformat_edit.text())
        # Plots.
        plotlist = self._plotdata.get_plot_list()
        for index, row in enumerate(self._plotlabels_table.get_rows()):
            plotlist[index]['plot_name'] = unicode(row[0])
            plotlist[index]['x_label'] = unicode(row[1])
            plotlist[index]['y_label'] = unicode(row[2])
            plotlist[index]['z_label'] = unicode(row[3])
        #
        self. _reset_labels()
        # Update chart.
        self._draw_embedded_chart()
        
        self._tabWidget.setCurrentIndex(0) # Go back to graph view.
        
#     def _applyLabelsJson(self):
#         """ """
#         # Tab: Edit data (JSON). For development.
#         if self._plotdata:
#             self._plotdata.setPlotDataInfo(
#                                 json.loads(unicode(self.plotdatainfo_textedit.toPlainText()), 
#                                            encoding = 'utf8'))
#             #
#             self._plotdata.setPlotList(
#                                 json.loads(unicode(self.plotdatalist_textedit.toPlainText()), 
#                                            encoding = 'utf8'))
#         #
#         self. _reset_labels()
#         # Update chart.
#         self._draw_embedded_chart()

    def _save_chart_to_file(self):
        """ """
        if self._plotdata:
            # Use matplotlib.pyplot for drawing.
            self._draw_chart(embedded = False)

