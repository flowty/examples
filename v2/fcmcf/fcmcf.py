# Fixed Charge Multi Commodity Flow
import flowty
import fetch_fcmcf
import sys

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("Usage: python fcmcf.py instanceName [logFile] [timeLimit]")
    sys.exit(1)

# From
# http://groups.di.unipi.it/optimize/Data/MMCF.html#Canad
# https://github.com/flowty/data/releases/tag/FCMCF
instance = "c33" if len(sys.argv) == 1 else sys.argv[1]
name, n, m, k, E, C, U, F, O, D, B = fetch_fcmcf.fetch(instance)

model = flowty.Model()
model.setParam("Pricer_MaxNumCols", k)
model.setParam("MIPGap", 0)

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
for u, *edges, y in zip(U, *[s.graph.edges for s in S], Y):
    model += flowty.sum(edges) <= u * y

# strong linking
lazy = True
for b, s in zip(B, S):
    for e, y in zip(s.graph.edges, Y):
        model += e <= b * y, lazy

if len(sys.argv) > 2:
    model.setParam("LogFilepath", sys.argv[2])
if len(sys.argv) > 3:
    model.setParam("TimeLimit", int(sys.argv[3]))

status = model.solve()
solution = model.getSolution()
if solution:
    print(f"Cost {round(solution.cost)}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
#     for var in solution.variables:
#         if var.variable.id < len(Z):
#             print(f"Penalty {var.variable.id}: {var.x}")
#         else:
#             print(f"Design {var.variable.id - len(Z)}: {var.x}")
