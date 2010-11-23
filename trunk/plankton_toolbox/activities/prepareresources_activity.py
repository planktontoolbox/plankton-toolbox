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
import plankton_toolbox.activities.activity_base as activity_base

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
        self.__dyntaxasource_list.addItems(["<select source type>",
                                            "Dyntaxa, SOAP",
                                            "Dyntaxa, REST",
                                            "Dyntaxa, DB-tables as text files"])
        self.__dyntaxafromdirectory_edit = QtGui.QLineEdit("../../data/dyntaxa")
        self.__dyntaxatofile_edit = QtGui.QLineEdit("../data/resources/dyntaxa_2009.json")        
        self.__dyntaxametadata_table = QtGui.QTableWidget()
        self.__dyntaxametadata_button = QtGui.QPushButton("Copy metadata from...")
        self.__dyntaxaprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.__dyntaxametadata_button, QtCore.SIGNAL("clicked()"), self.__copyDyntaxaMetadata)                
        self.connect(self.__dyntaxaprepare_button, QtCore.SIGNAL("clicked()"), self.__prepareDyntaxa)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Source:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__dyntaxasource_list, 0, 1, 1, 1);
        label2 = QtGui.QLabel("From directory:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__dyntaxafromdirectory_edit, 1, 1, 1, 10)
        label3 = QtGui.QLabel("To file:")
        form1.addWidget(label3, 2, 0, 1, 1)
        form1.addWidget(self.__dyntaxatofile_edit, 2, 1, 1, 10)
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
        self.__pegfromfile_edit = QtGui.QLineEdit("../../data/peg.txt")
        self.__pegtofile_edit = QtGui.QLineEdit("../data/resources/peg_2010.json")
        self.__pegmetadata_table = QtGui.QTableWidget()
        self.__pegmetadata_button = QtGui.QPushButton("Copy metadata from...")
        self.__pegprepare_button = QtGui.QPushButton("Create resource")
        self.connect(self.__pegmetadata_button, QtCore.SIGNAL("clicked()"), self.__copyPegMetadata)                
        self.connect(self.__pegprepare_button, QtCore.SIGNAL("clicked()"), self.__preparePeg)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("From file:")
        form1.addWidget(label1, 0, 0, 1, 1)
        form1.addWidget(self.__pegfromfile_edit, 0, 1, 1, 10);
        label2 = QtGui.QLabel("To file:")
        form1.addWidget(label2, 1, 0, 1, 1)
        form1.addWidget(self.__pegtofile_edit, 1, 1, 1, 10)
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
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)

    def __copyDyntaxaMetadata(self):
        """ """
#        self._writeToLog("Name: " + self.__nameedit.text())

    def __prepareDyntaxa(self):
        """ """
        dt = taxa.Dyntaxa()
        importer = taxa_prepare.DyntaxaDbTablesAsTextFiles(taxaObject = dt)
        importer.importTaxa('../data/')
        print('Number of Dyntaxa taxon:' + str(len(dt.getTaxonList())))
        exporter = taxa_sources.JsonFile(taxaObject = dt)
        exporter.exportTaxa(file = '../data/dyntaxa.json', encoding = 'iso-8859-1')
        
    def __prepare_smhi_extented_peg(self):
        """ """
#        smhi_phytowin_to_peg = taxon.SmhiPhytowin()
#        importer = taxa_sources.SmhiPhytowinToPegAsTextFiles(taxaObject = smhi_phytowin_to_peg)
##        importer.importTaxa('mellifica/data/')
#        importer.importTaxa('../data/smhi_phytowin_to_peg.txt')
#        
#        pp = pprint.PrettyPrinter()
#
#        print('Number of:' + str(len(smhi_phytowin_to_peg.getTaxonList())))
#        print('Number of:' + str(len(smhi_phytowin_to_peg.getIdToTaxonMap())))
#
##        pp.pprint(smhi_phytowin_to_peg)
#        pp.pprint(smhi_phytowin_to_peg.getIdToTaxonMap())
#        
#        exporter = taxa_sources.JsonFile(taxaObject = smhi_phytowin_to_peg)
#        exporter.exportTaxa(file = 'SmhiPhytowinToPeg.json', encoding = 'iso-8859-1')
#
#        print(json.dumps(smhi_phytowin_to_peg.getIdToTaxonMap(),  encoding = 'iso-8859-1', sort_keys=True, indent=1))
#        self._writeToLog("Name: " + self.__nameedit.text())

    def __copyPegMetadata(self):
        """ """
#        self._writeToLog("Name: " + self.__nameedit.text())

    def __preparePeg(self):
        """ """
        """ """
        peg = taxa.Peg()
        importer = taxa_prepare.PegTextFile(taxaObject = peg)
        importer.importTaxa(file = '../data/species_peg_bvol.txt')
        print('Number of PEG taxon: ' + str(len(peg.getTaxonList())))                
        exporter = taxa_sources.JsonFile(taxaObject = peg)
        exporter.exportTaxa(file = '../data/peg.json', encoding = 'iso-8859-1')
        # Test: reload json file:
###        peg2 = taxon.Peg()
###        importer = taxa_sources.JsonFile(taxaObject = peg2)
###        importer.importTaxa(file = '../data/peg.json')
###        print('Number of PEG taxon: ' + str(len(peg2.getTaxonList())))
        # Test: pretty printer:
###        pp = pprint.PrettyPrinter()
###        pp.pprint(peg2.getTaxonList())
        # Test: json.dumps:
###        print(json.dumps(peg2.getTaxonList(), encoding = 'iso-8859-1', sort_keys=True, indent=1))
#        self._writeToLog("Name: " + self.__nameedit.text())


