import platform
import getmac
import os
import json
import subprocess

# Computer network name
print(f"Computer network name: {platform.node()}")
# Machine type
print(f"Machine type: {platform.machine()}")
# Processor type
print(f"Processor type: {platform.processor()}")
# Platform type
print(f"Platform type: {platform.platform()}")
# Operating system
print(f"Operating system: {platform.system()}")
# Operating system release
print(f"Operating system release: {platform.release()}")
# Operating system version
print(f"Operating system version: {platform.version()}")
# MAC Adress
print(f"MAC Adress: {getmac.get_mac_address()}")

string = "STRING"

booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "BIOS"
print("The system booted with %s" % booted)
jsb = {
    "This": "CD",
    "is": "AB",
    1: {"a": "c"},
    "Test": "",
    "JSON": {2: [1, 2, 3, 4, 5]}
}

js = json.dumps(jsb,indent=4)

print(js)

json.dump(js, "config.json")


#subprocess.run(["echo", "myTest", string], check=True, text=True)
#subprocess.run(["archinstall", "--config" "config.json", "--dry-run"], check=True, text=True)
