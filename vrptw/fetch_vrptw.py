import math
from itertools import islice
import os
import shutil
import tempfile
from typing import List, Tuple
import urllib.request


def fetch(collection: str, instance: str, n: int = 100):
    filename = os.path.join(tempfile.gettempdir(), f"{collection}_{instance}.txt")

    if not os.path.exists(filename):
        url = (
            "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/"
            f"{collection}/{instance}.txt"
        )
        headers = {"Accept": "application/xml"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

    with open(filename, "r") as file:
        name = f"{next(file).strip()}_{n:03d}"
        line = next(file)
        line = next(file)
        line = next(file)
        line = next(file)
        _, Q = (int(val) for val in line.split())

        line = next(file)
        line = next(file)
        line = next(file)
        line = next(file)

        x: List[int] = []
        y: List[int] = []
        d: List[int] = []
        a: List[int] = []
        b: List[int] = []
        s: List[int] = []
        lines = islice(file, n + 1)
        for line in lines:
            _, xx, yy, dd, aa, bb, ss = (int(val) for val in line.split())
            x.append(xx)
            y.append(yy)
            d.append(dd)
            a.append(aa)
            b.append(bb)
            s.append(ss)

        # Clone depot
        x.append(x[0])
        y.append(y[0])
        d.append(d[0])
        a.append(a[0])
        b.append(b[0])
        s.append(s[0])

        E: List[Tuple[int, int]] = []
        c: List[float] = []
        t: List[float] = []
        for i in range(n + 2):
            for j in range(n + 2):
                if j <= i:
                    continue
                value = (
                    int(
                        math.sqrt(math.pow(x[i] - x[j], 2) + math.pow(y[i] - y[j], 2))
                        * 10
                    )
                    / 10
                )
                if i != n + 1 and j != 0 and not (i == 0 and j == n + 1):
                    c.append(value)
                    t.append(value + s[i])
                    E.append((i, j))
                if j != n + 1 and i != 0:
                    c.append(value)
                    t.append(value + s[j])
                    E.append((j, i))

    return name, n + 2, E, c, d, Q, t, a, b, x, y
