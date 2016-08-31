# Plankton Toolbox #

The Plankton Toolbox is a free tool for aquatic scientists, and others, working with environmental monitoring related to phyto- and zooplankton.

## Features ##

  * Imports phyto- or zooplankton data in .txt and .xlsx files in different formats (configurable)
  * Work with data on abundance, biovolume and carbon content
  * Data screening - quality control of data
  * Aggregate data, e.g. from species level to class level
  * Plotting tools
  * Statistics (in early development)
  * Export data in .txt or .xlsx for further analyses or plotting
  * A future update will include functionality for using Plankton Toolbox as a counting tool by the microscope

## Downloads ##

Plankton Toolbox version 1.0.0 is available for MacOS and Windows at:

http://nordicmicroalgae.org/tools

## Platforms ##
Plankton Toolbox is available for MacOS and Windows. (Ubuntu on request.)

Plankton Toolbox is also possible to run directly from Python.
The program is developed in Python 2.7 and Qt/PyQt4. Released under the MIT license.
More info: [For developers](https://code.google.com/p/plankton-toolbox/wiki/ForDevelopers)


## Do we need more tools? ##

There are many tools available for data analysis and statistics, for example R for statistics and Primer for ecological multivariate statistics. Especially if you are working with time series there is no need to develop your own tool.

When working with plankton samples from environmental monitoring there are some recurring problems that take a lot of time before you can use your favourite standard analysis and plotting tool. Plankton Toolbox tries to address these initial time consuming steps in your analysis work.

## Why is it called a “toolbox”? ##

We have identified some areas where we need tool support when working with plankton data. If these tools are but together in a “toolbox” it is easier to make the parts interact with each other, compared to developing separate tools for different tasks.

## Plankton Toolbox characteristics ##

Plankton Toolbox does not have ambitions to be a complete tool for all types of analyses. As soon as the user wants to analyse further in other tools there should be possibilities to export data from the various steps in the analysis part. For some commonly used tools there are custom exports formats (e.g. for Primer).

Plankton Toolbox is not build to support analysis of time series and environmental monitoring data is often hard to translate to time series. They are often sampled with low frequency or sometimes just once at a specific place. From one sample a large number of parameter values are extracted, grouped by species name, sizeclasses, development stage, etc.

Plankton Toolbox is delivered with preloaded species lists and species related data.

Plankton Toolbox contains a flexible mechanism for importing and parsing different kind of datasets.

The analysis part of Plankton Toolbox is adapted for the special needs associated with plankton analyses.

## Where can current version be best used? ##

Our users so far are mainly Phytoplankton experts working with marine monitoring in the seas surrounding Sweden. Plankton Toolbox is preloaded with taxonomic information, size-class related information and dataset parsers. There is also some test datasets downloaded from SHARKweb (http://sharkweb.smhi.se).

For Zooplankton users there is a preliminary taxonomic classification embedded for test purposes.

## Adjustments needed for other datasets ##

If the set of species in datasets does not match the preloaded set of species and your data not is downloaded from SHARKweb, then some work is needed.
1.	The dataset parsers should be rewritten or adjusted.
2.	The species lists should be replaced and/or adjusted.
3.	Dataset parsers must be adjusted to use species information available in the dataset.

How to do this is described in the sections below.

## Free software ##

The software developed for Plankton Toolbox is open and free software. More information is available
in the "For developers" section.

## Future development ##

Plankton Toolbox is under constant development, and should be as long as there is need for more functionality and features. User needs should govern the further development of Plankton Toolbox.