#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Mellifica toolbox. http://toolbox.mellifica.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 Arnold Andreasson
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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import webbrowser
import plankton_toolbox.toolbox.utils as utils
import plankton_toolbox.tools.tool_base as tool_base
from plankton_toolbox.core.map_projections.swedish_geoposition_converter import SwedishGeoPositionConverter
import plankton_toolbox.core.map_projections.latlong_dd_dm_dms as latlong

class LatLongTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentWidget):
        """ """
        # User input data.
        self.__lat_dd = None
        self.__lat_dm = None
        self.__lat_dms = None
        self.__long_dd = None
        self.__long_dm = None
        self.__long_dms = None
        self.__proj_rt90 = None
        self.__x_rt90 = None
        self.__y_rt90 = None
        self.__proj_sweref99 = None
        self.__n_sweref99 = None
        self.__e_sweref99 = None
        self.__latitude = None # Decimal degrees. Type=float.
        self.__longitude = None # Decimal degrees. Type=float.
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(LatLongTool, self).__init__(name, parentWidget)
 
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget for single point or table. 
        tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(tabWidget)
        tabWidget.addTab(self.__createContentSinglePoint(), "Single point")
        tabWidget.addTab(self.__createContentMultiplePoints(), "Multiple points")

    def __createContentSinglePoint(self):
        """ """
        singleWidget = QtGui.QWidget()
        # === Active widgets and connections. ===
        # Decimal degree.
        self.__latDd = QtGui.QLineEdit("")
        self.__longDd = QtGui.QLineEdit("")
#        self.connect(self.__latDd, QtCore.SIGNAL("textChanged(QString)"), self.__latDd_calculate)
#        self.connect(self.__longDd, QtCore.SIGNAL("textChanged(QString)"), self.__longDd_calculate)
        self.connect(self.__latDd, QtCore.SIGNAL("textEdited(QString)"), self.__latDd_calculate)
        self.connect(self.__longDd, QtCore.SIGNAL("textEdited(QString)"), self.__longDd_calculate)
        self.connect(self.__latDd, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDd, QtCore.SIGNAL("editingFinished()"), self.__update_long)
        # Degree, minutes.
        self.__latDm = QtGui.QLineEdit("")
        self.__longDm = QtGui.QLineEdit("")
#        self.connect(self.__latDm, QtCore.SIGNAL("textChanged(QString)"), self.__latDm_calculate)
#        self.connect(self.__longDm, QtCore.SIGNAL("textChanged(QString)"), self.__longDm_calculate)
        self.connect(self.__latDm, QtCore.SIGNAL("textEdited(QString)"), self.__latDm_calculate)
        self.connect(self.__longDm, QtCore.SIGNAL("textEdited(QString)"), self.__longDm_calculate)
        self.connect(self.__latDm, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDm, QtCore.SIGNAL("editingFinished()"), self.__update_long)
        # Degree, minutes, seconds.
        self.__latDms = QtGui.QLineEdit("")
        self.__longDms = QtGui.QLineEdit("")
#        self.connect(self.__latDms, QtCore.SIGNAL("textChanged(QString)"), self.__latDms_calculate)
#        self.connect(self.__longDms, QtCore.SIGNAL("textChanged(QString)"), self.__longDms_calculate)
        self.connect(self.__latDms, QtCore.SIGNAL("textEdited(QString)"), self.__latDms_calculate)
        self.connect(self.__longDms, QtCore.SIGNAL("textEdited(QString)"), self.__longDms_calculate)
        self.connect(self.__latDms, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDms, QtCore.SIGNAL("editingFinished()"), self.__update_long)
        # RT 90.
        self.__rt90Proj = QtGui.QComboBox()
        self.__rt90Proj.addItems(["rt90_7.5_gon_v",
                                "rt90_5.0_gon_v",
                                "rt90_2.5_gon_v",
                                "rt90_0.0_gon_v",
                                "rt90_2.5_gon_o",
                                "rt90_5.0_gon_o"])
        self.__rt90Proj.setCurrentIndex(2) # Default rt90_2.5_gon_v
        self.connect(self.__rt90Proj, QtCore.SIGNAL("currentIndexChanged(int)"), self.__update_rt90)
        self.__rt90X = QtGui.QLineEdit("")
        self.__rt90Y = QtGui.QLineEdit("")
