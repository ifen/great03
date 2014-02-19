__author__ = 'Ian Fenech Conti'

from galaxy_prep.convert_xy import *
from galaxy_prep.prepare_header import *
from galaxy_prep.set_tabledata import *
from galaxy_prep.write_headfile import *
from galaxy_prep.pad_image import *
from galaxy_prep.package_results import *
from galaxy_prep.tile_image import *
from star_prep.crop_psf import *

import os
import datetime
import time

# DEFINE RUNTIME PROCEDURES
file_handling = 1
lensfit_run = 1
exec_run = 1
lensfit_read = 1
run_plots = 1

# START TIMER
time_start = time.time()

# SET ROOT PATHS FOR G3 AND LENSFIT
great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Documents/LENSFIT/'

# SET BRANCH FOLDER AND BRANCH TYPE
great3_branch = '0/'
great3_branch = great3_folder_root + great3_branch
great3_branch_type = 'standard_non_tiled/'
great3_branch_type = great3_branch + great3_branch_type

# SET PREP/OUTPUT FOLDERS
great3_prep = great3_branch_type + 'prep/'
great3_out = great3_branch_type + 'out/'

# SET TILE FOLDER
great3_tile = great3_prep + ''

# SET LENSIFT SOURCE FOLDER
lensfit_source = lensfit_folder_root + 'src/'

# SET PATH TO SWARP FILE
path_swarp = 'swarp/create_coadd_swarp.swarp'

# SETUP LENSFIT ARGUMENT FILES
args_input_name = 'file_list.asc'
date_time = datetime.datetime.now()
date_time_string = date_time.strftime("%d.%m.%y.%I.%M.%S")
args_output_name = 'output.' + date_time_string + '.fits'
args_output_read_name = 'output.' + date_time_string + '.asc'

# SET PATHS TO INPUT DATA
path_dither = great3_branch + 'epoch_dither-000-0.txt'
path_offsets = great3_branch + 'subfield_offset-000.txt'
path_catalogue = great3_branch + 'galaxy_catalog-000.fits'
path_original_starfield = great3_branch + 'starfield_image-000-0.fits'
path_original = great3_branch + 'image-000-0.fits'

# DEFINE ITEM NAMES TO SAVE
image_name = 'image0'
catalogue_name = 'catalog0'
starfield_name = 'starfield0'

# SET SAVE PATHS FOR PREP. ITEMS
path_padded = great3_prep + image_name + '.pad.fits'
path_new = great3_prep + image_name + '.fits[0]'
path_save = great3_prep + image_name + '.fits'
path_coeff = great3_prep + image_name + '.psfcoeffs.fits'
path_catalogue_deg = great3_prep + catalogue_name + '.fits'
path_catalogue_deg_asc = great3_prep + image_name + '.asc'
path_asc = great3_prep + image_name + '.asc'
path_headfile = great3_prep + image_name + '.head'
path_save_starfield = great3_prep + starfield_name + '.crop.fits'
path_imagefilelist = great3_prep + args_input_name

# DEFINE RUNTIME PARAMATERS
pad_size = 0
crop_size = 48
use_tiles = 0

# BUILD PSF COEFF EXEC
psfcoeff_args = './psfimage2coeffs ' + path_save_starfield + ' ' + path_coeff

# RUN LENSFIT COMMAND EXEC
args_input = great3_prep + args_input_name
args_output = great3_out + args_output_name
args_extra = '48 1 25 21. 24.'
lensfit_args = './flensfit'
lensfit_args += ' ' + args_input + ' ' + args_output + ' ' + args_extra

# RUN LENSFIT READ RESULTS EXEC
readlensfit_args = './readlensfit'
args_input_read = great3_out + args_output_name
args_output_read = great3_out + args_output_read_name
readlensfit_args += ' ' + args_input_read + ' ' + args_output_read

# SETUP ENVIRONMENT DATA
envdata_datadir = great3_prep
envdata_headdir = great3_prep
envdata_psfdir = great3_prep
envdata_cataloguedir = path_catalogue_deg_asc
envdata_swarpconfig = lensfit_folder_root + path_swarp

if file_handling:
    # FILE HANDLING
    if not os.path.isdir(great3_branch_type):
        print 'prep dir does not exist\n'
        print 'creating prep dir\n'
        os.makedirs(great3_prep)

    if not os.path.isdir(great3_prep):
        print 'prep dir does not exist\n'
        print 'creating prep dir\n'
        os.makedirs(great3_prep)

    if not os.path.isdir(great3_tile):
        print 'tile dir does not exist\n'
        print 'creating tile dir\n'
        os.makedirs(great3_tile)

    if not os.path.isdir(great3_out):
        print 'out dir does not exist\n'
        print 'creating out dir\n'
        os.makedirs(great3_out)

