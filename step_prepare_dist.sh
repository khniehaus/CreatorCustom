#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export BUILD_DIR=xbuild

# Ensure SVN source tree exists
if [ ! -d $BUILD_DIR/makehuman/dist ]
then
echo "Built version of MakeHuman application not found in: $BUILD_DIR"
exit 1
fi

cd $BUILD_DIR/makehuman

# Copy extra files
cp license.txt dist/license.txt
cp -R blendertools dist/Blender\ Plugins
rm -f dist/Blender\ Plugins/*.bat

# Move dist folder into OS X builder location
mv dist ../../dist

cd ../../