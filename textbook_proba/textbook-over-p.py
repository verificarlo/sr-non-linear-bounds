import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, cm
import numpy as np
import matplotlib
import subprocess

"""
Accompagnying script to replicate the numerical experiments of the paper:
"Bounds on Non-linear Errors for Variance Computation with Stochastic Rounding"

Before running this script, please compile textbook.c with the following command
line:

gcc ./textbook.c -o textbook -lm
"""

# SR unit-roundoff
u = 2**(-23)

# n
n= 10**6

def ieee_run(n):
    """ compute the IEEE RN-binary32 deterministic result
    """

    cmd = 'VFC_BACKENDS_LOGFILE="ieee.log" '
    cmd += 'VFC_BACKENDS="libinterflop_ieee.so" '
    cmd += './textbook {}'.format(n)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # The two values are the condition numbers in double
    return samples[0], samples[1]


cond_1, cond_2 = ieee_run(n)

# Bounds
bc = []
dm = []
ah = []

# x-coordinate 
x = []

# Lower and upper values to compute labmda
mi = 1
ma = 8*1000

# Compute the bounds across increasing lambda
for m in range(mi, ma, ma//100):
    lam = m / 10000
    z1 = math.sqrt(u*math.log(4 / lam) )
    z2 = math.sqrt((1+u)**(2*(n+1)) -1)
    d1 = math.sqrt(2*( (1+u)**(4*(n-1)) -1 ) )
    z3 = math.sqrt( (1+u)**(2*(n-1)) -1 )
    d2 = u*((1+u)**(2*(n-1)) - 1)/2
    dm.append(cond_2**(2) * z1 * z2 + cond_1**(2) * ((1+u)**3 * (z1*d1  +  d2 + 1 ) -1 ) )
    ah.append( cond_2**(2) * z1 * z2 + cond_1**(2)* ((1+u)**3 *(z1 * z3 +1)**2 -1 )) 
    a = ( (1+(u)**2)**(n+1)-1)*(2.0/(lam))
    b = ( (1+(u)**2)**(n-1)-1)*(2.0/(lam))
    bc.append( cond_2**(2) * math.sqrt( a ) + cond_1**(2) * ((1+u)**3 *(math.sqrt(b)+1)**2 -1 ))
    x.append( lam )

# Define plot title and labels
title = "n = {} ".format( "%.e"%n)
plt.figure(title, figsize=(10, 6))
plt.suptitle(title)
plt.xlabel("$\lambda$", fontsize = 14)
plt.xscale('log')

# Plot the upper bounds of the forward error across lambda
plt.plot(x, dm, linestyle = 'dashdot', color='m', label = 'DM bound')
plt.plot(x, ah, '--', color='g', label = 'AH bound')
plt.plot(x, bc, color='c', label = 'BC bound')




plt.legend(fontsize=14)
plt.savefig("textbook-p.pdf", format='pdf')
plt.show()
