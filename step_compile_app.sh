#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export MAKEHUMAN_HG_DIR=makehuman_hg
export BUILD_DIR=xbuild
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/2.7

# Ensure SVN source tree exists
if [ ! -d $BUILD_DIR ]
then
echo "MakeHuman not built to: $BUILD_DIR"
exit 1
fi

# Override Python installation from OS
export PATH=$PYTHONPATH/bin:$PATH
echo Using: $(which python)

# Set the bundle name
export MAKEHUMAN_APP_BUNDLE_NAME='MakeHuman'

cd $BUILD_DIR/makehuman

# Link py2app build dependencies
ln -s ../../setup.py setup.py
ln -s ../../build_dependencies/py2app py2app
ln -s ../../build_dependencies/altgraph-0.10.1-py2.7.egg altgraph-0.10.1-py2.7.egg
ln -s ../../build_dependencies/macholib-1.5-py2.7.egg macholib-1.5-py2.7.egg
ln -s ../../build_dependencies/modulegraph-0.10.2-py2.7.egg modulegraph-0.10.2-py2.7.egg
ln -s ../../build_dependencies/py2app-0.7.2-py2.7.egg py2app-0.7.2-py2.7.egg

# Run py2app (builds the makehuman.app)
python setup.py py2app

# Apply Mac OS X MakeHuman.app hacks to correct jpeg loading issue
rm dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Resources/qt.conf
macdeployqt dist/$MAKEHUMAN_APP_BUNDLE_NAME.app -verbose=0

cd ../../