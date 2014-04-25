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

from galaxy_prep.convert_xy import *
from galaxy_prep.prepare_header import *
from galaxy_prep.set_tabledata import *
from galaxy_prep.write_headfile import *
from galaxy_prep.pad_image import *
from galaxy_prep.package_results import *
from galaxy_prep.tile_image import *
from star_prep.crop_psf import *

# define the folder paths
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/variable_psf/ground/constant/'
DATA_PATH = '%s%s' % (ROOT_PATH, BRANCH_PATH)

# save directory
INSTANCE_NAME = 'VPGGc_1'

SAMPLE_HEADER = '%sutils/sample.fits' \
                % ROOT_PATH

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)

POSTAGE_SIZE = 48

DEEP_DATA = 0

if DEEP_DATA == 1:
    FILE_NAME = 'deep_image-'
else:
    FILE_NAME = 'image-'

if len(sys.argv) < 3:
    print 'not enough args passed. run : python psf_data_stacked.py [START] [END]'
    exit()

# disable all warnings
warnings.filterwarnings("ignore")

FIELD_START = int(sys.argv[1])
FIELD_END = int(sys.argv[2])

plt.figure(num=None, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='r')

for FIELD_ID in range(FIELD_START, FIELD_END):

    if DEEP_DATA == 1:
        # PREPARE THE INPUT PATHS
        image_path = '%s%s%03d-0.fits' % (DATA_PATH, FILE_NAME, FIELD_ID)
        catalogue_path = '%sdeep_galaxy_catalog-%03d.fits' % (DATA_PATH, FIELD_ID)
        offsets_path = '%sdeep_subfield_offset-%03d.txt' % (DATA_PATH, FIELD_ID)
        dither_path = '%sdeep_epoch_dither-%03d-0.txt' % (DATA_PATH, FIELD_ID)

        # PREPARE SAVE PATHS
        save_directory = '%s%s/deep_%03d/' % (DATA_PATH, INSTANCE_NAME, FIELD_ID)

        if os.path.isdir(save_directory):
            shutil.rmtree(save_directory)
        os.mkdir(save_directory)

        print '  loading subfield : %03d' % FIELD_ID,
        sys.stdout.flush()
    else:
        # PREPARE THE INPUT PATHS
        image_path = '%s%s%03d-0.fits' % (DATA_PATH, FILE_NAME, FIELD_ID)
        catalogue_path = '%sgalaxy_catalog-%03d.fits' % (DATA_PATH, FIELD_ID)
        offsets_path = '%ssubfield_offset-%03d.txt' % (DATA_PATH, FIELD_ID)
        dither_path = '%sepoch_dither-%03d-0.txt' % (DATA_PATH, FIELD_ID)

        # PREPARE SAVE PATHS
        save_directory = '%s%s/%03d/' % (DATA_PATH, INSTANCE_NAME, FIELD_ID)

        if os.path.isdir(save_directory):
            shutil.rmtree(save_directory)
        os.mkdir(save_directory)

        print '  loading subfield : %03d' % FIELD_ID,
        sys.stdout.flush()

    image_data = load_grid_image(image_path)
    galaxy_catalogue = get_starfield_catalogue_data(catalogue_path)

    print ' [ %s ]' % u'\u2713'
    sys.stdout.flush()

    # prepare header with the correct WCS values
    whole_image = '%s%03d.fits' % (save_directory, FIELD_ID)
    whole_image_convert = '%s[0]' % whole_image
    whole_table = '%s%03d.table.fits' % (save_directory, FIELD_ID)
    whole_asc = '%s%03d.asc' % (save_directory, FIELD_ID)
    whole_input = '%sinput.asc' % save_directory

    offsets = np.genfromtxt(offsets_path, dtype=None)
    offset_x = offsets[0]
    offset_y = offsets[1]

    # offset_x = 0
    # offset_y = 0

    prepare_header_offset(offsets_path, dither_path, image_path, whole_image, 0, 0)
    if DEEP_DATA == 1:
        set_tabledata_offset_deep(catalogue_path, whole_table, offset_x, offset_y)
    else:
        set_tabledata_offset(whole_table, galaxy_catalogue)

    convert(whole_image_convert, whole_table, whole_asc, True)

    input_list = []

    for tile_x in range(0, TILES_IMAGE):
        for tile_y in range(0, TILES_IMAGE):

            tile_directory = '%s%02d_%02d/' % (save_directory,
                                               tile_x,
                                               tile_y)

            print '  preparing GALAXY data for tile (%d, %d) ' % (tile_x, tile_y)
            print '  --------------------------------------'
            sys.stdout.flush()

            for subtile_x in range(0, SUBTILE_IMAGE):
                for subtile_y in range(0, SUBTILE_IMAGE):
                    print '    processing subtile (%d, %d) (%d, %d) ' % (tile_x, tile_y, subtile_x, subtile_y),
                    sys.stdout.flush()

                    subtile_directory = save_directory

                    if DEEP_DATA == 0:
                        file_name = 'subtile%02d%02d%02d%02d%02d' % ((FIELD_ID / 20),
                                                                     tile_x,
                                                                     tile_y,
                                                                     subtile_x,
                                                                     subtile_y)
                    else:
                        file_name = 'subtile%02d%02d%02d%02d%02d' % (FIELD_ID,
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

                    subtile_truth = '%s%s.include.asc' % (subtile_directory,
                                                          file_name)
                    if DEEP_DATA == 0:
                        galaxy_tile = get_galaxy_images_tile(galaxy_catalogue,
                                                             tile_x,
                                                             tile_y)

                        galaxy_subtile = get_galaxy_images_sub_tile(galaxy_tile,
                                                                    tile_x,
                                                                    tile_y,
                                                                    subtile_x,
                                                                    subtile_y,
                                                                    TILE_SIZE,
                                                                    SUBTILE_SIZE)
                    else:
                        galaxy_subtile = get_deep_galaxy_images_sub_tile(galaxy_catalogue,
                                                                         tile_x,
                                                                         tile_y,
                                                                         subtile_x,
                                                                         subtile_y,
                                                                         TILE_SIZE,
                                                                         SUBTILE_SIZE)

                    x_start_deg = (((tile_x * TILE_SIZE) + (subtile_x * SUBTILE_SIZE)) * 4800) / 10
                    x_end_deg = (((tile_x * TILE_SIZE) + (subtile_x * SUBTILE_SIZE) + SUBTILE_SIZE) * 4800) / 10

                    y_start_deg = (((tile_y * TILE_SIZE) + (subtile_y * SUBTILE_SIZE)) * 4800) / 10
                    y_end_deg = (((tile_y * TILE_SIZE) + (subtile_y * SUBTILE_SIZE) + SUBTILE_SIZE) * 4800) / 10

                    crop = image_data[y_start_deg:y_end_deg, x_start_deg:x_end_deg]

                    save_grid(image_path,
                              subtile_imagepath,
                              crop)

                    set_header_data_galaxy(subtile_imagepath,
                                           tile_x, tile_y,
                                           subtile_x, subtile_y,
                                           offset_x, offset_y,
                                           SAMPLE_HEADER)

                    write_headfile_star(subtile_headpath,
                                        subtile_imagepath)

                    input_list.append(file_name)

                    fo = open(subtile_truth, "wb")
                    for galaxy in galaxy_subtile:
                        # if int(galaxy[2]) == 200024023:
                        #     print '\n%d %d %d %d' % (tile_x, tile_y, subtile_x, subtile_y)
                        #     exit()
                        fo.write('%d\n' % galaxy[2])
                    fo.close()
                    print ' [ %s ]' % u'\u2713'
                    sys.stdout.flush()

    fo = open(whole_input, "wb")
    for f_name in input_list:
        fo.write('%s\n' % f_name)
    fo.close()
