__author__ = 'ian'

import pyfits
from pylab import *
import os

#SET BRANCH PATHS
GREAT03 = '/home/ian/Documents/GREAT03/branch/control/ground/constant/'
UTILS = '/home/ian/Documents/GREAT03/utils'


def load_starfield(path):

    fits_hdu = pyfits.open(path)
    fits_image = fits_hdu[0].data
    return fits_image


def crop_psf(path_original, path_save, crop_size):

    fits_hdu = pyfits.open(path_original)
    fits_image = fits_hdu[0].data
    fits_crop = fits_image[48:48+48, 96:96+48]
    fits_hdu[0].data = fits_crop
    print shape(fits_crop)

    plt.imshow(fits_crop, aspect='auto', origin='lower')
    plt.show()

    fits_hdu.writeto(path_save, clobber=True)

starfield_path = '%sstarfield_image-000-0.fits' % GREAT03
starfield_path_new = '%sstarfield_image-000-0.peak.fits' % GREAT03
starfield_path_coeff = '%sstarfield_image-000-0.psfcoeffs.fits' % GREAT03
crop_psf(starfield_path, starfield_path_new, 48)
psfcoeff_args = './psfimage2coeffs ' + starfield_path_new + ' ' + starfield_path_coeff
os.chdir(UTILS)
os.system(psfcoeff_args)



