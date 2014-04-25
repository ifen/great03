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
import os

from star_prep.crop_psf import *

# define the folder paths
LENSFIT_ROOT = '/home/ian/Documents/LENSFIT/'
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/variable_psf/ground/constant/'
DATA_PATH = '%s%s' % (ROOT_PATH, BRANCH_PATH)
# save directory
INSTANCE_NAME = 'VPGGc_1'
PSF_INSTANCE_NAME = 'VPGPc_1'

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)

POSTAGE_SIZE = 48

DEEP_DATA = 1

if len(sys.argv) < 3:
    print 'not enough args passed. run : python galaxy_run_variable.py [START] [END]'
    exit()

# disable all warnings
warnings.filterwarnings("ignore")

FIELD_START = int(sys.argv[1])
FIELD_END = int(sys.argv[2])

for FIELD_ID in range(FIELD_START, FIELD_END):

    if DEEP_DATA == 0:
        # PREPARE THE INPUT PATHS
        output_folder = ROOT_PATH + 'VPGc_OUT/%03d/out/' % FIELD_ID

        # PREPARE SAVE PATHS
        data_directory = '%s%s/%03d/' % (DATA_PATH, INSTANCE_NAME, FIELD_ID)
        psf_directory = '%s%s/%02d/' % (DATA_PATH, PSF_INSTANCE_NAME, FIELD_ID)
    else:
        # PREPARE THE INPUT PATHS
        output_folder = ROOT_PATH + 'VPGc_OUT/deep_%03d/out/' % FIELD_ID

        # PREPARE SAVE PATHS
        data_directory = '%s%s/deep_%03d/' % (DATA_PATH, INSTANCE_NAME, FIELD_ID)
        psf_directory = '%s%s/deep_%02d/' % (DATA_PATH, PSF_INSTANCE_NAME, FIELD_ID)

    # input paths
    whole_asc = '%s%03d.asc' % (data_directory, FIELD_ID)
    whole_input = '%sinput.asc' % data_directory

    # if not os.path.isdir(output_folder):
    #     os.makedirs(output_folder)

    # LENSFIT STUFF
    lensfit_args = './flensfit'
    args_extra = '48 1 1'
    args_input_name = '%sinput.asc' % data_directory
    args_output_name = '%soutput_%03d.fits' % (output_folder, FIELD_ID)
    path_swarp = 'swarp/create_coadd_swarp.swarp'
    lensfit_run_args = '%s %s %s %s' % (lensfit_args, args_input_name, args_output_name, args_extra)
    print lensfit_run_args

    # SETUP ENVIRONMENT DATA
    envdata_datadir = data_directory
    envdata_headdir = data_directory
    envdata_psfdir = psf_directory
    envdata_cataloguedir = whole_asc
    envdata_swarpconfig = LENSFIT_ROOT + path_swarp

    print '\n\n  debugging env_variables\n'
    print envdata_datadir
    print envdata_headdir
    print envdata_psfdir
    print envdata_cataloguedir
    print envdata_swarpconfig

    os.chdir('%ssrc' % LENSFIT_ROOT)  # write environment variables to system os
    # lensift needs these in order to run.
    os.environ['SWARP_CONFIG'] = envdata_swarpconfig
    os.environ['HEAD_DIR'] = envdata_headdir
    os.environ['PSF_DIR'] = envdata_psfdir
    os.environ['CATALOGUE_GALAXIES'] = envdata_cataloguedir
    os.environ['DATA_DIR'] = envdata_datadir

    # os.system(lensfit_run_args)

