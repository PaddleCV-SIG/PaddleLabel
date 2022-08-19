import os
import sys


if len(sys.argv) == 1:
    port = 17995
else:
    port = sys.argv[1]

res = os.popen(f"lsof -i :{port}")
res = res.read().split("\n")

print("======")
print(res)
print("======")

if len(res) == 1:
    print(f"no process on {port}")
    exit(0)


res = res[1].strip().split(" ")
pid = [r for r in res if r != ""][1]
print(f"killing process on {port} with pid {pid}")
os.popen(f"kill -9 {pid}")
