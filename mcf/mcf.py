# Multi Commodity Flow
import flowty
import fetch_mcf

name, n, m, k, E, C, U, O, D, B = fetch_mcf.fetch("grid", 1)

model = flowty.Model()

# define graphs
graphs = []
for o, d, b in zip(O, D, B):
    g = model.addGraph(obj=C, edges=E, source=o, sink=d, L=b, U=b, type="C")
    model.addResourceDisposable(
        graph=g, consumptionType="V", weight=1, boundsType="V", lb=0, ub=n
    )
    graphs.append(g)

# demand constraints
for g, b in zip(graphs, B):
    model += flowty.xsum(x for x in g.vars if x.source == g.source) == b

# capacity constraints
for u, X in zip(U, zip(*[g.vars for g in graphs])):
    model += flowty.xsum(X) <= u

status = model.optimize()

# get the variable values
#
# if (
#     status == flowty.OptimizationStatus.Optimal
#     or status == flowty.OptimizationStatus.Feasible
# ):
#     for path in model.solutions[0].paths:
#         print(f"Path {path.idx}")
#         for var in path.vars:
#             print(f" {var.name}")
