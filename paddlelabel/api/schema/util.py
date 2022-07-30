import hashlib


def path2sault(path):
    return hashlib.md5(path.encode("utf-8")).hexdigest()[:10]
