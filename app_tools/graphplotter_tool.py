#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.tools.tool_base as tool_base
# import json
import app_framework
import toolbox_utils
import plankton_core
import matplotlib.backends.backend_qt4agg as mpl_backend
import matplotlib.figure as mpl_figure

class GraphPlotterTool(app_framework.ToolBase):
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
        try:
            self.set_plot_data(None)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def set_plot_data(self, plot_data):
        """ """
        try:
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def set_chart_selection(self, 
                          chart = 'Line chart', # Line chart, Bar chart, Scatter chart, Pie chart, Map chart.
                          combined = False,
                          stacked = False,
                          y_log_scale = False):
        """ """
        try:
            comboindex = self._charttype_list.findText(chart)
            if comboindex >= 0:  self._charttype_list.setCurrentIndex(comboindex)
            #
            self._combined_checkbox.setChecked(combined)
            self._stacked_checkbox.setChecked(stacked)
            self._ylogscale_checkbox.setChecked(y_log_scale)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget. 
        self._tabWidget = QtWidgets.QTabWidget()
        contentLayout.addWidget(self._tabWidget)
        self._tabWidget.addTab(self._create_content_chart(), 'Chart')
        self._tabWidget.addTab(self._create_content_labels(), 'Labels')        
#        tabWidget.addTab(self._create_content_settings(), "Settings')        
#        tabWidget.addTab(self._create_contentEditDataJson(), "Edit data (JSON)')        

    def _create_content_chart(self):
        """ """
        widget = QtWidgets.QWidget()
        contentLayout = QtWidgets.QVBoxLayout()
        contentLayout.addLayout(self._create_content_select_chart())
        contentLayout.addLayout(self._create_content_chart_area(), 10)
        #
        widget.setLayout(contentLayout)
        #
        return widget

    def _create_content_settings(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
        self._timeseriesforat_edit = QtWidgets.QLineEdit(""" bo, ro, g^, ys""")
        self._xyplotformat_edit = QtWidgets.QLineEdit(""" bo, ro, g^, ys""")
        #
        self._editable_listview = app_framework.ToolboxEditableQTableView()
        data = plankton_core.DatasetTable()
        data.set_header(['X label     ', 'Y label     ', 'Z label     '])
        data.append_row(['a', 'b', 'c'])
        data.append_row(['1', '2', '3'])
        self._editable_listview.setTableModel(data)
        self._editable_listview.resetModel() # Model data has changed.
        self._editable_listview.resizeColumnsToContents()
        #                
        self._resetsettings_button = QtWidgets.QPushButton('Reset')
#        self._resetsettings_button.clicked.connect(self._resetSettings)                
        #                
        self._applysettings_button = QtWidgets.QPushButton('Apply')
#        self._applysettings_button.clicked.connect(self._applySettings)                
        # Layout.
        form = QtWidgets.QFormLayout()
        form.addRow('Test 1:', self._timeseriesforat_edit)
        form.addRow('Test 2', self._xyplotformat_edit)
        form.addRow('Plot labels', self._editable_listview)
        #
        hbox = QtWidgets.QHBoxLayout()
#         hbox.addStretch(5)
        hbox.addWidget(self._resetsettings_button)
        hbox.addWidget(self._applysettings_button)
        hbox.addStretch(10)
        #
        vbox = QtWidgets.QVBoxLayout()
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
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
        self._title_edit = QtWidgets.QLineEdit()
        self._xlabel_edit = QtWidgets.QLineEdit()
        self._xtype_edit = QtWidgets.QLineEdit()
        self._xformat_edit = QtWidgets.QLineEdit()
        self._ylabel_edit = QtWidgets.QLineEdit()
        self._ytype_edit = QtWidgets.QLineEdit()
        self._yformat_edit = QtWidgets.QLineEdit()
        self._zlabel_edit = QtWidgets.QLineEdit()
        self._ztype_edit = QtWidgets.QLineEdit()
        self._zformat_edit = QtWidgets.QLineEdit()
        # 
        self._plotlabels_editable = app_framework.ToolboxEditableQTableView()
        self._plotlabels_table = plankton_core.DatasetTable()
        self._plotlabels_table.set_header(['Plot name     ', 'X-label     ', 'Y-label     ', 'Z-label     '])
        self._plotlabels_table.append_row(['', '', '', ''])
        self._plotlabels_editable.setTableModel(self._plotlabels_table)
        #                
        self._labelsreset_button = QtWidgets.QPushButton('Reset')
        self._labelsreset_button.clicked.connect(self._reset_labels)                
        self._labelsapply_button = QtWidgets.QPushButton('Apply')
        self._labelsapply_button.clicked.connect(self._apply_labels)                
        # Layout.
        form0 = QtWidgets.QFormLayout()
        form0.addRow('Title:    ', self._title_edit)
        form1 = QtWidgets.QFormLayout()
        form1.addRow('X-label:', self._xlabel_edit)
        form1.addRow('Y-label:', self._ylabel_edit)
        form1.addRow('Z-label:', self._zlabel_edit)
        form2 = QtWidgets.QFormLayout()
        form2.addRow('X-type:', self._xtype_edit)
        form2.addRow('Y-type:', self._ytype_edit)
        form2.addRow('Z-type:', self._ztype_edit)
        form3 = QtWidgets.QFormLayout()
        form3.addRow('X-format:', self._xformat_edit)
        form3.addRow('Y-format:', self._yformat_edit)
        form3.addRow('Z-format:', self._zformat_edit)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addLayout(form0)
        hbox1.addStretch()
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addLayout(form1)
        hbox2.addLayout(form2)
        hbox2.addLayout(form3)
        hbox2.addStretch()
        #
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(QtWidgets.QLabel('          '))
        hbox3.addWidget(self._plotlabels_editable)
        hbox3.addStretch()
        #
        hbox4 = QtWidgets.QHBoxLayout()
#         hbox4.addStretch(5)
        hbox4.addWidget(self._labelsreset_button)
        hbox4.addWidget(self._labelsapply_button)
        hbox4.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Graph:'))
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QtWidgets.QLabel('Plots:'))
        layout.addLayout(hbox3, 10)
        layout.addLayout(hbox4)
        #
        widget.setLayout(layout)
        #
        return widget

