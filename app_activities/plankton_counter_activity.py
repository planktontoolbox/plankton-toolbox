#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import os
# import ntpath
import datetime
import zipfile
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import plankton_core
import toolbox_utils
import app_framework
import app_activities

class PlanktonCounterActivity(app_framework.ActivityBase):
    """ """
    planktonCounterListChanged = QtCore.pyqtSignal()
    
    def __init__(self, name, parentwidget):
        """ """
        self._current_dataset = None
        self._current_sample = None
        self._counter_samples_model = QtGui.QStandardItemModel()
        # Initialize parent (self._create_content will be called).
        super(PlanktonCounterActivity, self).__init__(name, parentwidget)
        # Update lists for datasets and samples.
        self._update_counter_sample_list()
        # Mark first rows for dataset and sample.
        if self._counter_samples_model.rowCount() > 0:
            index = self._counter_samples_model.createIndex(0, 0)
            self._counter_samples_listview.setCurrentIndex(index)
        # Update plankton counter datasets when changes occured.
        plankton_core.PlanktonCounterManager().planktonCounterListChanged.connect(self._update_counter_sample_list)
        
    def _emit_change_notification(self):
        """ Emit signal to update GUI lists for available datasets and samples. """
        self.planktonCounterListChanged.emit()

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_datasets_and_samples())

    # ===== Counter datasets and samples =====    
    def _content_datasets_and_samples(self):
        """ """
        widget = QtWidgets.QGroupBox('Plankton counter - datasets and samples', self)
        #
        self._counter_samples_listview = QtWidgets.QListView()
        self._counter_samples_listview.setModel(self._counter_samples_model)
        self._counter_samples_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._counter_samples_selection_model = self._counter_samples_listview.selectionModel()
        self._counter_samples_selection_model.selectionChanged.connect(self._selected_sample_changed)
        #
        self._counter_samples_listview.doubleClicked.connect(self._open_edit_count)
        #
        self._newdataset_button = QtWidgets.QPushButton('New dataset...')        
        self._newdataset_button.clicked.connect(self._new_datasets)
        self._newsample_button = QtWidgets.QPushButton('New sample...')        
        self._newsample_button.clicked.connect(self._new_sample)
        self._deletesample_button = QtWidgets.QPushButton('Delete...')
        self._deletesample_button.clicked.connect(self._delete_datasets_and_sample)               
        self._countsample_button = QtWidgets.QPushButton('Edit/count sample...')
        self._countsample_button.clicked.connect(self._open_edit_count)               
        #
        self._refresh_button = QtWidgets.QPushButton('Refresh dataset list')
#         self._refresh_button.clicked.connect(self._update_counter_sample_list)
        self._refresh_button.clicked.connect(self._emit_change_notification)
        self._exportimportsamples_button = QtWidgets.QPushButton('Export/import samples (.xlsx)...')
        self._exportimportsamples_button.clicked.connect(self._export_import_samples)
        self._backup_button = QtWidgets.QPushButton('Export/import toolbox data (.zip)...')
        self._backup_button.clicked.connect(self._backup_export_import)
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._newdataset_button)
        hbox1.addWidget(self._newsample_button)
        hbox1.addWidget(self._deletesample_button)
        hbox1.addWidget(self._countsample_button)
        hbox1.addStretch(10)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self._refresh_button)
        hbox2.addWidget(self._exportimportsamples_button)
        hbox2.addWidget(self._backup_button)
        hbox2.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._counter_samples_listview)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        widget.setLayout(layout)                
        #
        return widget
    
    def _new_datasets(self):
        """ """        
        my_dialog = NewDatasetDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._current_sample = None
            self._update_counter_sample_list()

    def _new_sample(self):
        """ """
        dialog = NewSampleDialog(self, self._current_dataset)
        if dialog.exec_():
            self._update_counter_sample_list()
            
    def _delete_datasets_and_sample(self):
        """ """        
        dialog = DeleteDialog(self)
        if dialog.exec_():
            self._update_counter_sample_list()
            
    def _backup_export_import(self):
        """ """
        my_dialog = BackupExportImportDialog(self)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_sample_list()
            
    def _export_import_samples(self):
        """ """
        my_dialog = ExportImportSamplesDialog(self, self._current_dataset)
        if my_dialog.exec_():
            self._current_dataset = None
            self._update_counter_sample_list()
            
    def _selected_sample_changed(self):
        """ """
        self._current_dataset = None
        self._current_sample = None
        index = self._counter_samples_listview.currentIndex()
        if index.isValid():
            for row_index in range(index.row() + 1):
                datasetandsamplestring = str(self._counter_samples_model.item(row_index + 0, column = 0).text())
                if datasetandsamplestring.startswith('Dataset: '):
                    self._current_dataset =  datasetandsamplestring.replace('Dataset: ', '').strip()
                    self._current_sample = None
                elif datasetandsamplestring.startswith('- Sample: '):
                    self._current_sample =  datasetandsamplestring.replace('- Sample: ', '').strip()
    
    def _update_counter_sample_list(self):
        """ """
        self._counter_samples_model.clear()
        for datasetname in sorted(plankton_core.PlanktonCounterManager().get_dataset_names()):
            item = QtGui.QStandardItem('Dataset: ' + datasetname)
