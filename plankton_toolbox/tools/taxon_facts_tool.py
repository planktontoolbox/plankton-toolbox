#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base

class TaxonFactsTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(TaxonFactsTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentFacts())
#        contentLayout.addStretch(5)

    def _contentFacts(self):
        """ """
        layout = QtGui.QVBoxLayout()

        label = QtGui.QLabel('<b><i>Dinophysis acuta</i> Ehrenberg 1839</b>')
        label.setAlignment(QtCore.Qt.AlignHCenter)
        text = QtGui.QTextBrowser()
        text.setHtml("""
<tbody>
    <tr>
        <th>Note on taxonomy</th>
        <td><p id="data_note_on_taxonomy"></p></td>
    </tr>
    <tr>
        <th>Morphology</th>
    
        <td><span id="data_morphology">The cells are widest below the middle</span></td>
    </tr>
    <tr>
        <th>Ecology</th>
        <td><span id="data_ecology"></span></td>
    </tr>
    <tr>
        <th>Other remarks</th>
    
        <td><p id="data_other_remarks">Width here = dorso-ventral depth. Dimorphic cells have been observed (Hansen 1993a). This species has been associated with DSP outbreaks (Larsen &amp; Moestrup 1992) 
        Distribution: Worldwide
        </p></td>
    </tr>
    <tr>
        <th>Trophic type</th>
        <td>
            <span id="data_trophic_type">A/H</span>

        </td>
    </tr>
    <tr>
        <th>Harmful</th>
        <td>
            <span id="data_harmful">Test test</span>
        </td>
    </tr>

    <tr>
        <th>Note on harmfulness</th>
        <td><p id="data_note_on_harmfulness"></p></td>
    </tr>
    <tr>
        <th>Substrate</th>
        <td><span id="data_substrate"></span></td>
    </tr>

    <tr>
        <th>Life form</th>
        <td><span id="data_life_form">Solitary</span></td>
    </tr>
    <tr>
        <th>Width</th>
        <td><span id="data_width"></span></td>

    </tr>
    <tr>
        <th>Length</th>
        <td><span id="data_length"></span></td>
    </tr>
    <tr>
        <th>Size</th>
        <td><span id="data_size">Length 54-94 um, width 43-60 um</span></td>

    </tr>
    <tr>
        <th>Resting spore</th>
        <td><span id="data_resting_spore"></span></td>
    </tr>
    <tr>
        <th>Literature</th>
        <td><p id="data_literature">
        Drebes, G. 1974. Marines Phytoplankton, Eine Auswahl der Helgoländer Planktonalgen (Diatomeen, Peridineen). Georg Thieme Verlag, Stuttgart. 186 pp.<br/><br/>
        Hansen, G. 1993a. Dimorphic individuals of<i> Dinophysis acuta</i> and <i>D.  norvegica</i> (Dinophyceae) from Danish waters. Phycologia. 32: 73-75.<br/><br/>
        Hansen, G. &amp; Larsen, J. 1992. Dinoflagellater i danske farvande. In: Thomsen, H. A. (ed.) Plankton i de indre danske farvande. Havforskning fra Miljöstyrelsen, Copenhagen, p. 45-155.<br/><br/>
        Larsen, J. &amp; Moestrup, Ö. 1992. Potentially toxic phytoplankton. 2. Genus <i>Dinophysis</i> (Dinophyceae). In: Lindley, J. A. (ed.) ICES Identification leaflets for plankton. International Council for the exploration of the sea, Copenhagen, p. 1-12.<br/><br/>
        Steidinger, K. A. &amp; Tangen, K. 1996. Dinoflagellates. In: Tomas, C. R. (ed.) Identifying marine diatoms and dinoflagellates. Academic Press, Inc., San Diego, p. 387-584.<br/><br/>
        </p></td>

    </tr>
</tbody>        
        """)

        layout.addWidget(label)
        layout.addWidget(text)
        #
        return layout
    
    def _test(self):
        """ """
        self._writeToLog("Name: " + unicode(self._nameedit.text()))
