#!/bin/bash

# Useful to clean working dir up if something goes wrong

rm -rf xbuild
rm -rf dist

# Cleanup symlinks
find . -type l -exec rm {} \;

# Cleanup pyc files
find . -iname \*.pyc -exec rm {} \;