#     def _create_contentEditDataJson(self):
#         """ """
#         widget = QtWidgets.QWidget()
#         # Active widgets and connections.
#         self.plotdatainfo_textedit = QtWidgets.QTextEdit()
#         self.plotdatalist_textedit = QtWidgets.QTextEdit()
#         self._resetplotdata_button = QtWidgets.QPushButton('Reset')
#         self._resetplotdata_button.clicked.connect(self._reset_labels)                
#         #                
#         self._applyplotdata_button = QtWidgets.QPushButton('Apply')
#         self._applyplotdata_button.clicked.connect(self._applyLabelsJson)                
#         # Layout.
#         hbox = QtWidgets.QHBoxLayout()
#         hbox.addStretch(5)
#         hbox.addWidget(self._resetplotdata_button)
#         hbox.addWidget(self._applyplotdata_button)
#         #
#         layout = QtWidgets.QVBoxLayout()
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
        self._charttype_list = QtWidgets.QComboBox()
        self._charttype_list.addItems(['Line chart',
                                       'Bar chart',
                                       'Scatter chart',
                                       'Pie chart',
                                       'Boxplot chart'
#                                        'Map chart"  # Can't use BaseMap with PyInstaller, sorry...
                                       ])
#        self._charttype_list.setDisabled(True)
        self._charttype_list.currentIndexChanged.connect(self._draw_embedded_chart)
        #
        self._combined_checkbox = QtWidgets.QCheckBox('Combined')
        self._combined_checkbox.setChecked(False) 
