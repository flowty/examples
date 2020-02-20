# vehicle routing with time windows

from flowty import Model, xsum, IntParam
from flowty.datasets import fetch_vrp_rep

bunch = fetch_vrp_rep("solomon-1987-r1", instance="R101_050")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

#####################################
# Modelling with implicit subproblem definitions

# build model, add aggregated graphs and resources.
# Extracting to MIP may result in 3-index model or 2-index model depending on resources and number of aggregations
m = Model()

m.setParam(IntParam.Algorithm, 6)

# one graph, it is identical for all vehicles.
# creates variables per edge and constraints for a single from source to sink
g = m.addGraph(
# for U > 1, the parameter specifies that there are identical subproblems
    directed=True, obj=c, edges=es, source=0, sink=n - 1, L=1, U=n-2, type="B", namePrefix="x"
)

# set partition constriants per customer
# only |E| variables due to aggregation
for i in range(n)[1:-1]:
    m.addConstr(xsum(x * 1 for x in g.vars if i == x.source) == 1)

# adds resources variables to the graph, again an aggregation therefore only |V|
# inputs for weights, lb, and ub can be arrays or constants that is replicated per edge/vertex
m.addResourceDisposible(
    graph=g,
    consumptionType="V",
    weight=d,
    boundsType="V",
    lb=0,
    ub=Q,
    obj=0,
    namePrefix="d",
)
m.addResourceDisposible(
    graph=g,
    consumptionType="E",
    weight=t,
    boundsType="V",
    lb=a,
    ub=b,
    obj=0,
    namePrefix="t",
)

# visit at node at most once on a path
m.addResourceElementary(graph=g, type="V", namePrefix="e")

# m.write("dump.lp")

status = m.optimize()

# get the variables
xs = m.vars

for x in xs:
    if x.x > 0:
        print(f"{x.name} id:{x.idx} = {x.x}")
