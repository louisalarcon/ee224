#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:17:07 2021

@author: louis
"""

import os
import matplotlib.pyplot as plt
import numpy as np

import ngspice_link as ngl

# setup the simulation configuration
cfg = {
        'ngspice' : '/Applications/ngspice/bin/ngspice', 
        'cir_dir' : '/Users/louis/Documents/UPEEEI/Classes/EE 224/git/ee224/',
        'cir_file' : 'butter_lpf_5.sp',
        }

# create the ngspice object
sim1 = ngl.ngspice(cfg)

# data file from ngspice (generated by the wrdata command)
dfile = '/Users/louis/Documents/UPEEEI/Classes/EE 224/git/ee224/butter_lpf_5.dat'
if os.path.isfile(dfile):
    os.remove(dfile)

# run ngspice with the configuration above
sim1.run_ngspice()

# read simulation data
index_list = [[1, 2]]
f, [v_o] = sim1.read_ac_analysis(dfile, index_list)  

vo_mag = np.abs(v_o)
vo_mag_db = 20*np.log10(vo_mag)

ix1, f1 = ngl.find_in_data(f, 10e6)
ix2, f2 = ngl.find_in_data(f, 20e6)


plt_cfg = {
        'grid_linestyle' : 'dotted',
        'title' : r'5th Order Low-Pass Butterworth Filter',
        'xlabel' : r'Frequency [Hz]',
        'ylabel' : r'Magnitude [dB]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : None
        }

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.semilogx(f, vo_mag_db, '-', label = r'$v_o$')

ngl.add_vline_text(ax, 10e6, -55, '10 MHz')
ngl.add_vline_text(ax, 20e6, -55, '20 MHz')

ngl.add_hline_text(ax, 20*np.log10(vo_mag[0]), 2.5e7, '{:.2f} dB'.format(20*np.log10(vo_mag[0])))

ngl.add_hline_text(ax, 20*np.log10(vo_mag[ix1]), 2.5e7, '{:.2f} dB'.format(20*np.log10(vo_mag[ix1])))
ngl.add_hline_text(ax, 20*np.log10(vo_mag[ix2]), 2.5e7, '{:.2f} dB'.format(20*np.log10(vo_mag[ix2])))

ax.set_ylim((-60, 0))

ngl.label_plot(plt_cfg, fig, ax)
plt.savefig('butter_lpf_5.svg')

