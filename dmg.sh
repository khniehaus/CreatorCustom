#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PACKAGE_NAME=makehumanhg-r$(hg identify -n makehuman_hg)-osx

# Work around a bug that sometimes causes error -5341 with hdiutil on
# Mavericks
#touch dist/.Trash
# Appears not to be enough, so we just add -size 500M as extra option
# (MH will not approach this size anytime soon)

if [ -n "$MAKEHUMAN_DMG_VOLNAME" ]
then
    export MAKEHUMAN_DMG_VOLNAME='MakeHuman for Mac OS X'
fi

# Package result from package.sh into a Mac OS X disk image (dmg)
echo Creating distributable disk image
hdiutil create $PACKAGE_NAME -srcfolder dist -volname "$MAKEHUMAN_DMG_VOLNAME" -size 500M

if [ ! -f "${PACKAGE_NAME}.dmg" ]
then
	echo "Creating DMG image failed, file not found: ${PACKAGE_NAME}.dmg"
	exit 1
fi

