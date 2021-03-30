# time constrained multi-commodity flow
#
# Implements
#
# Christian Vad Karsten, David Pisinger, Stefan Ropke, and Berit Dangaard Brouer
# "The time constrained multi-commodity network flow problem and its application to
# liner shipping network design"
# Transportation Research Part E: Logistics and Transportation Review
# Volume 76, April 2015, Pages 122-138
# https://doi.org/10.1016/j.tre.2015.01.005

import networkx
from flowty import Model, xsum, LinExpr
from or_datasets import linerlib

# data = linerlib.fetch_linerlib(instance="Mediterranean")
# network = linerlib.fetch_linerlib_rotations(instance="Med_base_best")

data = linerlib.fetch_linerlib(instance="Baltic")
network = linerlib.fetch_linerlib_rotations(instance="Baltic_best_base")

name, _, _, _, _ = data["instance"]

builder = linerlib.GraphBuilder(data, network)

# build the graph
g = networkx.DiGraph()

# port call, origin, destination nodes
g.add_nodes_from(
    [
        (n, {"index": g.number_of_nodes() + i})
        for i, n in enumerate(builder.portCallNodes())
    ]
)
g.add_nodes_from(
    [
        (n, {"index": g.number_of_nodes() + i})
        for i, n in enumerate(builder.originNodes())
    ]
)
g.add_nodes_from(
    [
        (n, {"index": g.number_of_nodes() + i})
        for i, n in enumerate(builder.destinationNodes())
    ]
)

# voyage, transit, load, forfeit edges
voyageEdges = builder.voyageEdges()
g.add_edges_from(
    [
        (n[0], n[1], {"index": g.number_of_edges() + i})
        for i, n in enumerate(voyageEdges)
    ]
)
g.add_edges_from(
    [
        (n[0], n[1], {"index": g.number_of_edges() + i})
        for i, n in enumerate(builder.transitEdges())
    ]
)
g.add_edges_from(
    [
        (n[0], n[1], {"index": g.number_of_edges() + i})
        for i, n in enumerate(builder.loadEdges())
    ]
)
g.add_edges_from(
    [
        (n[0], n[1], {"index": g.number_of_edges() + i})
        for i, n in enumerate(builder.forfeitEdges())
    ]
)

# model building
m = Model()

# number of subproblems
k = len(builder.demand["Destination"])

# for keeping track of voyage edge variables
voyageEdgeIds = [g.edges[edge[0], edge[1]] for edge in voyageEdges]
voyageEdgeVarsIds = [{} for j in range(len(voyageEdgeIds))]

# resource constrained graphs
gs = []
for i in range(k):
    origin = builder.demand["Origin"][i]
    dest = builder.demand["Destination"][i]
    vs = builder.portCallNodes() + [f"O{i}_{origin}", f"D{i}_{dest}"]
    es = g.edges(nbunch=vs)

    source = g.nodes[f"O{i}_{origin}"]["index"]
    sink = g.nodes[f"D{i}_{dest}"]["index"]
    obj = [
        builder.demand["FFEPerWeek"][i] * builder.cost[g.edges[e]["index"]] for e in es
    ]
    edges = [(g.nodes[e[0]]["index"], g.nodes[e[1]]["index"]) for e in es]
    gk = m.addGraph(
        obj=obj,
        edges=edges,
        source=source,
        sink=sink,
        L=1,
        U=1,
        type="C",
        names=f"x_{i}",
    )

    time = [builder.travelTime[g.edges[e]["index"]] for e in es]
    m.addResourceDisposable(
        graph=gk,
        consumptionType="E",
        weight=time,
        boundsType="V",
        lb=0,
        ub=builder.demand["TransitTime"][i],
        name=f"time_{i}",
    )
    gs.append(gk)

    # keep track of voyageEdges for constraints later
    tmp = list([eid["index"] for eid in voyageEdgeIds])
    for j, e in enumerate(es):
        for h, eid in enumerate(tmp):
            if g.edges[e]["index"] == eid:
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

status = m.optimize()
# print(f"ObjectiveValue {round(m.objectiveValue, 5)}")

# get the variable values
# for var in m.vars:
#     if var.x > 0:
#         print(f"{var.name} = {round(var.x, 5)}")
