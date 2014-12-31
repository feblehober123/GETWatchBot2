#!/usr/bin/env python2
# setup file for RepDigits module

from distutils.core import setup, Extension

module1 = Extension('repdigits',
    sources = ['repdigits.c'])

setup (name = 'RepDigits',
    version = '0.3',
    description = 'Python module for my efficient GET functions',
    ext_modules = [module1])
