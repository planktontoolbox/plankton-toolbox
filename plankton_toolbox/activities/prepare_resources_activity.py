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
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources
import plankton_toolbox.core.biology.taxa_prepare as taxa_prepare
import plankton_toolbox.toolbox.toolbox_resources as toolbox_resources

class PrepareResourcesActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(PrepareResourcesActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self.__activityheader = QtGui.QLabel('<b>Activity: ' + self.objectName() + '</b>', self)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self.__activityheader)
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
        self.__dyntaxasource_list = QtGui.QComboBox()
        self.__dyntaxasource_list.addItems(["<select>",
                                            "(Dyntaxa, SOAP)",
                                            "(Dyntaxa, REST)",
                                            "Dyntaxa, DB-tables as text files"])
        self.__dyntaxafromdirectory_edit = QtGui.QLineEdit("")
        self.__dyntaxafrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath')
        self.__dyntaxatofile_edit = QtGui.QLineEdit(filepath)        
        self.__dyntaxato_button = QtGui.QPushButton("Browse...")
        self.__dyntaxametadata_table = QtGui.QTableWidget()
        self.__dyntaxametadata_button = QtGui.QPushButton("(Edit metadata...)")
        self.__dyntaxaprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.__dyntaxafrom_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaFromBrowse)               
        self.connect(self.__dyntaxato_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaToBrowse)               
        self.connect(self.__dyntaxametadata_button, QtCore.SIGNAL("clicked()"), self.__editDyntaxaMetadata)                
        self.connect(self.__dyntaxaprepare_button, QtCore.SIGNAL("clicked()"), self.__prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Source type:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__dyntaxasource_list, gridrow, 1, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__dyntaxafromdirectory_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__dyntaxafrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self.__dyntaxatofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__dyntaxato_button, gridrow, 10, 1, 1)
        gridrow += 1
        label4 = QtGui.QLabel("Metadata:")
        form1.addWidget(label4, gridrow, 0, 1, 1)
        form1.addWidget(self.__dyntaxametadata_table, gridrow, 1, 10, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__dyntaxametadata_button)
        hbox1.addWidget(self.__dyntaxaprepare_button)
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
###        self.__pegfromfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_extended_peg_version_2010-10-26.txt")
        self.__pegfromfile_edit = QtGui.QLineEdit("smhi_extended_peg_version_xxxx-xx-xx.txt")
        self.__pegfrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        self.__pegtofile_edit = QtGui.QLineEdit(filepath)
        self.__pegto_button = QtGui.QPushButton("Browse...")        
###        self.__pwtopegfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/translate_pw_to_smhi_extended_peg.txt")
        self.__pwtopegfile_edit = QtGui.QLineEdit("translate_pw_to_smhi_extended_peg.txt")
        self.__pwtopegfile_button = QtGui.QPushButton("Browse...")
