#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

"""
Main module for the desktop application.

Organization name, domain and application name are used by QSettings. Settings
are stored in the register on Windows (path: "HKEY_CURRENT_USER/Software/...), 
in $HOME/.config on Linux and in $HOME/Library/Preferences on MacOS.
"""

import sys
import pathlib

# import base64
from PyQt6 import QtGui
from PyQt6 import QtWidgets
import app_framework

__version__ = ""


def desktop_application():
    """
    Main function for the desktop application.
    """

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Plankton Toolbox")
    app.setOrganizationDomain("plankton-toolbox.org")
    app.setApplicationName("Plankton Toolbox")

    # Windows only (needed for application icon):
    try:
        if sys.platform.startswith("win"):
            import ctypes

            myappid = "plankton-toolbox"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass
    # Create directory with icon.
    icon_path = pathlib.Path("plankton_toolbox_data/img/plankton_toolbox_icon.png")
    if not icon_path.exists():
        if not icon_path.parents[0].exists():
            icon_path.parents[0].mkdir(parents=True)
    #         # Create icon from embedded base64 image.
    #         imgData = base64.b64decode(get_icon_base64()) # TODO:
    #         with icon_path.open('wb') as icon_file:
    #             icon_file.write(imgData)
    #
    app.setWindowIcon(
        QtGui.QIcon("plankton_toolbox_data/img/plankton_toolbox_icon.png")
    )
    # Style, colours, etc.
    app_framework.set_app_style_sheet(app)
    # Create application and start the main event loop.
    window = app_framework.MainWindow()
    window.setVersion(__version__)
    window.initialise()
    #
    window.show()
    sys.exit(app.exec())


# def get_icon_base64():
#     """ """
#     # Note: image_base64 is created by running this code.
#     #     image = open('plankton_toolbox_data/img/plankton_toolbox_icon.png', 'rb')
#     #     image_read = image.read()
#     #     image_64_encode = base64.encodestring(image_read)
#     #     print(image_64_encode)
#     image_base64 = b'<<< TODO >>>'
#     return image_base64


def set_version(version):
    """ """
    global __version__
    __version__ = version


def get_version():
    """ """
    global __version__
    return __version__
