# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 13:54:32 2015
@author: Administrator
"""
import time
import ast

F1 = open("SERVICE.txt")
F1FIRST = []  
for i in range(0, 7000):
    F1FIRST.append(F1.readline().strip().split(' '))
F1.close()
FCOST = []  # COST data
F1COST = []  # COST data
for i in range(0, 7000):
    FCOST.append(int(100 * ast.literal_eval(F1FIRST[i][4])))
for i in range(0, 14):
    F1COST.append(FCOST[i*500:(i*500)+500])
FSTABILITY = []  # STABILITY data
F1STABILITY = []  # STABILITY data
for i in range(0, 7000):
    FSTABILITY.append(ast.literal_eval(F1FIRST[i][2]))
for i in range(0, 14):
    F1STABILITY.append(FSTABILITY[i*500:(i*500)+500])

F2 = open("PROCESS.txt")
F2FIRST = []
for i in range(0, 4):
    F2FIRST.append(F2.readline().strip().split(' '))
F2.close()
F2OPTION = []
F2OPTION1 = []
F2OPTION2 = []
F2OPTION3 = []
F2OPTION4 = []
for i in range(0, 4):
    for j in range(0, len(F2FIRST[i][0])):
        if i == 0 and F2FIRST[i][0][j] != '(' and F2FIRST[i][0][j] != ')' and \
        F2FIRST[i][0][j] != ',' and not F2FIRST[i][0][j] in F2OPTION1:
            F2OPTION1.append(F2FIRST[i][0][j])
        elif i == 1 and F2FIRST[i][0][j] != '(' and F2FIRST[i][0][j] != ')' and \
            F2FIRST[i][0][j] != ',' and not F2FIRST[i][0][j] in F2OPTION2:
            F2OPTION2.append(F2FIRST[i][0][j])
        elif i == 2 and F2FIRST[i][0][j] != '(' and F2FIRST[i][0][j] != ')' and \
            F2FIRST[i][0][j] != ',' and not F2FIRST[i][0][j] in F2OPTION3:
            F2OPTION3.append(F2FIRST[i][0][j])
        elif i == 3 and F2FIRST[i][0][j] != '(' and F2FIRST[i][0][j] != ')' and \
            F2FIRST[i][0][j] != ',' and not F2FIRST[i][0][j] in F2OPTION4:
            F2OPTION4.append(F2FIRST[i][0][j])
        else:
            pass
F2OPTION.append(F2OPTION1)
F2OPTION.append(F2OPTION2)
F2OPTION.append(F2OPTION3)
F2OPTION.append(F2OPTION4)

F3 = open("REQ.txt")
F3FIRST = []
for i in range(0, 4):
    F3FIRST.append(F3.readline().strip().split(','))
COST = []
STABILITY = []
for i in range(0, 4):
    COST.append(F3FIRST[i][1][:len(F3FIRST[i][1])-1])
    STABILITY.append(F3FIRST[i][0][1:])

OPTIONDATA = [[]for i in range(4)]  # service activities
for i in range(0, 4):
    for j in range(0, len(F2OPTION[i])):
        OPTIONDATA[i].append(ord(F2OPTION[i][j]) - 65)
# for i in range(4):
#     print OPTIONDATA[i]
# print "====================================================="
Q = []
PRICE = []
LST = []  # optimal combination
RELIA = []  # Reliability
FORPRINT = [['']for i in range(4)]  # print result

# change the start of j
START = [10000 for i in range(14)]
for i in range(1, 14):
    for j in range(0, 500):
        if F1COST[i][j] < START[i]:
            START[i] = F1COST[i][j]


for m in range(4):
    start = time.clock()
    r = [[0.0 for j in range(ast.literal_eval(COST[m])*100+1)]for i in range(len(OPTIONDATA[m]))]
    # STABILITY matrix
    tage = [[-1 for i in range(ast.literal_eval(COST[m])*100+1)]for i in range(len(OPTIONDATA[m]))]
    # Record COST corresponding sevice activity

    # init the matrix
    for j in range(500):
        if F1COST[OPTIONDATA[m][0]][j] < ast.literal_eval(COST[m])*100:
            r[0][F1COST[OPTIONDATA[m][0]][j]] = F1STABILITY[OPTIONDATA[m][0]][j]
            tage[0][F1COST[OPTIONDATA[m][0]][j]] = j

    # data filter
    kind = [0 for i in range(14)]
    filter_cost = [[] for i in range(14)]
    filter_stability = [[] for i in range(14)]
    choice = [[] for i in range(14)]
    fc = [0 for i in range(14)]
    fs = [0 for i in range(14)]
    for i in range(0, len(OPTIONDATA[m])):
        fc[OPTIONDATA[m][i]] = 10000
        fs[OPTIONDATA[m][i]] = 0
        for k in range(1, 500):
            if F1COST[OPTIONDATA[m][i]][k] < ast.literal_eval(COST[m])*100+1 and F1STABILITY\
            [OPTIONDATA[m][i]][k] > ast.literal_eval(STABILITY[m]) and fc[OPTIONDATA[m][i]] > \
            F1COST[OPTIONDATA[m][i]][k] and fs[OPTIONDATA[m][i]] < F1STABILITY[OPTIONDATA[m][i]][k]:
                fc[OPTIONDATA[m][i]] = F1COST[OPTIONDATA[m][i]][k]
                fs[OPTIONDATA[m][i]] = F1STABILITY[OPTIONDATA[m][i]][k]
    for i in range(0, len(OPTIONDATA[m])):
        for k in range(0, 500):
            if F1COST[OPTIONDATA[m][i]][k] < ast.literal_eval(COST[m])*100+1 and F1STABILITY\
            [OPTIONDATA[m][i]][k] > ast.literal_eval(STABILITY[m]) and not(fc[OPTIONDATA[m][i]] \
            < F1COST[OPTIONDATA[m][i]][k] and fs[OPTIONDATA[m][i]] > \
            F1STABILITY[OPTIONDATA[m][i]][k]):
                filter_cost[OPTIONDATA[m][i]].append(F1COST[OPTIONDATA[m][i]][k])
                filter_stability[OPTIONDATA[m][i]].append(F1STABILITY[OPTIONDATA[m][i]][k])
                choice[OPTIONDATA[m][i]].append(k)
        kind[OPTIONDATA[m][i]] = len(filter_cost[OPTIONDATA[m][i]])
    # for i in range(len(OPTIONDATA[m])):
    #     print i, kind[OPTIONDATA[m][i]], choice[OPTIONDATA[m][i]],

    for i in range(1, len(OPTIONDATA[m])):
        for j in range(START[OPTIONDATA[m][i]], ast.literal_eval(COST[m])*100+1):
            for k in range(0, kind[OPTIONDATA[m][i]]):
                if j - filter_cost[OPTIONDATA[m][i]][k] > 0:
                    if r[i][j] < r[i-1][j-filter_cost[OPTIONDATA[m][i]][k]] \
                    * filter_stability[OPTIONDATA[m][i]][k]:
                        r[i][j] = r[i-1][j-filter_cost[OPTIONDATA[m][i]][k]] \
                        * filter_stability[OPTIONDATA[m][i]][k]
                        tage[i][j] = choice[OPTIONDATA[m][i]][k]

    Q.append(0.0)
    PRICE.append(0)
    RELIA.append(0.0)

    # search the optimal Q, COST and RELIAbility
    for j in range(1, ast.literal_eval(COST[m])*100+1):
        if r[-1][j] > ast.literal_eval(STABILITY[m]) and r[-1][j] - j*1.0/10000 > Q[-1]:
            Q[-1] = r[-1][j] - j*1.0/10000
            PRICE[m] = j
            RELIA[-1] = r[-1][j]

    prince = PRICE[:]
    Lst = []

    # search the optimal combination
    for i in range(len(OPTIONDATA[m])-1, -1, -1):
        Lst.append(tage[i][prince[-1]]+1)
        prince[-1] -= F1COST[OPTIONDATA[m][i]][Lst[-1]-1]

    Lst.reverse()
    LST.append(Lst)

    # print result
    for j in range(len(F2FIRST[m][0])):
        if (F2FIRST[m][0][j] == '(') or (F2FIRST[m][0][j] == ')') or (F2FIRST[m][0][j] == ','):
            FORPRINT[m][0] = FORPRINT[m][0] + F2FIRST[m][0][j]
        else:
            FORPRINT[m][0] = FORPRINT[m][0] + F2FIRST[m][0][j] + '-' + \
            str(LST[m][F2OPTION[m].index(F2FIRST[m][0][j])])

    print FORPRINT[m][0] + ',Reliability=' + str(RELIA[m]) + ',COST=' + \
    str(PRICE[m]*1.0/100) + ',Q=' + str(Q[m])

    end = time.clock()

    print 'start time: {0}\nend time: {1}\nrun time: {2}'.format(start, end, end-start)
