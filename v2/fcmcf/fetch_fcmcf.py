import os
import urllib.request
import shutil
import tempfile


def _download(instance):
    tmpdir = tempfile.gettempdir()
    instanceName = instance + ".txt"
    filename = os.path.join(tmpdir, instanceName)
    if not os.path.exists(filename):
        url = f"https://raw.github.com/flowty/data/master/data/fcmcf/{instanceName}"
        headers = {"Accept": "application/txt"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)


def _getNextLine(file):
    line = next(file)
    while line[0] == "c":
        line = next(file)
    return line


def _read(instance):
    tmpdir = tempfile.gettempdir()
    print(os.getcwd())
    filename = os.path.join(tmpdir, instance + ".txt")
    E = []
    C = []
    U = []
    F = []
    O = []
    D = []
    B = []
    with open(filename, "r") as file:
        line = _getNextLine(file)
        n, m, k = [int(i) for i in line[2:].split()[1:]]
        for _ in range(k):
            line = _getNextLine(file)
            o, d, b = [int(i) for i in line.strip().split()[1:]]
            O.append(o)
            D.append(d)
            B.append(b)
        for _ in range(m):
            line = _getNextLine(file)
            s, t, c, u, f = [int(i) for i in line.strip().split()[1:]]
            E.append((s, t))
            C.append(c)
            U.append(u)
            F.append(f)
    return instance, n, m, k, E, C, U, F, O, D, B


def fetch(instance):
    _download(instance)
    return _read(instance)
