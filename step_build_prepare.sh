#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export SCRIPTDIR=`pwd`
export MAKEHUMAN_HG_DIR=$SCRIPTDIR/makehuman_hg
export BUILD_DIR=$SCRIPTDIR/xbuild
export PYTHONPATH=/Library/Frameworks/Python.framework/Versions/2.7

# Ensure HG source tree exists
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

if [ ! -d $MAKEHUMAN_HG_DIR/buildscripts ]
then
echo "Buildscripts folder not found in: $MAKEHUMAN_HG_DIR/buildscripts"
exit 1
fi

# Run the MakeHuman release preparation script
echo Running build prepare scripts
echo
cd $MAKEHUMAN_HG_DIR/buildscripts
if [ ! -f $MAKEHUMAN_HG_DIR/makehuman/numpy ]
then
	ln -s $SCRIPTDIR/core_dependencies/numpy $MAKEHUMAN_HG_DIR/makehuman
fi

python build_prepare.py $MAKEHUMAN_HG_DIR $BUILD_DIR
unlink $MAKEHUMAN_HG_DIR/makehuman/numpy

if [ ! -d $BUILD_DIR/makehuman ]
then
echo "Build_prepare failed, output folder not found in: $BUILD_DIR/makehuman"
exit 1
fi

# Retrieve useful information from build_prepare in env variables
export MAKEHUMAN_VERSION=$(python get_build_prepare_output_var.py -t 0 $MAKEHUMAN_HG_DIR/.build_prepare.out 'version')
export MAKEHUMAN_BUILD_TYPE=$(python get_build_prepare_output_var.py -t 0 $MAKEHUMAN_HG_DIR/.build_prepare.out 'type')

# Switch to exported directory and remove the makehuman startup script as it confuses py2app
echo
echo Preparing the exported build directory
cd $BUILD_DIR/makehuman
rm makehuman

# Remove icons directory since it is only a partial copy of the directory, then symlink the full directory
rm -rf icons
if [ ! -f $BUILD_DIR/makehuman/icons ]
then
	ln -s $MAKEHUMAN_HG_DIR/makehuman/icons $BUILD_DIR/makehuman/icons
fi

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

cd $SCRIPTDIR
