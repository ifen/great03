__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
from pylab import *

FitsHDU = pyfits.open('/home/ian/Documents/GREAT03/0/image-000-0.fits')
ImOrig = FitsHDU[0].data
FitsHeader = FitsHDU[0].header

#Crop the image
Im = ImOrig[0:200, 0:200]
FitsHDU[0].data = Im

#Write it to a new file
# FitsHDU.writeto(OutFile)
# plt.imshow(Im, aspect='auto', origin='lower')
# plt.imshow(ImOrig, aspect='auto', origin='lower')
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(121)
ax.imshow(Im, aspect='auto', origin='lower')

ax = fig.add_subplot(122)
ax.imshow(ImOrig, aspect='auto', origin='lower')
plt.show()


