#!/bin/zsh
yes | pacman -S git python-pip
yes | pip uninstall archinstall
git clone https://github.com/archlinux/archinstall
yes | pip install setuptools getmac psutil
cd archinstall
python setup.py install
cd ../BackUp
python automated_install.py
archinstall --creds creds.json --disk_layouts disk-layouts.json 2> errors.txt
