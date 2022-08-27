import platform
import getmac
import os
import json
import subprocess
import psutil


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
        print("Sebi")

    config = {
        "audio": "pipewire",
        "bootloader": "grub-install",
        "custom-commands": [
            "echo finished"
        ],
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
            "NetworkManager": True,
            "nic": "Use NetworkManager (necessary to configure internet graphically in GNOME and KDE)"
        },
        "ntp": True,
        "packages": [
            "efibootmgr",
            "os-prober",
            "mtools",
            "git",
            "wget",
            "zsh",
            "gnome",
            "xorg-server",
            "xorg-apps",
            "gnome",
            "gnome-extra",
            "networkmanager"
        ],
        "services": [],
        "swap": True,
        "sys-encoding": "utf-8",
        "sys-language": "de_DE@euro",
        "timezone": "Europe/Berlin"
    }

    return config


def create_creds(hwInfo):
    creds = {
        "!root-password": "root",
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


def main():
    hwInfo = get_hw()
    config = create_config(hwInfo=hwInfo)
    creds = create_creds(hwInfo=hwInfo)

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
        f.close()

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(creds, f, ensure_ascii=False, indent=4)
        f.close()

    subprocess.run(["archinstall", "--config", "config.json", "--creds", "creds.config",
                   "--dry-run"], check=True, text=True)


main()
