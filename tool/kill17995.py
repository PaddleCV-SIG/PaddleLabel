import os
import sys


if len(sys.argv) == 1:
    port = 17995
else:
    port = sys.argv[1]

res = os.popen(f"lsof -i :{port}")
res = res.read().split("\n")
if len(res) == 1:
    print(f"no process is on {port}")
    exit(0)
pid = res[1].strip().split(" ")[1]
print(f"killing process on {port} with pid {pid}")
os.popen(f"kill -9 {pid}")
