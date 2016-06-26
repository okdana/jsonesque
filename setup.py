#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import setuptools
import jsonesque

def read_file(path):
	return open(os.path.join(os.path.dirname(__file__), path)).read()

def main():
	setuptools.setup(
		name             = jsonesque.__name__,
		description      = jsonesque.__description__,
		url              = jsonesque.__url__,
		author           = jsonesque.__author__,
		author_email     = jsonesque.__author_email__,
		version          = jsonesque.__version__,
		license          = jsonesque.__license__,
		test_suite       = 'jsonesque.tests',
		packages         = setuptools.find_packages(),
		keywords         = ['json', 'json-like', 'comments', 'minify'],
		long_description = read_file('pypi_description.rst'),
		classifiers      = [
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 3',
			'Operating System :: OS Independent',
			'Intended Audience :: Developers',
			'Topic :: Software Development :: Libraries :: Python Modules',
			'Topic :: Software Development :: Pre-processors',
			'Topic :: Text Processing :: Filters',
			'Topic :: Utilities',
		],
	)

if __name__ == '__main__':
	main()

