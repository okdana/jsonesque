# -*- coding: utf-8 -*-

"""
A pre-processor to normalise and minify JSON-like strings into valid JSON.

Supports the following enhancements to JSON:
  - Trailing commas in lists/dicts: [1, 2, 3,]
  - Single-line Python/shell-style comments: # my comment
  - Single-line C/JavaScript-style comments: // my comment
  - Multi-line/in-line C/JavaScript-style comments: /* my comment */

Heavily based on JSON.minify:
  https://github.com/getify/JSON.minify/tree/python
"""

from jsonesque.process import *

__name__         = 'jsonesque'
__description__  = 'Normalise and minify JSON-like strings into valid JSON'
__url__          = 'https://github.com/okdana/jsonesque/'
__author__       = 'dana geier'
__author_email__ = 'dana@dana.is'
__version__      = '0.1.1'
__license__      = 'MIT'

