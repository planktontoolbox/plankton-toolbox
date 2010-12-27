#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Mellifica toolbox. http://toolbox.mellifica.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 Arnold Andreasson
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
import plankton_toolbox.utils as utils
import plankton_toolbox.tools.tool_base as tool_base
from plankton_toolbox.core.map_projections.swedish_geoposition_converter import SwedishGeoPositionConverter
import plankton_toolbox.core.map_projections.latlong_dd_dm_dms as latlong

class LatLongTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentWidget):
        """ """
        super(LatLongTool, self).__init__(name, parentWidget)
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
 
    def _createContent(self):
        """ """
        tabWidget = QtGui.QTabWidget(self._parent)
        self.setWidget(tabWidget)
        
        # Widgets for user input data.
        self.__latDd = QtGui.QLineEdit("", tabWidget)
        self.__longDd = QtGui.QLineEdit("", tabWidget)
#        self.connect(self.__latDd, QtCore.SIGNAL("textChanged(QString)"), self.__latDd_calculate)
#        self.connect(self.__longDd, QtCore.SIGNAL("textChanged(QString)"), self.__longDd_calculate)
        self.connect(self.__latDd, QtCore.SIGNAL("textEdited(QString)"), self.__latDd_calculate)
        self.connect(self.__longDd, QtCore.SIGNAL("textEdited(QString)"), self.__longDd_calculate)
        self.connect(self.__latDd, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDd, QtCore.SIGNAL("editingFinished()"), self.__update_long)

        self.__latDm = QtGui.QLineEdit("", tabWidget)
        self.__longDm = QtGui.QLineEdit("", tabWidget)
#        self.connect(self.__latDm, QtCore.SIGNAL("textChanged(QString)"), self.__latDm_calculate)
#        self.connect(self.__longDm, QtCore.SIGNAL("textChanged(QString)"), self.__longDm_calculate)
        self.connect(self.__latDm, QtCore.SIGNAL("textEdited(QString)"), self.__latDm_calculate)
        self.connect(self.__longDm, QtCore.SIGNAL("textEdited(QString)"), self.__longDm_calculate)
        self.connect(self.__latDm, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDm, QtCore.SIGNAL("editingFinished()"), self.__update_long)

        self.__latDms = QtGui.QLineEdit("", tabWidget)
        self.__longDms = QtGui.QLineEdit("", tabWidget)
#        self.connect(self.__latDms, QtCore.SIGNAL("textChanged(QString)"), self.__latDms_calculate)
#        self.connect(self.__longDms, QtCore.SIGNAL("textChanged(QString)"), self.__longDms_calculate)
        self.connect(self.__latDms, QtCore.SIGNAL("textEdited(QString)"), self.__latDms_calculate)
        self.connect(self.__longDms, QtCore.SIGNAL("textEdited(QString)"), self.__longDms_calculate)
        self.connect(self.__latDms, QtCore.SIGNAL("editingFinished()"), self.__update_lat)
        self.connect(self.__longDms, QtCore.SIGNAL("editingFinished()"), self.__update_long)

        self.__rt90Proj = QtGui.QComboBox(tabWidget)
        self.__rt90Proj.addItems(["rt90_7.5_gon_v",
                                "rt90_5.0_gon_v",
                                "rt90_2.5_gon_v",
                                "rt90_0.0_gon_v",
                                "rt90_2.5_gon_o",
                                "rt90_5.0_gon_o"])
        self.__rt90Proj.setCurrentIndex(2) # Default rt90_2.5_gon_v
        self.connect(self.__rt90Proj, QtCore.SIGNAL("currentIndexChanged(int)"), self.__update_rt90)

        self.__rt90X = QtGui.QLineEdit("", tabWidget)
        self.__rt90Y = QtGui.QLineEdit("", tabWidget)
#        self.connect(self.__rt90X, QtCore.SIGNAL("textChanged(QString)"), self.__rt90X_calculate)
#        self.connect(self.__rt90Y, QtCore.SIGNAL("textChanged(QString)"), self.__rt90Y_calculate)
        self.connect(self.__rt90X, QtCore.SIGNAL("textEdited(QString)"), self.__rt90_calculate)
        self.connect(self.__rt90Y, QtCore.SIGNAL("textEdited(QString)"), self.__rt90_calculate)
