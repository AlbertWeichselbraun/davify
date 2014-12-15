#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" install eWRT :) """
from setuptools import setup, find_packages

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="davify",
      version="0.0.1",
      description='Davify uploads mail attachments to webdav servers.',
      author='Albert Weichselbraun',
      author_email='albert@weichselbraun.net',
      url='http://weichselbraun.net',
      license="GPL3",
      package_dir={'': 'src'},

      ###########################################
      ## Run unittests
      test_suite='nose.collector',

      ###########################################
      ## Scripts
      #scripts=['src/eWRT/input/corpus/reuters/reuters.py' ],

      ###########################################
      ## Package List
      packages = find_packages('src'),
      install_requires = ['easywebdav>=1.2.0',]

)
