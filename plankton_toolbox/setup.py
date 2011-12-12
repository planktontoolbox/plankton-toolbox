#!/usr/bin/env python
"""
Command to make a source distribution: 
python setup.py sdist
"""

from setuptools import setup, find_packages
setup(
	name='Plankton Toolbox',
	version='0.0.2',
	packages=find_packages(),
	scripts=['plankton_toolbox.py', 'plankton_toolbox.pyw'],
	install_requires=['Openpyxl']
)

#from distutils.core import setup
#setup(name='Plankton Toolbox',
#      version='0.0.2',
#      description='',
#      author='',
#      author_email='',
#      url='',
#      packages=['plankton_toolbox', 
#				'plankton_toolbox.toolbox', 
#				'plankton_toolbox.activities', 
#				'plankton_toolbox.tools', 
#				'plankton_toolbox.core', 
#				'plankton_toolbox.core.biology', 
#				'plankton_toolbox.core.map_projections', 
#				'plankton_toolbox.core.monitoring' 
#				],
#      install_requires=['Openpyxl']
#      )
