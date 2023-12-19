# 0-1 Knapsack problem
import flowty
import fetch_knapsack

name, n, c, P, W, z, x = fetch_knapsack.fetch("small", instance="knapPI_1_50_1000_1")

# Construct multi-graph
E = [(i, i + 1) for i in range(n)] + [(i, i + 1) for i in range(n)]

# zero profit and weight for 'pick not' edges
# signs are flipped for maximization
P = [-p for p in P] + [0] * len(W)
W = W + [0] * len(W)

model = flowty.Model()
model.setParam("Algorithm", "DP")

g = model.addGraph(obj=P, edges=E, source=0, sink=n, L=1, U=1, type="B")

model.addResourceDisposable(
    graph=g, consumptionType="E", weight=W, boundsType="V", lb=0, ub=c
)

status = model.optimize()

if (
    status == flowty.OptimizationStatus.Optimal
    or status == flowty.OptimizationStatus.Feasible
):
    print(f"Cost: {model.objectiveValue}")
    # for path in model.solutions[0].paths:
    #     print(f"Path {path.idx}")
    #     for var in path.vars:
    #         print(f" {var.name}")
