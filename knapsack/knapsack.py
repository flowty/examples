# 0-1 knapsack problem

from flowty import Model, xsum
from flowty.constants import IntParam

p = [10, 13, 18, 31, 7, 15]
w = [11, 15, 20, 35, 10, 33]
c, I = 47, range(len(w))

es = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (0, 7),
    (1, 8),
    (2, 9),
    (3, 10),
    (4, 11),
    (5, 12),
    (7, 1),
    (8, 2),
    (9, 3),
    (10, 4),
    (11, 5),
    (12, 6),
]
ps = [-x for x in p] + [0] * len(w) * 2
ws = w + [0] * len(w) * 2

# es = [(0,1), (1,2), (2,3), (3,4), (4,5), (5, 6),
#  (0,1), (1,2), (2,3), (3,4), (4,5), (5,6)
#  ]
# ps = [-x for x in p] + [0] * len(w)
# ws = w + [0] * len(w)

m = Model()

m.setParam(IntParam.Algorithm, 4)

# one graph, it is identical for all vehicles.
# creates variables per edge and constraints for a single from source to sink
# for U > 1, the parameter specifies that there are identical subproblems
g = m.addGraph(directed=True, obj=ps, edges=es, source=0, sink=6, L=1, U=1, type="B")

m.addResourceDisposible(
    graph=g, consumptionType="E", weight=ws, boundsType="V", lb=0, ub=c, obj=0
)

# m.write("dump.lp")

status = m.optimize()

# get the variables
xs = m.vars

for x in xs:
    if x.x > 0:
        print(f"{x.name} id:{x.idx} = {x.x}")
