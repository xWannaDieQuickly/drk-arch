import platform
import time
import getmac
import os
import json
import subprocess
import psutil
import re


# path = "BackUp/"
path = ""

# Read the hardware of the system


def get_hw():
    hardInfo = {}
    # Computer network name
    hardInfo["computerNetworkName"] = platform.node()
    # Machine type
    hardInfo["machineType"] = platform.machine()
    # Processor type
    hardInfo["processorType"] = platform.processor()
    # Platform type
    hardInfo["platformType"] = platform.platform()
    # Operating system
    hardInfo["operatingSystem"] = platform.system()
    # Operating system release
    hardInfo["operatingSystemRelease"] = platform.release()
    # Operating system version
    hardInfo["operatingSystemVersion"] = platform.version()
    # MAC Adress
    hardInfo["macAddress"] = getmac.get_mac_address()
    # Disk Partitions
    hardInfo["diskPartitions"] = psutil.disk_partitions()
    # Firmware
    hardInfo["firmware"] = "UEFI" if os.path.exists(
        "/sys/firmware/efi") else "BIOS"
    # Disks
    hardInfo["disks"] = subprocess.run(["fdisk", "-l"], check=True,
                                       text=True, capture_output=True).stdout
    # VGA
    for e in subprocess.run(["lspci"], check=True,
                            text=True, capture_output=True).stdout.splitlines():
        if "VGA" in e:
            hardInfo["vga"] = e
    return hardInfo


# Create the config json
def create_config(hwInfo):

    # hostname = "refe"

    # Check the VGA
    if hwInfo["vga"] is None:
        vga = "All open-source (default)"
    elif "nvidia" in hwInfo["vga"].lower():
        vga = "Nvidia"
    elif "intel" in hwInfo["vga"].lower():
        vga = "Intel (open-source)"
    elif any(substring in hwInfo["vga"].lower() for substring in ["vmware", "virtualbox"]):
        vga = "VMware / VirtualBox (open-source)"
    elif "amd" in hwInfo["vga"].lower():
        vga = "AMD / ATI (open-source)"
    else:
        vga = "All open-source (default)"

    if hwInfo["macAddress"] == "00:0c:29:92:0f:3c":
        hostname = "Sebi"
    else:
        hostname = "NONE"

    # Get pkgs and services to install
    with open(f'{path}data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        pkgs = data["pkgs"]
        services = data["services"]
        customCommands = data["commands"]
        # print(pkgs, services)
        f.close()

    config = {
        "dry-run": True,
        "audio": "pipewire",
        "bootloader": "grub-install",
        "custom-commands": customCommands,
        "debug": False,
        "gfx_driver": vga,
        "hostname": hostname,
        "harddrives": [
            "/dev/sda"
        ],
        "kernels": [
            "linux"
        ],
        "keyboard-layout": "de",
        "keyboard-language": "de",
        "mirror-region": "Worldwide",
        "nic": {
            "NetworkManager": True
        },
        "ntp": True,
        "packages": pkgs,
        "services": ["gdm", "NetworkManager"],
        "swap": True,
        "sys-encoding": "utf-8",
        "sys-language": "de_DE@euro",
        "timezone": "Europe/Berlin"
    }

    return config


def create_creds(hwInfo):
    creds = {
        #"!root-password": "root",
        "!encryption-password": "root",
        "!users": [
            {
                "username": "sebi",
                "!password": "sebi",
                "sudo": True
            },
            {
                "username": "tester123",
                "!password": "tester123",
                "sudo": True
            },
            {
                "username": "admin",
                "!password": "admin",
                "sudo": False
            }
        ]
    }
    return creds


def create_disk_layouts(hwInfo):

    disks = {}
    diskSize = []
    for d in hwInfo["disks"].split("\n\n\n"):
        disk = d.split("\n")[0]
        size = int(re.findall("(?<=,\s)(.*)(?=\sbytes)", disk)[0])
        name = re.findall("(?<=Disk\s)(.*)(?=:)", disk)[0]
        diskSize.append(size)
        disks[name] = size

    # DEBUG
    # print disc sizes
    # print(max(diskSize))
    # for k, v in disks.items():
    #    if v == max(diskSize):
    #         print(k, "...", v)

    diskLayouts = {
        "/dev/sda": {
            "partitions": [
                {
                    "boot": True,
                    "encrypted": False,
                    "filesystem": {
                        "format": "fat32"
                    },
                    "mountpoint": "/boot",
                    "size": "203MiB",
                    "start": "3MiB",
                    "type": "primary",
                    "wipe": True
                },
                {
                    "boot": False,
                    "encrypted": True,
                    "filesystem": {
                        "format": "ext4",
                        "mount_options": []
                    },
                    "mountpoint": "/",
                    "size": "100%",
                    "start": "205MiB",
                    "type": "primary",
                    "wipe": True
                }
            ]
        }
    }

    return diskLayouts


def main():

    hwInfo = get_hw()
    config = create_config(hwInfo=hwInfo)
    creds = create_creds(hwInfo=hwInfo)
    diskLayouts = create_disk_layouts(hwInfo=hwInfo)

    with open(f'{path}config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
        f.close()

    with open(f'{path}creds.json', 'w', encoding='utf-8') as f:
        json.dump(creds, f, ensure_ascii=False, indent=4)
        f.close()

    with open(f'{path}disk-layouts.json', 'w', encoding='utf-8') as f:
        json.dump(diskLayouts, f, ensure_ascii=False, indent=4)
        f.close()

    conf = f'{path}config.json'
    cred = f'{path}creds.json'
    disk_lay = f'{path}disk-layouts.json'

   # subprocess.run(["archinstall",
   #                 "--config", json.dumps(config,
   #                                        ensure_ascii=False,
   #                                        indent=4),
   #                 "--disk-layout", json.dumps(diskLayouts,
   #                                             ensure_ascii=False,
   #                                             indent=4),
   #                 # "--creds", json.dumps(creds,
   #                 #                    ensure_ascii=False,
   #                 #                   indent=4),
   #                 ], check=True, text=True)


main()