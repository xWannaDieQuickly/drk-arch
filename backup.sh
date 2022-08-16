#!/bin/bash
# Program: backup.sh
# Call: ./backup.sh [option]
#		-d = save the backup on a disk / harddrive
#		-l = save the backup locally
# Description: File backup program
# Author: S. Joist
# Version: 1.0
# Date: 14.08.2022
#

# Full BackUp of given directory
# Args:
# 1: Directory
# 2: Current date
full_backup() {

	# Check if directory exists
	if [ ! -d "$1" ]; then
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory).\n"
		return
	fi

	# Create Full-Backup
	clean_dir_name=$(echo $1 | tr "/" "_")
	tar -czf /tmp/${2}${clean_dir_name}_full_backup.tar.gz $1

	# Safe the date
	echo $2 >/tmp/full_backup$clean_dir_name

	# Delete BackUp after it was send to the server
	# rm /tmp/${2}${clean_dir_name}_full_backup.tar.gz

}

# Incremental BackUp of given directory
# Args:
# 1: Directory
# 2: Current date
incremental_backup() {

	# Check if directory exists
	if [ ! -d "$1" ]; then
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory).\n"
		return
	fi

	clean_dir_name=$(echo $1 | tr "/" "_")

	# Check if a full Back-Up of the given directory has already been created
	# If no, create full Back-Up instead of incremental Back-Up
	if [ ! -f "/tmp/${2}${clean_dir_name}_full_backup.tar.gz" ]; then
		full_backup $1 $2
		return
	fi

	# Create new incremental BackUp
	tar -cz --after-date=$last_full_backup -f /tmp/${2}${clean_dir_name}_inc_backup.tar.gz $1

	# Delete BackUp after it was send to the server
	# rm /tmp/${2}${clean_dir_name}_inc_backup.tar.gz

}

# Save the Back-Up as Archive to a disk
# Args:
# 1: Directory
# 2: Current date
# 3: Disk / Harddrive
save_to_disk() {

	# Check if disk exists
	if [ ! -d "$3" ]; then
		echo -e "$3 does not exist. Please enter a valid disc (/path/to/disk).\n"
		return
	fi

	clean_dir_name=$(echo $1 | tr "/" "_")

	tar -czf ${3}${2}${clean_dir_name}_full_backup.tar.gz $1
}

# Check if any options are entered
if [ $# -eq "0" ]; then
	echo "Please enter a valid Option:"
	echo "-d [/path/to/disk] to save the backup to a disk"
	echo "-l to save the backup locally"
	exit
fi

# Current date
cur_date=$(date +%Y_%m_%d)

while getopts "d:l" opt; do
	case $opt in
	d) # Save the backup to a disk
		save_to_disk "/home" $cur_date $OPTARG
		exit
		;;
	l) # Save the backup locally

		# Check if a date for the last backup is stored
		if [ ! -f /tmp/full_backup_home ]; then
			echo -e "You started the first Backup"
			full_backup "/home" $cur_date
			exit
		fi

		last_full_backup=$(cat /tmp/full_backup_home)

		# Check if the last full back up was made this week
		# if yes do an incremental backup
		if [ $(date +%U -d $(echo $last_full_backup | tr "_" "-")) != $(date +%U -d $(echo $cur_date | tr "_" "-")) ]; then
			echo "The last full backup was last week"
			full_backup "/home" $cur_date
		else
			echo "The last full backup was this week"
			incremental_backup "/home" $cur_date
		fi
		;;
	\?) # No valid option was given
		echo "Please enter a valid Option:"
		echo "-d [/path/to/disk] to save the backup to a disk"
		echo "-l to save the backup locally"
		;;
	esac
done