#        self.connect(self.__rt90X, QtCore.SIGNAL("editingFinished()"), self.__update_rt90)
#        self.connect(self.__rt90Y, QtCore.SIGNAL("editingFinished()"), self.__update_rt90)

        self.__sweref99Proj = QtGui.QComboBox(tabWidget)
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

        self.__sweref99N = QtGui.QLineEdit("", tabWidget)
        self.__sweref99E = QtGui.QLineEdit("", tabWidget)
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
        
        
                
        # Layout.
        # Tabs, single and multiple.
        singleWidget = QtGui.QWidget(tabWidget)
        tableWidget = QtGui.QWidget(tabWidget)
        tabWidget.addTab(singleWidget, "Single point")
        tabWidget.addTab(tableWidget, "Multiple points")
        
        # === SINGLE POSITION ===
               
        # Single position tab.
        singleLayout = QtGui.QGridLayout()
        singleWidget.setLayout(singleLayout)
        # Single, lat/long.        
        latLongGroup = QtGui.QGroupBox("SWEREF 99 (~WGS 84)", tabWidget)
        singleLayout.addWidget(latLongGroup, 0, 0)
        latLongLayout =  QtGui.QGridLayout()
        latLongGroup.setLayout(latLongLayout)
        #
        latitudLabel = QtGui.QLabel("Latitud", tabWidget)
        longitudLabel = QtGui.QLabel("Longitud", tabWidget)
        latLongLayout.addWidget(latitudLabel, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        latLongLayout.addWidget(longitudLabel, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        #
        latDdLabel = QtGui.QLabel("Degree:", tabWidget)
        latLongLayout.addWidget(latDdLabel, 1, 0)
        latLongLayout.addWidget(self.__latDd, 1, 1)
        latLongLayout.addWidget(self.__longDd, 1, 2)
        #
        latDmLabel = QtGui.QLabel("Deg/min:", tabWidget)
        latLongLayout.addWidget(latDmLabel, 2, 0)
        latLongLayout.addWidget(self.__latDm, 2, 1)
        latLongLayout.addWidget(self.__longDm, 2, 2)
        #
        latDmsLabel = QtGui.QLabel("Deg/min/sec:", tabWidget)
        latLongLayout.addWidget(latDmsLabel, 3, 0)
        latLongLayout.addWidget(self.__latDms, 3, 1)
        latLongLayout.addWidget(self.__longDms, 3, 2)                
        # Single, rt90.        
        rt90Group = QtGui.QGroupBox("RT 90", tabWidget)
        singleLayout.addWidget(rt90Group, 1, 0)
        rt90Layout =  QtGui.QGridLayout()
        rt90Group.setLayout(rt90Layout)
        #
        rt90ProjWidget = QtGui.QWidget(tabWidget)
        rt90ProjLayout = QtGui.QHBoxLayout()
        rt90ProjWidget.setLayout(rt90ProjLayout)
        rt90ProjLabel = QtGui.QLabel("Map projection:", tabWidget)
        rt90ProjLayout.addStretch(5)
        rt90ProjLayout.addWidget(rt90ProjLabel)
        rt90ProjLayout.addWidget(self.__rt90Proj)
        rt90ProjLayout.addStretch(5)
        #
        rt90XLabel = QtGui.QLabel("X:", tabWidget)
        rt90YLabel = QtGui.QLabel("Y:", tabWidget)
        rt90Layout.addWidget(rt90ProjWidget, 0, 0, 1, 4)
        rt90Layout.addWidget(rt90XLabel, 1, 0)
        rt90Layout.addWidget(self.__rt90X, 1, 1)
        rt90Layout.addWidget(rt90YLabel, 1, 2)
        rt90Layout.addWidget(self.__rt90Y, 1, 3)        
        # Single, sweref 99 dd mm.        
        sweref99Group = QtGui.QGroupBox("SWEREF 99 TM, SWEREF 99 dd mm", tabWidget)
        singleLayout.addWidget(sweref99Group, 2, 0)
        sweref99Layout = QtGui.QGridLayout()
        sweref99Group.setLayout(sweref99Layout)
        #
        sweref99ProjWidget = QtGui.QWidget(tabWidget)
        sweref99ProjLayout = QtGui.QHBoxLayout()
        sweref99ProjWidget.setLayout(sweref99ProjLayout)
        sweref99ProjLabel = QtGui.QLabel("Map projection:", tabWidget)
        sweref99ProjLayout.addStretch(5)
        sweref99ProjLayout.addWidget(sweref99ProjLabel)
        sweref99ProjLayout.addWidget(self.__sweref99Proj)
        sweref99ProjLayout.addStretch(5)
        #
        sweref99NLabel = QtGui.QLabel("N:", tabWidget)
        sweref99ELabel = QtGui.QLabel("E:", tabWidget)
        sweref99Layout.addWidget(sweref99ProjWidget, 0, 0, 1, 4)
        sweref99Layout.addWidget(sweref99NLabel, 1, 0)
        sweref99Layout.addWidget(self.__sweref99N, 1, 1)
        sweref99Layout.addWidget(sweref99ELabel, 1, 2)
        sweref99Layout.addWidget(self.__sweref99E, 1, 3)
        #
        hbox = QtGui.QHBoxLayout()
        singleLayout.addLayout(hbox, 3, 0)
        hbox.addWidget(self.__opengooglemaps)
        hbox.addWidget(self.__openlatlongmellifica)
        #
        singleLayout.setRowStretch(4, 5)
        
        # === TABLE POSITIONS ===
        
#        # Table position tab. Active widgets.
#        self.__fromFormatComboBox = QtGui.QComboBox(tabWidget)
#        self.__fromFormatComboBox.addItems(["latlong_dd",
#                                            "latlong_dm",
#                                            "latlong_dms",
#                                            "rt90_7.5_gon_v",
#                                            "rt90_5.0_gon_v",
#                                            "rt90_2.5_gon_v",
#                                            "rt90_0.0_gon_v",
#                                            "rt90_2.5_gon_o",
#                                            "rt90_5.0_gon_o",
#                                            "sweref_99_tm",
#                                            "sweref_99_1200",
#                                            "sweref_99_1330",
#                                            "sweref_99_1500",
#                                            "sweref_99_1630",
#                                            "sweref_99_1800",
#                                            "sweref_99_1415",
#                                            "sweref_99_1545",
#                                            "sweref_99_1715",
#                                            "sweref_99_1845",
#                                            "sweref_99_2015",
#                                            "sweref_99_2145",
#                                            "sweref_99_2315"])
#        self.__fromFormatComboBox.setCurrentIndex(0) # Default: latlong_dd
#        self.connect(self.__fromFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.__calculateTable)
#        self.__pasteFromClipboardButton = QtGui.QPushButton("Paste from clipboard", tabWidget)
#        self.connect(self.__pasteFromClipboardButton, QtCore.SIGNAL("clicked()"), self.__pasteFromClipboard)
#        self.__reverseFromButton = QtGui.QPushButton("Reverse column order", tabWidget)
#        self.connect(self.__reverseFromButton, QtCore.SIGNAL("clicked()"), self.__reverseFromColumnOrder)
#        self.__fromTable = QtGui.QTableWidget(tabWidget)
#        self.__fromTable.setColumnCount(2)
#        self.__fromTable.setHorizontalHeaderLabels(["Lat", "Long"])
#        self.__fromTable.setRowCount(20)
#        #
#        self.__toFormatComboBox = QtGui.QComboBox(tabWidget)
#        self.__toFormatComboBox.addItems([  "latlong_dd",
#                                            "latlong_dm",
#                                            "latlong_dms",
#                                            "rt90_7.5_gon_v",
#                                            "rt90_5.0_gon_v",
#                                            "rt90_2.5_gon_v",
#                                            "rt90_0.0_gon_v",
#                                            "rt90_2.5_gon_o",
#                                            "rt90_5.0_gon_o",
#                                            "sweref_99_tm",
#                                            "sweref_99_1200",
#                                            "sweref_99_1330",
#                                            "sweref_99_1500",
#                                            "sweref_99_1630",
#                                            "sweref_99_1800",
#                                            "sweref_99_1415",
#                                            "sweref_99_1545",
#                                            "sweref_99_1715",
#                                            "sweref_99_1845",
#                                            "sweref_99_2015",
#                                            "sweref_99_2145",
#                                            "sweref_99_2315"])
#        self.__toFormatComboBox.setCurrentIndex(9) # Default: sweref_99_tm
#        self.connect(self.__toFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.__calculateTable)
#        self.__copyToClipboardButton = QtGui.QPushButton("Paste from clipboard", tabWidget)
#        self.connect(self.__copyToClipboardButton, QtCore.SIGNAL("clicked()"), self.__copyToClipboard)
#        self.__reverseToButton = QtGui.QPushButton("Reverse column order", tabWidget)
#        self.connect(self.__reverseToButton, QtCore.SIGNAL("clicked()"), self.__reverseToColumnOrder)
#        self.__toTable = QtGui.QTableWidget(tabWidget)
#        self.__toTable.setColumnCount(2)
#        self.__toTable.setHorizontalHeaderLabels(["Lat", "Long"])
#        self.__toTable.setRowCount(20)
#        #
#        
#        # Table position tab. Layout.
#        tableLayout = QtGui.QGridLayout()
#        tableWidget.setLayout(tableLayout)
##        tableLayout.setRowStretch(4, 5)
#        #
#        tableFromGroup = QtGui.QGroupBox("From", tabWidget)
#        tableLayout.addWidget(tableFromGroup, 0, 0)
#        tableFromLayout =  QtGui.QGridLayout()
#        tableFromGroup.setLayout(tableFromLayout)
#        #
##        aaaaaaLabel = QtGui.QLabel("Aaaaaa", tabWidget)
##        bbbbbbLabel = QtGui.QLabel("Bbbbbb", tabWidget)
##        tableFromLayout.addWidget(aaaaaaLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
##        tableFromLayout.addWidget(bbbbbbLabel, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
#        tableFromLayout.addWidget(self.__pasteFromClipboardButton, 0, 0, 1, 2, QtCore.Qt.AlignLeft)
#        tableFromLayout.addWidget(self.__fromTable, 1, 0, 1, 2)
                

    
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
        if ((self.__rt90X.text() == "") or (self.__rt90Y.text() == "")):
            self.__latitude = None
            self.__longitude = None
        else:
            x = float(self.__rt90X.text().replace(",", "."))
            y = float(self.__rt90Y.text().replace(",", "."))
            converter = SwedishGeoPositionConverter(self.__rt90Proj.currentText())
            self.__latitude, self.__longitude = converter.gridToGeodetic(x, y)
        self.__update_lat()
        self.__update_long()
        self.__update_sweref99()
        
    def __sweref99Proj_calculate(self, index):
        """ """
        
    def __sweref99_calculate(self, qstring):
        """ """
        if ((self.__sweref99N.text() == "") or (self.__sweref99E.text() == "")):
            self.__latitude = None
            self.__longitude = None
        else:
            n = float(self.__sweref99E.text().replace(",", "."))
            e = float(self.__sweref99E.text().replace(",", "."))
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
        if (len(self.__latDd.text()) == 0) or (len(self.__longDd.text()) == 0):
            utils.Logger().info("Failed to open maps.google.com. No values for lat/long.")
            return
        webbrowser.open("http://maps.google.com/maps/?ll=" + self.__latDd.text() + "," + self.__longDd.text())
        
    def __open_latlongmellifica(self):
        """ Launch web browser and use latlong.mellifica.se to display position. """
        if (len(self.__latDd.text()) == 0) or (len(self.__longDd.text()) == 0):
            utils.Logger().info("Failed to open latlong.mellifica.se. No values for lat/long.")
            return
        webbrowser.open("http://latlong.mellifica.se/?latlong=" + self.__latDd.text() + "," + self.__longDd.text())
        
        





#    def __paste(self):
#        """ """
#        clipboard = QtGui.QApplication.clipboard()
#        if clipboard.mimeData().hasText():
#            self.__fromTable.clearContents()
#            rows = clipboard.text().split("\n") # All whitespaces splits.
#            index = 0
#            for row in rows[:]:
#                items = row.split("\t")
#                try:
#                    if float(items[0]):
#                        self.__fromTable.setItem(index, 0, QtGui.QTableWidgetItem(items[0].trimmed()))
#                except ValueError: # Catch float errors.
#                    pass
#                try:
#                    if float(items[1]):
#                        self.__fromTable.setItem(index, 1, QtGui.QTableWidgetItem(items[1].trimmed()))
#                    index = index + 1
#                except ValueError: # Catch float errors.
#                    pass

    def __pasteFromClipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        if clipboard.mimeData().hasText():
            self.__fromTable.clearContents()
            rows = clipboard.text().split("\n") # All whitespaces splits.
            index = 0
            for row in rows[:]:
                items = row.split("\t")
                try:
                    if float(items[0]):
                        self.__fromTable.setItem(index, 0, QtGui.QTableWidgetItem(items[0].trimmed()))
                except ValueError: # Catch float errors.
                    pass
                try:
                    if float(items[1]):
                        self.__fromTable.setItem(index, 1, QtGui.QTableWidgetItem(items[1].trimmed()))
                    index = index + 1
                except ValueError: # Catch float errors.
                    pass

    def __copyToClipboard(self):
        """ """

    def __calculateTable(self):
        """ """

    def __reverseFromColumnOrder(self):
        """ """

    def __reverseToColumnOrder(self):
        """ """
