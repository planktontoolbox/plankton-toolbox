#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import plankton_core


class CreateReportCounted(object):
    """ """

    def __init__(self):
        """ """
        # Initialize parent.
        super(CreateReportCounted, self).__init__()
        #
        self._header_items = [
            "station_name",
            "station_code",
            "sample_date",
            "analysis_date",
            "sample_min_depth_m",
            "sample_max_depth_m",
            "taxon_class",
            "scientific_name",
            "species_flag_code",
            "cf",
            "scientific_authority",
            "trophic_type",
            "harmful",
            "param_abundance",
            "analytical_laboratory",
            "analysed_by",
            "size_class",
            "param_biovolume",
        ]

        self._translate_header = {
            "station_name": "Station name",  # 'Station', # 0
            "station_code": "Station code",  # 'Station', # 0
            "sample_date": "Sample date",  # 'Provtagningsdatum', # 1
            "analysis_date": "Analysis date",  # 'Analysdatum', # 2
            "sample_min_depth_m": "Min depth (m)",  # 'Min djup', # 3
            "sample_max_depth_m": "Max depth (m)",  # 'Max djup', # 4
            "taxon_class": "Class",  # 'Klass', # 5
            "scientific_name": "Scientific name",  # 'Art/Taxonomisk enhet', # 6
            "species_flag_code": "Species flag code",  # 'Sflag', # 7
            "cf": "Cf",  # 'Sflag', # 7
            "scientific_authority": "Authority",  # 'Author', # 8
            "trophic_type": "Trophic type",  # 'Trofigrad', # 9
            "harmful": "Pot. toxic",  # 'Potentiellt giftig', # 10
            "param_abundance": "Abundance",  # 'Celler/l', # 11
            "analytical_laboratory": "Analytical laboratory",  # 'Analys laboratorium', # 13
            "analysed_by": "Analysed by",  # 'Mikroskopist', # 14
            "size_class": "Size class",  # 'Storleksklass (PEG)' # 15
            "param_biovolume": "Biovolume (mm3/L)",  # 'Biovolym (mm3/L)', # 12
        }

        # Used as row key and for sort order.
        self._row_key_items = [
            "station_name",
            "station_code",
            "sample_date",
            "sample_min_depth_m",
            "sample_max_depth_m",
            "scientific_name",
            "species_flag_code",
            "cf",
            "trophic_type",
            "size_class",
        ]

        # Used as key for aggregated rows.
        self._row_key_aggregated_items = [
            "station_name",
            "station_code",
            "sample_date",
            "sample_min_depth_m",
            "sample_max_depth_m",
            "scientific_name",
            "species_flag_code",
            "cf",
            "trophic_type",
            # 'size_class',
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

            result_table.set_header(self._header_counted_items)
        # Set header.
        translated_header = []
        for item in self._header_items:
            if aggregate_rows and (item == "size_class"):
                translated_header.append("")
            else:
                translated_header.append(self._translate_header.get(item, item))
        #
        result_table.set_header(translated_header)

        # Iterate through datasets.
        report_rows_dict = {}
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        row_dict = {}
                        row_dict.update(datasetnode.get_data_dict())
                        row_dict.update(visitnode.get_data_dict())
                        row_dict.update(samplenode.get_data_dict())
                        row_dict.update(variablenode.get_data_dict())
                        #
                        parameter = row_dict.get("parameter", "")
                        if parameter in ["Abundance", "Biovolume concentration"]:
                            # Create key:
                            row_key = ""
                            for item in self._row_key_items:
                                if row_key:
                                    row_key += "<+>"
                                try:
                                    row_key += str(row_dict.get(item, ""))
                                except:
                                    pass
                            # Add to dict if first time.
                            if row_key not in report_rows_dict:
                                report_rows_dict[row_key] = row_dict
                            # Parameters as columns.
                            if parameter == "Abundance":
                                report_rows_dict[row_key][
                                    "param_abundance"
                                ] = row_dict.get("value", "")
                            if parameter == "Biovolume concentration":
                                report_rows_dict[row_key][
                                    "param_biovolume"
                                ] = row_dict.get("value", "")
                            # Complement columns.
                            self._add_more_content(row_dict)

        #
        if not aggregate_rows:
            # Not aggregated.
            sorted_key_list = sorted(report_rows_dict.keys())
            for key in sorted_key_list:
                # Copy items.
                report_row = []
                row_dict = report_rows_dict[key]
                for item in self._header_items:
                    report_row.append(row_dict.get(item, ""))
                #
                result_table.append_row(report_row)

        else:
            # Aggregated.
            # Add calculated valuse for aggregated rows.
            report_aggregated_rows_dict = {}
            for key in report_rows_dict.keys():
                row_dict = report_rows_dict[key]
                # Create aggregated key:
                agg_row_key = ""
                for item in self._row_key_aggregated_items:
                    if agg_row_key:
                        agg_row_key += "<+>"
                    try:
                        agg_row_key += str(row_dict.get(item, ""))
                    except:
                        pass

                if agg_row_key not in report_aggregated_rows_dict:
                    report_aggregated_rows_dict[agg_row_key] = row_dict.copy()
                else:
                    try:
                        old_abundance_value = report_aggregated_rows_dict[
                            agg_row_key
                        ].get("param_abundance", "<invalid>")
                        new_abundance_value = row_dict.get(
                            "param_abundance", "<invalid>"
                        )
                        abundance_value = float(old_abundance_value) + float(
                            new_abundance_value
                        )
                        report_aggregated_rows_dict[agg_row_key][
                            "param_abundance"
                        ] = str(abundance_value)
                    except:
                        report_aggregated_rows_dict[agg_row_key][
                            "param_abundance"
                        ] = "<invalid>"
                    #
                    try:
                        old_biovolume_value = report_aggregated_rows_dict[
                            agg_row_key
                        ].get("param_biovolume", "<invalid>")
                        new_biovolume_value = row_dict.get(
                            "param_biovolume", "<invalid>"
                        )
                        biovolume_value = float(old_biovolume_value) + float(
                            new_biovolume_value
                        )
                        report_aggregated_rows_dict[agg_row_key][
                            "param_biovolume"
                        ] = str(biovolume_value)
                    except:
                        report_aggregated_rows_dict[agg_row_key][
                            "param_biovolume"
                        ] = "<invalid>"
            #
            sorted_key_list = sorted(report_aggregated_rows_dict.keys())
            for key in sorted_key_list:
                # Copy items.
                report_row = []
                row_dict = report_aggregated_rows_dict[key]
                for item in self._header_items:
                    value = row_dict.get(item, "")
                    if (value == "<invalid>") or (item == "size_class"):
                        report_row.append("")
                    else:
                        report_row.append(value)
                #
                result_table.append_row(report_row)

    def _add_more_content(self, row_dict):
        """ """
        scientific_name = row_dict.get("scientific_name", "")
        scientific_authority = plankton_core.Species().get_taxon_value(
            scientific_name, "author"
        )
        row_dict["scientific_authority"] = scientific_authority
        harmful = plankton_core.Species().get_taxon_value(scientific_name, "harmful")
        row_dict["harmful"] = "X" if harmful else ""
