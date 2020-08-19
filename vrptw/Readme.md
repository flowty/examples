# Vehicle Routing Problem with Time Windows

This example illustrates a model for the vehicle routing problem with time windows (VRPTW).

In the VRPTW the objective is to minimize the total cost of routing vehicles from a central depot to a set of customers. Each customer must be visited exactly once within a specified time window to deliver their required demand, each customer has a service time it takes to unload the vehicle, and each vehicle has a maximum capacity of goods to deliver. If a vehicle arrives early it is allowed to wait for the customer's time window to start.

## Notation

Let *G(V,E)* be a directed graph with nodes *V* (customers *C* plus depot node split in two 0 and *n+1*) and edges *E*. Let *c* and *t* be cost and travel time, respectively for each edge and let *d, s, a,* and *b*, be the customer demand, service time, and time window start and end values. *Q* is the capacity of the vehicles.

A solution can be depicted as

![Graph](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgMSAtLT4gMlxuICAyIC0tPiAwWzAvbisxXVxuICAwIC0tPiAxXG4gIDAgLS0+IDNcbiAgMyAtLT4gNFxuICA0IC0tPiAwXG4gIDAgLS0+IDVcbiAgNSAtLT4gNlxuICA2IC0tPiAwXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ==)

<!-- ```mermaid
graph LR
  1 -#-> 2
  2 -#-> 0[0/n+1]
  0 -#-> 1
  0 -#-> 3
  3 -#-> 4
  4 -#-> 0
  0 -#-> 5
  5 -#-> 6
  6 -#-> 0
``` -->

where 0 and *n+1* is the (split) depot node. Each node has associated the  attributes *[a,b], s*, and  *d*, that is, time windows bounds, service time and demand respectively. The edges have cost *c* and travel time *t* attributes attached to them.

## An Edge Formulation

Let *K* be an upper bound on number of vehicles available, in worst case it is equal to the number of customers.

A compact mathematical formulation of the VRPTW is:

