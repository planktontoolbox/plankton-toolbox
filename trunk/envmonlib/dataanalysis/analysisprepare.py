#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import envmonlib

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
        # Step 1: Create lists of taxa (name, trophy, stage and sex) and parameters (parameter and unit).
        parameter_set = set()
        taxon_set = set()
        for visitnode in analysisdata.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData(u'parameter')
                    unit = variablenode.getData(u'unit')
                    if parameter:
                        parameter_set.add((parameter, unit))
                    taxonname = variablenode.getData(u'scientific_name')
                    trophy = variablenode.getData(u'trophy')
                    stage = variablenode.getData(u'stage')
                    sex = variablenode.getData(u'sex')
                    if taxonname:
                        taxon_set.add((taxonname, trophy, stage, sex))
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
                    parameter = variablenode.getData(u'parameter')
                    unit = variablenode.getData(u'unit')
                    taxon = variablenode.getData(u'scientific_name')
                    trophy = variablenode.getData(u'trophy')
                    stage = variablenode.getData(u'stage')
                    sex = variablenode.getData(u'sex')
                    sample_parameter_taxon_list.append(((parameter, unit), (taxon, trophy, stage, sex)))
                # Add missing variables.
                for itempairs in parameter_taxon_list:
                    if itempairs not in sample_parameter_taxon_list:
                        variable = envmonlib.VariableNode()
                        samplenode.addChild(variable)
                        variable.addData(u'scientific_name', itempairs[1][0])
                        variable.addData(u'trophy', itempairs[1][1])
                        variable.addData(u'stage', itempairs[1][2])
                        variable.addData(u'sex', itempairs[1][3])
                        variable.addData(u'parameter', itempairs[0][0])
                        variable.addData(u'value', float(0.0))
                        variable.addData(u'unit', itempairs[0][1])
