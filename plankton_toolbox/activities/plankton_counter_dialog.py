#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.plankton_counter_sample_info as plankton_counter_sample_info
import plankton_toolbox.activities.plankton_counter_sample_edit as plankton_counter_sample_edit
import plankton_toolbox.activities.plankton_counter_sample_count as plankton_counter_sample_count
import plankton_toolbox.activities.plankton_counter_sample_methods as plankton_counter_sample_methods
# import plankton_toolbox.activities.plankton_counter_sample_methods_OLD as plankton_counter_sample_methods_OLD
import plankton_core

class PlanktonCounterDialog(QtGui.QDialog):
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

    def closeEvent(self, event):
        """ Called from Qt when dialog is closed. """
        # Save content.
        self.metadata_widget.save_data()
        self.methods_widget.save_data()
        self.count_widget.save_data()
        #
        self.reject()
        
    def _create_content(self):
        """ """
        contentLayout = QtGui.QVBoxLayout(self)
        self.setLayout(contentLayout)
        #
        dataset_sample_label = QtGui.QLabel('Dataset: <b>' + self._current_dataset + '</b>' +
                                            ' Sample: <b>' + self._current_sample + '</b>')
        contentLayout.addWidget(dataset_sample_label)
        contentLayout.addWidget(QtGui.QLabel('')) # Empty label to create space.

        self._main_tab_widget = QtGui.QTabWidget(self)
        
        # Add scroll capabilities.
        scrollarea = QtGui.QScrollArea()
        scrollarea.setFrameShape(QtGui.QFrame.NoFrame)
        scrollarea.setWidget(self._main_tab_widget)
        scrollarea.setWidgetResizable(True)

        contentLayout.addWidget(scrollarea)
#         contentLayout.addWidget(self._main_tab_widget)
        
        
        self._main_tab_widget.addTab(self._content_metadata(), 'Sample info')
#         self._main_tab_widget.addTab(self._content_methods_OLD(), 'Counting methods OLD')
        self._main_tab_widget.addTab(self._content_methods(), 'Counting methods')
        self._main_tab_widget.addTab(self._content_count(), 'Count sample')
        self._main_tab_widget.addTab(self._content_sample_data(), 'Sample data')
#         tabWidget.addTab(self._content_export_import(), 'Export/import')
        contentLayout.addWidget(self._content_bottom())
        
        
        
#         # TODO: DEBUG......
#         self._main_tab_widget.setCurrentIndex(2)
        
        
        
        
        # Detect tab selecteion changes.
        self._main_tab_widget.currentChanged.connect(self._tab_in_tabwidget_changed)

    def _content_metadata(self):
        """ """
        self.metadata_widget = plankton_counter_sample_info.PlanktonCounterSampleInfo(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        # Add scroll capabilities.
#         scrollarea = QtGui.QScrollArea()
#         scrollarea.setFrameShape(QtGui.QFrame.NoFrame)
#         scrollarea.setWidget(self.metadata_widget)
#         scrollarea.setWidgetResizable(True)
#         return scrollarea
        return self.metadata_widget

#     def _content_methods_OLD(self):
#         """ """
#         self.methods_widget = plankton_counter_sample_methods_OLD.PlanktonCounterSampleMethods(self,
#                                                            self._current_dataset, 
#                                                            self._current_sample, 
#                                                            self._current_sample_object)
# #         # Add scroll capabilities.
# #         scrollarea = QtGui.QScrollArea()
# #         scrollarea.setFrameShape(QtGui.QFrame.NoFrame)
# #         scrollarea.setWidget(self.methods_widget)
# #         scrollarea.setWidgetResizable(True)
# #         return scrollarea
#         return self.methods_widget
    def _content_methods(self):
        """ """
        self.methods_widget = plankton_counter_sample_methods.PlanktonCounterSampleMethods(self,
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
#         # Add scroll capabilities.
#         scrollarea = QtGui.QScrollArea()
#         scrollarea.setFrameShape(QtGui.QFrame.NoFrame)
#         scrollarea.setWidget(self.methods_widget)
#         scrollarea.setWidgetResizable(True)
#         return scrollarea
        return self.methods_widget

    def _content_count(self):
        """ """
        self.count_widget = plankton_counter_sample_count.PlanktonCounterSampleCount(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        return self.count_widget

    def _content_sample_data(self):
        """ """
        self.sample_data_widget = plankton_counter_sample_edit.PlanktonCounterSampleEdit(self, 
                                                           self._current_dataset, 
                                                           self._current_sample, 
                                                           self._current_sample_object)
        return self.sample_data_widget

    def _content_bottom(self):
        """ """
        widget = QtGui.QWidget()
        #
        self._close_button = QtGui.QPushButton('Close plankton counter')
        self._close_button.clicked.connect(self.close)
        #
        layout = QtGui.QHBoxLayout()
        layout.addStretch(10)
        layout.addWidget(self._close_button)
        widget.setLayout(layout)
        #
        return widget
        
    def keyPressEvent(self, qKeyEvent):
        """ Overridden from base class. """
        if qKeyEvent.key() == QtCore.Qt.Key_Escape: 
            self.closeEvent(qKeyEvent)  
            qKeyEvent.accept() # Was handled here.
        else:
            qKeyEvent.ignore() # Will be propagated.
            super(PlanktonCounterDialog, self).keyPressEvent(qKeyEvent)

