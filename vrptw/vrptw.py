# vehicle routing with time windows

from flowty import Model
from flowty.datasets import fetch_vrp_rep

bunch = fetch_vrp_rep("solomon-1987-r1", instance="R101_050")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

#####################################
# Modelling with implicit subproblem definitions

# build model, add aggregated graphs and resources.
# Extracting to MIP may result in 3-index model or 2-index model depending on resources and number of aggregations
m = Model()

# one graph, it is identical for all vehicles.
# creates variables per edge and constraints for a single from source to sink
# for U > 1, the parameter specifies that there are identical subproblems
g = m.addGraph(
    Directed=True, cost=c, edges=es, source=0, sink=n - 1, L=1, U=n-2, type="B", name="x"
)

# set partition constriants per customer
# only |E| variables due to aggregation
for i in range(n)[1:-1]:
    m.addConstraint(x * 1 for x in g.x if i == x.source == 1)

# adds resources variables to the graph, again an aggregation therefore only |V|
# inputs for weights, lb, and ub can be arrays or constants that is replicated per edge/vertex
m.addResourceDisposible(
    graph=g,
    consumptionType="V",
    weight=d,
    boundsType="V",
    lb=0,
    ub=Q,
    cost=0,
    name="demand",
)
m.addResourceDisposible(
    graph=g,
    consumptionType="E",
    weight=t,
    boundsType="V",
    lb=a,
    ub=b,
    cost=0,
    name="time",
)
# visit at node at most once on a path
m.addResourceElementary(graph=g, type="V")

m.optimize()
status = m.Status
# get the 2-index aggregated variables
xs = m.getVars(name="x")
# gets the 3-index variables
xsk = m.getVarsDisaggregated(name="x")
