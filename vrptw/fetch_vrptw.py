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
        _, q = (int(val) for val in line.split())

        line = next(file)
        line = next(file)
        line = next(file)
        line = next(file)

        X: List[int] = []
        Y: List[int] = []
        D: List[int] = []
        A: List[int] = []
        B: List[int] = []
        S: List[int] = []
        lines = islice(file, n + 1)
        for line in lines:
            _, xx, yy, dd, aa, bb, ss = (int(val) for val in line.split())
            X.append(xx)
            Y.append(yy)
            D.append(dd)
            A.append(aa)
            B.append(bb)
            S.append(ss)

        # Clone depot
        X.append(X[0])
        Y.append(Y[0])
        D.append(D[0])
        A.append(A[0])
        B.append(B[0])
        S.append(S[0])

        E: List[Tuple[int, int]] = []
        C: List[float] = []
        T: List[float] = []
        for i in range(n + 2):
            for j in range(n + 2):
                if j <= i:
                    continue
                value = (
                    int(
                        math.sqrt(math.pow(X[i] - X[j], 2) + math.pow(Y[i] - Y[j], 2))
                        * 10
                    )
                    / 10
                )
                if i != n + 1 and j != 0 and not (i == 0 and j == n + 1):
                    C.append(value)
                    T.append(value + S[i])
                    E.append((i, j))
                if j != n + 1 and i != 0:
                    C.append(value)
                    T.append(value + S[j])
                    E.append((j, i))

    return name, n + 2, E, C, D, q, T, A, B, X, Y