![Edge formulation](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%5Cmin%20%26%20%5Csum_%7Bk%20%5Cin%20K%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20E%7D%20c_%7Bij%7D%20x_%7Bijk%7D%20%26%20%26%20%26%20%281%29%20%5C%5C%20%5Ctext%7Bsubject%20to%7D%20%26%20%5Csum_%7Bk%20%5Cin%20K%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7Bi%7D%7D%20x_%7Bijk%7D%20%3D%201%20%26%20%5Cforall%20i%20%5Cin%20C%20%26%20%26%20%282%29%20%5C%5C%20%26%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7B0%7D%7D%20x_%7B0jk%7D%20%3D%201%20%26%5Cforall%20k%20%5Cin%20K%20%26%20%26%20%283%29%5C%5C%20%26%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7Bi%7D%7D%20x_%7Bijk%7D%20-%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E-%7Bi%7D%7D%20x_%7Bijk%7D%20%3D%200%20%26%20%5Cforall%20k%20%5Cin%20K%2C%20%5Cforall%20i%20%5Cin%20C%20%26%20%26%20%284%29%5C%5C%20%26%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7Bn&plus;1%7D%7D%20x_%7Bi%2Cn&plus;1%2Ck%7D%20%3D%201%20%26%5Cforall%20k%20%5Cin%20K%20%26%20%26%20%285%29%5C%5C%20%26%20q_%7Bik%7D%20&plus;%20s_i%20&plus;%20t_%7Bij%7D%20-%20q_%7Bjk%7D%20%5Cleq%20%281%20-%20x_%7Bijk%7D%29%20M_%7Bik%7D%20%26%20%5Cforall%20k%20%5Cin%20K%2C%20%5Cforall%20%28i%2Cj%29%20%5Cin%20E%20%26%20%26%20%286%29%5C%5C%20%26%20a_i%20%5Cleq%20q_%7Bik%7D%20%5Cleq%20b_i%20%26%20%5Cforall%20k%20%5Cin%20K%2C%20%5Cforall%20%28i%2Cj%29%20%5Cin%20E%20%26%20%26%20%287%29%20%5C%5C%20%26%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20E%7D%20d_i%20x_%7Bijk%7D%20%5Cleq%20Q%20%26%20%5Cforall%20k%20%5Cin%20K%20%26%20%26%20%288%29%20%5C%5C%20%26%20x_%7Bijk%7D%20%5Cin%20%5Cmathbb%7BB%7D%20%26%20%5Cforall%20%28i%2Cj%29%20%5Cin%20E%2C%20k%20%5Cin%20K%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
\min & \sum_{k \in K} \sum_{(i,j) \in E} c_{ij} x_{ijk} & & & (1) \\
\text{subject to} & \sum_{k \in K} \sum_{(i,j) \in \delta^+{i}} x_{ijk} = 1 & \forall i \in C & & (2) \\
& \sum_{(i,j) \in \delta^+{0}} x_{0jk} = 1 &\forall k \in K & & (3)\\
& \sum_{(i,j) \in \delta^+{i}} x_{ijk} - \sum_{(i,j) \in \delta^-{i}} x_{ijk} = 0  & \forall k \in K, \forall i \in C & & (4)\\
& \sum_{(i,j) \in \delta^+{n+1}} x_{i,n+1,k} = 1 &\forall k \in K & & (5)\\
& q_{ik} + s_i + t_{ij} - q_{jk} \leq (1 - x_{ijk}) M_{ik} & \forall k \in K, \forall (i,j) \in E & & (6)\\
& a_i \leq q_{ik} \leq b_i & \forall k \in K, \forall (i,j) \in E & & (7) \\
& \sum_{(i,j) \in E} d_i x_{ijk} \leq Q & \forall k \in K & & (8) \\
& x_{ijk} \in \mathbb{B} & \forall (i,j) \in E, k \in K
\end{aligned}
``` -->

where the *x*'s are binary variables indicating if the *k*th vehicle travels from customer *i* to *j* and *M* is a sufficiently big constant. The objective (1) minimizes travel cost, constraints (2) ensures that customers are visited exactly once, (3)-(5) ensures that all routes start and end in the depot an that flow conservation is preserved, (6)-(7) are the time window constraints, and (8) are the capacity constraints. The solution provides a path (or not) for each *K* vehicles from 0 to *n+1*.

The model has a high degree of symmetry since all *K* vehicles are identical and  the time windows constraints using the big-*M* notations is notoriously bad for performance. The model can be solved by conventional mixed integer programming solvers but quickly becomes intractable.

## A Path Formulation

Historically path formulations have performed much better. Using Dantzig-Wolfe decomposition on the above and aggregating the K identical vehicles one arrives at a path-based formulation

![Path formulation](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%5Cmin%20%26%20%5Csum_%7Bp%20%5Cin%20P%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20E%7D%20c_%7Bij%7D%20%5Calpha_%7Bij%7D%5Ep%20%5Clambda_p%20%26%20%26%20%26%20%289%29%20%5C%5C%20%5Ctext%7Bsubject%20to%7D%20%26%20%5Csum_%7Bp%20%5Cin%20P%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7Bi%7D%7D%20%5Calpha_%7Bij%7D%5Ep%20%5Clambda_p%20%3D%201%20%26%20%5Cforall%20i%20%5Cin%20C%20%26%20%26%20%2810%29%20%5C%5C%20%26%20%5Clambda_p%20%5Cin%20%5Cmathbb%7BB%7D%20%26%20%5Cforall%20p%20%5Cin%20P%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
\min & \sum_{p \in P} \sum_{(i,j) \in E} c_{ij} \alpha_{ij}^p \lambda_p & & & (9) \\
\text{subject to} & \sum_{p \in P} \sum_{(i,j) \in \delta^+{i}} \alpha_{ij}^p \lambda_p = 1 & \forall i \in C & & (10) \\
& \lambda_p \in \mathbb{B} & \forall p \in P
\end{aligned}
``` -->

where *P* is the set of feasible paths a vehicle can use, lambda variables indicates if a path is used or not, and the alpha constant indicates if the edge from *i* to *j* is used on path *p*. As before the the objective (9) is to minimize total travel cost and constraints (10) ensures that customers are visited exactly once. The constraints correspond to (2) in the edge formulation and are also referred to as linking constraints - since they link paths together.

The path-based model is solved using column generation based approaches where paths (columns in the model matrix) are constructed on-the-fly and when needed. To construct paths one needs to solve a subproblem that is a variant of the shortest path problem, but with negative cost cycles and time window and capacity constraints on the path.

The subproblem is generally referred to as a resource constrained shortest path problem (RCSPP) where resources *R* are some quantity *q* accumulated along the path subject to bound constraints *[l, u]* at each node. For instances, travel time *t* and service time s accumulates for each traversed edge and customer serviced and must obey the time window *[a,b]* at each customer. Similarly, the demand *d* is accumulated for at each customer and must be with the vehicle capacity *[0,Q]* for at each step.

## Using Flowty's Solver

The path-based formulation is not readily solved with a standard mixed integer solver but can be solved with Flowty. Under the hood Flowty solves the path formulation and automatically adds paths by solving the RCSPP subproblem.

One needs to deliver 

- a graph formulation of the subproblems, here a single one *G* (as a path problem),
- a formulation given in edges including only the constraints that are relevant for linking paths together, in this case the objective (1) and constraints (2),
- lower and upper bounds on the number of paths allowed from each subproblem,
- and a mapping between *x* variables and edges in graph, in this case it is a 1:1 mapping.

### Graph

Hence, we have a graph

![Graph](https://latex.codecogs.com/png.latex?G%28V%2CE%29%2C%20V%20%3D%20%5C%7B0%2C1%2C...%2C%7CC%7C%2Cn&plus;1%5C%7D%2C%20v_%7Bsource%7D%20%3D0%2C%20v_%7Btarget%7D%3Dn&plus;1)

<!-- ```math
    G(V,E), V = \{0,1,...,|C|,n+1\}, v_{source}  =0, v_{target}=n+1
``` -->

in which to find a resource constrained shortest path from *0* to *n+1*. The resources *R* are given as time *t*, demand *d*, and a set of binary resource *v*, on for each customer such that

![Resources](https://latex.codecogs.com/png.latex?R%20%3D%20%5C%7B%20t%2C%20d%2C%20v%2C%20%5Cforall%20v%20%5Cin%20C%5C%7D)

<!-- ```math
  R = \{ t, d, v, \forall v \in C\}
``` -->

the consumption *q* for each resource is given as

![Resource accumulation](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%26q_%7Btij%7D%20%3D%20t_%7Bij%7D%20&plus;%20s_i%20%26%20%5Cforall%20%28i%2Cj%29%20%5Cin%20E%5C%5C%20%26q_%7Bdi%7D%20%3D%20d_j%20%26%20%5Cforall%20i%20%5Cin%20V%5C%5C%20%26q_%7Bvi%7D%20%3D%201%20%5Ctext%7B%20iff%20%7D%20v%20%3D%20i%20%26%20%5Cforall%20i%2Cv%20%5Cin%20V%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
    &q_{tij} = t_{ij} + s_i & \forall (i,j) \in E\\
    &q_{di} = d_j & \forall i \in V\\
    &q_{vi} = 1 \text{ iff } v = i & \forall i,v \in V
\end{aligned}
``` -->

and 0 otherwise. The resource bounds are

![Resource bounds](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%26%5Bl_%7Bti%7D%2Cu_%7Bti%7D%5D%20%3D%20%5Ba_i%2C%20b_i%5D%20%26%20%5Cforall%20i%20%5Cin%20V%20%5C%5C%20%26%5Bl_%7Bdi%7D%2Cu_%7Bdi%7D%5D%20%3D%20%5B0%2C%20Q%5D%20%26%20%5Cforall%20i%20%5Cin%20V%20%5C%5C%20%26%5Bl_%7Bvi%7D%2Cu_%7Bvi%7D%5D%20%3D%20%5B0%2C%201%5D%20%26%20%5Cforall%20i%2Cv%20%5Cin%20V%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
    &[l_{ti},u_{ti}] = [a_i, b_i] & \forall i \in V \\
    &[l_{di},u_{di}] = [0, Q] & \forall i \in V \\
    &[l_{vi},u_{vi}] = [0, 1] & \forall i,v \in V
\end{aligned}
``` -->

### Formulation

The path-based model expressed in edges

![Formulation](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%5Cmin%20%26%20%5Csum_%7Bk%20%5Cin%20K%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20E%7D%20c_%7Bij%7D%20x_%7Bijk%7D%20%26%20%26%20%26%20%281%29%20%5C%5C%20%5Ctext%7Bsubject%20to%7D%20%26%20%5Csum_%7Bk%20%5Cin%20K%7D%20%5Csum_%7B%28i%2Cj%29%20%5Cin%20%5Cdelta%5E&plus;%7Bi%7D%7D%20x_%7Bijk%7D%20%3D%201%20%26%20%5Cforall%20i%20%5Cin%20C%20%26%20%26%20%282%29%20%5C%5C%20%26%20x_%7Bijk%7D%20%5Cin%20%5Cmathbb%7BB%7D%20%26%20%5Cforall%20%28i%2Cj%29%20%5Cin%20E%2C%20k%20%5Cin%20K%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
\min & \sum_{k \in K} \sum_{(i,j) \in E} c_{ij} x_{ijk} & & & (1) \\
\text{subject to} & \sum_{k \in K} \sum_{(i,j) \in \delta^+{i}} x_{ijk} = 1 & \forall i \in C & & (2) \\
& x_{ijk} \in \mathbb{B} & \forall (i,j) \in E, k \in K
\end{aligned}
``` -->

The constraints (3)-(8) from the edge formulation are represented in the subproblem and are enforced as resource constraints on the path as defined in the graph described above.

Together with the mapping and the bounds described below, the formulation holds information to automatically decompose the model into a path formulation that is more tractable. Note, that the formulation alone is not valid for solving the VRPTW.

### Bounds

Define the bounds on the number of paths allowed to be used as

![Bounds](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%26%20L%20%3D%20%5Cbigg%20%5Clceil%20%5Csum_%7Bi%20%5Cin%20C%7D%20d_i%20/%20Q%20%5Cbigg%20%5Crceil%20%5C%5C%20%26%20U%20%3D%20%7CC%7C%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
 & L = \bigg \lceil \sum_{i \in C} d_i / Q \bigg \rceil \\
 & U = |C|
\end{aligned}
``` -->

The lower bound is bin packing lower bound given as the sum of all demand divided by the vehicle capacity ceiled to nearest integer, and the upper bound is to consider one vehicle per customer.

### Mapping

This is where the magic happens between the *x* variables and the subproblem graph. The 1:1 mapping between *x*'s and edges is

![Mapping](https://latex.codecogs.com/png.latex?%5Cbegin%7Baligned%7D%20%26%20M%28x_%7Bij%7D%29%20%3D%20%5C%7B%20%28i%2Cj%29%20%5C%7D%2C%20%26%20%28i%2Cj%29%20%5Cin%20E%20%5Cend%7Baligned%7D)

<!-- ```math
\begin{aligned}
 & M(x_{ij}) = \{ (i,j) \}, & (i,j) \in E
\end{aligned}
``` -->

An interpretation of this relationship is, that if a path uses an edge then the path contributes (have a coefficient) to any linking constraints given in the formulation where the mapped *x* variable appears. For VRPTW it is the mapping that defines the value of the *alpha* coefficient when translating the path into a variable in the path formulation (9)-(10).

Feed everything to the solver and solve. See the python code example below.