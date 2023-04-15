#!/usr/bin/env python3

"""
Accompagnying script to replicate the numerical experiments of the paper:
"Bounds on Non-linear Errors for Variance Computation with Stochastic Rounding"

Before running this script, please compile text_vs_tp_sr.c with the following command
line:

verificarlo-c -O2 --function=text_vs_tp_sr ./text_vs_tp_sr.c -o text_vs_tp_sr -lm
"""


import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, cm
import numpy as np
import matplotlib
import subprocess
import matplotlib.ticker as ticker


# SR samples
sr_samples = 30

# n interval
n_values = [i*10**4  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]]



def verificarlo_run(n):
    """ simulate with verificarlo the textbook algorithm with SR single precision
    """

    cmd = 'VFC_BACKENDS="libinterflop_mca_int.so --precision-binary32=24 --mode=rr" '
    cmd += './text_vs_tp_sr {} {} 2> error_mca.log'.format(n, sr_samples)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # the two first values are the textbook and two-pass references computation in double.   
    return samples[0], samples[1], np.array(samples[2:])

def ieee_run(n):
    """ compute the IEEE RN-binary32 deterministic result
    """

    cmd = 'VFC_BACKENDS="libinterflop_ieee.so" '
    cmd += './text_vs_tp_sr {} {} 2> error_ieee.log'.format(n, sr_samples)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # textbook and two-pass IEEE RN-binary32 deterministic results
    return samples[2], samples[3]

def error(x, ref):
    """ returns relative forward error """
    return abs((x-ref)/ref)

# RN-Binary32
text_ieee_error = []
tp_ieee_error = []

# SR-Binary32
text_sr_data = []
tp_sr_data = []


# Compute all textbook and two-pass errors across increasing n
for n in n_values:
    text_ref, tp_ref, samples = verificarlo_run(n)
    ieee_text, ieee_tp = ieee_run(n)
    # RN_errors
    text_ieee_error.append(error(ieee_text, text_ref))
    tp_ieee_error.append(error(ieee_tp, text_ref))
    # SR errors
    text_sr = [] 
    tp_sr = [] 
    for r in range(sr_samples):
       text_sr.append(error(samples[2*r],text_ref))
       tp_sr.append(error(samples[2*r+1],tp_ref))
    text_sr_data.append(text_sr)   
    tp_sr_data.append(tp_sr)


# Define plot labels
plt.figure(figsize=(10, 6))
plt.xlabel("$n$", fontsize=14)
plt.ylabel("Error", fontsize=14)
plt.xscale('log')
plt.yscale('log')

# Set the widths 
box_wi  = [i*10**3  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]]

# Set the positions of the box plots
low_values = [0.9*i*10**4  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]]
hei_values = [1.1*i*10**4  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]]

# Create the box plot
text = plt.boxplot(text_sr_data, widths=box_wi, positions=low_values, patch_artist=True, boxprops=dict(facecolor="C0"))
tp = plt.boxplot(tp_sr_data, widths=box_wi, positions=hei_values, patch_artist=True, boxprops=dict(facecolor="C2"))



# Add labels to legend
plt.legend([text["boxes"][0], tp["boxes"][0], plt.Line2D([], [], marker='*', color='y', linestyle='None'),
            plt.Line2D([], [], marker='p', color='k', linestyle='None')],
           ['Textbook', 'Two-pass', 'RN-Text', 'RN-TP'], fontsize=14, loc='lower right')

# Plot RN samples
plt.plot(low_values, text_ieee_error, ' *', color='y', label="RN-Text")
plt.plot(hei_values, tp_ieee_error, 'p', color='k', label="RN-TP")

plt.xticks(n_values, fontsize = 14)
plt.yticks(fontsize = 14)

# Set x-axis tick formatter to scientific notation
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())

plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))


plt.savefig("text-vs-tp.pdf", format='pdf')
plt.show()

