__author__ = 'Ian Fenech Conti'

import pyfits
from pylab import *

fits_hdu = pyfits.open('/home/ian/Documents/GREAT03/0/out/starfieldimage-000-0X.fits')
fits_image = fits_hdu[0].data
fits_crop = fits_image[0:48, 0:48]
fits_hdu[0].data = fits_crop

print len(fits_crop)

plt.imshow(fits_crop, aspect='auto', origin='lower')
plt.show()

fits_hdu.writeto('/home/ian/Documents/GREAT03/0/out/starfield_crop-000-0X.fits')