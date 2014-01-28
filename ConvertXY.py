__author__ = 'Ian Fenech Conti'

import sys
import os
import pydrizzle.xytosky as xyConv
import pyfits

# PERFORM THE FILE CONVERSION USING XYTOSKY MODULE
sys.stdout = open(os.devnull, "w")
output = xyConv.XYtoSky_pars('/home/ian/Documents/GREAT03/0/out/image-000-0X.fits[0]', None, None, '/home/ian/Documents/GREAT03/0/galaxy_catalog-000.fits', 'x,y', xyConv.yes, 'IDCTAB')
sys.stdout = sys.__stdout__

# LOAD AND SAVE THE G03 GALAXY IDS
f2 = pyfits.open('/home/ian/Documents/GREAT03/0/galaxy_catalog-000.fits')
tbdata = f2[1].data
idData = []

# COMBINE AND CLOSE THE IDS + NEW (RA, DECS) AND SAVE TO ASC FILE
f = open('/home/ian/Documents/GREAT03/0/out/image-000-0X.asc', 'w')
f.write("RA\t\tDEC\t\tID\n")

for (counter, tableData) in enumerate(tbdata.base):
    idData.append(tableData[2])

for RA, DEC, ID in zip(output[0], output[1], idData):
    f.write("%f\t%f\t%d\n" % (RA, DEC, ID))

f.close()

