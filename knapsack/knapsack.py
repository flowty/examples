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
c = 47

# creating a 
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

# 0-1 Knapsack

m = Model()
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmDp)

g = m.addGraph(directed=True, obj=ps, edges=es, source=0, sink=6, L=1, U=1, type="B")

m.addResourceDisposable(
    graph=g, consumptionType="E", weight=ws, boundsType="V", lb=0, ub=c, obj=0
)

status = m.optimize()

print(f"ObjValue {m.objective}")

# get the variables
xs = m.vars

# for x in xs:
#    if x.x > 0:
#        print(f"{x.name} id:{x.idx} = {x.x}")

# display solution
import math

import networkx
import matplotlib
import matplotlib.pyplot as plt

if status == OptimizationStatus.Optimal or status == OptimizationStatus.Feasible:
    plt.figure(figsize=(20,10))
    
    edges = [x.edge for x in g.vars if not math.isclose(x.x, 0, abs_tol=0.001)]
    g = networkx.DiGraph()
    g.add_edges_from(edges)
    pos = networkx.spring_layout(g)
    networkx.draw_networkx_nodes(g, pos, nodelist=g.nodes)
    labels = {i: i for i in g.nodes}
    networkx.draw_networkx_labels(g, pos, labels=labels)


    one_edges = [e for e in g.edges if e[0] < len(w) and e[1] < len(w)]
    networkx.draw_networkx_edges(g, pos, edgelist=one_edges, edge_color='b')
    
    zero_edges = [e for e in g.edges if e not in one_edges]
    networkx.draw_networkx_edges(g, pos, edgelist=zero_edges, edge_color='r')
    
    plt.show()