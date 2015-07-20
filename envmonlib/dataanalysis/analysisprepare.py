#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

# import envmonlib
import toolbox_utils
import toolbox_core

class AnalysisPrepare(object):
    """
    """
    def __init__(self):
        """ """
        # Initialize parent.
        super(AnalysisPrepare, self).__init__()


    def addMissingTaxa(self, analysisdata):
        """ """
        if not analysisdata:        
            return
        # Step 1: Create lists of taxa (name, trophic_type, stage and sex) and parameters (parameter and unit).
        parameter_set = set()
        taxon_set = set()
        for visitnode in analysisdata.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData('parameter')
                    unit = variablenode.getData('unit')
                    if parameter:
                        parameter_set.add((parameter, unit))
                    taxonname = variablenode.getData('scientific_name')
                    trophic_type = variablenode.getData('trophic_type')
                    stage = variablenode.getData('stage')
                    sex = variablenode.getData('sex')
                    if taxonname:
                        taxon_set.add((taxonname, trophic_type, stage, sex))
        # Step 2: Create list with parameter-taxon pairs.
        parameter_taxon_list = []
        for parameterpair in parameter_set:
            for taxonpair in taxon_set:
                parameter_taxon_list.append((parameterpair, taxonpair))
        # Step 3: Iterate over samples. 
        parameter_set = set()
        taxon_set = set()
        #
        for visitnode in analysisdata.getChildren():
            #
            for samplenode in visitnode.getChildren():
                sample_parameter_taxon_list = []
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData('parameter')
                    unit = variablenode.getData('unit')
                    taxon = variablenode.getData('scientific_name')
                    trophic_type = variablenode.getData('trophic_type')
                    stage = variablenode.getData('stage')
                    sex = variablenode.getData('sex')
                    sample_parameter_taxon_list.append(((parameter, unit), (taxon, trophic_type, stage, sex)))
                # Add missing variables.
                for itempairs in parameter_taxon_list:
                    if itempairs not in sample_parameter_taxon_list:
                        variable = toolbox_utils.VariableNode()
                        samplenode.addChild(variable)
                        variable.addData('scientific_name', itempairs[1][0])
                        variable.addData('trophic_type', itempairs[1][1])
                        variable.addData('stage', itempairs[1][2])
                        variable.addData('sex', itempairs[1][3])
                        variable.addData('parameter', itempairs[0][0])
                        variable.addData('value', float(0.0))
                        variable.addData('unit', itempairs[0][1])
