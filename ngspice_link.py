#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:37:07 2020
@author: louis
"""


import subprocess

# -------------------------------
# The ngspice class and functions
# -------------------------------

# Python class to run and get data from ngspice
class ngspice:
    
    # create ngspice object with the location of the simulator executable,
    # the directory of the circuit file and the circuit file name.
    def __init__(self, cfg):
        self.ngspice_exec = cfg['ngspice']
        self.ckt_dir = cfg['cir_dir']
        self.ckt_file = cfg['cir_file']
        
        self.cli_cmd = [self.ngspice_exec, self.ckt_dir + self.ckt_file]
        
    # explicitly run the ngspice simulator
    def run_ngspice(self):
        print('Running the command:')
        print(self.cli_cmd)
        print('')
        
        process = subprocess.Popen(self.cli_cmd, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        print(stdout.decode('utf-8'))
        # uncomment the line below to see error messages
        print(stderr.decode('utf-8'))
        
        return stdout, stderr
        
    # read the data written by the 'wrdata' command after a dc analysis
    # index_list = [1, 3, 5, ...] since the even indices are the sweep_var values
    def read_dc_analysis(self, dc_data_file, index_list):
        sweep_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(dc_data_file, 'r') as f:
            for line in f:
                sweep_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val]))
                    
        return sweep_var, data_array
    
    # read the data written by the 'wrdata' command after a transient analysis
    # index_list = [1, 3, 5, ...] since the even indices are the time_var values
    def read_tran_analysis(self, tran_data_file, index_list):
        time_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(tran_data_file, 'r') as f:
            for line in f:
                time_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val]))
                    
        return time_var, data_array
    
    # read the data written by the 'wrdata' command after an ac analysis
    # index_list = [[1,2], [4,5], ...] for the real and imaginary components
    # the indices 0, 3, 6, 9, ... are the values of freq_var
    def read_ac_analysis(self, ac_data_file, index_list):
        freq_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(ac_data_file, 'r') as f:
            for line in f:
                freq_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val[0]]) + \
                        float(line.split()[val[1]]) * 1j)
                    
        return freq_var, data_array
    
# -------------------------
# Plotting helper functions
# -------------------------

# label a plot
def label_plot(plt_cfg, fig, ax):
    # ax.grid(True)
    ax.grid(True, linewidth=0.5, color='gray')
    ax.grid(linestyle=plt_cfg['grid_linestyle'])
    ax.set_title(plt_cfg['title'])
    ax.set_xlabel(plt_cfg['xlabel'])
    ax.set_ylabel(plt_cfg['ylabel'])
    if plt_cfg['add_legend']:
        ax.legend(loc=plt_cfg['legend_loc'], title=plt_cfg['legend_title'])
    fig.set_tight_layout('True')
    
# add a vertical line with text annotation
def add_vline_text(ax, xd, ypos, txt_label):
    ax.axvline(x=xd, color='gray', linestyle='-.', linewidth=1)
    ax.text(xd, ypos, txt_label, \
        rotation=90, color='black', \
        horizontalalignment='right', verticalalignment='bottom')
    
# add a horizontal line with text annotation
def add_hline_text(ax, yd, xpos, txt_label):
    ax.axhline(y=yd, color='gray', linestyle='-.', linewidth=1)
    ax.text(xpos, yd, txt_label,\
        rotation=0, color='black', \
        horizontalalignment='left', verticalalignment='bottom')
    
# -----------------------
# Miscellaneous functions
# -----------------------

# calculate the index and closest value (in a list) to a given number
def find_in_data(data, value):
    index, closest = min(enumerate(data), key=lambda x: abs(x[1] - value))
    
    return index, closest
    
# scale a vector or list by f
def scale_vec(value, f):       
    return [v/f for v in value]
