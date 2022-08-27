#!/bin/zsh
loadkeys de-latin1
pacman -Sy python-pip archinstall --noconfirm
pip install getmac psutil --no-input
#archinstall --config BackUp/config.json --creds BackUp/creds.json --disk_layouts BackUp/disk-layouts.json
