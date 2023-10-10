# 0-1 Knapsack problem
import flowty
import fetch_knapsack

name, n, c, P, W, z, x = fetch_knapsack.fetch("small", instance="knapPI_1_50_1000_1")

m = flowty.Model()
m.setParam("Algorithm", "MIP")

X = [m.addVar(lb=0, ub=1, obj=-P[i], type="B") for i in range(n)]

m.addConstr(flowty.xsum(w * x for w, x in zip(W, X)) <= c)

status = m.optimize()

# get the variable values
#
# if (
#     status == flowty.OptimizationStatus.Optimal
#     or status == flowty.OptimizationStatus.Feasible
# ):
#     for var in model.solutions[0].vars:
#        print(f" {var.name}")
