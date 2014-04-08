__author__ = 'Ian Fenech Conti'

import os

RANGE_START = 0
RANGE_END = 200

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Documents/LENSFIT/src'


for ID in range(RANGE_START, RANGE_END):
    great3_out = great3_folder_root + 'outputs/%d/' % ID
    great3_save = great3_folder_root + 'outputs_final/%d/' % ID
    table_name = [each for each in os.listdir(great3_out) if each.endswith('.fits')]

    readlensfit_args = './readlensfit %s%s %sfinal.asc' % (great3_out, table_name[0], great3_save)

    os.chdir(lensfit_folder_root)
    os.system(readlensfit_args)
