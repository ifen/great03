__author__ = 'Ian Fenech Conti'

import os
import re

RANGE_START = 0
RANGE_END = 200

GALAXIES_PROCESSED = 0
WEIGHTED_CORRECTION = 0

great3_folder_root = '/home/ian/Documents/GREAT03/'
lensfit_folder_root = '/home/ian/Downloads/correction_code/'

galaxies_proc = []

fo = open("/home/ian/Documents/GREAT03/sub_5.txt", "wb")

for ID in range(RANGE_START, RANGE_END):
    log_path = '%sdata/submission_4/outputs/%d/out4.log' % (great3_folder_root, ID)
    shakes = open(log_path, "r")
    print '  processing bias on field %d' % ID

    for line in shakes:
    	if GALAXIES_PROCESSED:
    		if re.match("(.*)galaxies used(.*)", line):
        		# get the number of galaxies processed.
        		galaxies = int(line.split()[0])
            		galaxies_proc.append(galaxies)
    	
    	elif WEIGHTED_CORRECTION:
        	if re.match("(.*)weighted correction factor applied(.*)", line):
        		# get the weighted correction factor.
        		wcf = line.split()[4]
            		fo.write('%03d %s\n' % (ID, wcf))
        else:
        	if re.match("(.*)mean weighted, corrected shear(.*)", line):      	
			# g1 and g2.
		     	g1 = line.split()[4]
		     	g2 = line.split()[5]
		     	fo.write('%03d %s %s\n' % (ID, g1, g2))
		     	
     
fo.close()

if GALAXIES_PROCESSED:
	print 'galaxy stats'
	print max(galaxies_proc)
	print min(galaxies_proc)
	print reduce(lambda x, y: x + y, galaxies_proc) / len(galaxies_proc)
