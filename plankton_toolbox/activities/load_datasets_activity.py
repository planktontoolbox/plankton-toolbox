#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os.path
import glob
import locale

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync
# import plankton_toolbox.toolbox.help_texts as help_texts

import envmonlib
import toolbox_utils
import toolbox_core

class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._datasettabledata = DatasetTableData()
        self._last_used_textfile_name = ''
        self._last_used_excelfile_name = ''
        # Load available dataset parsers.
        self._parser_list = []
        self._load_available_parsers()
        # Initialize parent (self._create_content will be called).
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(10, self._log_available_parsers)
        

    def _load_available_parsers(self):
        """ """
        self._parser_path = 'toolbox_data/parsers/'
        self._parser_list = []
        for parserpath in glob.glob(self._parser_path + '*.xlsx'):
            self._parser_list.append(os.path.basename(parserpath))

    def _log_available_parsers(self):
        """ """
        if len(self._parser_list) > 0:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Available dataset parsers (located in "toolbox_data/parsers"):')
            for parserpath in self._parser_list:
                toolbox_utils.Logging().log('- ' + os.path.basename(parserpath))
        else:
            toolbox_utils.Logging().log('No dataset parsers are found in "/toolbox_data/parsers". ')

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
        contentLayout.addWidget(self._content_load_dataset())
        contentLayout.addWidget(self._content_loaded_datasets(), 10)
#        contentLayout.addStretch(5)
        # Style.
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
    
    def _content_load_dataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Import', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_textfile(), 'Text files (*.txt)')
        tabWidget.addTab(self._content_xlsx(), 'Excel files (*.xlsx)')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== TEXT FILES ======
    def _content_textfile(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('LoadDatasetsActivity_text_intro'))
        # - Select dataset parsers:
        self._textfile_parser_list = QtGui.QComboBox()
        self._textfile_parser_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._textfile_parser_list.addItems(["<select>"])
        self.connect(self._textfile_parser_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._textfile_parser_selected)                
        # - Add available dataset parsers.
        self._textfile_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._textfile_importcolumn_list = QtGui.QComboBox()
        self._textfile_importcolumn_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._textfile_importcolumn_list.addItems(["<no parser selected>"])        
        self.connect(self._textfile_importcolumn_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._textfile_import_column_selected)                
        # - Select export column:
        self._textfile_exportcolumn_list = QtGui.QComboBox()
        self._textfile_exportcolumn_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._textfile_exportcolumn_list.addItems(["<no parser selected>"])        
        # - Select text coding.
        self._textfile_encoding_list = QtGui.QComboBox()
        self._encodings_list = ['<platform default>',
                                'windows-1252',
                                'utf-8',
                                'utf-16',
                                'ascii',
                                'latin1',
                                'macroman']
        self._textfile_encoding_list.addItems(self._encodings_list)
        # Load dataset.
        self._textfile_getdataset_button = QtGui.QPushButton('Import dataset(s)...')
        self.connect(self._textfile_getdataset_button, QtCore.SIGNAL('clicked()'), self._load_text_files)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Select parser:')
        stretchlabel = QtGui.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel('Select import column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel('Select export column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel('Text file character encoding (affects å, è, µ, etc.):')
        hbox1.addWidget(label1)
        hbox1.addWidget(self._textfile_encoding_list)
        hbox1.addStretch(10)
        hbox1.addWidget(self._textfile_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def _textfile_parser_selected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._parser_list)):
            toolbox_utils.Logging().log('Selected parser: ' + unicode(self._parser_list[selected_row - 1]))
