__author__ = 'Ian Fenech Conti'

import pyfits
import matplotlib.pyplot as plt
import numpy
import sys
import os
import copy
import pydrizzle.xytosky as xy_conv
# from scipy.spatial import Delaunay
import matplotlib.delaunay as triang

from pyfits import Column
from decimal import *
from galaxy_prep.write_headfile import *


def display_tiles(catalogue_path):

    f = pyfits.open(catalogue_path)

    table_data = f[1].data
    real_x_pos = []
    real_y_pos = []
    real_tile = []
    tile_count = 0

    for starfield_position in enumerate(table_data.base):
        real_x_pos.append((starfield_position[1][6] * 4800) / 10)
        real_y_pos.append((starfield_position[1][7] * 4800) / 10)

        real_tile_x = starfield_position[1][2]
        real_tile_y = starfield_position[1][3]

        if real_tile_x == 2 and real_tile_y == 2:
            tile_count += 1

        real_tile.append(real_tile_x * 1.5 + real_tile_y * 9.323)

    print 'smallest x-value : %f' % min(real_x_pos)
    print 'smallest y-value : %f' % min(real_y_pos)
    print 'tile count : %d' % tile_count

    plt.figure()
    plt.ylim([-10, 4810])
    plt.xlim([-10, 4810])
    plt.plot(real_x_pos, real_y_pos, 'ko', markersize=0.9)
    plt.title('Starfield - True Star Positions')

    plt.figure()
    plt.ylim([-10, 4810])
    plt.xlim([-10, 4810])
    plt.title('Starfield - True Gridded Star Positions')
    plt.scatter(real_x_pos, real_y_pos, c=real_tile, marker='o')

    plt.draw()
    plt.show()


def load_grid_image(image_path):

    fits_hdu = pyfits.open(image_path)
    fits_image = fits_hdu[0].data
    return fits_image


def get_star(grid_x, grid_y, grid_image):
    star_postage = grid_image[grid_y-23:grid_y+25, grid_x-23:grid_x+25]
    return star_postage


def display_star(grid_image_path, grid_x, grid_y):

    grid_image = load_grid_image(grid_image_path)
    star_postage = get_star(grid_x, grid_y, grid_image)

    plt.imshow(star_postage, aspect='auto', origin='lower')
    plt.grid()
    plt.show()


def get_starfield_images_tile(catalogue_path, tile_index_x, tile_index_y):

    starfield_images = []

    f = pyfits.open(catalogue_path)
    table_data = f[1].data

    for starfield_position in table_data.base:
        starfield_data = starfield_position
        if starfield_data[2] == tile_index_x and starfield_data[3] == tile_index_y:
            starfield_images.append(starfield_data)

    starfield_images.sort(key=lambda tup: (tup[4], tup[5]))

    return starfield_images


def get_starfield_images_tile_constant(catalogue_path):

    starfield_images = []

    f = pyfits.open(catalogue_path)
    table_data = f[1].data

    for starfield_position in table_data.base:
        starfield_data = starfield_position
        starfield_images.append(starfield_data)

    return starfield_images


def get_starfield_images_tile_offset(catalogue_path, tile_index_x, tile_index_y, offset_x, offset_y):

    starfield_images = []

    f = pyfits.open(catalogue_path)
    table_data = f[1].data

    for starfield_position in table_data.base:
        starfield_data = starfield_position
        if starfield_data[2] == tile_index_x and starfield_data[3] == tile_index_y:
            starfield_data[4] += offset_x
            starfield_data[5] += offset_y
            starfield_data[6] += offset_x
            starfield_data[7] += offset_y
            starfield_images.append(starfield_data)

    starfield_images.sort(key=lambda tup: (tup[4], tup[5]))

    return starfield_images


def get_starfield_images_tile_2(catalogue_path, tile_index_x, tile_index_y, overlap):

    starfield_images = []
    starfield_images_deg = []

    f = pyfits.open(catalogue_path)
    table_data = f[1].data

    x_start_deg = (2.0 * tile_index_x) - overlap
    x_end_deg = ((2.0 * tile_index_x) + 2.0) + overlap
    y_start_deg = (2.0 * tile_index_y) - overlap
    y_end_deg = ((2.0 * tile_index_y) + 2.0) + overlap

    for starfield_position in table_data.base:
        starfield_data = starfield_position
        if (x_start_deg <= starfield_data[6] < x_end_deg) and (y_start_deg <= starfield_data[7] < y_end_deg):
            starfield_images_deg.append(starfield_data)

    starfield_images_deg.sort(key=lambda tup: (tup[4], tup[5]))

    display_tile(starfield_images_deg)

    return starfield_images_deg