#        self.connect(self.__rt90X, QtCore.SIGNAL("textChanged(QString)"), self.__rt90X_calculate)
#        self.connect(self.__rt90Y, QtCore.SIGNAL("textChanged(QString)"), self.__rt90Y_calculate)
        self.connect(self.__rt90X, QtCore.SIGNAL("textEdited(QString)"), self.__rt90_calculate)
        self.connect(self.__rt90Y, QtCore.SIGNAL("textEdited(QString)"), self.__rt90_calculate)
#        self.connect(self.__rt90X, QtCore.SIGNAL("editingFinished()"), self.__update_rt90)
#        self.connect(self.__rt90Y, QtCore.SIGNAL("editingFinished()"), self.__update_rt90)
        # SWEREF 99 TM/deg-min.
        self.__sweref99Proj = QtGui.QComboBox()
        self.__sweref99Proj.addItems(["sweref_99_tm",
                                    "sweref_99_1200",
                                    "sweref_99_1330",
                                    "sweref_99_1500",
                                    "sweref_99_1630",
                                    "sweref_99_1800",
                                    "sweref_99_1415",
                                    "sweref_99_1545",
                                    "sweref_99_1715",
                                    "sweref_99_1845",
                                    "sweref_99_2015",
                                    "sweref_99_2145",
                                    "sweref_99_2315"])
        self.connect(self.__sweref99Proj, QtCore.SIGNAL("currentIndexChanged(int)"), self.__update_sweref99)
        self.__sweref99N = QtGui.QLineEdit("")
        self.__sweref99E = QtGui.QLineEdit("")
#        self.connect(self.__sweref99N, QtCore.SIGNAL("textChanged(QString)"), self.__sweref99N_calculate)
#        self.connect(self.__sweref99E, QtCore.SIGNAL("textChanged(QString)"), self.__sweref99E_calculate)
        self.connect(self.__sweref99N, QtCore.SIGNAL("textEdited(QString)"), self.__sweref99_calculate)
        self.connect(self.__sweref99E, QtCore.SIGNAL("textEdited(QString)"), self.__sweref99_calculate)
#        self.connect(self.__sweref99N, QtCore.SIGNAL("editingFinished()"), self.__update_sweref99)
#        self.connect(self.__sweref99E, QtCore.SIGNAL("editingFinished()"), self.__update_sweref99)
        # Open in web browser: Google maps.
        self.__opengooglemaps = QtGui.QPushButton("Open maps.google.com")
        self.connect(self.__opengooglemaps, QtCore.SIGNAL("clicked()"), self.__open_googlemaps)                
        # Open in web browser: latlong.mellifica.se.
        self.__openlatlongmellifica = QtGui.QPushButton("Open latlong.mellifica.se")
        self.connect(self.__openlatlongmellifica, QtCore.SIGNAL("clicked()"), self.__open_latlongmellifica)                
        # === Layout. ===
        # Single position tab.
        singleLayout = QtGui.QGridLayout()
        singleWidget.setLayout(singleLayout)
        # Single, lat/long.        
        latLongGroup = QtGui.QGroupBox("SWEREF 99 (~WGS 84)")
        singleLayout.addWidget(latLongGroup, 0, 0)
        latLongLayout =  QtGui.QGridLayout()
        latLongGroup.setLayout(latLongLayout)
        gridrow = 0
        latitudLabel = QtGui.QLabel("Latitud")
        longitudLabel = QtGui.QLabel("Longitud")
        latLongLayout.addWidget(latitudLabel, gridrow, 1, 1, 1, QtCore.Qt.AlignHCenter)
        latLongLayout.addWidget(longitudLabel, gridrow, 2, 1, 1, QtCore.Qt.AlignHCenter)
        gridrow += 1
        latDdLabel = QtGui.QLabel("Degree:")
        latLongLayout.addWidget(latDdLabel, gridrow, 0)
        latLongLayout.addWidget(self.__latDd, gridrow, 1)
        latLongLayout.addWidget(self.__longDd, gridrow, 2)
        gridrow += 1
        latDmLabel = QtGui.QLabel("Deg/min:")
        latLongLayout.addWidget(latDmLabel, gridrow, 0)
        latLongLayout.addWidget(self.__latDm, gridrow, 1)
        latLongLayout.addWidget(self.__longDm, gridrow, 2)
        gridrow += 1
        latDmsLabel = QtGui.QLabel("Deg/min/sec:")
        latLongLayout.addWidget(latDmsLabel, gridrow, 0)
        latLongLayout.addWidget(self.__latDms, gridrow, 1)
        latLongLayout.addWidget(self.__longDms, gridrow, 2)                
        # Single, rt90.        
        rt90Group = QtGui.QGroupBox("RT 90")
        singleLayout.addWidget(rt90Group, 1, 0)
        rt90Layout =  QtGui.QGridLayout()
        rt90Group.setLayout(rt90Layout)
