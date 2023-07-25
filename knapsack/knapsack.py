# 0-1 Knapsack problem
from flowty import Model
from fetch_knapsack import fetch

name, n, c, p, w, z, x = fetch("small", instance="knapPI_1_50_1000_1")

# Construct multi-graph
E = [(i, i + 1) for i in range(n)] + [(i, i + 1) for i in range(n)]

# zero profit and weight for 'pick not' edges
# signs are flipped for maximization
ps = [-x for x in p] + [0] * len(w)
ws = w + [0] * len(w)

m = Model()
# specify dynamic programming algorithm
m.setParam("Algorithm", "DP")

g = m.addGraph(obj=ps, edges=E, source=0, sink=n, L=1, U=1, type="B")

m.addResourceDisposable(
    graph=g, consumptionType="E", weight=ws, boundsType="V", lb=0, ub=c
)

status = m.optimize()
