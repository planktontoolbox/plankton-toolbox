#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import os
import zipfile
import shutil
import tempfile
import toolbox_utils
import plankton_core


class SharkArchive:
    """ """

    def __init__(
        self,
        file_path=None,
        archive_filename=None,
    ):
        """ """
        self._file_path = file_path
        self._archive_filename = archive_filename
        #
        self._data_tableobject = None
        self._metadata_text = None
        self._metadataauto_text = None

    def clear(self):
        """ """
        self._data_tableobject = None
        self._metadata_text = None
        self._metadataauto_text = None

    def load_all(self):
        """ """
        self.load_shark_data()
        self.load_shark_metadata()
        self.load_shark_metadata_auto()

    def get_data_tableobject(self):
        """ """
        return self._data_tableobject

    def get_metadata_text(self):
        """ """
        if self._metadata_text is not None:
            return self._metadata_text
        else:
            return ""

    def get_metadata_dict(self):
        """ """
        metadata_dict = {}
        for row in self.get_metadata_text().split("\r\n"):
            if ":" in row:
                keyvalue = row.strip().split(":", 1)
                if len(keyvalue) >= 2:
                    metadata_dict[keyvalue[0]] = keyvalue[1]
        return metadata_dict

    def get_metadataauto_text(self):
        """ """
        if self._metadataauto_text is not None:
            return self._metadataauto_text
        else:
            return ""

    def get_metadataauto_dict(self):
        """ """
        metadataauto_dict = {}
        for row in self.get_metadataauto_text().split("\r\n"):
            if ":" in row:
                keyvalue = row.strip().split(":", 1)
                if len(keyvalue) >= 2:
                    metadataauto_dict[keyvalue[0]] = keyvalue[1]
        return metadataauto_dict

    def load_shark_data(self):
        """ """
        try:
            self._data_tableobject = toolbox_utils.TableFileReader(
                file_path=self._file_path,
                zip_file_name=self._archive_filename,
                zip_file_entry="shark_data.txt",
            )
        except:
            self._data_tableobject = toolbox_utils.TableFileReader()  # Empty object.

    def load_shark_metadata(self):
        """ """
        try:
            self._metadata_dict = {}
            metadata_tableobject = toolbox_utils.TableFileReader(
                file_path=self._file_path,
                zip_file_name=self._archive_filename,
                zip_file_entry="shark_metadata.txt",
                select_columns_by_index=[0],
            )
            # Metadata is a key/value list with no header. Merge header and row.
            concat_table = [metadata_tableobject.header()] + metadata_tableobject.rows()
            concat_table = map("\t".join, concat_table)
            self._metadata_text = "\r\n".join(concat_table)
        except:
            self._metadata_dict = toolbox_utils.TableFileReader()  # Empty object.

    def load_shark_metadata_auto(self):
        """ """
        try:
            self._metadataauto_dict = {}
            metadataauto_tableobject = toolbox_utils.TableFileReader(
                file_path=self._file_path,
                zip_file_name=self._archive_filename,
                zip_file_entry="shark_metadata_auto.txt",
                select_columns_by_index=[0],
            )
            # Metadata is a key/value list with no header. Merge header and row.
            concat_table = [
                metadataauto_tableobject.header()
            ] + metadataauto_tableobject.rows()
            concat_table = map("\t".join, concat_table)
            self._metadataauto_text = "\r\n".join(concat_table)
        except:
            self._metadataauto_dict = toolbox_utils.TableFileReader()  # Empty object.

    def generate_metadata_auto(self):
        """ """
        # Index for columns.
        year_index = None
        date_index = None
        longitude_index = None
        latitude_index = None
        parameter_index = None
        unit_index = None
        # Scanned field values.
        min_year = None
        max_year = None
        min_date = None
        max_date = None
        min_longitude = None
        max_longitude = None
        min_latitude = None
        max_latitude = None
        parameter_unit_list = []
        # Check header. Supports different sets of column names.
        for item_index, item in enumerate(self._data_tableobject.header()):
            if item in ["year", "visit_year"]:
                year_index = item_index
            if item in ["sample_date", "sampling_date", "visit_date"]:
                date_index = item_index
            if item in ["sample_latitude_dd", "latitude_dd", "lat_dd"]:
                latitude_index = item_index
            if item in ["sample_longitude_dd", "sample_longitude_dd", "long_dd"]:
                longitude_index = item_index
            if item in ["parameter"]:
                parameter_index = item_index
            if item in ["unit"]:
                unit_index = item_index
            #
            max_index = max(
                year_index,
                date_index,
                latitude_index,
                longitude_index,
                parameter_index,
                unit_index,
            )
        # Scan rows.
        for row in self._data_tableobject.rows():
            if len(row) > max_index:
                if year_index:
                    min_year = (
                        min(row[year_index], min_year) if min_year else row[year_index]
                    )
                    max_year = (
                        max(row[year_index], max_year) if max_year else row[year_index]
                    )
                if date_index:
                    min_date = (
                        min(row[date_index], min_date) if min_date else row[date_index]
                    )
                    max_date = (
                        max(row[date_index], max_date) if max_date else row[date_index]
                    )
                if latitude_index:
                    min_latitude = (
                        min(row[latitude_index], min_latitude)
                        if min_latitude
                        else row[latitude_index]
                    )
                    max_latitude = (
                        max(row[latitude_index], max_latitude)
                        if max_latitude
                        else row[latitude_index]
                    )
                if longitude_index:
                    min_longitude = (
                        min(row[longitude_index], min_longitude)
                        if min_longitude
                        else row[longitude_index]
                    )
                    max_longitude = (
                        max(row[longitude_index], max_longitude)
                        if max_longitude
                        else row[longitude_index]
                    )
                if parameter_index:
                    param_unit = row[parameter_index] + ":" + row[unit_index]
                    if param_unit not in parameter_unit_list:
                        parameter_unit_list.append(param_unit)
        # Put together generated metadata.
        metadata_rows = []
        # Extract parts from the dataset file name.
        name, datatype, version = self._split_shark_archive_filename(
            self._archive_filename
        )
        metadata_rows.append("dataset_name: " + name)
        metadata_rows.append("dataset_version: " + version)
        metadata_rows.append("dataset_category: " + datatype)
        metadata_rows.append("dataset_filename: " + self._archive_filename)
        # Scanned results.
        if year_index:
            metadata_rows.append("min_year: " + min_year)
            metadata_rows.append("max_year: " + max_year)
        if date_index:
            if not year_index:
                metadata_rows.append("min_year: " + min_date[0:4])
                metadata_rows.append("max_year: " + max_date[0:4])
            metadata_rows.append("min_date: " + min_date)
            metadata_rows.append("max_date: " + max_date)
        if latitude_index:
            metadata_rows.append("min_latitude: " + min_latitude.replace(",", "."))
            metadata_rows.append("max_latitude: " + max_latitude.replace(",", "."))
        if longitude_index:
            metadata_rows.append("min_longitude: " + min_longitude.replace(",", "."))
            metadata_rows.append("max_longitude: " + max_longitude.replace(",", "."))
        if parameter_index:
            for index, param_unit in enumerate(sorted(parameter_unit_list)):
                pair = param_unit.split(":")
                metadata_rows.append("parameter#" + str(index) + ": " + pair[0])
                metadata_rows.append("unit#" + str(index) + ": " + pair[1])
        # Join rows.
        self._metadataauto_text = "\r\n".join(metadata_rows)

    def update_archive_file(self):
        """ """
        entries_to_remove = []
        if self._data_tableobject is not None:
            entries_to_remove.append("shark_data.txt")
        if self._metadata_text is not None:
            entries_to_remove.append("shark_metadata.txt")
        if self._metadataauto_text is not None:
            entries_to_remove.append("shark_metadata_auto.txt")
        #
        if len(entries_to_remove) > 0:
            self._remove_entries_from_zip(
                self._file_path, self._archive_filename, entries_to_remove
            )
            #
            zip_namepath = os.path.join(self._file_path, self._archive_filename)
            zip_write = zipfile.ZipFile(
                zip_namepath, "a", zipfile.ZIP_DEFLATED
            )  # Append to zip.
            try:
                if self._data_tableobject is not None:
                    data = (
                        "\t".join(self._data_tableobject.header())
                        + "\r\n"
                        + "\r\n".join(map("\t".join, self._data_tableobject.rows()))
                    )
                    zip_write.writestr(
                        "shark_data.txt", data.encode("cp1252", errors="ignore")
                    )
                #
                if self._metadata_text is not None:
                    zip_write.writestr(
                        "shark_metadata.txt",
                        self._metadata_text.encode("cp1252", errors="replace"),
                    )
                #
                if self._metadataauto_text is not None:
                    zip_write.writestr(
                        "shark_metadata_auto.txt",
                        self._metadataauto_text.encode("cp1252", errors="replace"),
                    )
            finally:
                zip_write.close()

    def _split_shark_archive_filename(self, shark_filename):
        """Extracts name parts from the SHARK Archive filename format.
        Example: SHARK_Phytoplankton_2013_UMSC_version_2015-04-14.zip
        - Dataset name: SHARK_Phytoplankton_2013_UMSC
        - Datatype: Phytoplankton
        - Version: 2015-04-14
        """
        datasetname = ""
        datatype = ""
        version = ""
        try:
            filename = os.path.splitext(shark_filename)[0]
            parts = filename.split("version")
            datasetname = parts[0].strip("_").strip()
            version = parts[1].strip("_").strip() if len(parts) > 0 else ""
            parts = filename.split("_")
            datatype = parts[1].strip("_").strip()
        except:
            pass
        #
        return datasetname, datatype, version

    def _remove_entries_from_zip(self, zip_file_path, zip_file_name, entries_to_remove):
        """There is no method in Python for this.
        Copy everything else to a temporary zip file and rename when finished."""
        tmpdir = tempfile.mkdtemp()
        try:
            zip_file = os.path.join(zip_file_path, zip_file_name)
            new_tmp_file = os.path.join(tmpdir, "tmp.zip")
            zip_read = zipfile.ZipFile(zip_file, "r")
            zip_write = zipfile.ZipFile(new_tmp_file, "w", zipfile.ZIP_DEFLATED)
            for item in zip_read.infolist():
                if item.filename not in entries_to_remove:
                    data = zip_read.read(item.filename)
                    zip_write.writestr(item, data)
            #
            zip_read.close()
            zip_write.close()
            shutil.move(new_tmp_file, zip_file)
        finally:
            shutil.rmtree(tmpdir)  # Delete the temporary directory.


