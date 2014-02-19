__author__ = 'Ian Fenech Conti'

import pyfits


def write_headfile(path_headfile, path_image):

    # LOAD AND SAVE THE G03 GALAXY IDS
    f = open(path_headfile, 'w')

    hdulist = pyfits.open(path_image)
    prihdr = hdulist[0].header

    for header_info in prihdr.cards:
        f.write(header_info.cardimage + "\n")

    f.close()


def write_headfile_tiles(tile_path, tile_list):

    for tile_name in tile_list:
        tile_image_path = '%s%s.fits' % (tile_path, tile_name)
        tile_head_path = '%s%s.head' % (tile_path, tile_name)
        write_headfile(tile_head_path, tile_image_path)


def write_imagefile(imagefile_path, image_name):
    f = open(imagefile_path, 'w')
    f.write(image_name + '\n')
    f.close()


def write_imagefile_tiles(imagefile_path, tile_names):
    f = open(imagefile_path, 'w')

    for tile_name in tile_names:
        f.write(tile_name + '\n')

    f.close()
