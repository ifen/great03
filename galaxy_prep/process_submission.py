__author__ = 'Ian Fenech Conti'

import os
import re

RANGE_START = 0
RANGE_END = 200

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Downloads/correction_code/'

weighted_correction = []

fo = open("/home/ian/Documents/GREAT03/sub_2.txt", "wb")

for ID in range(RANGE_START, RANGE_END):
    log_path = '%soutputs_final/%d/out.log' % (great3_folder_root, ID)
    shakes = open(log_path, "r")

    for line in shakes:
        if re.match("(.*)mean weighted, corrected shear(.*)", line):
            #print
            #val = re.findall("\d+.\d+", line)
            #weighted_correction.append('%s %s' % (val[0], val[1]))
            g1 = line.split()[4]
            g2 = line.split()[5]
            #print '%s %s' % (g1, g2)
            #if tmp < 9950:
                #print ' **WARNING : %d with %d galaxies ' % (ID, tmp)
            #weighted_correction.append(tmp)
            fo.write('%03d %s %s\n' % (ID, g1, g2))
            # print val[0]

    # print max(weighted_correction)

fo.close()

    # for line in shakes:
    #     # if re.match("(.*)corrected shear(.*)", line):
    #     print line,
#print weighted_correction
#print max(weighted_correction)
#print min(weighted_correction)
#print reduce(lambda x, y: x + y, weighted_correction) / len(weighted_correction)