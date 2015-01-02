#!/bin/bash
#A simple script to recompile repdigits.c,
#for those that don't know how to use the distutils 
#repdigits_setup.py file.

#Requires gcc.

./repdigits_setup.py build
cp build/lib.*/repdigits*.so repdigits.so
rm -r build
