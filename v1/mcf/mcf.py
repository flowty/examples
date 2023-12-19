from flowty import Model, xsum, OptimizationStatus
import sys

sys.path.insert(1, "./v2/mcf")
import fetch_mcf

# from
# https://commalab.di.unipi.it/datasets/mmcf/#Plnr
# https://github.com/flowty/data/tree/main/data/mcf
#
# grid{i}, i in [1,...,15]
# planar{i}, i in [30, 50, 80, 100, 150, 300, 500, 800, 1000, 2500]
name, n, m, k, E, C, U, O, D, B = fetch_mcf.fetch("grid1")

model = Model()

# define graphs
graphs = []
for o, d, b in zip(O, D, B):
    g = model.addGraph(obj=C, edges=E, source=o, sink=d, L=b, U=b, type="C")
    model.addResourceDisposable(
        graph=g, consumptionType="V", weight=1, boundsType="V", lb=0, ub=n
    )
    graphs.append(g)

# demand constraints
for g, b in zip(graphs, B):
    model += xsum(x for x in g.vars if x.source == g.source) == b

# capacity constraints
for u, X in zip(U, zip(*[g.vars for g in graphs])):
    model += xsum(X) <= u

status = model.optimize()
if status != OptimizationStatus.Infeasible:
    print(f"ObjectiveValue {round(model.objectiveValue, 2)}")
