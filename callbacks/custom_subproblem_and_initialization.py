# vehicle routing with time windows

from flowty import (
    Model,
    xsum,
    ParamKey,
    ParamValue,
    OptimizationStatus,
    CallbackModel,
    Where,
)

from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()
# use the PathMip algorithm
m.setParam(ParamKey.Algorithm, ParamValue.AlgorithmPathMip)

# the graph
g = m.addGraph(
    directed=True, obj=c, edges=es, source=0, sink=n - 1, L=1, U=n - 2, type="B"
)


def callback(cb: CallbackModel, where: Where):
    # Pricing
    if where == Where.PathMipSubproblem:
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
        p.setParam(ParamKey.Algorithm, ParamValue.AlgorithmDp)
        pg = p.addGraph(
            directed=True,
            obj=redCost,
            edges=es,
            source=0,
            sink=n - 1,
            L=1,
            U=1,
            type="B",
        )

        # resource constriants
        p.addResourceDisposable(
            graph=pg,
            consumptionType="V",
            weight=d,
            boundsType="V",
            lb=0,
            ub=Q,
            obj=0,
            names="d",
        )

        p.addResourceDisposable(
            graph=pg,
            consumptionType="E",
            weight=t,
            boundsType="V",
            lb=zeroA,
            ub=zeroB,
            obj=0,
            names="t",
        )
        p.addResourceElementary(graph=pg, type="V", names="e")

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

        cb.reject()

    # Initialization
    if where == Where.PathMipInit:
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

# set partitioning constraints
for i in range(n)[1:-1]:
    m.addConstr(xsum(1 * x for x in g.vars if i == x.source) == 1)

status = m.optimize()

print(f"ObjectiveValue {m.objectiveValue}")

# get the variables
xs = m.vars

for var in xs:
    if var.x > 0:
        print(f"{var.name} id:{var.idx} = {var.x}")
