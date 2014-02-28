__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
import numpy as np
import math

import sys
import os

log_file = '/home/ian/Documents/LENSFIT/TAMAL/2/starfield_image-000-0.grid_ellipticities.log'

lines = [line.strip() for line in open(log_file)]

e1_model = np.zeros(len(lines))
e1_data = np.zeros(len(lines))
mean = 0

for i, line in enumerate(lines):
    vals = line.split(' ')
    e1_model[i] = vals[6]
    e1_data[i] = vals[10]
    # mean += (e1_model[i]-e1_data[i]) ** 2


print np.sqrt(((e1_model - e1_data) ** 2).mean(axis=None))

plt.figure()
plt.title('Starfield - True Gridded Star Positions')
plt.scatter(e1_model, e1_data, marker='.')
plt.show()