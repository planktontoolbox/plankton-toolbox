#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import pathlib
import os.path
import glob
import locale

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import plankton_core
import app_framework
import app_tools

class LoadDatasetsActivity(app_framework.ActivityBase):
    """ """
    def __init__(self, name, parentwidget):
        """ """
        self._last_used_textfile_name = ''
        self._last_used_excelfile_name = ''
        # Load available dataset parsers.
        self._parser_list = []
        self._load_available_parsers()
        #
        self._lastusedsharkwebfilename = ''
        self._lastusedphytowinfilename = ''
        self._lastusedplanktoncounterfilename = ''
        # Initialize parent (self._create_content will be called).
        super(LoadDatasetsActivity, self).__init__(name, parentwidget)
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(10, self._log_available_parsers)
        
        # Update plankton counter datasets. 
        self._counter_update_dataset_list()
        # Update plankton counter datasets when changes occured.
        plankton_core.PlanktonCounterManager().planktonCounterListChanged.connect(self._counter_update_dataset_list)

    def _load_available_parsers(self):
        """ """
        try:
            plankton_toolbox_data_path = app_framework.ToolboxUserSettings().get_path_to_plankton_toolbox_data()
            self._parser_path = str(pathlib.Path(plankton_toolbox_data_path, 'parsers'))
            self._parser_list = []
            for parserpath in glob.glob(self._parser_path + '/*.xlsx'):
                self._parser_list.append(os.path.basename(parserpath))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _log_available_parsers(self):
        """ """
        try:
            if len(self._parser_list) > 0:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Available dataset parsers (located in "plankton_toolbox_data/parsers"):')
                for parserpath in self._parser_list:
                    toolbox_utils.Logging().log('- ' + os.path.basename(parserpath))
            else:
                toolbox_utils.Logging().log('No dataset parsers are found in "/plankton_toolbox_data/parsers". ')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = app_framework.HeaderQLabel()
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
        try:
            # Active widgets and connections.
            selectdatabox = QtWidgets.QGroupBox('Import datasets/datafiles', self)
            tabWidget = QtWidgets.QTabWidget()
            tabWidget.addTab(self._content_predefined_formats(), 'Predefined formats')
            tabWidget.addTab(self._content_plankton_counter(), 'Plankton counter samples')
            tabWidget.addTab(self._content_textfile(), 'Parsers - Text file (*.txt)')
            tabWidget.addTab(self._content_xlsx(), 'Parsers - Excel files (*.xlsx)')
            # Layout widgets.
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(tabWidget)
            selectdatabox.setLayout(layout)
            #
            return selectdatabox
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # ===== PLANKTON COUNTER DATASETS ======
    def _content_plankton_counter(self):
        """ """
        widget = QtWidgets.QWidget()
        #
        counter_datasets_listview = QtWidgets.QListView()
        self._counter_datasets_model = QtGui.QStandardItemModel()
        counter_datasets_listview.setModel(self._counter_datasets_model)
        #
        self._cleara_metadata_button = app_framework.ClickableQLabel('Clear all')
        self._cleara_metadata_button.label_clicked.connect(self._counter_uncheck_all_datasets)
        self._markall_button = app_framework.ClickableQLabel('Mark all')
        self._markall_button.label_clicked.connect(self._counter_check_all_datasets)
        self._importcounterdataset_button = QtWidgets.QPushButton('Import marked dataset(s)')
        self._importcounterdataset_button.clicked.connect(self._counter_import_counter_datasets)
        self._importcounter_trophic_list_checkbox = QtWidgets.QCheckBox('Update trophic types')
        self._importcounter_trophic_list_checkbox.setChecked(True)

        # Layout widgets.
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self._cleara_metadata_button)
        hbox1.addWidget(self._markall_button)
