# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 08:02:18 2017

@author: abhi
"""

import math


n = 3
A = [
     [ 1,   -49,   -50],
     [   49, -2399, -2552],
     [   50, -2348, -7699]
    ]


def Fib(n):
    phi = 1.61803398874989484820
    phi_ = phi - 1
    return int((phi**n - (-1*phi_)**n)/math.sqrt(5))

#for i in range(n):
#    for j in range(i):
##        print(str(i) + ',' + str(j))
#        print(A[i][j])

for i in range(110, 120):
    print(Fib(i))

