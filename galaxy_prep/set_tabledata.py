__author__ = 'Ian Fenech Conti'

import pyfits
from pyfits import Column


def set_tabledata(path_cat_pixel, path_cat_deg, pad_size):

    f = pyfits.open(path_cat_pixel)

    table_data = f[1].data

    for (counter, tableData) in enumerate(table_data.base):
        table_data[counter][0] = table_data[counter][0] + 2 + pad_size
        table_data[counter][1] = table_data[counter][1] + 1 + pad_size

    hdu = pyfits.BinTableHDU(table_data)
    hdu.writeto(path_cat_deg)


def set_tabledata_offset_deep(path_cat_pixel, path_cat_deg, offset_x, offset_y):

    f = pyfits.open(path_cat_pixel)

    table_data = f[1].data

    offset_x_p = (offset_x * 4800) / 10.0
    offset_y_p = (offset_y * 4800) / 10.0

    for (counter, tableData) in enumerate(table_data.base):
        table_data[counter][0] = table_data[counter][0] + 2 + offset_x_p
        table_data[counter][1] = table_data[counter][1] + 2 + offset_y_p

    hdu = pyfits.BinTableHDU(table_data)
    hdu.writeto(path_cat_deg)


def set_tabledata_offset(table_path, tiled_positions):

    c1 = Column(name='x', format='D')
    c2 = Column(name='y', format='D')
    c3 = Column(name='ID', format='D')
    coldefs = pyfits.ColDefs([c1, c2, c3])
    tbhdu = pyfits.new_table(coldefs, nrows=len(tiled_positions))

    for c, tiled_position in enumerate(tiled_positions):
        tbhdu.data[c] = [((tiled_position[7]*4800)/10) + 24,
                         ((tiled_position[8]*4800)/10) + 24,
                         (tiled_position[2])]

    tbhdu.writeto(table_path)

