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

from galaxy_prep.convert_xy import *

convert('/home/ian/Documents/GREAT03/0/out/image-000-0X.fits[0]',
        '/home/ian/Documents/GREAT03/0/galaxy_catalog-000.fits',
        '/home/ian/Documents/GREAT03/0/out/image-000-0X.asc')



























































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