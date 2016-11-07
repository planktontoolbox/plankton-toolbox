# Plankton Toolbox: Datasets and parsers #

## Datasets ##
A dataset is a collection of data and Plankton Toolbox handle datasets as units of data for import. 
Datasets can be small, for example contain analysis results for one sample only, or be big and contain results from many stations and visits.

Current version of Plankton Toolbox supports single file datasets. Both text files and Excel files in the *.xlsx format can be imported.
Datasets should be table oriented, which means that there should be a header row and rows with data.

One example where it is possible to download this kind of datasets is SHARKweb: [http://smhi.se/sharkweb]

## Parsers ##
Internally the Plankton Toolbox only operates on datasets organised in a tree structure. 
Table oriented datasets must therefore be translated from table format to tree format by a parser. 
Since dataset column names and content differ a lot depending on the dataset origin the parsing process must be configurable. 
To handle this requirement parsers are stored in Excel format and can easily be modified by users with enough knowledge on how they work.

## Where are parsers located? ##

When Plankton Toolbox is downloaded and the zip-file is decompressed the directory structure below will occur (Windows example). 
Parsers must be placed in the directory called **toolbox_data/parsers** and shall be Excel files in the .xlsx format. 
The file name must end with the string **_parser.xlsx**.

    - PlanktonToolbox_ver_1_0_0_Windows_YYYY-MM-DD
        - PlanktonToolbox.exe 
        - toolbox_data 
            - cache 
            - code_lists 
            - img 
            - species 
            - parsers 
                - sharkweb_phytoplankton_parser.xlsx
                - sharkweb_zooplankton_parser.xlsx

On Windows and Ubuntu the directory named **toolbox_data** should be a directory folder located in the same folder as the executable file. 
On MacOS the directory should be moved to the **user directory**.


## The internal memory model ##

The internal memory model for each imported dataset is a tree structure where the nodes are:
  * **Dataset** One for each imported dataset.
  * **Visit** One for each sampling event (place/position and time).
  * **Sample** On for each sample or unit for analysis.
  * **Variable** A number of parameter values from the sample.

Each node contains a key/value list where all needed data from the dataset can be stored. 
Some fields are mandatory if the analysis part of Plankton Toolbox should work properly.

Mandatory fields on the **visit** node level:
  * sample_date
  * visit_month
  * station_name

Mandatory fields on the **sample** node level:
  * sample_min_depth_m
  * sample_max_depth_m

Mandatory fields on the **variable** node level:
  * scientific_name
  * size_class (for phytoplankton)
  * tropic_level (for phytoplankton)
  * sex (for zooplankton)
  * stage (for zooplankton)
  * parameter
  * value
  * unit