#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import dateutil.parser

import toolbox_utils
import plankton_core


class ParsedFormat(plankton_core.FormatBase):
    """ """

    def __init__(self):
        """Abstract class for parsed import formats."""
        super(ParsedFormat, self).__init__()
        #
        self._parsercommands = []

    def replace_method_keywords(self, parse_command, node_level=None, view_format=None):
        """Mapping between Excel parser code and python code."""
        command = str(parse_command.strip())
        #
        if "Column:" in command:
            # An easier notation for "$Text('Example column')": "Column:Example column".
            # For simple column name mapping based on the format column.
            command = str(command.replace("Column:", "").strip())
            if view_format is None:
                command = 'self._as_text("' + command + '")'
            elif view_format == "text":
                command = 'self._as_text("' + command + '")'
            elif view_format == "integer":
                command = 'self._as_integer("' + command + '")'
            elif view_format == "float":
                command = 'self._as_float("' + command + '")'
            elif view_format == "sample_date":
                command = 'self._as_date("' + command + '")'
            else:
                command = 'self._as_text("' + command + '")'
        #
        elif "$" in command:
            # Mapping for more advanced alternatives.
            command = command.replace("$Text(", "self._as_text(")
            command = command.replace("$Integer(", "self._as_integer(")
            command = command.replace("$Float(", "self._as_float(")
            command = command.replace("$Date(", "self._as_date(")
            command = command.replace("$GetTaxonInfo(", "self._taxon_info_by_key(")
            command = command.replace(
                "$GetSizeClassInfo(", "self._get_sizeclass_info_by_key("
            )
            command = command.replace(
                "$GetSizeclassInfo(", "self._get_sizeclass_info_by_key("
            )  # Alternative spelling.
            command = command.replace("$GetTrophicType(", "self._get_trophic_type(")
            command = command.replace("$GetPlanktonGroup(", "self._get_plankton_group(")
        #         else:
        #             # For hard-coded values.
        #             command = ''' + str(command.strip()) + ''"

        #
        if node_level == "function_sample":
            command = command.replace(
                "$CreateVariable(", "self._create_variable(currentsample, "
            )
        if node_level == "function_variable":
            command = command.replace(
                "$CopyVariable(", "self._copy_variable(currentvariable, "
            )
        ### TODO: Also replace:
        # $Text(   --> self._as_text(
        # $Year(   --> self._asYear(
        # $Datetime(   --> self._asDatetime(
        # $Date(   --> self._as_date(
        # $Time(   --> self._asTime(
        # $Int(   --> self._asInt(
        # $Float(   --> self._as_float(
        # $Position(   --> self._asPosition(
        # $Station(   --> self._asStation(
        # $Param(   --> self._asParam(
        #
        return command

    def append_parser_command(self, command_string):
        """ """
        commanddict = {}
        commanddict["command_string"] = command_string
        commanddict["command"] = compile(command_string, "", "exec")

        # For development:
        print("Parser command: " + command_string)

        self._parsercommands.append(commanddict)

    def _as_text(self, column_name):
        """To be called from Excel-based parser."""
        column_name = str(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            return self._row[index] if len(self._row) > index else ""
        else:
            return ""

    def _as_integer(self, column_name):
        """To be called from Excel-based parser."""
        column_name = str(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(" ", "").replace(",", ".")
                        return int(round(float(value)))
                except:
                    toolbox_utils.Logging().warning(
                        "Parser: Failed to convert to integer: " + self._row[index]
                    )
                    return self._row[index]
        return ""

    def _as_float(self, column_name):
        """To be called from Excel-based parser."""
        column_name = str(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(" ", "").replace(",", ".")
                        return float(value)
                except:
                    toolbox_utils.Logging().warning(
                        "Parser: Failed to convert to float: " + self._row[index]
                    )
                    return self._row[index]
        return ""

    def _as_date(self, column_name):
        """Reformat to match the ISO format. (2000-01-01)
        To be called from Excel-based parser."""
        column_name = str(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = dateutil.parser.parse(self._row[index])
                    if value:
                        return value.strftime("%Y-%m-%d")
                except:
                    toolbox_utils.Logging().warning(
                        "Parser: Failed to convert to date: " + self._row[index]
                    )
                    return self._row[index]
        return ""

    def _get_taxon_info_by_key(self, scientific_name, key):
        """To be called from Excel-based parser."""
        scientific_name = str(scientific_name)
        key = str(key)
        return plankton_core.Species().get_taxon_value(scientific_name, key)

    def _get_sizeclass_info_by_key(self, scientific_name, size_class, key):
        """To be called from Excel-based parser."""
        scientific_name = str(scientific_name)
        key = str(key)
        size_class = str(size_class)
        value = plankton_core.Species().get_bvol_value(scientific_name, size_class, key)
        if value:
            return value
        return ""

    def _get_trophic_type(self, scientific_name, size_class, reported_trophic_type=""):
        """To be called from Excel-based parser."""
        scientific_name = str(scientific_name)
        size_class = str(size_class)
        reported_trophic_type = str(reported_trophic_type)
        value = plankton_core.Species().get_bvol_value(
            scientific_name, size_class, "trophic_type"
        )
        if not value:
            value = plankton_core.Species().get_taxon_value(
                scientific_name, "trophic_type"
            )
        if not value:
            value = reported_trophic_type
        #
        return value

    def _get_plankton_group(self, scientific_name):
        """To be called from Excel-based parser."""
        scientific_name = str(scientific_name)
        return plankton_core.Species().get_plankton_group_from_taxon_name(
            scientific_name
        )

    def _to_station(self, current_node, station_name, **kwargs):
        """To be called from Excel-based parser."""
        # TODO: For test:
        station_name = str(station_name)
        current_node.add_data("station_name", station_name)

    def _to_position(self, current_node, latitude, longitude, **kwargs):
        """To be called from Excel-based parser."""
        latitude = str(latitude)
        longitude = str(longitude)

    #        print('DEBUG: _to_position: ' + latitude + ' ' + longitude)

    def _create_variable(self, current_node, **kwargs):
        """To be called from Excel-based parser."""
        if isinstance(current_node, plankton_core.VisitNode):
            newsample = plankton_core.SampleNode()
            current_node.add_child(newsample)
            variable = plankton_core.VariableNode()
            newsample.add_child(variable)
            variable.add_data("parameter", kwargs["p"])
            variable.add_data("value", kwargs["v"])
            # variable.add_data('value_float', kwargs['v'])
            variable.add_data("unit", kwargs["u"])
        if isinstance(current_node, plankton_core.SampleNode):
            variable = plankton_core.VariableNode()
            current_node.add_child(variable)
            variable.add_data("parameter", kwargs["p"])
            variable.add_data("value", kwargs["v"])
            # variable.add_data('value_float', kwargs['v'])
            variable.add_data("unit", kwargs["u"])

    def _copy_variable(self, current_node, **kwargs):
        """To be called from Excel-based parser."""
        if isinstance(current_node, plankton_core.VariableNode):
            variable = current_node.clone()
            variable.add_data("parameter", kwargs["p"])
            variable.add_data("value", kwargs["v"])
            # variable.add_data('value_float', kwargs['v'])
            variable.add_data("unit", kwargs["u"])

    def _modify_variable(self, current_node, **kwargs):
        """To be called from Excel-based parser."""
        if isinstance(current_node, plankton_core.VariableNode):
            current_node.add_data("parameter", kwargs["p"])
            current_node.add_data("value", kwargs["v"])
            # current_node.add_data('value_float', kwargs['v'])
            current_node.add_data("unit", kwargs["u"])
