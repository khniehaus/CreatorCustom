#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export SCRIPTDIR=`pwd`
export BUILD_DIR=$SCRIPTDIR/xbuild
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
if [ ! -f $BUILD_DIR/makehuman/setup.py ]
then
	ln -s $SCRIPTDIR/setup.py $BUILD_DIR/makehuman/setup.py
fi
if [ ! -L $BUILD_DIR/makehuman/py2app ]
then
	ln -s $SCRIPTDIR/build_dependencies/py2app $BUILD_DIR/makehuman/py2app
fi
if [ ! -f $BUILD_DIR/makehuman/altgraph-0.10.1-py2.7.egg ]
then
	ln -s $SCRIPTDIR/build_dependencies/altgraph-0.10.1-py2.7.egg $BUILD_DIR/makehuman/altgraph-0.10.1-py2.7.egg
fi
if [ ! -f $BUILD_DIR/makehuman/macholib-1.5-py2.7.egg ]
then
	ln -s $SCRIPTDIR/build_dependencies/macholib-1.5-py2.7.egg $BUILD_DIR/makehuman/macholib-1.5-py2.7.egg
fi
if [ ! -f $BUILD_DIR/makehuman/modulegraph-0.10.2-py2.7.egg ]
then
	ln -s $SCRIPTDIR/build_dependencies/modulegraph-0.10.2-py2.7.egg $BUILD_DIR/makehuman/modulegraph-0.10.2-py2.7.egg
fi
if [ ! -L $BUILD_DIR/makehuman/py2app-0.7.2-py2.7.egg ]
then
	ln -s $SCRIPTDIR/build_dependencies/py2app-0.7.2-py2.7.egg $BUILD_DIR/makehuman/py2app-0.7.2-py2.7.egg
fi

# Run py2app (builds the makehuman.app)
echo
echo Running py2app build
python setup.py py2app

if [ ! -d "$BUILD_DIR/makehuman/dist/${MAKEHUMAN_APP_BUNDLE_NAME}.app" ]
then
echo "Py2app failed to output to: $BUILD_DIR/makehuman/dist/${MAKEHUMAN_APP_BUNDLE_NAME}.app"
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

# Some checks to verify whether the package contains all required libraries
if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Frameworks/QtCore.framework/QtCore ]
then 
	echo 'Error: Missing QtCore component in app bundle'
	echo Verify by running macdeployqt verbose manually as jenkins user
	exit 1
fi
if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Frameworks/QtOpenGL.framework/QtOpenGL ]
then 
        echo 'Error: Missing QtOpenGL component in app bundle'
	echo Verify by running macdeployqt verbose manually as jenkins user
        exit 1
fi
if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/Frameworks/QtSvg.framework/QtSvg ]
then
        echo 'Error: Missing QtSvg component in app bundle'
        echo Verify by running macdeployqt verbose manually as jenkins user
        exit 1
fi

if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/PlugIns/imageformats/libqsvg.dylib ]
then
        echo 'Error: Missing Qt SVG image plugin in app bundle'
        echo Verify by running macdeployqt verbose manually as jenkins user
        exit 1
fi
if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/PlugIns/imageformats/libqjpeg.dylib ]
then
        echo 'Error: Missing Qt JPeG image plugin in app bundle'
        echo Verify by running macdeployqt verbose manually as jenkins user
        exit 1
fi
if [ ! -f dist/$MAKEHUMAN_APP_BUNDLE_NAME.app/Contents/PlugIns/codecs/libqjpcodecs.dylib ]
then
        echo 'Error: Missing Qt JPeG codec plugin in app bundle'
        echo Verify by running macdeployqt verbose manually as jenkins user
        exit 1
fi

cd $SCRIPTDIR
