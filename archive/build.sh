#!/bin/bash

# This script is used to build the package for the project.
# It will create a tarball of the project and place it in the `gh-pages` directory.
# Usage: ./build.sh

# Check if the dist directory exists, if not create it
if [ ! -d "gh-pages" ]; then
  mkdir gh-pages
fi

# Create the zipfiles of the projects
python create_repository.py \
  --data_dir gh-pages \
  repo/plugin*

# Copy the zipfiles to the gh-pages directory
for zipfile in $(find repo/zips/ -name *.zip); do
  echo $zipfile
  fname=$(basename "$zipfile")
  cp ${zipfile} "gh-pages/${fname}"
done

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