#         hbox1.addStretch(10)
        hbox1.addWidget(self._importcounterdataset_button)
        hbox1.addWidget(self._importcounter_trophic_list_checkbox)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(counter_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _counter_update_dataset_list(self):
        """ """
        try:
            self._counter_datasets_model.clear()
            for datasetname in sorted(plankton_core.PlanktonCounterManager().get_dataset_names()):
                for samplename in sorted(plankton_core.PlanktonCounterManager().get_sample_names(datasetname)):
                    item = QtGui.QStandardItem(datasetname + ': ' + samplename)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    item.setCheckable(True)
                    self._counter_datasets_model.appendRow(item)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _counter_check_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._counter_datasets_model.rowCount()):
                item = self._counter_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Checked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
            
    def _counter_uncheck_all_datasets(self):
        """ """
        try:
            for rowindex in range(self._counter_datasets_model.rowCount()):
                item = self._counter_datasets_model.item(rowindex, 0)
                item.setCheckState(QtCore.Qt.Unchecked)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _counter_import_counter_datasets(self):
        """ """
        try:
            # Create a list with selected datasets.
            selectedsamples = []
            for rowindex in range(self._counter_datasets_model.rowCount()):
                item = self._counter_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    selectedsamples.append(str(item.text()))
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
                
    #                 print('DEBUG: dataset_name: ' + dataset_name)
    #                 print('DEBUG: sample_name: ' + sample_name)
    
                    update_trophic_type = self._importcounter_trophic_list_checkbox.isChecked()
                    datasetnode = plankton_core.DataImportManager().import_dataset_file(dataset_name = dataset_name, 
                                                                                        sample_name = sample_name, 
                                                                                        import_format = 'PlanktonCounter',
                                                                                        update_trophic_type=update_trophic_type)
                    # Use datasets-wrapper to emit change notification when dataset list is updated.
                    app_framework.ToolboxDatasets().emit_change_notification()
    
                    # Add metadata related to imported file.
                    datasetnode.add_metadata('parser', '-')
                    datasetnode.add_metadata('file_name', datasetandsample)
                    datasetnode.add_metadata('file_path', '-')
                    datasetnode.add_metadata('import_column', '-')
                    datasetnode.add_metadata('export_column', '-')
                #
            except Exception as e:
                toolbox_utils.Logging().error('Plankton conter file import failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Plankton conter file loading.\n', 
                                          'Plankton conter file import failed on exception.\n' + str(e))
                raise
            finally:
                datasetcount = len(plankton_core.Datasets().get_datasets())
                self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + str(datasetcount))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

            
            
            
            

    # ===== PREDEFINED FORMATS ======
    def _content_predefined_formats(self):
        """ """
        widget = QtWidgets.QWidget()
        # - Select dataset parsers:
        self._predefined_format_combo = QtWidgets.QComboBox()
        self._predefined_format_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
#         self._textfile_parser_list.currentIndexChanged(int)'), self._textfile_parser_selected)                
        # - Add available dataset parsers.