###        self.__pegtodyntaxafile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_peg_to_dyntaxa.txt")
        self.__pegtodyntaxafile_edit = QtGui.QLineEdit("smhi_peg_to_dyntaxa.txt")
        self.__pegtodyntaxafile_button = QtGui.QPushButton("Browse...")
        self.__pegmetadata_table = QtGui.QTableWidget()
        self.__pegmetadata_button = QtGui.QPushButton("(Edit metadata...)")
        self.__pegprepare_button = QtGui.QPushButton("Create resource")
        #
        self.connect(self.__pegfrom_button, QtCore.SIGNAL("clicked()"), self.__pegFromBrowse)              
        self.connect(self.__pegto_button, QtCore.SIGNAL("clicked()"), self.__pegToBrowse)
        self.connect(self.__pwtopegfile_button, QtCore.SIGNAL("clicked()"), self.__pwToPegFileBrowse)
        self.connect(self.__pegtodyntaxafile_button, QtCore.SIGNAL("clicked()"), self.__pegToDyntaxaFileBrowse)
        self.connect(self.__pegmetadata_button, QtCore.SIGNAL("clicked()"), self.__editPegMetadata)                
        self.connect(self.__pegprepare_button, QtCore.SIGNAL("clicked()"), self.__preparePeg)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.txt):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__pegfromfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__pegfrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Translate PW to PEG file (.txt):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__pwtopegfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__pwtopegfile_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("Translate PEG to Dyntaxa file (.txt):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__pegtodyntaxafile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__pegtodyntaxafile_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__pegtofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__pegto_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self.__pegmetadata_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__pegmetadata_button)
        hbox1.addWidget(self.__pegprepare_button)
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
        self.__harmfulfromfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_harmful_plankton.txt")
###        self.__harmfulfromfile_edit = QtGui.QLineEdit("")
        self.__harmfulfrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath')
        self.__harmfultofile_edit = QtGui.QLineEdit(filepath)
        self.__harmfulto_button = QtGui.QPushButton("Browse...")        
        #
        self.__harmfulmetadata_table = QtGui.QTableWidget()
        self.__harmfulmetadata_button = QtGui.QPushButton("(Edit metadata...)")
        self.__harmfulprepare_button = QtGui.QPushButton("Create resource")
        #
        self.connect(self.__harmfulfrom_button, QtCore.SIGNAL("clicked()"), self.__harmfulFromBrowse)              
        self.connect(self.__harmfulto_button, QtCore.SIGNAL("clicked()"), self.__harmfulToBrowse)
        self.connect(self.__harmfulmetadata_button, QtCore.SIGNAL("clicked()"), self.__editHarmfulMetadata)                
        self.connect(self.__harmfulprepare_button, QtCore.SIGNAL("clicked()"), self.__prepareHarmful)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("From file (.txt):")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__harmfulfromfile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__harmfulfrom_button, gridrow, 10, 1, 1)
        gridrow += 1
        label2 = QtGui.QLabel("To file (.json):")
        form1.addWidget(label2, gridrow, 0, 1, 1)
        form1.addWidget(self.__harmfultofile_edit, gridrow, 1, 1, 9)
        form1.addWidget(self.__harmfulto_button, gridrow, 10, 1, 1)
        gridrow += 1
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, gridrow, 0, 1, 1)
        form1.addWidget(self.__harmfulmetadata_table, gridrow, 1, 10, 10)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__harmfulmetadata_button)
        hbox1.addWidget(self.__harmfulprepare_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)
        #
        return widget

    def __dyntaxaFromBrowse(self):
        """ """
        # Show directory dialog box.
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setFileMode(QtGui.QFileDialog.Directory)
        dirdialog.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        dirdialog.setDirectory(unicode(self.__dyntaxafromdirectory_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        # Check if user pressed ok or cancel.
        if dirpath:
            self.__dyntaxafromdirectory_edit.setText(dirpath)
#        """ """
#        dirdialog = QtGui.QFileDialog(self)
#        dirdialog.setDirectory(unicode(self.__dyntaxafromdirectory_edit.text()))
#        filepath = dirdialog.getOpenFileName()
#        if filepath:
#            self.__dyntaxafromdirectory_edit.setText(filepath)

    def __dyntaxaToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__dyntaxatofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__dyntaxatofile_edit.setText(filepath)

    def __pegFromBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegfromfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegfromfile_edit.setText(filepath)

# self.connect(self.__pwtopegfile_button, QtCore.SIGNAL("clicked()"), self.__pwToPegFileBrowse)
    def __pwToPegFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pwtopegfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pwtopegfile_edit.setText(filepath)

# self.connect(self.__pegtodyntaxafile_button, QtCore.SIGNAL("clicked()"), self.__pegToDyntaxaFileBrowse)
    def __pegToDyntaxaFileBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegtodyntaxafile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegtodyntaxafile_edit.setText(filepath)

    def __pegToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegtofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegtofile_edit.setText(filepath)

    def __editDyntaxaMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def __prepareDyntaxa(self):
        """ """
        utils.Logger().log("Prepare dyntaxa. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Prepare dyntaxa.")
        try:
            if self.__dyntaxasource_list.currentIndex() == 3:
                dt = taxa.Dyntaxa()
                importer = taxa_prepare.PrepareDyntaxaDbTablesAsTextFiles(taxaObject = dt)
                importer.importTaxa(unicode(self.__dyntaxafromdirectory_edit.text()))
                utils.Logger().log('Number of dyntaxa taxa: ' + str(len(dt.getTaxonList())))
                exporter = taxa_sources.JsonFile(taxaObject = dt)                
                exporter.exportTaxa(file = unicode(self.__dyntaxatofile_edit.text()))
            else:
                raise UserWarning('The selected data source type is not implemented.')
        except UserWarning, e:
            utils.Logger().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            utils.Logger().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            utils.Logger().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            utils.Logger().logAllWarnings()    
            utils.Logger().logAllErrors()    
            utils.Logger().info("Prepare dyntaxa. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourceDyntaxa()

    def __editPegMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def __preparePeg(self):
        """ """
        utils.Logger().log("Prepare PEG. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Prepare PEG.")
        try:
            peg = taxa.Peg()
            importer = taxa_prepare.PreparePegTextFile(taxaObject = peg)
            importer.importTaxa(file = unicode(self.__pegfromfile_edit.text()))
            # New:
            
            
            
############################            importer.addPwToPeg(file = unicode(self.__pwtopegfile_edit.text()))
            
            
            
            
            importer.addDyntaxaToPeg(file = unicode(self.__pegtodyntaxafile_edit.text()))
            #
            utils.Logger().log('Number of PEG taxa: ' + str(len(peg.getTaxonList())))                
            exporter = taxa_sources.JsonFile(taxaObject = peg)
            exporter.exportTaxa(file = unicode(self.__pegtofile_edit.text()))
        except UserWarning, e:
            utils.Logger().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            utils.Logger().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            utils.Logger().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            utils.Logger().logAllWarnings()    
            utils.Logger().logAllErrors()    
            utils.Logger().log("Prepare PEG. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourcePeg()

    def __harmfulFromBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__harmfulfromfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__harmfulfromfile_edit.setText(filepath)

    def __harmfulToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__harmfultofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__harmfultofile_edit.setText(filepath)

    def __editHarmfulMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def __prepareHarmful(self):
        """ """
        utils.Logger().log("Prepare Harmful plankton. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Prepare Harmful plankton.")
        try:
            harmful = taxa.HarmfulPlankton()
            importer = taxa_prepare.PrepareHarmfulMicroAlgae(taxaObject = harmful)
            importer.importTaxa(file = unicode(self.__harmfulfromfile_edit.text()))
            #
            utils.Logger().log('Number of Harmful plankton taxa: ' + str(len(harmful.getTaxonList())))                
            exporter = taxa_sources.JsonFile(taxaObject = harmful)
            exporter.exportTaxa(file = unicode(self.__harmfultofile_edit.text()))
        except UserWarning, e:
            utils.Logger().error("UserWarning: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Warning", unicode(e))
        except (IOError, OSError), e:
            utils.Logger().error("Error: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Error", unicode(e))
        except Exception, e:
            utils.Logger().error("Failed on exception: " + unicode(e))
            QtGui.QMessageBox.warning(self, "Exception", unicode(e))
            raise
        finally:
            utils.Logger().logAllWarnings()    
            utils.Logger().logAllErrors()    
            utils.Logger().log("Prepare Harmful plankton. Ended.")
            self._writeToStatusBar("")
        # Reload resources.
        toolbox_resources.ToolboxResources().loadResourceHarmfulPlankton()

