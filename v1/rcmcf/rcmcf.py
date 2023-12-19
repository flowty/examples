from flowty import Model, xsum, OptimizationStatus
import sys

sys.path.insert(1, "./v2/rcmcf")
import fetch_rcmcf

model = Model()

# from
# https://github.com/flowty/LINERLIB
# https://github.com/flowty/flow-first-route-next-heuristic-shipping-network-design
# https://github.com/flowty/data/tree/main/data/linerlib
#
# Baltic ...
name, n, m, k, E, C, U, O, D, B, R, T = fetch_rcmcf.fetch("WAF_base_best")

# create graphs per commodity
graphs = []
for o, d, b, r in zip(O, D, B, R):
    graph = model.addGraph(
        obj=C,
        edges=E,
        source=o,
        sink=d,
        L=0,
        U=b,
        type="C",
    )
    # add transit time constraints to graphs
    model.addResourceDisposable(graph=graph, consumptionType="E", weight=T, lb=0, ub=r)
    graphs.append(graph)

gvars = {g: g.vars for g in graphs}

# penalty variables
penalty = sum(C) + 1
Y = [model.addVar(obj=penalty, lb=0, name=f"y_{g.idx}") for g in graphs]

# demand constraints
for g, b, y in zip(graphs, B, Y):
    model.addConstr(xsum(x for x in gvars[g] if x.source == g.source) + y == b)

# capacity constraints
sumDemand = sum(B)
for i, u in enumerate(U):
    if u < sumDemand:
        model.addConstr(xsum(gvars[g][i] for g in graphs) <= u)

status = model.optimize()
if status != OptimizationStatus.Infeasible:
    print(f"ObjectiveValue {round(model.objectiveValue, 2)}")
