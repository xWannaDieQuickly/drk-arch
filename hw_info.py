import platform
import getmac
import os
import json
import subprocess
import psutil

# Computer network name
computerNetworkName = platform.node()
# Machine type
machineType = platform.machine()
# Processor type
processorType = platform.processor()
# Platform type
platformType = platform.platform()
# Operating system
operatingSystem = platform.system()
# Operating system release
operatingSystemRelease = platform.release()
# Operating system version
operatingSystemVersion = platform.version()
# MAC Adress
macAdress = getmac.get_mac_address()
# Disk Partitions
diskPartitions = psutil.disk_partitions()

print(diskPartitions)


booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "BIOS"
print("The system booted with %s" % booted)
jsb = {
    "This": "CD",
    "is": "AB",
    1: {"a": "c"},
    "Test": "",
    "JSON": {2: [1, 2, 3, 4, 5]}
}

js = json.dumps(jsb, indent=4)

print(js)

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(jsb, f, ensure_ascii=False, indent=4)


#subprocess.run(["echo", "myTest", string], check=True, text=True)
#subprocess.run(["archinstall", "--config" "config.json", "--dry-run"], check=True, text=True)
