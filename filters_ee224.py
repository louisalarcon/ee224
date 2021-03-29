# -*- coding: utf-8 -*-
"""
Spyder Editor

LPA 01-Mar-2021
"""

import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np

# define a convenient class and functions for filters
class ee224:
    
    def __init__ (self):
        return
                  
    # get the frequency rsponse from the poles, zeros, and gain of an LTI system
    def get_freq_resp(self, sys, num_pts):
        x = np.logspace(-2, 2, num_pts, endpoint=True)
        w, mag, phase = signal.bode(sys, x)         # use the signal.bode function
        gd = -np.gradient(phase * np.pi/180, w)     # calculate group delay as well
        return w, mag, phase, gd
    
    # get the Butterworth filter response
    def proto_butter_LPF(self, N, num_pts):
        sys_lpf = signal.butter(N, 1, btype='low', analog=True, output='zpk', fs=None)
        w, mag, phase, gd = self.get_freq_resp(sys_lpf, num_pts)
        return w, mag, phase, gd, sys_lpf
    
    # get the Chebyshev-I filter response
    def proto_cheby1_LPF(self, N, num_pts, pb_ripple_dB):
        sys_lpf = signal.cheby1(N, pb_ripple_dB, 1, btype='low', analog=True, output='zpk', fs=None)
        w, mag, phase, gd = self.get_freq_resp(sys_lpf, num_pts)
        return w, mag, phase, gd, sys_lpf
    
    # get the Chebyshev-II filter response
    def proto_cheby2_LPF(self, N, num_pts, sb_ripple_dB):
        # adjusted since w0 is defined differently (referred to the stop-band)
        sys_lpf = signal.cheby2(N, sb_ripple_dB, 1.62, btype='low', analog=True, output='zpk', fs=None)
        w, mag, phase, gd = self.get_freq_resp(sys_lpf, num_pts)
        return w, mag, phase, gd, sys_lpf
    
    # get the Elliptic filter response
    def proto_elliptic_LPF(self, N, num_pts, pb_ripple_dB, sb_ripple_dB):
        sys_lpf = signal.ellip(N, pb_ripple_dB, sb_ripple_dB, 1, btype='low', analog=True, output='zpk', fs=None)
        w, mag, phase, gd = self.get_freq_resp(sys_lpf, num_pts)
        return w, mag, phase, gd, sys_lpf
    
    # get the Bessel filter response
    def proto_bessel_LPF(self, N, num_pts):
        sys_lpf = signal.bessel(N, 1, btype='low', analog=True, output='zpk', norm='mag', fs=None)
        w, mag, phase, gd = self.get_freq_resp(sys_lpf, num_pts)
        return w, mag, phase, gd, sys_lpf
            
    # create a single function with the filter family as input parameter (so we can loop)
    def filter_proto(self, family, N, num_pts, pb_ripple_dB, sb_ripple_dB):        
        w, mag, phase, gd, sys_lpf = {
            'Butterworth'   : self.proto_butter_LPF(N, num_pts),
            'Chebyshev-I'   : self.proto_cheby1_LPF(N, num_pts, pb_ripple_dB),
            'Chebyshev-II'  : self.proto_cheby2_LPF(N, num_pts, sb_ripple_dB),
            'Elliptic'      : self.proto_elliptic_LPF(N, num_pts, pb_ripple_dB, sb_ripple_dB),
            'Bessel'       : self.proto_bessel_LPF(N, num_pts)
            }[family]
        return w, mag, phase, gd, sys_lpf
        
    # function to label plots
    def label_plot(self, plt_cfg, fig, ax):
        ax.grid(linestyle=plt_cfg['grid_linestyle'])
        ax.grid(True, linewidth=0.5, color='gray')
        ax.set_title(plt_cfg['title'])
        ax.set_xlabel(plt_cfg['xlabel'])
        ax.set_ylabel(plt_cfg['ylabel'])
        if plt_cfg['add_legend']:
            ax.legend(loc=plt_cfg['legend_loc'], title=plt_cfg['legend_title'])
        fig.set_tight_layout('True')
        
    # function to add a vertical marker
    def add_vline_text(self, ax, xd, ypos, txt_label):
        ax.axvline(x=xd, color='black', linestyle='-.', linewidth=1)
        ax.text(xd, ypos, txt_label, \
            rotation=90, color='black', \
            horizontalalignment='right', verticalalignment='bottom')
        
    # function to add a horizontal marker
    def add_hline_text(self, ax, yd, xpos, txt_label):
        ax.axhline(y=yd, color='black', linestyle='-.', linewidth=1)
        ax.text(xpos, yd, txt_label,\
            rotation=0, color='black', \
            horizontalalignment='left', verticalalignment='bottom')
      
    # function to search for the index of a desired value (closest)
    def find_in_data(self, data, value):
        index, closest = min(enumerate(data), key=lambda x: abs(x[1] - value))
        return index, closest
           
# ----------------------
# define filters to plot
# ----------------------

family = ['Butterworth', 'Chebyshev-I', 'Chebyshev-II', 'Elliptic', 'Bessel']

pb_ripple = 3       # pass-band ripple (for filters that need it)
sb_ripple = 40      # minimum stop-band attentiation (if needed)
    
Nord = 5            # filter order
Npts = 10000        # number of frequency response points

