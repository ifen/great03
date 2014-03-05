__author__ = 'Ian Fenech Conti'

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime

sys.path.append('~/great03/')

if len(sys.argv) < 2:
    print 'missing args'
    exit()

order = sys.argv[1]
log_name = sys.argv[2]
root_path = sys.argv[3]
lensfit_path = sys.argv[4]

os.environ['SWARP_CONFIG'] = lensfit_path + 'swarp/create_coadd_swarp.swarp'
os.environ['HEAD_DIR'] = root_path
os.environ['PSF_DIR'] = root_path
os.environ['CATALOGUE_STARS'] = root_path + '00.asc'
os.environ['DATA_DIR'] = root_path
os.environ['SAVE_NAME'] = '00'

print 'env. variables set'

makeopsf_exec = './makeospsf %sinput.asc %s none 30 > %s%s' % (root_path, order, root_path, log_name)
#makeopsf_exec = './makeospsf %sfile_list.asc %s none 30' % (root_path, order)
log_file = '%s%s' % (root_path, log_name)
source_path = '%ssrc/' % lensfit_path

if os.path.isfile(log_file):
    os.remove(log_file)

print 'running makeospsf code'
print strftime("%Y-%m-%d %H:%M:%S", gmtime())

os.chdir(source_path)
os.system(makeopsf_exec)

# print '\nreading results'
#
# with open(log_file) as f:
#     content = f.readlines()
#
# results = []
#
# for line in content:
#     if 'solve-psf:' in line:
#         results.append(line.rstrip().split(':')[1].split(','))
#
# timings = np.array(results)
#
# plt.figure()
# plt.xlim([0, 14])
# plt.plot(timings[:, 2], timings[:, 3], 'bo', markersize=5)
# plt.xlabel('Inner Iteration (i)')
# plt.ylabel('Time Taken (s)')
# plt.title('Lensfit Analysis')
# plt.show()
#
# print 'running makeospsf done'