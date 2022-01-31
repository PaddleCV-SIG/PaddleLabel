import os
import os.path as osp
import shutil


# TODO: change to raise error
def create_dir(path):
    if path is None:
        return False, "Path to create is None"
    if not osp.isabs(path):
        return False, f"Only supports absolute path, got {path}"
    if not osp.isdir(path):
        try:
            os.makedirs(path)
            return True, f"Created directory {path}"
        except Exception as e:
            return False, f"Create {path} failed. Got exception: {e}"
    else:
        return True, f"{path} exists"


def listdir(path, filters={"exclude_prefix": ["."]}):
    files = []
    for root, fdrs, fs in os.walk(path):
        for f in fs:
            files.append(osp.normpath(osp.join(root, f)))
    # TODO: support regx
    include_prefix = filters.get("include_prefix", None)
    include_postfix = filters.get("include_postfix", None)

    def include(path):
        f = osp.basename(path)
        for pref in include_prefix:
            if f[: len(pref)] == pref:
                return True
        for postf in include_postfix:
            if f[-len(postf) :] == postf:
                return True
        return False

    if include_prefix is not None or include_postfix is not None:
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
