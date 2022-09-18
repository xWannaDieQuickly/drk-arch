#!/bin/zsh
pacman -S git python-pip --noconfirm
pip uninstall archinstall --no-input
git clone https://github.com/archlinux/archinstall
pip install setuptools getmac psutil --no-input
cd archinstall
python setup.py install
cd
python automated_install.py
archinstall --config BackUp/config.json --creds BackUp/creds.json --disk_layouts BackUp/disk-layouts.json
