# Vehicle Routing Problem with Time Windows

The vehicle routing problem with time windows is to service a set of customers from a central depot. The customers demand must be meet and they are visited exactly once within their time window. The fleet of identical vehicles have a capacity. The objective is to minimise overall travel cost. For convenience the depot can be split into a start and end depot. 

Let $G(V, E)$ be a graph where $C \subset V$ is the set of customers and $\{v_0, v_{|C|+1} \} \in V$ is the start and end depot. There is an ede cost $c_{e}$ for traversing edge $e$. $P$ are feasible paths in  $G$ from the start depot to the end depot such that the capacity and time windows constraints on the path are OK. $\alpha_{e}^p$ is 1 if edge $e$ is on path $p$ and 0 otherwise. This is equivalent for $\alpha_v^p$ for vertex $v$.

The set partitioning formulation is

```math
\begin{aligned}
\min{ } & \sum_{p \in P} \sum_{e \in E} \alpha_{e}^p c_{e} \lambda_p \\
\text{s.t. } & \sum_{p \in P} \alpha_{v}^p \lambda_p = 1 && v \in C \\
& 1 \leq \sum_{p \in P} \lambda_p \leq |C| \\
& \lambda_p \in \{0,1\} && p \in P
\end{aligned}
```

where $\lambda_p$ indicates if path $p$ is used.

> **Modelling with edges and vertices**
> Flowty supports modelling with edges $e \in E$ and vertices $v \in V$ for graphs $G(V,E)$. When adding a graph to a subproblem in flowty it is automatically transformed into variables $x_e$ for $e \in E$ and $x_v$ for $i \in V$ respectively. 

Using an edge and vertex modelling approach we get

```math
\begin{aligned}
\min{ } & \sum_{e \in E} c_{e} x_{e} \\
\text{s.t. } & x_v = 1 && v \in C \\
& x_{e} \in \{0, 1\} && e \in E \\
& x_v \in \{0, 1\} && v \in C
\end{aligned}
```

with $G(V,E)$ and resource constraints given as the capacity and time window constraints. Note that vehicle routing problem only have one subproblem but allows multiple routes. Because the subproblems per vehicle are collapsed into one because they are identical. 

Goto [code](vrptw.py).