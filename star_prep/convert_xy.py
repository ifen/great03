__author__ = 'Ian Fenech Conti'

import sys
import os
import pydrizzle.xytosky as xyConv
import pyfits

# PERFORM THE FILE CONVERSION USING XYTOSKY MODULE
sys.stdout = open(os.devnull, "w")
output = xyConv.XYtoSky_pars('/home/ian/Documents/GREAT03/0/out/starfieldimage-000-0X.fits[0]', None, None, '/home/ian/Documents/GREAT03/0/out/star_catalog-000-X.fits', 'x,y', xyConv.yes, 'IDCTAB', xyConv.no, None, xyConv.no)
sys.stdout = sys.__stdout__


# COMBINE AND CLOSE THE IDS + NEW (RA, DECS) AND SAVE TO ASC FILE
f = open('/home/ian/Documents/GREAT03/0/out/starfieldimage-000-0X.asc', 'w')
f.write("RA\t\tDEC\n")

for RA, DEC in zip(output[0], output[1]):
    f.write("%f\t%f\n" % (RA, DEC))

f.close()