if lensfit_run:
    # START THE CONVERSION CODE

    # log the start time.
    print 'lensfit run started at : ' + str(datetime.datetime.now())

    # remove the previous prep. data from the
    # folder and replace with new data.
    os.chdir(great3_prep)
    os.system('rm -f *')

    # crop the perfectly centered PSF from the starfield
    # postagestamp and save it.
    crop_psf(path_original_starfield,
             path_save_starfield,
             crop_size)

    # pad the image in order to cater for galaxies on the
    # edges. padding will be 0 values.
    pad_image(path_original, path_padded, pad_size)

    # prepare header with the correct WCS values
    prepare_header(path_offsets, path_dither,
                   path_padded, path_save)

    # re-write the table data to match centroid
    # this caters for the G3 conventions
    set_tabledata(path_catalogue,
                  path_catalogue_deg, pad_size)

    # convert cords. from pixel to dec/ra and save.
    convert(path_new,
            path_catalogue_deg,
            path_asc,
            False)

    if use_tiles:
        # write the tile names acii file with the image name.
        tile_names = tile_image(path_save,
                                great3_tile,
                                'ground')
        write_imagefile_tiles(path_imagefilelist,
                              tile_names)
        write_headfile_tiles(great3_tile,
                             tile_names)
    else:
        # write the acii file with the image name.
        write_imagefile(path_imagefilelist,
                        image_name)
         # write lensift's .head file with WCS props.
        write_headfile(path_headfile, path_save)

    if exec_run:
        # DEBUGGING THE FILENAMES/ EXEC PATHS
        print 'debugging args\n'
        print lensfit_args
        print readlensfit_args
        print psfcoeff_args

        print '\n\ndebugging env_variables\n'
        print envdata_datadir
        print envdata_headdir
        print envdata_psfdir
        print envdata_cataloguedir
        print envdata_swarpconfig

        # RUN LENSFIT
        print '\n\npreparing to start lensfit\n'

        os.chdir(great3_folder_root + '/utils/')
        if use_tiles:
            for tile_name in tile_names:
                tile_name_path = '%s/%s.psfcoeffs.fits' % \
                                 (great3_tile,
                                  tile_name)
                psfcoeff_args = './psfimage2coeffs ' + path_save_starfield + ' ' + tile_name_path
                os.system(psfcoeff_args)
        else:
            os.system(psfcoeff_args)

        os.chdir(lensfit_source)

        # write environment variables to system os
        # lensift needs these in order to run.
        os.environ['SWARP_CONFIG'] = envdata_swarpconfig
        os.environ['HEAD_DIR'] = envdata_headdir
        os.environ['PSF_DIR'] = envdata_psfdir
        os.environ['CATALOGUE_GALAXIES'] = envdata_cataloguedir
        os.environ['DATA_DIR'] = envdata_datadir

        os.system(lensfit_args)

if lensfit_read:
    # CONVERT OUTPUTS TO ASCII TABLE
    os.system(readlensfit_args)

# END TIMER
time_end = time.time()
time_length = time_end - time_start

m, s = divmod(time_length, 60)
h, m = divmod(m, 60)
run_time = "%d:%02d:%d" % (h, m, s)

print 'lensfit run-time was : ' + run_time

if run_plots:
    # PLOT THE RESULTS FOR ANALYSIS
    results_path = args_output_read
    # results_path = '/home/ian/Documents/GREAT03/0/deep/out/output.17.02.14.09.12.12.asc'

    plot_path = great3_out+date_time_string + '/'
    os.makedirs(plot_path)

    path_1 = plot_attribute(results_path,
                            'E1', 'E2', plot_path)
    path_2 = plot_attribute(results_path,
                            'SCALE_LENGTH', 'MEAN_LIKELIHOOD_E', plot_path)
    path_3 = plot_attribute(results_path,
                            'MODEL_SN_RATIO', 'SCALE_LENGTH', plot_path)
    path_4 = plot_attribute(results_path,
                            'MODEL_SN_RATIO', 'BULGE_FRACTION', plot_path)

    proc_galaxies = processed_galaxies(results_path)

    # body_of_email can be plaintext or html!
    content = "\r\n\r\n" + 'Dear Ian, <br /><br />'  \
              'Your Lensfit Run Has Completed with ID (' + date_time_string + ').<br />' \
              'No. Processed Galaxies : ' + str(proc_galaxies) + '<br />' \
              'Execution Time Was : ' + run_time + '<br /><br />' \
              'Best Regards,<br /><br />Lensfit Bot'

    email_results('Lensifit Run (' + date_time_string + ') Complete',
                  'ianfc89@gmail.com',
                  'ianfc89@gmail.com',
                  content,
                  [path_1,
                  path_2,
                  path_3,
                  path_4])

    # plt.show()
    # raw_input("Press Enter to close...")




