#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    # n is the real dimension of the grid
    if futo_grid:
        n = len(futo_grid)
    else:
        print("invalid futo grid")
        return
    if futo_grid[0]:
        width = len(futo_grid[0])
    else:
        print("invalid futo grid")
        return
    # all variables nxn 2D
    vars = []
    # all variables 1x(nxn) 1D
    vars_list = []
    # all inequity symboles nxn 2D
    inequity = []
    # initial domain 1~n
    domain = range(1,n+1)
    #print("domain is",domain)
    for i in range(n):
        # row contains variable in this row
        row = []
        # row inequity stands for every inequity symbol initalized (<, >, .)
        row_inequity = []
        for j in range(width):
            # for every two variables
            if j%2 == 0:
                # if the pos was not initialized
                if futo_grid[i][j] == 0:
                    var = Variable("Variable[{}][{}]".format(i, j//2), domain)
                else:
                    # if the pos was initialized with a value
                    var = Variable("Variable[{}][{}]".format(i, j//2), [futo_grid[i][j]])
                row.append(var)
                #print("at {} {} var have domain {}".format(i,j//2,var.cur_domain()))
                vars_list.append(var)
            else:
                row_inequity += [futo_grid[i][j]]
        vars.append(row)
        inequity.append(row_inequity)
    #print("var_array:",vars, "inequity",inequity)

    # now create constraint
    n = len(vars)
    #print("n is",n)
    constraints = []

    # deal with row
    #print("now dealing with row")
    for i in range(n):
        for j in range(n):
            # inequity for neighbor of row (i,j) and (i,j+1)
            if j < n-1:
                first = vars[i][j]
                second = vars[i][j+1]
                c = Constraint("Constrant(Variable[{}][{}],Variable[{}][{}])".format(i, j, i, j+1), [first, second])
                sat_tuples = get_sat_tuples(first,second, inequity[i][j])
                # add satisfying tuples to constraint
                c.add_satisfying_tuples(sat_tuples)
                constraints.append(c)
            # row element distinction (i,j) and everything else
            for k in range(j+2,n):
                first = vars[i][j]
                second = vars[i][k]
                c = Constraint("Constrant(Variable[{}][{}],Variable[{}][{}])".format(i,j,i,k), [first, second])
                sat_tuples = get_sat_tuples(first, second, '.')
                # add satisfying tuples to constraint
                c.add_satisfying_tuples(sat_tuples)
                constraints.append(c)
    # deal with column
    #print("now dealing with column")
    for j in range(n):
        for i in range(n):
            for k in range(i+1,n):
                first = vars[i][j]
                second = vars[k][j]
                c = Constraint("Constrant(Variable[{}][{}],Variable[{}][{}])".format(i,j,k,j), [first, second])
                sat_tuples = get_sat_tuples(first,second, '.')
                # add satisfying tuples to constraint
                c.add_satisfying_tuples(sat_tuples)
                constraints.append(c)

    csp = CSP("Futoshiki{}x{}".format(n, n), vars_list)
    for c in constraints:
        # add all constraint into csp
        csp.add_constraint(c)
    return csp, vars



def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT
    # n is the real dimension of the grid
    if futo_grid:
        n = len(futo_grid)
    else:
        print("invalid futo grid")
        return
    if futo_grid[0]:
        width = len(futo_grid[0])
    else:
        print("invalid futo grid")
        return
    # all variables nxn 2D
    vars = []
    # all variables 1x(nxn) 1D
    vars_list = []
    # all inequity symboles nxn 2D
    inequity = []
    # initial domain 1~n
    domain = range(1,n+1)
    # print("domain is",domain)
    for i in range(n):
        row = []
        row_inequity = []
        for j in range(width):
            # every two variables
            if j % 2 == 0:
                if futo_grid[i][j] == 0:
                    # if the pos was not initialized
                    var = Variable("Variable[{}][{}]".format(i, j//2), domain)
                else:
                    # if the pos was initialized with a value
                    var = Variable("Variable[{}][{}]".format(i, j//2), [futo_grid[i][j]])
                row.append(var)
                # print("at {} {} var have domain {}".format(i,j//2,var.cur_domain()))
                vars_list.append(var)
            else:
                row_inequity += [futo_grid[i][j]]
        vars.append(row)
        inequity.append(row_inequity)
    # now create constraint
    n = len(vars)
    #print("n is",n)
    constraints = []
    # deal with only binary inequality constraints (neighbors first)
    for i in range(n):
        for j in range(n-1):
            # inequity for neighbor of row (i,j) and (i,j+1)
            first = vars[i][j]
            second = vars[i][j + 1]
            c = Constraint("Constrant(Variable[{}][{}],Variable[{}][{}])".format(i, j, i, j + 1), [first, second])
            sat_tuples = get_sat_tuples(first, second, inequity[i][j])
            c.add_satisfying_tuples(sat_tuples)
            constraints.append(c)

    # now deal with all different constraint
    # 1) deal with rows
    for i in range(n):
        row_vars = vars[i]
        #print("row_vars",row_vars)
        # row vars for each row
        c = Constraint("Constraint(Row[{}])".format(i),row_vars)
        # now we have to check the whole row to be different
        sat_tuples = get_all_diff_sat_tuples(row_vars)
        c.add_satisfying_tuples(sat_tuples)
        constraints.append(c)
    # 2) deal with cols
    for j in range(n):
        col_vars = [vars[i][j] for i in range(n)]
        # column vars for each column
        c = Constraint("Constraint(Col[{}])".format(j), col_vars)
        sat_tuples = get_all_diff_sat_tuples(col_vars)
        c.add_satisfying_tuples(sat_tuples)
        constraints.append(c)
    csp = CSP("Futoshiki{}x{}".format(n, n), vars_list)
    for c in constraints:
        csp.add_constraint(c)
    return csp, vars



# helper function to get tuples that satisfy inequity relations for binary constraint
def get_sat_tuples(var1, var2,inequity):
    sat_tuples = []
    for x in var1.cur_domain():
        for y in var2.cur_domain():
            if inequity == '.' and x != y:
                sat_tuples.append((x,y))
            elif inequity == '>' and x > y:
                sat_tuples.append((x,y))
            elif inequity == '<' and x < y:
                sat_tuples.append((x,y))
    #print("sat_tuple for {} {} is {}".format(var1,var2,sat_tuple))
    #print("sat_tuples", sat_tuple)
    return sat_tuples

# helper function to get tuples that satisfy inequity relations for multiple constraint
def get_all_diff_sat_tuples(vars):
    sat_tuples = []
    #print([var.cur_domain() for var in vars])
    # for all combinations
    for comb in itertools.product(*[var.cur_domain() for var in vars]):
        #print("comb:",comb)
        n = len(comb)
        flag = True
        for i in range(n):
            for j in range(i+1,n):
                if comb[i] == comb[j]:
                    flag =  False
        if flag:
            sat_tuples.append(comb)
    #print("sat_tuples", sat_tuples)
    return sat_tuples






