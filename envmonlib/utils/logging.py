#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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

import time
from envmonlib.utils import patterns

@patterns.singleton
class Logging(object):
    """
    Utility class for logging.
    Normal logging is done by calling log('message').
    Tagged log rows can be of the types Info, Warning and Error.
    Similar log rows can be accumulated and printed with info about the number 
    of times they occurred. 
    """
    def __init__(self):
        self._logtarget = None
        self._accumulatedloggingactive = False
        self._infoacc = {} # Contains accumulated info rows and counter.
        self._warningacc = {} # Contains accumulated warnings and counter.
        self._erroracc = {} # Contains accumulated errors and counter.
        #
        self.setLogTarget(DefaultLogTarget())
        
    def setLogTarget(self, target):
        """ Target must be an object containing a method named writeToLog(message). """
        self._logtarget = target

    def clear(self):
        """ Clears all accumulated log rows. """
        self._infoacc.clear()
        self._warningacc.clear()
        self._erroracc.clear()
        
    def log(self, message):
        """ Used for direct logging. """
        message = unicode(message)
        if message:
            if self._logtarget:
                self._logtarget.writeToLog(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
            else:
                # Use console if no target is defined.
                print(time.strftime("%Y-%m-%d %H:%M:%S") + ': ' + message)
        else:
            # Don't write time info if row is empty.
            if self._logtarget:
                self._logtarget.writeToLog(u"")
            else:
                print(u"")

        
    def info(self, message):
        """ Accumulates info rows. Increment counter if it already exists. """
        message = unicode(message)
        message = 'INFO: ' + message
        if self._accumulatedloggingactive:
            if message in self._infoacc:
                self._infoacc[message] += 1
            else:
                self._infoacc[message] = 1
        else:
            self.log(message)

    def warning(self, message):
        """ Accumulates warnings. Increment counter if it already exists. """
        message = unicode(message)
        message = 'WARNING: ' + message
        if self._accumulatedloggingactive:
            if message in self._warningacc:
                self._warningacc[message] += 1
            else:
                self._warningacc[message] = 1
        else:
            self.log(message)
        
    def error(self, message):
        """ Accumulates errors. Increment counter if it already exists. """
        message = unicode(message)
        message = 'ERROR: ' + message
        if self._accumulatedloggingactive:
            if message in self._erroracc:
                self._erroracc[message] += 1
            else:
                self._erroracc[message] = 1
        else:
            self.log(message)
            
    def startAccumulatedLogging(self):
        """ """
        self.clear()
        self._accumulatedloggingactive = True
        
    def logAllAccumulatedRows(self):
        """ """
        self._accumulatedloggingactive = False
        self.log('Accumulated log summary:')
        self.logAllInfoRows()
        self.logAllWarnings()
        self.logAllErrors()        
        errorcount = sum(self._erroracc.values())
        warningcount = sum(self._warningacc.values())
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
        for message in sorted(self._infoacc):
            self.log('- ' + message + '   (' + unicode(self._infoacc[message]) + ' times)')
        
    def logAllWarnings(self):
        """ Log all the content in the accumulated warning list. """
        for message in sorted(self._warningacc):
            self.log('- ' + message + '   (' + unicode(self._warningacc[message]) + ' times)')
        
    def logAllErrors(self):
        """ Log all the content in the accumulated error list. """
        for message in sorted(self._erroracc):
            self.log('- ' + message + '   (' + unicode(self._erroracc[message]) + ' times)')


class DefaultLogTarget(object):
    """ """
    def __init__(self):
        """ """
        
    def writeToLog(self, message):
        """ """
        print(message)