def get_starfield_images_tile_deg(catalogue_path, tile_index_x, tile_index_y, width, overlap):

    starfield_images_deg = []

    f = pyfits.open(catalogue_path)
    table_data = f[1].data

    x_start_deg = tile_index_x
    x_end_deg = tile_index_x + width
    y_start_deg = tile_index_y
    y_end_deg = tile_index_y + width

    for starfield_position in table_data.base:
        starfield_data = starfield_position
        if (x_start_deg <= starfield_data[6] < x_end_deg) and (y_start_deg <= starfield_data[7] < y_end_deg):
            starfield_images_deg.append(starfield_data)

    starfield_images_deg.sort(key=lambda tup: (tup[4], tup[5]))

    display_tile(starfield_images_deg)

    return starfield_images_deg


def get_starfield_images_sub_tile(stars, starfield_tile, starfield_subtile, overlap, flag):

    stars_in_subtile = []

    x_start_deg = (starfield_tile.tile_x * starfield_tile.tile_size) + \
                  (starfield_subtile.tile_x * starfield_subtile.tile_size) - overlap
    x_end_deg = (starfield_tile.tile_x * starfield_tile.tile_size) + \
                (starfield_subtile.tile_x * starfield_subtile.tile_size) + starfield_subtile.tile_size + overlap

    y_start_deg = (starfield_tile.tile_y * starfield_tile.tile_size) + \
                  (starfield_subtile.tile_y * starfield_subtile.tile_size) - overlap
    y_end_deg = (starfield_tile.tile_y * starfield_tile.tile_size) + \
                (starfield_subtile.tile_y * starfield_subtile.tile_size) + starfield_subtile.tile_size + overlap

    # print 'x (%f : %f) y (%f : %f) ' % (x_start_deg, x_end_deg, y_start_deg, y_end_deg)

    for starfield_position in stars:
        starfield_data = starfield_position
        if (x_start_deg <= starfield_data[6] < x_end_deg) and (y_start_deg <= starfield_data[7] < y_end_deg):
            stars_in_subtile.append(starfield_data)

    stars_in_subtile.sort(key=lambda tup: (tup[4], tup[5]))
    res = stars_in_subtile

    # display_tile(res)

    return res


def display_tile(tile, i):
    real_x_pos = []
    real_y_pos = []
    real_tile = []

    for starfield_position in tile:
        real_x_pos.append((starfield_position[6] * 4800) / 10)
        real_y_pos.append((starfield_position[7] * 4800) / 10)

        real_tile_x = starfield_position[2]
        real_tile_y = starfield_position[3]

        real_tile.append(i)

    plt.ylim([0, 270])
    plt.xlim([0, 270])
    plt.title('Starfield - True Gridded Star Single Subfield')
    c = i/20.0
    print c
    plt.scatter(real_x_pos, real_y_pos, color=(0.1, 0.0, 0.0), marker='+')

    # plt.ion()
    plt.draw()
    plt.show()


def display_tile_stacked(tile):
    real_x_pos = []
    real_y_pos = []
    real_tile = []
    point = []

    for starfield_position in tile:
        real_x_pos.append((starfield_position[6] * 4800) / 10)
        real_y_pos.append((starfield_position[7] * 4800) / 10)

        point.append(((starfield_position[6] * 4800) / 10, (starfield_position[7] * 4800) / 10))

        real_tile_x = starfield_position[2]
        real_tile_y = starfield_position[3]

        real_tile.append(real_tile_x + 1.5 * real_tile_y + 9.323)

    # plt.ylim([-10, 4810])
    # plt.xlim([-10, 4810])
    # plt.title('Starfield - True Gridded Star Single Subfield')
    # plt.scatter(real_x_pos, real_y_pos, c=real_tile, marker='+')
    # plt.ion()
    # plt.draw()
    # plt.show()

    real_x_pos = numpy.array(real_x_pos)
    real_y_pos = numpy.array(real_y_pos)

    cens, edg, tri, neig = triang.delaunay(real_x_pos, real_y_pos)

    for t in tri:
        t_i = [t[0], t[1], t[2], t[0]]
        plt.plot(real_x_pos[t_i], real_y_pos[t_i])

    plt.plot(real_x_pos, real_y_pos, 'o')
    plt.show()


