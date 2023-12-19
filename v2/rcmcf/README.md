# Resource Constrained Multi Commodity Flow Problem

In the resource constrained multi commodity flow problem graphs $G_k(V_k,E_k)$ are given for commodities $k \in K$ that each have an origin $o_k \in V$ and destination vertex $d_k \in V$. Each commodity have a demand $B_k$ and each edge $e \in \cup_{k \in K} E_k$ have a capacity $u_e$. $P_k$ is the set of paths for commodity $k$ from origin to destination such that the resource constraints is not violated. The resource constraint enforces a capacity constraint on the max transit time per commodity.  $\alpha_e^p$ is 1 is edge $e$ is on oath $p$ otherwise 0.

The path formulation is

```math
\begin{aligned}
\min{ } & \sum_{k \in K} \sum_{p \in P_k} \sum_{(i,j) \in E} \alpha_e c_e \lambda_p \\
\text{s.t. } & \sum_{p \in P_k} \lambda_p = B_k && k \in K \\
& \sum_{k \in K} \sum_{p \in P_k} \alpha_e^p \lambda_p \leq u_e && e \in \cup_{k \in K} E_k \\
& \lambda_p \geq 0 && k \in K, p \in P_k
\end{aligned}
```

where $\lambda_p$ for $p \in P_k$ indicates how much of commodity $k$ flows on $p$. 

> **Modelling with edges and vertices**
> Flowty supports modelling with edges $e \in E$ and vertices $v \in V$ for graphs $G(V,E)$. When adding a graph to a subproblem to the model it is automatically transformed into variables $x_e$ for $e \in E$ and $x_v$ for $v \in V$ respectively.

> **Modelling with subproblems**
> Flowty supports modelling with subproblems $s \in S$. When adding a subproblem to the model one can model using $x_s \in S$.

Each commodity give rise to a subproblem. Let $\beta_e^k$ be 1 if $e \in E_k$ and 0 otherwise.

```math
\begin{aligned}
\min{ } & \sum_{k \in K} \sum_{e \in E_k} c_e x_e + \sum_{k \in K} P_k y_k \\
\text{s.t. } & y_k + s_k \geq B_k && k \in K \\
& \sum_{k \in K} \beta_e^k x_e \leq u_e && e \in \cup_{k \in K} E_k \\
& x_e \geq 0 && e \in \cup_{k \in K} E_k \\
& y_k \geq 0 && k \in K
\end{aligned}
```

with $G^k(V^k,E^k)$ and a resource constraint given as the capacity constraints. Variables $y_k$ for $k \in K$ are penalty variables with cost $P_k$ for not covering a commodity demand. In many cases they improve convergence.

Goto [code](rcmcf.py).