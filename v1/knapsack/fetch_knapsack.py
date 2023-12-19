import os
import tarfile
import urllib.request
import shutil
import tempfile


def _download(collection: str, instance: str):
    lookup = {
        "small": "smallcoeff_pisinger.tgz",
        "large": "largecoeff_pisinger.tgz",
        "hard": "hardinstances_pisinger.tgz",
    }
    tmpdir = tempfile.gettempdir()
    filename = os.path.join(tmpdir, lookup[collection])
    if not os.path.exists(filename):
        # get data
        url = f"http://www.diku.dk/~pisinger/{lookup[collection]}"
        headers = {"Accept": "application/zip"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

    instanceName = "_".join(instance.split("_")[:-1]) + ".csv"
    with tarfile.open(filename, "r") as tf:
        for member in tf.getmembers():
            if member.name == instanceName:
                if not os.path.exists(os.path.join(tmpdir, instanceName)):
                    tf.extract(member, tmpdir)
                return
        raise TypeError(f"{instance} not in {collection} data set")


def _read(collection: str, instance: str):
    tmpdir = tempfile.gettempdir()
    instanceName = "_".join(instance.split("_")[:-1]) + ".csv"
    filename = os.path.join(tmpdir, instanceName)
    with open(filename, "r") as f:
        # 100 instances per file
        for i in range(100):
            name = f.readline().strip("\n")
            n = int(f.readline().strip("\n").split()[1])

            if name != instance:
                for _ in range(n + 5):
                    next(f)
                continue

            c = int(f.readline().strip("\n").split()[1])
            z = int(f.readline().strip("\n").split()[1])
            f.readline()  # time
            # edges
            p = []
            w = []
            x = []
            for i in range(n):
                item, profit, weight, xValue = [
                    int(x) for x in f.readline().strip("\n").split(",")
                ]
                p.append(profit)
                w.append(weight)
                x.append(xValue)
            f.readline()
            f.readline()
            return name, n, c, p, w, z, x


def fetch(collection: str, instance: str):
    _download(collection, instance)
    return _read(collection, instance)
