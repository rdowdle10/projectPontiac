#!/bin/bash

# Begin the gathering of Traffic Data here:

# Download source code of WADOT web page
wget -q https://www.wsdot.com/traffic/tacoma/default.aspx -O default.aspx
# Remove previous output from both blocked traffic and special events
rm blockedtraffic
rm specialevents
rm volumelevel

# Filter information from output and write to blockedtraffic file
cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/" >> blockedtraffic
# Filter information from output and write to specialevents file
cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/" >> specialevents
# Download the map for traffic
wget -q https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png -O tacoma.png

sleep 1s

# Once that is done, insert any pre-startup scripts below:

# Restore volume level on volume slider:
amixer sget Master | grep 'Right:' | awk -F'[][]' '{ print $2 }' | rev | cut -c 2- | rev | tr -d " \t\n\r" >> volumelevel

# Begin the main interface:
echo "starting main program"
sleep 1s
python main.py
