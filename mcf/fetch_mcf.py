import os
import urllib.request
import tarfile
import shutil
import tempfile


def _download(instance):
    instance_lookup = {
        "planar": "planar.tgz",
        "grid": "grid.tgz",
        "Canad-C": "C.tgz",
        "Canad-C+": "CPlus.tgz",
        "Canad-R": "R.tgz",
    }

    tmpdir = tempfile.gettempdir()
    filename = os.path.join(tmpdir, instance_lookup[instance])
    if os.path.exists(filename):
        return
    url = f"http://groups.di.unipi.it/optimize/Data/MMCF/{instance_lookup[instance]}"
    headers = {"Accept": "application/zip"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(filename, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
    with tarfile.open(filename, "r") as tf:
        tf.extractall(tmpdir)


def _read(instance, num):
    tmpdir = tempfile.gettempdir()
    name = instance + str(num)
    filename = os.path.join(tmpdir, name)
    numN = 0
    numE = 0
    numK = 0
    E = []
    c = []
    u = []
    s = []
    t = []
    d = []
    with open(filename, "r") as f:
        numN = int(f.readline())
        numE = int(f.readline())
        numK = int(f.readline())
        for _ in range(numE):
            source, target, cost, capacity = [
                int(w) for w in f.readline().split(" ") if w.strip()
            ]
            E.append((source - 1, target - 1))
            c.append(cost)
            u.append(capacity)
        for _ in range(numK):
            origin, dest, demand = [
                int(w) for w in f.readline().split(" ") if w.strip()
            ]
            s.append(origin - 1)
            t.append(dest - 1)
            d.append(demand)
    return name, numN, numE, numK, E, c, u, s, t, d


def fetch(instance, num):
    _download(instance)
    return _read(instance, num)
