import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import datetime as datetime

a = 0.332   #Exponential rate from least squares fit
R0 = 2.28   #Estimated R0 from cruise ship

Re = R0     #Effective transmission rate
I0 = 3.13   #Initial number of cases from least squares fit
N = 10e6    #Population pt
steps = 250 #Euler integration steps per day
noaction = 3650  #Large number, action never happens 

c = a/(R0 - 1)
b = a+c
incub = 14  #Incubation time, used for delayed action of R1 only

'''
The I state is assumed to be the time where active transmission is active, and is different from the disease time

'''

def dX(X, b, c):
    """Returns the derivative of the SIR system of equations"""
    
    #b rate of new infections
    #c half time of infectious state
    S,I,R = X
    dS = - b * S * I 
    dI = b * S * I - c * I
    dR = c * I

    return np.array([dS, dI, dR])



def simul(action,R1,R0=R0,b=b,incub=incub,N=N,I0=I0,NDAYS=180, dX=dX):
    """Simulate SIR Model"""
    X = np.zeros((NDAYS,3))       #SRI vector
    X[0] = [(N-I0)/N, I0/N, 0]  #Inital state
    for i in range(1,len(X)):
        if i < action+incub:
            Re = R0
        else:
            Re = R1

        c = b/Re

        X[i] = X[i-1]
        for j in range(steps):
            X[i] = X[i] + dX(X[i], b, c)/steps
    return(N*X)

def quickplot(X, H):
    date_list = [base + datetime.timedelta(days=x) for x in range(len(X))]
    p = plt.plot_date(date_list, X[:,0], label='S_'+str(H), linestyle='--', marker='')
    plt.plot_date(date_list, X[:,1], label='I_'+str(H), linestyle='-', color = p[0].get_color(), marker='')
    plt.plot_date(date_list, X[:,2], label='R_'+str(H), linestyle=':', color = p[0].get_color(), marker='')

#Plot experimental data
filename = "pt_20200318.dat"
base = datetime.date(2020,3,2)

data = pd.read_table(filename)
I_real = data.values[:,1]
date_list = [base + datetime.timedelta(days=x) for x in range(len(I_real))]

plt.plot_date(date_list, I_real, marker="x", label=filename)
plt.ion()
plt.show()

#Scenario 0: No action taken
H = 0
X = simul(noaction, Re)
quickplot(X, H)

#Scenario 1: Action now, 1/3 the reproduction rate
#How to estimate effect of measures??
H = 1
X = simul(16, Re/3)
quickplot(X, H)

plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('simul.png')
