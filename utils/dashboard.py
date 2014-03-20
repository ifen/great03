__author__ = 'Ian Fenech Conti'

import numpy as np
import pyfits
import pylab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from array import array
import pydrizzle.xytosky as converter
import sys
import os
from decimal import *

from galaxy_prep.package_results import *
from galaxy_prep.tile_image import *

from star_prep.tiling_handler import *

# compare_outputs('/home/ian/Documents/GREAT03/0/out/OUTPUT_STANDARD.asc',
#                 '/home/ian/Documents/GREAT03/0/out/OUTPUT_CELESTIAL_DISTORTION.asc')

# plot_attribute('/home/ian/Documents/GREAT03/0/deep/OUTPUT_FIXED2.asc',
#                'SCALE_LENGTH', 'MEAN_LIKELIHOOD_E')
# plot_attribute('/home/ian/Documents/GREAT03/0/deep/OUTPUT_FIXED2.asc',
#                'MODEL_SN_RATIO', 'SCALE_LENGTH')
# plot_attribute('/home/ian/Documents/GREAT03/0/deep/OUTPUT_FIXED2.asc',
#                'MODEL_SN_RATIO', 'BULGE_FRACTION')

# path_image = '/home/ian/Documents/GREAT03/variable_psf/ground/constant/000/data_test_1_0/prep/image0.fits'
# path_tile = '/home/ian/Documents/GREAT03/variable_psf/ground/constant/000/data_test_1_0/prep/tiles/'
#
# print tile_image(path_image, path_tile, 'ground')

ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'variable_psf/ground/constant/'
OFFSET_NAME = 'subfield_offset-'
IMAGE_NAME = 'starfield_image-'

FIELD_ID = 0
SUB_FIELDS = 20

FIELD_START = FIELD_ID * SUB_FIELDS
FIELD_END = (FIELD_ID * SUB_FIELDS) + SUB_FIELDS

STARS = []


class StarSubfield:
    def __init__(self):
        self.data = []
        self.stars = []
        self.tile_x = 0
        self.tile_y = 0


def append_stars(stars, index_x, index_y):
    for subfield in STARS:
        if subfield.tile_x == index_x and subfield.tile_y == index_y:
            subfield.stars += stars

for tile_x in range(0, 5):
    for tile_y in range(0, 5):

        subfield_range = StarSubfield()

        subfield_range.tile_x = tile_x
        subfield_range.tile_y = tile_y

        STARS.append(subfield_range)

for subfield_id in range(0, 1):

    offsets_path = '%s%s%s%03d.txt' % (ROOT_PATH,
                                       BRANCH_PATH,
                                       OFFSET_NAME,
                                       subfield_id)

    image_path = '%s%s%s%03d-0.fits' % (ROOT_PATH,
                                        BRANCH_PATH,
                                        IMAGE_NAME,
                                        subfield_id)

    catalogue_path = '%s%sstar_catalog-%03d.fits' % (ROOT_PATH,
                                                     BRANCH_PATH,
                                                     subfield_id)

    offsets = np.genfromtxt(offsets_path,
                            dtype=None)

    print offsets_path
    print offsets[0]
    print offsets[1]

    for tile_x in range(0, 1):
        for tile_y in range(0, 1):

            temp_stars = get_starfield_images_tile_offset(catalogue_path,
                                                          tile_x,
                                                          tile_y,
                                                          0,
                                                          0)

            append_stars(temp_stars,
                         tile_x,
                         tile_y)


display_tile(STARS[0].stars)

print len(STARS[0].stars)


raw_input("Press Enter to continue...")























# hdulist = pyfits.open('/home/ian/Documents/GREAT03/sample/sample_image.fits')
# prihdr = hdulist[0].header
# prihdr.set('CTYPE1', 'RA---TAN')
# prihdr.set('CTYPE2', 'DEC---TAN')
# prihdr.update('EXPTIME', 21600.)
# prihdr.update('PHOTPLAM', 0.000000)
# prihdr.update('PHOTZPT', 0.000000)
# prihdr.update('PHOTFLAM', 0.000000)
# hdulist.writeto('/home/ian/Documents/GREAT03/sample/s1.fits')
# hdulist.close()

# sys.stdout = open(os.devnull, "w")
# result = converter.XYtoSky_pars('/home/ian/Documents/GREAT03/sample/s1.fits[0]', 1000, 1000, None, None, converter.yes, 'IDCTAB')
# result = converter.XYtoSky_pars('/home/ian/Documents/GREAT03/sample/s1.fits[0]', None, None, None, '/home/ian/Documents/GREAT03/sample/galaxy_catalog-000.fits', converter.yes, 'IDCTAB')
# result = converter.XYtoSky('/home/ian/Documents/GREAT03/sample/s1.fits[0]', '/home/ian/Documents/GREAT03/sample/galaxy_catalog-000.fits')
# result = converter.XYtoSky_pars('/home/ian/Documents/GREAT03/sample/s1.fits[0]', None, None, '/home/ian/Documents/GREAT03/sample/galaxy_catalog-000.fits','x,y', converter.yes, 'IDCTAB')
# sys.stdout = sys.__stdout__
#
# f = open('/home/ian/Documents/GREAT03/sample/g1.asc', 'w')
# f.write("RA\t\tDEC\n")
# for i, j in zip(result[0], result[1]):
#     f.write("%f\t%f\n" % (i, j))

#
#
# print result[0][0]
# print result[1]

#print prihdr.keys()
# hdulist[0].header['CD1_1'] = 0.1
# prihdr.update('EXPTIME', 2)
# #prihdr.set('BITPIX', 69)
# #print prihdr['BITPIX']
#
# #scidata = hdulist[0].data
# #print scidata.shape
# #print scidata[30:40, 10:20]
# hdulist.writeto('/home/ian/Documents/GREAT03/sample/s1.fits')
# #hdulist.flush();
# hdulist.close()

# f = pyfits.open('/home/ian/Documents/GREAT03/sample/galaxy_catalog-000.fits')
# tbdata = f[1].data
# newData = []
#
# for (counter, tableData) in enumerate(tbdata.base):
#     newData.append(tableData[2])
#

# img = pyfits.getdata('/home/ian/Documents/GREAT03/sample/s1.fits')
# # pylab.imshow(img)
# plt.imshow(img, aspect='auto', origin='lower')
# plt.show()

# f = open('/home/ian/Documents/GREAT03/0/subfield_offset-000.txt', 'r')
# fileHeader = f.readline()
# offsets = f.readline().split()
# print float(offsets[0])

# x = np.linspace(0, 2*np.pi, 100)
# y = np.sin(x)
#
# plt.plot(x,y)
# plt.show()