#        gridrow = 0
        rt90ProjWidget = QtGui.QWidget()
        rt90ProjLayout = QtGui.QHBoxLayout()
        rt90ProjWidget.setLayout(rt90ProjLayout)
        rt90ProjLabel = QtGui.QLabel("Map projection:")
        rt90ProjLayout.addStretch(5)
        rt90ProjLayout.addWidget(rt90ProjLabel)
        rt90ProjLayout.addWidget(self.__rt90Proj)
        rt90ProjLayout.addStretch(5)
        gridrow = 0
        rt90XLabel = QtGui.QLabel("X:")
        rt90YLabel = QtGui.QLabel("Y:")
        rt90Layout.addWidget(rt90ProjWidget, gridrow, 0, 1, 4)
        rt90Layout.addWidget(rt90XLabel, gridrow, 0)
        gridrow += 1
        rt90Layout.addWidget(self.__rt90X, gridrow, 1)
        
        rt90Layout.addWidget(rt90YLabel, gridrow, 2)
        rt90Layout.addWidget(self.__rt90Y, 1, 3)        
        # Single, sweref 99 dd mm.        
        sweref99Group = QtGui.QGroupBox("SWEREF 99 TM, SWEREF 99 dd mm")
        singleLayout.addWidget(sweref99Group, 2, 0)
        sweref99Layout = QtGui.QGridLayout()
        sweref99Group.setLayout(sweref99Layout)
#        gridrow = 0
        sweref99ProjWidget = QtGui.QWidget()
        sweref99ProjLayout = QtGui.QHBoxLayout()
        sweref99ProjWidget.setLayout(sweref99ProjLayout)
        sweref99ProjLabel = QtGui.QLabel("Map projection:")
        sweref99ProjLayout.addStretch(5)
        sweref99ProjLayout.addWidget(sweref99ProjLabel)
        sweref99ProjLayout.addWidget(self.__sweref99Proj)
        sweref99ProjLayout.addStretch(5)
        gridrow = 0
        sweref99NLabel = QtGui.QLabel("N:")
        sweref99ELabel = QtGui.QLabel("E:")
        sweref99Layout.addWidget(sweref99ProjWidget, 0, 0, 1, 4)
        gridrow += 1
        sweref99Layout.addWidget(sweref99NLabel, 1, 0)
        sweref99Layout.addWidget(self.__sweref99N, 1, 1)
        sweref99Layout.addWidget(sweref99ELabel, 1, 2)
        sweref99Layout.addWidget(self.__sweref99E, 1, 3)
        gridrow += 1
        hbox = QtGui.QHBoxLayout()
        singleLayout.addLayout(hbox, 3, 0)
        hbox.addWidget(self.__opengooglemaps)
        hbox.addWidget(self.__openlatlongmellifica)
        gridrow += 1
        singleLayout.setRowStretch(4, 5)
        
        return singleWidget
        
    def __createContentMultiplePoints(self):
        """ """
        multipleWidget = QtGui.QWidget()
        # === Active widgets and connections. ===
        # Table position tab. Active widgets.
        self.__fromFormatComboBox = QtGui.QComboBox()
        self.__fromFormatComboBox.addItems(["latlong_dd",
                                            "latlong_dm",
                                            "latlong_dms",
                                            "rt90_7.5_gon_v",
                                            "rt90_5.0_gon_v",
                                            "rt90_2.5_gon_v",
                                            "rt90_0.0_gon_v",
                                            "rt90_2.5_gon_o",
                                            "rt90_5.0_gon_o",
                                            "sweref_99_tm",
                                            "sweref_99_1200",
                                            "sweref_99_1330",
                                            "sweref_99_1500",
                                            "sweref_99_1630",
                                            "sweref_99_1800",
                                            "sweref_99_1415",
                                            "sweref_99_1545",
                                            "sweref_99_1715",
                                            "sweref_99_1845",
                                            "sweref_99_2015",
                                            "sweref_99_2145",
                                            "sweref_99_2315"])
        self.__fromFormatComboBox.setCurrentIndex(0) # Default: latlong_dd
        self.connect(self.__fromFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.__calculateTable)
        self.__pasteFromClipboardButton = QtGui.QPushButton("Paste from clipboard")
        self.connect(self.__pasteFromClipboardButton, QtCore.SIGNAL("clicked()"), self.__pasteFromClipboard)
        self.__fromTable = QtGui.QTableWidget()
        self.__fromTable.setColumnCount(2)
