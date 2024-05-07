# Resource Constrained Multi Commodity Flow
import flowty
import fetch_rcmcf

# from
# https://github.com/flowty/LINERLIB
# https://github.com/flowty/flow-first-route-next-heuristic-shipping-network-design
# https://github.com/flowty/data/tree/main/data/linerlib
name, n, m, k, E, C, U, O, D, B, R, T = fetch_rcmcf.fetch("WorldLarge-All-5")

model = flowty.Model()
model.setParam("Pricer_MultiThreading", False)

# create subproblems
subproblems = []
for o, d, b, r in zip(O, D, B, R):
    graph = model.addGraph(edges=E, edgeCosts=C, resources=[("E", T, "G", r)])
    subproblems.append(
        model.addSubproblem(graph, source=o, target=d, obj=0, lb=0, ub=b, domain="C")
    )

# create penalty variables
penalty = sum(C) + 1
Y = [model.addVariable(obj=penalty, lb=0, ub=b, domain="C") for b in B]

# demand constraints
for y, s, b in zip(Y, subproblems, B):
    model += y + s >= b

# capacity constraints
lazy = True
maxCapacity = sum(B) + 1
for u, *edges in zip(U, *[s.graph.edges for s in subproblems]):
    if u < maxCapacity:
        model += flowty.sum(edges) <= u, lazy

status = model.solve()
solution = model.getSolution()
# if solution:
#     print(f"Cost {solution.cost}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
#     for var in solution.variables:
#         print(f"Penalty {var.variable.id}: {var.x}")
