#!/bin/bash
# Program: backup.sh
# Call: ./backup.sh
# Description: File backup program
# Author: S. Joist
# Version: 1.0
# Date: 14.08.2022
#


# Current date
# Used to name the BackUp file
cur_date=$(date +%Y_%m_%d)

dir="/home"

# Create Full-Backup
clean_dir_name=$(echo $dir | tr "/" "_")
tar -czf /tmp/${cur_date}${clean_dir_name}_full_backup.tar.gz $dir

# Safe the date
echo $2 >/tmp/full_backup$clean_dir_name

# Log BackUp events
echo -e "Successfully created a new Full BackUp of $dir\n" >>/tmp/full_backup${clean_dir_name}.log

# Delete BackUp after it was send to the server
rm /tmp/${cur_date}${clean_dir_name}_full_backup.tar.gz

