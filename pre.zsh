#!/bin/zsh
pacman -Sy
yes | pacman -S python-pip
yes | pip uninstall archinstall
git clone https://github.com/archlinux/archinstall
yes | pip install setuptools getmac psutil
cd archinstall
python setup.py install
cd ../backup
python automated_install.py
python -m archinstall --config config.json --creds creds.json --disk_layouts disk-layouts.json
