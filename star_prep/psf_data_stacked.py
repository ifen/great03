__author__ = 'Ian Fenech Conti'

import shutil
import copy
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import warnings

# APPEND THE GREAT03 CODE REPOSITORY
sys.path.append('/home/ian/Documents/GITHUB/great03/')

from star_prep.psf_handler_stacked import *
from star_prep.tiling_handler import *

# define the folder paths
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/variable_psf/ground/constant/'
FILE_NAME = 'starfield_image-'

SAMPLE_HEADER = '%sutils/sample.fits' \
                % ROOT_PATH

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)
SUBTILE_OVERLAP = 0

POSTAGE_SIZE = 48
PADDING_SIZE = 10

FIELD_ID = 1
SUB_FIELDS = 20

FIELD_START = FIELD_ID * SUB_FIELDS
FIELD_END = (FIELD_ID * SUB_FIELDS) + SUB_FIELDS

if len(sys.argv) < 1:
    print 'not enough args. passed to psf_pipeline'
    exit()

# disable all warnings
warnings.filterwarnings("ignore")

# FIELD_ID = int(sys.argv[1])
# FIELD_ID = 0

branch_collection = BranchCollection()
branch_collection.branch_path = '%s%s' % (ROOT_PATH, BRANCH_PATH)

# create a new field class and assign the ID.
field = StarfieldField()
field.id = FIELD_ID

# append the field info. to the branch collection.
branch_collection.fields.append(field)

# save directory
instance_name = 'VPGc_3'
root_save_directory = '%s%s/' % (branch_collection.branch_path, instance_name)
#if os.path.isdir(root_save_directory):
#    shutil.rmtree(root_save_directory)
#os.mkdir(root_save_directory)

plt.figure(num=None, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='r')

print 'preparing PSF data for field : %d \n  instance name : %s' % (FIELD_ID, instance_name)

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
    subfield.starfield_catalogue = get_starfield_catalogue_data(subfield.catalogue_path)

    offsets = np.genfromtxt(subfield.offset_path,
                            dtype=None)

    # subfield.offset_x = offsets[0]
    # subfield.offset_y = offsets[1]
    subfield.offset_x = 0
    subfield.offset_y = 0

    # add the subfield to the field list
    field.subfields.append(subfield)

print '  data loaded. \n'

# create the directory to store the stacked field images
for field in branch_collection.fields:

    # create save_path for fields	
    field_directory = '%s%s/%02d/' % (branch_collection.branch_path,
                                      instance_name,
                                      field.id)

    field.directory = field_directory

    if os.path.isdir(field_directory):
        shutil.rmtree(field_directory)
    os.mkdir(field_directory)

# create the directory to store the stacked tiles
for tile_x in range(0, TILES_IMAGE):
    for tile_y in range(0, TILES_IMAGE):

        tile_directory = '%s%02d_%02d/' % (field.directory,
                                           tile_x,
                                           tile_y)

        if os.path.isdir(tile_directory):
            shutil.rmtree(tile_directory)

        os.mkdir(tile_directory)

        print '  preparing PSF data for tile (%d, %d) ' % (tile_x, tile_y)
        print '  save directory : %s' % tile_directory
        print '  --------------------------------------'

        global_tile_count = 0
        global_tile_stars = []

        # create the directory to store the stacked sub-tiles
        for subtile_x in range(0, SUBTILE_IMAGE):
            for subtile_y in range(0, SUBTILE_IMAGE):

                print '    processing sub-tile (%d, %d) ' % (subtile_x, subtile_y)

                subtile_directory = '%s%02d_%02d/' % (tile_directory,
                                                      subtile_x,
                                                      subtile_y)

                os.mkdir(subtile_directory)

                # prepare all the output paths

                subtile_imagepath = '%ssubtile_%02d_%02d.fits' % (subtile_directory,
                                                                  subtile_x,
                                                                  subtile_y)

                subtile_imageplaceholder = '%ssubtile_%02d_%02d.placeholder.fits' % (subtile_directory,
                                                                                     subtile_x,
                                                                                     subtile_y)

                subtile_cataloguepath_before = '%ssubtile_%02d_%02d.before.asc' \
                                               % (subtile_directory,
                                                  subtile_x,
                                                  subtile_y)

                subtile_cataloguepath = '%ssubtile_%02d_%02d.asc' % (subtile_directory,
                                                                     subtile_x,
                                                                     subtile_y)

                subtile_tablepath = '%ssubtile_%02d_%02d.table.fits' % (subtile_directory,
                                                                        subtile_x,
                                                                        subtile_y)

                subtile_headpath = '%ssubtile_%02d_%02d.head' % (subtile_directory,
                                                                 subtile_x,
                                                                 subtile_y)
                start_stacking = 1
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

                    # print '    offsets for branch are (%f, %f) ' % (subfield.offset_x,
                    #                                                 subfield.offset_y)

                    # get the stars in that specific tile.
                    stars_in_tile = get_starfield_images_tile_offset(subfield.starfield_catalogue,
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
                                                                     1)
                    # pick a number of stars from a random distribution.
                    # stars_in_subtile = random.sample(stars_in_subtile, 10)

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

                print '    stacking complete %d total stars' % len(stacked_stars)
                global_tile_count += len(stacked_stars)
                # # display the tile
                #print len(stacked_stars)
                # display_tile(stacked_stars, 1)
                #exit(0)

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
                subtile.tile_size = SUBTILE_SIZE

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
                                 'subtile_%02d_%02d' % (subtile_x, subtile_y))

                os.remove(subtile_imageplaceholder)
                global_tile_stars += stacked_stars
                print '    --------------------------------------'
        print '  global tile count : %d [%d]\n' % (global_tile_count, len(global_tile_stars))
        global_tile_stars.sort(key=lambda tup: (tup[6], tup[7]))
        save_catalogue(global_tile_stars,
                       '%sglobal_positions.asc' % tile_directory)
        print '  --------------------------------------'

