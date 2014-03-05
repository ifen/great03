__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.stats import kurtosis

path = '/home/ian/Documents/LENSFIT/TAMAL/11/starfield-000/00/00/00_residuals.modelamp.fits'

data_cube, header_data_cube = pyfits.getdata(path, 0, header=True)

data = data_cube[20]

# plt.imshow(data)
# plt.show()

cross = []

for x in range(0, 48):
    cross.append(data[24, x])

plt.figure()

plt.subplot(411, aspect='equal')
plt.imshow(data)

plt.subplot(412)
plt.hist(data)

his = ndimage.measurements.histogram(data, -100., 100., 48)
plt.subplot(413)
plt.plot(his)

plt.subplot(414)
plt.xlim((-3, 50))
plt.plot(data)

plt.tight_layout()
plt.show()

print kurtosis(his)