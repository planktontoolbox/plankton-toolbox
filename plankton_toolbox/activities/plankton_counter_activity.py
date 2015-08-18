#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import datetime
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.activities.plankton_counter_edit as plankton_counter_edit
import plankton_toolbox.activities.plankton_counter_count as plankton_counter_count
import toolbox_core

class PlanktonCounterActivity(activity_base.ActivityBase):
    """ """
    
    def __init__(self, name, parentwidget):
        """ """
        self._current_dataset = None
        self._current_sample = None
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
        self._counter_datasets_selection_model = self._counter_datasets_listview.selectionModel()
        self._counter_datasets_selection_model.selectionChanged.connect(self._selected_dataset_changed)
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
        hbox1.addWidget(self._exportdatasets_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._counter_datasets_listview)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _update_counter_dataset_list(self):
        """ """
        self._sampledata_groupbox.setTitle('Selected dataset: -')
        self._counter_datasets_model.clear()        
        for datasetname in toolbox_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem(datasetname)
            self._counter_datasets_model.appendRow(item)
        #
        self._selected_dataset_changed()

    def _selected_dataset_changed(self):
        """ """
        self._current_dataset = None
        index = self._counter_datasets_listview.currentIndex()
        if index.isValid():
            datasetname = self._counter_datasets_model.item(index.row(), column=0)
            datasetname = unicode(datasetname.text())
            self._current_dataset = datasetname
        #
        self._update_counter_sample_list()
    
    def _new_datasets(self):
        """ """        
        my_dialog = NewDatasetDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_dataset_list()

    def _delete_datasets(self):
        """ """
        my_dialog = DeleteDatasetDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_dataset_list()

    def _import_export(self):
        """ """
        my_dialog = ImportExportDatasetDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_dataset_list()

     
    ##############################################################################
    def _content_sample_tabs(self):
        """ """
        # Active widgets and connections.
        self._sampledata_groupbox = QtGui.QGroupBox('Selected dataset: -', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_samples(), 'Samples in dataset')
        tabWidget.addTab(self._content_dataset_metadata(), 'Metadata for dataset')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        self._sampledata_groupbox.setLayout(layout)        
        #
        return self._sampledata_groupbox

    # ===== _content_dataset_metadata =====    
    def _content_samples(self):
        """ """
        widget = QtGui.QWidget(self)
#         widget = QtGui.QGroupBox('Counter datasets', self)
        #
        self._counter_samples_listview = QtGui.QListView()
        self._counter_samples_listview.setModel(self._counter_samples_model)
        self._counter_samples_selection_model = self._counter_samples_listview.selectionModel()
        self._counter_samples_selection_model.selectionChanged.connect(self._selected_sample_changed)
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

    def _selected_sample_changed(self):
        """ """
        self._current_sample = None
        index = self._counter_samples_listview.currentIndex()
        if index.isValid():
            samplename = self._counter_samples_model.item(index.row(), column=0)
            samplename = unicode(samplename.text())
            self._current_sample = samplename
    
    def _update_counter_sample_list(self):
        """ """
        self._sampledata_groupbox.setTitle('Selected dataset: -')
        self._counter_samples_model.clear()        
        if self._current_dataset is not None:
            self._sampledata_groupbox.setTitle('Selected dataset: ' + self._current_dataset)
            
            for samplename in toolbox_core.PlanktonCounterManager().get_sample_names(self._current_dataset):
                item = QtGui.QStandardItem(samplename)
                self._counter_samples_model.appendRow(item)

    def _new_sample(self):
        """ """
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        #
        my_dialog = NewSampleDialog(self, self._current_dataset)
        if my_dialog.exec_():
            self._update_counter_sample_list()
            
    def _delete_sample(self):
        """ """        
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        if self._current_sample is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No sample is selected. Please try again.')
            return       
        #
        my_dialog = DeleteSampleDialog(self, self._current_dataset, self._current_sample)
        if my_dialog.exec_():
            self._update_counter_sample_list()
            
    def _edit_sample(self):
        """ """        
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        if self._current_sample is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No sample is selected. Please try again.')
            return       
        #
        my_dialog = plankton_counter_edit.PlanktonCounterEdit(self, self._current_dataset, self._current_sample)
        if my_dialog.exec_():
            self._update_counter_sample_list()
            
    def _count_sample(self):
        """ """        
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        if self._current_sample is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No sample is selected. Please try again.')
            return       
        #
        my_dialog = plankton_counter_count.PlanktonCounterCount(self, self._current_dataset, self._current_sample)
        if my_dialog.exec_():
            self._update_counter_sample_list()
            
    # ===== _content_samples =====    
    def _content_dataset_metadata(self):
        """ """
        widget = QtGui.QWidget()
        #
        return widget


class NewDatasetDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(NewDatasetDialog, self).__init__(parentwidget)
        self.setLayout(self._content())

    def _content(self):
        """ """
        self._datasetname_edit = QtGui.QLineEdit('')
        self._datasetname_edit.setMinimumWidth(400)
        createdataset_button = QtGui.QPushButton('Create dataset')
        createdataset_button.clicked.connect(self._create_dataset)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
        formlayout.addRow('Dataset name:', self._datasetname_edit)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createdataset_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _create_dataset(self):
        """ """
        datasetname = unicode(self._datasetname_edit.text())
        toolbox_core.PlanktonCounterManager().create_dataset(datasetname)
        #            
        self.accept() # Close dialog box.


class DeleteDatasetDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(DeleteDatasetDialog, self).__init__(parentwidget)
        self._parentwidget = parentwidget
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()

    def _content(self):
        """ """  
        datasets_listview = QtGui.QListView()
        self._datasets_model = QtGui.QStandardItemModel()
        datasets_listview.setModel(self._datasets_model)

        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_datasets)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_datasets)                
        delete_button = QtGui.QPushButton('Delete marked datasets')
        delete_button.clicked.connect(self._delete_marked_datasets)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
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


class ImportExportDatasetDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(ImportExportDatasetDialog, self).__init__(parentwidget)
        self.setLayout(self._content())
        self.setMinimumSize(800, 300)
        #
        self._update_export_dataset_list()

    def _content(self):
        """ """
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_import(), 'Import')
        tabWidget.addTab(self._content_export(), 'Export')
        tabWidget.addTab(self._content_publish(), 'Publish')
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        #
        return layout                
 
    def _content_import(self):
        """ """
        widget = QtGui.QWidget()
        self._importsourcetype_list = QtGui.QComboBox()
        self._importsourcetype_list.addItems(['<select>',
                                           'SHARK Archive',
                                           ])
        self._importsourcetype_list.setCurrentIndex(1)
        self._importsourcefile_edit = QtGui.QLineEdit('')
        self._importsourcefile_button = QtGui.QPushButton('Browse...')
        self._importsourcefile_button.clicked.connect(self._browse_source)
        self._importtargetdatasetname_edit = QtGui.QLineEdit('')        
        self._import_button = QtGui.QPushButton('Import')
        self._import_button.clicked.connect(self._import_dataset)
        self._importcancel_button = QtGui.QPushButton('Cancel')
        self._importcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Archive type:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._importsourcetype_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('Archive file:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._importsourcefile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._importsourcefile_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel('New dataset name:')
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._importtargetdatasetname_edit, gridrow, 1, 1, 9)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._import_button)
        hbox1.addWidget(self._importcancel_button)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget
    
    def _browse_source(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._importsourcefile_edit.text()))
        namefilter = 'Zip files (*.zip);;All files (*.*)'
        filepath = dirdialog.getOpenFileName(
                                self,
                                'Import Archive file',
                                self._importsourcefile_edit.text(),
                                namefilter)
        if not filepath.isEmpty():
            self._importsourcefile_edit.setText(unicode(filepath))
            head, tail = os.path.split(unicode(filepath))
            self._importtargetdatasetname_edit.setText(tail.replace('.zip', ''))
    
    def _import_dataset(self):
        """ """
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')        
        
    def _content_export(self):
        """ """
        widget = QtGui.QWidget()
        self._datasettoexport_list = QtGui.QComboBox()
        self._datasettoexport_list.addItems(['<select>'])
        self._datasettoexport_list.currentIndexChanged.connect(self._dataset_changed)
        self._exportsourcetype_list = QtGui.QComboBox()
        self._exportsourcetype_list.addItems(['<select>',
                                           'SHARK Archive',
                                           ])
        self._exportsourcetype_list.setCurrentIndex(1)
        self._exporttargetdir_edit = QtGui.QLineEdit('')
        self._exporttargetdir_button = QtGui.QPushButton('Browse...')
        self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
        self._exporttargetfilename_edit = QtGui.QLineEdit('')
        
        self._publish_checkbox = QtGui.QCheckBox('Publish dataset')
        self._publishtarget_list = QtGui.QComboBox()
        self._publishtarget_list.addItems(['<select>',
                                           'SHARKdata (http://sharkdata.se)',
                                           'SHARKdata-test (http://test.sharkdata.se)',
                                           ])
        self._publishuser_edit = QtGui.QLineEdit('')
        self._publishpassword_edit = QtGui.QLineEdit('')
        
        self._export_button = QtGui.QPushButton('Export/publish')
        self._export_button.clicked.connect(self._export_dataset)
        self._exportcancel_button = QtGui.QPushButton('Cancel')
        self._exportcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Dataset to export:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._datasettoexport_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel('Archive type:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._exportsourcetype_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('Export to directory:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._exporttargetdir_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('Export file name:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetfilename_edit, gridrow, 1, 1, 9)
        gridrow += 1
        # Empty row.
        form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._publish_checkbox, gridrow, 0, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('Publish on:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._publishtarget_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel('User:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._publishuser_edit, gridrow, 1, 1, 5)
        gridrow += 1
        label2 = QtGui.QLabel('Password:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._publishpassword_edit, gridrow, 1, 1, 5)
        gridrow += 1
        # Empty row.
        form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._export_button)
        hbox1.addWidget(self._exportcancel_button)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget

    def _update_export_dataset_list(self):
        """ """
        self._datasettoexport_list.clear()        
        self._datasettoexport_list.addItems(['<select>'])
        for datasetname in toolbox_core.PlanktonCounterManager().get_dataset_names():
            self._datasettoexport_list.addItem(datasetname)
        
    def _dataset_changed(self):
        """ """
        index = self._datasettoexport_list.currentIndex()
        if index > 0:
            datasetname = unicode(self._datasettoexport_list.itemText(index))
            if self._exportsourcetype_list.currentIndex() == 1:
                # Adjust ti SHARK archive name.
                datestring = datetime.date.today().isoformat()
                datasetname = 'SHARK_' + datasetname + '_version_' + datestring + '.zip' 
            #
            self._exporttargetfilename_edit.setText(datasetname)
        else:
            self._exporttargetfilename_edit.setText('')

    def _browse_target_dir(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._exporttargetdir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self._exporttargetdir_edit.setText(dirpath)
    
    def _export_dataset(self):
        """ """
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
        
    def _content_publish(self):
        """ """
        widget = QtGui.QWidget()
        return widget
    
class NewSampleDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset):
        """ """
        self._current_dataset = dataset
        super(NewSampleDialog, self).__init__(parentwidget)
        self.setLayout(self._content())

    def _content(self):
        """ """
        self._samplename_edit = QtGui.QLineEdit('')
        self._samplename_edit.setMinimumWidth(400)
        createsample_button = QtGui.QPushButton('Create sample')
        createsample_button.clicked.connect(self._create_sample)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
        formlayout.addRow('sample name:', self._samplename_edit)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createsample_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _create_sample(self):
        """ """
        samplename = unicode(self._samplename_edit.text())
        toolbox_core.PlanktonCounterManager().create_sample(self._current_dataset, samplename)
        #            
        self.accept() # Close dialog box.


class DeleteSampleDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset, sample):
        """ """
        self._current_dataset = dataset
        self._current_sample = sample
        super(DeleteSampleDialog, self).__init__(parentwidget)


