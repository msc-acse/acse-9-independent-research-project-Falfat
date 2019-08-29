# Falola Yusuf, Github: falfat
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:25:37 2019

@author: falol
"""

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(111)
ax1.margins(0.1)

x = np.linspace(50, 500, 10)

time = np.array([0.026799011230468749, 0.12059936523437501, 
                 0.23002319335937499, 0.46189956665039061, 
                 0.65479507446289065, 0.87720260620117185,
                 1.4553588867187499, 1.8932235717773438,
                 2.0490318298339845, 2.4676712036132811])


ax1.plot(x, time*1000, 'ro-')

plt.xlabel("number of fractures")
plt.ylabel("time (milli seconds)")
plt.title("average times for preparing intersection analysis matrix")
# Add a legend
ax1.legend(loc='best', fontsize=14);
plt.savefig('intersection_timings')
plt.show()
