#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run all the steps needed to prepare the Mac OS X MakeHuman app
./step_repo_update.sh
./step_build_prepare.sh
./step_compile_app.sh
./step_prepare_dist.sh
