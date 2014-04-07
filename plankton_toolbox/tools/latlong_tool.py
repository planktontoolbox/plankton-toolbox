#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import webbrowser
import envmonlib
import plankton_toolbox.tools.tool_base as tool_base
from plankton_toolbox.core.map_projections.swedish_geoposition_converter import SwedishGeoPositionConverter
import plankton_toolbox.core.map_projections.latlong_dd_dm_dms as latlong

class LatLongTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentWidget):
        """ """
        # User input data.
        self._lat_dd = None
        self._lat_dm = None
        self._lat_dms = None
        self._long_dd = None
        self._long_dm = None
        self._long_dms = None
        self._proj_rt90 = None
        self._x_rt90 = None
        self._y_rt90 = None
        self._proj_sweref99 = None
        self._n_sweref99 = None
        self._e_sweref99 = None
        self._latitude = None # Decimal degrees. Type=float.
        self._longitude = None # Decimal degrees. Type=float.
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(LatLongTool, self).__init__(name, parentWidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)
 
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget for single point or table. 
        tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(tabWidget)
        tabWidget.addTab(self._createContentSinglePoint(), "Single point")
        tabWidget.addTab(self._createContentMultiplePoints(), "Multiple points")        
#        contentLayout.addLayout(self._createContentControl())


    def _createContentSinglePoint(self):
        """ """
        singleWidget = QtGui.QWidget()
        # === Active widgets and connections. ===
        # Decimal degree.
        self._latDd = QtGui.QLineEdit("")
        self._longDd = QtGui.QLineEdit("")
#        self.connect(self._latDd, QtCore.SIGNAL("textChanged(QString)"), self._latDd_calculate)
#        self.connect(self._longDd, QtCore.SIGNAL("textChanged(QString)"), self._longDd_calculate)
        self.connect(self._latDd, QtCore.SIGNAL("textEdited(QString)"), self._latDd_calculate)
        self.connect(self._longDd, QtCore.SIGNAL("textEdited(QString)"), self._longDd_calculate)
        self.connect(self._latDd, QtCore.SIGNAL("editingFinished()"), self._update_lat)
        self.connect(self._longDd, QtCore.SIGNAL("editingFinished()"), self._update_long)
        # Degree, minutes.
        self._latDm = QtGui.QLineEdit("")
        self._longDm = QtGui.QLineEdit("")
#        self.connect(self._latDm, QtCore.SIGNAL("textChanged(QString)"), self._latDm_calculate)
#        self.connect(self._longDm, QtCore.SIGNAL("textChanged(QString)"), self._longDm_calculate)
        self.connect(self._latDm, QtCore.SIGNAL("textEdited(QString)"), self._latDm_calculate)
        self.connect(self._longDm, QtCore.SIGNAL("textEdited(QString)"), self._longDm_calculate)
        self.connect(self._latDm, QtCore.SIGNAL("editingFinished()"), self._update_lat)
        self.connect(self._longDm, QtCore.SIGNAL("editingFinished()"), self._update_long)
        # Degree, minutes, seconds.
        self._latDms = QtGui.QLineEdit("")
        self._longDms = QtGui.QLineEdit("")
#        self.connect(self._latDms, QtCore.SIGNAL("textChanged(QString)"), self._latDms_calculate)
#        self.connect(self._longDms, QtCore.SIGNAL("textChanged(QString)"), self._longDms_calculate)
        self.connect(self._latDms, QtCore.SIGNAL("textEdited(QString)"), self._latDms_calculate)
        self.connect(self._longDms, QtCore.SIGNAL("textEdited(QString)"), self._longDms_calculate)
        self.connect(self._latDms, QtCore.SIGNAL("editingFinished()"), self._update_lat)
        self.connect(self._longDms, QtCore.SIGNAL("editingFinished()"), self._update_long)
        # RT 90.
        self._rt90Proj = QtGui.QComboBox()
        self._rt90Proj.addItems(["rt90_7.5_gon_v",
                                "rt90_5.0_gon_v",
                                "rt90_2.5_gon_v",
                                "rt90_0.0_gon_v",
                                "rt90_2.5_gon_o",
                                "rt90_5.0_gon_o"])
        self._rt90Proj.setCurrentIndex(2) # Default rt90_2.5_gon_v
        self.connect(self._rt90Proj, QtCore.SIGNAL("currentIndexChanged(int)"), self._update_rt90)
        self._rt90X = QtGui.QLineEdit("")
        self._rt90Y = QtGui.QLineEdit("")
