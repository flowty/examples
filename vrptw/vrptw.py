# Vehicle Routing Problem with Time Windows

from flowty import Model, xsum
from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

# travel time and customer time windows
m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)

# set partition constriants
for i in range(n)[1:-1]:
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

# packing set
for i in range(n)[1:-1]:
    m.addPackingSet([x for x in g.vars if i == x.source])

status = m.optimize()
print(f"ObjectiveValue {round(m.objectiveValue, 1)}")

# get the variable values
for var in m.vars:
    if var.x > 0:
        print(f"{var.name} = {round(var.x, 1)}")
