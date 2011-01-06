#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
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
        layout = QtGui.QVBoxLayout()
        content.setLayout(layout)
        # Tab widget. 
        widget = QtGui.QTabWidget()
        layout.addWidget(widget)
        widget.addTab(self._createContentDyntaxa(), "Dyntaxa")
        widget.addTab(self._createContentPeg(), "PEG")
        
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
        self.__dyntaxametadata_button = QtGui.QPushButton("Edit metadata...")
        self.__dyntaxaprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.__dyntaxafrom_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaFromBrowse)               
        self.connect(self.__dyntaxato_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaToBrowse)               
        self.connect(self.__dyntaxametadata_button, QtCore.SIGNAL("clicked()"), self.__editDyntaxaMetadata)                
        self.connect(self.__dyntaxaprepare_button, QtCore.SIGNAL("clicked()"), self.__prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        row = 0
        label1 = QtGui.QLabel("Source type:")
        form1.addWidget(label1, row, 0, 1, 1)
        form1.addWidget(self.__dyntaxasource_list, row, 1, 1, 1)
        row += 1
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, row, 0, 1, 1)
        form1.addWidget(self.__dyntaxafromdirectory_edit, row, 1, 1, 9)
        form1.addWidget(self.__dyntaxafrom_button, row, 10, 1, 1)
        row += 1
        label3 = QtGui.QLabel("To file:")
        form1.addWidget(label3, row, 0, 1, 1)
        form1.addWidget(self.__dyntaxatofile_edit, row, 1, 1, 9)
        form1.addWidget(self.__dyntaxato_button, row, 10, 1, 1)
        row += 1
        label4 = QtGui.QLabel("Metadata:")
        form1.addWidget(label4, row, 0, 1, 1)
        form1.addWidget(self.__dyntaxametadata_table, row, 1, 10, 10)
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
        self.__pegfromfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_extended_peg_version_2010-10-26.txt")
###        self.__pegfromfile_edit = QtGui.QLineEdit("")
        self.__pegfrom_button = QtGui.QPushButton("Browse...")
        # Get filepath from toolbox settings.
        filepath = toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath')
        self.__pegtofile_edit = QtGui.QLineEdit(filepath)
        self.__pegto_button = QtGui.QPushButton("Browse...")        
        self.__pwtopegfile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_pw_to_extended_peg.txt")
###        self.__pwtopegfile_edit = QtGui.QLineEdit("")
        self.__pwtopegfile_button = QtGui.QPushButton("Browse...")
        self.__pegtodyntaxafile_edit = QtGui.QLineEdit("../../../../data/planktondata/originalfiles/smhi_peg_to_dyntaxa.txt")
###        self.__pegtodyntaxafile_edit = QtGui.QLineEdit("")
        self.__pegtodyntaxafile_button = QtGui.QPushButton("Browse...")
        self.__pegmetadata_table = QtGui.QTableWidget()
        self.__pegmetadata_button = QtGui.QPushButton("Edit metadata...")
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
        row = 0
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, row, 0, 1, 1)
        form1.addWidget(self.__pegfromfile_edit, row, 1, 1, 9)
        form1.addWidget(self.__pegfrom_button, row, 10, 1, 1)
        row += 1
        label2 = QtGui.QLabel("Translate PW to PEG file:")
        form1.addWidget(label2, row, 0, 1, 1)
        form1.addWidget(self.__pwtopegfile_edit, row, 1, 1, 9)
        form1.addWidget(self.__pwtopegfile_button, row, 10, 1, 1)
        row += 1
        label2 = QtGui.QLabel("Translate PEG to Dyntaxa file:")
        form1.addWidget(label2, row, 0, 1, 1)
        form1.addWidget(self.__pegtodyntaxafile_edit, row, 1, 1, 9)
        form1.addWidget(self.__pegtodyntaxafile_button, row, 10, 1, 1)
        row += 1
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, row, 0, 1, 1)
        form1.addWidget(self.__pegtofile_edit, row, 1, 1, 9)
        form1.addWidget(self.__pegto_button, row, 10, 1, 1)
        row += 1
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, row, 0, 1, 1)
        form1.addWidget(self.__pegmetadata_table, row, 1, 10, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__pegmetadata_button)
        hbox1.addWidget(self.__pegprepare_button)
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
        utils.Logger().info("Prepare dyntaxa. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Prepare dyntaxa.")
        try:
            if self.__dyntaxasource_list.currentIndex() == 3:
                dt = taxa.Dyntaxa()
                importer = taxa_prepare.PrepareDyntaxaDbTablesAsTextFiles(taxaObject = dt)
                importer.importTaxa(unicode(self.__dyntaxafromdirectory_edit.text()))
                utils.Logger().info('Number of dyntaxa taxa: ' + str(len(dt.getTaxonList())))
                exporter = taxa_sources.JsonFile(taxaObject = dt)
                exporter.exportTaxa(file = unicode(self.__dyntaxatofile_edit.text()), encoding = 'iso-8859-1')
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

    def __editPegMetadata(self):
        """ """
        QtGui.QMessageBox.information(self, 'Metadata', 'Not implemented.')

    def __preparePeg(self):
        """ """
        utils.Logger().info("Prepare PEG. Started.")
        utils.Logger().clear()
        self._writeToStatusBar("Prepare PEG.")
        try:
            peg = taxa.Peg()
            importer = taxa_prepare.PreparePegTextFile(taxaObject = peg)
            importer.importTaxa(file = unicode(self.__pegfromfile_edit.text()))
            # New:
            importer.addPwToPeg(file = unicode(self.__pwtopegfile_edit.text()))
            importer.addDyntaxaToPeg(file = unicode(self.__pegtodyntaxafile_edit.text()))
            #
            utils.Logger().info('Number of PEG taxa: ' + str(len(peg.getTaxonList())))                
            exporter = taxa_sources.JsonFile(taxaObject = peg)
            exporter.exportTaxa(file = unicode(self.__pegtofile_edit.text()), encoding = 'iso-8859-1')
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
            utils.Logger().info("Prepare PEG. Ended.")
            self._writeToStatusBar("")
