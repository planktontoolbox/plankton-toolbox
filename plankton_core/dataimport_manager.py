#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import toolbox_utils
import plankton_core


@toolbox_utils.singleton
class DataImportManager(object):
    """ """

    def __init__(self):
        """ """

    def import_dataset_file(
        self,
        filename=None,
        dataset_name=None,
        sample_name=None,
        import_format=None,
        update_trophic_type=False,
    ):
        """ """
        datasettopnode = plankton_core.DatasetNode()
        #
        if import_format == "SHARKweb":
            self._import_sharkweb_file(datasettopnode, filename, update_trophic_type)
        #         if import_format == 'PhytoWin':
        #             self._import_phytowin_file(datasettopnode, filename)
        if import_format == "PlanktonCounter":
            self._import_plankton_counter_sample(
                datasettopnode, dataset_name, sample_name, update_trophic_type
            )
        #
        if import_format == "PlanktonCounterExcel":
            self._import_plankton_counter_sample_from_excel(
                datasettopnode, filename, update_trophic_type
            )
        #
        if datasettopnode:
            plankton_core.Datasets().add_dataset(datasettopnode)
        #
        return datasettopnode

    def _import_sharkweb_file(self, dataset_top_node, file_name, update_trophic_type):
        """ """
        # Create dataset from file content.
        sharkweb = plankton_core.ImportSharkWeb()
        sharkweb.read_file(file_name)
        sharkweb.create_tree_dataset(dataset_top_node, update_trophic_type)

        # Add export info to dataset.
        columnsinfo = sharkweb.create_export_table_info()
        dataset_top_node.set_export_table_columns(columnsinfo)

    #     def _import_phytowin_file(self, dataset_top_node, file_name):
    #         """ """
    #         # Create dataset from file content.
    #         phytowin = plankton_core.ImportPhytowin()
    #         phytowin.read_file(file_name)
    #         phytowin.create_tree_dataset(dataset_top_node)
    #         # If older names and sizes are used.
    #         phytowin.update_species_and_sizes(dataset_top_node)
    #
    #         # Add export info to dataset.
    #         columnsinfo = phytowin.create_export_table_info()
    #         dataset_top_node.set_export_table_columns(columnsinfo)

    def _import_plankton_counter_sample(
        self, dataset_top_node, dataset_name, sample_name, update_trophic_type
    ):
        """ """
        # Create dataset from file content.
        counter = plankton_core.ImportPlanktonCounter()
        counter.read_file(dataset_name, sample_name)
        counter.create_tree_dataset(dataset_top_node, update_trophic_type)

        # Add export info to dataset.
        columnsinfo = counter.create_export_table_info()
        dataset_top_node.set_export_table_columns(columnsinfo)

    def _import_plankton_counter_sample_from_excel(
        self, dataset_top_node, excel_file_path, update_trophic_type
    ):
        """ """
        # Create dataset from file content.
        counter = plankton_core.ImportPlanktonCounter()
        counter.read_excel_file(excel_file_path)
        counter.create_tree_dataset(dataset_top_node, update_trophic_type)

        # Add export info to dataset.
        columnsinfo = counter.create_export_table_info()
        dataset_top_node.set_export_table_columns(columnsinfo)
