from cspbase import *
from futoshiki_csp import *
from propagators import *

test_ord_mrv = True;
test_model1 = True;
test_model2 = True;

board_1 = [[1,'<',0,'.',0],[0,'.',0,'.',2],[2,'.',0,'>',0]]
answer_1 = [1,2,3,3,1,2,2,3,1]
board_2 = [[1,'>',0,'.',3],[0,'.',0,'.',0],[3,'<',0,'.',1]]

def test(model_option,solver_option):
    score = 1
    # first test
    if model_option == 1:
        csp, var_array = futoshiki_csp_model_1(board_1)
    elif model_option == 2:
        csp, var_array = futoshiki_csp_model_2(board_1)
    else:
        print("invalid model option, return")
        return
    solver = BT(csp)
    if solver_option == 1:
        solver.bt_search(prop_BT)
    elif solver_option == 2:
        solver.bt_search(prop_FC)
    elif solver_option == 3:
        solver.bt_search(prop_GAC)
    else:
        print("invalid propagator selection, return")
        return
    sol = []
    for i in range(len(var_array)):
        for j in range(len(var_array)):
            sol.append(var_array[i][j].get_assigned_value())
    if sol == answer_1:
        print("*******Passed first model test for model {} ".format(model_option))
    else:
        print("Failed first model test for model {}: wrong solution".format(model_option))


    # second test
    if model_option == 1:
        csp2, var_array2 = futoshiki_csp_model_2(board_2)
    elif model_option == 2:
        csp2, var_array2 = futoshiki_csp_model_2(board_2)
    else:
        print("invalid model option, return")
        return
    solver = BT(csp)
    if solver_option == 1:
        solver.bt_search(prop_BT)
    elif solver_option == 2:
        solver.bt_search(prop_FC)
    elif solver_option == 3:
        solver.bt_search(prop_GAC)
    else:
        print("invalid propagator selection, return")
        return

    for i in range(len(var_array2)):
        for j in range(len(var_array2)):
            if var_array2[i][j].get_assigned_value() is not None:
                score = 0
    if score == 1:
        print("*******Passed second model test for model 1")
    else:
        print("Failed second model test for model 1: 'solved' unsolvable problem")






if __name__ == "__main__":
    
    if test_model1:

        test(1,1)
        test(1,2)
        test(1,3)


    if test_model2:
        test(2,1)
        test(2,2)
        test(2,3)

    if test_ord_mrv:

        a = Variable('A', [1])
        b = Variable('B', [1])
        c = Variable('C', [1])
        d = Variable('D', [1])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        count = 0
        for i in range(0,len(simpleCSP.vars)):
            simpleCSP.vars[count].add_domain_values(range(0, count))
            count += 1

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[0].name):
                print("*******Passed First Ord MRV Test")
            else:
                print("Failed First Ord MRV Test") 
        else:
           print("No Variable Returned from Ord MRV") 

        a = Variable('A', [1,2,3,4,5])
        b = Variable('B', [1,2,3,4])
        c = Variable('C', [1,2])
        d = Variable('D', [1,2,3])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[len(simpleCSP.vars)-1].name):
                print("*******Passed Second Ord MRV Test")
            else:
                print("Failed Second Ord MRV Test") 
        else:
           print("No Variable Returned from Ord MRV")

