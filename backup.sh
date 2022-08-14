#!/bin/bash
# Program: backup.sh
# Call: ./backup.sh
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
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory).\n\n"
		return
	fi

	# Create Full-Backup
	clean_dir_name=$(echo $1 | tr "/" "_")
	tar -czf /tmp/${2}${clean_dir_name}_full_backup.tar.gz $1

	# Safe the date
	echo $2 >/tmp/full_backup$clean_dir_name

	# Send archive to Server
	# scp /temp/full_backup_$2.tar.gz student1@192.168.10.1: ${2}${clean_dir_name}_full_backup.tar.gz

	# Log BackUp events
	echo -e "Successfully created a new Full BackUp of $1\n" >>/tmp/full_backup${clean_dir_name}.log

	# Delete BackUp after it was send to the server
	rm /tmp/${2}${clean_dir_name}_full_backup.tar.gz

}

# Incremental BackUp of given directory
# Args:
# 1: Directory
# 2: Current date
incremental_backup() {

	# Check if directory exists
	if [ ! -d "$1" ]; then
		echo -e "$1 does not exist. Please enter a valid directory (/path/to/directory).\n\n"
		return
	fi

	clean_dir_name=$(echo $1 | tr "/" "_")

	last_full_backup=$(cat /tmp/full_backup$clean_dir_name)

	echo $last_full_backup

	# Create new incremental BackUp
	tar -cz --after-date=$last_full_backup -f /tmp/${2}${clean_dir_name}_inc_backup.tar.gz $1

	# Send archive to Server
	# scp /tmp/${2}${clean_dir_name}_inc_backup.tar.gz student1@192.168.10.1: ${2}${clean_dir_name}_inc_backup.tar.gz

	# Log BackUp events
	echo -e "Successfully created a new Full BackUp of $1\n" >>/tmp/inc_backup${clean_dir_name}.log

	# Delete BackUp after it was send to the server
	rm /tmp/${2}${clean_dir_name}_inc_backup.tar.gz

}

main() {
	# Current date
	# Used to name the BackUp file
	cur_date=$(date +%Y_%m_%d)

	continue="y"

	# Display menu
	# 1: Full-Backup of "/home" directory
	# 2: Incremental-Backup of "/home" directory
	# 3: Full-Backup of a chosen directory
	# 4: Exit the Program
	# 5: Debug
	# *: Default
	while [ $continue = "y" ]; do
		echo -e "Backup-Menu\nPlease choose an option 1 - 4:\n"
		echo -e "----------------------------------------------------------------------------------------------------\n"
		echo -e "1: Full-Backup /home \n2: Incremetal-Backup /home \n3: Full-Backup any directory \n4: Exit \n5: DEBUG"
		read selection

		case $selection in
		1)
			full_backup "/home/"$(whoami) $cur_date
			;;
		2)
			incremental_backup "/home/"$(whoami) $cur_date
			;;
		3)
			read directory
			full_backup $directory $cur_date
			;;
		4)
			echo -e "Would you like to exit the program! (Y/N)"
			read exit_answer

			while [ ${exit_answer^} != "N" ] && [ ${exit_answer^} != "Y" ]; do
				echo "Please enter a valid response! \nWould you like to exit the program! (Y/N)"
				read exit_answer
			done
			if [ ${exit_answer^} == "Y" ]; then
				echo -e "Program finished!\n"
				exit 0
			else
				continue
			fi
			;;
		5)
			echo "2022-08-16" | tr "-" "_"
			read -rep "Please Enter a Message: "$'\n' message
			;;
		*)
			echo -e "Please enter a valid Input!\n"
			;;
		esac

	done
}

main
