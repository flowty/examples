# Vehicle Routing Problem with Time Windows
from flowty import Model, xsum, OptimizationStatus
from fetch_vrptw import fetch

name, n, E, c, d, Q, t, a, b, x, y = fetch("Solomon", "R102", 25)

m = Model()

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# travel time and customer time windows
m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)

# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

# set partition constriants
for i in range(1, n - 1):
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

# packing set
for i in range(1, n - 1):
    m.addPackingSet([x for x in g.vars if i == x.source])

status = m.optimize()

# get the variable values
if status == OptimizationStatus.Optimal:
    for path in m.solutions[0].paths:
        print(f"Path {path.idx}")
        for var in path.vars:
            print(f" {var.name}")
