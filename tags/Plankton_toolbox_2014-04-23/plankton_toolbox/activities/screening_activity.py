#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
# import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class ScreeningActivity(activity_base.ActivityBase):
    """ Used for screening of content of loaded datasets. """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(ScreeningActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self.update)
        # Data object used for plotting.
        self._graph_plot_data = None

    def update(self):
        """ """
        self.updateColumnList()
        self.updateParameterList()
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._contentScreeningTabs())

    def _contentScreeningTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._contentStructureScreening(), "Structure")
        tabWidget.addTab(self._contentCodesSpeciesScreening(), "Code lists and species")
        tabWidget.addTab(self._contentCheckColumnValues(), "Column values")
        tabWidget.addTab(self._contentPlotParameters(), "Plot parameters")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # === Content structure ===
    def _contentStructureScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_intro_0'))
        #
        self._checkdatasets_button = QtGui.QPushButton("View\ndatasets")
        self.connect(self._checkdatasets_button, QtCore.SIGNAL("clicked()"), self._checkDatasets)                
        self._checkvisits_button = QtGui.QPushButton("View\nsampling events")
        self.connect(self._checkvisits_button, QtCore.SIGNAL("clicked()"), self._checkVisits) 
        self._checksamples_button = QtGui.QPushButton("View\nsamples")
        self.connect(self._checksamples_button, QtCore.SIGNAL("clicked()"), self._checkSamples) 
        #                
        self._checkduplicates_button = QtGui.QPushButton("Scan for\nduplicates")
        self.connect(self._checkduplicates_button, QtCore.SIGNAL("clicked()"), self._scanForDuplicates)                

        # Result content.
        self._structureresult_list = QtGui.QTextEdit()
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Result:")
        form1.addWidget(label1, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkdatasets_button, gridrow, 0, 1, 1)
        form1.addWidget(self._structureresult_list, gridrow, 1, 30, 1)
        gridrow += 1
        form1.addWidget(self._checkvisits_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checksamples_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkduplicates_button, gridrow, 0, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def _checkDatasets(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        countvisits = 0
        countsamples = 0
        countvariables = 0
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                row = u'Dataset: ' + dataset.getMetadata(u'file_name')
                self._structureresult_list.append(row)
                countvisits = 0
                countsamples = 0
                countvariables = 0
                for visitnode in dataset.getChildren():
                    countvisits += 1
                    for samplenode in visitnode.getChildren():
                        countsamples += 1
                        countvariables += len(samplenode.getChildren())
                #
                row = u'   - Sampling events: ' + unicode(countvisits) + \
                      u', samples: ' + unicode(countsamples) + \
                      u', variable rows: ' + unicode(countvariables) 
                self._structureresult_list.append(row)

    def _checkVisits(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        countsamples = 0
        countvariables = 0
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                row = u'Dataset: ' + dataset.getMetadata(u'file_name')
                self._structureresult_list.append(row)
                countsamples = 0
                countvariables = 0
                for visitnode in dataset.getChildren():
                    row = u'   - Sampling event: ' + visitnode.getData(u'station_name') + \
                          u', ' + visitnode.getData(u'date')
                    self._structureresult_list.append(row)
                    countsamples = 0
                    countvariables = 0
                    for samplenode in visitnode.getChildren():
                        countsamples += 1
                        countvariables += len(samplenode.getChildren())
                    #
                    row = u'      - Samples: ' + unicode(countsamples) + \
                      u', variable rows: ' + unicode(countvariables) 
                    self._structureresult_list.append(row)

    def _checkSamples(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                row = u'Dataset: ' + dataset.getMetadata(u'file_name')
                self._structureresult_list.append(row)
                for visitnode in dataset.getChildren():
                    row = u'   - Sampling event: ' + \
                          unicode(visitnode.getData(u'station_name')) + u' ' + \
                          unicode(visitnode.getData(u'date'))
                    self._structureresult_list.append(row)
                    for samplenode in visitnode.getChildren():
                        row = u'      - Sample: ' + \
                              unicode(samplenode.getData(u'sample_min_depth')) + u'-' + \
                              unicode(samplenode.getData(u'sample_max_depth'))
                        self._structureresult_list.append(row)
                        countvariables = len(samplenode.getChildren())
                        #
                        row = u'         - Variable rows: ' + unicode(countvariables) 
                        self._structureresult_list.append(row)
                        #
                        parameter_set = set()
                        taxonname_set = set()
                        taxonsizestagesex_set = set()
                        for variablenode in samplenode.getChildren():
                            parameter = variablenode.getData(u'parameter')
                            unit = variablenode.getData(u'unit')
                            taxonname = variablenode.getData(u'scientific_name')
                            sizeclass = variablenode.getData(u'size_class')
                            stage = variablenode.getData(u'stage')
                            sex = variablenode.getData(u'sex')
                            if parameter:
                                parameter_set.add(parameter + u'+' + unit)
                            if taxonname:
                                taxonname_set.add(taxonname)
                                taxonsizestagesex_set.add(taxonname + u'+' + sizeclass + u'+' + stage + u'+' + sex)
                        row = u'         - Unique parameters/units: ' + unicode(len(parameter_set)) 
                        self._structureresult_list.append(row)
                        row = u'         - Unique taxon names: ' + unicode(len(taxonname_set)) 
                        self._structureresult_list.append(row)
                        row = u'         - Unique taxon-names/size-classes/stages/sex: ' + unicode(len(taxonsizestagesex_set)) 
                        self._structureresult_list.append(row)

    def _scanForDuplicates(self):
        """ """
        self._structureresult_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        dataset_descr = u''
        visit_descr = u''
        sample_descr = u''
        #
        check_duplicates_list = []
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                dataset_descr = dataset.getMetadata(u'file_name')
                for visitnode in dataset.getChildren():
                    visit_descr = unicode(visitnode.getData(u'station_name')) + u', ' + \
                                  unicode(visitnode.getData(u'date'))
                    for samplenode in visitnode.getChildren():
                        sample_descr = unicode(samplenode.getData(u'sample_min_depth')) + u'-' + \
                                       unicode(samplenode.getData(u'sample_max_depth'))
                        check_duplicates_list = [] # Duplicates can occur inside one sample.
                        sample_description = dataset_descr + u', ' + visit_descr + u', ' + sample_descr
                        for variablenode in samplenode.getChildren():
                            scientific_name = unicode(variablenode.getData(u'scientific_name'))
                            size_class = unicode(variablenode.getData(u'size_class'))
                            stage = unicode(variablenode.getData(u'stage'))
                            sex = unicode(variablenode.getData(u'sex'))
                            parameter = unicode(variablenode.getData(u"parameter"))
                            unit = unicode(variablenode.getData(u'unit'))
                            #
                            unique_items = (scientific_name, size_class, stage, sex, parameter, unit)
                            if unique_items in check_duplicates_list:
                                if sample_description:
                                    # Print first time for sample.
                                    self._structureresult_list.append(sample_description)
                                    sample_description = u''
                                row = u'   - Duplicate found: ' + \
                                      scientific_name + u', ' + \
                                      size_class + u', ' + \
                                      stage + u', ' + \
                                      sex + u', ' + \
                                      parameter + u', ' + \
                                      unit                                        
                                self._structureresult_list.append(row)
                            else:
                                check_duplicates_list.append(unique_items)

    # === Content code lists and species ===
    def _contentCodesSpeciesScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel_1 = utils_qt.RichTextQLabel()
#         introlabel_1.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_intro_1'))
#         introlabel_2 = utils_qt.RichTextQLabel()
#         introlabel_2.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_intro_2'))
#         introlabel_3 = utils_qt.RichTextQLabel()
#         introlabel_3.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_species'))
#         introlabel_4 = utils_qt.RichTextQLabel()
#         introlabel_4.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_sizeclasses'))
        #
        self._checkcodes_button = QtGui.QPushButton("Check\ncode lists")
        self.connect(self._checkcodes_button, QtCore.SIGNAL("clicked()"), self._codeListScreening)                
        self._checkspecies_button = QtGui.QPushButton("Check\nspecies")
        self.connect(self._checkspecies_button, QtCore.SIGNAL("clicked()"), self._speciesScreening) 
        self._checksizeclasses_button = QtGui.QPushButton("Check\nsize classes")
        self.connect(self._checksizeclasses_button, QtCore.SIGNAL("clicked()"), self._bvolScreening) 

        # Result content.
        self._codesspeciesresult_list = QtGui.QTextEdit()
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Result:")
        form1.addWidget(label1, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._checkcodes_button, gridrow, 0, 1, 1)
        form1.addWidget(self._codesspeciesresult_list, gridrow, 1, 30, 1)
        gridrow += 1
        form1.addWidget(self._checkspecies_button, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self._checksizeclasses_button, gridrow, 0, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel_1)
#         layout.addWidget(introlabel_2)
#         layout.addWidget(introlabel_3)
#         layout.addWidget(introlabel_4)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def _codeListScreening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("Code list screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Code list screening in progress...")
            # Perform screening.
            codetypes_set = envmonlib.ScreeningManager().codeListScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            # Log in result window.
            self._codesspeciesresult_list.append(u"Screening was done on these code types: " + 
                                              unicode(sorted(codetypes_set)))
            self._codesspeciesresult_list.append(u'')
            #
            inforows = envmonlib.Logging().getAllInfoRows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append(u'- ' + row)                
            warningrows = envmonlib.Logging().getAllWarnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            errorrows = envmonlib.Logging().getAllErrors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            # Also add to the logging tool.
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log("Screening was done on these code types: " + 
                                    unicode(sorted(codetypes_set)))
            envmonlib.Logging().log("Code list screening done.")
            self._writeToStatusBar("")

    def _speciesScreening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("Species screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Species screening in progress...")
            # Perform screening.
            envmonlib.ScreeningManager().speciesScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            # Log in result window.
#             self._codesspeciesresult_list.append(u"Screening was done on these code types: " + 
#                                               unicode(sorted(codetypes_set)))
#             self._codesspeciesresult_list.append(u'')
            #
            inforows = envmonlib.Logging().getAllInfoRows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append(u'- ' + row)                
            warningrows = envmonlib.Logging().getAllWarnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            errorrows = envmonlib.Logging().getAllErrors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            # Also add to the logging tool.
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"Species screening done.")
            self._writeToStatusBar("")

    def _bvolScreening(self):
        """ """
        # Screening results is also shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        self._codesspeciesresult_list.clear()
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("BVOL Species screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("BVOL Species screening in progress...")
            # Perform screening.
            envmonlib.ScreeningManager().bvolSpeciesScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            # Log in result window.
#             self._codesspeciesresult_list.append(u"Screening was done on these code types: " + 
#                                               unicode(sorted(codetypes_set)))
#             self._codesspeciesresult_list.append(u'')
            #
            inforows = envmonlib.Logging().getAllInfoRows()
            if inforows:
                for row in inforows:
                    self._codesspeciesresult_list.append(u'- ' + row)                
            warningrows = envmonlib.Logging().getAllWarnings()
            if warningrows:
                for row in warningrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            errorrows = envmonlib.Logging().getAllErrors()
            if errorrows:
                for row in errorrows:
                    self._codesspeciesresult_list.append(u'- ' + row)
            # Also add to the logging tool.
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"BVOL Species screening done.")
            self._writeToStatusBar("")

    # === Content column values ===
    def _contentCheckColumnValues(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_intro_3'))
        #
        self._column_list = QtGui.QComboBox()
        self._column_list.setMinimumContentsLength(30)
        self._column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._column_list.setEnabled(False)
        #
        self.connect(self._column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateColumnContent)                
        # Column content.
##        self._content_list = utils_qt.SelectableQListView()
##        self._content_list = QtGui.QListWidget()
        self._content_list = QtGui.QTextEdit()
#        self._content_list.setMaximumHeight(200)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Column:")
        label2 = QtGui.QLabel("Content:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_list, gridrow, 1, 30, 1)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def updateColumnList(self):
        """ """
        self._column_list.clear()
        self._content_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        if datasets and (len(datasets) > 0):        
            columns_set = set()
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for column in dataset.getExportTableColumns():
                    columns_set.add(column[u'header']) 
            #    
            self._column_list.addItems(sorted(columns_set))
            self._column_list.setEnabled(True)
        else:
            self._column_list.clear()
            self._column_list.setEnabled(False)
                               
    def _updateColumnContent(self, selected_row):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        self._content_list.clear()
        if not (datasets and (len(datasets) > 0)):        
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = u''
        key = u''
        for dataset in datasets:
            for info_dict in dataset.getExportTableColumns():
                if info_dict[u'header'] == selectedcolumn:
                    nodelevel = info_dict[u'node']
                    key = info_dict[u'key']
                    break # Break loop.
            if nodelevel:
                break # Also break next loop.
        #
        for dataset in datasets:
            if nodelevel == u'dataset':
                if key in dataset.getDataDict().keys():
                    columncontent_set.add(unicode(dataset.getData(key)))
                else:
                    columncontent_set.add(u'') # Add empty field.
            #
            for visitnode in dataset.getChildren():
                if nodelevel == u'visit':
                    if key in visitnode.getDataDict().keys():
                        columncontent_set.add(unicode(visitnode.getData(key)))
                    else:
                        columncontent_set.add(u'') # Add empty field.
                    continue    
                #
                for samplenode in visitnode.getChildren():
                    if nodelevel == u'sample':
                        if key in samplenode.getDataDict().keys():
                            columncontent_set.add(unicode(samplenode.getData(key)))
                        else:
                            columncontent_set.add(u'') # Add empty field.
                        continue    
                    #
                    for variablenode in samplenode.getChildren():
                        if nodelevel == u'variable':
                            if key in variablenode.getDataDict().keys():
                                columncontent_set.add(unicode(variablenode.getData(key)))
                            else:
                                columncontent_set.add(u'') # Add empty field.
                            continue    
        # Content list.
#        self._content_list.addItems(sorted(columncontent_set))
        for row in sorted(columncontent_set): 
            self._content_list.append(row)

    # === Content plot ===
    def _contentPlotParameters(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'ScreeningActivity_plotting'))
        #
        self._parameter_list = utils_qt.SelectableQListView()       
        #
        clearall_label = utils_qt.ClickableQLabel("Clear all")
        markall_label = utils_qt.ClickableQLabel("Mark all")
        self.connect(clearall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.uncheckAll)                
        self.connect(markall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.checkAll)                
        #
        self._plotparameters_button = QtGui.QPushButton("Plot parameter values")
        self.connect(self._plotparameters_button, QtCore.SIGNAL("clicked()"), self._plotScreening)                
        self._plotparameterperdate_button = QtGui.QPushButton("Plot parameters values per date")
        self.connect(self._plotparameterperdate_button, QtCore.SIGNAL("clicked()"), self._plotScreeningPerDate)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Parameters:")
        form1.addWidget(label1, gridrow, 0, 1, 2)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 30)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 0, 1, 1)
        form1.addWidget(markall_label, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._plotparameters_button)
        hbox1.addWidget(self._plotparameterperdate_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget

    def updateParameterList(self):
        """ """
        self._parameter_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        if datasets and (len(datasets) > 0):        
            parameter_set = set()
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for visitnode in dataset.getChildren():
                    for samplenode in visitnode.getChildren():
                        for variablenode in samplenode.getChildren():
                            parameter_set.add(variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')')
            self._parameter_list.setList(sorted(parameter_set))

    def _plotScreening(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().showToolByName(u'Graph plotter')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        graphtool.clearPlotData()
        # Set up plot data for this type.
        self._graph_plot_data = envmonlib.GraphPlotData(
                        title = u'Parameter values in sequence', 
                        y_type = u'float',
                        x_label = u'Sequence position in dataset',
                        y_label = u'Value')        
        # One plot for each selected parameter.
        for parameter in self._parameter_list.getSelectedDataList():
            self._addPlot(parameter)
        # View in the graph-plot tool.    
        graphtool.setChartSelection(chart = u"Line chart",
                                    combined = True, stacked = False, y_log_scale = True)
        graphtool.setPlotData(self._graph_plot_data)   

    def _addPlot(self, parameter):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        yarray = []
#        unit_set = set() # In case of different units on the same parameter.
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for visitnode in dataset.getChildren():
                    for samplenode in visitnode.getChildren():
                        for variablenode in samplenode.getChildren():
                            if (variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')') == parameter:
#                                 unit_set.add(variablenode.getData(u"unit"))
                                value = variablenode.getData(u"value")
                                yarray.append(value)                  
        #
#         units = u' --- '.join(sorted(unit_set))
#         parameter_unit = parameter + u' (' + units + u')' 
        #
#         self._graph_plot_data.addPlot(plot_name = parameter_unit, y_array = yarray)
        try:
            self._graph_plot_data.addPlot(plot_name = parameter, y_array = yarray)
        except UserWarning, e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))

    def _plotScreeningPerDate(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().showToolByName(u'Graph plotter')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        graphtool.clearPlotData()
        # Set up plot data for this type.
        self._graph_plot_data = envmonlib.GraphPlotData(
                        title = u'Parameter values per date', 
                        x_type = u'date',
                        y_type = u'float',
                        y_label = u'Value')        
        # One plot for each selected parameter.
        for parameter in self._parameter_list.getSelectedDataList():
            self._addPlotPerDate(parameter)
        # View in the graph-plot tool.    
        graphtool.setChartSelection(chart = u'Scatter chart',
                                    combined = True, stacked = False, y_log_scale = True)
        graphtool.setPlotData(self._graph_plot_data)   

    def _addPlotPerDate(self, parameter):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        xarray = []
        yarray = []
#        unit_set = set() # In case of different units on the same parameter.
        #
        if datasets and (len(datasets) > 0):
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for visitnode in dataset.getChildren():
                    date = visitnode.getData(u'date')
                    for samplenode in visitnode.getChildren():
                        for variablenode in samplenode.getChildren():
                            if (variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')') == parameter:
#                                 unit_set.add(variablenode.getData(u'unit'))
                                value = variablenode.getData(u'value')
                                xarray.append(date)                  
                                yarray.append(value)                  
        #
#         units = u' --- '.join(sorted(unit_set))
#         parameter_unit = parameter + u' (' + units + u')' 
        #
#         self._graph_plot_data.addPlot(plot_name = parameter_unit, y_array = yarray)
        try:
            self._graph_plot_data.addPlot(plot_name = parameter, x_array = xarray, y_array = yarray)
        except UserWarning, e:
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
