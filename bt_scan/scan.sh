#!/bin/bash

# Simple script to scan nearby bluetooth devices, and store results in a file to sort through.
# This may or may not be replaced by a Python script...

# Check to see if scan results file exists. If it does, it will be removed.
if [ -f scanres ] ; then
	echo 'Removing old dictionaries...'
	rm scanres
else
	echo 'Creating dictionary file...'
fi

# Scanning for nearby devices:
echo 'Scanning...'
timeout 5 bluetoothctl -- scan on >> scanres
#sudo bluetoothctl -- scan off

# Then display results
cat scanres

# Now look for any matches to MAC Prefixes (Testing)

if cat scanres | grep 62:FB ; then
	echo "Skimmer found!"
	cat scanres | grep 62:FB >> detectedskimmer
else
	echo "No match found..."
fi
