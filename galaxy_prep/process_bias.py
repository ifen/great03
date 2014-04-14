__author__ = 'Ian Fenech Conti'

import os

RANGE_START = 0
RANGE_END = 200

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Downloads/correction_code/'


for ID in range(RANGE_START, RANGE_END):
    root_path = '%sdata/outputs/%d/' % (great3_folder_root, ID)
    for file in os.listdir(root_path):
        if file.endswith(".asc"):
            asci_path = '%s%s' % (root_path, file)
            log_path = '%s/out2.log' % root_path
            readlensfit_args = './applyG3noisebias %s /home/ian/Downloads/correction_code/alphabeta7.dat > %s' % (asci_path, log_path)
            os.chdir(lensfit_folder_root)
            os.system(readlensfit_args)
            # b = os.path.getsize(asci_path)
            # print b