# ----------------------
# define plot parameters
# ----------------------

# Setup the magnitude response plot
plt_cfg1 = {
        'grid_linestyle' : 'dotted',
        'title' : r'Magnitude Response',
        'xlabel' : r'Frequency [rad/s]',
        'ylabel' : r'Magnitude [dB]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : 'N = {}'.format(Nord)
        }

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)

# Setup the phase response plot
plt_cfg2 = {
        'grid_linestyle' : 'dotted',
        'title' : r'Phase Response',
        'xlabel' : r'Frequency [rad/s]',
        'ylabel' : r'Phase [degrees]',
        'legend_loc' : 'lower left',
        'add_legend' : True,
        'legend_title' : 'N = {}'.format(Nord)
        }

fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)

# Setup the group delay plot
plt_cfg3 = {
        'grid_linestyle' : 'dotted',
        'title' : r'Group Delay',
        'xlabel' : r'Frequency [rad/s]',
        'ylabel' : r'Group Delay [seconds]',
        'legend_loc' : 'upper right',
        'add_legend' : True,
        'legend_title' : 'N = {}'.format(Nord)
        }

fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)

# Setup the pole-zero plot
plt_cfg4 = {
        'grid_linestyle' : 'dotted',
        'title' : r'Pole-Zero Plot',
        'xlabel' : r'$\sigma$',
        'ylabel' : r'$j\omega$',
        'legend_loc' : 'upper right',
        'add_legend' : True,
        'legend_title' : 'N = {}'.format(Nord)
        }

fig4 = plt.figure()
ax4 = fig4.add_subplot(1, 1, 1)

# Setup the step response plot
plt_cfg5 = {
        'grid_linestyle' : 'dotted',
        'title' : r'Step Response',
        'xlabel' : r'Time [s]',
        'ylabel' : r'Output [V]',
        'legend_loc' : 'lower right',
        'add_legend' : True,
        'legend_title' : 'N = {}'.format(Nord)
        }

fig5 = plt.figure()
ax5 = fig5.add_subplot(1, 1, 1)

# additional pole-zero plot settings
msize = 5           # marker size
mewidth = 1.5       # marker edge width

# ------------------------------------------------------------- 
# Use the 'scipy.signal' module to generate the filter response
# ------------------------------------------------------------- 

F = ee224()                         # create a filter class
T = np.arange(0, 50, 50/10000)      # define the time vector for the step response

# Generate the filter characteristic plots
for f in family:
    
    # get the filter frequency response
    w, mag, phase, gd, sys_lpf = F.filter_proto(f, Nord, Npts, pb_ripple, sb_ripple)
    
    # get the filter step response
    t, y = signal.step(sys_lpf, T=T)

    # magnitude plot
    ax1.semilogx(w, mag, '-', label = f + r' LPF')
    
    # phase plot
    ax2.semilogx(w, phase, '-', label = f + r' LPF')
    
    # group delay plaot
    ax3.semilogx(w, gd, '-', label = f + r' LPF')

    # plot the poles
    p = ax4.plot(np.real(sys_lpf[1]), np.imag(sys_lpf[1]), 'x', \
        markerfacecolor = 'none', markersize = msize, markeredgewidth=mewidth, \
        label = f + r' Poles')

    # plot the zeros
    ax4.plot(np.real(sys_lpf[0]), np.imag(sys_lpf[0]), 'o', color = p[-1].get_color(), \
        markerfacecolor = 'none', markersize = msize, markeredgewidth=mewidth, \
        label = f + r' Zeros')

    # step response plot
    ax5.plot(t, y, label = f + r' LPF')
    
# Adjust the plot limits for readability
ax3.set_ylim((-5, 40))
ax4.set_ylim((-3, 3))
ax4.set_xlim((-2, 6))
ax4.set_aspect('equal', adjustable='box')

# draw the unit circle
theta = np.arange(0, 360, 1) * np.pi/180
xc = np.cos(theta)
yc = np.sin(theta)
ax4.plot(xc, yc, ':', color = 'gray', linewidth=1)

# add vertical and horizontal labels
F.add_vline_text(ax1, 1, -100, '')              # add a marker for w0 (magnitude response)
idx, wo = F.find_in_data(w, 1)                  # find the index for w = w0
mag_wo = mag[idx]                               # get the -3dB point
txt_label = '{:.2f} dB'.format(mag_wo)
F.add_hline_text(ax1, mag_wo, 10, txt_label)    # add a marker at -3dB (magnitude response)
F.add_vline_text(ax2, 1, -200, '')              # add a marker for w0 (phase response)
F.add_vline_text(ax3, 1, 0, '')                 # add a marker for w0 (group delay plot)

# label the plots
F.label_plot(plt_cfg1, fig1, ax1)
F.label_plot(plt_cfg2, fig2, ax2)
F.label_plot(plt_cfg3, fig3, ax3)
F.label_plot(plt_cfg4, fig4, ax4)
F.label_plot(plt_cfg5, fig5, ax5)

# save the figures as SVG
fig1.savefig('filters_mag.svg')
fig2.savefig('filters_phase.svg')
fig3.savefig('filters_group_delay.svg')
fig4.savefig('filters_pz_plot.svg')
fig5.savefig('filters_step_response.svg')


