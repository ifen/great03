__author__ = 'Ian Fenech Conti'

import pyfits


def set_tabledata(path_cat_pixel, path_cat_deg, pad_size):

    f = pyfits.open(path_cat_pixel)

    table_data = f[1].data

    for (counter, tableData) in enumerate(table_data.base):
        table_data[counter][0] = table_data[counter][0] + 2 + pad_size
        table_data[counter][1] = table_data[counter][1] + 1 + pad_size

    hdu = pyfits.BinTableHDU(table_data)
    hdu.writeto(path_cat_deg)