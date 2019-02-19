#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import sys
import plankton_core
import app_activities
import app_framework
import toolbox_utils

class PlanktonCounterDialog(QtWidgets.QDialog):
    """ """
    def __init__(self, parentwidget, dataset, sample):
        """ """
        self._current_dataset = dataset
        self._current_sample = sample
        # Create sample object.
        dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
        self._current_sample_object = plankton_core.PlanktonCounterSample(dir_path,
                                                                         self._current_dataset,
                                                                         self._current_sample)
        #
        super(PlanktonCounterDialog, self).__init__(parentwidget)
        self.setWindowTitle("Plankton counter")
        #
#         self.resize(1500, 900)
        self.resize(1500, 845)
#         self.resize(1000, 750)
        #
        self.metadata_widget = None
        self.methods_widget = None
        self.count_widget = None
        self.sample_data_widget = None
        self._current_tab_index = 0
        #
        self._create_content()

    def _tab_in_tabwidget_changed(self):
        """ Used to update the edit table when tab is activated/deactivated. """
        try:
            oldtabindex = self._current_tab_index
            newtabindex = self._main_tab_widget.currentIndex()
            self._current_tab_index = newtabindex
            #
            if oldtabindex == newtabindex:
                return
            #
            if oldtabindex == 0:
                    self.metadata_widget.save_data()
            elif oldtabindex == 1:
                    self.methods_widget.save_data()
                    self.count_widget.load_data()
                    self.count_widget.save_data()
            elif oldtabindex == 2:
                    self.count_widget.save_data()
            elif oldtabindex == 3:
                    self.sample_data_widget.clear()
            #   
            if newtabindex == 0:
                self.metadata_widget.load_data()
            elif newtabindex == 1:
                self.methods_widget.load_data()
            elif newtabindex == 2:
                self.count_widget.load_data()
            elif newtabindex == 3:
                self.sample_data_widget.load_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def closeEvent(self, event):
        """ Called from Qt when dialog is closed. """
        try:
            # Save content.
            self.metadata_widget.save_data()
            self.methods_widget.save_data()
            self.count_widget.save_data()
            #
            self.reject()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _create_content(self):
        """ """
        contentLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(contentLayout)
        #
        dataset_sample_label = QtWidgets.QLabel('Dataset: <b>' + self._current_dataset + '</b>' +
                                            ' Sample: <b>' + self._current_sample + '</b>')
        contentLayout.addWidget(dataset_sample_label)
        contentLayout.addWidget(QtWidgets.QLabel('')) # Empty label to create space.

        self._main_tab_widget = QtWidgets.QTabWidget(self)
        
        # Add scroll capabilities.
        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollarea.setWidget(self._main_tab_widget)
        scrollarea.setWidgetResizable(True)

        contentLayout.addWidget(scrollarea)
        
        self._main_tab_widget.addTab(self._content_metadata(), 'Sample info')
#         self._main_tab_widget.addTab(self._content_methods_OLD(), 'Counting methods OLD')
        self._main_tab_widget.addTab(self._content_methods(), 'Counting methods')
        self._main_tab_widget.addTab(self._content_count(), 'Count sample')
        self._main_tab_widget.addTab(self._content_sample_data(), 'Sample data')
#         tabWidget.addTab(self._content_export_import(), 'Export/import')
        contentLayout.addWidget(self._content_bottom())
        
        # Detect tab selecteion changes.
        self._main_tab_widget.currentChanged.connect(self._tab_in_tabwidget_changed)

    def _content_metadata(self):
        """ """
        self.metadata_widget = app_activities.PlanktonCounterSampleInfo(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        # Add scroll capabilities.
#         scrollarea = QtWidgets.QScrollArea()
#         scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
#         scrollarea.setWidget(self.metadata_widget)
#         scrollarea.setWidgetResizable(True)
#         return scrollarea
        return self.metadata_widget

    def _content_methods(self):
        """ """
        self.methods_widget = app_activities.PlanktonCounterSampleMethods(self,
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
#         # Add scroll capabilities.
#         scrollarea = QtWidgets.QScrollArea()
#         scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
#         scrollarea.setWidget(self.methods_widget)
#         scrollarea.setWidgetResizable(True)
#         return scrollarea
        return self.methods_widget

    def _content_count(self):
        """ """
        self.count_widget = app_activities.PlanktonCounterSampleCount(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        return self.count_widget

    def _content_sample_data(self):
        """ """
        self.sample_data_widget = app_activities.PlanktonCounterSampleEdit(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        return self.sample_data_widget

    def _content_bottom(self):
        """ """
        widget = QtWidgets.QWidget()
        #
        self._sample_locked_checkbox = QtWidgets.QCheckBox('Locked')
        self._sample_locked_checkbox.setChecked(True)
        self._sample_locked_checkbox.stateChanged.connect(self.sample_locked_changed)
        #
        self._close_button = QtWidgets.QPushButton('Close plankton counter')
        self._close_button.clicked.connect(self.close)
        #
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._sample_locked_checkbox)
        layout.addStretch(30)
        layout.addWidget(self._close_button)
        widget.setLayout(layout)
        #
        return widget
    
    def sample_locked_changed(self):
        """ """
        # TODO: 
        print('DEBUG: sample_locked_changed')
        if self._sample_locked_checkbox.isChecked():
            if self.metadata_widget:
                self.metadata_widget.set_read_only(True)
            if self.methods_widget:
                self.methods_widget.set_read_only(True)
            if self.count_widget:
                self.count_widget.set_read_only(True)
            if self.sample_data_widget:
                self.sample_data_widget.set_read_only(True)
        else:
            if self.metadata_widget:
                self.metadata_widget.set_read_only(False)
            if self.methods_widget:
                self.methods_widget.set_read_only(False)
            if self.count_widget:
                self.count_widget.set_read_only(False)
            if self.sample_data_widget:
                self.sample_data_widget.set_read_only(False)
    
    def recalculate_sample(self):
        """ """
        # TODO: 
        print('DEBUG: recalculate_sample')
        
    
    def keyPressEvent(self, qKeyEvent):
        """ Overridden from base class. """
        try:
            if qKeyEvent.key() == QtCore.Qt.Key_Escape: 
                self.closeEvent(qKeyEvent)  
                qKeyEvent.accept() # Was handled here.
            else:
                qKeyEvent.ignore() # Will be propagated.
                super(PlanktonCounterDialog, self).keyPressEvent(qKeyEvent)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