#            tabledata = toolbox_core.DatasetTable()
#             toolbox_utils.ExcelFiles().readToTableDataset(tabledata, 
#                                                  file_name = self._parser_path + self._parser_list[selected_row - 1])            
            tablereader = toolbox_utils.TableFileReader(file_path = self._parser_path, 
                                                        excel_file_name = self._parser_list[selected_row - 1])
            self._textfile_importcolumn_list.clear()
            self._textfile_exportcolumn_list.clear()
            header = tablereader.header()
            for row in tablereader.rows():
                if (row[0] == 'info') and (row[1] == 'column_type'):
                    for index, item in enumerate(row):
                        if item == 'import':
                            self._textfile_importcolumn_list.addItems([header[index]])
                        if item == 'export':
                            self._textfile_exportcolumn_list.addItems([header[index]])
        else:
            self._textfile_importcolumn_list.clear()
            self._textfile_importcolumn_list.addItems(['no parser selected'])
            self._textfile_exportcolumn_list.clear()
            self._textfile_exportcolumn_list.addItems(['no parser selected'])

    def _textfile_import_column_selected(self, selected_row):
        """ """
        # Reset. 
        self._textfile_encoding_list.setCurrentIndex(0)
        #
        selectedimportcolumn = unicode(self._textfile_importcolumn_list.currentText())
        # Read parser file.
