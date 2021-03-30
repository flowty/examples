from flowty import Model

m = Model()
m.setParam("Algorithm", "MIP")
m.setParam("MIPSolver", "Xpress")

# Maximize
#  obj: x1 + 2 x2 + 3 x3 + x4
# Subject To
#  c1: - x1 + x2 + x3 + 10 x4 <= 20
#  c2: x1 - 3 x2 + x3 <= 30
#  c3: x2 - 3.5 x4 = 0
# Bounds
#  0 <= x1 <= 40
#  2 <= x4 <= 3
# General
#  x4
# End

x1 = m.addVar(lb=0, ub=40, obj=-1, type="C", name="x1w")
x2 = m.addVar(obj=-2, type="C", name="x2")
x3 = m.addVar(obj=-3, type="C", name="x3")
x4 = m.addVar(lb=2, ub=3, obj=-1, type="I", name="x4")

m += -x1 + x2 + x3 + 10 * x4 <= 20
m += x1 - 3 * x2 + x3 <= 30
m += x2 - 3.5 * x4 == 0

status = m.optimize()
# print(f"ObjectiveValue {round(m.objectiveValue, 1)}")

# get the variable values
# for var in m.vars:
#     if var.x > 0:
#         print(f"{var.name} = {round(var.x, 1)}")
