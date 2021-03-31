# Vehicle Routing Problem with Time Windows
import math
from flowty import Model, xsum, CallbackModel, Where
from or_datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, E, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

# travel time and customer time windows
m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)


# The callback for adding rounded capacity cuts
# x(delta(S)) >= floor( sum_(i \in S) d_i / Q ) ,  S \subset C, |S| >= 2
#
# We do a pretty stupid enumeration of all sets S with |S| = 2
# Do something smarter like CVRPSEP
def callback(cb: CallbackModel, where: Where):
    if where == Where.PathMIPCuts:
        epsilon = 1e-4
        relax = cb.x

        # Enumerate cuts for |S| = 2
        for i in range(n)[1:-1]:
            for j in range(n)[1:-1]:

                # not depot nodes in S
                if i == 0 or j == n - 1 or i == j:
                    continue

                rhs = math.ceil((d[i] + d[j]) / Q)

                lhs = 0
                lhsIdxs = []
                for e, edge in enumerate(E):
                    # inside S
                    if (i, j) == edge or (j, i) == edge:
                        continue

                    # if either end of edge is in S
                    if i == edge[0] or i == edge[1] or j == edge[0] or j == edge[1]:
                        lhs += relax[e]
                        lhsIdxs += [e]

                if lhs < rhs - epsilon:
                    cb.addCut(xsum(g.vars[e] for e in lhsIdxs) >= rhs)


m.setCallback(callback)

# set partition constriants
for i in range(n)[1:-1]:
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

# packing set
for i in range(n)[1:-1]:
    m.addPackingSet([x for x in g.vars if i == x.source])

status = m.optimize()
# print(f"ObjectiveValue {round(m.objectiveValue, 1)}")

# get the variable values
# for var in m.vars:
#     if var.x > 0:
#         print(f"{var.name} = {round(var.x, 1)}")
