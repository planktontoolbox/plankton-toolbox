#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import os
import sys
import shutil
import math

# from PyQt6 import QtGui
# from PyQt6 import QtWidgets
# from PyQt6 import QtCore

# import openpyxl
import xlsxwriter
import operator
from PyQt6 import QtCore
import toolbox_utils
import app_framework
import plankton_core


@toolbox_utils.singleton
class PlanktonCounterManager(QtCore.QObject):
    """ """

    planktonCounterListChanged = QtCore.pyqtSignal()

    def __init__(self):
        """ """
        QtCore.QObject.__init__(self)
        #
        plankton_toolbox_counter_path = (
            app_framework.ToolboxUserSettings().get_path_to_plankton_toolbox_counter()
        )
        self._dataset_dir_path = str(
            pathlib.Path(plankton_toolbox_counter_path, "datasets")
        )

        # Check if exists. Create if not.
        if (self._dataset_dir_path) and (
            not pathlib.Path(self._dataset_dir_path).exists()
        ):
            try:
                pathlib.Path(self._dataset_dir_path).mkdir(parents=True)
            except Exception as e:
                raise UserWarning(
                    "Can't create directories in path. Path: "
                    + str(self._dataset_dir_path)
                    + ". Exception: "
                    + str(e)
                )
        #

    def _emit_change_notification(self):
        """Emit signal to update GUI lists for available datasets and samples."""
        self.planktonCounterListChanged.emit()

    # === Datasets ===

    def get_dataset_dir_path(self):
        """ """
        return self._dataset_dir_path

    def get_dataset_names(self):
        """Returns a list with available datasets."""
        datasetnames = []
        if (self._dataset_dir_path) and (pathlib.Path(self._dataset_dir_path).exists()):
            for datasetdir in os.listdir(self._dataset_dir_path):
                if pathlib.Path(self._dataset_dir_path, datasetdir).is_dir():
                    datasetnames.append(datasetdir)
            return sorted(datasetnames)
        else:
            raise UserWarning(
                "The directory " + str(self._dataset_dir_path) + " does not exists."
            )

    def create_dataset(self, dataset_name):
        """Creates a new dataset (= a new directory)."""
        path = pathlib.Path(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if (path) and (not path.exists()):
            try:
                path.mkdir(parents=True)
            except Exception as e:
                raise UserWarning(
                    "Can't create directories in path. Path: "
                    + str(path)
                    + ". Exception: "
                    + str(e)
                )
        else:
            raise UserWarning(
                "Dataset already exists, create failed. Dataset name: "
                + str(dataset_name)
            )
        #
        self._emit_change_notification()

    def delete_dataset(self, dataset_name):
        """Deletes a dataset (the directory and all its content.)"""
        path = pathlib.Path(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if path and path.exists():
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise UserWarning(
                    "Can't delete directory. Path: "
                    + str(path)
                    + ". Exception: "
                    + str(e)
                )
        else:
            raise UserWarning(
                "Dataset did not exist, delete failed. Dataset name: "
                + str(dataset_name)
            )
        #
        self._emit_change_notification()

    # === Samples ===

    def get_sample_names(self, dataset_name):
        """Returns a list with available samples within a dataset."""
        samplenames = []
        path = pathlib.Path(self._dataset_dir_path, dataset_name)
        # Check if exists.
        if (path) and (path.exists()):
            for sampledir in os.listdir(path):
                if pathlib.Path(path, sampledir).is_dir():
                    samplenames.append(sampledir)
            return sorted(samplenames)
        else:
            raise UserWarning(
                "Dataset does not exist. Dataset name: " + str(dataset_name)
            )

    def create_sample(self, dataset_name, sample_name):
        """Creates a new sample (= a new directory in the dataset directory)."""
        if not dataset_name:
            dataset_name = "Default-dataset"
        if not sample_name:
            raise UserWarning("Can't create sample. Sample name is missing.")
        #
        path = pathlib.Path(self._dataset_dir_path, dataset_name, sample_name)
        # Check if exists.
        if (path) and (not path.exists()):
            try:
                path.mkdir(parents=True)
            #                 print('Directories created for this path: ' + path)
            except Exception as e:
                raise UserWarning(
                    "Can't create directories in path. Path: "
                    + str(path)
                    + ". Exception: "
                    + str(e)
                )
        else:
            raise UserWarning(
                "Sample already exists, create failed. Dataset name: "
                + str(dataset_name)
            )
        #
        self._emit_change_notification()

    def delete_sample(self, dataset_name, sample_name):
        """Deletes a sample (the directory and all its content.)"""
        path = pathlib.Path(self._dataset_dir_path, dataset_name, sample_name)
        # Check if exists.
        if path and path.exists():
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise UserWarning(
                    "Can't delete sample. Path: " + str(path) + ". Exception: " + str(e)
                )
        else:
            raise UserWarning(
                "Sample does not exist, delete failed. Sample name: " + str(sample_name)
            )
        #
        self._emit_change_notification()

    def rename_sample(self, dataset_name, old_sample_name, new_sample_name):
        """Renames a sample."""
        path = pathlib.Path(self._dataset_dir_path, dataset_name, old_sample_name)
        new_path = pathlib.Path(self._dataset_dir_path, dataset_name, new_sample_name)
        # Check if exists.
        if path and path.exists():
            try:
                shutil.move(path, new_path)
            except Exception as e:
                raise UserWarning(
                    "Can't rename sample. Path: " + str(path) + ". Exception: " + str(e)
                )
        else:
            raise UserWarning(
                "Sample does not exist, rename failed. Dataset name: "
                + str(old_sample_name)
            )
        #
        self._emit_change_notification()

    # === Dataset metadata ===

    def load_dataset_metadata(self, dataset_name):
        """ """
        path = pathlib.Path(self._dataset_dir_path, dataset_name)
        tablefilereader = toolbox_utils.TableFileReader(
            file_path=path,
            text_file_name="dataset_metadata.txt",
        )
        # Merge header and rows.
        self._current_dataset_metadata = [
            tablefilereader.header()
        ] + tablefilereader.rows()

    #         print('Dataset metadata: ' + str(self._current_dataset_metadata))

    def write_dataset_metadata(self, dataset_name):
        """ """
        raise UserWarning("Method: write_dataset_metadata(). Not implemented yet.")

    #     # === Sampling info ===
    #
    #     def load_sampling_info(self, dataset_name):
    #         """ """
    #         path = pathlib.Path(self._dataset_dir_path, dataset_name)
    #         tablefilereader = toolbox_utils.TableFileReader(
    #                     file_path = path,
    #                     text_file_name = 'sampling_info.txt',
    #                     )
    #         # Merge header and rows.
    #         self._current_sampling_info = [tablefilereader.header()] + tablefilereader.rows()
    # #         print('Sampling info: ' + str(self._current_sampling_info))

    # === Import/Export ===

    def import_dataset(self, source_path, source_file_name, dataset_name):
        """ """
        raise UserWarning("Method: import_dataset(). Not implemented yet.")

    def export_dataset(self, dataset_name, target_path, target_file_name):
        """ """
        raise UserWarning("Method: export_dataset(). Not implemented yet.")

    def import_orderer_info(self, source_path, source_file_name, dataset_name):
        """ """
        raise UserWarning("Method: import_orderer_info(). Not implemented yet.")

    def import_sampling_info(self, source_path, source_file_name, dataset_name):
        """ """
        raise UserWarning("Method: import_sampling_info(). Not implemented yet.")


class PlanktonCounterSample:
    """Manager for rows in sample."""

    def __init__(
        self,
        dataset_dir_path=None,
        dataset_name=None,
        sample_name=None,
    ):
        """ """
        self._dataset_dir_path = dataset_dir_path
        self._dataset_name = dataset_name
        self._sample_name = sample_name
        #
        self._sample_info_dict = {}  # <key>: <value>
        self._sample_rows = {}  # <row_key>: <SampleRow-object>
        self._sample_header = [
            "scientific_full_name",
            "taxon_class",
            "scientific_name",
            "size_class",
            "method_step",
            "count_area_number",
            "locked_at_area",
            "counted_units",
            "counted_units_list",
            "abundance_class",
            "coefficient",
            "abundance_units_l",
            "volume_mm3_l",
            "carbon_ugc_l",
            "volume_um3_unit",
            "carbon_pgc_unit",
            "variable_comment",
            "trophic_type",
            "unit_type",
            "species_flag_code",
            "cf",
            "bvol_list",
            "bvol_list_calc",
        ]

        # Create file writers.
        if not self._dataset_name:
            self._dataset_name = "Default-dataset"
        #
        path = pathlib.Path(
            self._dataset_dir_path, self._dataset_name, self._sample_name
        )
        self._tablefilewriter_sample_data = toolbox_utils.TableFileWriter(
            file_path=path,
            text_file_name="sample_data.txt",
        )
        self._tablefilewriter_sample_info = toolbox_utils.TableFileWriter(
            file_path=path,
            text_file_name="sample_info.txt",
        )
        # Load from file.
        self.load_sample_info()
        self.load_sample_data()

    def get_dir_path(self):
        """ """
        return pathlib.Path(
            self._dataset_dir_path, self._dataset_name, self._sample_name
        )

    def clear(self):
        """ """
        self._sample_rows = {}  # <row_key>: <CounterRow-object>

    def get_sample_info(self):
        """ """
        return self._sample_info_dict

    def set_sample_info(self, sample_info_dict):
        """ """
        self._sample_info_dict = sample_info_dict

    def save_sample_info(self):
        """ """
        try:
            header = ["key", "value"]
            rows = []
            for key in sorted(self._sample_info_dict.keys()):
                rows.append([key, self._sample_info_dict[key]])
            #
            self._tablefilewriter_sample_info.write_file(header, rows)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_sample_info(self, info_dict):
        """ """
        try:
            for key in info_dict.keys():
                self._sample_info_dict[key] = info_dict[key]
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def load_sample_info(self):
        """ """
        try:
            self._sample_info_dict = {}
            #
            if (
                (self._dataset_dir_path is None)
                or (self._dataset_name is None)
                or (self._sample_name is None)
            ):
                raise UserWarning(
                    "Failed to load sample file. Path, dataset name or sample name is missing."
                )
            # Create file if not exists.
            path = pathlib.Path(
                self._dataset_dir_path, self._dataset_name, self._sample_name
            )
            if not pathlib.Path(path, "sample_info.txt").exists():
                header = ["key", "value"]
                self._tablefilewriter_sample_info.write_file(header, [])
            # Read file to dict.
            tablefilereader = toolbox_utils.TableFileReader(
                file_path=path,
                text_file_name="sample_info.txt",
            )
            for row in tablefilereader.rows():
                if len(row) >= 2:
                    key = row[0].strip()
                    value = row[1].strip()
                    self._sample_info_dict[key] = value
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_sample_header_and_rows(self):
        """ """
        try:
            header = self.get_header()
            rows = self.get_rows()
            return header, rows
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_header(self):
        """ """
        return self._sample_header

    def get_rows(self):
        """ """
        try:
            rows = []
            for key in sorted(self._sample_rows.keys()):
                rows.append(
                    self._sample_rows[key].get_row_as_text_list(self._sample_header)
                )
            return rows
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def load_sample_data(self):
        """ """
        try:
            self._sample_rows = {}
            #
            if (
                (self._dataset_dir_path is None)
                or (self._dataset_name is None)
                or (self._sample_name is None)
            ):
                raise UserWarning(
                    "Failed to load sample file. Path, dataset name or sample name is missing."
                )
            # Create file if not exists.
            path = pathlib.Path(
                self._dataset_dir_path, self._dataset_name, self._sample_name
            )
            if not pathlib.Path(path, "sample_data.txt").exists():
                self._tablefilewriter_sample_data.write_file(self._sample_header, [])
            # Read sample data to self._sample_rows.
            tablefilereader = toolbox_utils.TableFileReader(
                file_path=path,
                text_file_name="sample_data.txt",
            )
            self.update_all_sample_rows(
                tablefilereader.header(), tablefilereader.rows()
            )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_all_sample_rows(self, header, rows):
        """ """
        try:
            self._sample_rows = {}
            for row in rows:
                if (len(row) >= 2) and (len(row[0]) >= 0) and (len(row[1]) >= 0):
                    info_dict = dict(zip(header, row))
                    sample_row = SampleRow(info_dict)
                    # Don't save samples without name or counted value = 0.
                    if len(sample_row.get_scientific_name()) > 0:
                        # Quantitative.
                        if sample_row.get_counted_units() > 0:
                            self._sample_rows[sample_row.get_key()] = sample_row
                        # Qualitative.
                        if sample_row.get_abundance_class():
                            self._sample_rows[sample_row.get_key()] = sample_row
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def recalculate_coefficient(self, current_method):
        """ """
        try:
            # Recalculate all rows.
            for sampleobject in self._sample_rows.values():
                # Get coefficient from method.
                method_step = sampleobject.get_method_step()
                method_step_fields = current_method.get_counting_method_step_fields(
                    method_step
                )
                coefficient_one_unit = float(
                    method_step_fields.get("coefficient_one_unit", "0.0")
                )
                # Calculate coefficient for one row.
                count_area_number = int(sampleobject.get_count_area_number())
                locked_at_area = sampleobject.get_locked_at_area()
                ###counted_units_list = sampleobject.get_counted_units_list()
                #
                number_of_areas = count_area_number
                if locked_at_area:
                    number_of_areas = int(locked_at_area)
                #
                #             coefficient = int((coefficient_one_unit / number_of_areas) + 0.5) # Python 2.
                coefficient = round(coefficient_one_unit / number_of_areas, 1)
                sampleobject.set_coefficient(str(coefficient))
                #
                sampleobject._calculate_values()
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def save_sample_data(self):
        """ """
        try:
            rows = []
            for key in sorted(self._sample_rows.keys()):
                rows.append(
                    [
                        "\t".join(
                            self._sample_rows[key].get_row_as_text_list(
                                self._sample_header
                            )
                        )
                    ]
                )
            #
            self._tablefilewriter_sample_data.write_file(self._sample_header, rows)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_taxa_summary(
        self, summary_type=None, most_counted_sorting=False, method_step=None
    ):
        """ """
        try:
            summary_data = []
            #
            totalcounted = 0
            counted_dict = {}
            size_range_dict = {}  # Value for sizeclasses aggregated.
            locked_list = []
            #
            for sampleobject in self._sample_rows.values():
                # Check method step.
                if method_step:
                    if not method_step == sampleobject.get_method_step():
                        continue
                # Count on scientific name. Standard alternative.
                taxon = sampleobject.get_scientific_full_name()
                sort_order = taxon
                size = sampleobject.get_size_class()
                # Use the same key for locked items.
                if sampleobject.is_locked():
                    if size:
                        locked_list.append(taxon + " {" + size + "} ")
                    else:
                        locked_list.append(taxon)
                # Count on class name.
                if summary_type == "Counted per classes":
                    taxon = plankton_core.Species().get_taxon_value(
                        taxon, "taxon_class"
                    )
                    sort_order = taxon
                    if len(taxon) == 0:
                        taxon = "<class unknown>"
                        sort_order = taxon
                # Count on scientific name and size class.
                elif summary_type == "Counted per taxa":
                    if size:
                        taxon = taxon
                        sort_order = taxon
                elif summary_type == "Counted per taxa/sizes":
                    if size:
                        size_for_sorting = f"{taxon} [{float(size):5.0f}]"
                        taxon = taxon + " {" + size + "} "
                        sort_order = size_for_sorting
                # Create in list, first time only.
                if taxon not in counted_dict:
                    counted_dict[taxon] = {}
                    counted_dict[taxon]["counted_units"] = 0
                    counted_dict[taxon]["as_text"] = "0"
                    counted_dict[taxon]["sort_order"] = sort_order
                # Add.
                try:
                    abundance_class = sampleobject.get_abundance_class()
                    if abundance_class in ["", 0]:
                        # Quantitative.
                        counted_dict[taxon]["counted_units"] += int(
                            sampleobject.get_counted_units()
                        )
                        counted_dict[taxon]["as_text"] = str(
                            counted_dict[taxon]["counted_units"]
                        )

                        totalcounted += int(sampleobject.get_counted_units())

                        counted_units_list = sampleobject.get_counted_units_list()
                        if ";" in counted_units_list:
                            last_transect_units = counted_units_list.split(";")[-1]
                            counted_dict[taxon]["as_text"] = (
                                str(counted_dict[taxon]["counted_units"])
                                + "/"
                                + last_transect_units
                            )
                    else:
                        # Qualitative.
                        if summary_type in [
                            "Counted per taxa",
                            "Counted per taxa/sizes",
                        ]:
                            # if counted_dict[taxon] == 0:
                            if counted_dict[taxon]["counted_units"] == 0:
                                if abundance_class == "1":
                                    counted_dict[taxon]["counted_units"] = 1
                                    counted_dict[taxon]["as_text"] = "1=Observed"
                                elif abundance_class == "2":
                                    counted_dict[taxon]["counted_units"] = 2
                                    counted_dict[taxon]["as_text"] = "2=Several cells"
                                elif abundance_class == "3":
                                    counted_dict[taxon]["counted_units"] = 3
                                    counted_dict[taxon]["as_text"] = "3=1-10%"
                                elif abundance_class == "4":
                                    counted_dict[taxon]["counted_units"] = 4
                                    counted_dict[taxon]["as_text"] = "4=10-50%"
                                elif abundance_class == "5":
                                    counted_dict[taxon]["counted_units"] = 5
                                    counted_dict[taxon]["as_text"] = "5=50-100%"
                            else:
                                counted_dict[taxon]["counted_units"] = 1
                                counted_dict[taxon]["as_text"] = "<Qualitative>"
                        else:
                            counted_dict[taxon]["as_text"] = "<Qualitative>"
                except:
                    pass  # If value = ''.
                #
                if summary_type in ["Counted per taxa/sizes"]:
                    bvol_size_range = (
                        plankton_core.Species()
                        .get_bvol_dict(sampleobject.get_scientific_name(), size)
                        .get("bvol_size_range", "")
                    )
                    if bvol_size_range:
                        size_range_dict[taxon] = "(Size: " + bvol_size_range + ")"
            #
            summary_data.append("Total counted: " + str(totalcounted))
            summary_data.append("")
            if most_counted_sorting == False:
                # Alphabetical.
                for key, _value in sorted(
                    counted_dict.items(), key=lambda x: x[1]["sort_order"]
                ):
                    size_range = ""
                    if key in size_range_dict:
                        size_range = "    " + size_range_dict[key]
                    lock_info = ""
                    if key in locked_list:
                        lock_info = " LOCKED"

                    summary_data.append(
                        key
                        + ": "
                        + str(counted_dict[key]["as_text"])
                        + lock_info
                        + size_range
                    )
            else:
                # Sort for most counted.
                for key, _value in sorted(
                    counted_dict.items(),
                    key=lambda x: x[1]["counted_units"],
                    reverse=True,
                ):
                    size_range = ""
                    if key in size_range_dict:
                        size_range = " " + size_range_dict[key]
                    lock_info = ""
                    if key in locked_list:
                        lock_info = " LOCKED"
                    summary_data.append(
                        key
                        + ": "
                        + str(counted_dict[key]["as_text"])
                        + lock_info
                        + size_range
                    )
            #
            return summary_data
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_locked_taxa(self, method_step=None):
        """ """
        try:
            species_locked_list = []
            #
            for sampleobject in self._sample_rows.values():
                # Check method step.
                if method_step:
                    if not method_step == sampleobject.get_method_step():
                        continue
                #
                taxon = sampleobject.get_scientific_full_name()
                size = sampleobject.get_size_class()
                #
                if sampleobject.is_locked():
                    species_locked_list.append([taxon, size, True])
                else:
                    species_locked_list.append([taxon, size, False])
            #
            return species_locked_list
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def lock_taxa(self, scientific_full_name, size_class, locked_at_count_area):
        """ """
        try:
            search_dict = {}
            search_dict["scientific_full_name"] = scientific_full_name
            search_dict["size_class"] = size_class
            samplerowkey = SampleRow(search_dict).get_key()
            if samplerowkey in self._sample_rows:
                if not self._sample_rows[samplerowkey].is_locked():
                    self._sample_rows[samplerowkey].set_lock(locked_at_count_area)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def unlock_taxa(self, scientific_full_name, size_class, count_area_number):
        """ """
        try:
            search_dict = {}
            search_dict["scientific_full_name"] = scientific_full_name
            search_dict["size_class"] = size_class
            samplerowkey = SampleRow(search_dict).get_key()
            if samplerowkey in self._sample_rows:
                self._sample_rows[samplerowkey].set_lock("")
            #
            self._sample_rows[samplerowkey].set_count_area_number(count_area_number)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_sample_row_dict(self, counted_row_dict):
        """ """
        try:
            samplerowkey = SampleRow(counted_row_dict).get_key()
            if samplerowkey in self._sample_rows:
                return self._sample_rows[samplerowkey].get_sample_row_dict()
            #
            return {}
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_sample_row(self, counted_row_dict):
        """ """
        try:
            if len(counted_row_dict.get("scientific_name", "")) > 0:
                samplerowkey = SampleRow(counted_row_dict).get_key()
                if samplerowkey in self._sample_rows:
                    self._sample_rows[samplerowkey].update_sample_row_dict(
                        counted_row_dict
                    )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_counted_value(self, selected_dict):
        """ """
        try:
            samplerowkey = SampleRow(selected_dict).get_key()
            if samplerowkey in self._sample_rows:
                return self._sample_rows[samplerowkey].get_counted_units()
            else:
                return 0
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_counted_value_in_core(self, counted_row_dict, value):
        """ """
        try:
            if value == "0":
                # Delete row.
                samplerowkey = SampleRow(counted_row_dict).get_key()
                if samplerowkey in self._sample_rows:
                    del self._sample_rows[samplerowkey]
                return
            #
            if len(counted_row_dict.get("scientific_full_name", "")) > 0:
                samplerowkey = SampleRow(counted_row_dict).get_key()
                if samplerowkey not in self._sample_rows:
                    self._sample_rows[samplerowkey] = SampleRow(counted_row_dict)
                # Check if the same method step or locked taxa.
                samplerowobject = self._sample_rows[samplerowkey]
                # Don't check for validity when the value is same same.
                if samplerowobject.get_counted_units() == value:
                    return
                if samplerowobject.is_locked():
                    raise UserWarning("Selected taxon is locked")

                #             if counted_row_dict.get('method_step') == samplerowobject.get_method_step():
                if True:
                    samplerowobject.set_counted_units(value)
                    samplerowobject.update_sample_row_dict(counted_row_dict)
                else:
                    raise UserWarning(
                        "Selected taxon is already counted in another method step."
                    )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_abundance_class_in_core(self, counted_row_dict, value):
        """ """
        try:
            if value == "0":
                # Delete row.
                samplerowkey = SampleRow(counted_row_dict).get_key()
                if samplerowkey in self._sample_rows:
                    del self._sample_rows[samplerowkey]
                return
            #
            if len(counted_row_dict.get("scientific_full_name", "")) > 0:
                samplerowkey = SampleRow(counted_row_dict).get_key()
                if samplerowkey not in self._sample_rows:
                    self._sample_rows[samplerowkey] = SampleRow(counted_row_dict)
                # Check if the same method step or locked taxa.
                samplerowobject = self._sample_rows[samplerowkey]
                # Don't check for validity when the value is same same.
                if samplerowobject.get_counted_units() == value:
                    return
                if samplerowobject.is_locked():
                    raise UserWarning("Selected taxon is locked")

                #             if counted_row_dict.get('method_step') == samplerowobject.get_method_step():
                if True:
                    #                 samplerowobject.set_counted_units(value)
                    samplerowobject.set_abundance_class(value)
                    samplerowobject.update_sample_row_dict(counted_row_dict)
                else:
                    raise UserWarning(
                        "Selected taxon is already counted in another method step."
                    )
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def delete_rows_in_method_step(self, current_method_step):
        """ """
        try:
            for sampleobject in list(
                self._sample_rows.values()
            ):  # Clone list when deleting content.
                if sampleobject.get_method_step() == current_method_step:
                    del self._sample_rows[sampleobject.get_key()]
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def update_coeff_for_sample_rows(
        self, current_method_step, count_area_number, coefficient
    ):
        """ """
        try:
            for sampleobject in self._sample_rows.values():
                if sampleobject.get_method_step() == current_method_step:
                    if not sampleobject.is_locked():
                        sampleobject.set_count_area_number(count_area_number)
                        sampleobject.set_coefficient(coefficient)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def import_sample_from_excel(self, excel_file_path):
        """Import from Excel."""
        try:
            # Sample info.
            tablefilereader = toolbox_utils.TableFileReader(
                file_path="",
                excel_file_name=excel_file_path,
                excel_sheet_name="sample_info.txt",
            )
            sample_header = tablefilereader.header()
            sample_rows = tablefilereader.rows()
            #
            self._tablefilewriter_sample_info.write_file(sample_header, sample_rows)

            # Sample data.
            tablefilereader = toolbox_utils.TableFileReader(
                file_path="",
                excel_file_name=excel_file_path,
                excel_sheet_name="sample_data.txt",
            )
            data_header = tablefilereader.header()
            data_rows = tablefilereader.rows()
            #
            self._tablefilewriter_sample_data.write_file(data_header, data_rows)

            # Sample method.
            tablefilereader = toolbox_utils.TableFileReader(
                file_path="",
                excel_file_name=excel_file_path,
                excel_sheet_name="counting_method.txt",
            )
            method_header = tablefilereader.header()
            method_rows = tablefilereader.rows()

            path = pathlib.Path(
                self._dataset_dir_path, self._dataset_name, self._sample_name
            )
            tablefilewriter_sample_method = toolbox_utils.TableFileWriter(
                file_path=path,
                text_file_name="counting_method.txt",
            )
            #
            tablefilewriter_sample_method.write_file(method_header, method_rows)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def export_sample_to_excel(self, export_target_dir, export_target_filename):
        """Export to Excel."""
        try:
            excel_export_writer = ExcelExportWriter(self)
            excel_export_writer.to_excel(export_target_dir, export_target_filename)
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )


class SampleRow:
    """Defines the content of one counted sample row."""

    def __init__(self, sample_row_dict):
        """ """
        try:
            self._sample_row_dict = {}
            self._sample_row_dict.update(sample_row_dict)
            #
            self._scientific_full_name = self._sample_row_dict.get(
                "scientific_full_name", ""
            )
            self._scientific_name = self._sample_row_dict.get("scientific_name", "")
            self._size_class = self._sample_row_dict.get("size_class", "")
            #
            # Get species related dictionaries for this taxon/sizeclass.
            self._taxon_dict = plankton_core.Species().get_taxon_dict(
                self._scientific_name
            )
            self._size_class_dict = plankton_core.Species().get_bvol_dict(
                self._scientific_name, self._size_class
            )
            self._sample_row_dict["taxon_class"] = self._taxon_dict.get(
                "taxon_class", ""
            )
            self._sample_row_dict["unit_type"] = self._size_class_dict.get(
                "bvol_unit", ""
            )

            bvol_list = self._size_class_dict.get("size_class_ref_list", "")
            old_bvol_list = self._sample_row_dict.get("bvol_list", "")
            if old_bvol_list == "":
                # Change only if empty. Keep counted bvol_list.
                self._sample_row_dict["bvol_list"] = bvol_list

            # Trophic type.
            if not self._sample_row_dict.get("trophic_type", ""):
                trophic_type = self._size_class_dict.get("trophic_type", "")
                if not trophic_type:
                    trophic_type = self._taxon_dict.get("trophic_type", "")
                if trophic_type:
                    self._sample_row_dict["trophic_type"] = trophic_type
            #
            self._bvol_volume = 0.0
            self._bvol_carbon = 0.0
            try:
                self._bvol_volume = float(
                    self._size_class_dict.get(
                        "bvol_calculated_volume_um3", "0"
                    ).replace(",", ".")
                )
                self._bvol_carbon = float(
                    self._size_class_dict.get("bvol_calculated_carbon_pg", "0").replace(
                        ",", "."
                    )
                )
            except Exception as e:
                raise UserWarning(
                    "Failed to read BVOL volume or carbon. Hint: Save Excel with values, not formulas. Exception: "
                    + str(e)
                )

            if (self._bvol_volume != 0.0) and (self._bvol_carbon != 0.0):
                self._sample_row_dict["volume_um3_unit"] = str(
                    self._round_value(self._bvol_volume)
                )
                self._sample_row_dict["carbon_pgc_unit"] = str(
                    self._round_value(self._bvol_carbon)
                )
                # Save last bvol_list used for calculations.
                self._sample_row_dict["bvol_list_calc"] = bvol_list

        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_sample_row_dict(self):
        """ """
        #         print('DEBUG GET scientific_full_name: ' + self._sample_row_dict.get('scientific_full_name', ''))
        #         print('DEBUG GET size_class: ' + self._sample_row_dict.get('size_class', ''))
        #         print('DEBUG GET variable_comment: ' + self._sample_row_dict.get('variable_comment', ''))
        return self._sample_row_dict

    def update_sample_row_dict(self, sample_row_dict):
        """ """
        #         print('DEBUG UPDATE scientific_full_name: ' + sample_row_dict.get('scientific_full_name', ''))
        #         print('DEBUG UPDATE size_class: ' + sample_row_dict.get('size_class', ''))
        #         print('DEBUG UPDATE variable_comment: ' + sample_row_dict.get('variable_comment', ''))
        self._sample_row_dict.update(sample_row_dict)

    def get_key(self):
        """ """
        rowkey = self._scientific_full_name + "+" + self._size_class
        return rowkey

    def get_scientific_full_name(self):
        """ """
        return self._scientific_full_name

    def get_scientific_name(self):
        """ """
        return self._scientific_name

    def get_size_class(self):
        """ """
        return self._size_class

    def get_method_step(self):
        """ """
        return self._sample_row_dict.get("method_step", "")

    def set_lock(self, locked_at_count_area):
        """ """
        self._sample_row_dict["locked_at_area"] = locked_at_count_area

    def get_locked_at_area(self):
        """ """
        return self._sample_row_dict.get("locked_at_area", "")

    def set_unlock(self):
        """ """
        self._sample_row_dict["locked_at_area"] = ""

    def is_locked(self):
        """ """
        if self._sample_row_dict.get("locked_at_area", "") == "":
            return False
        else:
            return True

    def get_count_area_number(self):
        """ """
        return self._sample_row_dict.get("count_area_number", "")

    def set_count_area_number(self, count_area_number):
        """ """
        try:
            self._sample_row_dict["count_area_number"] = count_area_number
            count_area_number = int(count_area_number)
            # Adjust length of list for counted per are.
            counted_units_list = self._sample_row_dict.get("counted_units_list", None)
            if counted_units_list:
                counted_units_list = [int(x) for x in counted_units_list.split(";")]
            else:
                counted_units_list = count_area_number * [0]
                counted_units_list[0] = self._sample_row_dict.get("counted_units", "0")
            #
            if len(counted_units_list) < count_area_number:
                counted_units_list += (count_area_number - len(counted_units_list)) * [
                    0
                ]
            if len(counted_units_list) > count_area_number:
                counted_units_list = counted_units_list[:count_area_number]
                # Recalculate when areas are removed.
                calculated_value = sum(counted_units_list)
                self._sample_row_dict["counted_units"] = str(calculated_value)
            #
            self._sample_row_dict["counted_units_list"] = ";".join(
                str(x) for x in counted_units_list
            )
            # print('DEBUG: add count area: ' + self._sample_row_dict['counted_units_list'])
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def set_coefficient(self, coefficient):
        """ """
        self._sample_row_dict["coefficient"] = coefficient

    def get_counted_units_list(self):
        """ """
        counted_units_list = self._sample_row_dict.get("counted_units_list", "0")
        #
        return counted_units_list

    def get_counted_units(self):
        """ """
        try:
            countedunits = self._sample_row_dict.get("counted_units", "0")
            if countedunits:
                countedunits = int(countedunits)
            else:
                countedunits = 0
        except:
            countedunits = 0
        #
        return countedunits

    def set_counted_units(self, value):
        """ """
        try:
            old_value = self._sample_row_dict.get("counted_units", 0)
            #
            self._sample_row_dict["counted_units"] = value
            self._sample_row_dict["abundance_class"] = ""
            #
            count_area_number = int(self._sample_row_dict.get("count_area_number", "1"))
            counted_units_list = self._sample_row_dict.get("counted_units_list", None)
            if counted_units_list:
                counted_units_list = [int(x) for x in counted_units_list.split(";")]
            else:
                counted_units_list = count_area_number * [0]
            #
            if count_area_number == 1:
                counted_units_list[0] = value
            else:
                if old_value != "":
                    diff_value_for_area = int(value) - int(old_value)
                else:
                    diff_value_for_area = int(value)

                old_value_for_area = counted_units_list[(count_area_number - 1)]
                new_value_for_area = old_value_for_area + diff_value_for_area
                if new_value_for_area >= 0:
                    counted_units_list[(count_area_number - 1)] = new_value_for_area
                else:
                    toolbox_utils.Logging().warning(
                        "Value for count area can't be negative."
                    )
                    self._sample_row_dict["counted_units"] = old_value
                    return

            #
            self._sample_row_dict["counted_units_list"] = ";".join(
                str(x) for x in counted_units_list
            )
            #
            # print('DEBUG: ' + self._sample_row_dict['counted_units_list'])
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def get_abundance_class(self):
        """ """
        try:
            abundance_class = str(self._sample_row_dict.get("abundance_class", ""))
        except:
            abundance_class = ""
        #
        return abundance_class

    def set_abundance_class(self, value):
        """ """
        self._sample_row_dict["abundance_class"] = value
        self._sample_row_dict["counted_units"] = ""

    def get_row_as_text_list(self, header_list):
        """ """
        try:
            self._calculate_values()
            #
            row = []
            for header_item in header_list:
                row.append(self._sample_row_dict.get(header_item, ""))
            #
            return row
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def _calculate_values(self):
        """ """
        try:
            counted_txt = self._sample_row_dict.get("counted_units", "")
            coefficient_txt = self._sample_row_dict.get("coefficient", "0")
            # Check if abundance_class.
            if counted_txt == "":
                self._sample_row_dict["abundance_units_l"] = ""
                self._sample_row_dict["volume_mm3_l"] = ""
                self._sample_row_dict["carbon_ugc_l"] = ""
                return
            #
            try:
                counted = float(counted_txt.replace(",", "."))
                coefficient = float(coefficient_txt.replace(",", "."))
                abundance = counted * coefficient
                self._sample_row_dict["abundance_units_l"] = str(
                    self._round_value(abundance)
                )
                #
                try:
                    if self._bvol_volume != 0.0:
                        value = abundance * self._bvol_volume / 1000000000.0
                        self._sample_row_dict["volume_mm3_l"] = str(
                            self._round_value(value)
                        )
                except:
                    self._sample_row_dict["volume_mm3_l"] = "0.00"
                #
                try:
                    if self._bvol_carbon != 0.0:
                        # CARBON calculation modified 2021-02-23.
                        # value = abundance * self._bvol_carbon / 1000.0
                        value = abundance * self._bvol_carbon / 1000000.0
                        self._sample_row_dict["carbon_ugc_l"] = str(
                            self._round_value(value)
                        )
                except:
                    self._sample_row_dict["carbon_ugc_l"] = "0.00"
            except:
                self._sample_row_dict["abundance_units_l"] = "0.00"
                self._sample_row_dict["volume_mm3_l"] = "0.00"
                self._sample_row_dict["carbon_ugc_l"] = "0.00"
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )

    def _round_value(self, value, n=4):  # Number of significant figures.
        """ """
        try:
            if value != 0.0:
                if value >= 1000.0:
                    value = round(value, 1)
                else:
                    value = round(
                        value, -int(math.floor(math.log10(abs(value)))) + (n - 1)
                    )
            return value
        #
        except Exception as e:
            debug_info = (
                self.__class__.__name__ + ", row  " + str(sys._getframe().f_lineno)
            )
            toolbox_utils.Logging().error(
                "Exception in counter: (" + debug_info + "): " + str(e)
            )


