# Multi Commodity Flow
import flowty
from fetch_fcmcf import fetch

name, n, m, k, E, c, u, f, s, t, d = fetch("Canad-C", "c33")

model = flowty.Model()

# define graphs
graphs = []
for i in range(k):
    graph = model.addGraph(
        obj=c, edges=E, source=s[i], sink=t[i], L=d[i], U=d[i], type="C"
    )
    model.addResourceDisposable(
        graph=graph, consumptionType="V", weight=1, boundsType="V", lb=0, ub=n
    )
    graphs.append(graph)

gvars = [g.vars for g in graphs]

# design variables
vars = [model.addVar(obj=f[i], type="B", name=f"y_{i}") for i in range(m)]

# demand constraints
for i in range(k):
    model += flowty.xsum(x for x in gvars[i] if x.source == graphs[i].source) == d[i]

# capacity constraints
for j in range(m):
    model += flowty.xsum(gvars[i][j] for i in range(k)) <= u[j] * vars[j]

status = model.optimize()

# get the variable values
if (
    status == flowty.OptimizationStatus.Optimal
    or status == flowty.OptimizationStatus.Feasible
):
    for path in model.solutions[0].paths:
        print(f"Path {path.idx}")
        for var in path.vars:
            print(f" {var.name}")
