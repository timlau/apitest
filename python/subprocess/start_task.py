import subprocess
import sys

print("starting")
pid = subprocess.Popen(["/usr/bin/yumex"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
print(f"started : {pid}")
sys.exit(0)