class ExcelExportWriter:
    """ """

    def __init__(self, sample_object):
        """ """
        self.sample_object = sample_object
        #
        self.load_overview_mappings()

    def to_excel(self, export_target_dir, export_target_filename):
        """Export to Excel."""
        self.export_target_filename = export_target_filename
        # Create Excel document.
        filepathname = pathlib.Path(export_target_dir, export_target_filename)
        workbook = xlsxwriter.Workbook(filepathname)
        # Add worksheets.
        self.summary_worksheet = workbook.add_worksheet("Sample summary")
        self.sampleinfo_worksheet = workbook.add_worksheet("sample_info.txt")
        self.sampledata_worksheet = workbook.add_worksheet("sample_data.txt")
        self.samplemethod_worksheet = workbook.add_worksheet("counting_method.txt")
        self.readme_worksheet = workbook.add_worksheet("README")
        # Adjust column width.
        self.sampleinfo_worksheet.set_column("A:B", 40)
        self.sampledata_worksheet.set_column("A:C", 30)
        self.sampledata_worksheet.set_column("D:W", 20)
        self.samplemethod_worksheet.set_column("A:Q", 30)
        self.readme_worksheet.set_column("A:A", 100)
        # Create cell formats.
        self.bold_format = workbook.add_format({"bold": True})
        self.bold_right_format = workbook.add_format({"bold": True, "align": "right"})
        self.integer_format = workbook.add_format()
        self.integer_format.set_num_format("0")
        self.decimal_format = workbook.add_format()
        self.decimal_format.set_num_format("0.00")
        self.decimal_6_format = workbook.add_format()
        self.decimal_6_format.set_num_format("0.000000")
        self.latlong_dd_format = workbook.add_format()
        self.latlong_dd_format.set_num_format("0.0000")

        # Prepare sample info header and rows.
        self.sample_data_header = self.sample_object.get_header()
        self.sample_data_rows = self.sample_object.get_rows()
        # Prepare method header and rows.
        self.sample_method_header = []
        self.sample_method_rows = []
        sample_path = self.sample_object.get_dir_path()
        if pathlib.Path(sample_path, "counting_method.txt").exists():
            (
                self.sample_method_header,
                self.sample_method_rows,
            ) = plankton_core.PlanktonCounterMethods().get_counting_method_table(
                sample_path, "counting_method.txt"
            )

        # === Sheet: Sample info. ===
        sample_info_header = ["key", "value"]
        sample_info_header_order = [
            "plankton_toolbox_version",
            "sample_name",
            "sample_id",
            "sample_date",
            "sample_time",
            "visit_year",
            "country_code",
            "platform_code",
            "sampling_series",
            "sampling_laboratory",
            "orderer",
            "project_code",
            "project_name",
            "method_documentation",
            "method_reference_code",
            "station_name",
            "station_code",
            "sample_latitude_dm",
            "sample_longitude_dm",
            "sample_latitude_dd",
            "sample_longitude_dd",
            "sample_min_depth_m",
            "sample_max_depth_m",
            "water_depth_m",
            "sampler_type_code",
            "sampled_volume_l",
            "net_type_code",
            "sampler_area_m2",
            "net_mesh_size_um",
            "wire_angle_deg",
            "net_tow_length_m",
            "analytical_laboratory",
            "analysis_date",
            "analysed_by",
            "sample_comment",
        ]
        sample_info_rows = []
        self.sample_info_dict = self.sample_object.get_sample_info()
        for header_item in sample_info_header_order:
            sample_info_rows.append(
                [header_item, self.sample_info_dict.get(header_item, "")]
            )
        # Sample info header.
        self.sampleinfo_worksheet.write_row(0, 0, sample_info_header, self.bold_format)
        # Rows.
        row_nr = 1
        for row in sample_info_rows:
            self.sampleinfo_worksheet.write_row(row_nr, 0, row)
            row_nr += 1
        # Extra info for restart of counting session.
        row_nr += 1
        for key in self.sample_info_dict.keys():
            if key == "last_used_method_step":
                self.sampleinfo_worksheet.write_row(
                    row_nr, 0, [key, self.sample_info_dict.get(key, "")]
                )
                row_nr += 1
            if key.startswith("max_count_area<+>"):
                self.sampleinfo_worksheet.write_row(
                    row_nr, 0, [key, self.sample_info_dict.get(key, "")]
                )
                row_nr += 1

        # === Sheet: Sample data. ===
        self.sampledata_worksheet.title = "sample_data.txt"
        # Header.
        self.sampledata_worksheet.write_row(
            0, 0, self.sample_data_header, self.bold_format
        )
        # Rows.
        row_nr = 1
        for row in self.sample_data_rows:
            self.sampledata_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Sheet: Sample method. ===
        # Header.
        self.samplemethod_worksheet.write_row(
            0, 0, self.sample_method_header, self.bold_format
        )
        # Rows.
        row_nr = 1
        for row in self.sample_method_rows:
            self.samplemethod_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Sheet: README. ===
        # Header.
        self.readme_worksheet.write_row(
            0, 0, ["Plankton Toolbox - Plankton counter"], self.bold_format
        )
        # Rows.
        readme_text = [
            [""],
            ["This Excel file is generated by Plankton Toolbox."],
            [""],
            [
                "The file represents one counted plankton sample. It can be used for export and import "
            ],
            [
                "between different computers running Plankton Toolbox, or as an archive file."
            ],
            [""],
            [
                'NOTE: Don\'t edit or rename the sheets "sample_info.txt", "sample_data.txt" or '
            ],
            [
                '"counting_method.txt" if the file should be imported later to Plankton Toolbox.'
            ],
            [""],
            ["Generated sheets:"],
            [
                "- Sample summary: Contains information in a compact format. May be used printed for archive purposes."
            ],
            [
                "- sample_info.txt: Copy of the internally used file for information connected to a sample (metadata)."
            ],
            [
                "- sample_data.txt: Copy of the internally used file for counted sample rows."
            ],
            [
                "- counting_method.txt: Copy of the internally used file for parameters related to the counting method."
            ],
            ["- README: This text."],
            [""],
            [
                "More info at: http://nordicmicroalgae.org and http://plankton-toolbox.org "
            ],
        ]
        #
        row_nr = 1
        for row in readme_text:
            self.readme_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Sheet: Sample summary. ===
        self.create_overview_sheet()

        # Done. Close the Excel document.
        workbook.close()

    def load_overview_mappings(self):
        """ """
        self.overview_info_mapping = [
            ["label", "Plankton Toolbox:", 0, 1, "text"],
            ["sample_info", "plankton_toolbox_version", 0, 2, "text"],
            # VISIT.
            ["label", "SAMPLING EVENT", 2, 1, "text"],
            ["label", "Station:", 3, 1, "text"],
            ["sample_info", "station_name", 3, 2, "text"],
            ["label", "Date:", 4, 1, "text"],
            ["sample_info", "sample_date", 4, 2, "text"],
            ["label", "Time:", 5, 1, "text"],
            ["sample_info", "sample_time", 5, 2, "text"],
            ["label", "Series:", 6, 1, "text"],
            ["sample_info", "sampling_series", 6, 2, "text"],
            ["label", "Platform:", 7, 1, "text"],
            ["sample_info", "platform_code", 7, 2, "text"],
            ["label", "Lat/long (DD):", 8, 1, "text"],
            ["sample_info", "sample_latitude_dd", 8, 2, "text"],  # , 'pos_dd'],
            ["sample_info", "sample_longitude_dd", 8, 3, "text"],  # , 'pos_dd'],
            ["label", "Lat/long (DM):", 9, 1, "text"],
            ["sample_info", "sample_latitude_dm", 9, 2, "text"],
            ["sample_info", "sample_longitude_dm", 9, 3, "text"],
            ["label", "Water depth (m):", 10, 1, "text"],
            ["sample_info", "water_depth_m", 10, 2, "decimal"],
            ["label", "Project code:", 11, 1, "text"],
            ["sample_info", "project_code", 11, 2, "text"],
            ["label", "Project name:", 12, 1, "text"],
            ["sample_info", "project_name", 12, 2, "text"],
            # SAMPLE.
            ["label", "SAMPLE", 2, 5, "text"],
            ["label", "Sampler type code:", 3, 5, "text"],
            ["sample_info", "sampler_type_code", 3, 7, "text"],
            ["label", "Min depth (m):", 4, 5, "text"],
            ["sample_info", "sample_min_depth_m", 4, 7, "decimal"],
            ["label", "Max depth (m):", 5, 5, "text"],
            ["sample_info", "sample_max_depth_m", 5, 7, "decimal"],
            ["label", "Analysed by/taxonomist:", 7, 5, "text"],
            ["sample_info", "analysed_by", 7, 7, "text"],
            ["label", "Analysis date:", 8, 5, "text"],
            ["sample_info", "analysis_date", 8, 7, "text"],
            ["label", "Sample comment:", 9, 5, "text"],
            ["sample_info", "sample_comment", 9, 7, "text"],
            ["label", "Sampled volume (l):", 10, 5, "text"],
            ["sample_info", "sampled_volume_l", 10, 7, "decimal"],
            # SIGNATURE.
            ["label", "SIGNATURE", 2, 9, "text"],
            ["label", "Date:", 4, 9, "text"],
            ["label", "Institute:", 6, 9, "text"],
            ["label", "Signature:", 8, 9, "text"],
        ]
        self.overview_method_mapping = [
            # METOD STEP.
            ["label", "Method step", 15, 1, "text"],
            ["counting_method", "counting_method_step", 16, 1, "text"],
            ["label", "Preservative", 15, 3, "text"],
            ["counting_method", "preservative", 16, 3, "text"],
            ["label", "Counted volume (ml)", 15, 5, "text_r"],
            ["counting_method", "counted_volume_ml", 16, 5, "decimal"],
            ["label", "Microscope", 15, 7, "text"],
            ["counting_method", "microscope", 16, 7, "text"],
            ["label", "Magnification", 15, 9, "text_r"],
            ["counting_method", "magnification", 16, 9, "integer"],
        ]
        self.overview_sample_mapping = [
            ["label", "Class", 15, 1, "text"],
            ["sample_data", "taxon_class", 15, 1, "text"],
            ["label", "Scientific name", 15, 2, "text"],
            ["sample_data", "scientific_full_name", 15, 2, "text"],
            ["label", "Trophic type", 15, 4, "text"],
            ["sample_data", "trophic_type", 15, 4, "text"],
            ["label", "Size class", 15, 5, "text_r"],
            ["sample_data", "size_class", 15, 5, "integer"],
            ["label", "Counted", 15, 6, "text_r"],
            ["sample_data", "counted_units", 15, 6, "integer"],
            ["label", "Coeff.", 15, 7, "text_r"],
            ["sample_data", "coefficient", 15, 7, "integer"],
            ["label", "Abundance (units/l)", 15, 8, "text_r"],
            ["sample_data", "abundance_units_l", 15, 8, "integer"],
            ["label", "Volume (mm3/l)", 15, 9, "text_r"],
            ["sample_data", "volume_mm3_l", 15, 9, "decimal_6"],
            ["label", "Carbon (ugc/l)", 15, 10, "text_r"],
            ["sample_data", "carbon_ugc_l", 15, 10, "decimal"],
            ["label", "Volume/unit (um3)", 15, 11, "text_r"],
            ["sample_data", "volume_um3_unit", 15, 11, "decimal"],
            ["label", "Counted trans/views", 15, 12, "text_r"],
            ["sample_data", "count_area_number", 15, 12, "integer"],
        ]

    def create_overview_sheet(self):
        """ """
        # Excel page setup.
        self.summary_worksheet.set_paper(9)  # A4
        self.summary_worksheet.set_landscape()
        self.summary_worksheet.fit_to_pages(1, 0)
        self.summary_worksheet.set_footer(
            "Plankton Toolbox   -   &F   -   &D &T   -   Page: &P (&N)"
        )
        # Image.
        ### worksheet.insert_image('G2', 'plankton_toolbox_icon.png')
        # Column width.
        xlsx_layout = [
            {"columns": "A:A", "width": 2},
            {"columns": "B:D", "width": 20},
            {"columns": "E:F", "width": 12},
            {"columns": "G:G", "width": 20},
            {"columns": "H:H", "width": 10},
            {"columns": "I:I", "width": 20},
            {"columns": "J:K", "width": 15},
            {"columns": "L:M", "width": 20},
        ]
        for row in xlsx_layout:
            if ("columns" in row.keys()) and ("width" in row.keys()):
                self.summary_worksheet.set_column(row["columns"], row["width"])
        #
        method_steps_dict = {}
        for data in self.sample_method_rows:
            # print(index)
            step_dict = dict(zip(self.sample_method_header, data))
            method_steps_dict[step_dict["counting_method_step"]] = step_dict
        # Write file name.
        self.summary_worksheet.write(
            0, 3, self.export_target_filename, self.bold_format
        )
        #
        for row in self.overview_info_mapping:
            source, field, cell_row, cell_col, cell_format = row

            try:
                value = ""
                if source == "label":
                    if cell_format == "text_r":
                        self.summary_worksheet.write(
                            cell_row, cell_col, field, self.bold_right_format
                        )
                    else:
                        self.summary_worksheet.write(
                            cell_row, cell_col, field, self.bold_format
                        )

                elif source == "sample_info":
                    if field in self.sample_info_dict:
                        value = self.sample_info_dict[field]

                        cell_style_obj = None
                        if cell_format == "integer":
                            cell_style_obj = self.integer_format
                            if value != "":
                                value = int(float(value))
                        elif cell_format == "decimal":
                            cell_style_obj = self.decimal_format
                            if value != "":
                                value = float(value)
                        elif cell_format == "decimal_6":
                            cell_style_obj = self.decimal_6_format
                            if value != "":
                                value = float(value)
                        elif cell_format == "pos_dd":
                            cell_style_obj = self.latlong_dd_format
                            if value != "":
                                value = float(value)
                        #
                        self.summary_worksheet.write(
                            cell_row, cell_col, value, cell_style_obj
                        )

            except:
                print(row)

            # Methods and row data.
            row_offset = 0
            header = True
            last_used_method_step = "not defined"

            # Sort order: method_step, 'scientific_full_name, size_class.
            sorted_data_rows = self.sample_data_rows.copy()
            sorted_data_rows.sort(key=operator.itemgetter(4, 0, 3))

            for data_row in sorted_data_rows:

                data_row_dict = dict(zip(self.sample_data_header, data_row))
                used_method_step = data_row_dict.get("method_step", "")
                if used_method_step:
                    method_dict = method_steps_dict[used_method_step]
                else:
                    method_dict = {}
                # New method step.
                if used_method_step != last_used_method_step:
                    row_offset += 1
                    self.overview_sheet_method(method_dict, row_offset)
                    row_offset += 3
                    header = True
                    last_used_method_step = used_method_step
                # Header for data rows.
                if header:
                    self.overview_sheet_data(data_row_dict, row_offset, header)
                    header = False
                    row_offset += 1
                # Data rows.
                self.overview_sheet_data(data_row_dict, row_offset, header)
                row_offset += 1

    def overview_sheet_method(self, method_dict, row_offset):
        """ """
        for row in self.overview_method_mapping:
            source, field, cell_row, cell_col, cell_format = row

            try:
                value = ""
                if source == "label":
                    if cell_format == "text_r":
                        self.summary_worksheet.write(
                            cell_row + row_offset,
                            cell_col,
                            field,
                            self.bold_right_format,
                        )
                    else:
                        self.summary_worksheet.write(
                            cell_row + row_offset, cell_col, field, self.bold_format
                        )

                elif source == "counting_method":
                    if field in method_dict:
                        value = method_dict[field]

                        cell_style_obj = None
                        if cell_format == "integer":
                            cell_style_obj = self.integer_format
                            if value != "":
                                value = int(float(value))
                                # Don't write zero values.
                                if value == 0:
                                    value = ""
                                    cell_style_obj = None
                        elif cell_format == "decimal":
                            cell_style_obj = self.decimal_format
                            if value != "":
                                value = float(value)
                                # Don't write zero values.
                                if value == 0.0:
                                    value = ""
                                    cell_style_obj = None
                        elif cell_format == "decimal_6":
                            cell_style_obj = self.decimal_6_format
                            if value != "":
                                value = float(value)
                                # Don't write zero values.
                                if value == 0.0:
                                    value = ""
                                    cell_style_obj = None
                        #
                        self.summary_worksheet.write(
                            cell_row + row_offset, cell_col, value, cell_style_obj
                        )
            #
            except Exception as e:
                print(str(row), "   Exception: ", str(e))

    def overview_sheet_data(self, sample_data_dict, row_offset, header=True):
        """ """
        for row in self.overview_sample_mapping:
            source, field, cell_row, cell_col, cell_format = row

            try:
                value = ""
                if header:
                    if source == "label":
                        if cell_format == "text_r":
                            self.summary_worksheet.write(
                                cell_row + row_offset,
                                cell_col,
                                field,
                                self.bold_right_format,
                            )
                        else:
                            self.summary_worksheet.write(
                                cell_row + row_offset, cell_col, field, self.bold_format
                            )
                else:
                    if source == "sample_data":
                        if field in sample_data_dict:
                            value = sample_data_dict[field]

                            # Special for qualitative analysis.
                            if (field == "counted_units") and (value == ""):
                                value = sample_data_dict["abundance_class"]
                                #
                                if value == "1":
                                    value = "1 (Observed)"
                                elif value == "2":
                                    value = "2 (Several cells)"
                                elif value == "3":
                                    value = "3 (1-10%)"
                                elif value == "4":
                                    value = "4 (10-50%)"
                                elif value == "5":
                                    value = "5 (50-100%)"
                                #
                                cell_format = "text"
                            #
                            cell_style_obj = None
                            if cell_format == "integer":
                                cell_style_obj = self.integer_format
                                if value != "":
                                    value = int(float(value))
                                    # Don't write zero values.
                                    if value == 0:
                                        value = ""
                                        cell_style_obj = None
                            elif cell_format == "decimal":
                                cell_style_obj = self.decimal_format
                                if value != "":
                                    value = float(value)
                                    # Don't write zero values.
                                    if value == 0.0:
                                        value = ""
                                        cell_style_obj = None
                            elif cell_format == "decimal_6":
                                cell_style_obj = self.decimal_6_format
                                if value != "":
                                    value = float(value)
                                    # Don't write zero values.
                                    if value == 0.0:
                                        value = ""
                                        cell_style_obj = None
                            #
                            self.summary_worksheet.write(
                                cell_row + +row_offset, cell_col, value, cell_style_obj
                            )
            #
            except Exception as e:
                print(str(row), "   Exception: ", str(e))
