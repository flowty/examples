# Multi Commodity Flow
import flowty
import fetch_mcf

# from
# https://commalab.di.unipi.it/datasets/mmcf/#Plnr
# https://github.com/flowty/data/tree/main/data/mcf
#
# grid{i}, i in [1,...,15]
# planar{i}, i in [30, 50, 80, 100, 150, 300, 500, 800, 1000, 2500]
name, n, m, k, E, C, U, O, D, B = fetch_mcf.fetch("planar500")

model = flowty.Model()
model.setParam("Pricer_MaxNumPricings", 1024 * 20)
model.setParam("Pricer_MaxNumVars", 1000 * 20)

# define graph
graph = model.addGraph(costs=C, edges=E)

penalty = sum(C) + 1
constant = sum(B) * penalty

# create subproblems
subproblems = [
    model.addSubproblem(graph, source=o, target=d, obj=-penalty, lb=0, ub=b, domain="C")
    for o, d, b in zip(O, D, B)
]

# demand constraints
for s, b in zip(subproblems, B):
    model += s <= b

# capacity constraints
lazy = True
for e, u in zip(graph.edges, U):
    model += e <= u, lazy

status = model.solve()
solution = model.getSolution()
if solution:
    print(f"Cost {(constant + solution.cost)}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
