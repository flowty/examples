# 0-1 knapsack problem

from flowty import (
    Model,
    xsum,
    CallbackModel,
    ParamKey,
    ParamValue,
    OptimizationStatus,
    Where,
)

p = [10, 13, 18, 31, 7, 15]
w = [11, 15, 20, 35, 10, 33]
c, I = 47, range(len(w))

es = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (0, 7),
    (1, 8),
    (2, 9),
    (3, 10),
    (4, 11),
    (5, 12),
    (7, 1),
    (8, 2),
    (9, 3),
    (10, 4),
    (11, 5),
    (12, 6),
]
ps = [-x for x in p] + [0] * len(w) * 2
ws = w + [0] * len(w) * 2

# es = [(0,1), (1,2), (2,3), (3,4), (4,5), (5, 6),
#  (0,1), (1,2), (2,3), (3,4), (4,5), (5,6)
#  ]
# ps = [-x for x in p] + [0] * len(w)
# ws = w + [0] * len(w)

m = Model()
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmDp)


def callback(callbackModel: CallbackModel, where: Where):
    if where == Where.DpInit:
        callbackModel.setResource("res", 20)
        return

    if where == Where.DpExtend:
        e = callbackModel.edge
        value = callbackModel.getResource("res")
        callbackModel.setResource("res", value + 2)
        return

    if where == Where.DpDominate:
        value = callbackModel.getResource("res")
        other = callbackModel.getResourceOther("res")
        return


m.setCallback(callback)

# one graph, it is identical for all vehicles.
# creates variables per edge and constraints for a single from source to sink
# for U > 1, the parameter specifies that there are identical subproblems
g = m.addGraph(directed=True, obj=ps, edges=es, source=0, sink=6, L=1, U=1, type="B")

m.addResourceDisposible(
    graph=g, consumptionType="E", weight=ws, boundsType="V", lb=0, ub=c, obj=0
)

m.addResourceCustom(graph=g, name="res")

# m.write("dump.lp")

status = m.optimize()

# get the variables
xs = m.vars

for x in xs:
    if x.x > 0:
        print(f"{x.name} id:{x.idx} = {x.x}")

# display solution
import math

# import igraph
# import cairocffi as cairo # noqa: needed by igraph.plot `pip install cairocffi`
# from IPython.core.display import display, SVG # noqa: `pip install ipython`

# if status == OptimizationStatus.Optimal or status == OptimizationStatus.Feasible:
#     edges = [x.edge for x in g.vars if not math.isclose(x.x, 0, abs_tol=0.001)]
#     g = igraph.Graph(directed=True, edges=edges)
#     g.vs["label"] = [v.index for v in g.vs]  # label the nodes
#     g.es["label"] = [e.source if e.target < len(w) and e.source < len(w) else "" for e in g.es]  # label the nodes
#     display(SVG(igraph.plot(g)._repr_svg_()))

#     # layout
#     layout = [(x[i], y[i]) for i in range(g.vcount())]  # node coordinates
#     display(SVG(igraph.plot(g, layout=layout)._repr_svg_()))

import networkx
import matplotlib
import matplotlib.pyplot as plt

if status == OptimizationStatus.Optimal or status == OptimizationStatus.Feasible:
    edges = [x.edge for x in g.vars if not math.isclose(x.x, 0, abs_tol=0.001)]
    g = networkx.DiGraph()
    g.add_edges_from(edges)
    pos = networkx.spring_layout(g)
    networkx.draw_networkx_nodes(g, pos, nodelist=g.nodes)
    labels = {i: i for i in g.nodes}
    networkx.draw_networkx_labels(g, pos, labels=labels)

    networkx.draw_networkx_edges(g, pos, nodelist=g.edges)
    labels = {e: e[0] if e[0] < len(w) and e[1] < len(w) else "" for e in g.edges}
    networkx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

    plt.show()
