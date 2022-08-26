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
    fdisk = subprocess.run(["fdisk", "-l"], check=True, text=True, capture_output=True)
    print(fdisk.stdout)
    print("-----------------------------------")
    print(type(fdisk.stdout))
    print("-----------------------------------")

    # hardInfo["fdisk"] = fdisk

    

    return hardInfo


def main():

    hwInfo = get_hw()
    print(json.dumps(hwInfo, indent=4))


    booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "BIOS"
    print("The system booted with %s" % booted)

    # with open('config.json', 'w', encoding='utf-8') as f:
    #     json.dump(jsb, f, ensure_ascii=False, indent=4)

    #subprocess.run(["echo", "myTest", string], check=True, text=True)
    #subprocess.run(["archinstall", "--config" "config.json", "--dry-run"], check=True, text=True)

main()  