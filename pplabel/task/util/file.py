import os
import os.path as osp
import shutil


def create_dir(path):
    if path is None:
        raise RuntimeError("Path to create is None")
    if not osp.isabs(path):
        raise RuntimeError(f"Only supports absolute path, got {path}")
    os.makedirs(path, exist_ok=True)


def listdir(path, filters={"exclude_prefix": ["."]}):
    files = []
    for root, fdrs, fs in os.walk(path):
        for f in fs:
            files.append(osp.normpath(osp.join(root, f)))
    # TODO: support regx
    include_prefix = filters.get("include_prefix", [])
    include_postfix = filters.get("include_postfix", [])

    def include(path):
        f = osp.basename(path)
        for pref in include_prefix:
            if f[: len(pref)] == pref:
                return True
        for postf in include_postfix:
            if f[-len(postf) :] == postf:
                return True
        return False

    if include_prefix is not [] or include_postfix is not []:
        files = list(filter(include, files))

    exclude_prefix = filters.get("exclude_prefix", [])
    exclude_postfix = filters.get("exclude_postfix", [])

    def exclude(path):
        f = osp.basename(path)
        for pref in exclude_prefix:
            if f[: len(pref)] == pref:
                return False
        for postf in exclude_postfix:
            if f[-len(postf) :] == postf:
                return False
        return True

    files = list(filter(exclude, files))
    files.sort()
    files = [osp.normpath(p) for p in files]
    return files


def copy(src, dst):
    src = osp.normpath(src)
    dst = osp.normpath(dst)
    shutil.copy(src, dst)


def copytree(src, dst):
    """Copy all files in src directory to dst directory.

    Parameters
    ----------
    src : str
        Description of parameter `src`.
    dst : str
        Description of parameter `dst`.
    """
    src = osp.normpath(src)
    dst = osp.normpath(dst)
    shutil.copytree(src, dst)