#         self._predefinedformat_list = ['PTBX Archive Format (*.zip) (Not implemented)',
#                                     'PTBX Archive Format (http://sharkdata.se) (Not implemented)',
#                                     'PTBX Archive Format (http://test.sharkdata.se) (Not implemented)',
#                                     'Darwin Core Archive (Not implemented)',
#                                     'Darwin Core Archive - EurOBIS (Not implemented)',
#                                     'PhytoWin (*.csv)']
        self._predefinedformat_list = ['Plankton counter sample(s) (*.xlsx)', 
                                       'SHARKweb download(s) (*.txt)',
#                                        'Phytoplankton-archive (*.csv)'
                                       ]
        self._predefined_format_combo.addItems(self._predefinedformat_list)
        
        self._predefined_format_combo.setCurrentIndex(0) # 0 = 'Plankton counter sample(s) (*.xlsx)'
        
        # Load dataset.
        self._predefined_getdataset_button = QtWidgets.QPushButton('Import datasets/datafiles...')
        self._predefined_getdataset_button.clicked.connect(self._import_predefined_datasets)
        self._predefined_trophic_list_checkbox = QtWidgets.QCheckBox('Update trophic types')
        self._predefined_trophic_list_checkbox.setChecked(True)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Format:')
        stretchlabel = QtWidgets.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._predefined_format_combo, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        #
        hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(10)
        hbox1.addWidget(self._predefined_getdataset_button)
        hbox1.addWidget(self._predefined_trophic_list_checkbox)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def _import_predefined_datasets(self):
        """ """
        try:
            selectedformat = self._predefined_format_combo.currentText()
            if selectedformat == 'Plankton counter sample(s) (*.xlsx)':
                self._load_plankton_counter_excel()
            elif selectedformat == 'SHARKweb download(s) (*.txt)':
                self._load_sharkweb_datasets()
    #         elif selectedformat == 'Phytoplankton-archive (*.csv)':
    #             self._load_phytowin_datasets()
            else: 
                QtWidgets.QMessageBox.information(self, "Information", 'Not implemented yet.')
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _load_plankton_counter_excel(self):
        """ """
        try:
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Importing datasets...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('Importing datasets...')
    
                # Show select file dialog box. Multiple files can be selected.
                namefilter = 'Plankton counter samples (*.xlsx);;All files (*.*)'
                filenames, _filters = QtWidgets.QFileDialog.getOpenFileNames(
                                    self,
                                    'Load plankton counter sample file(s). ',
                                    self._lastusedplanktoncounterfilename,
                                    namefilter)
                # Check if user pressed ok or cancel.
                if filenames:
                    for filename in filenames:
                        self._lastusedplanktoncounterfilename = filename
                        update_trophic_type = self._predefined_trophic_list_checkbox.isChecked()
                        datasetnode = plankton_core.DataImportManager().import_dataset_file(filename, 
                                                                                            import_format = 'PlanktonCounterExcel', 
                                                                                            update_trophic_type=update_trophic_type)
                        # Use datasets-wrapper to emit change notification when dataset list is updated.
                        app_framework.ToolboxDatasets().emit_change_notification()
                        # Add metadata related to imported file.
                        datasetnode.add_metadata('parser', '-')
                        datasetnode.add_metadata('file_name', os.path.basename(filename))
                        datasetnode.add_metadata('file_path', filename)
                        datasetnode.add_metadata('import_column', '-')
                        datasetnode.add_metadata('export_column', '-')
                #
            except Exception as e:
                toolbox_utils.Logging().error('Plankton counter sample import failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Text file loading.\n', 
                                          'Plankton counter sample import failed on exception.\n' + str(e))
                raise
            finally:
                datasetcount = len(plankton_core.Datasets().get_datasets())
                self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + str(datasetcount))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _load_sharkweb_datasets(self):
        """ """
        try:
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Importing datasets...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('Importing datasets...')
    
                # Show select file dialog box. Multiple files can be selected.
                namefilter = 'SHARKweb files (*.txt);;All files (*.*)'
                filenames, _filters = QtWidgets.QFileDialog.getOpenFileNames(
                                    self,
                                    'Load SHARKweb file(s). ',
                                    self._lastusedsharkwebfilename,
                                    namefilter)
                # Check if user pressed ok or cancel.
                if filenames:
                    for filename in filenames:
                        self._lastusedsharkwebfilename = filename
                        update_trophic_type = self._predefined_trophic_list_checkbox.isChecked()
                        datasetnode = plankton_core.DataImportManager().import_dataset_file(filename, 
                                                                                            import_format = 'SHARKweb',
                                                                                            update_trophic_type=update_trophic_type)
                        # Use datasets-wrapper to emit change notification when dataset list is updated.
                        app_framework.ToolboxDatasets().emit_change_notification()
                        # Add metadata related to imported file.
                        datasetnode.add_metadata('parser', '-')
                        datasetnode.add_metadata('file_name', os.path.basename(filename))
                        datasetnode.add_metadata('file_path', filename)
                        datasetnode.add_metadata('import_column', '-')
                        datasetnode.add_metadata('export_column', '-')
                #
            except Exception as e:
                toolbox_utils.Logging().error('SHARKweb file import failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Text file loading.\n', 
                                          'SHARKweb file import failed on exception.\n' + str(e))
                raise
            finally:
                datasetcount = len(plankton_core.Datasets().get_datasets())
                self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + str(datasetcount))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

