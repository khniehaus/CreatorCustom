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

if [ ! -d $BUILD_DIR/makehuman ]
then
echo "MakeHuman not built to: $BUILD_DIR/makehuman"
exit 1
fi

cd $BUILD_DIR/makehuman

# Link py2app build dependencies
if [ ! -a setup.py ]
then
	ln -s ../../setup.py setup.py
fi
if [ ! -a py2app ]
then
	ln -s ../../build_dependencies/py2app py2app
fi
if [ ! -a altgraph-0.10.1-py2.7.egg ]
then
	ln -s ../../build_dependencies/altgraph-0.10.1-py2.7.egg altgraph-0.10.1-py2.7.egg
fi
if [ ! -a macholib-1.5-py2.7.egg ]
then
	ln -s ../../build_dependencies/macholib-1.5-py2.7.egg macholib-1.5-py2.7.egg
fi
if [ ! -a modulegraph-0.10.2-py2.7.egg ]
then
	ln -s ../../build_dependencies/modulegraph-0.10.2-py2.7.egg modulegraph-0.10.2-py2.7.egg
fi
if [ ! -a py2app-0.7.2-py2.7.egg ]
then
	ln -s ../../build_dependencies/py2app-0.7.2-py2.7.egg py2app-0.7.2-py2.7.egg
fi

# Run py2app (builds the makehuman.app)
echo
echo Running py2app build
python setup.py py2app

if [ ! -d dist/$MAKEHUMAN_APP_BUNDLE_NAME.app ]
then
echo "Py2app failed to output to: dist/$MAKEHUMAN_APP_BUNDLE_NAME.app"
exit 1
fi

# Apply Mac OS X MakeHuman.app hacks to correct jpeg loading issue
echo
echo Running macdeployqt
if [ -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Resources/qt.conf ]
then
	rm dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Resources/qt.conf
fi
macdeployqt dist/$MAKEHUMAN_APP_BUNDLE_NAME.app -verbose=0
echo Deploying qtSvg component
# Since macdeployqt cannot detect which modules a pyqt project needs,
# we copy them manually
cp /Developer/Applications/Qt/plugins/imageformats/libqsvg.dylib dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/PlugIns/imageformats/
# Important: simply copying the required plugins over WILL make the
# application crash when running, to fix it we run macdeployqt again.
macdeployqt dist/$MAKEHUMAN_APP_BUNDLE_NAME.app -verbose=0

cd ../../
