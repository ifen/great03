__author__ = 'Ian Fenech Conti'

import sys
import os
import pydrizzle.xytosky as xy_conv
import pyfits


def convert(fits_path, catalogue_path, asc_path):
    # PERFORM THE FILE CONVERSION USING XYTOSKY MODULE
    sys.stdout = open(os.devnull, "w")
    output = xy_conv.XYtoSky_pars(fits_path,
                                 None, None,
                                 catalogue_path,
                                 'x,y', xy_conv.yes,
                                 'IDCTAB', xy_conv.no, None,
                                 xy_conv.no)
    sys.stdout = sys.__stdout__

    # LOAD AND SAVE THE G03 GALAXY IDS
    f2 = pyfits.open(catalogue_path)
    tb_data = f2[1].data
    id_data = []

    # COMBINE AND CLOSE THE IDS + NEW (RA, DECS) AND SAVE TO ASC FILE
    f = open(asc_path, 'w')

    for (counter, tableData) in enumerate(tb_data.base):
        id_data.append(tableData[2])

    for RA, DEC, ID in zip(output[0], output[1], id_data):
        f.write("%f %f 22.0 %d\n" % (RA, DEC, ID))

    f.close()

