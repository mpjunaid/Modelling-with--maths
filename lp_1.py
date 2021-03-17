from pulp import LpVariable, LpInteger, LpProblem, LpMinimize, lpSum, GLPK, LpStatus,PULP_CBC_CMD
from data import shop_location, dij, bip, ajp
from collections import defaultdict
import numpy as np  

def assignment_problem(ajp):
    J = list(range(1,21)) # shops
    I = [1, 2] # warehouses
    ajp=(np.array(ajp)*6).tolist()

    lp_var_keys = [(i, j) for i in I for j in J]

    x = LpVariable.dicts('serve', lp_var_keys, lowBound = 0, upBound = 1, cat = LpInteger)

    model = LpProblem("Assignment_Problem", LpMinimize)

    model += lpSum([x[route] * dij[route[0]-1][route[1]-1]  for route in lp_var_keys])

    for shop in J:
        model += (lpSum([x[route] for route in lp_var_keys if shop == route[1]]) == 1, f"route_{shop}")


    model += (lpSum([ajp[route[1]-1][0]*x[route] for route in lp_var_keys if route[0] == 1]) <= bip[0][0], "w1_p1")
    model += (lpSum([ajp[route[1]-1][1]*x[route] for route in lp_var_keys if route[0] == 1]) <= bip[0][1], "w1_p2")
    model += (lpSum([ajp[route[1]-1][0]*x[route] for route in lp_var_keys if route[0] == 2]) <= bip[1][0], "w2_p1")
    model += (lpSum([ajp[route[1]-1][1]*x[route] for route in lp_var_keys if route[0] == 2]) <= bip[1][1], "w2_p2")

    #print(ajp)
    model.writeLP("lp_structure")
    model.solve(PULP_CBC_CMD(msg=False))
    #model.solve(solver=GLPK(msg=False))
    warehouse_shop_map = defaultdict(list)

    for key in lp_var_keys:
        temp_str = (x[key].name)[(x[key].name).find('(') + 1 : (x[key].name).find(')')].replace("_", " ")
        warehouse, shop = tuple(map(int, temp_str.split(', ')))
        if x[key].value() == 1:
            warehouse_shop_map[warehouse].append(shop)
    
    print(dict(warehouse_shop_map))
    

for i in ajp:
    assignment_problem(i)
    
    