#        self.__fromTable.setHorizontalHeaderLabels(["Latitude", "Longitude"])
#        self.__fromTable.setRowCount(20)
        self.__fromTable.setAlternatingRowColors(True)
        self.__fromTable.verticalHeader().setDefaultSectionSize(18)
        self.__fromTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self.__fromTable.horizontalHeader().setStretchLastSection(True)
        # User for manually entered data.
        self.connect(self.__fromTable, QtCore.SIGNAL("cellChanged(int, int)"), self.__calculateTable)
        #
        self.__toFormatComboBox = QtGui.QComboBox()
        self.__toFormatComboBox.addItems([  "latlong_dd",
                                            "latlong_dm",
                                            "latlong_dms",
                                            "rt90_7.5_gon_v",
                                            "rt90_5.0_gon_v",
                                            "rt90_2.5_gon_v",
                                            "rt90_0.0_gon_v",
                                            "rt90_2.5_gon_o",
                                            "rt90_5.0_gon_o",
                                            "sweref_99_tm",
                                            "sweref_99_1200",
                                            "sweref_99_1330",
                                            "sweref_99_1500",
                                            "sweref_99_1630",
                                            "sweref_99_1800",
                                            "sweref_99_1415",
                                            "sweref_99_1545",
                                            "sweref_99_1715",
                                            "sweref_99_1845",
                                            "sweref_99_2015",
                                            "sweref_99_2145",
                                            "sweref_99_2315"])
        self.__toFormatComboBox.setCurrentIndex(9) # Default: sweref_99_tm
        self.connect(self.__toFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.__calculateTable)
        self.__copyToClipboardButton = QtGui.QPushButton("Copy to clipboard")
        self.connect(self.__copyToClipboardButton, QtCore.SIGNAL("clicked()"), self.__copyToClipboard)
        self.__toTable = QtGui.QTableWidget()
        self.__toTable.setColumnCount(2)
#        self.__toTable.setHorizontalHeaderLabels(["N", "E"])
#        self.__toTable.setRowCount(20)
        self.__toTable.setAlternatingRowColors(True)
        self.__toTable.verticalHeader().setDefaultSectionSize(18)
        self.__toTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self.__toTable.horizontalHeader().setStretchLastSection(True)
        #
        self.__setColumnHeader()
        
        # === Layout. ===
        multipleLayout = QtGui.QHBoxLayout()
        multipleWidget.setLayout(multipleLayout)
        #
        multipleFromGroup = QtGui.QGroupBox("From position")
        multipleLayout.addWidget(multipleFromGroup)
        fromGrid =  QtGui.QGridLayout()
        multipleFromGroup.setLayout(fromGrid)
        gridrow = 0
        fromFormatLabel = QtGui.QLabel("<b>Format:</b>")
        fromGrid.addWidget(fromFormatLabel, gridrow, 0, 1, 1, QtCore.Qt.AlignLeft)
        fromGrid.addWidget(self.__fromFormatComboBox, gridrow, 1, 1, 8, QtCore.Qt.AlignLeft)
        gridrow += 1
        fromGrid.addWidget(self.__pasteFromClipboardButton, gridrow, 0, 1, 9)
        gridrow += 1
        fromGrid.addWidget(self.__fromTable, gridrow, 0, 1, 9)
        #
        multipleToGroup = QtGui.QGroupBox("To position")
        multipleLayout.addWidget(multipleToGroup)
        toGrid =  QtGui.QGridLayout()
        multipleToGroup.setLayout(toGrid)
        gridrow = 0
        toFormatLabel = QtGui.QLabel("<b>Format:</b>")
        toGrid.addWidget(toFormatLabel, gridrow, 0, 1, 1, QtCore.Qt.AlignLeft)
        toGrid.addWidget(self.__toFormatComboBox, gridrow, 1, 1, 8, QtCore.Qt.AlignLeft)
        gridrow += 1
        toGrid.addWidget(self.__copyToClipboardButton, gridrow, 0, 1, 9)
        gridrow += 1
        toGrid.addWidget(self.__toTable, gridrow, 0, 1, 9)
                
        return multipleWidget
    
