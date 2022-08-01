version = open("paddlelabel/version", "r").read().strip().split(".")
version = [int(v) for v in version]
version[2] += 1
version = [str(v) for v in version]
version = ".".join(version)
print(version, file=open("paddlelabel/version", "w"))
