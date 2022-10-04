#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import toolbox_utils
import plankton_core


class FormatSingleFile(plankton_core.ParsedFormat):
    """Import format for single file."""

    def __init__(self):
        """Import format for single file."""
        super(FormatSingleFile, self).__init__()

    def parse_table_dataset(self, dataset, imported_table):
        """ """
        self._dataset = dataset
        #
        datasetparserrows = dataset.get_dataset_parser_rows()
        #
        #         visitkeycommand = None
        #         samplekeycommand = None
        #         variablekeycommand = None
        self.visit_key_parts = None
        self.sample_key_parts = None

        #
        try:
            for parserrow in datasetparserrows:
                parsernode = parserrow.get("node", "")
                parserkey = parserrow.get("key", "")
                view_format = parserrow.get("view_format", "")
                parsercommand = parserrow.get("command", "")
                if parsercommand:
                    #
                    parsercommand = str(
                        self.replace_method_keywords(
                            parsercommand, parsernode, view_format
                        )
                    )
                    #
                    if parsernode == "dataset":
                        commandstring = (
                            'dataset.add_data("'
                            + parserkey
                            + '", '
                            + parsercommand
                            + ")"
                        )
                        self.append_parser_command(commandstring)
                    if parsernode == "visit":
                        commandstring = (
                            'currentvisit.add_data("'
                            + parserkey
                            + '", '
                            + parsercommand
                            + ")"
                        )
                        self.append_parser_command(commandstring)
                    elif parsernode == "sample":
                        commandstring = (
                            'currentsample.add_data("'
                            + parserkey
                            + '", '
                            + parsercommand
                            + ")"
                        )
                        self.append_parser_command(commandstring)
                    elif parsernode == "variable":
                        commandstring = (
                            'currentvariable.add_data("'
                            + parserkey
                            + '", '
                            + parsercommand
                            + ")"
                        )
                        self.append_parser_command(commandstring)
                    #
                    elif (parsernode == "info") and (parserkey == "visit_key"):
                        self.visit_key_parts = "self.visit_keystring = " + parsercommand
                    elif (parsernode == "info") and (parserkey == "sample_key"):
                        self.sample_key_parts = (
                            "self.sample_keystring = " + parsercommand
                        )
                    #
                    elif parsernode == "function_dataset":
                        commandstring = parserkey + parsercommand
                        self.append_parser_command(commandstring)
                    elif parsernode == "function_visit":
                        commandstring = parserkey + parsercommand
                        self.append_parser_command(commandstring)
                    elif parsernode == "function_sample":
                        commandstring = parserkey + parsercommand
                        self.append_parser_command(commandstring)
                    elif parsernode == "function_variable":
                        commandstring = parserkey + parsercommand
                        self.append_parser_command(commandstring)

        except Exception as e:
            toolbox_utils.Logging().warning(
                "Failed to parse dataset: %s" % (e.args[0])
                + "- Command string: %s" % (commandstring)
            )
            pass  ### raise
        #
        try:
            # Base class must know header for _asText(), etc.
            self._set_header(imported_table.get_header())
            # Iterate over rows in imported_table.
            for row in imported_table.get_rows():
                # Current row to base class.
                self._set_row(row)
                # === Get or create nodes. ===
                currentvisit = None
                currentsample = None
                currentvariable = None
                # Check if visit exists. Create or reuse.
                self.visit_keystring = None
                exec(self.visit_key_parts)  # Command assigns keystring.
                currentvisit = dataset.get_visit_lookup(self.visit_keystring)
                if not currentvisit:
                    currentvisit = plankton_core.VisitNode()
                    dataset.add_child(currentvisit)
                    currentvisit.set_id_string(self.visit_keystring)
                # Check if sample exists. Create or reuse.
                self.sample_keystring = None
                exec(self.sample_key_parts)  # Command assigns keystring.
                currentsample = dataset.get_sample_lookup(self.sample_keystring)
                if not currentsample:
                    currentsample = plankton_core.SampleNode()
                    currentvisit.add_child(currentsample)
                    currentsample.set_id_string(self.sample_keystring)
                # Add all variables in row.
                currentvariable = plankton_core.VariableNode()
                currentsample.add_child(currentvariable)
                # === Parse row and add fields on nodes. ===

                for cmd in self._parsercommands:
                    try:
                        exec(cmd["command"])

                    except Exception as e:
                        toolbox_utils.Logging().warning(
                            "Failed to parse command: %s" % (e.args[0])
                            + "- Command string: %s" % (cmd["command_string"])
                        )
        #
        except Exception as e:
            toolbox_utils.Logging().warning("Failed to parse dataset: %s" % (e.args[0]))
