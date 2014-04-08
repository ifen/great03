__author__ = 'Ian Fenech Conti'

import os
import sys
import shutil
import Queue
from threading import Thread, current_thread
from time import gmtime, strftime


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

print '\n\n... configured with %d threads\n\n' % NO_THREADS

PROCESS_START = 0
PROCESS_FINISH = 5

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


        # def makeospsf():
        # tmp_env = os.environ
        # tmp_env['SWARP_CONFIG'] = LENSFIT_PATH + 'swarp/create_coadd_swarp.swarp'
        #
        # makeopsf_exec = './makeospsf %s %d none %d %s %s %s %s > %s' % (subtile_object.file_list,
        #                                                                 FIT_ORDER,
        #                                                                 SNR_RATIO,
        #                                                                 subtile_object.path,
        #                                                                 subtile_object.catalogue_path,
        #                                                                 subtile_object.tile_id,
        #                                                                 subtile_object.path,
        #                                                                 subtile_object.log_path)
        # os.chdir(LENSFIT_SRC)
        # os.system(makeopsf_exec)

        # shutil.move('%s%s_ellipticities.log' % (LENSFIT_SRC,
        #                                         subtile_object.tile_id),
        #             '%s' % subtile_object.path)
        # shutil.move('%s%s_shifts.log' % (LENSFIT_SRC,
        #                                  subtile_object.tile_id),
        #             '%s' % subtile_object.path)
        # shutil.move('%s%s_stars.fits' % (LENSFIT_SRC,
        #                                  subtile_object.tile_id),
        #             '%s' % subtile_object.path)
        # shutil.move('%s%s_residuals.modelamp.fits' % (LENSFIT_SRC,
        #                                               subtile_object.tile_id),
        #             '%s' % subtile_object.path)
        # shutil.move('%s%s_psf.fits' % (LENSFIT_SRC,
        #                                subtile_object.tile_id),
        #             '%s' % subtile_object.path)
        # shutil.move('%s%s_fracresiduals.fits' % (LENSFIT_SRC,
        #                                          subtile_object.tile_id),
        #             '%s' % subtile_object.path)

        # print '     ... (thread %s) run complete on %s\n' % (current_thread().name,
        #                                                      subtile_object.tile_id)


for ID in range(PROCESS_START, PROCESS_FINISH):
    branch_path = '%s%s/sanity_check/%d/' % \
                  (ROOT_PATH,
                   BRANCH_PATH,
                   ID)
    tmp_env = os.environ
    tmp_env['SWARP_CONFIG'] = LENSFIT_PATH + 'swarp/create_coadd_swarp.swarp'

    file_list = '%sinput.asc' % branch_path
    catalogue_path = '%simage0.asc' % branch_path
    log_path = '%s%03d.log' % (branch_path, ID)

    makeopsf_exec = './makeospsf %s 0 none %d %s %s image0 %s > %s' % (file_list,
                                                                     SNR_RATIO,
                                                                     branch_path,
                                                                     catalogue_path,
                                                                     branch_path,
                                                                     log_path)
    os.chdir(LENSFIT_SRC)
    os.system(makeopsf_exec)

    shutil.move('%simage0_ellipticities.log' % LENSFIT_SRC,
                '%s' % branch_path)
    shutil.move('%simage0_shifts.log' % LENSFIT_SRC,
                '%s' % branch_path)
    shutil.move('%simage0_stars.fits' % LENSFIT_SRC,
                '%s' % branch_path)
    shutil.move('%simage0_residuals.modelamp.fits' % LENSFIT_SRC,
                '%s' % branch_path)
    shutil.move('%simage0_psf.fits' % LENSFIT_SRC,
                '%s' % branch_path)
    shutil.move('%simage0_fracresiduals.fits' % LENSFIT_SRC,
                '%s' % branch_path)

print ' ... starting threaded run\n'
print strftime("%Y-%m-%d %H:%M:%S\n\n", gmtime())

print '\n   ... all items processed'
print strftime("  %Y-%m-%d %H:%M:%S\n", gmtime())