#     def _load_phytowin_datasets(self):
#         """ """
#         try:
#             toolbox_utils.Logging().log('') # Empty line.
#             toolbox_utils.Logging().log('Importing datasets...')
#             toolbox_utils.Logging().start_accumulated_logging()
#             self._write_to_status_bar('Importing datasets...')
# 
#             # Show select file dialog box. Multiple files can be selected.
#             namefilter = 'Phytowin files (*.csv);;All files (*.*)'
#             filenames, _filters = QtWidgets.QFileDialog.getOpenFileNames(
#                                 self,
#                                 'Load PhytoWin file(s). ',
#                                 self._lastusedphytowinfilename,
#                                 namefilter)
#             # From QString to str.
#             filenames = map(str, filenames)
#             # Check if user pressed ok or cancel.
# #             phytowin = plankton_core.ImportPhytowin()
# #             self._tabledataset = plankton_core.DatasetTable()
#             if filenames:
#                 for filename in filenames:
#                     self._lastusedphytowinfilename = filename
# 
# 
#                     datasetnode = plankton_core.DataImportManager().import_dataset_file(filename, 
#                                                                                         import_format = 'PhytoWin')
#                     # Use datasets-wrapper to emit change notification when dataset list is updated.
#                     app_framework.ToolboxDatasets().emit_change_notification()
# 
# 
# #                     phytowin.clear()
# #                     phytowin.read_file(filename)
# # #                     # Used for report 'combined datasets'.
# # #                     phytowin.add_to_table_dataset(self._tabledataset)
# #                     # Add as tree dataset for calculated reports.
# #                     datasetnode = plankton_core.DatasetNode()
# #                     phytowin.add_to_dataset_node(datasetnode)
# #                     # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
# #                     app_framework.ToolboxDatasets().add_dataset(datasetnode)
#                     # Add metadata related to imported file.
#                     datasetnode.add_metadata('parser', '-')
#                     datasetnode.add_metadata('file_name', os.path.basename(filename))
#                     datasetnode.add_metadata('file_path', filename)
#                     datasetnode.add_metadata('import_column', '-')
#                     datasetnode.add_metadata('export_column', '-')
#             #
#         except Exception as e:
#             toolbox_utils.Logging().error('PhytoWin file import failed on exception: ' + str(e))
#             QtWidgets.QMessageBox.warning(self, 'Text file loading.\n', 
#                                       'PhytoWin file import failed on exception.\n' + str(e))
#             raise
#         finally:
#             datasetcount = len(plankton_core.Datasets().get_datasets())
#             self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
#             toolbox_utils.Logging().log_all_accumulated_rows()
#             toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + str(datasetcount))

        
        

    # ===== TEXT FILES ======
    def _content_textfile(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('LoadDatasetsActivity_text_intro'))
        # - Select dataset parsers:
        self._textfile_parser_list = QtWidgets.QComboBox()
        self._textfile_parser_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._textfile_parser_list.addItems(["<select>"])
        self._textfile_parser_list.currentIndexChanged.connect(self._textfile_parser_selected)                
        # - Add available dataset parsers.
        self._textfile_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._textfile_importcolumn_list = QtWidgets.QComboBox()
        self._textfile_importcolumn_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._textfile_importcolumn_list.addItems(["<no parser selected>"])        
        self._textfile_importcolumn_list.currentIndexChanged.connect(self._textfile_import_column_selected)                
        # - Select export column:
        self._textfile_exportcolumn_list = QtWidgets.QComboBox()
        self._textfile_exportcolumn_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._textfile_exportcolumn_list.addItems(["<no parser selected>"])        
        # - Select text coding.
        self._textfile_encoding_list = QtWidgets.QComboBox()
        self._encodings_list = ['<platform default>',
                                'windows-1252',
                                'utf-8',
                                'utf-16',
                                'ascii',
                                'latin1',
                                'macroman']
        self._textfile_encoding_list.addItems(self._encodings_list)
        # Load dataset.
        self._textfile_getdataset_button = QtWidgets.QPushButton('Import dataset(s)...')
        self._textfile_getdataset_button.clicked.connect(self._load_text_files)
        self._textfile_trophic_list_checkbox = QtWidgets.QCheckBox('Update trophic types')
        self._textfile_trophic_list_checkbox.setChecked(True)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Select parser:')
        stretchlabel = QtWidgets.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select import column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select export column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._textfile_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel('Text file character encoding (affects å, è, µ, etc.):')
        hbox1.addWidget(label1)
        hbox1.addWidget(self._textfile_encoding_list)
