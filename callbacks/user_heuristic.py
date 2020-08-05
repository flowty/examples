# vehicle routing with time windows

from flowty import Model, xsum, CallbackModel, Where

from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# the graph
g = m.addGraph(obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# resource constriants
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)


def callback(cb: CallbackModel, where: Where):
    # Heuristic
    if where == Where.PathMIPHeuristic:
        x = cb.x  # lp relaxation

        # add all 1-customer routes
        cost = 0
        xEdges = [0] * len(x)
        for i in range(n)[1:-1]:
            index = es.index((0, i))
            xEdges[index] = 1
            cost += c[index]
            index = es.index((i, n - 1))
            xEdges[index] = 1
            cost += c[index]

        cb.addSolution(cost, xEdges)


m.setCallback(callback)

# set partitioning constraints
for i in range(n)[1:-1]:
    m.addConstr(xsum(1 * x for x in g.vars if i == x.source) == 1)

    packingSet = [x for x in g.vars if i == x.source]
    m.addPackingSet(packingSet)

status = m.optimize()

print(f"ObjectiveValue {m.objectiveValue}")

# get the variables
xs = m.vars

for var in xs:
    if var.x > 0:
        print(f"{var.name} id:{var.idx} = {var.x}")
