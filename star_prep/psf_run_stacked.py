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
BRANCH_PATH = 'branch/variable_psf/ground/constant/'
INSTANCE_NAME = 'VPGc_2'

if len(sys.argv) > 1:
    NO_THREADS = int(sys.argv[1])
    FIT_ORDER = int(sys.argv[2])
else:
    NO_THREADS = 8
    FIT_ORDER = 3

SNR_RATIO = 75

print '\n\n  psf run configured with %d threads' % NO_THREADS
print '  SNR of %d \n\n' % SNR_RATIO

PROCESS_START = 0
PROCESS_FINISH = 1

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.09

q = Queue.Queue()


class StarfieldSubtile:
    def __init__(self, path, _tile_x, _tile_y):
        self.data = []
        self.tile_x = _tile_x
        self.tile_y = _tile_y
        self.tile_id = 'subtile_%02d_%02d' % (_tile_x,
                                              _tile_y)
        self.tile_size = SUBTILE_SIZE
        self.path = path
        self.file_list = '%sinput.asc' % path
        self.image_path = '%ssubtile_%02d_%02d.fits' % (path,
                                                        _tile_x,
                                                        _tile_y)
        self.catalogue_path = '%ssubtile_%02d_%02d.asc' % (path,
                                                           _tile_x,
                                                           _tile_y)
        self.log_path = '%ssubtile_%02d_%02d.log' % (path,
                                                     _tile_x,
                                                     _tile_y)
        if os.path.isfile('%s%02d_%02d.log' % (path,
                                               _tile_x,
                                               _tile_y)):
            os.remove('%s%02d_%02d.log' % (path,
                                           _tile_x,
                                           _tile_y))


def makeospsf():
    while not q.empty():
        subtile_object = q.get()

        os.environ['SWARP_CONFIG'] = LENSFIT_PATH + 'swarp/create_coadd_swarp.swarp'

        makeopsf_exec = './makeospsf %s %d none %d %s %s %s %s > %s' % (subtile_object.file_list,
                                                                        FIT_ORDER,
                                                                        SNR_RATIO,
                                                                        subtile_object.path,
                                                                        subtile_object.catalogue_path,
                                                                        subtile_object.tile_id,
                                                                        subtile_object.path,
                                                                        subtile_object.log_path)

        print '    thread : %s starting run on %s\n' % (current_thread().name,
                                                        subtile_object.tile_id)

        os.chdir(LENSFIT_SRC)
        os.system(makeopsf_exec)

       	shutil.move('%s%s_ellipticities.log' % (LENSFIT_SRC,
                                                        subtile_object.tile_id),
                            '%s' % subtile_object.path)
        shutil.move('%s%s_shifts.log' % (LENSFIT_SRC,
                                                 subtile_object.tile_id),
                            '%s' % subtile_object.path)
        shutil.move('%s%s_stars.fits' % (LENSFIT_SRC,
                                                 subtile_object.tile_id),
                            '%s' % subtile_object.path)
       	shutil.move('%s%s_residuals.modelamp.fits' % (LENSFIT_SRC,
                                                             subtile_object.tile_id),
                            '%s' % subtile_object.path)
        shutil.move('%s%s_psf.fits' % (LENSFIT_SRC,
                                               subtile_object.tile_id),
                            '%s' % subtile_object.path)
       	shutil.move('%s%s_fracresiduals.fits' % (LENSFIT_SRC,
                                                         subtile_object.tile_id),
                            '%s' % subtile_object.path)

        print '    thread : %s run complete on %s\n' % (current_thread().name,
                                                                     subtile_object.tile_id)

        q.task_done()


for ID in range(PROCESS_START, PROCESS_FINISH):
    branch_path = '%s%s%s/%02d/' % \
                  (ROOT_PATH,
                   BRANCH_PATH,
                   INSTANCE_NAME,
                   ID)
    for tile_x in range(0, 1):
        for tile_y in range(0, 1):
            sub_directory = '%s%02d_%02d/' % \
                            (branch_path,
                             tile_x,
                             tile_y)
            for subtile_x in range(0, 1):
                for subtile_y in range(0, 1):
                    sub_subdirectory = '%s%02d_%02d/' % \
                                       (sub_directory,
                                        subtile_x,
                                        subtile_y)
                    subtile = StarfieldSubtile(sub_subdirectory, subtile_x, subtile_y)
                    q.put(subtile)

print '  starting stacked threaded run'
print strftime("  %Y-%m-%d %H:%M:%S\n\n", gmtime())

for i in range(NO_THREADS):
    t = Thread(target=makeospsf)
    t.daemon = True
    t.start()

q.join()

print '\n  all items processed'
print strftime("  %Y-%m-%d %H:%M:%S\n", gmtime())
