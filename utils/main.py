__author__ = 'Ian Fenech Conti'

from galaxy_prep.convert_xy import *
from galaxy_prep.prepare_header import *
from galaxy_prep.set_tabledata import *
from galaxy_prep.write_headfile import *

path_original = '/home/ian/Documents/GREAT03/0/image-000-0.fits'
path_save = '/home/ian/Documents/GREAT03/0/out/image0.fits'
path_coeff = '/home/ian/Documents/GREAT03/0/out/image0.psfcoeffs.fits'
path_dither = '/home/ian/Documents/GREAT03/0/epoch_dither-000-0.txt'
path_offsets = '/home/ian/Documents/GREAT03/0/subfield_offset-000.txt'
path_new = '/home/ian/Documents/GREAT03/0/out/image0.fits[0]'
path_catalogue = '/home/ian/Documents/GREAT03/0/galaxy_catalog-000.fits'
path_catalogue_deg = '/home/ian/Documents/GREAT03/0/out/galaxy_catalog0.fits'
path_asc = '/home/ian/Documents/GREAT03/0/out/image0.asc'
path_headfile = '/home/ian/Documents/GREAT03/0/out/image0.head'


prepare_header(path_offsets, path_dither,
               path_original, path_save)

set_tabledata(path_catalogue,
              path_catalogue_deg)

write_headfile(path_headfile, path_save)

convert(path_new,
        path_catalogue_deg,
        path_asc)

os.chdir("/home/ian/Documents/GREAT03/0/out/")
os.system("./psfimage2coeffs "
          "/home/ian/Documents/GREAT03/0/starfield_crop-000-0X.fits "
          "%s" % path_coeff)
