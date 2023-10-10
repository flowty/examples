import os
import urllib.request
import tarfile
import shutil
import tempfile

_instance_lookup = {
    "Canad-C": "C.tgz",
    "Canad-C+": "CPlus.tgz",
    "Canad-R": "R.tgz",
    "Canad-N": "CanadN.tgz",
}


def _getInstancename(instance, name):
    end = ".dow"
    if instance.endswith("N"):
        end = ".dat"
    return name + end


def _download(instance, name):
    tmpdir = tempfile.gettempdir()
    instancename = _getInstancename(instance, name)
    filename = os.path.join(tmpdir, _instance_lookup[instance])
    if not os.path.exists(filename):
        url = (
            f"http://groups.di.unipi.it/optimize/Data/MMCF/{_instance_lookup[instance]}"
        )
        headers = {"Accept": "application/zip"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
    with tarfile.open(filename, "r") as tf:
        for member in tf.getmembers():
            if member.name == instancename:
                if not os.path.exists(os.path.join(tmpdir, instancename)):
                    tf.extract(member, tmpdir)
                return
        raise TypeError(f"{name} not in {instance} data set")


def _readDow(instance, name):
    tmpdir = tempfile.gettempdir()
    instancename = _getInstancename(instance, name)
    filename = os.path.join(tmpdir, instancename)
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
    return instancename, numN, numE, numK, E, c, u, f, s, t, d


def fetch(instance, name):
    _download(instance, name)
    instancename = _getInstancename(instance, name)
    if instancename.endswith(".dow"):
        return _readDow(instance, name)
    raise TypeError(f"Instance format for {instancename} not supported")