# === Single methods. ===

    def set_latitude_longitude(self, lat, lon):
        """ 
        Set current position and update all fields. Used for external 
        program calls. 
        """
        self.__latitude = lat
        self.__longitude = lon
        self.__update_lat()
        self.__update_long()
        self.__update_rt90()
        self.__update_sweref99()

    def get_latitude_longitude(self):
        """ Get current position. Used for external program calls. """
        return (self.__latitude, self.__longitude)

    def __latDd_calculate(self, qstring):
        """ """
        self.__latitude = latlong.convert_lat_from_dd(str(qstring))
        self.__latDm.setText(latlong.convert_lat_to_dm(self.__latitude))
        self.__latDms.setText(latlong.convert_lat_to_dms(self.__latitude))
        self.__update_rt90()
        self.__update_sweref99()
        
    def __longDd_calculate(self, qstring):
        """ """
        self.__longitude = latlong.convert_long_from_dd(str(qstring))
        self.__longDm.setText(latlong.convert_long_to_dm(self.__longitude))
        self.__longDms.setText(latlong.convert_long_to_dms(self.__longitude))
        self.__update_rt90()
        self.__update_sweref99()
       
    def __latDm_calculate(self, qstring):
        """ """
        self.__latitude = latlong.convert_lat_from_dm(str(qstring))
        self.__latDd.setText(latlong.convert_lat_to_dd(self.__latitude))
        self.__latDms.setText(latlong.convert_lat_to_dms(self.__latitude))
        self.__update_rt90()
        self.__update_sweref99()
        
    def __longDm_calculate(self, qstring):
        """ """
        self.__longitude = latlong.convert_long_from_dm(str(qstring))
        self.__longDd.setText(latlong.convert_long_to_dd(self.__longitude))
        self.__longDms.setText(latlong.convert_long_to_dms(self.__longitude))
        self.__update_rt90()
        self.__update_sweref99()
        
    def __latDms_calculate(self, qstring):
        """ """
        self.__latitude = latlong.convert_lat_from_dms(str(qstring))
        self.__latDd.setText(latlong.convert_lat_to_dd(self.__latitude))
        self.__latDm.setText(latlong.convert_lat_to_dm(self.__latitude))
        self.__update_rt90()
        self.__update_sweref99()
        
    def __longDms_calculate(self, qstring):
        """ """
        self.__longitude = latlong.convert_long_from_dms(str(qstring))
        self.__longDd.setText(latlong.convert_long_to_dd(self.__longitude))
        self.__longDm.setText(latlong.convert_long_to_dm(self.__longitude))
        self.__update_rt90()
        self.__update_sweref99()
        
    def __rt90Proj_calculate(self, index):
        """ """
        
    def __rt90_calculate(self, qstring):
        """ """
        if ((unicode(self.__rt90X.text()) == "") or (unicode(self.__rt90Y.text()) == "")):
            self.__latitude = None
            self.__longitude = None
        else:
            x = float(unicode(self.__rt90X.text()).replace(",", "."))
            y = float(unicode(self.__rt90Y.text()).replace(",", "."))
            converter = SwedishGeoPositionConverter(self.__rt90Proj.currentText())
            self.__latitude, self.__longitude = converter.gridToGeodetic(x, y)
        self.__update_lat()
        self.__update_long()
        self.__update_sweref99()
        
    def __sweref99Proj_calculate(self, index):
        """ """
        
    def __sweref99_calculate(self, qstring):
        """ """
        if ((unicode(self.__sweref99N.text()) == "") or (unicode(self.__sweref99E.text()) == "")):
            self.__latitude = None
            self.__longitude = None
        else:
            n = float(unicode(self.__sweref99E.text()).replace(",", "."))
            e = float(unicode(self.__sweref99E.text()).replace(",", "."))
            converter = SwedishGeoPositionConverter(self.__sweref99Proj.currentText())
            self.__latitude, self.__longitude = converter.gridToGeodetic(n, e)
        self.__update_lat()
        self.__update_long()
        self.__update_rt90()
        
    def __update_lat(self):
        """ """
        self.__latDd.setText(latlong.convert_lat_to_dd(self.__latitude))
        self.__latDm.setText(latlong.convert_lat_to_dm(self.__latitude))
        self.__latDms.setText(latlong.convert_lat_to_dms(self.__latitude))

    def __update_long(self):
        """ """
        self.__longDd.setText(latlong.convert_long_to_dd(self.__longitude))
        self.__longDm.setText(latlong.convert_long_to_dm(self.__longitude))
        self.__longDms.setText(latlong.convert_long_to_dms(self.__longitude))

    def __update_rt90(self):
        """ """
        if ((self.__latitude != None) and (self.__longitude != None) and
            (self.__latitude >= -90.0) and (self.__latitude <= 90.0) and
            (self.__longitude >= -180.0) and (self.__longitude < 180.0)):
            converter = SwedishGeoPositionConverter(self.__rt90Proj.currentText())
            x, y = converter.geodeticToGrid(self.__latitude, self.__longitude)
            self.__rt90X.setText("%.3f" % x)
            self.__rt90Y.setText("%.3f" % y)
        else:
            self.__rt90X.setText("")
            self.__rt90Y.setText("")

    def __update_sweref99(self):
        """ """
        if ((self.__latitude != None) and (self.__longitude != None) and
            (self.__latitude >= -90.0) and (self.__latitude <= 90.0) and
            (self.__longitude >= -180.0) and (self.__longitude < 180.0)):
            converter = SwedishGeoPositionConverter(self.__sweref99Proj.currentText())
            n, e = converter.geodeticToGrid(self.__latitude, self.__longitude)
            self.__sweref99N.setText("%.3f" % n)
            self.__sweref99E.setText("%.3f" % e)
        else:
            self.__sweref99N.setText("")
            self.__sweref99E.setText("")

    def __execute_test_case(self):
        """
        Test-case:
        Lat: 66 0'0", long: 24 0'0".
        X:1135809.413803 Y:555304.016555.
        """
        print("Test case: X:1135809.413803 Y:555304.016555. Expected result: 66 0'0, 24 0'0.")
        test_converter = SwedishGeoPositionConverter("test_case")
        (lat, long) = test_converter.gridToGeodetic(1135809.413803, 555304.016555)
        print("Lat: X %.12f" % lat)
        print("Long: Y %.12f" % long)
        
        print("Test case: 66 0'0, 24 0'0. Expected result: X:1135809.413803 Y:555304.016555.")
        (x, y) = test_converter.geodeticToGrid(66.0, 24.0)
        print("X: %.12f" % x)
        print("Y: %.12f" % y)
                
        print("Test convert_long_to_dms(57.123): " + latlong.convert_long_to_dms(57.123))

    def __open_googlemaps(self):
        """ Launch web browser and use maps.google.com to display position. """
        if (len(unicode(self.__latDd.text())) == 0) or (len(unicode(self.__longDd.text())) == 0):
            utils.Logger().log("Failed to open maps.google.com. No values for lat/long.")
            return
        webbrowser.open("http://maps.google.com/maps/?ll=" + unicode(self.__latDd.text()) + "," + unicode(self.__longDd.text()))
        
    def __open_latlongmellifica(self):
        """ Launch web browser and use latlong.mellifica.se to display position. """
        if (len(unicode(self.__latDd.text())) == 0) or (len(unicode(self.__longDd.text())) == 0):
            utils.Logger().log("Failed to open latlong.mellifica.se. No values for lat/long.")
            return
        webbrowser.open("http://latlong.mellifica.se/?latlong=" + unicode(self.__latDd.text()) + "," + unicode(self.__longDd.text()))
        
