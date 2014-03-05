__author__ = 'Ian Fenech Conti'

import shutil
import copy

from star_prep.psf_handler import *
from star_prep.tiling_handler import *

# define the folder paths
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'variable_psf/ground/constant/'
FILE_NAME = 'starfield_image-'

SAMPLE_HEADER = '%s%s000/data_test_tiled/prep/image0.fits' \
                % (ROOT_PATH, BRANCH_PATH)
PROCESS_START = 0
PROCESS_FINISH = 1

TILE_SIZE = 2
TILES_IMAGE = int(10./TILE_SIZE)

SUBTILE_SIZE = 1
SUBTILE_IMAGE = int(TILE_SIZE/SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.1

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
    starfield_image.file_name = '%s%03d-0.fits' % (FILE_NAME, ID)
    starfield_image.file_path = '%s%s' % (branch_collection.branch_path,
                                          starfield_image.file_name)
    starfield_image.catalogue_path = '%sstar_catalog-%03d.fits' % (branch_collection.branch_path,
                                                                   ID)
    starfield_image.image_data = load_grid_image(starfield_image.file_path)

    branch_collection.images.append(starfield_image)

for starfield_image in branch_collection.images:

    sub_directory = '%sstarfield--%03d/' % (branch_collection.branch_path,
                                            starfield_image.image_id)

    if os.path.isdir(sub_directory):
        shutil.rmtree(sub_directory)

    os.mkdir(sub_directory)
    starfield_image.tile_path = sub_directory

    for tile_x in range(0, 1):
        for tile_y in range(0, 1):

            starfield_tile = StarfieldTile()
            starfield_tile.tile_x = tile_x
            starfield_tile.tile_y = tile_y
            starfield_image.tiles.append(starfield_tile)

    for starfield_tile in starfield_image.tiles:

        tile_directory = '%s%d%d/' % (starfield_image.tile_path,
                                      starfield_tile.tile_x,
                                      starfield_tile.tile_y)

        starfield_tile.path = tile_directory

        if os.path.isdir(tile_directory):
            shutil.rmtree(tile_directory)

        os.mkdir(tile_directory)

        # extract each of the star tiles per/image
        starfield_tile.stars_in_tile = get_starfield_images_tile(starfield_image.catalogue_path,
                                                                 starfield_tile.tile_x,
                                                                 starfield_tile.tile_y)

        # extract the sub-tiles for each tile
        for subtile_x in range(0, SUBTILE_IMAGE):
            for subtile_y in range(0, SUBTILE_IMAGE):

                starfield_subtile = StarfieldSubtile()
                starfield_subtile.tile_x = subtile_x
                starfield_subtile.tile_y = subtile_y
                starfield_subtile.tile_size = SUBTILE_SIZE
                starfield_tile.subtiles.append(starfield_subtile)

        # set the subtiles paths
        for starfield_subtile in starfield_tile.subtiles:

            subtile_directory = '%s%d%d/' % (starfield_tile.path,
                                             starfield_subtile.tile_x,
                                             starfield_subtile.tile_y)

            subtile_imagepath = '%s%d%d.fits' % (subtile_directory,
                                                 starfield_subtile.tile_x,
                                                 starfield_subtile.tile_y)

            subtile_imageplaceholder = '%s%d%d.placeholder.fits' % (subtile_directory,
                                                                    starfield_subtile.tile_x,
                                                                    starfield_subtile.tile_y)

            subtile_cataloguepath_before = '%s%d%d.before.asc' \
                                           % (subtile_directory,
                                              starfield_subtile.tile_x,
                                              starfield_subtile.tile_y)

            subtile_cataloguepath = '%s%d%d.asc' % (subtile_directory,
                                                    starfield_subtile.tile_x,
                                                    starfield_subtile.tile_y)

            subtile_tablepath = '%s%d%d.table.fits' % (subtile_directory,
                                                       starfield_subtile.tile_x,
                                                       starfield_subtile.tile_y)

            subtile_headpath = '%s%d%d.head' % (subtile_directory,
                                                starfield_subtile.tile_x,
                                                starfield_subtile.tile_y)

            starfield_subtile.directory = subtile_directory
            starfield_subtile.image_path = subtile_imagepath
            starfield_subtile.image_placeholder = subtile_imageplaceholder
            starfield_subtile.catalogue_path_before = subtile_cataloguepath_before
            starfield_subtile.catalogue_path = subtile_cataloguepath
            starfield_subtile.table_path = subtile_tablepath
            starfield_subtile.head_path = subtile_headpath

            if os.path.isdir(subtile_directory):
                shutil.rmtree(subtile_directory)

            os.mkdir(subtile_directory)

            starfield_subtile.stars_in_subtile = \
                get_starfield_images_sub_tile(starfield_tile.stars_in_tile,
                                              starfield_tile,
                                              starfield_subtile,
                                              SUBTILE_OVERLAP)

            starfield_subtile.image_data, starfield_subtile.stars_in_subtile\
                = regrid_tile(starfield_image.image_data,
                              starfield_subtile.stars_in_subtile,
                              POSTAGE_SIZE)

            save_grid(starfield_image.file_path,
                      starfield_subtile.image_path,
                      starfield_subtile.image_data)

            save_catalogue(starfield_subtile.stars_in_subtile,
                           starfield_subtile.catalogue_path_before)

            save_fitstable(starfield_subtile.table_path,
                           starfield_subtile.stars_in_subtile)

            set_header_data(starfield_tile,
                            starfield_subtile,
                            SAMPLE_HEADER)

            set_placeholder(starfield_subtile)

            convert_positions('%s[0]' % starfield_subtile.image_placeholder,
                              starfield_subtile.table_path,
                              starfield_subtile.catalogue_path)

            write_headfile_star(starfield_subtile.head_path,
                                starfield_subtile.image_path)

            write_input_file('%sinput.asc' % subtile_directory,
                             '%d%d' % (starfield_subtile.tile_x, starfield_subtile.tile_y))

