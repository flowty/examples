# 0-1 Knapsack problem
from flowty import Model, xsum
from or_datasets import pisinger

bunch = pisinger.fetch_knapsack("small", instance="knapPI_1_50_1000_1")
name, n, c, p, w, z, x = bunch["instance"]

m = Model()
m.setParam("Algorithm", "MIP")

for i in range(n):
    m.addVar(lb=0, ub=1, obj=-p[i], type="B")

m.addConstr(xsum(w[i] * v for i, v in enumerate(m.vars)) <= c)

status = m.optimize()
# print(f"ObjectiveValue {round(m.objectiveValue)} == {-z}")

# get the variable values
# for var in m.vars:
#     if var.x > 0:
#         print(f"{var.name} = {round(var.x, 1)}")
