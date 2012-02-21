#!/usr/bin/env python
""" 
Project: Plankton Toolbox. http://plankton-toolbox.org

Creates single file package for MS Windows: plankton_toolbox.exe

Command to execute this setup file: 
python py2exe_setup.py py2exe

"""

from distutils.core import setup
#import py2exe
setup(
  windows=[{"script":"plankton_toolbox.pyw"}],
  zipfile=None,
  options={
    "py2exe":{
      "bundle_files":1,
      "dll_excludes": ["MSVCP90.dll"],
	  "includes":["sip"],
    }
  }
)
