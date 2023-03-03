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
savename = 'precip'                                        # savename 保存路径文价夹名字
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)      #get all times in the file
ntimes = times.shape[0]                                            #number of times in the file

#------------------------------------------------------------------#
# Z = getvar(ncfile,'z').to_numpy()[:,1,1]
RAINC = getvar(ncfile,'RAINC',timeidx=ALL_TIMES).to_numpy()        #
RAINNC = getvar(ncfile,'RAINNC',timeidx=ALL_TIMES).to_numpy()   
RAIN_SUM = RAINC + RAINNC                                          #总降水

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
###降水
_,n,m =  RAINNC.shape

levels = np.arange(0,50,1.5)
x,y= np.meshgrid(range(m),range(n))
for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    sh=ax.contourf(x,y,RAIN_SUM[nt,...],levels=levels,cmap=cmaps.WhBlGrYeRe)
    name = f'CloudHeight_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)

    car = fig.colorbar(sh)
    car.ax.set_title('Rain(mm)',fontsize = 15)

    fig.savefig(f'{savename}/{name}.png',dpi=300)
