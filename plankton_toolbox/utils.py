#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module contains utilities for the Plankton toolbox project.
"""

import time

def singleton(cls):
    """
    This is an implementation of the Singleton pattern by using decorator.
    Usage example:
        @singleton
        class MyClass:
           ...               
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Logger(object):
    """
    Utility class for logging.
    Info are used for direct logging, and errors and warnings are accumulated. 
    """
    def __init__(self):
        self.__logtarget = None
        self.__errors = {} # Contains accumulated errors and counter.
        self.__warnings = {} # Contains accumulated warnings and counter.
        
    def setLogTarget(self, target):
        """ Target must be an object containing a method named writeToLog. """
        self.__logtarget = target

    def clear(self):
        """ """
        self.__errors.clear()
        self.__warnings.clear()
        
    def error(self, message):
        """ Accumulates errors. Increment counter if it alredy exists. """
        message = 'ERROR: ' + message
        if message in self.__errors:
            self.__errors[message] += 1
        else:
            self.__errors[message] = 1
        
    def warning(self, message):
        """ Accumulates warnings. Increment counter if it alredy exists. """
        message = 'WARNING: ' + message
        if message in self.__warnings:
            self.__warnings[message] += 1
        else:
            self.__warnings[message] = 1
        
    def info(self, message):
        """ Used for direct logging. """
        if self.__logtarget:
            self.__logtarget.writeToLog(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
        
    def getError(self):
        """ """
        return self.__errors
        
    def getWarning(self):
        """ """
        return self.__warnings
        
    def logAllErrors(self):
        """ Log all the content in the accumulated error list. """
        for message in self.__errors:
            self.info(message + ' (' + unicode(self.__errors[message]) + ' times)')
        
    def logAllWarnings(self):
        """ Log all the content in the accumulated warning list. """
        for message in self.__warnings:
            self.info(message + ' (' + unicode(self.__warnings[message]) + ' times)')
        
        
