__author__ = 'Ian Fenech Conti'

import numpy as np
import matplotlib.pyplot as plt


def get_outer_iteration(iteration, data):
    res = []

    for i in data:
        if int(i[1]) == iteration:
            res.append(i)

    res = np.array(res)

    return res

log_file = '/home/ian/Documents/GREAT03/log.all.log'

with open(log_file) as f:
    content = f.readlines()

results = []

for line in content:
    if 'solve-psf:' in line:
        results.append(line.rstrip().split(':')[1].split(','))

timings = np.array(results)

timings_1_x = []
timings_1_y = []
stars_tile_1 = 0

for x in range(1, 19):
    outer_loop = 0
    outer_iter = 0
    for entry in timings:
        if int(entry[1]) == x:
            outer_loop += float(entry[3])
            outer_iter = entry[1]
            stars_tile_1 = int(entry[0])
    timings_1_x.append(x)
    timings_1_y.append(outer_loop)

# SECOND FILE
log_file = '/home/ian/Documents/GREAT03/log.1000.log'
with open(log_file) as f:
    content = f.readlines()

results = []

for line in content:
    if 'solve-psf:' in line:
        results.append(line.rstrip().split(':')[1].split(','))

timings = np.array(results)

timings_2_x = []
timings_2_y = []
stars_tile_2 = 0

for x in range(1, 19):
    outer_loop = 0
    outer_iter = 0
    for entry in timings:
        if int(entry[1]) == x:
            outer_loop += float(entry[3])
            outer_iter = entry[1]
            stars_tile_2 = int(entry[0])
    timings_2_x.append(x)
    timings_2_y.append(outer_loop*(stars_tile_1/stars_tile_2))

# THIRD FILE
log_file = '/home/ian/Documents/GREAT03/log.150.log'
with open(log_file) as f:
    content = f.readlines()

results = []

for line in content:
    if 'solve-psf:' in line:
        results.append(line.rstrip().split(':')[1].split(','))

timings = np.array(results)

timings_3_x = []
timings_3_y = []
stars_tile_3 = 0

for x in range(1, 19):
    outer_loop = 0
    outer_iter = 0
    for entry in timings:
        if int(entry[1]) == x:
            outer_loop += float(entry[3])
            outer_iter = entry[1]
            stars_tile_3 = int(entry[0])
    timings_3_x.append(x)
    timings_3_y.append(outer_loop*(stars_tile_1/stars_tile_3))

time_1_total = 0
time_2_total = 0
time_3_total = 0

for i, time in enumerate(timings_1_y):
    time_1_total += time
    time_2_total += timings_2_y[i]
    time_3_total += timings_3_y[i]

speed_up = ((time_1_total/time_2_total))

print 'original run : %s' % (round(time_1_total/(60*60), 2))
print 'run (%d in tile) : %s, speed-up : %f' % (stars_tile_2, round(time_2_total/(60*60), 2), (time_1_total/time_2_total))
print 'run (%d in tile) : %s, speed-up : %f' % (stars_tile_3, round(time_3_total/(60*60), 2), (time_1_total/time_3_total))

plt.xlim([0, 19])
plt.scatter(timings_1_x, timings_1_y, c='black', label='%d stars/tile' % stars_tile_1)
plt.scatter(timings_2_x, timings_2_y, c='green', label='%d stars/tile, speed up : %0.2fx' % (stars_tile_2, round((time_1_total/time_2_total),2)))
plt.scatter(timings_3_x, timings_3_y, c='red', label='%d stars/tile, speed up : %0.2fx' % (stars_tile_3, round((time_1_total/time_3_total),2)))
plt.legend(loc=2)
plt.xlabel('Outer Iteration (i)')
plt.ylabel('Time Taken (s)')
plt.title('Sub-tile Timing')
plt.show()

