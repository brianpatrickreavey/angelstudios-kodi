#!/bin/bash

# This script is used to build the package for the project.
# It will create a tarball of the project and place it in the dist directory.
# Usage: ./build.sh

# Check if the dist directory exists, if not create it
if [ ! -d "gh-pages" ]; then
  mkdir gh-pages
fi

# Check if the version file exists, if not create it
if [ ! -f "version.txt" ]; then
  echo "0.0.1" > version.txt
fi

# Read the version from the version file
VERSION=$(cat version.txt)
# Update the addon.xml file with the current version
sed -i "/plugin.video.angelstudios/ s/\(version=\"\)[^\"]*\(\"\)/\1$VERSION\2/" plugin.video.angelstudios/addon.xml

# Create a zipfile of the project
zip -r "gh-pages/plugin.video.angelstudios-$VERSION.zip" plugin.video.angelstudios -x "*.git*" "dist/*" "package.sh" "version.txt"
