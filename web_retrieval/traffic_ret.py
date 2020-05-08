# Traffic Retrieval script.
# The purpose of this script is to directly rip information off
# of WADOT's website in order to provide information to 
# this project.

# Scrape all information from WSDOT, which contains information for all major highways,
# and places them all in a single file.
from bs4 import BeautifulSoup
import requests
import string
import fileinput
import os.path
from os import path
import sys

# Grab URLs for the pages we are going to use to scrape information from.
url_tac = 'https://www.wsdot.com/traffic/trafficalerts/tacoma.aspx'
url_wsdot = 'https://www.wsdot.com/traffic/trafficalerts/printer.aspx'

# STATEWIDE information regarding traffic in major Highways
try:
    traffic_raw_wsdot = requests.get(url_wsdot)
except requests.exceptions.RequestException as e:
    export_data = open("data_all", "w+")
    export_data.write("No connection \n")
    print("No connection for all")
    export_data.close()
    export_tacoma_data = open("tacoma_data", "w+")
    export_tacoma_data.write("No connection \n")
    print("No connection to get Tacoma data")
    export_tacoma_data.close()
    raise SystemExit(e)

traffic = BeautifulSoup(traffic_raw_wsdot.text, 'html.parser')
# Remove any and all <a> elements in the page
[x.extract() for x in traffic.find_all('a')]

# Find all div's that contain the information we want...
all_useful_info = traffic.find("div", class_="printerList")

# Then print the output... (when uncommented)
all_data_cont = all_useful_info.get_text()
#print(all_data_cont)

# Once we get our data, we must put it in a file
export_data = open("data_all", "w+")
export_data.write(all_data_cont)
export_data.close()

# Remove the IMPACTs
#counter = 0
#for line in fileinput.input('data_all', inplace=True):
#    if not counter:
#        if line.startswith('HIGHEST IMPACT'):
#            counter = 1
#        else:
#            print(line, end='')
#    else:
#        counter -= 1
#
#counter = 0
#for line in fileinput.input('data_all', inplace=True):
#    if not counter:
#        if line.startswith('HIGH IMPACT'):
#            counter = 1
#        else:
#            print(line, end='')
#    else:
#        counter -= 1
#
#counter = 0
#for line in fileinput.input('data_all', inplace=True):
#    if not counter:
#        if line.startswith('MODERATE IMPACT'):
#            counter = 1
#        else:
#            print(line, end='')
#    else:
#        counter -= 1
#
#counter = 0
#for line in fileinput.input('data_all', inplace=True):
#    if not counter:
#        if line.startswith('LOW IMPACT'):
#            counter = 1
#        else:
#            print(line, end='')
#    else:
#        counter -= 1
#
#counter = 0
#for line in fileinput.input('data_all', inplace=True):
#    if not counter:
#        if line.startswith('LOWEST IMPACT'):
#            counter = 1
#        else:
#            print(line, end='')
#    else:
#        counter -= 1


# The following section is for traffic in Tacoma
try:
    traffic_raw_tac = requests.get(url_tac)
except requests.exceptions.RequestException as e:
    export_tacoma_data = open("tacoma_data", "w+")
    export_tacoma_data.write("No connection \n")
    raise SystemExit(e)

tacoma_traffic = BeautifulSoup(traffic_raw_tac.text, 'html.parser')
# Remove any and all <a> elements in the page
[x.extract() for x in tacoma_traffic.find_all('a')]
[x.extract() for x in tacoma_traffic.find("div", class_="situationHeader")]

#with open("tacoma.aspx") as tacomapage:
#    tacoma_traffic = BeautifulSoup(tacomapage, features="html5lib")
#    # The following two lines remove all <a> elements, and then all <div> elements with the
#    # "situationHeader" class
#    [x.extract() for x in tacoma_traffic.find_all('a')]
#    [x.extract() for x in tacoma_traffic.find("div", class_="situationHeader")]

# Find all of the <div> elements with the "situationDiv" class. These contain
# the desired information in this website's case.
all_tacoma_info = tacoma_traffic.find("div", class_="situationDiv")
#print(all_tacoma_info)

# Grab all text after parsing is complete.
tacoma_data_cont = all_tacoma_info.get_text()

# Remove the whitespace in the beginning of the output for traffic.
tacoma_data_final = tacoma_data_cont.lstrip()
#print(tacoma_data_final)

# Export all of the above work into a file
export_tacoma_data = open("tacoma_data", "w+")
export_tacoma_data.write(tacoma_data_final)
export_tacoma_data.close()

# For whatever reason, the file printed contains unnecessary \n, so we will be modifying
# the file to remove them
counter = 0
for line in fileinput.input('tacoma_data', inplace=True):
    if not counter:
        if line.startswith('HIGHEST IMPACT'):
            counter = 3
        else:
            print(line, end='')
    else:
        counter -= 1

counter = 0
for line in fileinput.input('tacoma_data', inplace=True):
    if not counter:
        if line.startswith('HIGH IMPACT'):
            counter = 3
        else:
            print(line, end='')
    else:
        counter -= 1

counter = 0
for line in fileinput.input('tacoma_data', inplace=True):
    if not counter:
        if line.startswith('MODERATE IMPACT'):
            counter = 3
        else:
            print(line, end='')
    else:
        counter -= 1

counter = 0
for line in fileinput.input('tacoma_data', inplace=True):
    if not counter:
        if line.startswith('LOW IMPACT'):
            counter = 3
        else:
            print(line, end='')
    else:
        counter -= 1

counter = 0
for line in fileinput.input('tacoma_data', inplace=True):
    if not counter:
        if line.startswith('LOWEST IMPACT'):
            counter = 3
        else:
            print(line, end='')
    else:
        counter -= 1
