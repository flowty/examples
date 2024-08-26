# Vehicle Routing Problem with Time Windows
import flowty
import fetch_vrptw
import sys

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("Usage: python vrptw.py instanceName [logFile] [timeLimit]")
    sys.exit(1)

# from
# http://vrp.galgos.inf.puc-rio.br
# https://github.com/flowty/data/releases/tag/VRPTW
#
# C101...109, R101...112, RC101...108
# C201...208, R201...211, RC201...208
instance = "C101_25" if len(sys.argv) == 1 else sys.argv[1]
name, n, m, E, C, D, q, T, A, B, X, Y = fetch_vrptw.fetch(instance)

model = flowty.Model()
model.setParam("Master_Cut_UseSubsetRow", True)
model.setParam("PrimalHeu_DiveFrequency", 0)
model.setParam("MIPGap", 0)

# one graph with time and load resources, it is identical for all vehicles
time = {"E": [T], "V": [A, B]}, "time"
load = {"V": [D], "G": [q]}, "load"
timeRule = "Window", ["time"]
loadRule = "Capacity", ["load"]
rules = [timeRule, loadRule]

graph = model.addGraph(edges=E, edgeCosts=C, resources=[time, load], pathSense="S")
subproblem = model.addSubproblem(
    graph, source=0, target=n - 1, obj=0, lb=1, ub=n - 2, domain="B", rules=rules
)

# set partition constriants
for v in graph.vertices[1 : n - 1]:
    model += v == 1

if len(sys.argv) > 2:
    model.setParam("LogFilepath", sys.argv[2])
if len(sys.argv) > 3:
    model.setParam("TimeLimit", int(sys.argv[3]))

status = model.solve()
solution = model.getSolution()
if solution:
    print(f"Cost {round(solution.cost)}")
#     for path in solution.paths:
#         print(f"Path {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
