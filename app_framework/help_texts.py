#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).


class HelpTexts(object):
    """Help texts for the desktop application.
    Mostly displayed in util_qt.RichTextQLabel labels, basic HTML tags can be used.
    """

    def __init__(self, parent=None):
        """ """
        self._texts = {}
        self._add_texts()

    def get_text(self, key):
        """ """
        try:
            return self._texts[key]
        except:
            pass
        return ""

    def _add_texts(self):
        """ """

        # Start activity..

        self._texts[
            "start_activity"
        ] = """
        <br/>
        <h3>Welcome to Plankton Toolbox</h3>
        <p>
        Plankton Toolbox is a free tool for aquatic scientists, and others, 
        working with environmental monitoring related to phyto- and zooplankton. 
        </p>
        <p>
        Features include:
        <ul>        
            <li>Counting module for use by the microscope
            </li>
            <li>Imports phyto- or zooplankton data in .txt and .xlsx files in different formats (configurable)
            </li>
            <li>Work with data on abundance, biovolume and carbon content
            </li>
            <li>Data screening - quality control of data
            </li>
            <li>Report generator
            </li>
            <li>Aggregate data, e.g. from species level to class level
            </li>
            <li>Plotting tools
            </li>
            <li>Statistics (in early development)
            </li>
            <li>Export data in .txt or .xlsx for further analysis or plotting
            </li>
        </ul>
        </p>
        
        <h4>Usage instructions</h4>
        <p>
        A User Guide is available at: 
        <a href="http://nordicmicroalgae.org/tools">http://nordicmicroalgae.org/tools</a>.
        </p>
        
        <h4>Under development</h4>
        <p>
        Plankton Toolbox  is under development and provided for free with no guarantees regarding functionality. 
        Comments, bug reports and requests for new functionality are welcome and can be sent to 
        <a href="mailto:nordicmicroalgae@smhi.se">nordicmicroalgae@smhi.se</a>
        </p>
        <p>
        More information about the project is available via the menu "Help/About".
        </p>

        <h4>Acknowledgment</h4>
        <p>
        The development of Plankton Toolbox is funded by the 
        <a href="http://smhi.se">Swedish Meteorological and Hydrological Institute (SMHI)</a> 
        and the 
        <a href="http://www.vr.se"> Swedish Research Council</a> 
        through Grant No 2019-00242. 
        The software is part of the 
        <a href="https://biodiversitydata.se/">the Swedish Biodiversity Data Infrastructure (SBDI)</a> 
        and was former part of the Swedish Lifewatch project. 
        We further want to acknowledge the effort of the phytoplankton specialists who maintained the species lists 
        and also tested and suggested improvements of the software.
        </p>

        """

        # About.

        self._texts[
            "about"
        ] = """
        <p>
        <b>Plankton Toolbox</b> - ###version###
        </p>
        <p>
        Plankton Toolbox is a free tool for aquatic scientists, and others, 
        working with environmental monitoring related to phyto- and zooplankton.
        </p>
        <p>
        The software is under development and provided for free with no 
        guarantees regarding functionality. Comments, bug reports and requests 
        for new functionality are welcome and can be sent to 
        <a href="mailto:nordicmicroalgae@smhi.se">nordicmicroalgae@smhi.se</a>
        </p>
        <p>
        Plankton Toolbox can run on Windows and MacOS, no installation is needed.
        For Linux users it is possible to install it from the GitHub repository.
        The latest version can be found at: 
        <a href="http://nordicmicroalgae.org/tools">http://nordicmicroalgae.org/tools</a>.
        </p>
        <p>
        Plankton Toolbox is developed by the oceanographic unit of the
        <a href="http://smhi.se">Swedish Meteorological and Hydrological Institute (SMHI)</a>.
        The software is a product within 
        <a href="https://biodiversitydata.se/">the Swedish Biodiversity Data Infrastructure (SBDI)</a> 
        funded by SMHI and the 
        <a href="http://www.vr.se"> Swedish Research Council</a> through Grant No 2019-00242.
        </p>
        <p>
        The software is developed in Python and Qt/PyQt6. Released under the MIT license.
        Source code and info for developers at 
        <a href="https://github.com/planktontoolbox/plankton-toolbox">GitHub</a>.
        </p>
        """