#         tabledata = toolbox_core.DatasetTable()
#         toolbox_utils.ExcelFiles().readToTableDataset(tabledata, 
#                                 file_name = self._parser_path + self._parser_list[self._textfile_parser_list.currentIndex() - 1])
        tablereader = toolbox_utils.TableFileReader(file_path = self._parser_path, 
                                                    excel_file_name = self._parser_list[self._textfile_parser_list.currentIndex() - 1])
        header = tablereader.header()
        for index, headeritem in enumerate(header):
            if headeritem == selectedimportcolumn:
                for row in tablereader.rows():
                    if (row[0] == 'info') and (row[1] == 'character_encoding'):
                        if row[index] and (row[index] in self._encodings_list):
                            self._textfile_encoding_list.setCurrentIndex(self._encodings_list.index(row[index]))

    def _load_text_files(self):
        """ """
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Importing datasets...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Importing datasets...')
            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Text files (*.txt);;All files (*.*)'
            filenames = QtGui.QFileDialog.getOpenFileNames(
                                self,
                                'Import dataset(s)',
                                self._last_used_textfile_name,
                                namefilter)
            # From QString to unicode.
            filenames = map(unicode, filenames)
            # Check if user pressed ok or cancel.
            self._tabledataset = toolbox_core.DatasetTable()
            if filenames:
                for filename in filenames:
                    # Store selected path. Will be used as default next time.
                    self._last_used_textfile_name = filename
                    # Text files may have strange encodings.
                    if unicode(self._textfile_encoding_list.currentText()) == '<platform default>':
                        textfileencoding = locale.getpreferredencoding()
                    else:
                        textfileencoding = unicode(self._textfile_encoding_list.currentText())                        
                    # Set up for import file parsing.
                    importmanager = envmonlib.ImportManager(self._parser_path + unicode(self._textfile_parser_list.currentText()),
                                                     unicode(self._textfile_importcolumn_list.currentText()),
                                                     unicode(self._textfile_exportcolumn_list.currentText()))
                    # Import and parse file.
                    dataset = importmanager.importTextFile(filename, textfileencoding)
                    # Add metadata related to imported file.
                    dataset.addMetadata('parser', self._parser_path + unicode(self._textfile_parser_list.currentText()))
                    dataset.addMetadata('file_name', os.path.basename(filename))
                    dataset.addMetadata('file_path', filename)
                    dataset.addMetadata('import_column', unicode(self._textfile_importcolumn_list.currentText()))
                    dataset.addMetadata('export_column', unicode(self._textfile_exportcolumn_list.currentText()))
                    # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                    toolbox_datasets.ToolboxDatasets().add_dataset(dataset)
            #
        except Exception as e:
            toolbox_utils.Logging().error('Text file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Text file loading.\n', 
                                      'Text file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(toolbox_core.Datasets().get_datasets())
            self._write_to_status_bar('Imported datasets: ' + unicode(datasetcount))
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + unicode(datasetcount))

    # ===== EXCEL FILES ======
    def _content_xlsx(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        # Intro:
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('LoadDatasetsActivity_excel_intro'))
        # - Select dataset parser:
        self._excel_parser_list = QtGui.QComboBox()
        self._excel_parser_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._excel_parser_list.addItems(["<select>"])
        self.connect(self._excel_parser_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._excel_parser_selected)                
        # - Add available dataset parsers.
        self._excel_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._excel_importcolumn_list = QtGui.QComboBox()
        self._excel_importcolumn_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._excel_importcolumn_list.addItems(["<no parser selected>"])        
        # - Select export column:
        self._excel_exportcolumn_list = QtGui.QComboBox()
        self._excel_exportcolumn_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._excel_exportcolumn_list.addItems(["<no parser selected>"])        
        # Load dataset.
        self._excel_getdataset_button = QtGui.QPushButton('Load dataset(s)...')
        self.connect(self._excel_getdataset_button, QtCore.SIGNAL('clicked()'), self._load_excel_file)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Select parser:')
        stretchlabel = QtGui.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtGui.QLabel('Select import column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtGui.QLabel('Select export column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._excel_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _excel_parser_selected(self, selected_row):
        """ """
        if (selected_row > 0) and (selected_row <= len(self._parser_list)):
            toolbox_utils.Logging().log('Selected parser: ' + unicode(self._parser_list[selected_row - 1]))
            
#             tabledata = toolbox_core.DatasetTable()
#             toolbox_utils.ExcelFiles().readToTableDataset(tabledata, 
#                                                  file_name = self._parser_path + self._parser_list[selected_row - 1])
            tablereader = toolbox_utils.TableFileReader(file_path = self._parser_path, 
                                                        excel_file_name = self._parser_list[selected_row - 1])
            self._excel_importcolumn_list.clear()
            self._excel_exportcolumn_list.clear()
            header = tablereader.header()
            for row in tablereader.rows():
                if (row[0] == 'info') and (row[1] == 'column_type'):
                    for index, item in enumerate(row):
                        if item == 'import':
                            self._excel_importcolumn_list.addItems([header[index]])
                        if item == 'export':
                            self._excel_exportcolumn_list.addItems([header[index]])
        else:
            self._excel_importcolumn_list.clear()
            self._excel_importcolumn_list.addItems(['no parser selected'])
            self._excel_exportcolumn_list.clear()
            self._excel_exportcolumn_list.addItems(['no parser selected'])

    def _load_excel_file(self):
        """ """
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Importing datasets...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Importing datasets...')
            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            filenames = QtGui.QFileDialog.getOpenFileNames(
                                self,
                                'Import dataset(s)',
                                self._last_used_excelfile_name,
                                namefilter)
            # From QString to unicode.
            filenames = map(unicode, filenames)
            # Check if user pressed ok or cancel.
            self._tabledataset = toolbox_core.DatasetTable()
            if filenames:
                for filename in filenames:
                    # Store selected path. Will be used as default next time.
                    self._last_used_excelfile_name = filename
                    # Set up for import file parsing.
                    importmanager = envmonlib.ImportManager(self._parser_path + unicode(self._excel_parser_list.currentText()),
                                                     unicode(self._excel_importcolumn_list.currentText()),
                                                     unicode(self._excel_exportcolumn_list.currentText()))
                    # Import and parse file.
                    dataset = importmanager.importExcelFile(filename)
                    # Add metadata related to imported file.
                    dataset.addMetadata('parser', self._parser_path + unicode(self._excel_parser_list.currentText()))
                    dataset.addMetadata('file_name', os.path.basename(filename))
                    dataset.addMetadata('file_path', filename)
                    dataset.addMetadata('import_column', unicode(self._excel_importcolumn_list.currentText()))
                    dataset.addMetadata('export_column', unicode(self._excel_exportcolumn_list.currentText()))
                    # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                    toolbox_datasets.ToolboxDatasets().add_dataset(dataset)
        #
        except Exception as e:
            toolbox_utils.Logging().error('Excel file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Excel file loading.\n', 
                                      'Excel file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(toolbox_core.Datasets().get_datasets())
            self._write_to_status_bar('Imported datasets: ' + unicode(datasetcount))
            toolbox_utils.Logging().log_all_accumulated_rows()  
            toolbox_utils.Logging().log('Importing datasets done. Number of loaded datasets: ' + unicode(datasetcount))

    # ===== LOADED DATASETS =====    
    def _content_loaded_datasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Imported datasets', self)
        #
        self._datasets_table = utils_qt.ToolboxQTableView()
        self._datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self._datasettabledata.clear()
        self._datasettabledata.setHeader(['Dataset      ', 
#                                           'Type         ', 
                                          'Content      ', 
                                          'File         ', 
                                          'File path    ',
                                          'Parser       ',
                                          'Import column',
                                          'Export column'])
        self._datasets_table.tablemodel.setModeldata(self._datasettabledata)
        self._datasets_table.resizeColumnsToContents()
        
        self._datasets_table.selectionModel.Rows
        
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL('datasetListChanged'), 
             self._update_dataset_list)
        # Connection for selected row.
        self._datasets_table.clicked.connect(self._selection_changed)
                        
        # Buttons.
        self._unloadalldatasets_button = QtGui.QPushButton('Remove all datasets')
        self._unloadmarkeddatasets_button = QtGui.QPushButton('Remove marked dataset(s)')
        # If checked the selected dataset content should be viewed in the dataset viewer tool.
        self._viewdataset_checkbox = QtGui.QCheckBox('View marked dataset')
        self._viewdataset_checkbox.setChecked(False)
        # Button connections.
        self.connect(self._unloadalldatasets_button, QtCore.SIGNAL('clicked()'), self._unload_all_datasets)                
        self.connect(self._unloadmarkeddatasets_button, QtCore.SIGNAL('clicked()'), self._unload_marked_datasets)                
        self._viewdataset_checkbox.clicked.connect(self._selection_changed)
        # Layout widgets.
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self._unloadalldatasets_button)
        buttonlayout.addWidget(self._unloadmarkeddatasets_button)
        buttonlayout.addWidget(self._viewdataset_checkbox)
        buttonlayout.addStretch(5)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def _unload_all_datasets(self):
        """ """
        toolbox_datasets.ToolboxDatasets().clear()

    def _unload_marked_datasets(self):
        # Remove datasets, start with the last one. 
        rowcount = self._datasets_table.tablemodel.rowCount()
        for rowindex in range(rowcount):
            index = rowcount - rowindex - 1
            if self._datasets_table.selectionModel.isSelected(self._datasets_table.tablemodel.createIndex(index, 0)): # Check if selected by user.
                toolbox_datasets.ToolboxDatasets().remove_dataset_by_index(index)

    def _update_dataset_list(self):
        """ """
        self._datasettabledata.clearRows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            # Get content info depending on dataset type.
