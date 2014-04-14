__author__ = 'Ian Fenech Conti'

import os
import sys
import shutil
import Queue
from threading import Thread, current_thread
from time import gmtime, strftime

# APPEND THE GREAT03 CODE REPOSITORY
sys.path.append('/home/ian/Documents/GITHUB/great03/')

LENSFIT_PATH = '/home/ian/Documents/LENSFIT/'
LENSFIT_SRC = '%ssrc/' % LENSFIT_PATH
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/control/ground/constant/'
FILE_NAME = 'starfield_image-'

if len(sys.argv) > 1:
    NO_THREADS = 1
    FIT_ORDER = int(sys.argv[2])
else:
    NO_THREADS = 1
    FIT_ORDER = 3

PROCESS_START = 2
PROCESS_FINISH = 3

SAVE_TYPE = 'image0'

print '...starting PSF conversion range (%d, %d) with name : %s' % (PROCESS_START, PROCESS_FINISH, SAVE_TYPE)

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.09

SNR_RATIO = 30

q = Queue.Queue()


class StarfieldSubtile:
    def __init__(self, path, _tile_x, _tile_y):
        self.data = []
        self.tile_x = _tile_x
        self.tile_y = _tile_y
        self.tile_id = '%d%d' % (_tile_x,
                                 _tile_y)
        self.tile_size = SUBTILE_SIZE
        self.path = path
        self.file_list = '%sinput.asc' % path
        self.image_path = '%s%d%d.fits' % (path,
                                           _tile_x,
                                           _tile_y)
        self.catalogue_path = '%s%d%d.asc' % (path,
                                              _tile_x,
                                              _tile_y)
        self.log_path = '%s%d%d.log' % (path,
                                        _tile_x,
                                        _tile_y)
        if os.path.isfile('%s%d%d.log' % (path,
                                          _tile_x,
                                          _tile_y)):
            os.remove('%s%d%d.log' % (path,
                                      _tile_x,
                                      _tile_y))


for ID in range(PROCESS_START, PROCESS_FINISH):
    print '  processing image %d.' % ID
    branch_path = '%s%scontrol_ground_constant_run/%d/' % \
                  (ROOT_PATH,
                   BRANCH_PATH,
                   ID)
    tmp_env = os.environ
    tmp_env['SWARP_CONFIG'] = LENSFIT_PATH + 'swarp/create_coadd_swarp.swarp'

    file_list = '%sinput.asc' % branch_path
    catalogue_path = '%s%s.asc' % (branch_path, SAVE_TYPE)
    log_path = '%s%03d.log' % (branch_path, ID)

    makeopsf_exec = './makeospsf %s 0 none %d %s %s %s %s > %s' % (file_list,
                                                                     SNR_RATIO,
                                                                     branch_path,
                                                                     catalogue_path,
								     SAVE_TYPE,
                                                                     branch_path,
                                                                     log_path)
    os.chdir(LENSFIT_SRC)
    os.system(makeopsf_exec)

    shutil.move('%s%s_ellipticities.log' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    shutil.move('%s%s_shifts.log' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    shutil.move('%s%s_stars.fits' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    shutil.move('%s%s_residuals.modelamp.fits' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    shutil.move('%s%s_psf.fits' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    shutil.move('%s%s_fracresiduals.fits' % (LENSFIT_SRC,SAVE_TYPE),
                '%s' % branch_path)
    print '  psf model created.'

print '... psf model branch complete.'
