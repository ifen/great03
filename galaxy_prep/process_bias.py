__author__ = 'Ian Fenech Conti'

import os

RANGE_START = 0
RANGE_END = 200

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Downloads/correction_code/'


for ID in range(RANGE_START, RANGE_END):
    asci_path = '%soutputs_final/%d/final.asc' % (great3_folder_root, ID)
    log_path = '%soutputs_final/%d/out.log' % (great3_folder_root, ID)

    readlensfit_args = './applyG3noisebias %s /home/ian/Downloads/correction_code/alphabeta7.dat > %s' % (asci_path, log_path)
    print readlensfit_args

    os.chdir(lensfit_folder_root)
    os.system(readlensfit_args)