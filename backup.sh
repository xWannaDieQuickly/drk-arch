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

##########################################################################
#	VARIABLES															##
##########################################################################
cur_date=$(date +%Y_%m_%d) # Current date							##
user=$(whoami)             # Current user							##
##########################################################################

# Info Page
help_page() {
	echo -e "Usage: backup.sh [-l] [-d <path/to/disk>]\n"
	echo -e "'backup.sh' archives the files of your '/home'-Directory,\nyou can choose to save the files locally or on an external drive.\n"
	echo "-d </path/to/disk> 	save the backup to a disk"
	echo "-l 			save the backup locally"
}

# Full BackUp of given directory
# Args:
# 1: Directory
# 2: Current date
full_backup() {

	# Check if directory exists
	if [ ! -d "$1" ]; then
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory)."
		help_page
		return
	fi

	clean_dir_name=$(echo "$1" | tr "/" "_")

	# Create archive of the given directory
	# Exclude the directory the backups are stored in
	tar --exclude="$1/Backup" -czf "$1/Backup/${2}${clean_dir_name}_backup.tar.gz" "$1"

	# Safe the date
	echo "$2" >"$1/Backup/last_backup$clean_dir_name"
}

# Incremental BackUp of given directory
# Args:
# 1: Directory
# 2: Current date
incremental_backup() {

	# Check if directory exists
	if [ ! -d "$1" ]; then
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory)."
		help_page
		return
	fi

	clean_dir_name=$(echo "$1" | tr "/" "_")

	# Check if a full Back-Up of the given directory has already been created
	# If no, create full Back-Up instead of incremental Back-Up
	if [ ! -f "$1/Backup${2}${clean_dir_name}_backup.tar.gz" ]; then
		full_backup "$1" "$2"
		return
	fi

	last_full_backup=$(cat $1/Backup/last_backup$clean_dir_name)

	# Create archive of the given directory
	# Exclude the directory the backups are stored in
	tar --exclude="$1/Backup" -cz --newer-mtime=$(echo $last_full_backup | tr "_" "-") -f "$1/Backup/${2}${clean_dir_name}_backup.tar.gz" "$1"
}

# Save the Back-Up as Archive to a disk
# Args:
# 1: Directory
# 2: Current date
# 3: Disk / Harddrive
save_to_disk() {

	# Check if disk exists
	if [ ! -d "$3" ]; then
		echo -e "$3 does not exist. Please enter a valid disc (/path/to/disk)."
		help_page
		return
	fi

	clean_dir_name=$(echo $1 | tr "/" "_")

	# Create archive of the given directory
	# Exclude the directory the backups are stored in
	tar --exclude="$1/Backup" -czf "$3/${2}${clean_dir_name}_backup.tar.gz" "$1"
}

# Check if any options are entered
# Output help for the user
if [ $# == "0" ]; then
	echo "Please enter a valid Option:"
	help_page
	exit
fi

# Main loop
# Process the options
while getopts "d:lh" opt; do
	case $opt in
	d) # Save the backup to a disk
		save_to_disk "/home/$user" $cur_date $OPTARG
		exit
		;;
	l) # Save the backup locally

		# Check if a date for the last backup is stored
		if [ ! -f "/home/$user/Backup/last_backup_home_$user" ]; then
			full_backup "/home/$user" $cur_date
			exit
		fi

		last_full_backup=$(cat "/home/"$user/Backup/last_backup_home_$user)

		# Check if the last full back up was made this week
		# if yes do an incremental backup
		if [ $(date +%U -d $(echo $last_full_backup | tr "_" "-")) != $(date +%U -d $(echo $cur_date | tr "_" "-")) ]; then
			echo "The last full backup was last week"
			full_backup "/home/$user" $cur_date
		else
			echo "The last full backup was this week"
			incremental_backup "/home/$user" $cur_date
		fi
		;;
	h)
		help_page
		;;

	\?) # No valid option was given
		echo "Please enter a valid Option:"
		help_page
		;;
	esac
done
