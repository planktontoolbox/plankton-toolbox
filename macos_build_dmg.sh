#!/bin/sh

# Create a target folder for dmg.
mkdir -p dist/dmg
rm -r dist/dmg/*

# Copy the app.
cp -r dist/PlanktonToolbox-macOS.app dist/dmg

# Create the dmg.
create-dmg \
  --volname "PlanktonToolbox" \
  --volicon img/plankton_toolbox_icon.ico \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "PlanktonToolbox-macOS.app" 175 120 \
  --hide-extension "PlanktonToolbox-macOS.app" \
  --app-drop-link 425 120 \
  "dist/dmg/PlanktonToolbox-macOS.dmg" \
  "dist/dmg/"
