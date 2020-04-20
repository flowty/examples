import igraph
from numpy.matlib import empty
from flowty import Model, xsum, ParamKey, ParamValue, LinExpr, OptimizationStatus


class Arc:
    def __init__(self, start, end, flow_cost, capacity, fixed_cost, time, id):
        self.id = int(id)
        self.start = int(start) - 1
        self.end = int(end) - 1
        self.flow_cost = flow_cost
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.time = time

    def __repr__(self):
        return "Arc: %i %i %i %i %i %i %f" % (self.id, self.start, self.end, self.flow_cost, self.capacity, self.fixed_cost, self.time)

    def __str__(self):
        return self.__repr__()


class Commodity:

    def __init__(self, origin, destination, amount, time_limit):
        self.id = 0
        self.origin = int(origin) - 1
        self.destination = int(destination) - 1
        self.amount = amount
        self.time_limit = time_limit

    def __repr__(self):
        return "Arc: %i %i %i %i %f" % (self.id, self.origin, self.destination, self.amount, self.time_limit)

    def __str__(self):
        return self.__repr__()


f = open("canadFC\\ttinstances\\tt_r06.1_12.csv")

N, A, K = [int(x) for x in f.readline().split(" ")]
print(N,A,K)
arcs = []
commodities = []

for a in range(A):
    arcs.append(Arc(*[float(x) for x in f.readline().split(",")]))
    arcs[a].id = a

for k in range(K):
    commodities.append(Commodity(*[float(x) for x in f.readline().split(",")]))
    commodities[k].id = k


# build the graph
g = igraph.Graph(directed=True)

# port call, origin, destination nodes
g.add_vertices(N)

# voyage, transit, load, forfeit edges
print([(arc.start, arc.end) for arc in arcs])
g.add_edges([(arc.start, arc.end) for arc in arcs])

# model building
m = Model()
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)
m.name = "main_model"

# number of subproblems

# resource constrained graphs
gs = []
for k in range(K):
    source = commodities[k].origin
    sink = commodities[k].destination
    obj = [arc.flow_cost for arc in arcs]
    edges = [(arc.start, arc.end) for arc in arcs]
    gk = m.addGraph(
        directed=True,
        obj=obj,
        edges=edges,
        source=source,
        sink=sink,
        L=1,
        U=1,
        type="C",
        names=f"x_{k}",
    )

    time = [arc.time for arc in arcs]
    m.addResourceDisposable(
        graph=gk,
        consumptionType="E",
        weight=time,
        boundsType="V",
        lb=0,
        ub=commodities[k].time_limit,
        obj=0,
        names=f"time_{k}",
    )
    gs.append(gk)



# graph vars
vars = [gs[k].vars for k in range(K)]

# design vars
y_vars = []
for a in range(A):
    y_vars.append(m.addVar(0, 1, arcs[a].fixed_cost, "B", r"y_%i" % a))


#sum_( i,j \in delta+(o^k)) x_ijk = 1 , forall k
for k in range(K):
    source = gs[k].source
    m.addConstr(xsum((1, x) for x in vars[k] if source == x.source) == 1)

for a in range(A):
    expr = LinExpr()
    for k in range(K):
        expr.addTerm(-commodities[k].amount, vars[k][a])
    expr.addTerm(arcs[a].capacity, y_vars[a])
    m.addConstr(expr >= 0)

status = m.optimize()
print("OPTIMISED")
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
    edges = [
        var.edge
        for i in range(k)
        for var in vars[i]
        if not math.isclose(var.x, 0, abs_tol=0.001)
    ]

    nodes = [v.index for v in g.vs]

    gn = networkx.DiGraph()
    gn.add_nodes_from(nodes)
    gn.add_edges_from(edges)
    pos = networkx.kamada_kawai_layout(gn)

    networkx.draw_networkx_labels(gn, pos)

    networkx.draw(gn, pos)
    plt.show()