def regrid_tile(gridded_image, starfield_images, postage_stamp_size):

    num_stars = len(starfield_images)
    new_grid = numpy.zeros(shape=(postage_stamp_size, num_stars*postage_stamp_size))

    tmp_starfield_images = []

    for i, starfield_image in enumerate(starfield_images):
        tmp_starfield = copy.copy(starfield_image)
        x = tmp_starfield[0]
        y = tmp_starfield[1]

        star = get_star(x, y, gridded_image)

        start = i * postage_stamp_size
        end = i * postage_stamp_size + postage_stamp_size

        new_grid[0:postage_stamp_size, start:end] = star

        tmp_starfield[0] = i * postage_stamp_size + 23
        tmp_starfield[1] = 23.

        tmp_starfield_images.append(tmp_starfield)

    #plt.imshow(new_grid, aspect='auto', origin='lower')
    #plt.show()
    return new_grid, tmp_starfield_images


def regrid_tile_stacked(gridded_image, starfield_images, postage_stamp_size, offset):

    num_stars = len(starfield_images)
    new_grid = numpy.zeros(shape=(postage_stamp_size, num_stars*postage_stamp_size))

    tmp_starfield_images = []

    for i, starfield_image in enumerate(starfield_images):
        tmp_starfield = copy.copy(starfield_image)
        x = tmp_starfield[0]
        y = tmp_starfield[1]

        star = get_star(x, y, gridded_image)

        start = i * postage_stamp_size
        end = i * postage_stamp_size + postage_stamp_size

        new_grid[0:postage_stamp_size, start:end] = star

        tmp_starfield[0] = i * postage_stamp_size + 23 + offset
        tmp_starfield[1] = 23.

        tmp_starfield_images.append(tmp_starfield)

    # plt.imshow(new_grid, aspect='auto', origin='lower')
    # plt.show()
    return new_grid, tmp_starfield_images


def save_grid(original_path, save_path, gridded_image):

    fits_hdu = pyfits.open(original_path)
    fits_hdu[0].data = gridded_image

    fits_hdu.writeto(save_path)


def save_catalogue(tile_positions, save_path):

    f = open(save_path, 'w')

    f.write('# elements %d\n' % len(tile_positions))
    f.write('# x_gridded_pos\n')
    f.write('# y_gridded_pos\n')
    f.write('# x_tile_index\n')
    f.write('# y_tile_index\n')
    f.write('# tile_x_pos_deg\n')
    f.write('# tile_y_pos_deg\n')
    f.write('# x_field_true_deg\n')
    f.write('# y_field_true_deg\n')
    f.write('# x_field_true_pixel\n')
    f.write('# y_field_true_pixel\n')

    for tile_position in tile_positions:
        f.write('%.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e\n'
                % (tile_position[0],
                   tile_position[1],
                   tile_position[2],
                   tile_position[3],
                   Decimal(tile_position[4]),
                   Decimal(tile_position[5]),
                   Decimal(tile_position[6]),
                   Decimal(tile_position[7]),
                   Decimal(((tile_position[6]*4800)/10)+2),
                   Decimal(((tile_position[7]*4800)/10)+1)))

    f.close()


def save_catalogue_constant(tile_positions, save_path):

    f = open(save_path, 'w')

    f.write('# elements %d\n' % len(tile_positions))
    f.write('# x_gridded_pos\n')
    f.write('# y_gridded_pos\n')

    for tile_position in tile_positions:
        f.write('%.18e %.18e\n'
                % (tile_position[0],
                   tile_position[1]))

    f.close()


def save_fitstable(table_path, tiled_positions):

    c1 = Column(name='x', format='D')
    c2 = Column(name='y', format='D')
    c3 = Column(name='x_tile', format='K')
    c4 = Column(name='y_tile', format='K')
    coldefs = pyfits.ColDefs([c1, c2, c3, c4])
    tbhdu = pyfits.new_table(coldefs, nrows=len(tiled_positions))

    for c, tiled_position in enumerate(tiled_positions):
        tbhdu.data[c] = [(tiled_position[6]*4800)/10,
                         (tiled_position[7]*4800)/10,
                         (tiled_position[0]+2),
                         (tiled_position[1]+1)
                         ]

    tbhdu.writeto(table_path)


def save_fitstable_constant(table_path, tiled_positions):

    c1 = Column(name='x', format='D')
    c2 = Column(name='y', format='D')
    coldefs = pyfits.ColDefs([c1, c2])
    tbhdu = pyfits.new_table(coldefs, nrows=len(tiled_positions))

    for c, tiled_position in enumerate(tiled_positions):
        tbhdu.data[c] = [(tiled_position[0]),
                         (tiled_position[1])]

    tbhdu.writeto(table_path)


