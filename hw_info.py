import platform
import getmac
import archinstall

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


print(archinstall.has_amd_cpu)