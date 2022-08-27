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
    hardInfo["macAdress"] = getmac.get_mac_address()
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
    print(type(hardInfo["vga"]))
    print(hardInfo["vga"])
    return hardInfo


def create_json(hwInfo):

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

    print(vga)

    {
        "audio": "pipewire",
        "bootloader": "grub-install",
        "custom-commands": [
            "echo finished"
        ],
        "debug": False,
        "gfx_driver": "Nvidia",
        "hostname": "myarch",
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


def main():
    hwInfo = get_hw()
    # print(json.dumps(hwInfo, indent=4))

    create_json(hwInfo=hwInfo)

    # with open('config.json', 'w', encoding='utf-8') as f:
    #     json.dump(jsb, f, ensure_ascii=False, indent=4)

    # subprocess.run(["echo", "myTest", string], check=True, text=True)
    # subprocess.run(["archinstall", "--config" "config.json", "--dry-run"], check=True, text=True)


main()
