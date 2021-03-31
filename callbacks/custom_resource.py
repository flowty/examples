# Vehicle Routing Problem with Time Windows
from flowty import Model, xsum, CallbackModel, Where
from or_datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, E, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# Make sure to invoke callback in the dynamic progrmaming algorithm
m.setParam("CallbackDP", "On")

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

# A custom resource to handle time
m.addResourceCustom(graph=g, name="time")


# The callback for handling the time resource
def callback(cb: CallbackModel, where: Where):
    # initialization
    if where == Where.DPInit:
        cb.setResource("time", 0)

    # extension
    if where == Where.DPExtend:
        e = cb.edge
        j = E[e][1]
        value = cb.getResource("time")
        value = max(a[j], value + t[e])

        if value > b[j]:
            cb.skip()
        else:
            cb.setResource("time", value)

    # dominance
    if where == Where.DPDominate:
        value = cb.getResource("time")
        other = cb.getResourceOther("time")

        # label is not dominated
        if other < value:
            cb.keep()


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
