import os
import tarfile
import urllib.request
import shutil
import tempfile


def _parse_file(tf: tarfile.TarFile, instance: str, member: tarfile.TarInfo):
    with tf.extractfile(member) as fh:
        # 100 instances per file
        for i in range(100):
            name = fh.readline().decode("utf-8").strip("\n")
            n = int(fh.readline().decode("utf-8").strip("\n").split()[1])
            c = int(fh.readline().decode("utf-8").strip("\n").split()[1])
            z = int(fh.readline().decode("utf-8").strip("\n").split()[1])
            fh.readline()  # time
            # edges
            p = []
            w = []
            x = []
            for i in range(n):
                item, profit, weight, xValue = [
                    int(x) for x in fh.readline().decode("utf-8").strip("\n").split(",")
                ]
                p.append(profit)
                w.append(weight)
                x.append(xValue)
            fh.readline()
            fh.readline()
            if name == instance:
                return name, n, c, p, w, z, x


def fetch(collection: str, instance: str):
    lookup = {
        "small": "smallcoeff_pisinger.tgz",
        "large": "largecoeff_pisinger.tgz",
        "hard": "hardinstances_pisinger.tgz",
    }
    filename = os.path.join(tempfile.gettempdir(), lookup[collection])
    if not os.path.exists(filename):
        # get data
        url = f"http://www.diku.dk/~pisinger/{lookup[collection]}"
        headers = {"Accept": "application/zip"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

    tarFile = tarfile.open(filename, "r")
    for instancefile in tarFile.getnames():
        rawInstanceFileName = "_".join(instance.split("_")[:-1])
        if instancefile == f"{rawInstanceFileName}.csv":
            member = tarFile.getmember(instancefile)
            return _parse_file(tarFile, instance, member)
