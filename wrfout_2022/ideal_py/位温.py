"""
Created on June 9 21:05 2022

@author: xianyun
"""

# Example script to produce dbz plots for a WRF ideal-data run
from fileinput import filename
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from wrf import getvar, ALL_TIMES,extract_times
import cmaps
import os

#begin--------------------------------------------------------------#
# The WRF ARW input file.  
# This needs to have a ".nc" appended, so just do it.
# a = addfile("../wrfout_d01_2000-01-24_12:00:00.nc","r")
filename = r'C:\Users\dzk\Desktop\test10\delt3\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)
savename = 'Theta'                                                # savename
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)  #get all times in the file
ntimes = times.shape[0]     #number of times in the file

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
Z = getvar(ncfile,'z').to_numpy()[:,1,1]
theta = getvar(ncfile,'th',units='degC',timeidx=ALL_TIMES).to_numpy()
tc = getvar(ncfile,'tc',timeidx=ALL_TIMES).to_numpy()
# print(theta.max())
#------------------------------------------------------------------#
# # 位温随高度

for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    ax.plot(theta[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='b',lw=1.5)
    # ax.set_xlim(0,12)
    
    ax.set_xlabel('Theta(degC)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)
    name = f'Theta_Height_{times[nt]}min'
    ax.set_title(name,fontsize = 15)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
# # 温度随高度

# for nt in range(ntimes):
#     print(f"Working on time: {times[nt]}")
#     fig = plt.figure(figsize=(10,8))
#     ax = fig.add_subplot()

#     ax.plot(tc[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='b',lw=1.5)
#     # ax.set_xlim(0,12)
    
#     ax.set_xlabel('T(degC)',fontsize = 20)
#     ax.set_ylabel('Height(km)',fontsize = 20)
#     name = f'T_Height_{times[nt]}min'
#     ax.set_title(name,fontsize = 15)
#     ax.tick_params(direction='out', length=8,labelsize=20)

#     fig.savefig(f'{savename}/{name}.png',dpi=300)