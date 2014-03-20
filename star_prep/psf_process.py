__author__ = 'Ian Fenech Conti'

import os
import numpy as np
import matplotlib.pyplot as plt

LENSFIT_PATH = '/home/ian/Documents/LENSFIT/'
LENSFIT_SRC = '%ssrc/' % LENSFIT_PATH
ROOT_PATH = '/home/ian/Documents/LENSFIT/'
BRANCH_PATH = 'TAMAL/25/'
FILE_NAME = 'starfield_image-'
SAMPLE_HEADER = '%s%s000/data_test_tiled/prep/image0.fits' \
                % (ROOT_PATH, BRANCH_PATH)

NO_THREADS = 6

PROCESS_START = 0
PROCESS_FINISH = 1

TILE_SIZE = 2
TILES_IMAGE = int(10./TILE_SIZE)

SUBTILE_SIZE = 2
SUBTILE_IMAGE = int(TILE_SIZE/SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.09

FIT_ORDER = 0.5
SNR_RATIO = 30
RUN_TIME = '1:10'


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

subtile_list = []
global_results = []
e1_mod = []
e1_true = []
e2_mod = []
e2_true = []

for ID in range(PROCESS_START, PROCESS_FINISH):
    branch_path = '%s%sfield-%02d/' % \
                  (ROOT_PATH,
                   BRANCH_PATH,
                   ID)
    for tile_x in range(0, 1):
        for tile_y in range(0, 1):
            sub_directory = '%s%d%d/' % \
                            (branch_path,
                             tile_x,
                             tile_y)
            for subtile_x in range(0, SUBTILE_IMAGE):
                for subtile_y in range(0, SUBTILE_IMAGE):
                    sub_subdirectory = '%s%d%d/' % \
                                       (sub_directory,
                                        subtile_x,
                                        subtile_y)
                    # print sub_subdirectory
                    subtile = StarfieldSubtile(sub_subdirectory, subtile_x, subtile_y)
                    subtile_list.append(subtile)

for i, subtile_results in enumerate(subtile_list):
    file_name = '%s%d%d_ellipticities.log' % (subtile_results.path,
                                              subtile_results.tile_x,
                                              subtile_results.tile_y)

    data_table = np.genfromtxt(file_name,
                               dtype=None)

    global_results += data_table

    for j, entry in enumerate(data_table):

        e1_mod.append(entry[5])
        e1_true.append(entry[9])
        e2_mod.append(entry[6])
        e2_true.append(entry[10])

e1_mod = np.array(e1_mod)
e1_true = np.array(e1_true)
e2_mod = np.array(e2_mod)
e2_true = np.array(e2_true)

e1_error = np.sqrt(((e1_mod - e1_true) ** 2).mean(axis=None))
e2_error = np.sqrt(((e2_mod - e2_true) ** 2).mean(axis=None))

plt.figure(1)
plt.suptitle('Tile Size : %.2f, Overlap : %.2f, Order : %d, Run-Time : %s' %
             (SUBTILE_SIZE, SUBTILE_OVERLAP, FIT_ORDER, RUN_TIME), fontsize=18)

plt.subplot(121, aspect='equal')
plt.title('e1 RMSE : %.3e' % e1_error, fontsize=14)
plt.scatter(e1_mod, e1_true, marker='.', s=10, facecolors='black', edgecolors='none')

plt.subplot(122, aspect='equal')
plt.title('e2 RMSE : %.3e' % e2_error, fontsize=14)
plt.scatter(e2_mod, e2_true, marker='.', s=10, facecolors='black', edgecolors='none')

plt.show()
