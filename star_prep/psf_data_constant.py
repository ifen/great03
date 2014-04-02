__author__ = 'Ian Fenech Conti'

import shutil
import copy

from star_prep.psf_handler import *
from star_prep.tiling_handler import *

# define the folder paths
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/control/ground/constant/'
FILE_NAME = 'starfield_image-'

SAMPLE_HEADER = '%sutils/sample.fits' \
                % ROOT_PATH
PROCESS_START = 0
PROCESS_FINISH = 1

POSTAGE_SIZE = 48

if len(sys.argv) < 1:
    print 'not enough args. passed to psf_pipeline'
    exit()

branch_collection = BranchCollection()
branch_collection.branch_path = '%s%s' % (ROOT_PATH, BRANCH_PATH)


def model_psf(package):
    for sub_tile in package:
        print sub_tile.image_path


for ID in range(PROCESS_START, PROCESS_FINISH):

    starfield_image = StarfieldImage()
    starfield_image.image_id = ID

    # file paths.
    starfield_image.file_name = '%s%03d-0.fits' % (FILE_NAME, ID)
    starfield_image.file_path = '%s%s' % (branch_collection.branch_path,
                                          starfield_image.file_name)
    starfield_image.catalogue_path = '%sstar_catalog-%03d.fits' % (branch_collection.branch_path,
                                                                   ID)
    starfield_image.image_data = load_grid_image(starfield_image.file_path)

    # save paths.
    save_directory = '%sstarfield-%03d/' % (branch_collection.branch_path,
                                            starfield_image.image_id)

    save_image = '%s%03d.fits' % (save_directory, starfield_image.image_id)

    save_catalogue_path_before = '%s%03d.before.asc' % (save_directory, starfield_image.image_id)

    save_catalogue_path = '%s%03d.asc' % (save_directory, starfield_image.image_id)

    save_table_path = '%s%03d.table.fits' % (save_directory, starfield_image.image_id)

    save_head_path = '%s%03d.head' % (save_directory, starfield_image.image_id)

    save_placeholder_path = '%s%03d.placeholder.fits' % (save_directory, starfield_image.image_id)

    branch_collection.images.append(starfield_image)

    # create save directory.
    if os.path.isdir(save_directory):
        shutil.rmtree(save_directory)

    os.mkdir(save_directory)

    # start the conversion process.

    # extract each of the star tiles per/image.
    stars_in_image = get_starfield_images_tile_constant(starfield_image.catalogue_path)
    print stars_in_image

    # regrid the tile.
    image_data, stars_in_image \
        = regrid_tile(starfield_image.image_data,
                      stars_in_image,
                      POSTAGE_SIZE)

    # save the new grid.
    save_grid(starfield_image.file_path,
              save_image,
              image_data)

    # save the catalogue.
    save_catalogue_constant(stars_in_image,
                            save_catalogue_path_before)

    # save the fits table for conversion.
    save_fitstable_constant(save_table_path,
                            stars_in_image)

    # load the fits placeholder.
    set_header_data_constant(save_image,
                             SAMPLE_HEADER)

    convert_positions('%s[0]' % save_image,
                      save_table_path,
                      save_catalogue_path)

    write_headfile_star(save_head_path,
                        save_image)

    write_input_file('%sinput.asc' % save_directory, '%03d' % starfield_image.image_id)



