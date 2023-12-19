import flowty
from typing import List, Tuple

## Build Model

# data
C: List[int] = [2, 2, 3, 1, 3, 1]
E: List[Tuple[int, int]] = [(0, 1), (0, 2), (1, 2), (2, 1), (1, 3), (2, 3)]
U: List[float] = [3, 6, 2, 2, 3, 4]
b: float = 6
T: List[int] = [1, 7, 6, 5, 3, 2]
q: int = 10

# create model
model = flowty.Model()

# create a maximum transit time constraint constraint
time = "E", T, "G", 0, q

# create a resource constrained graph
graph = model.addGraph(costs=C, edges=E, resources=[time])

# add a subproblem using the graph with source and target vertices. Enforce integer flows
s = model.addSubproblem(graph=graph, source=0, target=3, obj=0, lb=1, ub=b, domain="I")

# add a penalty variable for uncovered flow
penalty = sum(C) + 1
y = model.addVariable(obj=penalty, lb=0, ub=b, domain="C")

# add demand constraint
model += y + s >= b

# add edge capacity constraints
for e, u in zip(s.graph.edges, U):
    model += e <= u

# solve the model
status = model.solve()
if status:
    # get the best solution
    solution = model.getSolution()
    if solution:
        # get the solution cost
        obj = solution.cost


## Get Solution

# get the best solution, returns None if no solution
best = model.getSolution()

### Multiple Solutions

# get number of solutions
num = model.getNumSolutions()

# get the n'th solution, n = 0 is the best solution
n = 1
nSolution = model.getSolution(n)

# get all solutions
solutions = model.getSolutions()

### Get Paths

# get paths in the solution
paths = solution.paths

# loop the paths and extract info
for path in paths:
    # solution value
    x = path.x
    # the subproblem the path belongs to
    subproblem = path.subproblem
    # get the edges on the path
    edges = path.edges
    for edge in edges:
        edgeId = edge.id
        # edge source and target
        source = edge.source
        target = edge.target

### Get Variables

# get non-zero variables in the solution
variables = solution.variables

# loop the variables and extract info
for var in variables:
    # underlying variable
    variable = var.variable
    # solution value
    x = var.x

### Consumption and Bounds Types

resource: Tuple[
    flowty.Resource.ConsumptionType | str,
    List[int],
    flowty.Resource.BoundsType | str,
    int | List[int],
    int | List[int],
]
# The resource components
consumptionType: flowty.Resource.ConsumptionType | str
consumptionValues: List[int]
boundsType: flowty.Resource.BoundsType | str
lowerBounds: int | List[int]
upperBounds: int | List[int]

# consumption types
edgeConsumption = flowty.Resource.ConsumptionType.Edge
edgeConsumption = "E"
vertexConsumption = flowty.Resource.ConsumptionType.Vertex
vertexConsumption = "V"

# bound types
edgeBounds = flowty.Resource.BoundsType.Edge
edgeBounds = "E"
vertexBounds = flowty.Resource.BoundsType.Vertex
vertexBounds = "V"
globalBounds = flowty.Resource.BoundsType.Global
globalBounds = "G"


### Create Resources

# time window resource
T: List[int] = [1, 3, 4, 2]  # length |E|
A: List[int] = [0, 1, 1]  # length |V|
B: List[int] = [0, 4, 5]  # length |V|
time = "E", T, "V", A, B

# capacity resource
D: List[int] = [2, 2, 3]  # length |V|
a: int = 0
b: int = 4
capacity = "V", D, "G", a, b


### Add Graphs

# graph with no resource constraints
C: List[float] = [1, 3, 2, 5]  # length |E|
E: List[Tuple[int, int]] = [(0, 1), (0, 2), (2, 1), (2, 1)]
noResourceGraph = model.addGraph(costs=C, edges=E)

# graphs with resource constraints
oneResourceGraph = model.addGraph(costs=C, edges=E, resources=[time])
twoResourceGraph = model.addGraph(costs=C, edges=E, resources=[time, capacity])

# get graphs
graphs = model.graphs

# get graph properties
graphId = graph.id
costs = graph.costs
vertices = graph.vertices
edges = graph.edges
resources = graph.resources

## Add Subproblems