# === Multiple methods. ===        

    def __pasteFromClipboard(self):
        """ """
        self.__fromTable.blockSignals(True)
        self.__fromTable.clearContents()
        self.__toTable.clearContents()
        clipboard = QtGui.QApplication.clipboard()
        if clipboard.mimeData().hasText():
            rows = unicode(clipboard.text()).split('\n') # Row separator in clip board.
            self.__fromTable.setRowCount(len(rows))
            self.__toTable.setRowCount(len(rows))
            for index, row in enumerate(rows):
                items = row.split("\t") # Column separator in clip board.
                if len(items) >= 1:
                    try:
                        float(items[0].strip().replace(",", ".")) # Check if valid format.
                        self.__fromTable.setItem(index, 0, QtGui.QTableWidgetItem(items[0]))
                    except ValueError:
                        self.__fromTable.setItem(index, 0, QtGui.QTableWidgetItem(''))
                if len(items) >= 2:
                    try:
                        float(items[1].strip().replace(",", ".")) # Check if valid format.
                        self.__fromTable.setItem(index, 1, QtGui.QTableWidgetItem(items[1]))
                    except ValueError:
                        self.__fromTable.setItem(index, 1, QtGui.QTableWidgetItem(''))
        self.__fromTable.resizeColumnsToContents()
        self.__fromTable.blockSignals(False)
          
        self.__calculateTable()

    def __copyToClipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        clipboardstring = ''
        for index in range(self.__toTable.rowCount()):
            # Read from table.
            item_1 = self.__toTable.item(index, 0)
            if item_1:
                to_1 = unicode(item_1.data(QtCore.Qt.DisplayRole).toString())
            else:
                to_1 = ''
            item_2 = self.__toTable.item(index, 1)
            if item_2:
                to_2 = unicode(item_2.data(QtCore.Qt.DisplayRole).toString())
            else:
                to_2 = ''
            clipboardstring += to_1 + '\t' + to_2 + '\n'
        clipboard.setText(clipboardstring)

    def __calculateTable(self):
        """ """
        fromFormat = unicode(self.__fromFormatComboBox.currentText())
        toFormat = unicode(self.__toFormatComboBox.currentText())
        #
        fromConverter = SwedishGeoPositionConverter(self.__fromFormatComboBox.currentText())
        toConverter = SwedishGeoPositionConverter(self.__toFormatComboBox.currentText())
        #
        self.__setColumnHeader()
        # 
        for index in range(self.__fromTable.rowCount()):
            # Read from table.
            item_1 = self.__fromTable.item(index, 0)
            item_2 = self.__fromTable.item(index, 1)
            if (not item_1) or (not item_2) :
                self.__toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self.__toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
                continue # Go to next row.
            from_1 = unicode(item_1.data(QtCore.Qt.DisplayRole).toString())
            from_2 = unicode(item_2.data(QtCore.Qt.DisplayRole).toString())
            #
            from_1 = from_1.strip().replace(",", ".")
            from_2 = from_2.strip().replace(",", ".")                
            if (from_1 == '') or (from_2 == '') :
                self.__toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self.__toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
                continue # Go to next row.
            # From.
            if fromFormat == 'latlong_dd':
                dd_1 = latlong.convert_lat_from_dd(from_1)
                dd_2 = latlong.convert_long_from_dd(from_2)
            elif fromFormat == 'latlong_dm':
                dd_1 = latlong.convert_lat_from_dm(from_1)
                dd_2 = latlong.convert_long_from_dm(from_2)
            elif fromFormat == 'latlong_dms':
                dd_1 = latlong.convert_lat_from_dms(from_1)
                dd_2 = latlong.convert_long_from_dms(from_2)
            else:
