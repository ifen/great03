__author__ = 'Ian Fenech Conti'

import pyfits
from pylab import *

fits_hdu = pyfits.open('/home/ian/Documents/GREAT03/0/out/starfieldimage-000-0X.fits')
fits_image = fits_hdu[0].data
fits_crop = fits_image[0:48, 0:48]

plt.imshow(fits_crop, aspect='auto', origin='lower')
plt.show()