#         hbox1.addStretch(10)
        hbox1.addWidget(self._textfile_getdataset_button)
        hbox1.addWidget(self._textfile_trophic_list_checkbox)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def _textfile_parser_selected(self, selected_row):
        """ """
        try:
            if (selected_row > 0) and (selected_row <= len(self._parser_list)):
                toolbox_utils.Logging().log('Selected parser: ' + str(self._parser_list[selected_row - 1]))
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _textfile_import_column_selected(self, selected_row):
        """ """
        try:
            # Reset. 
            self._textfile_encoding_list.setCurrentIndex(0)
            #
            selectedimportcolumn = str(self._textfile_importcolumn_list.currentText())
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _load_text_files(self):
        """ """
        try:
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Importing datasets...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('Importing datasets...')
                # Show select file dialog box. Multiple files can be selected.
                namefilter = 'Text files (*.txt);;All files (*.*)'
                filenames, _filters = QtWidgets.QFileDialog.getOpenFileNames(
                                    self,
                                    'Import dataset(s)',
                                    self._last_used_textfile_name,
                                    namefilter)
                # Check if user pressed ok or cancel.
                self._tabledataset = plankton_core.DatasetTable()
                if filenames:
                    for filename in filenames:
                        # Store selected path. Will be used as default next time.
                        self._last_used_textfile_name = filename
                        # Text files may have strange encodings.
                        if str(self._textfile_encoding_list.currentText()) == '<platform default>':
                            textfileencoding = locale.getpreferredencoding()
                        else:
                            textfileencoding = str(self._textfile_encoding_list.currentText())                        
                        # Set up for import file parsing.
                        importmanager = plankton_core.ImportManager(str(pathlib.Path(self._parser_path, str(self._textfile_parser_list.currentText()))),
                                                         str(self._textfile_importcolumn_list.currentText()),
                                                         str(self._textfile_exportcolumn_list.currentText()))
                        # Import and parse file.
                        dataset = importmanager.import_text_file(filename, textfileencoding)
                        
                        
                        
                                
                        
                        # Update trophic_type.
                        update_trophic_type = self._textfile_trophic_list_checkbox.isChecked()
                        print('DEBUG: excel_trophic_list')
                        for visit in dataset.get_children():
                            for sample in visit.get_children():
                                for variable in sample.get_children():
                                    trophic_type = variable.get_data('trophic_type', '')
                                    # Update all trophic_types.
                                    if update_trophic_type:
                                        scientific_name = variable.get_data('scientific_name', '')
                                        size_class = variable.get_data('size_class', '')
                                        trophic_type = plankton_core.Species().get_bvol_value(scientific_name, size_class, 'trophic_type')
                                        if trophic_type:
                                            variable.add_data('trophic_type', trophic_type) # Use existing if not in local list.
                                    # Replace empty with NS=Not specified.
                                    if not trophic_type:
                                        variable.add_data('trophic_type', 'NS')
                        
                        
                        
                        # Add metadata related to imported file.
                        dataset.add_metadata('parser', str(pathlib.Path(self._parser_path, str(self._textfile_parser_list.currentText()))))
                        dataset.add_metadata('file_name', os.path.basename(filename))
                        dataset.add_metadata('file_path', filename)
                        dataset.add_metadata('import_column', str(self._textfile_importcolumn_list.currentText()))
                        dataset.add_metadata('export_column', str(self._textfile_exportcolumn_list.currentText()))
                        # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                        app_framework.ToolboxDatasets().add_dataset(dataset)
                #
            except Exception as e:
                toolbox_utils.Logging().error('Text file import failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Text file loading.\n', 
                                          'Text file import failed on exception.\n' + str(e))
                raise
            finally:
                datasetcount = len(plankton_core.Datasets().get_datasets())
                self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
                toolbox_utils.Logging().log_all_accumulated_rows()
                toolbox_utils.Logging().log('Importing datasets done. Number of imported datasets: ' + str(datasetcount))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # ===== EXCEL FILES ======
    def _content_xlsx(self):
        """ """
        widget = QtWidgets.QWidget()
        # Active widgets and connections.
        # Intro:
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('LoadDatasetsActivity_excel_intro'))
        # - Select dataset parser:
        self._excel_parser_list = QtWidgets.QComboBox()
        self._excel_parser_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._excel_parser_list.addItems(["<select>"])
        self._excel_parser_list.currentIndexChanged.connect(self._excel_parser_selected)                
        # - Add available dataset parsers.
        self._excel_parser_list.addItems(self._parser_list)                
        # - Select import column:
        self._excel_importcolumn_list = QtWidgets.QComboBox()
        self._excel_importcolumn_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._excel_importcolumn_list.addItems(["<no parser selected>"])        
        # - Select export column:
        self._excel_exportcolumn_list = QtWidgets.QComboBox()
        self._excel_exportcolumn_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._excel_exportcolumn_list.addItems(["<no parser selected>"])        
        # Load dataset.
        self._excel_getdataset_button = QtWidgets.QPushButton('Import dataset(s)...')
        self._excel_getdataset_button.clicked.connect(self._load_excel_file)                
        self._excel_trophic_list_checkbox = QtWidgets.QCheckBox('Update trophic types')
        self._excel_trophic_list_checkbox.setChecked(True)
        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Select parser:')
        stretchlabel = QtWidgets.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_parser_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,2, 1, 9)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select import column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_importcolumn_list, gridrow, 1, 1, 1)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select export column:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._excel_exportcolumn_list, gridrow, 1, 1, 1)
        #
        hbox1 = QtWidgets.QHBoxLayout()
