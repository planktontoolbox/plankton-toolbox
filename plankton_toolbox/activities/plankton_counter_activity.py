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
import plankton_toolbox.activities.plankton_counter_dialog as plankton_counter_dialog
import plankton_core
import toolbox_utils

class PlanktonCounterActivity(activity_base.ActivityBase):
    """ """
    
    def __init__(self, name, parentwidget):
        """ """
        self._current_dataset = None
        self._current_sample = None
        self._counter_datasets_model = QtGui.QStandardItemModel()
        self._counter_samples_model = QtGui.QStandardItemModel()
        # Initialize parent (self._create_content will be called).
        super(PlanktonCounterActivity, self).__init__(name, parentwidget)
        # Update lists for datasets and samples.
        self._update_counter_dataset_list()
        # Mark first rows for dataset and sample.
        if self._counter_datasets_model.rowCount() > 0:
            index = self._counter_datasets_model.createIndex(0, 0)
            self._counter_datasets_listview.setCurrentIndex(index)
        if self._counter_samples_model.rowCount() > 0:
            index = self._counter_samples_model.createIndex(0, 0)
            self._counter_samples_listview.setCurrentIndex(index)
            
            
            
        # Update plankton counter datasets when changes occured.
        self.connect(plankton_core.PlanktonCounterManager(), 
                     QtCore.SIGNAL('planktonCounterListChanged'), 
                     self._update_counter_sample_list)
#                      self._update_counter_dataset_list)

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
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._content_plankton_counter())
        splitter.addWidget(self._content_sample_tabs())
        splitter.setStretchFactor(3, 10)
        contentLayout.addWidget(splitter, 100)
#        contentLayout.addStretch(5)
    
    # ===== Counter datasets =====    
    def _content_plankton_counter(self):
        """ """
#         widget = QtGui.QWidget()
        widget = QtGui.QGroupBox('Plankton counter datasets', self)
        #
        self._counter_datasets_listview = QtGui.QListView()
        self._counter_datasets_listview.setModel(self._counter_datasets_model)
        self._counter_datasets_listview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._counter_datasets_selection_model = self._counter_datasets_listview.selectionModel()
        self._counter_datasets_selection_model.selectionChanged.connect(self._selected_dataset_changed)
        #
        self._newdataset_button = QtGui.QPushButton('New...')        
        self._newdataset_button.clicked.connect(self._new_datasets)
        self._deletedataset_button = QtGui.QPushButton('Delete...')
        self._deletedataset_button.clicked.connect(self._delete_datasets)               
        self._exportsamples_button = QtGui.QPushButton('Import/export...')
        self._exportsamples_button.clicked.connect(self._import_export_samples)
#         self._exportdatasets_button = QtGui.QPushButton('Import/export...')
#         self._exportdatasets_button.clicked.connect(self._import_export)
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._newdataset_button)
        hbox1.addWidget(self._deletedataset_button)
#         hbox1.addWidget(self._exportdatasets_button)
        hbox1.addWidget(self._exportsamples_button)
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
        self._current_dataset = None
        self._current_sample = None
        self._sampledata_groupbox.setTitle('Selected dataset: -')
        self._counter_datasets_model.clear()        
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem(datasetname)
            self._counter_datasets_model.appendRow(item)
        #
        self._selected_dataset_changed()

    def _selected_dataset_changed(self):
        """ """
        self._current_dataset = None
        self._current_sample = None
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

#     def _import_export(self):
#         """ """
#         my_dialog = ImportExportDatasetDialog(self)
#         if my_dialog.exec_():
#             self._current_dataset = None
#             self._update_counter_dataset_list()

    def _import_export_samples(self):
        """ """
        my_dialog = ImportExportSamplesDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_dataset_list()

     
    # ===== Counter samples =====    
    def _content_sample_tabs(self):
        """ """
        # Active widgets and connections.
        self._sampledata_groupbox = QtGui.QGroupBox('Selected dataset: -', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_samples(), 'Samples in dataset')
#         tabWidget.addTab(self._content_dataset_metadata(), 'Dataset info (metadata)')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        self._sampledata_groupbox.setLayout(layout)        
        #
        return self._sampledata_groupbox

    def _content_samples(self):
        """ """
        widget = QtGui.QWidget(self)
