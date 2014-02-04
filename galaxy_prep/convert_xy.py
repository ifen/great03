__author__ = 'Ian Fenech Conti'

import sys
import os
import pydrizzle.xytosky as xyConv
import pyfits


def convert(fits_path, catalogue_path, path_3):
    # PERFORM THE FILE CONVERSION USING XYTOSKY MODULE
    sys.stdout = open(os.devnull, "w")
    output = xyConv.XYtoSky_pars(fits_path,
                                 None, None,
                                 catalogue_path,
                                 'x,y', xyConv.yes,
                                 'IDCTAB', xyConv.no, None,
                                 xyConv.no)
    sys.stdout = sys.__stdout__

    # LOAD AND SAVE THE G03 GALAXY IDS
    f2 = pyfits.open('/home/ian/Documents/GREAT03/0/galaxy_catalog-000.fits')
    tb_data = f2[1].data
    id_data = []

    # COMBINE AND CLOSE THE IDS + NEW (RA, DECS) AND SAVE TO ASC FILE
    f = open('/home/ian/Documents/GREAT03/0/out/image-000-0X.asc', 'w')
    f.write("RA\t\tDEC\t\tID\n")

    for (counter, tableData) in enumerate(tb_data.base):
        id_data.append(tableData[2])

    for RA, DEC, ID in zip(output[0], output[1], id_data):
        f.write("%f\t%f\t%d\n" % (RA, DEC, ID))

    f.close()

