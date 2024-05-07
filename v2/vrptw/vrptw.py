# Vehicle Routing Problem with Time Windows
import flowty
import fetch_vrptw

# from
# http://vrp.galgos.inf.puc-rio.br
# https://github.com/flowty/data/tree/main/data/vrptw
#
# C101...109, R101...112, RC101...108
# C201...208, R201...211, RC201...208
name, n, m, E, C, D, q, T, A, B, X, Y = fetch_vrptw.fetch("C101_100")

model = flowty.Model()
model.setParam("Master_Cut_UseSubsetRow", True)

# one graph with time and load resources, it is identical for all vehicles
time = "E", T, "V", A, B
capacity = "V", D, "G", q
graph = model.addGraph(costs=C, edges=E, resources=[time, capacity], pathSense="S")
subproblem = model.addSubproblem(
    graph, source=0, target=n - 1, obj=0, lb=1, ub=n - 2, domain="B"
)

# set partition constriants
for v in graph.vertices[1 : n - 1]:
    model += v == 1

status = model.solve()
solution = model.getSolution()
# if solution:
#     print(f"Cost {solution.cost}")
#     for path in solution.paths:
#         print(f"Path {path.subproblem.id}: {path.x}")
#         for edge in path.edges:
#             print(f"{edge}")
