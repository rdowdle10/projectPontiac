#!/bin/bash
reset
echo " (                             (                              ";
echo " )\ )                      )   )\ )             )             ";
echo "(()/((       (    (     ( /(  (()/(          ( /((     )      ";
echo " /(_))(   (  )\  ))\ (  )\())  /(_))(   (    )\())\ ( /(  (   ";
echo "(_))(()\  )\((_)/((_))\(_))/  (_))  )\  )\ )(_))((_))(_)) )\  ";
echo "| _ \((_)((_) !(_)) ((_| |_   | _ \((_)_(_/(| |_ (_((_)_ ((_) ";
echo "|  _| '_/ _ \| / -_/ _||  _|  |  _/ _ | ' \)|  _|| / _\` / _|  ";
echo "|_| |_| \____/ \___\__| \__|  |_| \___|_||_| \__||_\__,_\__|  ";
echo "           |__/                                               ";

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Begin the gathering of Traffic Data here:
# Download source code of WADOT web page
rm default.aspx
wget -q https://www.wsdot.com/traffic/tacoma/default.aspx -O default.aspx

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Remove previous output from both blocked traffic and special events
rm blockedtraffic
rm specialevents
rm volumelevel
rm tacoma.png

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Filter information from output and write to blockedtraffic file
#cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "<>/\n\t" >> specialevents
if [ -f default.aspx ] ; then
    cat default.aspx | grep -i -A 2 SpecialU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "<>/\n\t" >> specialevents
else 
    echo "Traffic information is not available at this time" >> specialevents
fi
# Filter information from output and write to specialevents file
#cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "'</>\t\r'">> blockedtraffic
if [ -f default.aspx ] ; then
    cat default.aspx | grep -i -A 2 BlockingU | grep li | cut -b 29-500 | sed "s/'</li>'/" | tr -d "'</>\t\r'">> blockedtraffic
else 
    echo "Traffic information is not available at this time" >> blockedtraffic
fi

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Download the map for traffic

wget -q https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png tacoma.png

if [ -f tacoma.png ] ; then
    echo "Data download complete..."
else
    cp no_connection.png tacoma.png
fi


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Once that is done, insert any pre-startup scripts below:

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Restore volume level on volume slider:
amixer sget Master | grep 'Right:' | awk -F'[][]' '{ print $2 }' | rev | cut -c 2- | rev | tr -d " \t\n\r" >> volumelevel
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Begin the main interface:
echo "starting main program"

python main.py
