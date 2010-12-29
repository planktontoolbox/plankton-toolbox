#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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
import plankton_toolbox.utils as utils
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources
import plankton_toolbox.core.biology.taxa_prepare as taxa_prepare

class PrepareResourcesActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(PrepareResourcesActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        # === GroupBox: dyntaxabox === 
        dyntaxabox = QtGui.QGroupBox("Dynamic taxa", self)
        # Active widgets and connections.
        self.__dyntaxasource_list = QtGui.QComboBox()
        self.__dyntaxasource_list.addItems(["<select>",
                                            "Dyntaxa, SOAP",
                                            "Dyntaxa, REST",
                                            "Dyntaxa, DB-tables as text files"])
        self.__dyntaxafromdirectory_edit = QtGui.QLineEdit("")
        self.___dyntaxafrom_button = QtGui.QPushButton("Browse...")
        self.__dyntaxatofile_edit = QtGui.QLineEdit("planktondata/resources/smhi_dv_dyntaxa.json")        
        self.__dyntaxato_button = QtGui.QPushButton("Browse...")
        self.__dyntaxametadata_table = QtGui.QTableWidget()
        self.__dyntaxametadata_button = QtGui.QPushButton("Edit metadata...")
        self.__dyntaxaprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.___dyntaxafrom_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaFromBrowse)               
        self.connect(self.__dyntaxato_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaToBrowse)               
        self.connect(self.__dyntaxametadata_button, QtCore.SIGNAL("clicked()"), self.__copyDyntaxaMetadata)                
        self.connect(self.__dyntaxaprepare_button, QtCore.SIGNAL("clicked()"), self.__prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Source type:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__dyntaxasource_list, 0, 1, 1, 1);
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__dyntaxafromdirectory_edit, 1, 1, 1, 9)
        form1.addWidget(self.___dyntaxafrom_button, 1, 10, 1, 1)
        label3 = QtGui.QLabel("To file:")
        form1.addWidget(label3, 2, 0, 1, 1)
        form1.addWidget(self.__dyntaxatofile_edit, 2, 1, 1, 9)
        form1.addWidget(self.__dyntaxato_button, 2, 10, 1, 1)
        label4 = QtGui.QLabel("Metadata:")
        form1.addWidget(label4, 3, 0, 1, 1)
        form1.addWidget(self.__dyntaxametadata_table, 3, 1, 10, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__dyntaxametadata_button)
        hbox1.addWidget(self.__dyntaxaprepare_button)
        dyntaxalayout = QtGui.QVBoxLayout()
        dyntaxalayout.addLayout(form1)
        dyntaxalayout.addLayout(hbox1)
        dyntaxabox.setLayout(dyntaxalayout)

        # === GroupBox: pegbox === 
        pegbox = QtGui.QGroupBox("PEG, Plankton Expert Group", self)
        # Active widgets and connections.
        self.__pegfromfile_edit = QtGui.QLineEdit("")
        self.__pegfrom_button = QtGui.QPushButton("Browse...")
        self.__pegtofile_edit = QtGui.QLineEdit("planktondata/resources/smhi_extended_peg.json")
        self.__pegto_button = QtGui.QPushButton("Browse...")
        self.__pegmetadata_table = QtGui.QTableWidget()
        self.__pegmetadata_button = QtGui.QPushButton("Edit metadata from...")
        self.__pegprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.__pegfrom_button, QtCore.SIGNAL("clicked()"), self.__pegFromBrowse)              
        self.connect(self.__pegto_button, QtCore.SIGNAL("clicked()"), self.__pegToBrowse)          
        self.connect(self.__pegmetadata_button, QtCore.SIGNAL("clicked()"), self.__copyPegMetadata)                
        self.connect(self.__pegprepare_button, QtCore.SIGNAL("clicked()"), self.__preparePeg)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__pegfromfile_edit, 0, 1, 1, 9);
        form1.addWidget(self.__pegfrom_button, 0, 10, 1, 1);
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__pegtofile_edit, 1, 1, 1, 9)
        form1.addWidget(self.__pegto_button, 1, 10, 1, 1)
        label3 = QtGui.QLabel("Metadata:")
        form1.addWidget(label3, 2, 0, 1, 1)
        form1.addWidget(self.__pegmetadata_table, 2, 1, 10, 10)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.__pegmetadata_button)
        hbox1.addWidget(self.__pegprepare_button)
        peglayout = QtGui.QVBoxLayout()
        peglayout.addLayout(form1)
        peglayout.addLayout(hbox1)
        pegbox.setLayout(peglayout)
         
        # === Main level layout. ===
        content = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addWidget(dyntaxabox)
        contentLayout.addWidget(pegbox)
        contentLayout.addStretch(5)
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
#        mainscroll.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding)) # TEST
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)

#self.connect(self.___dyntaxafrom_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaFromBrowse) ###                
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

#self.connect(self.__dyntaxato_button, QtCore.SIGNAL("clicked()"), self.__dyntaxaToBrowse) ###                
    def __dyntaxaToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__dyntaxatofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__dyntaxatofile_edit.setText(filepath)

#self.connect(self.___pegfrom_button, QtCore.SIGNAL("clicked()"), self.__pegFromBrowse) ###                
    def __pegFromBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegfromfile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegfromfile_edit.setText(filepath)

#self.connect(self.__pegto_button, QtCore.SIGNAL("clicked()"), self.__pegToBrowse) ###                
    def __pegToBrowse(self):
        """ """
        dirdialog = QtGui.QFileDialog(self)
        dirdialog.setDirectory(unicode(self.__pegtofile_edit.text()))
        filepath = dirdialog.getOpenFileName()
        if filepath:
            self.__pegtofile_edit.setText(filepath)

    def __copyDyntaxaMetadata(self):
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

    def __copyPegMetadata(self):
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