#         widget = QtGui.QGroupBox('Counter datasets', self)
        #
        self._counter_samples_listview = QtGui.QListView()
        self._counter_samples_listview.setModel(self._counter_samples_model)
        self._counter_samples_listview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._counter_samples_selection_model = self._counter_samples_listview.selectionModel()
        self._counter_samples_selection_model.selectionChanged.connect(self._selected_sample_changed)
        self._counter_samples_listview.doubleClicked.connect(self._open_edit_count)
        #
        self._newsample_button = QtGui.QPushButton('New...')        
        self._newsample_button.clicked.connect(self._new_sample)
        self._deletesample_button = QtGui.QPushButton('Delete...')
        self._deletesample_button.clicked.connect(self._delete_sample)               
#         self._editsample_button = QtGui.QPushButton('Edit...')        
#         self._editsample_button.clicked.connect(self._edit_sample)
        self._countsample_button = QtGui.QPushButton('Edit/count...')
        self._countsample_button.clicked.connect(self._count_sample)               
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._newsample_button)
        hbox1.addWidget(self._deletesample_button)
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
    
    def _open_edit_count(self):
        """ """
        self._selected_sample_changed()
        
        self._count_sample()
    
    def _update_counter_sample_list(self):
        """ """
        self._sampledata_groupbox.setTitle('Selected dataset: -')
        self._counter_samples_model.clear()        
        if self._current_dataset is not None:
            self._sampledata_groupbox.setTitle('Selected dataset: ' + self._current_dataset)
            
            for samplename in plankton_core.PlanktonCounterManager().get_sample_names(self._current_dataset):
                item = QtGui.QStandardItem(samplename)
                self._counter_samples_model.appendRow(item)

    def _new_sample(self):
        """ """
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        #
        dialog = NewSampleDialog(self, self._current_dataset)
        if dialog.exec_():
            self._update_counter_sample_list()
            
    def _delete_sample(self):
        """ """        
        if self._current_dataset is None:
            QtGui.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
#         if self._current_sample is None:
#             QtGui.QMessageBox.warning(self, "Warning", 'No sample is selected. Please try again.')
#             return       
        #
        dialog = DeleteSampleDialog(self, self._current_dataset, self._current_sample)
        if dialog.exec_():
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
        dialog = plankton_counter_dialog.PlanktonCounterDialog(self, self._current_dataset, self._current_sample)
#         if dialog.exec_():
#             self._update_counter_sample_list()
        try:
            dialog.exec_()
        except Exception as e:
            print('EXCEPTION: ' + e.message)
            
#     def _content_dataset_metadata(self):
#         """ """
#         widget = QtGui.QWidget()
#         #
#         return widget


class NewDatasetDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(NewDatasetDialog, self).__init__(parentwidget)
        self.setWindowTitle("New dataset")
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
        if len(datasetname) > 0:
            plankton_core.PlanktonCounterManager().create_dataset(datasetname)
        #            
        self.accept() # Close dialog box.


class DeleteDatasetDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(DeleteDatasetDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete dataset")
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
        delete_button = QtGui.QPushButton('Delete marked dataset(s)')
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
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
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
                plankton_core.PlanktonCounterManager().delete_dataset(datasetname)
        #            
        self.accept() # Close dialog box.

# TODO:
class ImportExportSamplesDialog(QtGui.QDialog):
    """ """
    def __init__(self, parentwidget):
        """ """
        super(ImportExportSamplesDialog, self).__init__(parentwidget)
        self.setWindowTitle("Import/export samples")
        self.setLayout(self._content())
        self.setMinimumSize(600, 200)
        #
        self._update_import_dataset_list()
        self._counter_update_dataset_list()

    def _content(self):
        """ """
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_import(), 'Import')
        tabWidget.addTab(self._content_export(), 'Export')
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        #
        return layout                
 
    def _content_import(self):
        """ """
        widget = QtGui.QWidget()
        self._datasetforimport_list = QtGui.QComboBox()
        self._datasetforimport_list.setMinimumWidth(200)
        self._datasetforimport_list.addItems(['<not available>'])
        self._importsourcetype_list = QtGui.QComboBox()
        self._importsourcetype_list.setMinimumWidth(200)
        self._importsourcetype_list.addItems(['PTBX Excel',
                                              ])
        self._import_button = QtGui.QPushButton('Import sample(s)...')
        self._import_button.clicked.connect(self._import_dataset)
        self._importcancel_button = QtGui.QPushButton('Cancel')
        self._importcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(QtGui.QLabel('Import file format:   '))
        hbox1.addWidget(self._importsourcetype_list)
        hbox1.addStretch(5)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(QtGui.QLabel('Select target dataset:'))
        hbox2.addWidget(self._datasetforimport_list)
        hbox2.addStretch(5)
        #
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch(5)
        hbox3.addWidget(self._import_button)
        hbox3.addWidget(self._importcancel_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QtGui.QLabel(''))
        layout.addLayout(hbox3)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget
    
    def _update_import_dataset_list(self):
        """ """
        self._datasetforimport_list.clear()        
        self._datasetforimport_list.addItems(['<select>'])
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            self._datasetforimport_list.addItem(datasetname)
         
    def _import_dataset(self):
        """ """
        try:
            if self._datasetforimport_list.currentIndex() == 0:
                QtGui.QMessageBox.information(self, "Information", 'No target dataset is selected. Please try again.')
                return
            
            dirdialog = QtGui.QFileDialog(self)
    #         dirdialog.setDirectory(unicode(self._importsourcefile_edit.text()))
            namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            filepath_list = dirdialog.getOpenFileNames(
                                    self,
                                    'Import TPBX Excel file',
                                    '', # self._importsourcefile_edit.text(),
                                    namefilter)
            #
            if not filepath_list.isEmpty():
                #
                dataset = unicode(self._datasetforimport_list.currentText())
                datasetdirpath = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
                #
                for filepath in filepath_list:
                    #
                    excelfilepath = unicode(filepath)
                    excelfilename = os.path.basename(unicode(excelfilepath))
                    samplename = os.path.splitext(excelfilename)[0]
    
                    print('DEBUG: Excel import: ' + samplename)
                    #
                    try:
                        plankton_core.PlanktonCounterManager().create_sample(dataset, samplename)
                    except:
                        pass # Already exists.
                    new_sample_object = plankton_core.PlanktonCounterSample(datasetdirpath, dataset, samplename)
                    #
                    new_sample_object.import_sample_from_excel(excelfilepath)
            #            
            self.accept() # Close dialog box.
        #        
        except Exception as e:
            toolbox_utils.Logging().error('Failed to export sample. ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Warning', 'Failed to export sample. ' + unicode(e))

    def _content_export(self):
        """ """
        widget = QtGui.QWidget()
        
        self._counter_datasets_listview = QtGui.QListView()
        self._counter_datasets_model = QtGui.QStandardItemModel()
        self._counter_datasets_listview.setModel(self._counter_datasets_model)

        self._exportsourcetype_list = QtGui.QComboBox()
        self._exportsourcetype_list.addItems(['PTBX Archive',
                                              ])
        self._exportsourcetype_list.setCurrentIndex(0)
        self._exporttargetdir_edit = QtGui.QLineEdit('')
        self._exporttargetdir_button = QtGui.QPushButton('Browse...')
        self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
        
        self._export_button = QtGui.QPushButton('Export')
        self._export_button.clicked.connect(self._export_sample)
        self._exportcancel_button = QtGui.QPushButton('Cancel')
        self._exportcancel_button.clicked.connect(self.reject)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Sample(s) to export:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._counter_datasets_listview, gridrow, 1, 5, 9)
        gridrow += 5
        label1 = QtGui.QLabel('Export file type:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._exportsourcetype_list, gridrow, 1, 1, 9)
        gridrow += 1
        label2 = QtGui.QLabel('Export to directory:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 8)
        form1.addWidget(self._exporttargetdir_button, gridrow, 9, 1, 1)
        gridrow += 1
        form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1) # Empty row.
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

    def _counter_update_dataset_list(self):
        """ """
        self._counter_datasets_model.clear()
        for datasetname in sorted(plankton_core.PlanktonCounterManager().get_dataset_names()):
            for samplename in sorted(plankton_core.PlanktonCounterManager().get_sample_names(datasetname)):
                item = QtGui.QStandardItem(datasetname + ': ' + samplename)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setCheckable(True)
                self._counter_datasets_model.appendRow(item)
# 
#     def _update_export_dataset_list(self):
#         """ """
#         self._datasettoexport_list.clear()        
#         self._datasettoexport_list.addItems(['<select>'])
#         for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
#             self._datasettoexport_list.addItem(datasetname)
         
    def _browse_target_dir(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._exporttargetdir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self._exporttargetdir_edit.setText(dirpath)
     
    def _export_sample(self):
        """ """
        try:
            selectedsamples = []
            for rowindex in range(self._counter_datasets_model.rowCount()):
                item = self._counter_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    selectedsamples.append(unicode(item.text()))
            #
            if len(selectedsamples) == 0:
                QtGui.QMessageBox.warning(self, 'Warning', 'No sample is selected. Please try again.')
                return
            #            
            datasetdirpath = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
            exporttargetdir = unicode(self._exporttargetdir_edit.text())
            #
            for datasetandsample in selectedsamples:
                datasetandsamplepair = datasetandsample.split(':')
                datasetname = datasetandsamplepair[0].strip()
                samplename = datasetandsamplepair[1].strip()
                #
                export_sample_object = plankton_core.PlanktonCounterSample(datasetdirpath, datasetname, samplename)
                export_sample_object.export_sample_to_excel(exporttargetdir, samplename + '.xlsx')
            #            
            self.accept() # Close dialog box.
        #        
        except Exception as e:
            toolbox_utils.Logging().error('Failed to export sample. ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Warning', 'Failed to export sample. ' + unicode(e))



# === NOTE: Save this for the future. ===
# class ImportExportDatasetDialog(QtGui.QDialog):
#     """ This dialog is allowed to access private parts in the parent widget. """
#     def __init__(self, parentwidget):
#         """ """
#         super(ImportExportDatasetDialog, self).__init__(parentwidget)
#         self.setWindowTitle("Import/export dataset")
#         self.setLayout(self._content())
#         self.setMinimumSize(800, 300)
#         #
#         self._update_export_dataset_list()
# 
#     def _content(self):
#         """ """
#         tabWidget = QtGui.QTabWidget()
#         tabWidget.addTab(self._content_import(), 'Import')
#         tabWidget.addTab(self._content_export(), 'Export')
#         tabWidget.addTab(self._content_publish(), 'Publish')
#         #
#         layout = QtGui.QVBoxLayout()
#         layout.addWidget(tabWidget, 10)
#         #
#         return layout                
#  
#     def _content_import(self):
#         """ """
#         widget = QtGui.QWidget()
#         self._importsourcetype_list = QtGui.QComboBox()
#         self._importsourcetype_list.addItems(['<select>',
#                                            'PTBX Archive',
#                                            ])
#         self._importsourcetype_list.setCurrentIndex(1)
#         self._importsourcefile_edit = QtGui.QLineEdit('')
#         self._importsourcefile_button = QtGui.QPushButton('Browse...')
#         self._importsourcefile_button.clicked.connect(self._browse_source)
#         self._importtargetdatasetname_edit = QtGui.QLineEdit('')        
#         self._import_button = QtGui.QPushButton('Import')
#         self._import_button.clicked.connect(self._import_dataset)
#         self._importcancel_button = QtGui.QPushButton('Cancel')
#         self._importcancel_button.clicked.connect(self.reject)
#         # Layout widgets.
#         form1 = QtGui.QGridLayout()
#         gridrow = 0
#         label1 = QtGui.QLabel('Dataset archive type:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._importsourcetype_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtGui.QLabel('Dataset archive file:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._importsourcefile_edit, gridrow, 1, 1, 9)
#         form1.addWidget(self._importsourcefile_button, gridrow, 10, 1, 1)
#         gridrow += 1
#         label3 = QtGui.QLabel('New dataset name:')
#         form1.addWidget(label3, gridrow, 0, 1, 1)
#         form1.addWidget(self._importtargetdatasetname_edit, gridrow, 1, 1, 9)
#         #
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addStretch(5)
#         hbox1.addWidget(self._import_button)
#         hbox1.addWidget(self._importcancel_button)
#         layout = QtGui.QVBoxLayout()
#         layout.addLayout(form1)
#         layout.addLayout(hbox1)
#         layout.addStretch(100)
#         widget.setLayout(layout)
#         #
#         return widget
#     
#     def _browse_source(self):
#         """ """
#         dirdialog = QtGui.QFileDialog(self)
#         dirdialog.setDirectory(unicode(self._importsourcefile_edit.text()))
#         namefilter = 'Zip files (*.zip);;All files (*.*)'
#         filepath = dirdialog.getOpenFileName(
#                                 self,
#                                 'Import Archive file',
#                                 self._importsourcefile_edit.text(),
#                                 namefilter)
#         if not filepath.isEmpty():
#             self._importsourcefile_edit.setText(unicode(filepath))
#             head, tail = os.path.split(unicode(filepath))
#             self._importtargetdatasetname_edit.setText(tail.replace('.zip', ''))
#     
#     def _import_dataset(self):
#         """ """
#         QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')        
#         
#     def _content_export(self):
#         """ """
#         widget = QtGui.QWidget()
#         self._datasettoexport_list = QtGui.QComboBox()
#         self._datasettoexport_list.addItems(['<select>'])
#         self._datasettoexport_list.currentIndexChanged.connect(self._dataset_changed)
#         self._exportsourcetype_list = QtGui.QComboBox()
#         self._exportsourcetype_list.addItems(['<select>',
#                                            'PTBX Archive',
#                                            ])
#         self._exportsourcetype_list.setCurrentIndex(1)
#         self._exporttargetdir_edit = QtGui.QLineEdit('')
#         self._exporttargetdir_button = QtGui.QPushButton('Browse...')
#         self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
#         self._exporttargetfilename_edit = QtGui.QLineEdit('')
#         
#         self._publish_checkbox = QtGui.QCheckBox('Publish dataset')
#         self._publishtarget_list = QtGui.QComboBox()
#         self._publishtarget_list.addItems(['<select>',
#                                            'SHARKdata (http://sharkdata.se)',
#                                            'SHARKdata-test (http://test.sharkdata.se)',
#                                            ])
#         self._publishuser_edit = QtGui.QLineEdit('')
#         self._publishpassword_edit = QtGui.QLineEdit('')
#         
#         self._export_button = QtGui.QPushButton('Export/publish')
#         self._export_button.clicked.connect(self._export_dataset)
#         self._exportcancel_button = QtGui.QPushButton('Cancel')
#         self._exportcancel_button.clicked.connect(self.reject)
#         # Layout widgets.
#         form1 = QtGui.QGridLayout()
#         gridrow = 0
#         label1 = QtGui.QLabel('Dataset to export:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._datasettoexport_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label1 = QtGui.QLabel('Dataset archive type:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._exportsourcetype_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtGui.QLabel('Export to directory:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 9)
#         form1.addWidget(self._exporttargetdir_button, gridrow, 10, 1, 1)
#         gridrow += 1
#         label2 = QtGui.QLabel('Export file name:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._exporttargetfilename_edit, gridrow, 1, 1, 9)
#         gridrow += 1
#         # Empty row.
#         form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._publish_checkbox, gridrow, 0, 1, 1)
#         gridrow += 1
#         label2 = QtGui.QLabel('Publish on:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishtarget_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtGui.QLabel('User:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishuser_edit, gridrow, 1, 1, 5)
#         gridrow += 1
#         label2 = QtGui.QLabel('Password:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishpassword_edit, gridrow, 1, 1, 5)
#         gridrow += 1
#         # Empty row.
#         form1.addWidget(QtGui.QLabel(''), gridrow, 0, 1, 1)
#         #
#         hbox1 = QtGui.QHBoxLayout()
#         hbox1.addStretch(5)
#         hbox1.addWidget(self._export_button)
#         hbox1.addWidget(self._exportcancel_button)
#         layout = QtGui.QVBoxLayout()
#         layout.addLayout(form1)
#         layout.addLayout(hbox1)
#         layout.addStretch(100)
#         widget.setLayout(layout)
#         #
#         return widget
# 
#     def _update_export_dataset_list(self):
#         """ """
#         self._datasettoexport_list.clear()        
#         self._datasettoexport_list.addItems(['<select>'])
#         for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
#             self._datasettoexport_list.addItem(datasetname)
#         
#     def _dataset_changed(self):
#         """ """
#         index = self._datasettoexport_list.currentIndex()
#         if index > 0:
#             datasetname = unicode(self._datasettoexport_list.itemText(index))
#             if self._exportsourcetype_list.currentIndex() == 1:
#                 # Adjust to PTBX archive name.
#                 datestring = datetime.date.today().isoformat()
#                 datasetname = 'PTBX_' + datasetname + '_version_' + datestring + '.zip'
#                 datasetname = datasetname.replace(' ', '_')
#             #
#             self._exporttargetfilename_edit.setText(datasetname)
#         else:
#             self._exporttargetfilename_edit.setText('')
# 
#     def _browse_target_dir(self):
#         """ """
#         dirdialog = QtGui.QFileDialog(self)
#         dirdialog.setFileMode(QtGui.QFileDialog.Directory)
#         dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
#         dirdialog.setDirectory(unicode(self._exporttargetdir_edit.text()))
#         dirpath = dirdialog.getExistingDirectory()
#         if dirpath:
#             self._exporttargetdir_edit.setText(dirpath)
#     
#     def _export_dataset(self):
#         """ """
#         QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
#         
#     def _content_publish(self):
#         """ """
#         widget = QtGui.QWidget()
#         return widget
    
class NewSampleDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset):
        """ """
        self._current_dataset = dataset
        super(NewSampleDialog, self).__init__(parentwidget)
        self.setWindowTitle("New sample")
        self.setLayout(self._content())

    def _content(self):
        """ """
#         self._sampleid_edit = QtGui.QLineEdit('')
#         self._sampleid_edit.setMinimumWidth(400)
        self._samplename_edit = QtGui.QLineEdit('')
        self._samplename_edit.setMinimumWidth(400)
        createsample_button = QtGui.QPushButton('Create sample')
        createsample_button.clicked.connect(self._create_sample)               
        cancel_button = QtGui.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtGui.QFormLayout()
#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('Sample name:', self._samplename_edit)
        
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
#         if len(samplename) == 0:
#             samplename = unicode(self._sampleid_edit.text()) # Use id.
        #   
        plankton_core.PlanktonCounterManager().create_sample(self._current_dataset, samplename)
        #            
        self.accept() # Close dialog box.


class DeleteSampleDialog(QtGui.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset, sample):
        """ """
        self._current_dataset = dataset
        self._current_sample = sample
        self._parentwidget = parentwidget
        super(DeleteSampleDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete sample")
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_data()

    def _content(self):
        """ """  
        samples_listview = QtGui.QListView()
        self._samples_model = QtGui.QStandardItemModel()
        samples_listview.setModel(self._samples_model)

        clearall_button = utils_qt.ClickableQLabel('Clear all')
        self.connect(clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_samples)                
        markall_button = utils_qt.ClickableQLabel('Mark all')
        self.connect(markall_button, QtCore.SIGNAL('clicked()'), self._check_all_samples)                
        delete_button = QtGui.QPushButton('Delete marked sample(s)')
        delete_button.clicked.connect(self._delete_marked_samples)               
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
        layout.addWidget(samples_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        
        return layout                

    def _load_data(self):
        """ """
        self._samples_model.clear()        
        for samplename in plankton_core.PlanktonCounterManager().get_sample_names(self._current_dataset):
            item = QtGui.QStandardItem(samplename)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._samples_model.appendRow(item)
            
    def _check_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _delete_marked_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:
                samplename = unicode(item.text())
                print(samplename)
                plankton_core.PlanktonCounterManager().delete_sample(self._current_dataset, samplename)
        #            
        self.accept() # Close dialog box.