#         hbox1.addStretch(10)
        hbox1.addWidget(self._excel_getdataset_button)
        hbox1.addWidget(self._excel_trophic_list_checkbox)
        hbox1.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _excel_parser_selected(self, selected_row):
        """ """
        try:
            if (selected_row > 0) and (selected_row <= len(self._parser_list)):
                toolbox_utils.Logging().log('Selected parser: ' + str(self._parser_list[selected_row - 1]))
                
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _load_excel_file(self):
        """ """
        try:
            try:
                toolbox_utils.Logging().log('') # Empty line.
                toolbox_utils.Logging().log('Importing datasets...')
                toolbox_utils.Logging().start_accumulated_logging()
                self._write_to_status_bar('Importing datasets...')
                # Show select file dialog box. Multiple files can be selected.
                namefilter = 'Excel files (*.xlsx);;All files (*.*)'
                filenames, _filters = QtWidgets.QFileDialog.getOpenFileNames(
                                    self,
                                    'Import dataset(s)',
                                    self._last_used_excelfile_name,
                                    namefilter)
                # Check if user pressed ok or cancel.
                self._tabledataset = plankton_core.DatasetTable()
                if filenames:
                    for filename in filenames:
                        # Store selected path. Will be used as default next time.
                        self._last_used_excelfile_name = filename
                        # Set up for import file parsing.
                        importmanager = plankton_core.ImportManager(str(pathlib.Path(self._parser_path, str(self._excel_parser_list.currentText()))),
                                                         str(self._excel_importcolumn_list.currentText()),
                                                         str(self._excel_exportcolumn_list.currentText()))
                        # Import and parse file.
                        dataset = importmanager.import_excel_file(filename)
                        
                        
                        
                        # Update trophic_type.
                        update_trophic_type = self._excel_trophic_list_checkbox.isChecked()
                        print('DEBUG: excel_trophic_list')
                        for visit in dataset.get_children():
                            for sample in visit.get_children():
                                for variable in sample.get_children():
                                    trophic_type = variable.get_data('trophic_type', '')
                                    # Update all trophic_types.
                                    if update_trophic_type:
                                        scientific_name = variable.get_data('scientific_name', '')
                                        size_class = variable.get_data('size_class', '')
                                        trophic_type = plankton_core.Species().get_bvol_value(scientific_name, size_class, 'trophic_type')
                                        if trophic_type:
                                            variable.add_data('trophic_type', trophic_type) # Use existing if not in local list.
                                    # Replace empty with NS=Not specified.
                                    if not trophic_type:
                                        variable.add_data('trophic_type', 'NS')
                        
                        
                        
                        # Add metadata related to imported file.
                        dataset.add_metadata('parser', str(pathlib.Path(self._parser_path, str(self._excel_parser_list.currentText()))))
                        dataset.add_metadata('file_name', os.path.basename(filename))
                        dataset.add_metadata('file_path', filename)
                        dataset.add_metadata('import_column', str(self._excel_importcolumn_list.currentText()))
                        dataset.add_metadata('export_column', str(self._excel_exportcolumn_list.currentText()))
                        # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
                        app_framework.ToolboxDatasets().add_dataset(dataset)
            #
            except Exception as e:
                toolbox_utils.Logging().error('Excel file import failed on exception: ' + str(e))
                QtWidgets.QMessageBox.warning(self, 'Excel file loading.\n', 
                                          'Excel file import failed on exception.\n' + str(e))
                raise
            finally:
                datasetcount = len(plankton_core.Datasets().get_datasets())
                self._write_to_status_bar('Imported datasets: ' + str(datasetcount))
                toolbox_utils.Logging().log_all_accumulated_rows()  
                toolbox_utils.Logging().log('Importing datasets done. Number of loaded datasets: ' + str(datasetcount))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # ===== LOADED DATASETS =====    
    def _content_loaded_datasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtWidgets.QGroupBox('Imported datasets/datafiles', self)
        #
        self._datasets_table = app_framework.ToolboxQTableView()
        self._datasets_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self._datasets_table.getTableModel().clear()
        self._datasets_table.getTableModel().set_header(
                                        ['Import      ', 
#                                        'Type         ', 
                                         'Content      ', 
                                         'File or dataset     ', 
                                         'File-path or sample ',
                                         'Parser       ',
                                         'Import column',
                                         'Export column'])
        self._datasets_table.resetModel()
        self._datasets_table.resizeColumnsToContents()
        
        # Listen for changes in the toolbox dataset list.
        app_framework.ToolboxDatasets().datasetListChanged.connect(self._update_dataset_list)
        # Connection for selected row.
        self._datasets_table.clicked.connect(self._selection_changed)
        self._datasets_table.doubleClicked.connect(self._view_dataset)
                        
        # Buttons.
        self._unloadalldatasets_button = QtWidgets.QPushButton('Remove all datasets')
        self._unloadmarkeddatasets_button = QtWidgets.QPushButton('Remove marked dataset(s)')
        # If checked the selected dataset content should be viewed in the dataset viewer tool.
        self._viewdataset_checkbox = QtWidgets.QCheckBox('View marked dataset')
