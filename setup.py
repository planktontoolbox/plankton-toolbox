#!/usr/bin/env python
"""
Plankton Toolbox

Command to make a source distribution: 
python setup.py sdist
"""

from setuptools import setup, find_packages
setup(
	name='PlanktonToolbox',
	version='0.0.2',
	packages=find_packages(),
	scripts=['plankton_toolbox_start.py', 
			 'plankton_toolbox_start.pyw'],
	install_requires=['Openpyxl', 
					  'PyQt(>=4.4.0)'
					  ]
)
