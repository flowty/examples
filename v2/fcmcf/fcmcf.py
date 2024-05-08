# Fixed Charge Multi Commodity Flow
import flowty
import fetch_fcmcf

# From
# http://groups.di.unipi.it/optimize/Data/MMCF.html#Canad
# https://github.com/flowty/data/tree/main/data/fcmcf
name, n, m, k, E, C, U, F, O, D, B = fetch_fcmcf.fetch("c33")

model = flowty.Model()

# create subproblems
S = []
for o, d, b in zip(O, D, B):
    graph = model.addGraph(edges=E, edgeCosts=C)
    S.append(
        model.addSubproblem(graph, source=o, target=d, obj=0, lb=0, ub=b, domain="C")
    )

# create penalty variables
penalty = sum(C) + 1
Z = [model.addVariable(obj=penalty, lb=0, ub=b, domain="C") for b in B]

# fixed-charge variables
Y = [model.addVariable(obj=f, lb=0, ub=1, domain="B") for f in F]

# demand constraints
for s, b, z in zip(S, B, Z):
    model += s + z >= b

# capacity constraints
lazy = True
for u, *edges, y in zip(U, *[s.graph.edges for s in S], Y):
    model += flowty.sum(edges) <= u * y, lazy

# strong linking
lazy = True
for b, s in zip(B, S):
    for e, y in zip(s.graph.edges, Y):
        model += e <= b * y, lazy

status = model.solve()
solution = model.getSolution()
# if solution:
#     print(f"Cost {(solution.cost)}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
#     for var in solution.variables:
#         if var.variable.id < len(Z):
#             print(f"Penalty {var.variable.id}: {var.x}")
#         else:
#             print(f"Design {var.variable.id - len(Z)}: {var.x}")
