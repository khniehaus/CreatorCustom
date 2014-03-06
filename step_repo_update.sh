#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
export MAKEHUMAN_HG_DIR=makehuman_hg

# HG checkout or update
if [ -d $MAKEHUMAN_HG_DIR ]
then
echo Updating MakeHuman source code:
cd $MAKEHUMAN_HG_DIR
hg pull && hg update
cd ..
else
echo Checking out MakeHuman source code:
echo NOTE: Once it reaches the -adding file changes- step, it will appear to be frozen while it downloads the entire MakeHuman repository, be patient and wait for it to complete. Once you have downloaded the repository, it will only need to download updates as required in the future...
hg clone https://bitbucket.org/MakeHuman/makehuman $MAKEHUMAN_HG_DIR
fi