#         self._viewdataset_checkbox.setChecked(False)
        self._viewdataset_checkbox.setChecked(True)
        self._viewdataset_checkbox.hide()
        # Button connections.
        self._unloadalldatasets_button.clicked.connect(self._unload_all_datasets)                
        self._unloadmarkeddatasets_button.clicked.connect(self._unload_marked_datasets)                
        self._viewdataset_checkbox.stateChanged.connect(self._selection_changed)
        # Layout widgets.
        buttonlayout = QtWidgets.QHBoxLayout()
        buttonlayout.addWidget(self._unloadalldatasets_button)
        buttonlayout.addWidget(self._unloadmarkeddatasets_button)
        buttonlayout.addWidget(self._viewdataset_checkbox)
        buttonlayout.addStretch(5)
        #
        widget = QtWidgets.QWidget()        
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def _unload_all_datasets(self):
        """ """
        try:
            app_framework.ToolboxDatasets().clear()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _unload_marked_datasets(self):
        # Remove datasets, start with the last one. 
        try:
            rowcount = self._datasets_table.getTableModel().get_row_count()
            for rowindex in range(rowcount):
                index = rowcount - rowindex - 1
                if self._datasets_table.getSelectionModel().isSelected(self._datasets_table._tablemodel.createIndex(index, 0)): # Check if selected by user.
                    app_framework.ToolboxDatasets().remove_dataset_by_index(index)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _update_dataset_list(self):
        """ """
        try:
            self._datasets_table.getTableModel().clear_rows()
            for rowindex, dataset in enumerate(app_framework.ToolboxDatasets().get_datasets()):
                # Get content info depending on dataset type.
    #             datasettype = '',
                contentinfo = ''
                if isinstance(dataset, plankton_core.DatasetTable):
    #                 datasettype = 'Table dataset'
                    contentinfo = 'Rows: ' + str(len(dataset.get_rows())) + '. '
                elif isinstance(dataset, plankton_core.DatasetNode):
    #                 datasettype = 'Tree dataset'
                    visitcount, samplecound, variablecount = dataset.get_counters()
                    contentinfo = 'Visits: ' + str(visitcount) + ', ' + \
                                  'samples: ' + str(samplecound) + ', ' + \
                                  'variables: ' + str(variablecount) + '. '
    #             else:
    #                 datasettype = 'Unspecified'
    
                # Add row 
                self._datasets_table.getTableModel().append_row(
                    ['Import-' + str(rowindex + 1),
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
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def _selection_changed(self):
        """ """
        try:
            if self._viewdataset_checkbox.isChecked():
                self._view_dataset()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _view_dataset(self):
        """ """
        try:
            modelIndex = self._datasets_table.getSelectionModel().currentIndex()
            if modelIndex.isValid():
                # View tool.
                app_tools.ToolManager().show_tool_by_name('Dataset viewer') # Show tool if hidden.
                # graphtool = tool_manager.ToolManager().getToolByName('Dataset viewer')
                app_framework.AppSync().set_row_index('dataset', modelIndex.row())
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    
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

