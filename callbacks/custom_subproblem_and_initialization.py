# Vehicle Routing Problem with Time Windows

from flowty import Model, xsum, OptimizationStatus, CallbackModel, Where

from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# the graph
g = m.addGraph(obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B")


# The callback where we overwrite the internal subproblem algorithm
# and solve it ourselves
def callback(cb: CallbackModel, where: Where):
    # Pricing
    if where == Where.PathMIPSubproblem:
        # k = cb.k  # subproblem
        redCost = cb.reducedCost
        zeroEdges = cb.zeroEdges
        convexDual = cb.convexDual

        # invalidate zero edges by shrinking time window
        zeroA = list(a)
        zeroB = list(b)
        for e in zeroEdges:
            zeroA[e] = 0
            zeroB[e] = 0

        p = Model()
        # specify dynamic programming algorithm
        p.setParam("Algorithm", "DP")

        # one graph for the subproblem
        pg = p.addGraph(obj=redCost, edges=es, source=0, sink=n - 1, L=1, U=1, type="B")

        # adds resources variables to the graph.
        # demand and capacity
        p.addResourceDisposable(
            graph=pg,
            consumptionType="V",
            weight=d,
            boundsType="V",
            lb=0,
            ub=Q,
            name="d",
        )

        # travel time and customer time windows
        p.addResourceDisposable(
            graph=pg,
            consumptionType="E",
            weight=t,
            boundsType="V",
            lb=zeroA,
            ub=zeroB,
            name="t",
        )

        # Elementary paths needs license key - too many resources
        # for now solve the relaxation with cycles on paths
        #

        # for i in range(n)[1:-1]:
        #     w = [0] * n
        #     w[i] = 1
        #     p.addResourceDisposable(
        #         graph=pg,
        #         consumptionType="V",
        #         weight=w,
        #         boundsType="V",
        #         lb=0,
        #         ub=1,
        #         name=f"e_{i}",
        #     )

        status = p.optimize()

        if (
            status == OptimizationStatus.Optimal
            or status == OptimizationStatus.Feasible
        ):
            cost = p.objectiveValue

            if cost < convexDual - 1e-4:
                path = []
                for var in p.vars:
                    if var.x > 0:
                        path.append(var.idx)
                        print(f"{var.name} id:{var.idx} = {var.x}")
                cb.addPath(cost, path)

            cb.setStatus(status)

        # do not call internal algorithm
        cb.skip()

    # Initialization
    if where == Where.PathMIPInit:
        # k = cb.k  # we don't need the supbroblem index here

        # add all 1-customer routes
        for i in range(n)[1:-1]:
            cost = 0
            path = []

            index = es.index((0, i))
            path.append(index)
            cost += c[index]

            index = es.index((i, n - 1))
            path.append(index)
            cost += c[index]

            cb.addPath(cost, path)


m.setCallback(callback)

# set partition constriants
for i in range(n)[1:-1]:
    m += xsum(x * 1 for x in g.vars if i == x.source) == 1

# packing set
for i in range(n)[1:-1]:
    m.addPackingSet([x for x in g.vars if i == x.source])

status = m.optimize()
print(f"ObjectiveValue {round(m.objectiveValue, 1)}")

# get the variable values
for var in m.vars:
    if var.x > 0:
        print(f"{var.name} = {round(var.x, 1)}")
