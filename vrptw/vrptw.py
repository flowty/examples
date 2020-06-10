# vehicle routing with time windows

from flowty import (
    Model,
    xsum,
    ParamKey,
    ParamValue,
)

from flowty.datasets import vrp_rep

# playing with logging
import logging

logging.basicConfig(format=logging.BASIC_FORMAT)

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)
m.name = name

# one graph, it is identical for all vehicles.
g = m.addGraph(
    obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B",
)

# set partition constriants
for i in range(n)[1:-1]:
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

    packingSet = [x for x in g.vars if i == x.source]
    m.addPackingSet(packingSet)

# adds resources variables to the graph
m.addResourceDisposable(
    graph=g,
    consumptionType="V",
    weight=d,
    boundsType="V",
    lb=0,
    ub=Q,
    names="d",
)
m.addResourceDisposable(
    graph=g,
    consumptionType="E",
    weight=t,
    boundsType="V",
    lb=a,
    ub=b,
    names="t",
)

# visit at node at most once on a path
m.addResourceElementary(graph=g, type="V", names="e")

status = m.optimize()

print(f"ObjectiveValue {m.objectiveValue}")

m.write("dump")

m2 = Model()
m2.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)
m2.read("dump")

status = m2.optimize()

print(f"ObjectiveValue {m2.objectiveValue}")

# get the variables
# xs = m.vars

# for var in xs:
#     if var.x > 0:
#         print(f"{var.name} id:{var.idx} = {var.x}")
