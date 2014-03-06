#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export MAKEHUMAN_HG_DIR=makehuman_hg
export BUILD_DIR=xbuild
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/2.7

# Ensure SVN source tree exists
if [ ! -d $MAKEHUMAN_HG_DIR ]
then
echo "Source code not found in: $MAKEHUMAN_HG_DIR"
exit 1
fi

# Override Python installation from OS
export PATH=$PYTHONPATH/bin:$PATH
echo Using: $(which python)

# Remove old 'build' directories
echo Remove old build directory
rm -rf dist
rm -rf $BUILD_DIR
sleep 2

# Run the MakeHuman release preparation script
echo Running build prepare scripts
cd $MAKEHUMAN_HG_DIR/buildscripts
ln -s ../../core_dependencies/numpy ../makehuman
python build_prepare.py .. ../../$BUILD_DIR
rm ../makehuman/numpy

# Remove makehuman startup script as it confuses py2app, link icons, then link core makehuman dependencies
echo Preparing the exported build directory
cd ../../$BUILD_DIR/makehuman
rm makehuman
ln -s ../../$MAKEHUMAN_HG_DIR/makehuman/icons icons
ln -s ../../core_dependencies/numpy numpy
ln -s ../../core_dependencies/OpenGL OpenGL
ln -s ../../core_dependencies/PyQt4 PyQt4
ln -s ../../core_dependencies/sip.so sip.so
ln -s ../../core_dependencies/sipconfig.py sipconfig.py
cd ../../../../

