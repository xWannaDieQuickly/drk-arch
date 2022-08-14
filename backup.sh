#!/bin/bash

full_backup() {
	echo "Parameter " $1
	echo "Full-Backup"
}

incremental_backup() {
	echo "Incremental-Backup"

}

main() {
	# Current date
	cur_date=$(date +%Y-%m-%d)
	echo $cur_date
	continue="y"

	# Display menu
	# 1: Full-Backup of "/home" directory
	# 2: Incremental-Backup of "/home" directory
	# 3: Full-Backup of a chosen directory
	# 4: Exit the Program
	while [ $continue = "y" ]; do
		echo -e "Please choose an option 1 - 4: \n1: Full-Backup /home \n2: Incremetal-Backup /home \n3: Full-Backup any directory \n4: Exit"
		read -p "Input: " selection
		echo -e "\n"
		# TODO:
		case $selection in
		1)
			echo -e "You have chosen Full-Backup /home!\n"
			full_backup "ABC_TEST123"
			;;
		2)
			echo -e "You have chosen an Incremental-Backup /home!\n"
			;;
		3)
			echo -e "You have chosen a Full-Backup any directory!\n"
			;;
		4)
			echo -e "Would you like to exit the program! (Y/N)"
			read -p "Input: " exit_answer
			echo -e "\n"

			while [ ${exit_answer^} != "N" ] && [ ${exit_answer^} != "Y" ]; do
				echo "Please enter a valid response!"
				echo -e "Would you like to exit the program! (Y/N)"
				read -p "Input: " exit_answer
				echo -e "\n"
			done
			if [ ${exit_answer^} == "Y" ]; then
				echo -e "Program finished!\n"
				exit 0
			else
				continue
			fi
			;;
		*)
			echo -e "Please enter a valid Input!\n"
			;;
		esac

	done
}

main "$@"
