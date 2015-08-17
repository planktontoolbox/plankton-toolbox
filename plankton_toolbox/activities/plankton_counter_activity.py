#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import toolbox_core

class PlanktonCounterActivity(activity_base.ActivityBase):
    """ """
    
    def __init__(self, name, parentwidget):
        """ """
        self._counter_datasets_model = QtGui.QStandardItemModel()
        self._counter_samples_model = QtGui.QStandardItemModel()
        #
        # Initialize parent (self._create_content will be called).
        super(PlanktonCounterActivity, self).__init__(name, parentwidget)
        #
        self._update_counter_dataset_list()
        
    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._content_plankton_counter())
        splitter.addWidget(self._content_sample_tabs())
        splitter.setStretchFactor(3, 10)
        contentLayout.addWidget(splitter, 100)
#        contentLayout.addStretch(5)
        # Style.
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
    
    # ===== COUNTER DATASETS =====    
    def _content_plankton_counter(self):
        """ """
#         widget = QtGui.QWidget()
        widget = QtGui.QGroupBox('Plankton counter datasets', self)
        #
        self._counter_datasets_listview = QtGui.QListView()
        self._counter_datasets_listview.setModel(self._counter_datasets_model)
#         self._counter_datasets_listview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #
        self._counter_datasets_selection_model = self._counter_datasets_listview.selectionModel()
        self._counter_datasets_selection_model.selectionChanged.connect(self._update_selected_sample)
        #
        self._newdataset_button = QtGui.QPushButton('New...')        
        self._newdataset_button.clicked.connect(self._new_datasets)
        self._deletedataset_button = QtGui.QPushButton('Delete...')
        self._deletedataset_button.clicked.connect(self._delete_datasets)               
        self._exportdatasets_button = QtGui.QPushButton('Import/export...')
        self._exportdatasets_button.clicked.connect(self._import_export)
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._newdataset_button)
        hbox1.addWidget(self._deletedataset_button)
        hbox1.addStretch(10)
        hbox1.addWidget(self._exportdatasets_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._counter_datasets_listview)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _update_counter_dataset_list(self):
        """ """
        self._counter_datasets_model.clear()        
        for datasetname in toolbox_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem(datasetname)
            self._counter_datasets_model.appendRow(item)

    def _new_datasets(self):
        """ """        
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
            
    def _delete_datasets(self):
        """ """
        my_dialog = NewSampleDialog(self)
        if my_dialog.exec_():
            self._update_counter_dataset_list()

    def _import_export(self):
        """ """
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
    
    def _update_selected_sample(self):
        """ """
        index = self._counter_datasets_listview.currentIndex()
        datasetname = self._counter_datasets_model.item(index.row(), column=0)
        datasetname = unicode(datasetname.text())
        self._update_counter_sample_list(datasetname)
    
     
    ##############################################################################
    def _content_sample_tabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_samples(), 'Samples in dataset')
        tabWidget.addTab(self._content_dataset_metadata(), 'Metadata for dataset')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== _content_dataset_metadata =====    
    def _content_samples(self):
        """ """
        widget = QtGui.QWidget(self)
#         widget = QtGui.QGroupBox('Counter datasets', self)
        #
        self._counter_samples_listview = QtGui.QListView()
        self._counter_samples_listview.setModel(self._counter_samples_model)
#         self._counter_datasets_listview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #
#         self._counter_samples_selection_model = self._counter_samples_listview.selectionModel()
#         self._counter_samples_selection_model.selectionChanged.connect(self._update_selected_sample)
        #
        self._newsample_button = QtGui.QPushButton('New...')        
        self._newsample_button.clicked.connect(self._new_sample)
        self._deletesample_button = QtGui.QPushButton('Delete...')
        self._deletesample_button.clicked.connect(self._delete_sample)               
        self._editsample_button = QtGui.QPushButton('Edit...')        
        self._editsample_button.clicked.connect(self._edit_sample)
        self._countsample_button = QtGui.QPushButton('Count...')
        self._countsample_button.clicked.connect(self._count_sample)               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._newsample_button)
        hbox1.addWidget(self._deletesample_button)
        hbox1.addWidget(self._editsample_button)
        hbox1.addWidget(self._countsample_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._counter_samples_listview)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _update_counter_sample_list(self, dataset_name):
        """ """
        self._counter_samples_model.clear()        
        for samplename in toolbox_core.PlanktonCounterManager().get_sample_names(dataset_name):
            item = QtGui.QStandardItem(samplename)
            self._counter_samples_model.appendRow(item)

    def _new_sample(self):
        """ """
#         my_dialog = NewSampleDialog(self)
#         if my_dialog.exec_():
#             self._update_counter_dataset_list()
            
            
    def _delete_sample(self):
        """ """        
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
            
    def _edit_sample(self):
        """ """        
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
            
    def _count_sample(self):
        """ """        
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
            
    # ===== _content_samples =====    
    def _content_dataset_metadata(self):
        """ """
        widget = QtGui.QWidget()
        #
        return widget


class NewSampleDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(NewSampleDialog, self).__init__(parentwidget)
        self._parentwidget = parentwidget
        self.setLayout(self._content())
        self._load_data()

    def _content(self):
        """ """  
        datasets_listview = QtGui.QListView()
        self._datasets_model = QtGui.QStandardItemModel()
        datasets_listview.setModel(self._datasets_model)
        #
        self._clearall_button = QtGui.QPushButton('Clear all')
        self._clearall_button.clicked.connect(self._uncheck_all_datasets)                
        self._markall_button = QtGui.QPushButton('Mark all')
        self._markall_button.clicked.connect(self._check_all_datasets)                
        self._delete_button = QtGui.QPushButton('Delete marked datasets')
        self._delete_button.clicked.connect(self._delete_marked_datasets)               
        self._cancel_button = QtGui.QPushButton('Cancel')
        self._cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._clearall_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(self._delete_button)
        hbox2.addWidget(self._cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(datasets_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        
        return layout                

    def _load_data(self):
        """ """  
        self._datasets_model.clear()        
        for datasetname in toolbox_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem(datasetname)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._datasets_model.appendRow(item)
    def _check_all_datasets(self):
        """ """
        for rowindex in range(self._datasets_model.rowCount()):
            item = self._datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_datasets(self):
        """ """
        for rowindex in range(self._datasets_model.rowCount()):
            item = self._datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _delete_marked_datasets(self):
        """ """
        for rowindex in range(self._datasets_model.rowCount()):
            item = self._datasets_model.item(rowindex, 0)
            
            if item.checkState() == QtCore.Qt.Checked:
                datasetname = unicode(item.text())
                print(datasetname)
                toolbox_core.PlanktonCounterManager().delete_dataset(datasetname)
        #            
        self.accept() # Close dialog box.
