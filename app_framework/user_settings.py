#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import platform
import toolbox_utils


@toolbox_utils.singleton
class ToolboxUserSettings:
    """Used for specific user settings."""

    def __init__(self):
        """ """
        self.clear()
        self.user_settings_loaded = False

    def clear(self):
        """ """
        # Default values.
        self.path_to_plankton_toolbox_data = "plankton_toolbox_data"
        self.path_to_plankton_toolbox_counter = "plankton_toolbox_counter"

    def home_for_mac(self):
        """ """
        if platform.system() == "Darwin": 
            return pathlib.Path.home()
        return "."

    def get_path_to_plankton_toolbox_data(self):
        """ """
        if not self.user_settings_loaded:
            self.load_user_settings()
        # Extra check for macOS. Can't be located inside App content folder.
        if platform.system() == "Darwin": 
            if self.path_to_plankton_toolbox_data == "plankton_toolbox_data":
                return str(pathlib.Path(self.home_for_mac(), "plankton_toolbox_data"))
        # Normal response.
        return self.path_to_plankton_toolbox_data

    def get_path_to_plankton_toolbox_counter(self):
        """ """
        if not self.user_settings_loaded:
            self.load_user_settings()
        # Extra check for macOS. Can't be located inside App content folder.
        if platform.system() == "Darwin": 
            if self.path_to_plankton_toolbox_data == "plankton_toolbox_counter":
                return str(pathlib.Path(self.home_for_mac(), "plankton_toolbox_counter"))
        # Normal response.
        return self.path_to_plankton_toolbox_counter

    def load_user_settings(self):
        """ """
        self.user_settings_loaded = True
        settings_dir_path = pathlib.Path(self.home_for_mac(), "plankton_toolbox_data")
        # Check if plankton_toolbox_data exists.
        if not settings_dir_path.exists():
            settings_dir_path.mkdir(parents=True)
        # Check if the user settings file exists.
        settings_file_path = pathlib.Path(settings_dir_path, "user_settings.txt")
        if settings_file_path.exists():
            # Read settings.
            with settings_file_path.open("r", encoding="cp1252") as settings_file:
                for row in settings_file:
                    try:
                        parts = row.split(":", 1)  # Split in first ':'.
                        if len(parts) > 1:
                            if row.startswith("path_to_plankton_toolbox_data:"):
                                self.path_to_plankton_toolbox_data = str(
                                    pathlib.Path(parts[1].strip())
                                )
                            if row.startswith("path_to_plankton_toolbox_counter:"):
                                self.path_to_plankton_toolbox_counter = str(
                                    pathlib.Path(parts[1].strip())
                                )
                    except Exception as e:
                        print("DEBUG: Exception", e)
        else:
            # Write default values to file.
            with settings_file_path.open("w", encoding="cp1252") as settings_file:
                settings_file.write("# User settings for Plankton Toolbox.\n")
                settings_file.write("\n")
                settings_file.write(
                    "path_to_plankton_toolbox_data: "
                    + self.get_path_to_plankton_toolbox_data()
                    + "\n"
                )
                settings_file.write(
                    "path_to_plankton_toolbox_counter: "
                    + self.get_path_to_plankton_toolbox_counter()
                    + "\n"
                )
