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
