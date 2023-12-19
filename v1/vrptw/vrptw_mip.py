# Vehicle Routing Problem with Time Windows
import flowty
import sys

sys.path.insert(1, "./v2/vrptw")
import fetch_vrptw

# from
# http://vrp.galgos.inf.puc-rio.br
# https://github.com/flowty/data/tree/main/data/vrptw
#
# C101...109, R101...112, RC101...108
# C201...208, R201...211, RC201...208
name, n, m, E, C, D, q, T, A, B, X, Y = fetch_vrptw.fetch("C101_25")

model = flowty.Model()
model.setParam("Algorithm", "MIP")

# placeholder for added variables
xs = []

# construct a 3-index model
# add variables and constraints for each subproblem
for k in range(n)[1:-1]:
    # edge variables for this subproblem
    xsk = [
        model.addVar(lb=0, ub=1, obj=C[i], type="B", name=f"x_({e[0]},{e[1]})_{k}")
        for i, e in enumerate(E)
    ]
    xFeasiblity = model.addVar(lb=0, ub=1, obj=0, type="B", name=f"x_({0},{n-1})_{k}")
    xs += xsk

    # graph, flow constraints
    # sum_(0,j) x_0j = 1
    expr = flowty.LinExpr()
    [expr.addTerm(1, x) for x, e in zip(xsk, E) if e[0] == 0]
    model.addConstr(expr + xFeasiblity == 1)

    # sum_(j) x_ji - sum_(j) x_ij = 0 , forall i
    for i in range(n)[1:-1]:
        expr = flowty.LinExpr()
        [expr.addTerm(1, x) for x, e in zip(xsk, E) if e[1] == i]
        [expr.addTerm(-1, x) for x, e in zip(xsk, E) if e[0] == i]
        model.addConstr(expr == 0)
        # sum_(j,n-1) x_j,n-1 = 1

    expr = flowty.LinExpr()
    [expr.addTerm(1, x) for x, e in zip(xsk, E) if e[1] == n - 1]
    model.addConstr(expr + xFeasiblity == 1)

    # capacity constraint
    # sum_(ij) d_i * x_ij <= Q
    model.addConstr(flowty.xsum(x * D[e[0]] for x, e in zip(xsk, E)) <= q)

    # time stamp per vertex
    qt = [
        model.addVar(lb=0, ub=max(B), obj=0, type="C", name=f"q_t_{i}_{k}")
        for i in range(n)
    ]

    # time winwos
    # q_ik + t_ij - q_jk <= (1 - x_ijk)M , forall (i,j)
    for j, e in enumerate(E):
        bigM = B[e[0]] + T[j]
        model.addConstr(qt[e[0]] * 1 - qt[e[1]] * 1 + xsk[j] * bigM <= bigM - T[j])
    # a_i sum_(j) x_ijk <= q_ik
    for i in range(n)[1:-1]:
        expr = flowty.LinExpr()
        [expr.addTerm(A[i], x) for x, e in zip(xsk, E) if e[0] == i]
        model.addConstr(expr - qt[i] <= 0)
    # q_ik <= b_i sum_(j) x_ijk
    for i in range(n)[1:-1]:
        expr = flowty.LinExpr()
        [expr.addTerm(-B[i], x) for x, e in zip(xsk, E) if e[0] == i]
        model.addConstr(expr + qt[i] <= 0)

# set partition constraints
for i in range(n)[1:-1]:
    expr = flowty.LinExpr()
    [expr.addTerm(1, x) for x, e in zip(xs, E * (n - 2)) if e[0] == i]
    model.addConstr(expr == 1)

status = model.optimize()

# get the variable values
if (
    status == flowty.OptimizationStatus.Optimal
    or status == flowty.OptimizationStatus.Feasible
):
    print(f"Cost: {model.objectiveValue}")
    # for var in model.solutions[0].vars:
    #     print(f" {var.name}")
