# -*- coding: utf-8 -*-
'''
IGCViewer.py

Copyright (c) 2016 Hiraku Toida

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''

'''
Data plot script in *.igc file.
'''

import os.path
import datetime
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import IGCProcessor

# parse the options
parser = argparse.ArgumentParser(description = 'Data plot script in *.igc file.')
parser.add_argument('filename', \
        action = 'store', \
        nargs = None, \
        const = None, \
        default = None, \
        type = str, \
        choices = None, \
        help = 'Filename of the *.igc file to be converted.', \
        metavar = None)
parser.add_argument('-s', '--start-gnss-time', \
        action = 'store', \
        nargs = '?', \
        const = None, \
        default = None, \
        type = str, \
        choices = None, \
        help = 'Plot starting time. Format: HHMMSS', \
        metavar = None)
parser.add_argument('-e', '--end-gnss-time', \
        action = 'store', \
        nargs = '?', \
        const = None, \
        default = None, \
        type = str, \
        choices = None, \
        help = 'Plot ending time. Format: HHMMSS', \
        metavar = None)
args = parser.parse_args()
start_gnss_time = args.start_gnss_time
end_gnss_time = args.end_gnss_time

# read the file
filename = args.filename
root, ext = os.path.splitext(filename)
f = open(filename)
lines = f.readlines()
f.close()

igc = IGCProcessor.IGCProcess()
igc.process_lines(lines)

# process 'A'
print("***** A *****")
igc.rec_a.print_payload()

# process 'B'
igc.rec_b.line2dat()
dat_B = igc.rec_b.dat
time_B = igc.rec_b.time
gps_valid = igc.rec_b.gps_valid

# process 'E'
print("***** E *****")
igc.rec_e.print_payload()

# process 'F'
igc.rec_f.line2dat()
dat_F = igc.rec_f.dat
time_F = igc.rec_f.time

# process 'G'
print("***** G *****")
igc.rec_g.print_payload()

# process 'H'
print("***** H *****")
igc.rec_h.print_payload()
igc.rec_h.get_date()
print(igc.rec_h.date)

# process 'I'
print("***** I *****")
igc.rec_i.print_payload()

# process 'L'
print("***** L *****")
igc.rec_l.print_payload()

# plot the data
if start_gnss_time != None:
    plot_x_min = datetime.datetime.strptime(start_gnss_time, "%H%M%S")
else:
    plot_x_min_float = np.min([np.min(dat_B[gps_valid,0]), np.min(dat_F[:,0])])
    plot_x_min = datetime.datetime.strptime(str(int(plot_x_min_float)), "%H%M%S")

if end_gnss_time != None:
    plot_x_max = datetime.datetime.strptime(end_gnss_time, "%H%M%S")
else:
    plot_x_max_float = np.max([np.max(dat_B[gps_valid,0]), np.max(dat_F[:,0])])
    plot_x_max = datetime.datetime.strptime(str(int(plot_x_max_float)), "%H%M%S")

matplotlib.rcdefaults()
style = ['bmh', 'classic', 'dark_background', 'fivethirtyeight', 'ggplot', 'grayscale']
#seabone_style = ['seaborn-bright', 'seaborn-colorblind', 'seaborn-dark',
#                 'seaborn-darkgrid', 'seaborn-dark-palette', 'seaborn-deep',
#                 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
#                 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk',
#                 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid']
plt.style.use(style[0]) # 0-5
#plt.style.use(seabone_style[14])    # 0-14
figsize = (24, 13.5)
dpi = 100

formatter = matplotlib.dates.DateFormatter('%H:%M:%S')

fig1 = plt.figure("1", figsize = figsize)
fig1.subplots_adjust(hspace = 0.0)
ax1_1 = plt.subplot(2,1,1)
ax1_1.plot_date(time_B, dat_B[gps_valid,1], '-')
ax1_1.set_ylabel('Latitude (deg.)')
ax1_1.get_yaxis().get_major_formatter().set_useOffset(False)
ax1_2 = plt.subplot(2,1,2, sharex=ax1_1)
ax1_2.plot_date(time_B, dat_B[gps_valid,2], '-')
ax1_2.set_xlim([plot_x_min, plot_x_max])
ax1_2.set_ylabel('Longitude (deg.)')
ax1_2.set_xlabel("Time")
ax1_2.get_xaxis().set_major_formatter(formatter)
ax1_2.get_yaxis().get_major_formatter().set_useOffset(False)
fig1.savefig(root + "_1.png", dpi = dpi)

figT = plt.figure("Trajectory", figsize = figsize)
ax = plt.subplot(1,1,1)
ax.plot(dat_B[gps_valid,2], dat_B[gps_valid,1], '-')
ax.set_xlabel('Longitude (deg.)')
ax.set_ylabel('Latitude (deg.)')
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.get_yaxis().get_major_formatter().set_useOffset(False)
figT.savefig(root + "_T.png", dpi = dpi)

fig2 = plt.figure("2", figsize = figsize)
fig2.subplots_adjust(hspace = 0.0)
ax2_1 = plt.subplot(3,1,1)
ax2_1.plot_date(time_B[1:], dat_B[gps_valid[1:],4] - dat_B[gps_valid[1],4], '-', label = "Pressure")
ax2_1.plot_date(time_B[1:], dat_B[gps_valid[1:],5] - dat_B[gps_valid[1],5], '-', label = "GNSS")
ax2_1.set_ylabel('Altitude (m)')
ax2_1.legend(loc = 'best')
ax2_2 = plt.subplot(3,1,2, sharex=ax2_1)
ax2_2.plot_date(time_B, dat_B[gps_valid,8] / 360, '-')
ax2_2.set_ylabel("Ground Speed (m/s)")
ax2_3 = plt.subplot(3,1,3, sharex=ax2_1)
ax2_3.plot_date(time_B, np.rad2deg(np.unwrap(np.deg2rad(dat_B[gps_valid,9]))), '-')
ax2_3.set_xlim([plot_x_min, plot_x_max])
ax2_3.set_ylabel("Heading (deg.)")
ax2_3.set_xlabel("Time")
ax2_3.get_xaxis().set_major_formatter(formatter)
fig2.savefig(root + "_2.png", dpi = dpi)

fig3 = plt.figure("3", figsize = figsize)
fig3.subplots_adjust(hspace = 0.0)
ax3_1 = plt.subplot(3,1,1)
ax3_1.plot_date(time_B, dat_B[gps_valid,6], '-')
ax3_1.set_ylabel("Fix Accuracy (m)")
ax3_2 = plt.subplot(3,1,2, sharex=ax3_1)
ax3_2.plot_date(time_B, dat_B[gps_valid,7], '-')
ax3_2.set_ylabel("Environmental Noise inside FR")
ax3_3 = plt.subplot(3,1,3, sharex=ax3_1)
ax3_3.plot_date(time_F, np.sum(dat_F[:,1:], axis = 1), 'o-')
ax3_3.set_xlim([plot_x_min, plot_x_max])
ax3_3.get_xaxis().set_major_formatter(formatter)
ax3_3.set_ylabel('Number of satellites')
ax3_3.set_xlabel("Time")
fig3.savefig(root + "_3.png", dpi = dpi)

plt.show()
