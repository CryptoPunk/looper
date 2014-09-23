#!/usr/bin/env python
from setuptools import setup
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'lib'))
import looper

setup(name='looper',
      version=looper.__version__,
      description='A library for generating test cases',
      author='Max Vohra',
      author_email='max@seattlenetworks.com',
      url='http://seattlenetworks.com/',
      license="GNU General Public License v3 (GPLv3)",
      packages=['looper'],
     )