def convert_positions(tiled_galaxy_image_path, tiled_starfield_positions, tiled_starfield_path):

    # PERFORM THE FILE CONVERSION USING XYTOSKY MODULE
    sys.stdout = open(os.devnull, "w")
    output = xy_conv.XYtoSky_pars(tiled_galaxy_image_path,
                                  None, None,
                                  tiled_starfield_positions,
                                  'x,y', xy_conv.yes,
                                  'IDCTAB', xy_conv.no, None,
                                  xy_conv.no)
    # val = xy_conv.XYtoSky_pars(fits_path, x=23, y=23)
    sys.stdout = sys.__stdout__
    #
    f2 = pyfits.open(tiled_starfield_positions)
    table_data = f2[1].data

    # COMBINE AND CLOSE THE IDS + NEW (RA, DECS) AND SAVE TO ASC FILE
    f = open(tiled_starfield_path, 'w')

    for RA, DEC, TABLE_DATA in zip(output[0], output[1], table_data):
        f.write("%.18e %.18e\n" % (RA, DEC))
        # f.write("%.18e %.18e %.18e %.18e 23.0\n" % (
        #     Decimal(RA),
        #     Decimal(DEC),
        #     TABLE_DATA[2],
        #     TABLE_DATA[3]))
    f.close()


def copy_galaxy_tile_header(galaxy_tile_image, starfield_tile_image):

    fits_hdu = pyfits.open(galaxy_tile_image)
    galaxy_tile_header = fits_hdu[0].header

    fits_hdu_starfield = pyfits.open(starfield_tile_image)
    fits_hdu_starfield[0].header = galaxy_tile_header

    fits_hdu_starfield[0].header.set('GAIN', 10000)

    fits_hdu_starfield.writeto(starfield_tile_image, clobber=True)


def set_header_data(starfield_tile, starfield_subtile, galaxy_tile_image):

    fits_hdu = pyfits.open(galaxy_tile_image)
    galaxy_tile_header = fits_hdu[0].header

    naxis_1 = galaxy_tile_header['NAXIS1']
    naxis_2 = galaxy_tile_header['NAXIS2']

    fits_hdu_starfield = pyfits.open(starfield_subtile.image_path)
    fits_hdu_starfield[0].header = galaxy_tile_header

    tile_start_x = (starfield_tile.tile_x * naxis_1) / 10
    tile_start_y = (starfield_tile.tile_y * naxis_1) / 10

    subtile_start_x = (((starfield_subtile.tile_x*starfield_subtile.tile_size)*naxis_2) / 10)
    subtile_start_y = (((starfield_subtile.tile_y*starfield_subtile.tile_size)*naxis_2) / 10)

    x_offset = naxis_1/2 - (tile_start_x + subtile_start_x)
    y_offset = naxis_2/2 - (tile_start_y + subtile_start_y)

    fits_hdu_starfield[0].header.update('CRPIX1', x_offset)
    fits_hdu_starfield[0].header.update('CRPIX2', y_offset)
    fits_hdu_starfield[0].header.set('GAIN', 10000)

    fits_hdu_starfield.writeto(starfield_subtile.image_path, clobber=True)


def set_header_data_constant(save_path, galaxy_tile_image):

    fits_hdu = pyfits.open(galaxy_tile_image)
    galaxy_tile_header = fits_hdu[0].header

    fits_hdu_starfield = pyfits.open(save_path)
    fits_hdu_starfield[0].header = galaxy_tile_header

    fits_hdu_starfield[0].header.set('GAIN', 10000)

    fits_hdu_starfield.writeto(save_path, clobber=True)


def set_placeholder(starfield_subtile):

    gridded_hdu = pyfits.open(starfield_subtile.image_path)

    placeholder_size = (starfield_subtile.tile_size*4800)/10
    placeholder = numpy.zeros(shape=(placeholder_size, placeholder_size))

    gridded_hdu[0].data = placeholder

    gridded_hdu.writeto(starfield_subtile.image_placeholder, clobber=True)


def write_headfile_star(path_headfile, path_image):
    write_headfile(path_headfile, path_image)


def write_input_file(path_input, file_name):
    f = open(path_input, 'w')
    f.write(file_name + '\n')
    f.close()


def plot_lensift_star(star_path):
    lines = [line.strip() for line in open(star_path)]

    image = numpy.zeros(shape=(48, 48))

    for line in lines:
        val = line.split()
        image[val[1], val[0]] = val[2]

    plt.imshow(image, aspect='auto', origin='lower')
    plt.show()



