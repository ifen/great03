__author__ = 'Ian Fenech Conti'

import os

RANGE_START = 0
RANGE_END = 200

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Documents/LENSFIT/src'


for ID in range(RANGE_START, RANGE_END):
    great3_out = great3_folder_root + 'data/submission_4/outputs/%d/' % ID
    great3_save = great3_folder_root + 'data/submission_4/outputs/%d/' % ID
    table_name = [each for each in os.listdir(great3_out) if each.endswith('.fits')]

    readlensfit_args = './readlensfit %s%s %sfinal2.asc' % (great3_out, table_name[0], great3_save)
    print '  running readlensfits for %s' % table_name

    os.chdir(lensfit_folder_root)
    os.system(readlensfit_args)
