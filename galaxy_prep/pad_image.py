__author__ = 'Ian Fenech Conti'

import pyfits
import numpy
from pylab import *


def pad_image(original_path, save_path, pad_size):
    fits_hdu = pyfits.open(original_path)
    image_data = fits_hdu[0].data

    image_size = image_data.shape[0]
    new_dimensions = image_size + (pad_size * 2)

    new_image = numpy.zeros(shape=(new_dimensions, new_dimensions))

    new_image[pad_size:pad_size+image_size, pad_size:pad_size+image_size] = image_data

    #plt.imshow(new_image, aspect='auto', origin='lower')
    #plt.show()

    fits_hdu[0].data = new_image
    fits_hdu.writeto(save_path)