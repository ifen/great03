__author__ = 'Ian Fenech Conti'

import os
import numpy as np
import matplotlib.pyplot as plt

LENSFIT_PATH = '/home/ian/Documents/LENSFIT/'
LENSFIT_SRC = '%ssrc/' % LENSFIT_PATH
ROOT_PATH = '/home/ian/Documents/LENSFIT/'
BRANCH_PATH = 'TAMAL/5/'
FILE_NAME = 'starfield_image-'
SAMPLE_HEADER = '%s%s000/data_test_tiled/prep/image0.fits' \
                % (ROOT_PATH, BRANCH_PATH)

NO_THREADS = 6

PROCESS_START = 0
PROCESS_FINISH = 1

TILE_SIZE = 2
TILES_IMAGE = int(10./TILE_SIZE)

SUBTILE_SIZE = 0.5
SUBTILE_IMAGE = int(TILE_SIZE/SUBTILE_SIZE)
SUBTILE_OVERLAP = 0.08

FIT_ORDER = 3
SNR_RATIO = 30


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

subtile_list = []
global_results = []
x_val = []
y_val = []

for ID in range(PROCESS_START, PROCESS_FINISH):
    branch_path = '%s%sstarfield-%03d/' % \
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
                    subtile = StarfieldSubtile(sub_subdirectory, subtile_x, subtile_y)
                    print subtile.path
                    print subtile.tile_x
                    print subtile.tile_y
                    subtile_list.append(subtile)

for subtile_results in subtile_list:
    data_table = np.genfromtxt('%s%d%d_ellipticities.log' % (subtile_results.path,
                                                             subtile_results.tile_x,
                                                             subtile_results.tile_y),
                               dtype=None)
    global_results += data_table
    for entry in data_table:

        x_val.append(entry[6])
        y_val.append(entry[10])

x_val = np.array(x_val)
y_val = np.array(y_val)

plt.figure()
plt.title('Starfield - True Gridded Star Positions')
plt.scatter(x_val, y_val, marker='.')
plt.show()

print np.sqrt(((x_val - y_val) ** 2).mean(axis=None))