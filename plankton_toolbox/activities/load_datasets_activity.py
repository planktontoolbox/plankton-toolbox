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

import toolbox_utils
import plankton_core

class LoadDatasetsActivity(activity_base.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._last_used_textfile_name = ''
        self._last_used_excelfile_name = ''
        # Load available dataset parsers.
        self._parser_list = []
        self._load_available_parsers()
        #
        self._lastusedphytowinfilename = ''
        # Initialize parent (self._create_content will be called).
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(10, self._log_available_parsers)
        
        # Update plankton counter datasets. 
        self._counter_update_dataset_list()
        # Update plankton counter datasets when changes occured.
        self.connect(plankton_core.PlanktonCounterManager(), 
             QtCore.SIGNAL('planktonCounterListChanged'), 
             self._counter_update_dataset_list)

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
        self._activityheader = utils_qt.HeaderQLabel()
        self._activityheader.setText('<h2>' + self.objectName() + '</h2>')
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_load_dataset())
        contentLayout.addWidget(self._content_loaded_datasets(), 10)
#        contentLayout.addStretch(5)
    
    def _content_load_dataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Import datasets/datafiles', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_plankton_counter(), 'Plankton counter datasets')
        tabWidget.addTab(self._content_predefined_formats(), 'Predefined formats')
        tabWidget.addTab(self._content_textfile(), 'Data files - Text (*.txt)')
        tabWidget.addTab(self._content_xlsx(), 'Data files - Excel (*.xlsx)')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== PLANKTON COUNTER DATASETS ======
    def _content_plankton_counter(self):
        """ """
        widget = QtGui.QWidget()
        #
        counter_datasets_listview = QtGui.QListView()
        self._counter_datasets_model = QtGui.QStandardItemModel()
        counter_datasets_listview.setModel(self._counter_datasets_model)
        #
        self._cleara_metadata_button = QtGui.QPushButton('Clear all')
        self.connect(self._cleara_metadata_button, QtCore.SIGNAL('clicked()'), self._counter_uncheck_all_datasets)                
        self._markall_button = QtGui.QPushButton('Mark all')
        self.connect(self._markall_button, QtCore.SIGNAL('clicked()'), self._counter_check_all_datasets)                
        self._importcounterdataset_button = QtGui.QPushButton('Import marked dataset(s)')
        self.connect(self._importcounterdataset_button, QtCore.SIGNAL('clicked()'), self._counter_import_counter_datasets)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._cleara_metadata_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        hbox1.addWidget(self._importcounterdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(counter_datasets_listview, 10)
        layout.addLayout(hbox1)
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
            
    def _counter_check_all_datasets(self):
        """ """
        for rowindex in range(self._counter_datasets_model.rowCount()):
            item = self._counter_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _counter_uncheck_all_datasets(self):
        """ """
        for rowindex in range(self._counter_datasets_model.rowCount()):
            item = self._counter_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _counter_import_counter_datasets(self):
        """ """
        # Create a list with selected datasets.
        selectedsamples = []
        for rowindex in range(self._counter_datasets_model.rowCount()):
            item = self._counter_datasets_model.item(rowindex, 0)
            if item.checkState() == QtCore.Qt.Checked:        
                selectedsamples.append(unicode(item.text()))
        #
        if len(selectedsamples) == 0:
            return
        #            
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Importing datasets...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Importing datasets...')

            for datasetandsample in selectedsamples:
                datasetandsamplepair = datasetandsample.split(':')
                dataset_name = datasetandsamplepair[0].strip()
                sample_name = datasetandsamplepair[1].strip()
            
                print('DEBUG: dataset_name: ' + dataset_name)
                print('DEBUG: sample_name: ' + sample_name)


                datasetnode = plankton_core.DataImportManager().import_dataset_file(dataset_name = dataset_name, 
                                                                                    sample_name = sample_name, 
                                                                                    import_format = 'PlanktonCounter')
                # Use datasets-wrapper to emit change notification when dataset list is updated.
                toolbox_datasets.ToolboxDatasets().emit_change_notification()

                # Add metadata related to imported file.
                datasetnode.add_metadata('parser', '-')
#                 datasetnode.add_metadata('file_name', os.path.basename(filename))
#                 datasetnode.add_metadata('file_path', filename)
                datasetnode.add_metadata('import_column', '-')
                datasetnode.add_metadata('export_column', '-')
            #
        except Exception as e:
            toolbox_utils.Logging().error('Plankton conter file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Plankton conter file loading.\n', 
                                      'Plankton conter file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(plankton_core.Datasets().get_datasets())
            self._write_to_status_bar('Imported datasets: ' + unicode(datasetcount))
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + unicode(datasetcount))

            
            
            
            

    # ===== PREDEFINED FORMATS ======
    def _content_predefined_formats(self):
        """ """
        widget = QtGui.QWidget()
        # - Select dataset parsers:
        self._predefined_format_combo = QtGui.QComboBox()
        self._predefined_format_combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self.connect(self._textfile_parser_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._textfile_parser_selected)                
        # - Add available dataset parsers.
#         self._predefinedformat_list = ['PTBX Archive Format (*.zip) (Not implemented)',
#                                     'PTBX Archive Format (http://sharkdata.se) (Not implemented)',
#                                     'PTBX Archive Format (http://test.sharkdata.se) (Not implemented)',
#                                     'Darwin Core Archive (Not implemented)',
#                                     'Darwin Core Archive - EurOBIS (Not implemented)',
#                                     'PhytoWin (*.cvs)']
        self._predefinedformat_list = ['PhytoWin (*.cvs)']
        self._predefined_format_combo.addItems(self._predefinedformat_list)
        
        self._predefined_format_combo.setCurrentIndex(0) # 'PhytoWin (*.cvs)
        
        # Load dataset.
        self._predefined_getdataset_button = QtGui.QPushButton('Import datasets/datafiles...')
        self.connect(self._predefined_getdataset_button, QtCore.SIGNAL('clicked()'), self._import_predefined_datasets)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel('Format:')
        stretchlabel = QtGui.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._predefined_format_combo, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._predefined_getdataset_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def _import_predefined_datasets(self):
        """ """
        selectedformat = self._predefined_format_combo.currentText()
        if selectedformat == 'PhytoWin (*.cvs)':
            self._load_phytowin_datasets()
        else: 
            QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')

    def _load_phytowin_datasets(self):
        """ """
        try:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Importing datasets...')
            toolbox_utils.Logging().start_accumulated_logging()
            self._write_to_status_bar('Importing datasets...')

            # Show select file dialog box. Multiple files can be selected.
            namefilter = 'Phytowin files (*.csv);;All files (*.*)'
            filenames = QtGui.QFileDialog.getOpenFileNames(
                                self,
                                'Load PhytoWin file(s). ',
                                self._lastusedphytowinfilename,
                                namefilter)
            # From QString to unicode.
            filenames = map(unicode, filenames)
            # Check if user pressed ok or cancel.
#             phytowin = plankton_core.ImportPhytowin()
#             self._tabledataset = plankton_core.DatasetTable()
            if filenames:
                for filename in filenames:
                    self._lastusedphytowinfilename = filename


                    datasetnode = plankton_core.DataImportManager().import_dataset_file(filename, 
                                                                                        import_format = 'PhytoWin')
                    # Use datasets-wrapper to emit change notification when dataset list is updated.
                    toolbox_datasets.ToolboxDatasets().emit_change_notification()


#                     phytowin.clear()
#                     phytowin.read_file(filename)
# #                     # Used for report 'combined datasets'.
# #                     phytowin.add_to_table_dataset(self._tabledataset)
#                     # Add as tree dataset for calculated reports.
#                     datasetnode = plankton_core.DatasetNode()
#                     phytowin.add_to_dataset_node(datasetnode)
#                     # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
#                     toolbox_datasets.ToolboxDatasets().add_dataset(datasetnode)
                    # Add metadata related to imported file.
                    datasetnode.add_metadata('parser', '-')
                    datasetnode.add_metadata('file_name', os.path.basename(filename))
                    datasetnode.add_metadata('file_path', filename)
                    datasetnode.add_metadata('import_column', '-')
                    datasetnode.add_metadata('export_column', '-')
            #
        except Exception as e:
            toolbox_utils.Logging().error('PhytoWin file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Text file loading.\n', 
                                      'PhytoWin file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(plankton_core.Datasets().get_datasets())
            self._write_to_status_bar('Imported datasets: ' + unicode(datasetcount))
            toolbox_utils.Logging().log_all_accumulated_rows()
            toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + unicode(datasetcount))

        
        

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
#            tabledata = plankton_core.DatasetTable()
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
            self._textfile_importcolumn_list.addItems(['<no parser selected>'])
            self._textfile_exportcolumn_list.clear()
            self._textfile_exportcolumn_list.addItems(['<no parser selected>'])

    def _textfile_import_column_selected(self, selected_row):
        """ """
        # Reset. 
        self._textfile_encoding_list.setCurrentIndex(0)
        #
        selectedimportcolumn = unicode(self._textfile_importcolumn_list.currentText())
        # Read parser file.
#         tabledata = plankton_core.DatasetTable()
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
            self._tabledataset = plankton_core.DatasetTable()
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
                    importmanager = plankton_core.ImportManager(self._parser_path + unicode(self._textfile_parser_list.currentText()),
                                                     unicode(self._textfile_importcolumn_list.currentText()),
                                                     unicode(self._textfile_exportcolumn_list.currentText()))
                    # Import and parse file.
                    dataset = importmanager.import_text_file(filename, textfileencoding)
                    # Add metadata related to imported file.
                    dataset.add_metadata('parser', self._parser_path + unicode(self._textfile_parser_list.currentText()))
                    dataset.add_metadata('file_name', os.path.basename(filename))
                    dataset.add_metadata('file_path', filename)
                    dataset.add_metadata('import_column', unicode(self._textfile_importcolumn_list.currentText()))
                    dataset.add_metadata('export_column', unicode(self._textfile_exportcolumn_list.currentText()))
                    # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                    toolbox_datasets.ToolboxDatasets().add_dataset(dataset)
            #
        except Exception as e:
            toolbox_utils.Logging().error('Text file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Text file loading.\n', 
                                      'Text file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(plankton_core.Datasets().get_datasets())
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
        self._excel_getdataset_button = QtGui.QPushButton('Import dataset(s)...')
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
            
#             tabledata = plankton_core.DatasetTable()
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
            self._tabledataset = plankton_core.DatasetTable()
            if filenames:
                for filename in filenames:
                    # Store selected path. Will be used as default next time.
                    self._last_used_excelfile_name = filename
                    # Set up for import file parsing.
                    importmanager = plankton_core.ImportManager(self._parser_path + unicode(self._excel_parser_list.currentText()),
                                                     unicode(self._excel_importcolumn_list.currentText()),
                                                     unicode(self._excel_exportcolumn_list.currentText()))
                    # Import and parse file.
                    dataset = importmanager.import_excel_file(filename)
                    # Add metadata related to imported file.
                    dataset.add_metadata('parser', self._parser_path + unicode(self._excel_parser_list.currentText()))
                    dataset.add_metadata('file_name', os.path.basename(filename))
                    dataset.add_metadata('file_path', filename)
                    dataset.add_metadata('import_column', unicode(self._excel_importcolumn_list.currentText()))
                    dataset.add_metadata('export_column', unicode(self._excel_exportcolumn_list.currentText()))
                    # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                    toolbox_datasets.ToolboxDatasets().add_dataset(dataset)
        #
        except Exception as e:
            toolbox_utils.Logging().error('Excel file import failed on exception: ' + unicode(e))
            QtGui.QMessageBox.warning(self, 'Excel file loading.\n', 
                                      'Excel file import failed on exception.\n' + unicode(e))
            raise
        finally:
            datasetcount = len(plankton_core.Datasets().get_datasets())
            self._write_to_status_bar('Imported datasets: ' + unicode(datasetcount))
            toolbox_utils.Logging().log_all_accumulated_rows()  
            toolbox_utils.Logging().log('Importing datasets done. Number of loaded datasets: ' + unicode(datasetcount))

    # ===== LOADED DATASETS =====    
    def _content_loaded_datasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Imported datasets/datafiles', self)
        #
        self._datasets_table = utils_qt.ToolboxQTableView()
        self._datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self._datasets_table.getTableModel().clear()
        self._datasets_table.getTableModel().set_header(
                                        ['Dataset      ', 
#                                        'Type         ', 
                                         'Content      ', 
                                         'File         ', 
                                         'File path    ',
                                         'Parser       ',
                                         'Import column',
                                         'Export column'])
        self._datasets_table.resetModel()
        self._datasets_table.resizeColumnsToContents()
        
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL('datasetListChanged'), 
             self._update_dataset_list)
        # Connection for selected row.
        self._datasets_table.clicked.connect(self._selection_changed)
        self._datasets_table.doubleClicked.connect(self._view_dataset)
                        
        # Buttons.
        self._unloadalldatasets_button = QtGui.QPushButton('Remove all datasets')
        self._unloadmarkeddatasets_button = QtGui.QPushButton('Remove marked dataset(s)')
        # If checked the selected dataset content should be viewed in the dataset viewer tool.
        self._viewdataset_checkbox = QtGui.QCheckBox('View marked dataset')
        self._viewdataset_checkbox.setChecked(False)
        # Button connections.
        self.connect(self._unloadalldatasets_button, QtCore.SIGNAL('clicked()'), self._unload_all_datasets)                
        self.connect(self._unloadmarkeddatasets_button, QtCore.SIGNAL('clicked()'), self._unload_marked_datasets)                
        self._viewdataset_checkbox.stateChanged.connect(self._selection_changed)
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
        rowcount = self._datasets_table.getTableModel().get_row_count()
        for rowindex in range(rowcount):
            index = rowcount - rowindex - 1
            if self._datasets_table.getSelectionModel().isSelected(self._datasets_table._tablemodel.createIndex(index, 0)): # Check if selected by user.
                toolbox_datasets.ToolboxDatasets().remove_dataset_by_index(index)

    def _update_dataset_list(self):
        """ """
        self._datasets_table.getTableModel().clear_rows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            # Get content info depending on dataset type.
#             datasettype = '',
            contentinfo = ''
            if isinstance(dataset, plankton_core.DatasetTable):
#                 datasettype = 'Table dataset'
                contentinfo = 'Rows: ' + unicode(len(dataset.get_rows())) + '. '
            elif isinstance(dataset, plankton_core.DatasetNode):
#                 datasettype = 'Tree dataset'
                visitcount, samplecound, variablecount = dataset.get_counters()
                contentinfo = 'Visits: ' + unicode(visitcount) + ', ' + \
                              'samples: ' + unicode(samplecound) + ', ' + \
                              'variables: ' + unicode(variablecount) + '. '
#             else:
#                 datasettype = 'Unspecified'

            # Add row 
            self._datasets_table.getTableModel().append_row(
                ['Dataset-' + unicode(rowindex + 1),
#                  datasettype,
                 contentinfo,
                 dataset.get_metadata('file_name'),
                 dataset.get_metadata('file_path'),
                 dataset.get_metadata('parser'),
                 dataset.get_metadata('import_column'),
                 dataset.get_metadata('export_column')])
            #
        self._datasets_table.resetModel()
        self._datasets_table.resizeColumnsToContents()

    
    def _selection_changed(self):
        """ """
        if self._viewdataset_checkbox.isChecked():
            self._view_dataset()

    def _view_dataset(self):
        """ """
        modelIndex = self._datasets_table.getSelectionModel().currentIndex()
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

    def clear_rows(self):
        """ """
        self._rows = []

    def set_header(self, header):
        """ """
        self._header = header

    def addRow(self, row):
        """ """
        self._rows.append(row)

    def get_header_item(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def get_data_item(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def get_column_count(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return ''

    def get_row_count(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return ''

