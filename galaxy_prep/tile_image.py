__author__ = 'Ian Fenech Conti'

import pyfits
import os

from pylab import *

def tile_image(image_path,
               save_folder,
               survey_type):
    if survey_type == 'ground':
        tile_area = 960
    elif survey_type == 'space':
        tile_area = 96
    else:
        tile_area = 1600

    tile_paths = []

    [tile_paths.append(prepare_tile(tile_area, i, j, image_path, save_folder))
     for i in range(5) for j in range(5)]

    # plt.imshow(fits_crop, aspect='auto', origin='lower')
    # plt.show()

    return tile_paths

def prepare_tile(tile_area, tile_index_x, tile_index_y,
                 image_path, save_folder):

    x_crop_start = tile_index_x * tile_area
    y_crop_start = tile_index_y * tile_area

    x_crop_end = x_crop_start + tile_area
    y_crop_end = y_crop_start + tile_area

    fits_hdu = pyfits.open(image_path)
    fits_image = fits_hdu[0].data
    fits_header = fits_hdu[0].header

    naxis_1 = fits_header['NAXIS1']
    naxis_2 = fits_header['NAXIS2']

    fits_header.set('CRPIX1', (naxis_1/2) - x_crop_start)
    fits_header.set('CRPIX2', (naxis_2/2) - y_crop_start)

    fits_crop = fits_image[y_crop_start:y_crop_end,
                           x_crop_start:x_crop_end]

    fits_hdu[0].data = fits_crop
    fits_hdu[0].header = fits_header

    image_name = os.path.splitext(os.path.basename(image_path))[0]

    tile_name = '%s-%d%d.tile' % (image_name,
                                  tile_index_x,
                                  tile_index_y)

    save_path = '%s%s.fits' % (save_folder,
                               tile_name)

    fits_hdu.writeto(save_path, clobber=True)

    return tile_name