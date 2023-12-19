# 0-1 Knapsack problem
import flowty
import fetch_knapsack

name, n, c, P, W, z, x = fetch_knapsack.fetch("small", instance="knapPI_1_50_1000_1")

model = flowty.Model()
model.setParam("Algorithm", "MIP")

X = [model.addVar(lb=0, ub=1, obj=-P[i], type="B") for i in range(n)]

model.addConstr(flowty.xsum(w * x for w, x in zip(W, X)) <= c)

status = model.optimize()

if (
    status == flowty.OptimizationStatus.Optimal
    or status == flowty.OptimizationStatus.Feasible
):
    print(f"Cost: {model.objectiveValue}")
    # for var in model.solutions[0].vars:
    #    print(f" {var.name}")
