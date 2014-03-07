#!/bin/bash
export PACKAGE_NAME=makehumansvn-r$(hg identify -n makehuman_hg)-osx

# Package result from package.sh into a Mac OS X disk image (dmg)
echo Creating distributable disk image
hdiutil create $PACKAGE_NAME -srcfolder dist -volname 'MakeHuman for Mac OS X'

