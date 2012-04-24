#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
"""

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import envmonlib
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources
import plankton_toolbox.core.biology.taxa_prepare as taxa_prepare
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class ManageSpeciesListsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(ManageSpeciesListsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
#        self._activityheader.setStyleSheet(""" 
#            * { color: white; background-color: #00677f; }
#            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        widget = QtGui.QTabWidget()
        contentLayout.addWidget(widget)
        widget.addTab(self._createContentDyntaxa(), "Dyntaxa")
        widget.addTab(self._createContentPeg(), "PEG")
        widget.addTab(self._createContentHarmfulPlankton(), "Harmful plankton")
        
    def _createContentDyntaxa(self):
        """ """        
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._dyntaxasource_list = QtGui.QComboBox()
        self._dyntaxasource_list.addItems(["<select>",
                                            "(Dyntaxa, SOAP)",
                                            "(Dyntaxa, REST)",
                                            "Dyntaxa, DB-tables as text files"])
        self._dyntaxafromdirectory_edit = QtGui.QLineEdit("")
        self._dyntaxafrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath')
        self._dyntaxatofile_edit = QtGui.QLineEdit(filepath)        
        self._dyntaxato_button = QtGui.QPushButton("Browse...")
        self._dyntaxametadata_table = QtGui.QTableWidget()
        self._dyntaxametadata_button = QtGui.QPushButton("(Edit metadata...)")
        self._dyntaxaprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self._dyntaxafrom_button, QtCore.SIGNAL("clicked()"), self._dyntaxaFromBrowse)               
        self.connect(self._dyntaxato_button, QtCore.SIGNAL("clicked()"), self._dyntaxaToBrowse)               
        self.connect(self._dyntaxametadata_button, QtCore.SIGNAL("clicked()"), self._editDyntaxaMetadata)                
        self.connect(self._dyntaxaprepare_button, QtCore.SIGNAL("clicked()"), self._prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Source type:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._dyntaxasource_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._dyntaxafromdirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._dyntaxafrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._dyntaxatofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._dyntaxato_button, gridrow, 10, 1, 1)
        gridrow += 1
        label4 = QtGui.QLabel("Metadata:")
        form1.addWidget(label4, gridrow, 0, 1, 1)
        form1.addWidget(self._dyntaxametadata_table, gridrow, 1, 10, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._dyntaxametadata_button)
        hbox1.addWidget(self._dyntaxaprepare_button)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget

    def _createContentPeg(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
###        self._pegfromfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_extended_peg_version_2010-10-26.txt")
        self._pegfromfile_edit = QtGui.QLineEdit("smhi_extended_peg_version_xxxx-xx-xx.txt")
        self._pegfrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        self._pegtofile_edit = QtGui.QLineEdit(filepath)
        self._pegto_button = QtGui.QPushButton("Browse...")        
###        self._pwtopegfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/translate_pw_to_smhi_extended_peg.txt")
        self._pwtopegfile_edit = QtGui.QLineEdit("translate_pw_to_smhi_extended_peg.txt")
        self._pwtopegfile_button = QtGui.QPushButton("Browse...")
###        self._pegtodyntaxafile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_peg_to_dyntaxa.txt")
        self._pegtodyntaxafile_edit = QtGui.QLineEdit("smhi_peg_to_dyntaxa.txt")
        self._pegtodyntaxafile_button = QtGui.QPushButton("Browse...")
        self._pegmetadata_table = QtGui.QTableWidget()
        self._pegmetadata_button = QtGui.QPushButton("(Edit metadata...)")
        self._pegprepare_button = QtGui.QPushButton("Create resource")
        #
        self.connect(self._pegfrom_button, QtCore.SIGNAL("clicked()"), self._pegFromBrowse)              
        self.connect(self._pegto_button, QtCore.SIGNAL("clicked()"), self._pegToBrowse)
        self.connect(self._pwtopegfile_button, QtCore.SIGNAL("clicked()"), self._pwToPegFileBrowse)
        self.connect(self._pegtodyntaxafile_button, QtCore.SIGNAL("clicked()"), self._pegToDyntaxaFileBrowse)
        self.connect(self._pegmetadata_button, QtCore.SIGNAL("clicked()"), self._editPegMetadata)                
        self.connect(self._pegprepare_button, QtCore.SIGNAL("clicked()"), self._preparePeg)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.txt):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._pegfromfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._pegfrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Translate PW to PEG file (.txt):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._pwtopegfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._pwtopegfile_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Translate PEG to Dyntaxa file (.txt):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._pegtodyntaxafile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._pegtodyntaxafile_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._pegtofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._pegto_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._pegmetadata_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._pegmetadata_button)
        hbox1.addWidget(self._pegprepare_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget

    def _createContentHarmfulPlankton(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._harmfulfromfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_harmful_plankton.txt")
###        self._harmfulfromfile_edit = QtGui.QLineEdit("")
        self._harmfulfrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath')
        self._harmfultofile_edit = QtGui.QLineEdit(filepath)
        self._harmfulto_button = QtGui.QPushButton("Browse...")        
        #
        self._harmfulmetadata_table = QtGui.QTableWidget()
        self._harmfulmetadata_button = QtGui.QPushButton("(Edit metadata...)")
        self._harmfulprepare_button = QtGui.QPushButton("Create resource")
        #
        self.connect(self._harmfulfrom_button, QtCore.SIGNAL("clicked()"), self._harmfulFromBrowse)              
        self.connect(self._harmfulto_button, QtCore.SIGNAL("clicked()"), self._harmfulToBrowse)
        self.connect(self._harmfulmetadata_button, QtCore.SIGNAL("clicked()"), self._editHarmfulMetadata)                
        self.connect(self._harmfulprepare_button, QtCore.SIGNAL("clicked()"), self._prepareHarmful)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.txt):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._harmfulfromfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._harmfulfrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self._harmfultofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self._harmfulto_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self._harmfulmetadata_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self._harmfulmetadata_button)
        hbox1.addWidget(self._harmfulprepare_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget

    def _dyntaxaFromBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self._dyntaxafromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self._dyntaxafromdirectory_edit.setText(dirpath)
#        """ """
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setDirectory(unicode(self._dyntaxafromdirectory_edit.text()))
#        filepath = dirdialog.getOpenFileName()
#        if filepath:
#            self._dyntaxafromdirectory_edit.setText(filepath)

    def _dyntaxaToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._dyntaxatofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._dyntaxatofile_edit.setText(filepath)

    def _pegFromBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._pegfromfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._pegfromfile_edit.setText(filepath)

# self.connect(self._pwtopegfile_button, QtCore.SIGNAL("clicked()"), self._pwToPegFileBrowse)
    def _pwToPegFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._pwtopegfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._pwtopegfile_edit.setText(filepath)

# self.connect(self._pegtodyntaxafile_button, QtCore.SIGNAL("clicked()"), self._pegToDyntaxaFileBrowse)
    def _pegToDyntaxaFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._pegtodyntaxafile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._pegtodyntaxafile_edit.setText(filepath)

    def _pegToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._pegtofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._pegtofile_edit.setText(filepath)

    def _editDyntaxaMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def _prepareDyntaxa(self):
        """ """
        envmonlib.Logging().log("Prepare dyntaxa. Started.")
        envmonlib.Logging().clear()
        self._writeToStatusBar("Prepare dyntaxa.")
        try:
            if self._dyntaxasource_list.currentIndex() == 3:
                dt = taxa.Dyntaxa()
                importer = taxa_prepare.PrepareDyntaxaDbTablesAsTextFiles(taxaObject = dt)
                importer.importTaxa(unicode(self._dyntaxafromdirectory_edit.text()))
                envmonlib.Logging().log('Number of dyntaxa taxa: ' + str(len(dt.getTaxonList())))
                exporter = taxa_sources.JsonFile(taxaObject = dt)                
                exporter.exportTaxa(file = unicode(self._dyntaxatofile_edit.text()))
            else:
                raise UserWarning('The selected data source type is not implemented.')
        except UserWarning, e:
            envmonlib.Logging().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            envmonlib.Logging().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            envmonlib.Logging().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            envmonlib.Logging().logAllWarnings()    
            envmonlib.Logging().logAllErrors()    
            envmonlib.Logging().info("Prepare dyntaxa. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourceDyntaxa()

    def _editPegMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def _preparePeg(self):
        """ """
        envmonlib.Logging().log("Prepare PEG. Started.")
        envmonlib.Logging().clear()
        self._writeToStatusBar("Prepare PEG.")
        try:
            peg = taxa.Peg()
            importer = taxa_prepare.PreparePegTextFile(taxaObject = peg)
            importer.importTaxa(file = unicode(self._pegfromfile_edit.text()))
            # New:
            
            
            
############################            importer.addPwToPeg(file = unicode(self._pwtopegfile_edit.text()))
            
            
            
            
            importer.addDyntaxaToPeg(file = unicode(self._pegtodyntaxafile_edit.text()))
            #
            envmonlib.Logging().log('Number of PEG taxa: ' + str(len(peg.getTaxonList())))                
            exporter = taxa_sources.JsonFile(taxaObject = peg)
            exporter.exportTaxa(file = unicode(self._pegtofile_edit.text()))
        except UserWarning, e:
            envmonlib.Logging().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            envmonlib.Logging().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            envmonlib.Logging().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            envmonlib.Logging().logAllWarnings()    
            envmonlib.Logging().logAllErrors()    
            envmonlib.Logging().log("Prepare PEG. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourcePeg()

    def _harmfulFromBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._harmfulfromfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._harmfulfromfile_edit.setText(filepath)

    def _harmfulToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self._harmfultofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self._harmfultofile_edit.setText(filepath)

    def _editHarmfulMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def _prepareHarmful(self):
        """ """
        envmonlib.Logging().log("Prepare Harmful plankton. Started.")
        envmonlib.Logging().clear()
        self._writeToStatusBar("Prepare Harmful plankton.")
        try:
            harmful = taxa.HarmfulPlankton()
            importer = taxa_prepare.PrepareHarmfulMicroAlgae(taxaObject = harmful)
            importer.importTaxa(file = unicode(self._harmfulfromfile_edit.text()))
            #
            envmonlib.Logging().log('Number of Harmful plankton taxa: ' + str(len(harmful.getTaxonList())))                
            exporter = taxa_sources.JsonFile(taxaObject = harmful)
            exporter.exportTaxa(file = unicode(self._harmfultofile_edit.text()))
        except UserWarning, e:
            envmonlib.Logging().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            envmonlib.Logging().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            envmonlib.Logging().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            envmonlib.Logging().logAllWarnings()    
            envmonlib.Logging().logAllErrors()    
            envmonlib.Logging().log("Prepare Harmful plankton. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourceHarmfulPlankton()

