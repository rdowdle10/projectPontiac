#!/bin/bash

# Simple script that scans for nearby bluetooth devices and stores results in a file
# to sort through. 

# Checking for a results file. This is temporary for the scanning of results. If it exists, it will be
# removed and then recreated later on in the script.

if [ -f scanres ] ; then
	echo 'Removing old results file...'
	rm scanres
    rm scanct
else
	echo 'Creating results file...'
	touch scanct
fi

# Ensuring that bluetooth is turned on.
bluetoothctl -- power on

# Scan for nearby devices for about 10 seconds and store results in afforementioned dictionary file
timeout 10 bluetoothctl -- scan on >> scanres

# Display results (CONSOLE USE ONLY)
cat scanres

# Now display any potential matches using the first filter in the console
if cat scanres | grep 00:06:66 ; then
	echo "Skimmer found!"
	date >> scanlog
	echo "The following possible skimmer(s) were detected: " >> scanlog
	cat scanres | grep 00:06:66 >> scanlog
	cat scanres | grep 00:06:66 >> scanct # This is purely for line counting purposes.
	echo "" >> scanlog
	echo "Skimmer logged!"
else
	date >> scanlog
	echo "No match found..." >> scanlog
	echo "" >> scanlog
	echo "No match found..."
fi