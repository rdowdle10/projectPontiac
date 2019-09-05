#!/bin/bash

# This script simply downloads and places an image in the root directory of
# Project Pontiac. 

echo "Downloading traffic status image..."

# the following wget command has the q and O flags, where q suppresses output and 
# O overwrites the image in question if the command is run more than once.
wget -q https://images.wsdot.wa.gov/traffic/flowmaps/tacoma.png -O tacoma.png
