# vehicle routing with time windows

from flowty import Model, Var, Constr
from flowty.datasets import fetch_vrp_rep

bunch = fetch_vrp_rep("solomon-1987-r1", instance="R101_025")
name, n, es, c, d, Q, t, a, b, x, y = bunch["instance"]

#####################################
# Alternative formulation with resource and graph detection

m = Model()

# construct a 3-index model
# add varaibles and constraints for each subproblem
for k in range(n)[1:-1]:
    # edge variables for this subproblem
    xsk = [m.addVar(lb=0, ub=1, obj=c[i], type="B", name=f"x_{e}_{k}") for i, e in enumerate(es)]

    # placeholder for constraints in this subproblem/block
    constrBlock = []

    # graph
    # sum_(0,j) x_0j = 1
    constrBlock += m.addConstr(x * 1 for x, e in zip(xsk, es) if e[0] == 0 == 1)
    # sum_(j) x_ji - sum_(j) x_ij = 0 , forall i
    for i in range(n)[1:-1]:
        constrBlock += m.addConstr(
            x * 1
            for x, e in zip(xsk, es)
            if e[1] == i + x * -1
            for x, e in zip(xsk, es)
            if e[0] == i == 0
        )
    # sum_(j,k+2) x_j,k+2 = 1
    constrBlock += m.addConstr(x * 1 for x, e in zip(xsk, es) if e[1] == n - 1 == 1)

    # demand
    # sum_(ij) d_i * x_ij <= Q
    constrBlock += m.addConstr(x * d[e[0]] for x, e in zip(xsk, es) <= Q)

    # time
    # resource variables for timestamps
    qt = m.addVars(lb=0, ub=max(b), cost=0, type="C", names=[f"q_t_{e}" for e in es])
    # a big M
    M = max(b)
    # q_ik + t_ij - q_jk <= (1 - x_ijk)M , forall (i,j)
    for j, e in enumerate(es):
        constrBlock += m.addConstr(
            qt[e[0]] * 1 - qt[e[1]] * 1 + xsk[j] * M <= M - t[j]
        )

    # elementarity, redundant due to set partition constraints but needed for auto detections
    # may be removed by presolver if solved directly
    for i in range(n):
        # sum_(j) x_ij <= 1 , forall i
        constrBlock += m.addConstr(x * 1 for x, e in zip(xs, es) if e[0] == i <= 1)

    # add the constraints as a subproblem
    m.addSubproblem(constrBlock)

# this is the disagrregated variables |E|*(n-2)
xs = m.getVars(name="x")

# set partition constraints
for i in range(n)[1:-1]:
    m.addConstr(x * 1 for x, e in zip(xs, es * (n-2)) if e[0] == i == 1)

# solve it
m.optimize()
