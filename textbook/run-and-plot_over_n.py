#!/usr/bin/env python3

"""
Accompagnying script to replicate the numerical experiments of the paper:
"Bounds on Non-linear Errors for Variance Computation with Stochastic Rounding"

Before running this script, please compile textbook.c with the following command
line:

verificarlo-c -O2 --function=textbook_sr ./textbook.c -o textbook -lm
"""


import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, cm
import numpy as np
import matplotlib
import subprocess

# SR unit-roundoff
u = 2**(-23)

# Lambda
lam = 0.1

# SR samples
sr_samples = 1

# n interval
n_values = [i*10**7  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]]


def verificarlo_run(n):
    """ simulate with verificarlo the textbook algorithm with SR single precision
    """

    cmd = 'VFC_BACKENDS="libinterflop_mca_int.so --precision-binary32=24 --mode=rr" '
    cmd += './textbook {} {} 2> error_mca.log'.format(n, sr_samples)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # The first value is the reference computation in double
    return samples[2], np.array(samples[3:])

def ieee_run(n):
    """ compute the IEEE RN-binary32 deterministic result
    """

    cmd = 'VFC_BACKENDS="libinterflop_ieee.so" '
    cmd += './textbook {} {} 2> error_ieee.log'.format(n, 1)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # The first two values are the condition numbers in double
    return samples[0], samples[1], np.array(samples[3])


def error(x, ref):
    """ returns relative forward error """
    return abs((x-ref)/ref)

# Define plot title and labels
title = "1 - $\lambda$ = {} ".format(1-lam)
plt.figure(title, figsize=(10, 6))
plt.suptitle(title)
plt.xlabel("$n$", fontsize = 14)
plt.ylabel("Error", fontsize = 14)
plt.xscale('log')
plt.yscale('log')

# RN-Binary32
ieee_error = []

# SR-Binary32
sr = [[] for _ in range(sr_samples)]
sr_average = []

# Bounds
bc = []
dm =  []
dete_bound = []
ah = []

# Compute all errors and upper bounds across increasing n
for n in n_values:
    ref, samples = verificarlo_run(n)
    cond_1, cond_2, ieee_value = ieee_run(n)
    sr_average.append(error(np.mean(samples), ref))
    ieee_error.append(error(ieee_value, ref))
    for r in range(sr_samples):
        sr[r].append([error(samples[r],ref)])
    z1 = math.sqrt(u*math.log(4 / lam) )
    z2 = math.sqrt((1+u)**(2*(n+1)) -1)
    d1 = math.sqrt(2*( (1+u)**(4*(n-1)) -1 ) )
    z3 = math.sqrt( (1+u)**(2*(n-1)) -1 )
    d2 = u*((1+u)**(2*(n-1)) - 1)/2
    dm.append(cond_2**(2) * z1 * z2 + cond_1**(2) * ((1+u)**3 * (z1*d1  +  d2 + 1 ) -1 ) )
    ah.append( cond_2**(2) * z1 * z2 + cond_1**(2)* ((1+u)**3 *(z1 * z3 +1)**2 -1 ) ) 
    a = ( (1+(u)**2)**(n+1)-1)*(2.0/(lam))
    b = ( (1+(u)**2)**(n-1)-1)*(2.0/(lam))
    bc.append( cond_2**(2) * math.sqrt( a ) + cond_1**(2) * ((1+u)**3 *(math.sqrt(b)+1)**2 -1 ))
    dete_bound.append( cond_2**(2) * ( (1+u)**(n+1)-1) + cond_1**(2) *  ((1+u)**(2*n+1) -1 ) )
    

# Plot the deterministic and probabilistic upper bounds on forward error
plt.plot(n_values, dete_bound, linestyle=':', color='b', label = 'DET-Text')
plt.plot(n_values, dm, linestyle = 'dashdot', color='m', label = 'DM-Text')
plt.plot(n_values, ah, '--', color='g', label = 'AH-Text')
plt.plot(n_values, bc, color='c', label = 'BC-Text')


# Plot RN and SR samples
for r in range(sr_samples):
   plt.plot(n_values, sr[r], ' v', color='r', label = 'SR-nearness' if r == 0 else '')
plt.plot(n_values, ieee_error, ' *', color='y', label = "RN-binary32")

plt.plot(n_values, sr_average, ' o', color='k', label = 'SR-average')



plt.legend(fontsize=14)
plt.savefig("textbook-n.pdf", format='pdf')
plt.show()

