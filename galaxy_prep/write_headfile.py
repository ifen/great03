__author__ = 'Ian Fenech Conti'

import pyfits

def write_headfile(path_headfile, path_image):

    # LOAD AND SAVE THE G03 GALAXY IDS
    f = open(path_headfile, 'w')

    hdulist = pyfits.open(path_image)
    prihdr = hdulist[0].header

    for header_info in prihdr.cards:
        f.write(header_info.cardimage + "\n")

    f.close()