# ===== TEST =====

if __name__ == "__main__":
    """Used for tests."""

    print("\n=== TEST: 1. ===")
    try:
        sharkarchive = SharkArchive(
            file_path="../test_data",
            archive_filename="SHARK_Phytoplankton_2013_UMSC_version_2015-04-14.zip",
        )
        #
        sharkarchive.load_shark_data()
        print("\nDEBUG: " + str(sharkarchive.get_data_tableobject().header()))
        for index, row in enumerate(sharkarchive.get_data_tableobject().rows()):
            if index >= 10:
                print("DEBUG: Show 10 first rows.")
                break
            print("DEBUG: " + str(row))
        #
        sharkarchive.load_shark_metadata()
        print("\nDEBUG: " + str(sharkarchive.get_metadata_text()))
        print("\nDEBUG: " + str(sharkarchive.get_metadata_dict()))
        #
        sharkarchive.load_shark_metadata_auto()
        print("\nDEBUG: " + str(sharkarchive.get_metadataauto_text()))
        print("\nDEBUG: " + str(sharkarchive.get_metadataauto_dict()))
        #
        sharkarchive.generate_metadata_auto()
        print("\nDEBUG: " + str(sharkarchive.get_metadataauto_text()))
        print("\nDEBUG: " + str(sharkarchive.get_metadataauto_dict()))
        #
        sharkarchive.update_archive_file()

    except Exception as e:
        print("Test failed: " + str(e))
        raise