#             item.setCheckState(QtCore.Qt.Unchecked)
#             item.setCheckable(True)
            self._counter_samples_model.appendRow(item)
            for samplename in sorted(plankton_core.PlanktonCounterManager().get_sample_names(datasetname)):
                item = QtGui.QStandardItem('- Sample: ' + samplename)
#                 item = QtWidgets.QStandardItem(datasetname + ': ' + samplename)
#                 item.setCheckState(QtCore.Qt.Unchecked)
#                 item.setCheckable(True)
                self._counter_samples_model.appendRow(item)

    def _open_edit_count(self):
        """ """        
        self._selected_sample_changed()
        #
        if self._current_dataset is None:
            QtWidgets.QMessageBox.warning(self, "Warning", 'No dataset is selected. Please try again.')
            return       
        if self._current_sample is None:
            QtWidgets.QMessageBox.warning(self, "Warning", 'No sample is selected. Please try again.')
            return       
        #
        dialog = app_activities.PlanktonCounterDialog(self, self._current_dataset, self._current_sample)
#         if dialog.exec_():
#             self._update_counter_sample_list()
        try:
            dialog.exec_()
        except Exception as e:
            print('EXCEPTION: ' + e.message)


class NewDatasetDialog(QtWidgets.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(NewDatasetDialog, self).__init__(parentwidget)
        self.setWindowTitle("New dataset")
        self._parentwidget = parentwidget
        self.setLayout(self._content())

    def _content(self):  
        """ """
        self._datasetname_edit = QtWidgets.QLineEdit('')
        self._datasetname_edit.setMinimumWidth(400)
        createdataset_button = QtWidgets.QPushButton('Create dataset')
        createdataset_button.clicked.connect(self._create_dataset)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
        formlayout.addRow('Dataset name:', self._datasetname_edit)
        formlayout.addRow('', QtWidgets.QLabel('Example: SHARK_Phytoplankton_2016_NationalMonitoring'))
        
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createdataset_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _create_dataset(self):
        """ """
        datasetname = str(self._datasetname_edit.text())
        if len(datasetname) > 0:
            plankton_core.PlanktonCounterManager().create_dataset(datasetname)
        #            
        self.accept() # Close dialog box.


class NewSampleDialog(QtWidgets.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset):
        """ """
        self._current_dataset = dataset
        super(NewSampleDialog, self).__init__(parentwidget)
        self._parentwidget = parentwidget
        self.setWindowTitle("New sample")
        self.setLayout(self._content())
        self._load_dataset_data()

    def _content(self):
        """ """
        self._dataset_list = QtWidgets.QComboBox(self)        
        self._samplename_edit = QtWidgets.QLineEdit('')
        self._samplename_edit.setMinimumWidth(400)
        createsample_button = QtWidgets.QPushButton('Create sample')
        createsample_button.clicked.connect(self._create_sample)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('Dataset:', self._dataset_list)
        formlayout.addRow('Sample name:', self._samplename_edit)
        formlayout.addRow('', QtWidgets.QLabel('Example: Släggö_2016-06-01_0-10m_Net'))
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(createsample_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout, 10)
        layout.addLayout(hbox1)
        #
        return layout                

    def _load_dataset_data(self):
        """ """
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            self._dataset_list.addItem(datasetname)
        #
        if self._current_dataset:
            currentindex = self._dataset_list.findText(self._current_dataset, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._dataset_list.setCurrentIndex(currentindex)

    def _create_sample(self):
        """ """
        datasetname = str(self._dataset_list.currentText())
        samplename = str(self._samplename_edit.text())
#         if len(samplename) == 0:
#             samplename = str(self._sampleid_edit.text()) # Use id.
        #   
        plankton_core.PlanktonCounterManager().create_sample(datasetname, samplename)
        #
        self._parentwidget._emit_change_notification()
        #            
        self.accept() # Close dialog box.


class DeleteDialog(QtWidgets.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget):
        """ """
        super(DeleteDialog, self).__init__(parentwidget)
        self.setWindowTitle("Delete datasets and samples")
        self._parentwidget = parentwidget
        self.setLayout(self._content())
        self.setMinimumSize(500, 500)
        self._load_dataset_data()
        self._load_sample_data()
        
    def _content(self):
        """ """  
        contentLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(contentLayout)
        #
        self._main_tab_widget = QtWidgets.QTabWidget(self)
        contentLayout.addWidget(self._main_tab_widget)
        self._main_tab_widget.addTab(self._dataset_content(), 'Delete datasets')
        self._main_tab_widget.addTab(self._sample_content(), 'Delete samples')
        
        return contentLayout                

    # DATASETS.
    
    def _dataset_content(self):
        """ """
        widget = QtWidgets.QWidget()
        #  
        datasets_listview = QtWidgets.QListView()
        self._datasets_model = QtGui.QStandardItemModel()
        datasets_listview.setModel(self._datasets_model)

        clearall_button = app_framework.ClickableQLabel('Clear all')
        clearall_button.label_clicked.connect(self._uncheck_all_datasets)                
        markall_button = app_framework.ClickableQLabel('Mark all')
        markall_button.label_clicked.connect(self._check_all_datasets)                
        delete_button = QtWidgets.QPushButton('Delete marked dataset(s)')
        delete_button.clicked.connect(self._delete_marked_datasets)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(datasets_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        #
        widget.setLayout(layout)
        #
        return widget                

    def _load_dataset_data(self):
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
                datasetname = str(item.text())
                print(datasetname)
                plankton_core.PlanktonCounterManager().delete_dataset(datasetname)
        #
        self._parentwidget._emit_change_notification()
        #            
        self.accept() # Close dialog box.

    # SAMPLES.
    
    def _sample_content(self):
        """ """  
        widget = QtWidgets.QWidget()
        #  
        samples_listview = QtWidgets.QListView()
        self._samples_model = QtGui.QStandardItemModel()
        samples_listview.setModel(self._samples_model)
        #
        clearall_button = app_framework.ClickableQLabel('Clear all')
        clearall_button.label_clicked.connect(self._uncheck_all_samples)                
        markall_button = app_framework.ClickableQLabel('Mark all')
        markall_button.label_clicked.connect(self._check_all_samples)                
        delete_button = QtWidgets.QPushButton('Delete marked sample(s)')
        delete_button.clicked.connect(self._delete_marked_samples)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(samples_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        #
        widget.setLayout(layout)
        #
        return widget                

    def _load_sample_data(self):
        """ """
        self._samples_model.clear()        
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem('Dataset: ' + datasetname)
            self._samples_model.appendRow(item)
            # Samples.
            for samplename in plankton_core.PlanktonCounterManager().get_sample_names(datasetname):
                item = QtGui.QStandardItem(samplename)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setCheckable(True)
                self._samples_model.appendRow(item)
            
    def _check_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if item.isCheckable ():
                item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if item.isCheckable ():
                item.setCheckState(QtCore.Qt.Unchecked)

    def _delete_marked_samples(self):
        """ """
        datasetname = None
        samplename = None
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if str(item.text()).startswith('Dataset: '):
                datasetname = str(item.text()).replace('Dataset: ', '')
            if item.checkState() == QtCore.Qt.Checked:
                samplename = str(item.text())
                print(samplename)
                plankton_core.PlanktonCounterManager().delete_sample(datasetname, samplename)
        #            
        self.accept() # Close dialog box.


class BackupExportImportDialog(QtWidgets.QDialog):
    """ """
    def __init__(self, parentwidget):
        """ """
        super(BackupExportImportDialog, self).__init__(parentwidget)
        self.setWindowTitle("Plakton toolbox data export/import")
        self._parentwidget = parentwidget
        self.setLayout(self._content())
        self.setMinimumSize(600, 200)
        #
        backupzipfilename = 'BACKUP-PlanktonToolbox-ver'
        backupzipfilename += app_framework.get_version() # .replace('.', '-')
        backupzipfilename += '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        backupzipfilename += '.zip'
        self._backupzipfilename_edit.setText(backupzipfilename)
  
    def _content(self):
        """ """
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(self._content_to_backup(), 'Export to backup')
        tabWidget.addTab(self._content_from_backup(), 'Import from backup')
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        #
        return layout                
   
    def _content_to_backup(self):
        """ """
        widget = QtWidgets.QWidget()
           
        self._backupdir_edit = QtWidgets.QLineEdit('')
        self._backupdir_button = QtWidgets.QPushButton('Browse...')
        self._backupdir_button.clicked.connect(self._browse_backup_dir)
        self._backupzipfilename_edit = QtWidgets.QLineEdit('')
        self._backup_button = QtWidgets.QPushButton('Backup')
        self._backup_button.clicked.connect(self._backup)
        self._backupcancel_button = QtWidgets.QPushButton('Cancel')
        self._backupcancel_button.clicked.connec(self.reject)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label2 = QtWidgets.QLabel('Backup to directory:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._backupdir_edit, gridrow, 1, 1, 8)
        form1.addWidget(self._backupdir_button, gridrow, 9, 1, 1)
        gridrow += 1
        label3 = QtWidgets.QLabel('Backup filename (zip):')
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._backupzipfilename_edit, gridrow, 1, 1, 8)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 1) # Empty row.
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._backup_button)
        hbox1.addWidget(self._backupcancel_button)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget
           
    def _browse_backup_dir(self):
        """ """
        dirdialog = QtWidgets.QFileDialog(self)
        dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(str(self._backupdir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self._backupdir_edit.setText(dirpath)
       
    def _backup(self):
        """ """
        backup_zip_dir_name = str(self._backupdir_edit.text())
        backup_zip_file_name = str(self._backupzipfilename_edit.text())
        #
        source_dir = 'plankton_toolbox_data'
        source_dir_len = len(source_dir) + 1
        #
        try:
            backup_dir_file_name = os.path.join(backup_zip_dir_name, backup_zip_file_name)
            with zipfile.ZipFile(backup_dir_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(source_dir):
                    for file_name in files:   
                        #print('DEBUG: ' + file_name)    
                        if (not file_name.startswith('.')) and (not file_name.startswith('~')):                        
                            path_file_name = os.path.join(root, file_name)
                            zip_file_name = os.path.join('plankton_toolbox_data', path_file_name[source_dir_len:])
                            zip_file.write(path_file_name, zip_file_name)
        #
        except Exception as e:
            toolbox_utils.Logging().error('Failed to backup "plankton_toolbox_data". Error: ' + str(e))
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Failed to backup "plankton_toolbox_data". Error: ' + str(e))
        #
        self.accept() # Close dialog box.
    
    def _content_from_backup(self):
        """ """
        widget = QtWidgets.QWidget()
        #  
        self._importfile_edit = QtWidgets.QLineEdit('')
        self._importfile_button = QtWidgets.QPushButton('Browse...')
        self._importfile_button.clicked.connect(self._browse_import_files)
        self._copyold_checkbox = QtWidgets.QCheckBox('Rename the old plankton_toolbox_data before import.')
        self._copyold_checkbox.setChecked(True)
        self._import_button = QtWidgets.QPushButton('Import from backup')
        self._import_button.clicked.connect(self._import_from_backup)
        self._importcancel_button = QtWidgets.QPushButton('Cancel')
        self._importcancel_button.clicked.connec(self.reject)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label2 = QtWidgets.QLabel('Import from backup file:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._importfile_edit, gridrow, 1, 1, 1)
        form1.addWidget(self._importfile_button, gridrow, 9, 1, 1)
        gridrow += 1
        form1.addWidget(self._copyold_checkbox, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 1) # Empty row.
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._import_button)
        hbox1.addWidget(self._importcancel_button)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(100)
        widget.setLayout(layout)
        #
        return widget
  
    def _browse_import_files(self):
        """ """
        namefilter = 'Backup files (*.zip);;All files (*.*)'
        dirfilename = QtWidgets.QFileDialog.getOpenFileName(
                            self,
                            'Load backup. ',
                            '', # self._lastusedsharkwebfilename,
                            namefilter)
        # From QString to str.
        dirfilename = str(dirfilename)
        if dirfilename:
            self._importfile_edit.setText(dirfilename)
       
    def _import_from_backup(self):
        """ """
#         source_filename = 'BACKUP-PlanktonToolbox-ver1.2.0_2016-12-12_203805.zip'
        source_zip_dir_file_name = str(self._importfile_edit.text())
        if source_zip_dir_file_name:
            dest_dir = 'plankton_toolbox_data'
            #
            try:
                if self._copyold_checkbox.isChecked():
                    # Rename 'plankton_toolbox_data'.
                    dest_dir_old = dest_dir + '_OLD_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
                    os.rename(dest_dir, dest_dir_old)
                #
            except Exception: ## as e:
                toolbox_utils.Logging().error('Failed to rename plankton_toolbox_data. Check if files are locked by Excel. ') # ...Error: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Failed to rename plankton_toolbox_data.  Check if files are locked by Excel. ') # ...Error: ' + str(e))
            #
            try:
                # Extract from zip.
                with zipfile.ZipFile(source_zip_dir_file_name) as zip_file:
    #                 zip_file.extractall(dest_dir)
                    zip_file.extractall('')
                #
                QtWidgets.QMessageBox.information(self, 'Restart Plankton Toolbox', 
                                              'Please restart Plankton Toolbox to load the new species lists, etc.')
                
            #
            except Exception as e:
                toolbox_utils.Logging().error('Failed to import from backup.  Check if files are locked by Excel. ') # ...Error: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Failed to import from backup.  Check if files are locked by Excel. ') # ...Error: ' + str(e))
            #
            self._parentwidget._emit_change_notification()
            #
            self.accept() # Close dialog box.
        else:
            QtWidgets.QApplication.beep()
        

class ExportImportSamplesDialog(QtWidgets.QDialog):
    """ This dialog is allowed to access private parts in the parent widget. """
    def __init__(self, parentwidget, dataset):
        """ """
        super(ExportImportSamplesDialog, self).__init__(parentwidget)
        self.setWindowTitle("Export/import samples")
        self._parentwidget = parentwidget
        self.setLayout(self._content())
        self.setMinimumSize(800, 300)
        #
        self._current_dataset = dataset
        #
        self._load_sample_list()
        self._load_dataset_list()
  
    def _load_sample_list(self):
        """ """
        self._samples_model.clear()        
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            item = QtGui.QStandardItem('Dataset: ' + datasetname)
            self._samples_model.appendRow(item)
            # Samples.
            for samplename in plankton_core.PlanktonCounterManager().get_sample_names(datasetname):
                item = QtGui.QStandardItem(samplename)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setCheckable(True)
                self._samples_model.appendRow(item)

    def _load_dataset_list(self):
        """ """
        for datasetname in plankton_core.PlanktonCounterManager().get_dataset_names():
            self._dataset_list.addItem(datasetname)
        #
        if self._current_dataset:
            currentindex = self._dataset_list.findText(self._current_dataset, QtCore.Qt.MatchFixedString)
            if currentindex >= 0:
                self._dataset_list.setCurrentIndex(currentindex)
    
    def _content(self):
        """ """
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(self._content_export(), 'Export samples')
        tabWidget.addTab(self._content_import(), 'Import samples')
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabWidget, 10)
        #
        return layout                
   
    def _content_export(self):
        """ """
        widget = QtWidgets.QWidget()
        #
        self._browse_export_target_dir = QtWidgets.QLineEdit('')
        self._exportdir_button = QtWidgets.QPushButton('Browse...')
        self._exportdir_button.clicked.connect(self._browse_export_dir)
        #  
        samples_listview = QtWidgets.QListView()
        self._samples_model = QtGui.QStandardItemModel()
        samples_listview.setModel(self._samples_model)
        #
        clearall_button = app_framework.ClickableQLabel('Clear all')
        clearall_button.label_clicked.connect(self._uncheck_all_samples)                
        markall_button = app_framework.ClickableQLabel('Mark all')
        markall_button.label_clicked.connect(self._check_all_samples)                
        delete_button = QtWidgets.QPushButton('Export marked sample(s)')
        delete_button.clicked.connect(self._export_marked_samples)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label2 = QtWidgets.QLabel('Export to directory:')
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._browse_export_target_dir, gridrow, 1, 1, 8)
        form1.addWidget(self._exportdir_button, gridrow, 9, 1, 1)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(clearall_button)
        hbox1.addWidget(markall_button)
        hbox1.addStretch(10)
        #
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(delete_button)
        hbox2.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addWidget(samples_listview, 10)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        #
        widget.setLayout(layout)
        #
        return widget                
    
    def _browse_export_dir(self):
        """ """
        dirdialog = QtWidgets.QFileDialog(self)
        dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(str(self._browse_export_target_dir.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self._browse_export_target_dir.setText(dirpath)
    
    def _check_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if item.isCheckable ():
                item.setCheckState(QtCore.Qt.Checked)
    
    def _uncheck_all_samples(self):
        """ """
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if item.isCheckable ():
                item.setCheckState(QtCore.Qt.Unchecked)
    
    def _content_import(self):
        """ """
        widget = QtWidgets.QWidget()
        
        self._dataset_list = QtWidgets.QComboBox(self)        
        self._replaceoldsamples_checkbox = QtWidgets.QCheckBox('Replace samples with same name.')
        self._replaceoldsamples_checkbox.setChecked(True)
        importsamples_button = QtWidgets.QPushButton('Import sample(s)...')
        importsamples_button.clicked.connect(self._import_samples)               
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject) # Close dialog box.               
        # Layout widgets.
        formlayout = QtWidgets.QFormLayout()
#         formlayout.addRow('Sample id:', self._sampleid_edit)
        formlayout.addRow('Target dataset:', self._dataset_list)
        formlayout.addRow('', self._replaceoldsamples_checkbox)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(importsamples_button)
        hbox1.addWidget(cancel_button)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(formlayout)
        layout.addStretch(10)
        layout.addLayout(hbox1)
        #
        widget.setLayout(layout)
        #
        return widget
    
    def _export_marked_samples(self):
        """ """
        datasetname = None
        samplename = None
        for rowindex in range(self._samples_model.rowCount()):
            item = self._samples_model.item(rowindex, 0)
            if str(item.text()).startswith('Dataset: '):
                datasetname = str(item.text()).replace('Dataset: ', '')
            if item.checkState() == QtCore.Qt.Checked:
                samplename = str(item.text())
                #print('DEBUG: ' + datasetname + '   ' + samplename)
                try:
                    # Export path and file name.
                    export_target_dir = str(self._browse_export_target_dir.text())
                    export_target_filename = samplename + '.xlsx'
                    filepathname = os.path.join(export_target_dir, export_target_filename)
                    # Check if it already exists.
                    if os.path.isfile(filepathname):  
                        box_result =  QtWidgets.QMessageBox.warning(self, 'Warning', 
                                                     'Excel file already exists. Do you want to replace it?', 
                                                     QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)
                        if box_result != QtWidgets.QMessageBox.Ok:
                            continue
                    # Create sample object.
                    dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
                    sample_object = plankton_core.PlanktonCounterSample(dir_path, datasetname, samplename)
                    #
                    sample_object.export_sample_to_excel(export_target_dir, export_target_filename)
                #        
                except Exception as e:
                    toolbox_utils.Logging().error('Failed to export sample. ' + str(e))
                    QtWidgets.QMessageBox.warning(self, 'Warning', 'Failed to export sample. ' + str(e))
        #            
        self.accept() # Close dialog box.
    
    def _import_samples(self):
        """ """
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Import sample...')
            toolbox_utils.Logging().start_accumulated_logging()
            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            filenames = QtWidgets.QFileDialog.getOpenFileNames(
                                self,
                                'Import sample(s)',
                                '', # self._last_used_excelfile_name,
                                namefilter)
            # From QString to str.
            filenames = map(str, filenames)
            # Check if user pressed ok or cancel.
            if filenames:
                for filename in filenames:
                    # Store selected path. Will be used as default next time.
                    dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
                    datasetname = str(self._dataset_list.currentText())
                    samplename = os.path.basename(filename).replace('.xlsx', '') 
                    # Check if overwrite.
                    if self._replaceoldsamples_checkbox.isChecked() == False:
                        if os.path.exists(os.path.join(dir_path, datasetname, samplename)):
                            continue # Don't overwrite if it exists.
                    # Create sample object.
                    sample_object = plankton_core.PlanktonCounterSample(dir_path, datasetname, samplename)
                    #
                    sample_object.import_sample_from_excel(filename)
        #
        except Exception as e:
            toolbox_utils.Logging().error('Excel file import failed on exception: ' + str(e))
            QtWidgets.QMessageBox.warning(self, 'Excel file loading.\n', 
                                      'Excel file import failed on exception.\n' + str(e))
            raise
        finally:
            toolbox_utils.Logging().log_all_accumulated_rows()  
            toolbox_utils.Logging().log('Importing samples done.')
        #
        self._parentwidget._emit_change_notification()
        #            
        self.accept() # Close dialog box.



# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:

# ===========================================
# === NOTE: Save this for the future use. ===
# class ImportExportDatasetDialog(QtWidgets.QDialog):
#     """ This dialog is allowed to access private parts in the parent widget. """
#     def __init__(self, parentwidget):
#         """ """
#         super(ImportExportDatasetDialog, self).__init__(parentwidget)
#         self.setWindowTitle("Import/export dataset")
#         self._parentwidget = parentwidget
#         self.setLayout(self._content())
#         self.setMinimumSize(800, 300)
#         #
#         self._update_export_dataset_list()
#   
#     def _content(self):
#         """ """
#         tabWidget = QtWidgets.QTabWidget()
#         tabWidget.addTab(self._content_import(), 'Import')
#         tabWidget.addTab(self._content_export(), 'Export')
#         tabWidget.addTab(self._content_publish(), 'Publish')
#         #
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(tabWidget, 10)
#         #
#         return layout                
#    
#     def _content_import(self):
#         """ """
#         widget = QtWidgets.QWidget()
#         self._importsourcetype_list = QtWidgets.QComboBox()
#         self._importsourcetype_list.addItems(['<select>',
#                                            'PTBX Archive',
#                                            ])
#         self._importsourcetype_list.setCurrentIndex(1)
#         self._importsourcefile_edit = QtWidgets.QLineEdit('')
#         self._importsourcefile_button = QtWidgets.QPushButton('Browse...')
#         self._importsourcefile_button.clicked.connect(self._browse_source)
#         self._importtargetdatasetname_edit = QtWidgets.QLineEdit('')        
#         self._import_button = QtWidgets.QPushButton('Import')
#         self._import_button.clicked.connect(self._import_dataset)
#         self._importcancel_button = QtWidgets.QPushButton('Cancel')
#         self._importcancel_button.clicked.reject)
#         # Layout widgets.
#         form1 = QtWidgets.QGridLayout()
#         gridrow = 0
#         label1 = QtWidgets.QLabel('Dataset archive type:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._importsourcetype_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('Dataset archive file:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._importsourcefile_edit, gridrow, 1, 1, 9)
#         form1.addWidget(self._importsourcefile_button, gridrow, 10, 1, 1)
#         gridrow += 1
#         label3 = QtWidgets.QLabel('New dataset name:')
#         form1.addWidget(label3, gridrow, 0, 1, 1)
#         form1.addWidget(self._importtargetdatasetname_edit, gridrow, 1, 1, 9)
#         #
#         hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(5)
#         hbox1.addWidget(self._import_button)
#         hbox1.addWidget(self._importcancel_button)
#         layout = QtWidgets.QVBoxLayout()
#         layout.addLayout(form1)
#         layout.addLayout(hbox1)
#         layout.addStretch(100)
#         widget.setLayout(layout)
#         #
#         return widget
#       
#     def _browse_source(self):
#         """ """
#         dirdialog = QtWidgets.QFileDialog(self)
#         dirdialog.setDirectory(str(self._importsourcefile_edit.text()))
#         namefilter = 'Zip files (*.zip);;All files (*.*)'
#         filepath = dirdialog.getOpenFileName(
#                                 self,
#                                 'Import Archive file',
#                                 self._importsourcefile_edit.text(),
#                                 namefilter)
#         if not filepath.isEmpty():
#             self._importsourcefile_edit.setText(str(filepath))
#             head, tail = os.path.split(str(filepath))
#             self._importtargetdatasetname_edit.setText(tail.replace('.zip', ''))
#       
#     def _import_dataset(self):
#         """ """
#         QtWidgets.QMessageBox.information(self, "Information", 'Not implemented yet.')        
#           
#     def _content_export(self):
#         """ """
#         widget = QtWidgets.QWidget()
#         self._datasettoexport_list = QtWidgets.QComboBox()
#         self._datasettoexport_list.addItems(['<select>'])
#         self._datasettoexport_list.currentIndexChanged._dataset_changed)
#         self._exportsourcetype_list = QtWidgets.QComboBox()
#         self._exportsourcetype_list.addItems(['<select>',
#                                            'PTBX Archive',
#                                            ])
#         self._exportsourcetype_list.setCurrentIndex(1)
#         self._exporttargetdir_edit = QtWidgets.QLineEdit('')
#         self._exporttargetdir_button = QtWidgets.QPushButton('Browse...')
#         self._exporttargetdir_button.clicked.connect(self._browse_target_dir)
#         self._exporttargetfilename_edit = QtWidgets.QLineEdit('')
#           
#         self._publish_checkbox = QtWidgets.QCheckBox('Publish dataset')
#         self._publishtarget_list = QtWidgets.QComboBox()
#         self._publishtarget_list.addItems(['<select>',
#                                            'SHARKdata (http://sharkdata.se)',
#                                            'SHARKdata-test (http://test.sharkdata.se)',
#                                            ])
#         self._publishuser_edit = QtWidgets.QLineEdit('')
#         self._publishpassword_edit = QtWidgets.QLineEdit('')
#           
#         self._export_button = QtWidgets.QPushButton('Export/publish')
#         self._export_button.clicked.connect(self._export_dataset)
#         self._exportcancel_button = QtWidgets.QPushButton('Cancel')
#         self._exportcancel_button.clicked.reject)
#         # Layout widgets.
#         form1 = QtWidgets.QGridLayout()
#         gridrow = 0
#         label1 = QtWidgets.QLabel('Dataset to export:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._datasettoexport_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label1 = QtWidgets.QLabel('Dataset archive type:')
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._exportsourcetype_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('Export to directory:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._exporttargetdir_edit, gridrow, 1, 1, 9)
#         form1.addWidget(self._exporttargetdir_button, gridrow, 10, 1, 1)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('Export file name:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._exporttargetfilename_edit, gridrow, 1, 1, 9)
#         gridrow += 1
#         # Empty row.
#         form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._publish_checkbox, gridrow, 0, 1, 1)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('Publish on:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishtarget_list, gridrow, 1, 1, 1)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('User:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishuser_edit, gridrow, 1, 1, 5)
#         gridrow += 1
#         label2 = QtWidgets.QLabel('Password:')
#         form1.addWidget(label2, gridrow, 0, 1, 1)
#         form1.addWidget(self._publishpassword_edit, gridrow, 1, 1, 5)
#         gridrow += 1
#         # Empty row.
#         form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 1)
#         #
#         hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(5)
#         hbox1.addWidget(self._export_button)
#         hbox1.addWidget(self._exportcancel_button)
#         layout = QtWidgets.QVBoxLayout()
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
#             datasetname = str(self._datasettoexport_list.itemText(index))
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
#         dirdialog = QtWidgets.QFileDialog(self)
#         dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
#         dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
#         dirdialog.setDirectory(str(self._exporttargetdir_edit.text()))
#         dirpath = dirdialog.getExistingDirectory()
#         if dirpath:
#             self._exporttargetdir_edit.setText(dirpath)
#       
#     def _export_dataset(self):
#         """ """
#         QtWidgets.QMessageBox.information(self, "Information", 'Not implemented yet.')
#           
#     def _content_publish(self):
#         """ """
#         widget = QtWidgets.QWidget()
#         return widget
