__author__ = 'Ian Fenech Conti'

import shutil
import copy
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import warnings
import locale
import time

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
SUBTILE_OVERLAP = 0.05

POSTAGE_SIZE = 48
PADDING_SIZE = 10

if len(sys.argv) < 2:
    print 'not enough args passed. run : python psf_data_stacked.py [FIELD_ID]'
    exit()

# disable all warnings
warnings.filterwarnings("ignore")

FIELD_ID = int(sys.argv[1])
SUB_FIELDS = 20

FIELD_START = FIELD_ID * SUB_FIELDS
FIELD_END = (FIELD_ID * SUB_FIELDS) + SUB_FIELDS

branch_collection = BranchCollection()
branch_collection.branch_path = '%s%s' % (ROOT_PATH, BRANCH_PATH)

# create a new field class and assign the ID.
field = StarfieldField()
field.id = FIELD_ID

# append the field info. to the branch collection.
branch_collection.fields.append(field)

# save directory
instance_name = 'VPGc_1'
root_save_directory = '%s%s/' % (branch_collection.branch_path, instance_name)
#if os.path.isdir(root_save_directory):
#    shutil.rmtree(root_save_directory)
#os.mkdir(root_save_directory)

plt.figure(num=None, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='r')

print '--------------------------------------'
print 'preparing PSF data for field : %d \n  instance name : %s\n  overlap deg : %.3f' % (
    FIELD_ID, instance_name, SUBTILE_OVERLAP)

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
    print '  loading subfield : %03d' % ID,
    sys.stdout.flush()
    subfield.image_data = load_grid_image(subfield.file_path)
    subfield.starfield_catalogue = get_starfield_catalogue_data(subfield.catalogue_path)
    print ' [ %s ]' % u'\u2713'
    sys.stdout.flush()
    offsets = np.genfromtxt(subfield.offset_path,
                            dtype=None)

    # subfield.offset_x = offsets[0]
    # subfield.offset_y = offsets[1]
    subfield.offset_x = 0
    subfield.offset_y = 0

    # add the subfield to the field list
    field.subfields.append(subfield)

print '  catalog information loaded'
print '--------------------------------------\n'

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

time_start = time.time()

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
        #print '  save directory : %s' % tile_directory
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

                file_name = 'subtile_%02d_%02d_%02d_%02d_%02d' % (FIELD_ID,
                                                                  tile_x,
                                                                  tile_y,
                                                                  subtile_x,
                                                                  subtile_y)

                subtile_imagepath = '%s%s.fits' % (subtile_directory, file_name)

                subtile_imageplaceholder = '%s%s.placeholder.fits' % (subtile_directory,
                                                                      file_name)

                subtile_cataloguepath_before = '%s%s.before.asc' \
                                               % (subtile_directory,
                                                  file_name)

                subtile_cataloguepath = '%s%s.asc' % (subtile_directory,
                                                      file_name)

                subtile_tablepath = '%s%s.table.fits' % (subtile_directory,
                                                         file_name)

                subtile_headpath = '%s%s.head' % (subtile_directory,
                                                  file_name)
                start_stacking = 1
                stacked_stars = []
                stacked_image = np.zeros(shape=(0, 0))

                # go through each subfield across a field and get the resepective
                # subtile data.
                for subfield in field.subfields:
                    print '     subfield (%03d)' % subfield.image_id,
                    sys.stdout.flush()
                    tile = StarfieldTile()
                    tile.tile_x = tile_x
                    tile.tile_y = tile_y

                    subtile = StarfieldSubtile()
                    subtile.tile_x = subtile_x
                    subtile.tile_y = subtile_y
                    subtile.tile_size = SUBTILE_SIZE
                    stars_in_tile = []
                    stars_in_subtile = []

                    # print '    offsets for branch are (%f, %f) ' % (subfield.offset_x,
                    #                                                 subfield.offset_y)

                    # get the stars in that specific tile.
                    t0 = time.time()
                    stars_in_tile = get_starfield_images_tile_offset(subfield.starfield_catalogue,
                                                                     tile_x,
                                                                     tile_y,
                                                                     subfield.offset_x,
                                                                     subfield.offset_y)

                    # extract the stars from the tile into a sub-tile with an
                    # overlap.
                    t1 = time.time()
                    print ' %.3f' % (t1 - t0),
                    sys.stdout.flush()

                    stars_in_subtile = get_starfield_images_sub_tile(stars_in_tile,
                                                                     tile,
                                                                     subtile,
                                                                     SUBTILE_OVERLAP,
                                                                     1)

                    t2 = time.time()
                    print ' %.3f' % (t2 - t1),
                    sys.stdout.flush()

                    ## pick a number of stars from a random distribution.
                    ## stars_in_subtile = random.sample(stars_in_subtile, 20)

                    # # re-grid the stars we just extracted
                    # data = load_grid_image(subfield.file_path)
                    tmp_grid, tmp_layout = regrid_tile_stacked(subfield.image_data,
                                                               stars_in_subtile,
                                                               POSTAGE_SIZE,
                                                               stacked_image.shape[1])

                    t3 = time.time()
                    print ' %03.3f' % (t3 - t2),
                    sys.stdout.flush()

                    if start_stacking:
                        stacked_image = tmp_grid
                        start_stacking = 0
                    else:
                        stacked_image = numpy.concatenate((stacked_image, tmp_grid), axis=1)

                    stacked_stars += tmp_layout
                    print ' [ %s ]' % u'\u2713'
                    sys.stdout.flush()

                print '    stacking complete %s total stars' % ("{:,}".format(len(stacked_stars)))
                global_tile_count += len(stacked_stars)
                print '    sorting stacked stars'
                #stacked_stars.sort(key=lambda tup: (tup[4], tup[5]))
                ## display the tile
                #print len(stacked_stars)
                #display_tile(stacked_stars, 1)
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
                                 '%s' % file_name)

                # remove the unused files to save space
                os.remove(subtile_imageplaceholder)
                os.remove(subtile_tablepath)
                os.remove(subtile_cataloguepath_before)

                global_tile_stars += stacked_stars
                print '    --------------------------------------'

        print '  global tile count : %s [%s]' % (
            "{:,}".format(global_tile_count), "{:,}".format(len(global_tile_stars)))
        # global_tile_stars.sort(key=lambda tup: (tup[6], tup[7]))
        # save_catalogue(global_tile_stars,
        #                '%sglobal_positions.asc' % tile_directory)
        print '  --------------------------------------\n'

time_end = time.time()
print 'field conversion complete %.3f' % ((time_end - time_start) / 60)

