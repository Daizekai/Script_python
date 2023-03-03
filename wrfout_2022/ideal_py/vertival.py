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
filename = r'C:\Users\dzk\Desktop\test10\delt5\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)
savename = 'Vertical_delt5'                                                # savename
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)  #get all times in the file
ntimes = times.shape[0]     #number of times in the file

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#计算
def w_mean(W):  #风阔线
    k =  W.shape[0]
    ww = np.zeros((k,))
    for i in range(k):
        tmp = W[i,...]           #单层
        # tmp = tmp[QT[i,...]!=0]
        # print(tmp.shape)
        ww[i] = tmp[tmp>0.5].mean()
    return ww

def max_up_down(W):  #最大垂直速度时间序列
    updraft = W.max(axis=-1).max(axis=-1).max(axis=-1)
    downdraft = W.min(axis=-1).min(axis=-1).min(axis=-1)
    return updraft,downdraft

#------------------------------------------------------------------#
Z = getvar(ncfile,'z').to_numpy()[:,1,1]
W = getvar(ncfile,'W',timeidx=ALL_TIMES).to_numpy()
U = getvar(ncfile,'U',timeidx=ALL_TIMES).to_numpy()
V = getvar(ncfile,'V',timeidx=ALL_TIMES).to_numpy()

W = (W[:,:-1,:,:]+W[:,1:,:,:])/2                                   #插值为标量


#------------------------------------------------------------------#
# import matplotlib as mpl
# bwith = 2 
# mpl.rcParams['axes.spines.top'] = bwith
# mpl.rcParams['axes.spines.bottom'] = bwith
# mpl.rcParams['axes.spines.left'] = bwith
# mpl.rcParams['axes.spines.right'] = bwith
#------------------------------------------------------------------#
# # 垂直速度

for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    ax.plot(w_mean(W[nt,...]),Z/1000,c='b',lw=1.5)
    ax.set_xlim(0,12)
    ax.set_xlabel('Wind Speed(m/s)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)
    name = f'W_SpeedHeight_{times[nt]}min'
    ax.set_title(name,fontsize = 15)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#最大垂直速度时间序列
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot()
updraft,downdraft = max_up_down(W)
ax.plot(times,updraft,c='r',lw=1.5)
ax.plot(times,downdraft,c='b',lw=1.5)
# ax.set_ylim(-10,30)
ax.set_xlabel('Times(min)',fontsize = 20)
ax.set_ylabel('Maximum vertical velocity(m/s)',fontsize = 20)
fig.savefig(f'{savename}/Maximum.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
# # 水平速度
savename = 'UV'                                                # savename
if not os.path.exists(savename):
    os.mkdir(savename)

for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    ax.plot(w_mean(U[nt,...]),Z/1000,c='b',lw=1.5)
    ax.plot(w_mean(V[nt,...]),Z/1000,c='g',lw=1.5,linestyle = "dashed")
    ax.set_xlim(0,30)
    ax.set_xlabel('Wind Speed(m/s)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)
    name = f'UVSpeed_Height_{times[nt]}min'
    ax.set_title(name,fontsize = 15)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)
# print(U.max())