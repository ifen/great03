__author__ = 'Ian Fenech Conti'

import shutil
import copy
import numpy as np
import random
import matplotlib.pyplot as plt

from star_prep.psf_handler_stacked import *
from star_prep.tiling_handler import *

# define the folder paths
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'variable_psf/ground/constant/'
FILE_NAME = 'starfield_image-'

SAMPLE_HEADER = '%s%s000/data_test_tiled/prep/image0.fits' \
                % (ROOT_PATH, BRANCH_PATH)

TILE_SIZE = 2
TILES_IMAGE = int(10./TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE/SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.02

POSTAGE_SIZE = 48

FIELD_ID = 0
SUB_FIELDS = 20

FIELD_START = FIELD_ID * SUB_FIELDS
FIELD_END = (FIELD_ID * SUB_FIELDS) + SUB_FIELDS

if len(sys.argv) < 1:
    print 'not enough args. passed to psf_pipeline'
    exit()

branch_collection = BranchCollection()
branch_collection.branch_path = '%s%s' % (ROOT_PATH, BRANCH_PATH)

# create a new field class and assign the ID.
field = StarfieldField()
field.id = FIELD_ID

# append the field info. to the branch collection.
branch_collection.fields.append(field)

plt.figure(num=None, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k')

for ID in range(FIELD_START, FIELD_END):

    # create a sub field instance
    subfield = StarfieldSubField()
    subfield.image_id = ID
    subfield.file_name = '%s%03d-0.fits' % (FILE_NAME, ID)
    subfield.file_path = '%s%s' % (branch_collection.branch_path,
                                   subfield.file_name)
    subfield.catalogue_path = '%sstar_catalog-%03d.fits' % (branch_collection.branch_path,
                                                                   ID)
    subfield.offset_path = '%ssubfield_offset-%03d.txt' % (branch_collection.branch_path,
                                                                  ID)
    subfield.image_data = load_grid_image(subfield.file_path)

    offsets = np.genfromtxt(subfield.offset_path,
                            dtype=None)

    subfield.offset_x = offsets[0]
    subfield.offset_y = offsets[1]

    # add the subfield to the field list
    field.subfields.append(subfield)

# create the directory to store the stacked field images
for field in branch_collection.fields:

    field_directory = '%sfield-%02d/' % (branch_collection.branch_path,
                                         field.id)

    field.directory = field_directory

# create the directory to store the stacked tiles
for tile_x in range(0, 1):
        for tile_y in range(0, 1):

            tile_directory = '%s%d%d/' % (field.directory,
                                          tile_x,
                                          tile_y)

            if os.path.isdir(tile_directory):
                shutil.rmtree(tile_directory)

            print tile_directory
            os.mkdir(tile_directory)

            # create the directory to store the stacked sub-tiles
            for subtile_x in range(0, SUBTILE_IMAGE):
                for subtile_y in range(0, SUBTILE_IMAGE):

                    subtile_directory = '%s%d%d/' % (tile_directory,
                                                     subtile_x,
                                                     subtile_y)

                    os.mkdir(subtile_directory)

                    # prepare all the output paths

                    subtile_imagepath = '%s%d%d.fits' % (subtile_directory,
                                                         subtile_x,
                                                         subtile_y)

                    subtile_imageplaceholder = '%s%d%d.placeholder.fits' % (subtile_directory,
                                                                            subtile_x,
                                                                            subtile_y)

                    subtile_cataloguepath_before = '%s%d%d.before.asc' \
                                                   % (subtile_directory,
                                                      subtile_x,
                                                      subtile_y)

                    subtile_cataloguepath = '%s%d%d.asc' % (subtile_directory,
                                                            subtile_x,
                                                            subtile_y)

                    subtile_tablepath = '%s%d%d.table.fits' % (subtile_directory,
                                                               subtile_x,
                                                               subtile_y)

                    subtile_headpath = '%s%d%d.head' % (subtile_directory,
                                                        subtile_x,
                                                        subtile_y)

                    # print '---------------- in subtile --------------'

                    start_stacking = 1
                    flag = 0
                    stacked_stars = []
                    stacked_image = np.zeros(shape=(0, 0))

                    # go through each subfield across a field and get the resepective
                    # subtile data.
                    for i, subfield in enumerate(field.subfields):

                        tile = StarfieldTile()
                        tile.tile_x = tile_x
                        tile.tile_y = tile_y

                        subtile = StarfieldSubtile()
                        subtile.tile_x = subtile_x
                        subtile.tile_y = subtile_y
                        subtile.tile_size = SUBTILE_SIZE

                        # print ' extracting offsets from %f %f' % \
                              # (subfield.offset_x, subfield.offset_y)

                        # get the stars in that specific tile.
                        stars_in_tile = get_starfield_images_tile_offset(subfield.catalogue_path,
                                                                         tile_x,
                                                                         tile_y,
                                                                         subfield.offset_x,
                                                                         subfield.offset_y)

                        # extract the stars from the tile into a sub-tile with an
                        # overlap.
                        stars_in_subtile = get_starfield_images_sub_tile(stars_in_tile,
                                                                         tile,
                                                                         subtile,
                                                                         SUBTILE_OVERLAP,
                                                                         flag)

                        stars_in_subtile = random.sample(stars_in_subtile, 40)

                        if flag == 0:
                            flag = 1
                        else:
                            flag = 0

                        # re-grid the stars we just extracted
                        tmp_grid, tmp_layout = regrid_tile_stacked(subfield.image_data,
                                                                   stars_in_subtile,
                                                                   POSTAGE_SIZE,
                                                                   stacked_image.shape[1])

                        if start_stacking:
                            stacked_image = tmp_grid
                            start_stacking = 0
                        else:
                            stacked_image = numpy.concatenate((stacked_image, tmp_grid), axis=1)

                        stacked_stars += tmp_layout

                    # # display the tile
                    print len(stacked_stars)
                    display_tile(stacked_stars, 1)
                    exit(0)
                    # plt.suptitle('')
                    # plt.suptitle(len(stacked_stars))
                    # stacked_stars.sort(key=lambda tup: (tup[4], tup[5]))


                    # plt.draw()
                    # plt.show()

                    # save the new regridded image to fits file.
                    save_grid(field.subfields[0].file_path,
                              subtile_imagepath,
                              stacked_image)

                    # save the star positions before we convert to RA/Dec.
                    save_catalogue(stacked_stars,
                                   subtile_cataloguepath_before)

                    save_fitstable(subtile_tablepath,
                                   stacked_stars)

                    tile = StarfieldTile()
                    tile.tile_x = tile_x
                    tile.tile_y = tile_y

                    subtile = StarfieldSubtile()
                    subtile.tile_x = subtile_x
                    subtile.tile_y = subtile_y
                    subtile.image_path = subtile_imagepath
                    subtile.image_placeholder = subtile_imageplaceholder
                    subtile.tile_size = TILE_SIZE

                    set_header_data(tile,
                                    subtile,
                                    SAMPLE_HEADER)

                    set_placeholder(subtile)

                    convert_positions('%s[0]' % subtile_imageplaceholder,
                                      subtile_tablepath,
                                      subtile_cataloguepath)

                    write_headfile_star(subtile_headpath,
                                        subtile_imagepath)

                    write_input_file('%sinput.asc' % subtile_directory,
                                     '%d%d' % (subtile_x, subtile_y))

                    os.remove(subtile_imageplaceholder)


