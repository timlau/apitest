import subprocess
import sys

print("starting")
subprocess.Popen(["/usr/bin/yumex"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("started")
sys.exit(0)