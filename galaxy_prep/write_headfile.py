__author__ = 'Ian Fenech Conti'

import pyfits

# LOAD AND SAVE THE G03 GALAXY IDS
f = open('/home/ian/Documents/GREAT03/0/out/image-000-0X.head', 'w')

hdulist = pyfits.open('/home/ian/Documents/GREAT03/0/out/image-000-0X.fits')
prihdr = hdulist[0].header

for header_info in prihdr.cards:
    f.write(header_info.cardimage + "\n")

f.close()

