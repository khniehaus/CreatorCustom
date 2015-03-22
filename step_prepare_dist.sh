#!/bin/bash

echo "Preparing distribution ..."

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export SCRIPTDIR=`pwd`
export BUILD_DIR=$SCRIPTDIR/xbuild

# Ensure HG source tree exists
if [ ! -d $BUILD_DIR/makehuman/dist ]
then
echo "Built version of MakeHuman application not found in: $BUILD_DIR"
exit 1
fi

cd $BUILD_DIR/makehuman

echo Copying extra files in dist folder
# Copy extra files
cp license.txt dist/license.txt
cp -R blendertools dist/Blender\ Plugins
cp $SCRIPTDIR/extra_files/Install\ Blender\ Plugins.command dist
rm -f dist/Blender\ Plugins/*.bat

# Move dist folder into OS X builder location
mv $BUILD_DIR/makehuman/dist $SCRIPTDIR/dist

if [ ! -d "$SCRIPTDIR/dist" ]
then
echo "Py2app failed to output to: $SCRIPTDIR/dist"
exit 1
fi

cd $SCRIPTDIR

echo OSX build done