graph: flowty.Graph = model.addGraph(costs=C, edges=E)
source: int = 0
target: int = 2
obj: float = 0
lb: float = 1  # >= 0
ub: float = 1
domain: flowty.Variable.Domain | str = "C"
subproblem = model.addSubproblem(graph, source, obj, target, lb, ub, domain)

# get subproblems
subproblems = model.subproblems

# get subproblem properties
subproblemId = subproblem.id
source = subproblem.source
target = subproblem.target

### Domains

continousType = flowty.Variable.Domain.Continuous
continousType = "C"
integerType = flowty.Variable.Domain.Integer
integerType = "I"
binaryType = flowty.Variable.Domain.Binary
binaryType = "B"


## Add Variables

obj: float = 1  # default to 0
lb: float = 0  # default to -inf
ub: float = float("inf")  # default to inf
variable = model.addVariable(obj, lb, ub, domain)

# get model variables
variables = model.variables

## Add Constraints

x = model.addVariable(obj, lb, ub, domain)
y = model.addVariable(obj, lb, ub, domain)
terms: List[
    Tuple[float, flowty.Subproblem | flowty.Vertex | flowty.Edge | flowty.Variable]
] = [(1, x), (2, y)]
rhs: float = 1
sense: flowty.Constraint.Sense = flowty.Constraint.Sense.GreaterEqual
model.addConstraint(terms, sense, rhs)


senseLEQ = flowty.Constraint.Sense.LessEqual
senseE = flowty.Constraint.Sense.Equal
senseGEQ = flowty.Constraint.Sense.GreaterEqual


### Shorthand Notation

model += 2 * x - y + 5 <= 4
model += 2 * x - y + 5 == 4
model += 2 * x - y + 5 >= 4

constant: float = 10
model += flowty.sum(terms) + constant <= rhs

# mixing
model += flowty.sum(terms) + constant + 2 * x - y + 5 <= rhs


### Lazy Constraints

lazy: bool = True
model += flowty.sum(terms) + constant <= rhs, lazy
model.addConstraint(terms, sense, rhs, lazy)


### Modelling with Subproblems, Vertices and Edges

s: flowty.Subproblem = subproblem
v: flowty.Vertex = graph.vertices[0]
e: flowty.Edge = graph.edges[0]
coef: float = 1
model += coef * s + coef * v + coef * e <= rhs

# vertices and edges are accesed through added graphs
vertices = graph.vertices
edges = graph.edges

# set partitioning constraints
for v in vertices:
    model += v == 1

# edge capacities
U: List[float]  # length |E|
for e, u in zip(edges, U):
    model += e <= u

# sum on edges
model += flowty.sum(2 * e for e in graph.edges) == 1

# sum on outgoing edges
vertex = graph.vertices[0]
model += flowty.sum(2 * e for e in graph.edges if e.source == vertex.id) == 1


## Share Graphs In Subproblems

s1 = model.addSubproblem(graph, source=0, target=1, obj=0, lb=0, ub=1, domain="C")
s2 = model.addSubproblem(graph, source=2, target=0, obj=1, lb=1, ub=2, domain="I")

graph2 = model.addGraph(costs=C, edges=E)
s3 = model.addSubproblem(graph2, source=2, target=0, obj=1, lb=1, ub=2, domain="I")

# edge capacities for two graphs in different subproblems
for e1, e2, u in zip(graph.edges, graph2.edges, U):
    model += e1 + e2 <= u

# edge capacities for one graph in different subproblems
for e, u in zip(graph.edges, U):
    model += e <= u

## Visualization

import networkx
import matplotlib.pyplot as plt

# the graph
graph = model.graphs[0]

# get best solution
solution = model.getSolution()

# get the first path
path = solution.paths[0]

edges = [(e.source, e.target) for e in path.edges]
gx = networkx.DiGraph()
gx.add_nodes_from([v.id for v in graph.vertices])
gx.add_edges_from(edges)
# pos = {i: (x[i], y[i]) for i in range(n)} # for lists of x,y coordinates
pos = networkx.spring_layout(gx)  # alternative layout
networkx.draw_networkx_nodes(gx, pos, nodelist=gx.nodes)
networkx.draw_networkx_labels(gx, pos, labels={i: i for i in gx.nodes})
networkx.draw_networkx_edges(gx, pos, nodelist=gx.edges)
# plt.show() # if gui backend is supported
plt.savefig("mypath.png")
