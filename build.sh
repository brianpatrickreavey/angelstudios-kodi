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


cat > gh-pages/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Angel Studios Kodi Downloads</title>
  <style>
    body { font-family: sans-serif; margin: 2em; }
    h1 { font-size: 1.5em; }
    ul { list-style: none; padding: 0; }
    li { margin: 0.5em 0; }
    a { text-decoration: none; color: #0366d6; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Angel Studios Kodi Downloads</h1>
  <ul>
EOF

for f in gh-pages/*.zip; do
  [ -e "$f" ] || continue
  fname=$(basename "$f")
  echo "    <li><a href=\"$fname\">$fname</a></li>" >> gh-pages/index.html
done

cat >> gh-pages/index.html <<EOF
  </ul>
</body>
</html>
EOF