# Vehicle Routing Problem with Time Windows
import flowty
import sys

sys.path.insert(1, "./v2/vrptw")
import fetch_vrptw

# from
# http://vrp.galgos.inf.puc-rio.br
# https://github.com/flowty/data/tree/main/data/vrptw
#
# C101...109, R101...112, RC101...108
# C201...208, R201...211, RC201...208
name, n, m, E, C, D, q, T, A, B, X, Y = fetch_vrptw.fetch("C101_25")

model = flowty.Model()

# one graph, it is identical for all vehicles
g = model.addGraph(obj=C, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# travel time and customer time windows
model.addResourceDisposable(
    graph=g, consumptionType="E", weight=T, boundsType="V", lb=A, ub=B
)

# demand and capacity
model.addResourceDisposable(
    graph=g, consumptionType="V", weight=D, boundsType="V", lb=0, ub=q
)

# set partition constriants
for i in range(1, n - 1):
    model += flowty.xsum(x for x in g.vars if i == x.source) == 1

# packing set
for i in range(1, n - 1):
    model.addPackingSet([x for x in g.vars if i == x.source])

status = model.optimize()

if (
    status == flowty.OptimizationStatus.Optimal
    or status == flowty.OptimizationStatus.Feasible
):
    print(f"Cost: {model.objectiveValue}")
    # for path in model.solutions[0].paths:
    #     print(f"Path {path.idx}")
    #     for var in path.vars:
    #         print(f" {var.name}")
