#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import operator

from plankton_core.species import Species


class CreateReportStandard(object):
    """ """

    def __init__(self):
        """ """
        # Initialize parent.
        super(CreateReportStandard, self).__init__()
        #
        self.taxon_cache = {}
        #
        self._header_items = [
            "visit_year",
            "sample_date",
            "sample_time",
            "visit_month",
            "station_name",
            "station_code",
            "sample_latitude_dd",
            "sample_longitude_dd",
            "water_depth_m",
            "sample_id",
            "sample_min_depth_m",
            "sample_max_depth_m",
            "scientific_name",
            "species_flag_code",
            "cf",
            "size_class",  #'text',
            "trophic_type",
            "parameter",
            "value",
            "unit",
            "plankton_group",
            "taxon_kingdom",
            "taxon_phylum",
            "taxon_class",
            "taxon_order",
            "taxon_family",
            "taxon_genus",
            "taxon_species",
            "rank",
            #             'taxon_hierarchy',
            "sampling_laboratory",
            "analytical_laboratory",
            "analysed_by",
        ]

    def create_report(self, datasets, result_table, aggregate_rows=False):
        """
        Note:
        - Datasets must be of the format used in the modules dataset_tree and datasets_tree.
        - The result_table object must contain self._header = [] and self._rows = [].
        """
        # Check indata.
        if datasets == None:
            raise UserWarning("Datasets are missing.")
        if result_table == None:
            raise UserWarning("Result table is missing.")
        # Set header.
        result_table.set_header(self._header_items)

        # Iterate through datasets.
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        datadict = {}
                        datadict.update(datasetnode.get_data_dict())
                        datadict.update(visitnode.get_data_dict())
                        datadict.update(samplenode.get_data_dict())
                        datadict.update(variablenode.get_data_dict())
                        #
                        self.add_taxon_related_info(datadict)
                        #
                        report_row = []
                        #
                        for item in self._header_items:
                            report_row.append(datadict.get(item, ""))
                        #
                        result_table.append_row(report_row)

        # Sort order: Station, date, min depth, max depth, scientific name, size.
        result_table.get_rows().sort(key=operator.itemgetter(3, 1, 9, 10, 11, 13))

    def add_taxon_related_info(self, datadict):
        """ """
        taxa = datadict.get("scientific_name", "")

        datadict["plankton_group"] = Species().get_plankton_group_from_taxon_name(taxa)

        if taxa:
            taxon_dict = Species().get_taxon_dict(taxa)

            for taxon_key in [
                "taxon_species",
                "taxon_genus",
                "taxon_family",
                "taxon_order",
                "taxon_class",
                "taxon_phylum",
                "taxon_kingdom",
                "rank",
            ]:

                value = taxon_dict.get(taxon_key, "")
                if value:
                    datadict[taxon_key] = value
