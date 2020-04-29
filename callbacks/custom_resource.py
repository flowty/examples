# vehicle routing with time windows

import logging

logging.basicConfig(format=logging.BASIC_FORMAT)


from flowty import (
    Model,
    xsum,
    ParamKey,
    ParamInt,
    ParamValue,
    OptimizationStatus,
    CallbackModel,
    Where,
)

from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()
# use the PathMip algorithm
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)

# the graph
g = m.addGraph(
    directed=True, obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B"
)

# resource constriants
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, obj=0, names="d"
)

# m.addResourceDisposable(
#     graph=g,
#     consumptionType="E",
#     weight=t,
#     boundsType="V",
#     lb=a,
#     ub=b,
#     obj=0,
#     names="t",
# )


def callback(cb: CallbackModel, where: Where):
    # initialization
    if where == Where.DpInit:
        cb.setResource("time", 0)

    # extension
    if where == Where.DpExtend:
        e = cb.edge
        j = es[e][1]
        value = cb.getResource("time")
        value = max(a[j], value + t[e])

        if value > b[j]:
            cb.reject()
        else:
            cb.setResource("time", value)

    # dominance
    if where == Where.DpDominate:
        value = cb.getResource("time")
        other = cb.getResourceOther("time")

        if other < value:
            cb.reject()


m.setCallback(callback)
m.addResourceCustom(graph=g, name="time")

m.addResourceElementary(graph=g, type="V", names="e")

# set partitioning constraints
for i in range(n)[1:-1]:
    m.addConstr(xsum(1 * x for x in g.vars if i == x.source) == 1)

status = m.optimize()

print(f"ObjValue {m.objective}")

# get the variables
xs = m.vars

# for var in xs:
#     if var.x > 0:
#         print(f"{var.name} id:{var.idx} = {var.x}")

# display solution
# import math
# import networkx
# import matplotlib
# import matplotlib.pyplot as plt

# if (
#     status == OptimizationStatus.Optimal
#     or status == OptimizationStatus.Feasible
# ):
#     edges = [
#         var.edge
#         for var in g.vars
#         if not math.isclose(var.x, 0, abs_tol=0.001)
#     ]
#     g = networkx.DiGraph()
#     g.add_nodes_from([i for i in range(n)])
#     g.add_edges_from(edges)
#     pos = {i: (x[i], y[i]) for i in range(n)}

#     networkx.draw_networkx_nodes(g, pos, nodelist=g.nodes)
#     labels = {i: i for i in g.nodes}
#     networkx.draw_networkx_labels(g, pos, labels=labels)

#     networkx.draw_networkx_edges(g, pos, edgeslist=g.edges)

#     plt.show()