#             datasettype = '',
            contentinfo = ''
            if isinstance(dataset, toolbox_core.DatasetTable):
#                 datasettype = 'Table dataset'
                contentinfo = 'Rows: ' + unicode(len(dataset.getRows())) + '. '
            elif isinstance(dataset, toolbox_core.DatasetNode):
#                 datasettype = 'Tree dataset'
                visitcount, samplecound, variablecount = dataset.getCounters()
                contentinfo = 'Visits: ' + unicode(visitcount) + ', ' + \
                              'samples: ' + unicode(samplecound) + ', ' + \
                              'variables: ' + unicode(variablecount) + '. '
#             else:
#                 datasettype = 'Unspecified'

            # Add row 
            self._datasettabledata.addRow(
                ['Dataset-' + unicode(rowindex + 1),
#                  datasettype,
                 contentinfo,
                 dataset.getMetadata('file_name'),
                 dataset.getMetadata('file_path'),
                 dataset.getMetadata('parser'),
                 dataset.getMetadata('import_column'),
                 dataset.getMetadata('export_column')])
            #
        self._datasets_table.tablemodel.reset()
        self._datasets_table.resizeColumnsToContents()

    
    def _selection_changed(self):
        """ """
        if self._viewdataset_checkbox.isChecked():
            modelIndex = self._datasets_table.selectionModel.currentIndex()
            if modelIndex.isValid():
                # View tool.
                tool_manager.ToolManager().show_tool_by_name('Dataset viewer') # Show tool if hidden.
                # graphtool = tool_manager.ToolManager().getToolByName('Dataset viewer')
                toolbox_sync.ToolboxSync().set_row_index('dataset', modelIndex.row())

    
class DatasetTableData(object):
    """ """
    def __init__(self):
        """ """
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def clearRows(self):
        """ """
        self._rows = []

    def setHeader(self, header):
        """ """
        self._header = header

    def addRow(self, row):
        """ """
        self._rows.append(row)

    def getHeaderItem(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def getDataItem(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def getColumnCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return ''

    def getRowCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return ''

