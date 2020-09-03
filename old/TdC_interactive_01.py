#!/usr/bin/env python
# coding: utf-8


import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import sympy as sym
from sympy import symbols
from scipy.optimize import fsolve





#b, psi, xi, d, fcd, beta, As, fyd, d2, MEd, mylambda, x, A1s, Es, epsilon_su = symbols('b psi xi d fcd beta As fyd d2 MEd mylambda x A1s Es, epsilon_su')




b = float(input('b = [mm]'))
fck = float(input('fck = [MPa]'))
fcd = round(fck*.85/1.5, 2)
fyk = float(input('fyk = [MPa]'))
fyd = round(fyk/1.15, 2)
d1 = float(input('d1 = [mm]'))
d2 = float(input('d2 = [mm]'))
Es = float(input('Es = [GPa]'))*10**3
epsilon_se = fyd/Es
epsilon_su = float(input('epsilon_su = [per thousand]'))/1000
epsilon_c2 = float(input('epsilon_c2 = [per thousand]'))/1000
epsilon_cu = float(input('epsilon_cu = [per thousand]'))/1000
beta = float(input('beta = A1s/As = '))
MEd = abs(float(input('MEd = [kNm]'))*10**6)
d = input(f'd = [mm] (empty if unknown)')    

#----------------------------------------As--------------------------------------
def steelArea(): 
    As_0 = initialValues.As_0
            
    print('\nInsert integer number of tensed steel reinforcement (>=2): ')
    num_As = int(input('n.:'))

            
    if (num_As < 2):
        i=0;
        while i<3:
            print('\nMinumum bars number must be greater or at least equal 2: ')
            num_As = int(input('n.:'))
            i+=1;
        if i==3:
           num_As = 2;
           print('\nNumber of tensed bars has been set to ', num_As)


    print('Insert tensed bars diameter (even number >= 12mm): ')
    phi_As = int(input('Phi = '))
            
    if (phi_As % 2) != 0 or phi_As < 12:
        i=0;
        while i<3:
            print('\nDiameter must be even and greater than 12mm): ')
            phi_As = int(input('Phi = '))
            i+=1;
        if i==3:
            phi_As = 12;
            print('\nDiameter of tensed bars has been set to ', phi_As, 'mm')
            
    As = round(num_As * np.pi * phi_As**2 /4,4)
    print('\nAs = ',num_As,'ϕ',phi_As,'mm = ',As,'mm^2')
        
    if As < As_0:
        print(As,'<',As_0,'\nMore bars needed')
        steelArea()
    return As        
#-----------------------------------------A1s----------------------------------    

def steelArea1(): 
    A1s_0 = initialValues.A1s_0
    print('\nInsert integer number of compressed steel reinforcement (>=2): ')
    num_A1s = int(input('n.:'))

    if (num_A1s < 2):
        i=0;
        while i<3:
            print('\nMinumum bars number must be greater or at least equal 2: ')
            num_A1s = int(input('n.: '))
            i+=1;

        if i==3:
            num_A1s = 2;
            print('\nNumber of compressed bars has been set to ', num_A1s)


    print('Insert compressed bars diameter (even number >= 12mm): ')
    phi_A1s = int(input('Phi = '))

    if (phi_A1s % 2) != 0 or phi_A1s < 12:
        i=0;
        while i<3:                
            print('\nDiameter must be even and greater than 12mm): ')
            phi_A1s = int(input('Phi = '))
            i+=1;
        if i==3:
            phi_A1s = 12;
            print('\nDiameter of compressed bars has been set to ', phi_A1s, 'mm')
                
    A1s = round(num_A1s * np.pi * phi_A1s**2 /4,4)
    print('\nA1s = ',num_A1s,'\u03d5',phi_A1s,'mm = ',A1s,'mm^2\n')

    if A1s < A1s_0:
        print(A1s,'<',A1s_0,'\nMore bars needed')
        steelArea1()   
    
    return A1s

        
if d == '':
    d = symbols('d')
    class initialValues():
        xi_23 = .2593;
        psi = 0.80952;
        mylambda = 0.416;
        xi = xi_23;
        dd = sym.solve(b*psi*xi*d**2 *fcd*(1-mylambda*xi) + beta* ((b*psi*xi*d*fcd)/(1-beta)) *(d-d2) - MEd, d)
        d = list(filter(lambda val: val >= 0, dd))[0]
        print('\n\nd = ', d, 'mm')
        As_0 = b*psi*xi*d*fcd/((1-beta)*fyd)
        A1s_0 = beta*As_0
        print('As = ',As_0,'mm^2\nA1s = ', A1s_0,'mm^2\n')
            
    steelArea()
    steelArea1()    

    print('Set value of d:')
    d = float(input('d = [mm] '))
    h = d+d1
    print('h = ',h, 'mm')
    
elif d<=0:
    print('Height must be positive!')
    exit()
else:
    d = float(d);
    if d<=0:
        print('Height must be positive!')
        exit()
    elif d > 0:
        print('\nd = ',d,'mm')
        class initialValues():
            As = symbols('As')
            xi_23 = .2593;
            psi = 0.80952;
            mylambda = 0.416;
            xi = xi_23;
            As_0 = sym.solve(-b*psi*xi*d *fcd*(mylambda*xi*d - d2) + As*fyd*(d-d2) - MEd, As)
            As_0 = list(filter(lambda val: val >= 0, As_0))[0]
            A1s_0 = beta*As_0
            print('As = ',As_0,'mm^2\nA1s = ', A1s_0,'mm^2\n')
            
        As = steelArea()
        A1s = steelArea1()
        As
        A1s        
        
        print('d = ',d,'\nAs = ',As,'\nA1s = ',A1s)

