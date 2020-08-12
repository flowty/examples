from flowty import Model

p = [10, 13, 18, 31, 7, 15]
w = [11, 15, 20, 35, 10, 33]
c = 47

es = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
]

ps = [-x for x in p] + [0] * len(w) 
ws = w + [0] * len(w)

m = Model()
m.setParam("Algorithm", "DP")

g = m.addGraph(obj=ps, edges=es, source=0, sink=6, L=1, U=1, type="B")

m.addResourceDisposable(
    graph=g, consumptionType="E", weight=ws, boundsType="V", lb=0, ub=c
)

status = m.optimize()

print(f"ObjectiveValue {m.objectiveValue}")

# get the variables
xs = m.vars

for x in xs:
    if x.x > 0:
        print(f"{x.name} id:{x.idx} = {x.x}")
