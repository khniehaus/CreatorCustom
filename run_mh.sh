#!/bin/bash

##
# Allows to run MakeHuman from source once the build script has been
# run once. Requires a step_build_prepare.sh to be executed first and a valid
# xbuild folder to be built.
##

echo "Running MakeHuman from source"

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export MH_SOURCE_PATH=xbuild
export SCRIPTDIR=`pwd`
export BUILD_DIR=$SCRIPTDIR/xbuild
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/2.7

# Override Python installation from OS
export PATH=$PYTHONPATH/bin:$PATH
echo Using: $(which python)

# Link core dependencies
if [ ! -f $BUILD_DIR/makehuman/numpy ]
then
	ln -s $SCRIPTDIR/core_dependencies/numpy $BUILD_DIR/makehuman/numpy
fi
if [ ! -f $BUILD_DIR/makehuman/OpenGL ]
then
	ln -s $SCRIPTDIR/core_dependencies/OpenGL $BUILD_DIR/makehuman/OpenGL
fi
if [ ! -f $BUILD_DIR/makehuman/PyQt4 ]
then
	ln -s $SCRIPTDIR/core_dependencies/PyQt4 $BUILD_DIR/makehuman/PyQt4
fi
if [ ! -f $BUILD_DIR/makehuman/sip.so ]
then
	ln -s $SCRIPTDIR/core_dependencies/sip.so $BUILD_DIR/makehuman/sip.so
fi
if [ ! -f $BUILD_DIR/makehuman/sipconfig.py ]
then
	ln -s $SCRIPTDIR/core_dependencies/sipconfig.py $BUILD_DIR/makehuman/sipconfig.py
fi

cd $MH_SOURCE_PATH/makehuman
python ./makehuman.py
