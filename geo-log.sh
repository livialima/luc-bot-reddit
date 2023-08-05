#!/bin/bash

# Extra script to capture Geolocation of visitors
# Used to create posts about challenge students, but not anymore.
# Only useful if running in the same server that runs bot_script.py

logfile='/var/log/apache2/access.log'
visitors='/tmp/visitors'
locations='/tmp/locations'

cat $logfile | grep -o "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" | sort | uniq > $visitors

while read line; do
        geoiplookup $line >> $locations
done < $visitors

cat $locations | cut -f 5- -d" " | sort | uniq | grep -v 'Address not found'
