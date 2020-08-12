# vehicle routing with time windows

from flowty import Model, xsum
from flowty.datasets import vrp_rep

bunch = vrp_rep.fetch_vrp_rep("solomon-1987-r1", instance="R102_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

m = Model()
m.setParam("Algorithm", "MIP")

# placeholder for added variables
xs = []

# construct a 3-index model
# add varaibles and constraints for each subproblem
for k in range(n)[1:-1]:
    # edge variables for this subproblem
    xsk = [
        m.addVar(lb=0, ub=1, obj=c[i], type="B", name=f"x_({e[0]},{e[1]})_{k}")
        for i, e in enumerate(es)
    ]
    xFeasiblity = m.addVar(lb=0, ub=1, obj=0, type="B", name=f"x_({0},{n-1})_{k}")
    xs += xsk

    # graph, flow constraints
    # sum_(0,j) x_0j = 1
    [m.addConstr(xsum(1 * x for x, e in zip(xsk, es) if e[0] == 0) + xFeasiblity == 1)]

    # sum_(j) x_ji - sum_(j) x_ij = 0 , forall i
    for i in range(n)[1:-1]:
        [
            m.addConstr(
                xsum(1 * x for x, e in zip(xsk, es) if e[1] == i)
                + xsum(-1 * x for x, e in zip(xsk, es) if e[0] == i)
                == 0
            )
        ]
    # sum_(j,n-1) x_j,n-1 = 1
    [
        m.addConstr(
            xsum(1 * x for x, e in zip(xsk, es) if e[1] == n - 1) + xFeasiblity == 1
        )
    ]

    # capacity constraint
    # sum_(ij) d_i * x_ij <= Q
    [m.addConstr(xsum(x * d[e[0]] for x, e in zip(xsk, es)) <= Q)]

    # time stamp per vertex
    qt = [
        m.addVar(lb=0, ub=max(b), obj=0, type="C", name=f"q_t_{i}_{k}")
        for i in range(n)
    ]

    # time winwos
    bigM = max(b)    
    # q_ik + t_ij - q_jk <= (1 - x_ijk)M , forall (i,j)
    for j, e in enumerate(es):
        [m.addConstr(qt[e[0]] * 1 - qt[e[1]] * 1 + xsk[j] * bigM <= bigM - t[j])]
    # a_i sum_(j) x_ijk <= q_ik
    for i in range(n):
        [m.addConstr(xsum(a[i] * x for x, e in zip(xsk, es) if e[0] == i) - qt[i] <= 0)]
    # q_ik <= b_i sum_(j) x_ijk
    for i in range(n):
        [
            m.addConstr(
                xsum(-b[i] * x for x, e in zip(xsk, es) if e[0] == i) + qt[i] <= 0
            )
        ]

# set partition constraints
for i in range(n)[1:-1]:
    m.addConstr(xsum(x * 1 for x, e in zip(xs, es * (n - 2)) if e[0] == i) == 1)

status = m.optimize()

print(f"ObjectiveValue {m.objectiveValue}")

# get the variables
for var in m.vars:
    if var.x > 0:
        print(f"{var.name} id:{var.idx} = {var.x}")
