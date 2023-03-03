"""
Created on June 9 23:28 2022

@author: xianyun
"""

# Example script to produce dbz plots for a WRF ideal-data run     ##参考ncl脚本
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
filename = r'C:\Users\dzk\Desktop\test10\delt5\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)
savename = 'vapor_delt5'                                                  # savename 保存路径文价夹名字
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)      #get all times in the file
ntimes = times.shape[0]                                            #number of times in the file
#------------------------------------------------------------------#
###高度
Z = getvar(ncfile,'z').to_numpy()[:,1,1]
###水汽
QV = getvar(ncfile,'QVAPOR',timeidx=ALL_TIMES).to_numpy()*1000     #convert g/kg

###垂直风
W = getvar(ncfile,'W',timeidx=ALL_TIMES).to_numpy()
W = (W[:,:-1,:,:]+W[:,1:,:,:])/2                                   #插值为标量

#------------------------------------------------------------------#
#画图 水汽
_,l,n,m =  QV.shape
levels = np.arange(0,12,1.5)
x,z= np.meshgrid(range(m),Z/1000.)
for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(9,8))
    ax = fig.add_subplot()
    # plt.rcParams['font.family'] = 'YaHei Consolas Hybrid'
    N=1
    cl1=ax.contour(x[::N,::N],z[::N,::N],QV[nt,::N,20,::N],levels=3,linewidths = 1.25,colors='r')
    plt.clabel(cl1 ,  fmt='%.2f',inline=True, fontsize=10)
    sh=ax.contourf(x,z,W[nt,:,20,:],levels= np.arange(-15,35,4),cmap = cmaps.cmp_b2r)

    car = fig.colorbar(sh)
    car.ax.set_ylabel('velocity(m/s)',fontsize = 20)

    ax.set_xlabel('Times(min)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)

    bwith = 2                                                      #画布边框粗细
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)

    name = f'QVAPOR_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#