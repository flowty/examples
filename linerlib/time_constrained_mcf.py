# time constrained multi-commodity flow
#
# Implements
#
# Christian Vad Karsten, David Pisinger, Stefan Ropke, and Berit Dangaard Brouer
# "The time constrained multi-commodity network flow problem and its application to liner shipping network design"
# Transportation Research Part E: Logistics and Transportation Review Volume 76, April 2015, Pages 122-138
# https://doi.org/10.1016/j.tre.2015.01.005


import igraph
from flowty import Model, xsum, IntParam, LinExpr
from flowty.datasets import fetch_linerlib, fetch_linerlib_rotations, linerlib

# data = fetch_linerlib(instance="Mediterranean")
# network = fetch_linerlib_rotations(instance="Med_base_best")

data = fetch_linerlib(instance="Baltic")
network = fetch_linerlib_rotations(instance="Baltic_best_base")

name, _, _, _, _ = data["instance"]

builder = linerlib.GraphBuilder(data, network)

# build the graph
g = igraph.Graph(directed=True)

# port call, origin, destination nodes
g.add_vertices(builder.portCallNodes())
g.add_vertices(builder.originNodes())
g.add_vertices(builder.destinationNodes())

# voyage, transit, load, forfeit edges
voyageEdges = builder.voyageEdges()
g.add_edges(voyageEdges)
g.add_edges(builder.transitEdges())
g.add_edges(builder.loadEdges())
g.add_edges(builder.forfeitEdges())

# model building
m = Model()
m.setParam(IntParam.Algorithm, 6)
m.name = name

# number of subproblems
k = len(builder.demand["Destination"])

# for keeping track of voyage edge variables
voyageEdgeIds = [
    g.es.find(
        _source=g.vs.find(name=edge[0]).index, _target=g.vs.find(name=edge[1]).index
    ).index
    for edge in voyageEdges
]
voyageEdgeVarsIds = [{} for j in range(len(voyageEdgeIds))]

# resource constrained graphs
gs = []
for i in range(k):
    origin = builder.demand["Origin"][i]
    dest = builder.demand["Destination"][i]
    vs = g.vs.select(
        name_in=builder.portCallNodes() + [f"O{i}_{origin}", f"D{i}_{dest}"]
    )
    es = g.es.select(_within=[v.index for v in vs])

    source = g.vs.find(f"O{i}_{origin}").index
    sink = g.vs.find(f"D{i}_{dest}").index
    obj = [builder.demand["FFEPerWeek"][i] * builder.cost[e.index] for e in es]
    edges = [(e.source, e.target) for e in es]
    gk = m.addGraph(
        directed=True,
        obj=obj,
        edges=edges,
        source=source,
        sink=sink,
        L=1,
        U=1,
        type="C",
        names=f"x_{i}",
    )

    time = [builder.travelTime[e.index] for e in es]
    m.addResourceDisposible(
        graph=gk,
        consumptionType="E",
        weight=time,
        boundsType="V",
        lb=0,
        ub=builder.demand["TransitTime"][i],
        obj=0,
        names=f"time_{i}",
    )
    gs.append(gk)

    # keep track of voyageEdges for constraints later
    tmp = list(voyageEdgeIds)
    for j, e in enumerate(es):
        for h, eid in enumerate(tmp):
            if e.index == eid:
                voyageEdgeVarsIds[eid][i] = j
                tmp.remove(eid)
                break

# graph vars
vars = [gs[i].vars for i in range(k)]

# sum_( i,j \in delta+(o^k)) x_ijk = 1 , forall k
for i in range(k):
    source = gs[i].source
    m.addConstr(xsum((1, x) for x in vars[i] if source == x.source) == 1)

for j, ks in enumerate(voyageEdgeVarsIds):
    expr = LinExpr()
    for i, h in ks.items():
        x = vars[i][h]
        expr.addTerm(builder.demand["FFEPerWeek"][i], x)
    m.addConstr(expr <= builder.capacity[j])

# sum_(k) x_ijk <= u_ij , forall i,j
# for j, edge in enumerate(voyageEdges):
#     e = (g.vs.find(name=edge[0]).index, g.vs.find(name=edge[1]).index)
#     m.addConstr(
#         xsum(
#             (builder.demand["FFEPerWeek"][i], x)
#             for i in range(k)
#             for x in vars[i]
#             if x.edge == e
#         )
#         <= builder.capacity[j]
#     )

status = m.optimize()

# get the variables
xs = m.vars

for x in xs:
    if x.x > 0:
        print(f"{x.name} id:{x.idx} = {x.x}")
