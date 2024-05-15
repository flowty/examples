# Multi Commodity Flow
import flowty
import fetch_mcf
import sys

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("Usage: python mcf.py instanceName [logFile] [timeLimit]")
    sys.exit(1)

# from
# https://commalab.di.unipi.it/datasets/mmcf/#Plnr
# https://github.com/flowty/data/releases/download/MCF
#
# grid{i}, i in [1,...,15]
# planar{i}, i in [30, 50, 80, 100, 150, 300, 500, 800, 1000, 2500]
instance = "planar500" if len(sys.argv) == 1 else sys.argv[1]
name, n, m, k, E, C, U, O, D, B = fetch_mcf.fetch(instance)

model = flowty.Model()
model.setParam("Pricer_MaxNumPricings", 1024 * 20)
model.setParam("Pricer_MaxNumCols", 1000 * 20)

# define graph
graph = model.addGraph(edges=E, edgeCosts=C)

# create subproblems
S = [
    model.addSubproblem(graph, source=o, target=d, obj=0, lb=0, ub=b, domain="C")
    for o, d, b in zip(O, D, B)
]

penalty = sum(C) + 1

# create penalty variables
Y = [model.addVariable(obj=penalty, lb=0, ub=b, domain="C") for b in B]

# demand constraints
for s, y, b in zip(S, Y, B):
    model += s + y >= b

# capacity constraints
lazy = True
for e, u in zip(graph.edges, U):
    model += e <= u, lazy

if len(sys.argv) > 2:
    model.setParam("LogFilepath", sys.argv[2])
if len(sys.argv) > 3:
    model.setParam("TimeLimit", int(sys.argv[3]))

status = model.solve()
solution = model.getSolution()
if solution:
    print(f"Cost {round(solution.cost,1)}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
#     for var in solution.variables:
#         print(f"Penalty {var.variable.id}: {var.x}")