#        self.connect(self._rt90X, QtCore.SIGNAL("textChanged(QString)"), self._rt90X_calculate)
#        self.connect(self._rt90Y, QtCore.SIGNAL("textChanged(QString)"), self._rt90Y_calculate)
        self.connect(self._rt90X, QtCore.SIGNAL("textEdited(QString)"), self._rt90_calculate)
        self.connect(self._rt90Y, QtCore.SIGNAL("textEdited(QString)"), self._rt90_calculate)
#        self.connect(self._rt90X, QtCore.SIGNAL("editingFinished()"), self._update_rt90)
#        self.connect(self._rt90Y, QtCore.SIGNAL("editingFinished()"), self._update_rt90)
        # SWEREF 99 TM/deg-min.
        self._sweref99Proj = QtGui.QComboBox()
        self._sweref99Proj.addItems(["sweref_99_tm",
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
        self.connect(self._sweref99Proj, QtCore.SIGNAL("currentIndexChanged(int)"), self._update_sweref99)
        self._sweref99N = QtGui.QLineEdit("")
        self._sweref99E = QtGui.QLineEdit("")
#        self.connect(self._sweref99N, QtCore.SIGNAL("textChanged(QString)"), self._sweref99N_calculate)
#        self.connect(self._sweref99E, QtCore.SIGNAL("textChanged(QString)"), self._sweref99E_calculate)
        self.connect(self._sweref99N, QtCore.SIGNAL("textEdited(QString)"), self._sweref99_calculate)
        self.connect(self._sweref99E, QtCore.SIGNAL("textEdited(QString)"), self._sweref99_calculate)
#        self.connect(self._sweref99N, QtCore.SIGNAL("editingFinished()"), self._update_sweref99)
#        self.connect(self._sweref99E, QtCore.SIGNAL("editingFinished()"), self._update_sweref99)
        # Open in web browser: Google maps.
        self._opengooglemaps = QtGui.QPushButton("Open maps.google.com")
        self.connect(self._opengooglemaps, QtCore.SIGNAL("clicked()"), self._open_googlemaps)                
        # Open in web browser: latlong.mellifica.se.
        self._openlatlongmellifica = QtGui.QPushButton("Open latlong.mellifica.se")
        self.connect(self._openlatlongmellifica, QtCore.SIGNAL("clicked()"), self._open_latlongmellifica)                
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
        latLongLayout.addWidget(self._latDd, gridrow, 1)
        latLongLayout.addWidget(self._longDd, gridrow, 2)
        gridrow += 1
        latDmLabel = QtGui.QLabel("Deg/min:")
        latLongLayout.addWidget(latDmLabel, gridrow, 0)
        latLongLayout.addWidget(self._latDm, gridrow, 1)
        latLongLayout.addWidget(self._longDm, gridrow, 2)
        gridrow += 1
        latDmsLabel = QtGui.QLabel("Deg/min/sec:")
        latLongLayout.addWidget(latDmsLabel, gridrow, 0)
        latLongLayout.addWidget(self._latDms, gridrow, 1)
        latLongLayout.addWidget(self._longDms, gridrow, 2)                
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
        rt90ProjLayout.addWidget(self._rt90Proj)
        rt90ProjLayout.addStretch(5)
        gridrow = 0
        rt90XLabel = QtGui.QLabel("X:")
        rt90YLabel = QtGui.QLabel("Y:")
        rt90Layout.addWidget(rt90ProjWidget, gridrow, 0, 1, 4)
        gridrow += 1
        rt90Layout.addWidget(rt90XLabel, gridrow, 0)
        rt90Layout.addWidget(self._rt90X, gridrow, 1)        
        rt90Layout.addWidget(rt90YLabel, gridrow, 2)
        rt90Layout.addWidget(self._rt90Y, 1, 3)        
        # Single, sweref 99 dd mm.        
        sweref99Group = QtGui.QGroupBox("SWEREF 99 TM, SWEREF 99 dd mm")
        singleLayout.addWidget(sweref99Group, 2, 0)
        sweref99Layout = QtGui.QGridLayout()
        sweref99Group.setLayout(sweref99Layout)
        #
        sweref99ProjWidget = QtGui.QWidget()
        sweref99ProjLayout = QtGui.QHBoxLayout()
        sweref99ProjWidget.setLayout(sweref99ProjLayout)
        sweref99ProjLabel = QtGui.QLabel("Map projection:")
        sweref99ProjLayout.addStretch(5)
        sweref99ProjLayout.addWidget(sweref99ProjLabel)
        sweref99ProjLayout.addWidget(self._sweref99Proj)
        sweref99ProjLayout.addStretch(5)
        #
        sweref99NLabel = QtGui.QLabel("N:")
        sweref99ELabel = QtGui.QLabel("E:")
        sweref99Layout.addWidget(sweref99ProjWidget, 0, 0, 1, 4)
        #
        sweref99Layout.addWidget(sweref99NLabel, 1, 0)
        sweref99Layout.addWidget(self._sweref99N, 1, 1)
        sweref99Layout.addWidget(sweref99ELabel, 1, 2)
        sweref99Layout.addWidget(self._sweref99E, 1, 3)
        #
        viewInBrowserLabel = QtGui.QLabel("\nView current position in web browser:")
        singleLayout.addWidget(viewInBrowserLabel, 3, 0)
        hbox = QtGui.QHBoxLayout()
        singleLayout.addLayout(hbox, 4, 0)
        hbox.addWidget(self._opengooglemaps)
        hbox.addWidget(self._openlatlongmellifica)
        hbox.addStretch(2)
        #
        singleLayout.setRowStretch(5, 5)
        #
        return singleWidget
        
    def _createContentMultiplePoints(self):
        """ """
        multipleWidget = QtGui.QWidget()
        # === Active widgets and connections. ===
        # Table position tab. Active widgets.
        self._fromFormatComboBox = QtGui.QComboBox()
        self._fromFormatComboBox.addItems(["latlong_dd",
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
        self._fromFormatComboBox.setCurrentIndex(0) # Default: latlong_dd
        self.connect(self._fromFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self._calculateTable)
        self._pasteFromClipboardButton = QtGui.QPushButton("Paste from clipboard")
        self.connect(self._pasteFromClipboardButton, QtCore.SIGNAL("clicked()"), self._pasteFromClipboard)
        self._fromTable = QtGui.QTableWidget()
        self._fromTable.setColumnCount(2)
#        self._fromTable.setHorizontalHeaderLabels(["Latitude", "Longitude"])
#        self._fromTable.setRowCount(20)
        self._fromTable.setAlternatingRowColors(True)
        self._fromTable.verticalHeader().setDefaultSectionSize(18)
        self._fromTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self._fromTable.horizontalHeader().setStretchLastSection(True)
        # User for manually entered data.
        self.connect(self._fromTable, QtCore.SIGNAL("cellChanged(int, int)"), self._calculateTable)
        #
        self._toFormatComboBox = QtGui.QComboBox()
        self._toFormatComboBox.addItems([  "latlong_dd",
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
        self._toFormatComboBox.setCurrentIndex(9) # Default: sweref_99_tm
        self.connect(self._toFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self._calculateTable)
        self._copyToClipboardButton = QtGui.QPushButton("Copy to clipboard")
        self.connect(self._copyToClipboardButton, QtCore.SIGNAL("clicked()"), self._copyToClipboard)
        self._toTable = QtGui.QTableWidget()
        self._toTable.setColumnCount(2)
#        self._toTable.setHorizontalHeaderLabels(["N", "E"])
#        self._toTable.setRowCount(20)
        self._toTable.setAlternatingRowColors(True)
        self._toTable.verticalHeader().setDefaultSectionSize(18)
        self._toTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
#        self._toTable.horizontalHeader().setStretchLastSection(True)
        #
        self._clear_button = QtGui.QPushButton("Clear")
        self.connect(self._clear_button, QtCore.SIGNAL("clicked()"), self._clear)                
        # Update headers.
        self._setColumnHeader()
        
        # === Layout. ===
        multipleLayout = QtGui.QVBoxLayout()
        multipleWidget.setLayout(multipleLayout)
        hLayout = QtGui.QHBoxLayout()
        multipleLayout.addLayout(hLayout)
        #
        multipleFromGroup = QtGui.QGroupBox("From position")
        hLayout.addWidget(multipleFromGroup)
        fromGrid =  QtGui.QGridLayout()
        multipleFromGroup.setLayout(fromGrid)
        gridrow = 0
        fromFormatLabel = QtGui.QLabel("<b>Format:</b>")
        fromGrid.addWidget(fromFormatLabel, gridrow, 0, 1, 1, QtCore.Qt.AlignLeft)
        fromGrid.addWidget(self._fromFormatComboBox, gridrow, 1, 1, 8, QtCore.Qt.AlignLeft)
        gridrow += 1
        fromGrid.addWidget(self._pasteFromClipboardButton, gridrow, 0, 1, 9)
        gridrow += 1
        fromGrid.addWidget(self._fromTable, gridrow, 0, 1, 9)
        #
        multipleToGroup = QtGui.QGroupBox("To position")
        hLayout.addWidget(multipleToGroup)
        toGrid =  QtGui.QGridLayout()
        multipleToGroup.setLayout(toGrid)
        gridrow = 0
        toFormatLabel = QtGui.QLabel("<b>Format:</b>")
        toGrid.addWidget(toFormatLabel, gridrow, 0, 1, 1, QtCore.Qt.AlignLeft)
        toGrid.addWidget(self._toFormatComboBox, gridrow, 1, 1, 8, QtCore.Qt.AlignLeft)
        gridrow += 1
        toGrid.addWidget(self._copyToClipboardButton, gridrow, 0, 1, 9)
        gridrow += 1
        toGrid.addWidget(self._toTable, gridrow, 0, 1, 9)
        #
        hBoxLayout = QtGui.QHBoxLayout()
        hBoxLayout.addWidget(self._clear_button)
        hBoxLayout.addStretch(5)
        multipleLayout.addLayout(hBoxLayout)

        return multipleWidget
    
#    def _createContentControl(self):
#        """ """
#        # Active widgets and connections.
#        self._clear_button = QtGui.QPushButton("Clear")
#        self.connect(self._clear_button, QtCore.SIGNAL("clicked()"), self._clear)                
#        # Layout widgets.
#        layout = QtGui.QHBoxLayout()
#        layout.addWidget(self._clear_button)
#        layout.addStretch(5)
#        #
#        return layout

# === Single methods. ===

    def _clear(self):
        """ """
        self._fromTable.clearContents()
        self._toTable.clearContents()
        self._fromTable.setRowCount(0)
        self._toTable.setRowCount(0)
        self._fromTable.resizeColumnsToContents()
        self._toTable.resizeColumnsToContents()

    def set_latitude_longitude(self, lat, lon):
        """ 
        Set current position and update all fields. Used for external 
        program calls. 
        """
        self._latitude = lat
        self._longitude = lon
        self._update_lat()
        self._update_long()
        self._update_rt90()
        self._update_sweref99()

    def get_latitude_longitude(self):
        """ Get current position. Used for external program calls. """
        return (self._latitude, self._longitude)

    def _latDd_calculate(self, qstring):
        """ """
        self._latitude = latlong.convert_lat_from_dd(str(qstring))
        self._latDm.setText(latlong.convert_lat_to_dm(self._latitude))
        self._latDms.setText(latlong.convert_lat_to_dms(self._latitude))
        self._update_rt90()
        self._update_sweref99()
        
    def _longDd_calculate(self, qstring):
        """ """
        self._longitude = latlong.convert_long_from_dd(str(qstring))
        self._longDm.setText(latlong.convert_long_to_dm(self._longitude))
        self._longDms.setText(latlong.convert_long_to_dms(self._longitude))
        self._update_rt90()
        self._update_sweref99()
       
    def _latDm_calculate(self, qstring):
        """ """
        self._latitude = latlong.convert_lat_from_dm(str(qstring))
        self._latDd.setText(latlong.convert_lat_to_dd(self._latitude))
        self._latDms.setText(latlong.convert_lat_to_dms(self._latitude))
        self._update_rt90()
        self._update_sweref99()
        
    def _longDm_calculate(self, qstring):
        """ """
        self._longitude = latlong.convert_long_from_dm(str(qstring))
        self._longDd.setText(latlong.convert_long_to_dd(self._longitude))
        self._longDms.setText(latlong.convert_long_to_dms(self._longitude))
        self._update_rt90()
        self._update_sweref99()
        
    def _latDms_calculate(self, qstring):
        """ """
        self._latitude = latlong.convert_lat_from_dms(str(qstring))
        self._latDd.setText(latlong.convert_lat_to_dd(self._latitude))
        self._latDm.setText(latlong.convert_lat_to_dm(self._latitude))
        self._update_rt90()
        self._update_sweref99()
        
    def _longDms_calculate(self, qstring):
        """ """
        self._longitude = latlong.convert_long_from_dms(str(qstring))
        self._longDd.setText(latlong.convert_long_to_dd(self._longitude))
        self._longDm.setText(latlong.convert_long_to_dm(self._longitude))
        self._update_rt90()
        self._update_sweref99()
        
    def _rt90Proj_calculate(self, index):
        """ """
        
    def _rt90_calculate(self, qstring):
        """ """
        if ((unicode(self._rt90X.text()) == "") or (unicode(self._rt90Y.text()) == "")):
            self._latitude = None
            self._longitude = None
        else:
            x = float(unicode(self._rt90X.text()).replace(",", "."))
            y = float(unicode(self._rt90Y.text()).replace(",", "."))
            converter = SwedishGeoPositionConverter(self._rt90Proj.currentText())
            self._latitude, self._longitude = converter.gridToGeodetic(x, y)
        self._update_lat()
        self._update_long()
        self._update_sweref99()
        
    def _sweref99Proj_calculate(self, index):
        """ """
        
    def _sweref99_calculate(self, qstring):
        """ """
        if ((unicode(self._sweref99N.text()) == "") or (unicode(self._sweref99E.text()) == "")):
            self._latitude = None
            self._longitude = None
        else:
            n = float(unicode(self._sweref99E.text()).replace(",", "."))
            e = float(unicode(self._sweref99E.text()).replace(",", "."))
            converter = SwedishGeoPositionConverter(self._sweref99Proj.currentText())
            self._latitude, self._longitude = converter.gridToGeodetic(n, e)
        self._update_lat()
        self._update_long()
        self._update_rt90()
        
    def _update_lat(self):
        """ """
        self._latDd.setText(latlong.convert_lat_to_dd(self._latitude))
        self._latDm.setText(latlong.convert_lat_to_dm(self._latitude))
        self._latDms.setText(latlong.convert_lat_to_dms(self._latitude))

    def _update_long(self):
        """ """
        self._longDd.setText(latlong.convert_long_to_dd(self._longitude))
        self._longDm.setText(latlong.convert_long_to_dm(self._longitude))
        self._longDms.setText(latlong.convert_long_to_dms(self._longitude))

    def _update_rt90(self):
        """ """
        if ((self._latitude != None) and (self._longitude != None) and
            (self._latitude >= -90.0) and (self._latitude <= 90.0) and
            (self._longitude >= -180.0) and (self._longitude < 180.0)):
            converter = SwedishGeoPositionConverter(self._rt90Proj.currentText())
            x, y = converter.geodeticToGrid(self._latitude, self._longitude)
            self._rt90X.setText("%.3f" % x)
            self._rt90Y.setText("%.3f" % y)
        else:
            self._rt90X.setText("")
            self._rt90Y.setText("")

    def _update_sweref99(self):
        """ """
        if ((self._latitude != None) and (self._longitude != None) and
            (self._latitude >= -90.0) and (self._latitude <= 90.0) and
            (self._longitude >= -180.0) and (self._longitude < 180.0)):
            converter = SwedishGeoPositionConverter(self._sweref99Proj.currentText())
            n, e = converter.geodeticToGrid(self._latitude, self._longitude)
            self._sweref99N.setText("%.3f" % n)
            self._sweref99E.setText("%.3f" % e)
        else:
            self._sweref99N.setText("")
            self._sweref99E.setText("")

    def _execute_test_case(self):
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

    def _open_googlemaps(self):
        """ Launch web browser and use maps.google.com to display position. """
        if (len(unicode(self._latDd.text())) == 0) or (len(unicode(self._longDd.text())) == 0):
            envmonlib.Logging().log("Failed to open maps.google.com. No values for lat/long.")
            return
        webbrowser.open("http://maps.google.com/maps/?ll=" + unicode(self._latDd.text()) + "," + unicode(self._longDd.text()))
        
    def _open_latlongmellifica(self):
        """ Launch web browser and use latlong.mellifica.se to display position. """
        if (len(unicode(self._latDd.text())) == 0) or (len(unicode(self._longDd.text())) == 0):
            envmonlib.Logging().log("Failed to open latlong.mellifica.se. No values for lat/long.")
            return
        webbrowser.open("http://latlong.mellifica.se/?latlong=" + unicode(self._latDd.text()) + "," + unicode(self._longDd.text()))
        
# === Multiple methods. ===        

    def _pasteFromClipboard(self):
        """ """
        self._fromTable.blockSignals(True)
        self._fromTable.clearContents()
        self._toTable.clearContents()
        clipboard = QtGui.QApplication.clipboard()
        if clipboard.mimeData().hasText():
            rows = unicode(clipboard.text()).split('\n') # Row separator in clip board.
            self._fromTable.setRowCount(len(rows))
            self._toTable.setRowCount(len(rows))
            for index, row in enumerate(rows):
                items = row.split("\t") # Column separator in clip board.
#                if unicode(self._fromFormatComboBox.currentText()) in (u'latlong_dm', u'latlong_dms'):
#                    # Formats DM and DMS are not pure numeric values. 
                if len(items) >= 1:
                    self._fromTable.setItem(index, 0, QtGui.QTableWidgetItem(items[0]))
                if len(items) >= 2:
                    self._fromTable.setItem(index, 1, QtGui.QTableWidgetItem(items[1]))
#                else:
#                    if len(items) >= 1:
#                        try:
#                            float(items[0].strip().replace(",", ".")) # Check if valid format.
#                            self._fromTable.setItem(index, 0, QtGui.QTableWidgetItem(items[0]))
#                        except ValueError:
#                            self._fromTable.setItem(index, 0, QtGui.QTableWidgetItem(''))
#                    if len(items) >= 2:
#                        try:
#                            float(items[1].strip().replace(",", ".")) # Check if valid format.
#                            self._fromTable.setItem(index, 1, QtGui.QTableWidgetItem(items[1]))
#                        except ValueError:
#                            self._fromTable.setItem(index, 1, QtGui.QTableWidgetItem(''))
        self._fromTable.resizeColumnsToContents()
        self._fromTable.blockSignals(False)
          
        self._calculateTable()

    def _copyToClipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        clipboardstring = ''
        for index in range(self._toTable.rowCount()):
            # Read from table.
            item_1 = self._toTable.item(index, 0)
            if item_1:
                to_1 = unicode(item_1.data(QtCore.Qt.DisplayRole).toString())
            else:
                to_1 = ''
            item_2 = self._toTable.item(index, 1)
            if item_2:
                to_2 = unicode(item_2.data(QtCore.Qt.DisplayRole).toString())
            else:
                to_2 = ''
            clipboardstring += to_1 + '\t' + to_2 + '\n'
        clipboard.setText(clipboardstring)

    def _calculateTable(self):
        """ """
        fromFormat = unicode(self._fromFormatComboBox.currentText())
        toFormat = unicode(self._toFormatComboBox.currentText())
        #
        fromConverter = SwedishGeoPositionConverter(self._fromFormatComboBox.currentText())
        toConverter = SwedishGeoPositionConverter(self._toFormatComboBox.currentText())
        #
        self._setColumnHeader()
        # 
        for index in range(self._fromTable.rowCount()):
            # Read from table.
            item_1 = self._fromTable.item(index, 0)
            item_2 = self._fromTable.item(index, 1)
            if (not item_1) or (not item_2) :
                self._toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self._toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
                continue # Go to next row.
            from_1 = unicode(item_1.data(QtCore.Qt.DisplayRole).toString())
            from_2 = unicode(item_2.data(QtCore.Qt.DisplayRole).toString())
            #
            from_1 = from_1.strip().replace(",", ".")
            from_2 = from_2.strip().replace(",", ".")                
            if (from_1 == '') or (from_2 == '') :
                self._toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self._toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
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
                try:
                    dd_1, dd_2 = fromConverter.gridToGeodetic(float(from_1), float(from_2))
                except:
                    continue # Go to next row.
            #
            if (not dd_1) or (not dd_2) :
                self._toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode('')))
                self._toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode('')))            
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
#                toConverter = SwedishGeoPositionConverter(self._toFormatComboBox.currentText())
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
            self._toTable.setItem(index, 0, QtGui.QTableWidgetItem(unicode(to_1)))
            self._toTable.setItem(index, 1,QtGui.QTableWidgetItem(unicode(to_2)))            
        #
        self._toTable.resizeColumnsToContents()

    def _setColumnHeader(self):
        """ Column names differ depending on selected projections. """
        fromFormat = self._fromFormatComboBox.currentText()
        toFormat = self._toFormatComboBox.currentText()
        # From columns.
        if fromFormat in (["latlong_dd"]):
            self._fromTable.setHorizontalHeaderLabels(["Latitude DD", "Longitude DD"])
        if fromFormat in (["latlong_dm"]):
            self._fromTable.setHorizontalHeaderLabels(["Latitude DM", "Longitude DM"])
        if fromFormat in (["latlong_dms"]):
            self._fromTable.setHorizontalHeaderLabels(["Latitude DMS", "Longitude DMS"])
        if fromFormat in ([ "rt90_7.5_gon_v",
                            "rt90_5.0_gon_v",
                            "rt90_2.5_gon_v",
                            "rt90_0.0_gon_v",
                            "rt90_2.5_gon_o",
                            "rt90_5.0_gon_o"]):
            self._fromTable.setHorizontalHeaderLabels(["     X     ", "     Y     "])
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
            self._fromTable.setHorizontalHeaderLabels(["     N     ", "     E     "])
        # To columns.
        if toFormat in (["latlong_dd"]):
            self._toTable.setHorizontalHeaderLabels(["Latitude DD", "Longitude DD"])
        if toFormat in (["latlong_dm"]):
            self._toTable.setHorizontalHeaderLabels(["Latitude DM", "Longitude DM"])
        if toFormat in (["latlong_dms"]):
            self._toTable.setHorizontalHeaderLabels(["Latitude DMS", "Longitude DMS"])
        if toFormat in ([ "rt90_7.5_gon_v",
                            "rt90_5.0_gon_v",
                            "rt90_2.5_gon_v",
                            "rt90_0.0_gon_v",
                            "rt90_2.5_gon_o",
                            "rt90_5.0_gon_o"]):
            self._toTable.setHorizontalHeaderLabels(["     X     ", "     Y     "])
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
            self._toTable.setHorizontalHeaderLabels(["     N     ", "     E     "])
        #
        self._fromTable.resizeColumnsToContents()
        self._toTable.resizeColumnsToContents()
