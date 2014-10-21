#!/bin/bash

##
# Allows to run MakeHuman from source once the build script has been
# run once. Requires a step_build_app.sh to be executed first and a valid
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

cd $MH_SOURCE_PATH/makehuman
python ./makehuman.py
