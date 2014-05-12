#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run all the steps needed to prepare the Mac OS X MakeHuman app
if [ "$MH_OSX_SKIP_HG_UPDATE" != "true" ]
then
    ./step_repo_update.sh
fi
echo
. ./step_build_prepare.sh
echo
./step_compile_app.sh
echo
./step_prepare_dist.sh
echo
