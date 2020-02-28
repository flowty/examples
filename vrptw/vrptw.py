# vehicle routing with time windows

from flowty import Model, xsum, ParamKey, ParamValue, OptimizationStatus
from flowty.datasets import fetch_vrp_rep

bunch = fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

#####################################
# Modelling with implicit subproblem definitions

# build model, add aggregated graphs and resources.
# Extracting to MIP may result in 3-index model or 2-index model depending on resources and number of aggregations
m = Model()
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)
m.name = name

# one graph, it is identical for all vehicles.
# creates variables per edge and constraints for a single from source to sink
g = m.addGraph(
    # for U > 1, the parameter specifies that there are identical subproblems
    directed=True,
    obj=c,
    edges=es,
    source=0,
    sink=n - 1,
    L=1,
    U=n - 2,
    type="B",
)

# set partition constriants per customer
# only |E| variables due to aggregation
for i in range(n)[1:-1]:
    m.addConstr(xsum(x * 1 for x in g.vars if i == x.source) == 1)

# adds resources variables to the graph, again an aggregation therefore only |V|
# inputs for weights, lb, and ub can be arrays or constants that is replicated per edge/vertex
m.addResourceDisposible(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, obj=0, names="d"
)
m.addResourceDisposible(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, obj=0, names="t"
)

# visit at node at most once on a path
m.addResourceElementary(graph=g, type="V", names="e")

# m.write("dump.lp")

status = m.optimize()

# get the variables
xs = m.vars

for var in xs:
    if var.x > 0:
        print(f"{var.name} id:{var.idx} = {var.x}")

# display solution
import math
import networkx
import matplotlib
import matplotlib.pyplot as plt

if status == OptimizationStatus.Optimal or status == OptimizationStatus.Feasible:
    edges = [var.edge for var in g.vars if not math.isclose(var.x, 0, abs_tol=0.001)]
    g = networkx.DiGraph()
    g.add_nodes_from([i for i in range(n)])
    g.add_edges_from(edges)
    pos = {i: (x[i], y[i]) for i in range(n)}

    networkx.draw_networkx_nodes(g, pos, nodelist=g.nodes)
    labels = {i: i for i in g.nodes}
    networkx.draw_networkx_labels(g, pos, labels=labels)

    networkx.draw_networkx_edges(g, pos, nodelist=g.edges)

    plt.show()
