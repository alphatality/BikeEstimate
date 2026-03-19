import pulp 

def def_problem(mat,d_max):
    problem = pulp.LpProblem("Bike_Station_Placement", pulp.LpMinimize)
    x= [pulp.LpVariable("x%s"%(i), cat="Binary") for i in range(len(mat))]
    y = [[pulp.LpVariable("i%s_%s"%(i,j),cat="Binary") for j in range(len(mat))] for i in range(len(mat))]
    problem += pulp.lpSum(x[i] for i in range(len(mat)))

    for j in range(len(x)):
        problem += pulp.lpSum(y[i][j] for i in range(len(mat)) if mat[i][j] <= d_max) >= 1

    for i in range(len(mat)):
        for j in range(len(mat)):
            problem+=pulp.LpConstraint(y[i][j]<=x[i])
    return problem,x,y


