import os
import urllib.request
import tarfile
import shutil
import tempfile


def _download(instance):
    instance_lookup = {
        "Canad-C": "C.tgz",
        "Canad-C+": "CPlus.tgz",
        "Canad-R": "R.tgz",
        "Canad-N": "CanadN.tgz",
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


def _read(instance, name):
    tmpdir = tempfile.gettempdir()
    filename = os.path.join(tmpdir, name + ".dow")
    numN = 0
    numE = 0
    numK = 0
    E = []
    c = []
    u = []
    f = []
    s = []
    t = []
    d = []
    with open(filename, "r") as fi:
        fi.readline()
        numN, numE, numK = [int(w) for w in fi.readline().split(" ") if w.strip()]
        for _ in range(numE):
            source, target, cost, capacity, fixed, any1, any2 = [
                int(w) for w in fi.readline().split(" ") if w.strip()
            ]
            E.append((source - 1, target - 1))
            c.append(cost)
            u.append(capacity)
            f.append(fixed)
        for _ in range(numK):
            origin, dest, demand = [
                int(w) for w in fi.readline().split(" ") if w.strip()
            ]
            s.append(origin - 1)
            t.append(dest - 1)
            d.append(demand)
    return filename, numN, numE, numK, E, c, u, f, s, t, d


def fetch(instance, num):
    _download(instance)
    return _read(instance, num)
