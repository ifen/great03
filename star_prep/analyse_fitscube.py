__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.stats import kurtosis

path = '/home/ian/Documents/LENSFIT/TAMAL/15/starfield-000/00/22/22_residuals.modelamp.fits'

data_cube, header_data_cube = pyfits.getdata(path, 0, header=True)

data = data_cube[32]

# plt.imshow(data)
# plt.show()

cross = []

for x in range(0, 48):
    cross.append(data[24, x])

plt.figure()
plt.suptitle('Residual for Star 32')

plt.subplot(211)
plt.xlim((-3, 50))
plt.title('Cross Section Pixel Values')
plt.plot(data)

plt.subplot(223, aspect='equal')
plt.title('Residual')
plt.imshow(data)

plt.subplot(224)
plt.title('Histogram')
plt.hist(data)


# plt.tight_layout()
plt.show()
