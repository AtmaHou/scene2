# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 13:54:32 2015

@author: Administrator
"""
import time

f1 = open("SERVICE.txt")
f1first = []#original data such as ffirst[0] = ['A-1', '954.21', '0.92', '19.33', '80.58']
for i in range(0,7000):
    f1first.append(f1.readline().strip().split(' '))
f1.close()
fcost = []#cost data
f1cost = []#cost data
for i in range(0,7000):
    fcost.append(int(100 * eval(f1first[i][4])))
for i in range(0,14):
    f1cost.append(fcost[i*500:(i*500)+500])
fstability = []#stability data
f1stability = []#stability data
for i in range(0,7000):
    fstability.append(eval(f1first[i][2]))
for i in range(0,14):
    f1stability.append(fstability[i*500:(i*500)+500])

f2 = open("PROCESS.txt")
f2first = []
for i in range(0,4):
    f2first.append(f2.readline().strip().split(' '))
f2.close()
f2option = []
f2option1 = []
f2option2 = []
f2option3 = []
f2option4 = []
for i in range(0,4):
    for j in range(0,len(f2first[i][0])):
        if i == 0 and (f2first[i][0][j] != '(') and (f2first[i][0][j] != ')') and (f2first[i][0][j] != ',') and not (f2first[i][0][j] in f2option1):
            f2option1.append(f2first[i][0][j])
        elif i == 1 and (f2first[i][0][j] != '(') and (f2first[i][0][j] != ')') and (f2first[i][0][j] != ',') and not (f2first[i][0][j] in f2option2):
            f2option2.append(f2first[i][0][j])
        elif i == 2 and (f2first[i][0][j] != '(') and (f2first[i][0][j] != ')') and (f2first[i][0][j] != ',') and not (f2first[i][0][j] in f2option3):
            f2option3.append(f2first[i][0][j])
        elif i == 3 and (f2first[i][0][j] != '(') and (f2first[i][0][j] != ')') and (f2first[i][0][j] != ',') and not (f2first[i][0][j] in f2option4):
            f2option4.append(f2first[i][0][j])
        else:
            pass
f2option.append(f2option1)
f2option.append(f2option2)
f2option.append(f2option3)
f2option.append(f2option4)
        
f3 = open("REQ.txt")
f3first = []
for i in range(0,4):
    f3first.append(f3.readline().strip().split(','))
cost = []
stability = []
for i in range(0,4):
    cost.append(f3first[i][1][:len(f3first[i][1])-1])
    stability.append(f3first[i][0][1:])
    
optiondata = [[]for i in range(4)]#sevice activities
for i in range(0,4):
    for j in range(0,len(f2option[i])):
        optiondata[i].append(ord(f2option[i][j]) - 65)

Q = []
price = []
lst = [] #optimal combination
Relia = []#Reliability
forprint = [['']for i in range(4)] #print result 

for m in range(4):
    
    start = time.clock()
    r = [[0.0 for j in range(eval(cost[m])*100+1)]for i in range(len(optiondata[m]))]#stability matrix
    tage = [[-1 for i in range(eval(cost[m])*100+1)]for i in range(len(optiondata[m]))]#Record cost corresponding sevice activity
    
    #init the matrix    
    for j in range(500):
        if f1cost[optiondata[m][0]][j] < eval(cost[m])*100:
            r[0][f1cost[optiondata[m][0]][j]] = f1stability[optiondata[m][0]][j]
            tage[0][f1cost[optiondata[m][0]][j]] = j
            
    #dp r[i][j] =max{r[i][j],r[i-1][j-f1cost[optiondata[m][i]][k]]*f1stability[optiondata[m][i]][k]}
    for i in range(1,len(optiondata[m])):
        for j in range(1,eval(cost[m])*100+1):
            for k in range(0,500):
                if j - f1cost[optiondata[m][i]][k] > 0:
                    if r[i][j] < r[i-1][j-f1cost[optiondata[m][i]][k]]*f1stability[optiondata[m][i]][k]:
                        r[i][j] = r[i-1][j-f1cost[optiondata[m][i]][k]]*f1stability[optiondata[m][i]][k]
                        tage[i][j] = k
    
    Q.append(0.0)
    price.append(0)
    Relia.append(0.0)
    
    #search the optimal Q, cost and reliability 
    for j in range(1,eval(cost[m])*100+1):
        if r[-1][j] > eval(stability[m]) and r[-1][j] - j*1.0/10000 > Q[-1]:
            Q[-1] = r[-1][j] - j*1.0/10000
            price[m] = j
            Relia[-1] = r[-1][j]
    
    prince = price[:]
    Lst = []
    #change for R10
    #search the optimal combination      
    for i in range(len(optiondata[m])-1,-1,-1):
        Lst.append(tage[i][prince[-1]]+1)
        prince[-1] -= f1cost[optiondata[m][i]][Lst[-1]-1]
         
    Lst.reverse()
    lst.append(Lst)
             
    #print result
    for j in range(len(f2first[m][0])):
        if (f2first[m][0][j] == '(') or (f2first[m][0][j] == ')') or (f2first[m][0][j] == ','):
            forprint[m][0] = forprint[m][0] + f2first[m][0][j]
        else:
            forprint[m][0] = forprint[m][0] + f2first[m][0][j] + '-' + str(lst[m][f2option[m].index(f2first[m][0][j])])
            
    print forprint[m][0] + ',Reliability=' + str(Relia[m]) + ',Cost=' + str(price[m]*1.0/100) + ',Q=' + str(Q[m])
    
    end = time.clock()
    
    print 'start time: {0}\nend time: {1}\nrun time: {2}'.format(start,end,end-start)
