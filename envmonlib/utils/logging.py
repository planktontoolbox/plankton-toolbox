#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import time
import envmonlib

@envmonlib.singleton
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
        """ Used for direct logging. Also used by other methods in the class. """
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
        errorcount = sum(self._erroracc.values())
        warningcount = sum(self._warningacc.values())
        #
        if (errorcount > 0) or (warningcount > 0):
            self._accumulatedloggingactive = False
            self.log('Accumulated log summary:')
            self.logAllInfoRows()
            self.logAllWarnings()
            self.logAllErrors()        
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
            count = self._infoacc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')
        
    def getAllInfoRows(self):
        """ Returns a list of strings. """
        result = []
        for message in sorted(self._infoacc):
            count = self._infoacc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')
        return result
        
    def logAllWarnings(self):
        """ Log all the content in the accumulated warning list. """
        for message in sorted(self._warningacc):
            count = self._warningacc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')
        
    def getAllWarnings(self):
        """ Returns a list of strings. """
        result = []
        for message in sorted(self._warningacc):
            count = self._warningacc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')
        return result
        
    def logAllErrors(self):
        """ Log all the content in the accumulated error list. """
        for message in sorted(self._erroracc):
            count = self._erroracc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')

    def getAllErrors(self):
        """ Returns a list of strings. """
        result = []
        for message in sorted(self._erroracc):
            count = self._erroracc[message]
            if count == 1:
                self.log('- ' + message + '   (' + unicode(count) + ' time)')
            else:
                self.log('- ' + message + '   (' + unicode(count) + ' times)')
        return result


class DefaultLogTarget(object):
    """ """
    def __init__(self):
        """ """
        
    def writeToLog(self, message):
        """ """
        print(message)

