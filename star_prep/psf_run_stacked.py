__author__ = 'Ian Fenech Conti'

import os
import sys
import shutil
import Queue
from threading import Thread, current_thread
from time import gmtime, strftime, localtime

LENSFIT_PATH = '/home/ian/Documents/LENSFIT/'
LENSFIT_SRC = '%ssrc/' % LENSFIT_PATH
ROOT_PATH = '/home/ian/Documents/GREAT03/'
BRANCH_PATH = 'branch/variable_psf/ground/constant/'
INSTANCE_NAME = 'VPGc_1'

if len(sys.argv) == 7:
    FIELD_ID = int(sys.argv[1])
    TILE_X_START = int(sys.argv[2])
    TILE_Y_START = int(sys.argv[3])
    TILE_END = int(sys.argv[4])
    NO_THREADS = int(sys.argv[5])
    FIT_ORDER = int(sys.argv[6])
else:
    print 'not enough args passed. run : python psf_run_stacked.py [FIELD_ID] [TILE_X_START] [TILE_Y_START] [TILE_END] [NO_THREADS] [FIT_ORDER]'
    exit()

SNR_RATIO = 230

#print '\n\n  psf run configured with %d threads' % NO_THREADS
#print '  SNR of %d \n\n' % SNR_RATIO

#PROCESS_START = 0
#PROCESS_FINISH = 0

TILE_SIZE = 2
TILES_IMAGE = int(10. / TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE / SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.09

q = Queue.Queue()


class StarfieldSubtile:
    def __init__(self, path, _field_ID, _tile_x, _tile_y, _sub_tile_x, _sub_tile_y):
        self.data = []
        self.save_file_name = 'subtile_%02d_%02d_%02d_%02d_%02d' % (_field_ID,
                                                                _tile_x,
                                                                _tile_y,
                                                                _sub_tile_x,
                                                                _sub_tile_y)
        self.tile_x = _tile_x
        self.tile_y = _tile_y
        self.tile_id = '%s' % self.save_file_name
        self.tile_size = SUBTILE_SIZE
        self.path = path
        self.file_list = '%sinput.asc' % path
        self.image_path = '%s%s.fits' % (path,
                                         self.save_file_name)
        self.catalogue_path = '%s%s.asc' % (path,
                                            self.save_file_name)
        self.log_path = '%s%s.log' % (path,
                                      self.save_file_name)
        if os.path.isfile('%s%s.log' % (path,
                                        self.save_file_name)):
            os.remove('%s%s.log' % (path,
                                    self.save_file_name))


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
        # print makeopsf_exec
        print '      --------------------------------------\n      in thread : %s starting run on %s\n\n' % (current_thread().name,subtile_object.tile_id)

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

        print '      in thread : %s run complete on %s\n' % (current_thread().name,
                                                             subtile_object.tile_id)

        q.task_done()


print '--------------------------------------'
print ' preparing PSF modelling run for field : %d \n  instance name : %s\n  runtime paramaters\n     [tile start : %d\n      tile length : %d\n      threads : %d\n      SNR : %d]\n' % (
    FIELD_ID, INSTANCE_NAME, TILE_X_START, TILE_END, NO_THREADS, SNR_RATIO)

for ID in range(FIELD_ID, FIELD_ID + 1):
    branch_path = '%s%s%s/%02d/' % \
                  (ROOT_PATH,
                   BRANCH_PATH,
                   INSTANCE_NAME,
                   ID)
    for tile_x in range(TILE_X_START, TILE_X_START + TILE_END):
        for tile_y in range(TILE_Y_START, TILE_Y_START + 1):
            sub_directory = '%s%02d_%02d/' % \
                            (branch_path,
                             tile_x,
                             tile_y)
            for subtile_x in range(0, SUBTILE_IMAGE):
                for subtile_y in range(0, SUBTILE_IMAGE):
                    sub_subdirectory = '%s%02d_%02d/' % \
                                       (sub_directory,
                                        subtile_x,
                                        subtile_y)
                    subtile = StarfieldSubtile(sub_subdirectory, FIELD_ID, tile_x, tile_y, subtile_x, subtile_y)
                    print '    %s' % subtile.tile_id
                    q.put(subtile)
            print '    ---------------------------------'

print '    --------------------------------------'
print '    preparing threaded run'
print strftime("    started at : %H:%M:%S %Y-%m-%d\n", localtime())

#for i in range(NO_THREADS):
#    t = Thread(target=makeospsf)
#    t.daemon = True
#    t.start()

#q.join()

print '    --------------------------------------'
print '    run complete'
print strftime("    finished at : %H:%M:%S %Y-%m-%d\n", localtime())


