__author__ = 'Ian Fenech Conti'

import pyfits

# LOAD AND SAVE THE G03 GALAXY IDS
f = open('/home/ian/Documents/GREAT03/sample/g1.head', 'w')

hdulist = pyfits.open('/home/ian/Documents/GREAT03/sample/g1.fits')
prihdr = hdulist[0].header

for headerInfo in prihdr.cards:
    f.write(headerInfo.cardimage + "\n")

f.close()

