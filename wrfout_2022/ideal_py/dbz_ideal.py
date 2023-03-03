"""
Created on June 9 20:30 2022

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
#begin
# The WRF ARW input file.  
# This needs to have a ".nc" appended, so just do it.
# a = addfile("../wrfout_d01_2000-01-24_12:00:00.nc","r")
filename = r'C:\Users\dzk\Desktop\test10\delt3\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)

savename = 'Reflectivity1'
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)  #get all times in the file
ntimes = times.shape[0]     #number of times in the file

#------------------------------------------------------------------#
#------------------------------------------------------------------#
dbz = getvar(ncfile,'dbz',timeidx=ALL_TIMES).to_numpy()            # time*lev*x*y
_,l,n,m =  dbz.shape
dbz[dbz<0]=0.
#------------------------------------------------------------------#
#水平dbz
#
x,y= np.meshgrid(range(m),range(n))

k=5                                                                #层数

for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    levels = np.arange(5,75,5)
    sh=ax.contourf(x,y,dbz[nt,k,:,:],levels=levels,cmap=cmaps.radar)

    name = f'Reflectivity_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)
    
    car = fig.colorbar(sh)
    car.ax.set_title('dbz',fontsize = 20)


    fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#
# #垂直dbz
# dbz = getvar(ncfile,'dbz',timeidx=ALL_TIMES).to_numpy()            # time*lev*y*x
# _,l,n,m =  dbz.shape
# dbz[dbz<0]=0.
# x,z= np.meshgrid(range(m),range(l))
# for nt in range(ntimes):
#     print(f"Working on time: {times[nt]}")

#     fig = plt.figure(figsize=(10,8))
#     ax = fig.add_subplot()

#     levels = np.arange(5,75,5)
#     tmp = dbz[nt,:,:,:].mean(axis=-2)
#     sh=ax.contourf(x,z,tmp,levels=levels,cmap=cmaps.radar)

#     name = f'ver_Reflectivity_{times[nt]}min'
#     ax.set_title(name,fontsize = 20)
#     ax.tick_params(direction='out', length=8,labelsize=20)
    
#     car = fig.colorbar(sh)
#     car.ax.set_title('dbz',fontsize = 20)


#     fig.savefig(f'{savename}/{name}.png',dpi=300)

