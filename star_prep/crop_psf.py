__author__ = 'Ian Fenech Conti'

import pyfits
from pylab import *


def crop_psf(path_original, path_save, crop_size):

    fits_hdu = pyfits.open(path_original)
    fits_image = fits_hdu[0].data
    fits_crop = fits_image[0:crop_size, 0:crop_size]
    fits_hdu[0].data = fits_crop

    # plt.imshow(fits_crop, aspect='auto', origin='lower')
    # plt.ion()
    # plt.show()

    fits_hdu.writeto(path_save)