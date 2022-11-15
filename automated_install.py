import platform
import getmac
import os
import json
import subprocess
import psutil
import re


# path = "BackUp/"
path = "backup/"

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

    # if hwInfo["macAddress"] == "00:0c:29:92:0f:3c":
    #     hostname = "Sebi"
    # else:
    #     hostname = "NONE"
    hostname = 'drk_bs_client'

    # Get pkgs and services to install
    with open(f'{path}data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        # pkgs = data["pkgs"]
        services = data["services"]
        customCommands = data["commands"]
        f.close()

    pkgs = []

    config = {
        "archinstall-language": "German",
        "audio": "pipwire",
        "bootloader": "grub-install",
        "config_version": "2.5.1",
        "debug": False,
        "desktop-environment": "gnome",
        "gfx_driver": vga,
        "harddrives": [
            "/dev/sda"
        ],
        "hostname": hostname,
        "keyboard-layout": "de",
        "mirror-region": "Worldwide",
        "nic": {
            "dhcp": True,
            "dns": "null",
            "gateway": "null",
            "iface": "null",
            "ip": "null",
            "type": "nm"
        },
        "no_pkg_lookups": False,
        "offline": False,
        "packages": pkgs,
        "profile": {"path": ""},
        "silent": True,
        "services": services,
        "sys-encoding": "UTF-8",
        "sys-language": "de_DE.UTF-8",
        "version": "2.5.1"
    }

    return config


def create_creds(hwInfo):
    creds = {
        "!root-password": "root",
        # "!encryption-password": "root",
        "!users": [
            {
                "username": "mitarbeiter",
                "!password": "mitarbeiter",
                "sudo": False
            },
            {
                "username": "admin",
                "!password": "admin",
                "sudo": True
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
                    "size": "512MiB",
                    "start": "1MiB",
                    "type": "primary",
                    "wipe": True
                },
                {
                    "encrypted": False,
                    "filesystem": {
                        "format": "ext4",
                        "mount_options": []
                    },
                    "mountpoint":"/",
                    "size": "20GiB",
                    "start": "523MiB",
                    "type": "primary",
                    "wipe": True
                },
                {
                    "encrypted": False,
                    "filesystem": {
                        "format": "ext4",
                        "mount_options": []
                    },
                    "mountpoint": "/home",
                    "size": "100%",
                    "start": "20GiB",
                    "type": "primary",
                    "wipe": True
                }
            ],
            "wipe": True
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

    # json.dumps(diskLayouts,
    #                                             ensure_ascii=False,
    #                                             indent=4)

    subprocess.run(["archinstall",
                   "--config", json.dumps(config),
                    "--disk-layout", json.dumps(diskLayouts),
                    "--creds", json.dumps(creds), "--silent"
                    ], check=True, text=True)


main()