#        self._combined_checkbox.setDisabled(True)
        self._combined_checkbox.stateChanged.connect(self._draw_embedded_chart)
        #
        self._stacked_checkbox = QtWidgets.QCheckBox('Stacked')
        self._stacked_checkbox.setChecked(False) 
#        self._stacked_checkbox.setDisabled(True)
        self._stacked_checkbox.stateChanged.connect(self._draw_embedded_chart)
        #
        self._ylogscale_checkbox = QtWidgets.QCheckBox('Y log scale')
        self._ylogscale_checkbox.setChecked(False) 
#        self._ylogscale_checkbox.setDisabled(True)
        self._ylogscale_checkbox.stateChanged.connect(self._draw_embedded_chart)
        #                
        self._clear_button = QtWidgets.QPushButton('Clear')
        self._clear_button.clicked.connect(self.clear_plot_data)                
        #                
        self._savecharttofile_button = QtWidgets.QPushButton('Edit and save...')
        self._savecharttofile_button.clicked.connect(self._save_chart_to_file)                
        # Layout widgets.
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Chart type:'))
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
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._canvas)
        #
        return layout
        
    def _draw_embedded_chart(self):
        """ """
        try:
            self._draw_chart(embedded = True)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _draw_chart(self, embedded = True):
        """ """
        try:
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
                selectedchart = str(self._charttype_list.currentText())
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
            except UserWarning as e:
                QtWidgets.QMessageBox.warning(self, "Warning", str(e))
                toolbox_utils.Logging().warning(str(e))
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                toolbox_utils.Logging().error(str(e))
                raise
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _reset_labels(self):
        """ """
        try:
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _apply_labels(self):
        """ """
        try:
            # The graph part.
            plotdatainfo = self._plotdata.get_plot_data_info()
            plotdatainfo['title'] = str(self._title_edit.text())  
            plotdatainfo['x_label'] = str(self._xlabel_edit.text())
            plotdatainfo['x_type'] = str(self._xtype_edit.text())
            plotdatainfo['x_format'] = str(self._xformat_edit.text())
            plotdatainfo['y_label'] = str(self._ylabel_edit.text())
            plotdatainfo['y_type'] = str(self._ytype_edit.text())
            plotdatainfo['y_format'] = str(self._yformat_edit.text())
            plotdatainfo['z_label'] = str(self._zlabel_edit.text())
            plotdatainfo['z_type'] = str(self._ztype_edit.text())
            plotdatainfo['z_format'] = str(self._zformat_edit.text())
            # Plots.
            plotlist = self._plotdata.get_plot_list()
            for index, row in enumerate(self._plotlabels_table.get_rows()):
                plotlist[index]['plot_name'] = str(row[0])
                plotlist[index]['x_label'] = str(row[1])
                plotlist[index]['y_label'] = str(row[2])
                plotlist[index]['z_label'] = str(row[3])
            #
            self. _reset_labels()
            # Update chart.
            self._draw_embedded_chart()
            
            self._tabWidget.setCurrentIndex(0) # Go back to graph view.
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
#     def _applyLabelsJson(self):
#         """ """
#         # Tab: Edit data (JSON). For development.
#         if self._plotdata:
#             self._plotdata.setPlotDataInfo(
#                                 json.loads(str(self.plotdatainfo_textedit.toPlainText()), 
#                                            encoding = 'utf8'))
#             #
#             self._plotdata.setPlotList(
#                                 json.loads(str(self.plotdatalist_textedit.toPlainText()), 
#                                            encoding = 'utf8'))
#         #
#         self. _reset_labels()
#         # Update chart.
#         self._draw_embedded_chart()

    def _save_chart_to_file(self):
        """ """
        try:
            if self._plotdata:
                # Use matplotlib.pyplot for drawing.
                self._draw_chart(embedded = False)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            app_framework.Logging().error('Exception: (' + debug_info + '): ' + str(e))

