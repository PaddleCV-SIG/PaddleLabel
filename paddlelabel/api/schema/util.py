# -*- coding: utf-8 -*-
import hashlib


def str2sault(seed):
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:20]
