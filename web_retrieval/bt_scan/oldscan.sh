#!/bin/bash

# Simple script to scan nearby bluetooth devices, and store results in a file to sort through.
# This may or may not be replaced by a Python script...

# Check to see if scan results file exists. If it does, it will be removed.
if [ -f scanres ] ; then
	echo 'Removing old results file...'
	rm scanres
else
	echo 'Creating results file...'
fi

# Scanning for nearby devices:
echo 'Scanning...'
timeout 10 bluetoothctl -- scan on >> scanres
#sudo bluetoothctl -- scan off

# Then display results
cat scanres

# Now look for any matches to MAC Prefixes (Testing)

if cat scanres | grep 45:1D ; then
	echo "Skimmer found!"
	date >> scanlog
	echo "The following possible skimmer(s) were detected: " >> scanlog
	cat scanres | grep 45:1D >> scanlog
	cat scanres | grep 45:1D >> scanct # This is purely for line counting purposes.
	echo "" >> scanlog
else
	date >> scanlog
	echo "No match found..." >> scanlog
	echo "" >> scanlog
	echo "No match found..."
fi
