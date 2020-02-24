# time constrained multi-commodity flow
#
# Implements
#
# Christian Vad Karsten, David Pisinger, Stefan Ropke, and Berit Dangaard Brouer
# "The time constrained multi-commodity network flow problem and its application to liner shipping network design"
# Transportation Research Part E: Logistics and Transportation Review Volume 76, April 2015, Pages 122-138
# https://doi.org/10.1016/j.tre.2015.01.005


import igraph
import mip
from flowty.decomposition import Mapping, NetworkModel
from flowty.datasets import fetch_linerlib, fetch_linerlib_rotations, linerlib

data = fetch_linerlib(instance="Baltic")
network = fetch_linerlib_rotations(instance="Baltic_best_base")

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

# resource constrained graphs
gs = []
for i in range(len(builder.demand["Destination"])):
    origin = builder.demand["Origin"][i]
    dest = builder.demand["Destination"][i]
    vs = g.vs.select(
        name_in=builder.portCallNodes() + [f"O{i}_{origin}", f"D{i}_{dest}"]
    )

    gk = g.subgraph(vs)
    gk.es["cost"] = builder.cost
    gk.es["time"] = builder.travelTime
    gk.vs["time_lb"] = 0
    gk.vs["time_ub"] = builder.demand["TransitTime"][i]
    gk["main"] = ["time"]
    gk["source"] = f"O{i}_{origin}"
    gk["target"] = f"D{i}_{dest}"
    gs.append(gk)


# mip helper function to get variable name from edge
def getVarName(k, i, j=None):
    if j:
        return f"e({i},{j},{k})"

    return f"e({gs[k].vs[i.source]['name']},{gs[k].vs[i.target]['name']},{k})"


# mip helper function to get variable index from subgraph edge
def getIndex(i):
    s = g.vs.find(name_eq=i.source_vertex["name"])
    t = g.vs.find(name_eq=i.target_vertex["name"])
    e = g.es.find(_source_eq=s.index, _target_eq=t.index)
    return e.index


# mip model
m = mip.Model()
xs = {
    getVarName(k, e): m.add_var(var_type=mip.CONTINUOUS, name=getVarName(k, e))
    for k, gk in enumerate(gs)
    for e in gk.es
}

m.objective = mip.xsum(
    builder.demand["FFEPerWeek"][k] * builder.cost[getIndex(e)] * xs[getVarName(k, e)]
    for k, gk in enumerate(gs)
    for e in gk.es
)

# demand per commodity
for i in range(len(builder.demand["Destination"])):
    origin = builder.demand["Origin"][i]
    dest = builder.demand["Destination"][i]
    v = gs[i].vs.find(name_eq=f"O{i}_{origin}")
    es = gs[i].incident(v)

    m += (mip.xsum(xs[getVarName(i, gs[i].es[eid])] for eid in es) == 1, f"d({i})")

# edge capacity constraints
for i, e in enumerate(voyageEdges):
    m += (
        mip.xsum(
            builder.demand["FFEPerWeek"][k] * xs[getVarName(k, e[0], e[1])]
            for k in range(len(gs))
        )
        >= builder.capacity[i],
        f"c({i})",
    )

# convexity bounds
L = [1] * len(gs)
U = [1] * len(gs)

# mapping between mip and graph
mapping = Mapping({xs[getVarName(k, e)]: [e] for k, gk in enumerate(gs) for e in gk.es})


net = NetworkModel(m, mapping, list(zip(gs, L, U)))
status = net.solve()
