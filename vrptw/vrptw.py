# Vehicle Routing Problem with Time Windows
import sys
from flowty import Model, xsum
from or_datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, E, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()

# Get reduced number of customers from cmd line
if len(sys.argv) > 1:
    numCustomer = int(sys.argv[1])

    print(f"Number of customers: {numCustomer}")

    # strip customers
    old_n = n
    n = numCustomer + 2
    data = [
        ((e[0], e[1]), c[i], t[i])
        for i, e in enumerate(E)
        if (e[0] < n - 1 and e[1] < n - 1) or (e[0] < n - 1 and e[1] == old_n - 1)
    ]
    E = [e[0] for e in data]
    E = [e if e[1] != old_n - 1 else (e[0], n - 1) for e in E]
    c = [e[1] for e in data]
    t = [e[2] for e in data]

    d = d[: n - 1] + [d[-1]]
    a = a[: n - 1] + [a[-1]]
    b = b[: n - 1] + [b[-1]]

# one graph, it is identical for all vehicles
g = m.addGraph(obj=c, edges=E, source=0, sink=n - 1, L=1, U=n - 2, type="B")

# adds resources variables to the graph.
# travel time and customer time windows
m.addResourceDisposable(
    graph=g, consumptionType="E", weight=t, boundsType="V", lb=a, ub=b, name="t"
)

# demand and capacity
m.addResourceDisposable(
    graph=g, consumptionType="V", weight=d, boundsType="V", lb=0, ub=Q, name="d"
)

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
