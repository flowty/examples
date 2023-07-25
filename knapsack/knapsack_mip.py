# 0-1 Knapsack problem
from flowty import Model, xsum
from fetch_knapsack import fetch

name, n, c, p, w, z, x = fetch("small", instance="knapPI_1_50_1000_1")

m = Model()
m.setParam("Algorithm", "MIP")

for i in range(n):
    m.addVar(lb=0, ub=1, obj=-p[i], type="B")

m.addConstr(xsum(w[i] * v for i, v in enumerate(m.vars)) <= c)

status = m.optimize()
