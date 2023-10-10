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
    instanceName = _getInstancename(instance, name)
    with tarfile.open(filename, "r") as tf:
        for member in tf.getmembers():
            if member.name == instanceName:
                if not os.path.exists(os.path.join(tmpdir, instanceName)):
                    tf.extract(member, tmpdir)
                return
        raise TypeError(f"{name} not in {instance} data set")


def _readDow(instance, name):
    tmpdir = tempfile.gettempdir()
    instanceName = _getInstancename(instance, name)
    filename = os.path.join(tmpdir, instanceName)
    numN = 0
    numE = 0
    numK = 0
    E = []
    C = []
    U = []
    F = []
    O = []
    D = []
    B = []
    with open(filename, "r") as f:
        f.readline()
        numN, numE, numK = [int(w) for w in f.readline().split(" ") if w.strip()]
        for _ in range(numE):
            source, target, cost, capacity, fixed, any1, any2 = [
                int(w) for w in f.readline().split(" ") if w.strip()
            ]
            E.append((source - 1, target - 1))
            C.append(cost)
            U.append(capacity)
            F.append(fixed)
        for _ in range(numK):
            origin, dest, demand = [
                int(w) for w in f.readline().split(" ") if w.strip()
            ]
            O.append(origin - 1)
            D.append(dest - 1)
            B.append(demand)
    return instanceName, numN, numE, numK, E, C, U, F, O, D, B


def fetch(instance, name):
    _download(instance, name)
    instancename = _getInstancename(instance, name)
    if instancename.endswith(".dow"):
        return _readDow(instance, name)
    raise TypeError(f"Instance format for {instancename} not supported")
