#!/bin/bash
# Script is intended to be run when the application is open
# Update the map shown in the traffic page
rm default.aspx
rm tacoma.png
rm specialevents
rm blockedtraffic

wget -q https://www.wsdot.com/traffic/tacoma/default.aspx -O default.aspx

wget -q https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png tacoma.png

if [ -f tacoma.png ] ; then
    echo "Data download complete..."
else
    cp no_connection.png tacoma.png
fi

# Update the information shown in the traffic page.

# Filter information from output and write to blockedtraffic file
cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "<>/\n\t" >> specialevents
if [ -f default.aspx ] ; then
    rm specialevents
    cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "<>/\n\t" >> specialevents
    echo "Special Events notices updated"
else 
    echo "Traffic information is not available at this time" >> specialevents
fi
# Filter information from output and write to specialevents file
cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "'</>\t\r'">> blockedtraffic
if [ -f default.aspx ] ; then
    rm blockedtraffic
    cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "'</>\t\r'">> blockedtraffic
    echo "Blocked traffic notices updated"

else 
   echo "Traffic information is not available at this time" >> blockedtraffic
fi