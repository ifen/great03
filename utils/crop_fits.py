__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
from pylab import *


if __name__ == "__main__":

    #LOAD IMAGES
    FitsHDU = pyfits.open('/home/ian/Documents/GREAT03/0/image-000-0.fits')
    ImOrig = FitsHDU[0].data
    FitsHeader = FitsHDU[0].header

    #EXTRACT THE DATA FROM THE FITS FILE
    Im = ImOrig[0:200, 4600:4800]
    FitsHDU[0].data = Im

    #PLOT CROPPED IMAGE AND ORIGINAL
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.imshow(Im, aspect='auto', origin='lower')

    ax = fig.add_subplot(122)
    ax.imshow(ImOrig, aspect='auto', origin='lower')
    plt.show()




