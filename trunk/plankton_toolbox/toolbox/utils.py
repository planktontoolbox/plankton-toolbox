#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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
This module contains utilities for the Plankton Toolbox project.
"""

import time

def singleton(cls):
    """
    This is an implementation of the Singleton pattern by using decorators.
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
    Normal logging is done by calling log('message').
    Tagged log rows can be of the types Info, Warning and Error.
    Similar log rows can be accumulated and printed with info about the number 
    of times they occurred. 
    """
    def __init__(self):
        self.__logtarget = None
        self.__accumulatedloggingactive = False
        self.__infoacc = {} # Contains accumulated info rows and counter.
        self.__warningacc = {} # Contains accumulated warnings and counter.
        self.__erroracc = {} # Contains accumulated errors and counter.
        
    def setLogTarget(self, target):
        """ Target must be an object containing a method named writeToLog(message). """
        self.__logtarget = target

    def clear(self):
        """ Clears all accumulated log rows. """
        self.__infoacc.clear()
        self.__warningacc.clear()
        self.__erroracc.clear()
        
    def log(self, message):
        """ Used for direct logging. """
        message = unicode(message)
        if self.__logtarget:
            self.__logtarget.writeToLog(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
        
    def info(self, message):
        """ Accumulates info rows. Increment counter if it already exists. """
        message = unicode(message)
        message = 'INFO: ' + message
        if self.__accumulatedloggingactive:
            if message in self.__info:
                self.__infoacc[message] += 1
            else:
                self.__infoacc[message] = 1
        else:
            self.log(message)

    def warning(self, message):
        """ Accumulates warnings. Increment counter if it already exists. """
        message = unicode(message)
        message = 'WARNING: ' + message
        if self.__accumulatedloggingactive:
            if message in self.__warningacc:
                self.__warningacc[message] += 1
            else:
                self.__warningacc[message] = 1
        else:
            self.log(message)
        
    def error(self, message):
        """ Accumulates errors. Increment counter if it already exists. """
        message = unicode(message)
        message = 'ERROR: ' + message
        if self.__accumulatedloggingactive:
            if message in self.__erroracc:
                self.__erroracc[message] += 1
            else:
                self.__erroracc[message] = 1
        else:
            self.log(message)
            
    def startAccumulatedLogging(self):
        """ """
        self.clear()
        self.__accumulatedloggingactive = True
        
    def logAllAccumulatedRows(self):
        """ """
        self.__accumulatedloggingactive = False
        self.log('Accumulated log summary:')
        self.logAllInfoRows()
        self.logAllWarnings()
        self.logAllErrors()        
        errorcount = sum(self.__erroracc.values())
        warningcount = sum(self.__warningacc.values())
        if errorcount == 0:
            self.log('- Errors: 0.')
        else:
            self.log('- ERRORS: ' + unicode(errorcount) + '.')
        if warningcount == 0:
            self.log('- Warnings: 0.')
        else:
            self.log('- WARNINGS: ' + unicode(warningcount) + '.')
        self.clear()
        
    def logAllInfoRows(self):
        """ Log all the content in the accumulated info row list. """
        for message in self.__infoacc:
            self.log('- ' + message + ' (' + unicode(self.__infoacc[message]) + ' times)')
        
    def logAllWarnings(self):
        """ Log all the content in the accumulated warning list. """
        for message in self.__warningacc:
            self.log('- ' + message + ' (' + unicode(self.__warningacc[message]) + ' times)')
        
    def logAllErrors(self):
        """ Log all the content in the accumulated error list. """
        for message in self.__erroracc:
            self.log('- ' + message + ' (' + unicode(self.__erroracc[message]) + ' times)')


