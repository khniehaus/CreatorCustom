#!/bin/bash

echo "Creating OSX DMG image ..."

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PACKAGE_NAME=makehumanhg-r$(hg identify -n makehuman_hg)-osx

if [ -z "$MAKEHUMAN_DMG_VOLNAME" ]
then
    echo "MAKEHUMAN_DMG_VOLNAME variable not set, using default: MakeHuman for Mac OS X"
    export MAKEHUMAN_DMG_VOLNAME='MakeHuman for Mac OS X'
fi

echo "Summary of DMG properties:"
echo "  Volume name: $MAKEHUMAN_DMG_VOLNAME"
echo "  Output filename: ${PACKAGE_NAME}.dmg"

# Package result from package.sh into a Mac OS X disk image (dmg)
echo Creating distributable disk image
hdiutil create $PACKAGE_NAME -srcfolder dist -volname "$MAKEHUMAN_DMG_VOLNAME" -size 600M -format UDBZ

if [ ! -f "${PACKAGE_NAME}.dmg" ]
then
	echo "Creating DMG image failed, file not found: ${PACKAGE_NAME}.dmg"
	exit 1
fi