#                fromConverter = SwedishGeoPositionConverter(self.__fromFormatComboBox.currentText())
                dd_1, dd_2 = fromConverter.gridToGeodetic(float(from_1), float(from_2))
            #
            if (not dd_1) or (not dd_2) :
                self.__toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self.__toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
                continue # Go to next row.
            # To.
            if toFormat == 'latlong_dd':
                to_1, to_2 = dd_1, dd_2
            elif toFormat == 'latlong_dm':
                to_1 = latlong.convert_lat_to_dm(dd_1)
                to_2 = latlong.convert_long_to_dm(dd_2)
            elif toFormat == 'latlong_dms':
                to_1 = latlong.convert_lat_to_dms(dd_1)
                to_2 = latlong.convert_long_to_dms(dd_2)
            else:
#                toConverter = SwedishGeoPositionConverter(self.__toFormatComboBox.currentText())
                to_1, to_2 = toConverter.geodeticToGrid(dd_1, dd_2)
            #
            if toFormat == 'latlong_dd':
                to_1 = unicode(' %.6f' %(to_1)).replace(".", ",")
                to_2 = unicode(' %.6f' %(to_2)).replace(".", ",")
            elif toFormat in ['latlong_dm', 'latlong_dms']:
                to_1 = unicode(to_1).replace(".", ",")
                to_2 = unicode(to_2).replace(".", ",")
            else:
                to_1 = unicode(' %.3f' %(to_1)).replace(".", ",")
                to_2 = unicode(' %.3f' %(to_2)).replace(".", ",")
            self.__toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode(to_1)))
            self.__toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode(to_2)))            
        #
        self.__toTable.resizeColumnsToContents()

    def __setColumnHeader(self):
        """ Column names differ depending on selected projections. """
        fromFormat = self.__fromFormatComboBox.currentText()
        toFormat = self.__toFormatComboBox.currentText()
        # From columns.
        if fromFormat in (["latlong_dd"]):
            self.__fromTable.setHorizontalHeaderLabels(["Latitude DD", "Longitude DD"])
        if fromFormat in (["latlong_dm"]):
            self.__fromTable.setHorizontalHeaderLabels(["Latitude DM", "Longitude DM"])
        if fromFormat in (["latlong_dms"]):
            self.__fromTable.setHorizontalHeaderLabels(["Latitude DMS", "Longitude DMS"])
        if fromFormat in ([ "rt90_7.5_gon_v",
                            "rt90_5.0_gon_v",
                            "rt90_2.5_gon_v",
                            "rt90_0.0_gon_v",
                            "rt90_2.5_gon_o",
                            "rt90_5.0_gon_o"]):
            self.__fromTable.setHorizontalHeaderLabels(["     X     ", "     Y     "])
        if fromFormat in ([ "sweref_99_tm",
                            "sweref_99_1200",
                            "sweref_99_1330",
                            "sweref_99_1500",
                            "sweref_99_1630",
                            "sweref_99_1800",
                            "sweref_99_1415",
                            "sweref_99_1545",
                            "sweref_99_1715",
                            "sweref_99_1845",
                            "sweref_99_2015",
                            "sweref_99_2145",
                            "sweref_99_2315"]):
            self.__fromTable.setHorizontalHeaderLabels(["     N     ", "     E     "])
        # To columns.
        if toFormat in (["latlong_dd"]):
            self.__toTable.setHorizontalHeaderLabels(["Latitude DD", "Longitude DD"])
        if toFormat in (["latlong_dm"]):
            self.__toTable.setHorizontalHeaderLabels(["Latitude DM", "Longitude DM"])
        if toFormat in (["latlong_dms"]):
            self.__toTable.setHorizontalHeaderLabels(["Latitude DMS", "Longitude DMS"])
        if toFormat in ([ "rt90_7.5_gon_v",
                            "rt90_5.0_gon_v",
                            "rt90_2.5_gon_v",
                            "rt90_0.0_gon_v",
                            "rt90_2.5_gon_o",
                            "rt90_5.0_gon_o"]):
            self.__toTable.setHorizontalHeaderLabels(["     X     ", "     Y     "])
        if toFormat in ([ "sweref_99_tm",
                            "sweref_99_1200",
                            "sweref_99_1330",
                            "sweref_99_1500",
                            "sweref_99_1630",
                            "sweref_99_1800",
                            "sweref_99_1415",
                            "sweref_99_1545",
                            "sweref_99_1715",
                            "sweref_99_1845",
                            "sweref_99_2015",
                            "sweref_99_2145",
                            "sweref_99_2315"]):
            self.__toTable.setHorizontalHeaderLabels(["     N     ", "     E     "])
        #
        self.__fromTable.resizeColumnsToContents()
        self.__toTable.resizeColumnsToContents()
