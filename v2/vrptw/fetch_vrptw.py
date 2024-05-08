import gzip
import os
import io
import urllib.request
import shutil
import tempfile


def _download(instance):
    tmpdir = tempfile.gettempdir()
    instanceName = instance + ".txt.gz"
    filename = os.path.join(tmpdir, instanceName)
    if not os.path.exists(filename):
        url = f"https://github.com/flowty/data/releases/download/VRPTW_v1.0.0/{instanceName}"
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
    filename = os.path.join(tmpdir, instance + ".txt.gz")
    E = []
    C = []
    D = []
    T = []
    A = []
    B = []
    X = []
    Y = []
    with io.TextIOWrapper(gzip.open(filename, "rb"), encoding="utf-8") as file:
        line = _getNextLine(file)
        n, m, q = [int(i) for i in line[2:].split()[1:]]
        for _ in range(n):
            line = _getNextLine(file)
            _, a, b, d, x, y = [int(i) for i in line.strip().split()[1:]]
            A.append(a)
            B.append(b)
            D.append(d)
            X.append(x)
            Y.append(y)
        for _ in range(m):
            line = _getNextLine(file)
            i, j, c, t = [int(i) for i in line.strip().split()[1:]]
            E.append((i, j))
            C.append(c)
            T.append(t)
    return instance, n, m, E, C, D, q, T, A, B, X, Y


def fetch(instance):
    _download(instance)
    return _read(instance)
