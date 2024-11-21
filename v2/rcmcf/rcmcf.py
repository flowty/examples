# Resource Constrained Multi Commodity Flow
import flowty
import fetch_rcmcf
import sys

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("Usage: python rcmcf.py instanceName [logFilepath] [timeLimit]")
    sys.exit(1)

# from
# https://github.com/flowty/LINERLIB
# https://github.com/flowty/flow-first-route-next-heuristic-shipping-network-design
# https://github.com/flowty/data/releases/tag/RCMCF
instance = "WorldLarge-All-5" if len(sys.argv) == 1 else sys.argv[1]
name, n, m, k, E, C, U, O, D, B, R, T = fetch_rcmcf.fetch(instance)

model = flowty.Model()
model.setParam("Pricer_MultiThreading", False)
model.setParam("Pricer_MaxNumCols", k)
model.setParam("Pricer_Algorithm", 2)
model.setParam("pricer_HeuristicLowFilter", 0)
model.setParam("pricer_HeuristicHighFilter", 0)

# create subproblems
subproblems = []
for o, d, b, r in zip(O, D, B, R):
    resource = {"E": [T], "G": [r]}, "time"
    resourceRule = "Capacity", ["load"]
    rules = [resourceRule]    
    graph = model.addGraph(edges=E, edgeCosts=C, resources=[resource])
    subproblems.append(
        model.addSubproblem(graph, source=o, target=d, obj=0, lb=0, ub=b, domain="C", rules=rules)
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

if len(sys.argv) > 2:
    model.setParam("LogFilepath", sys.argv[2])
if len(sys.argv) > 3:
    model.setParam("TimeLimit", int(sys.argv[3]))

status = model.solve()
solution = model.getSolution()
if solution:
    print(f"Cost {round(solution.cost, 1)}")
#     for path in solution.paths:
#         print(f"Commodity {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
#     for var in solution.variables:
#         print(f"Penalty {var.variable.id}: {var.x}")
