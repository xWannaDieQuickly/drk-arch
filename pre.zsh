#!/bin/zsh
pacman -S git python-pip --noconfirm
pip uninstall archinstall
git clone https://github.com/archlinux/archinstall
pip install setuptools
cd archinstall
pip install setuptools --no-input
python setup.py install
pip install getmac psutil --no-input
chmod +x BackUp/hw-info.py
python BackUp/hw-info.py
#archinstall --config BackUp/config.json --creds BackUp/creds.json --disk_layouts BackUp/disk-layouts.json
