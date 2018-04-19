#!/bin/bash

# Ensure we are working from the same directory this script is in
cd "$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
clear

export BLENDER_CONFIG_DIR=~/Library/Application\ Support/Blender
export CURRENT_WORKING_DIRECTORY=$(pwd)
export BLENDER_PLUGINS_DIR=$CURRENT_WORKING_DIRECTORY/Blender\ Plugins

# Check that the 'Blender Plugins' directory exists before proceeding
if [ ! -d "$BLENDER_PLUGINS_DIR" ]; then
echo
echo "Error: Could not find the plugins in the script directory. Please run this script from its original location..."
echo
exit 1
fi

# Display instructions
echo 'MAKEHUMAN PLUGIN INSTALLATION SCRIPT FOR BLENDER'
echo '------------------------------------------------'
echo 'This script will install the MakeHuman plugins for Blender to the appropriate locations in:'
echo "$BLENDER_CONFIG_DIR"
echo
echo 'To ensure this script is able to locate the correct path to install the plugins, you must run your'
echo 'version of Blender at least once and save the user preferences file. This can be done by clicking'
echo 'on "File"->"User Prefereneces". Then click the "Save User Settings" button on the bottom-left of'
echo 'the dialog. This will create the path to store configuration files and plugins for your version of'
echo 'Blender. This script will then be able to install the plugins to the correct path.'
echo
echo -n 'Do you want to proceed with the installation? [y/n]: '
read -n 1 ACCEPTED

if [ ! "$ACCEPTED" == "y" ] && [ ! "$ACCEPTED" == "Y" ]; then
  echo
  echo
  echo
  echo 'Installation aborted...'
  echo
  echo
  exit 0
fi

# For formatting reasons, we need a few spaces after the question since it remains on the original line
echo
echo
echo

# Ensure the Blender application support directory exists, then switch to it
if [ ! -d "$BLENDER_CONFIG_DIR" ]; then
  echo "Error: Could not find the Blender configuration path, did you follow the instructions above?"
  echo
  echo
  exit 1
fi
cd "$BLENDER_CONFIG_DIR"

# Copy plugins to each Blender configuration directory found
for D in *; do
if [ -d "${D}" ]; then
  # Make plugins directory if required and copy the blender plugins to that directory
  mkdir -p "${D}/scripts/addons"
  cp -Rf "$BLENDER_PLUGINS_DIR/" "${D}/scripts/addons"
  echo "  Copied plugins to: $BLENDER_CONFIG_DIR/${D}/scripts/addons"
  export SUCCESSFUL="TRUE"
fi
done

if [ ! "$SUCCESSFUL" == "TRUE" ]; then
  echo 'Error: Could not find any Blender configuration paths, did you follow the instructions above?'
  echo
  echo
  exit 1
fi

# Leave some spaces so the Logout message goes on its own line
echo
echo
echo 'Installation complete.'
echo
echo 'You will have to restart Blender and go back into the user preferences to enable the installed'
echo 'plugins. Also note that the MHX/MHX2 plugins are no longer officially supported. If you require'
echo 'these plugins you will have to install them yourself. More information available at:'
echo 'http://www.makehuman.org/doc/faq/where_is_mhx_exporter.html'
echo
echo