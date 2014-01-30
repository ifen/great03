__author__ = 'Ian Fenech Conti'

import pyfits

f = pyfits.open('/home/ian/Documents/GREAT03/0/star_catalog-000.fits')

table_data = f[1].data

for (counter, tableData) in enumerate(table_data.base):
    table_data[counter][0] = table_data[counter][0] + 2
    table_data[counter][1] = table_data[counter][1] + 1

hdu = pyfits.BinTableHDU(table_data)
hdu.writeto('/home/ian/Documents/GREAT03/0/out/star_catalog-000-X.fits')